"""
Billing Services
Lógica de negócio para billing e pagamentos
"""
import logging
from decimal import Decimal
from datetime import timedelta, date
from typing import Optional, Tuple, Literal
from django.db import transaction
from django.utils import timezone
from django.core.exceptions import ValidationError
from .models import Plan, Subscription, Invoice, Payment, PaymentMethod
from .gateway.asaas import AsaasGatewayService
from .gateway.stripe import StripeGatewayService
from apps.tenants.models import Tenant

logger = logging.getLogger(__name__)


GatewayType = Literal['asaas', 'stripe']


def get_gateway_service(gateway: GatewayType):
    """
    Retorna a implementação correta de gateway
    """
    if gateway == 'stripe':
        return StripeGatewayService()
    # Default: Asaas
    return AsaasGatewayService()


class BillingService:
    """Serviço para gerenciar billing"""
    
    @staticmethod
    def get_plan_price_for_tenant(plan: Plan, tenant: Tenant, billing_cycle: str = 'monthly') -> Decimal:
        """
        Retorna o preço do plano baseado no país do tenant
        
        Args:
            plan: Instância do plano
            tenant: Instância do tenant
            billing_cycle: 'monthly' ou 'yearly'
            
        Returns:
            Preço em Decimal
        """
        return plan.get_price_for_country(tenant.country, billing_cycle)
    
    @staticmethod
    @transaction.atomic
    def create_subscription(
        tenant: Tenant,
        plan: Plan,
        payment_method: Optional[PaymentMethod] = None,
        billing_cycle: str = 'monthly'
    ) -> Subscription:
        """
        Cria uma nova assinatura
        
        Args:
            tenant: Instância do tenant
            plan: Instância do plano
            payment_method: Método de pagamento (opcional)
            billing_cycle: 'monthly' ou 'yearly'
            
        Returns:
            Subscription criada
            
        Raises:
            ValidationError: Se já existe assinatura ativa ou plano inválido
        """
        # Verificar se já existe assinatura ativa
        if hasattr(tenant, 'subscription') and tenant.subscription.is_active:
            raise ValidationError('Tenant já possui uma assinatura ativa')
        
        # Validar se plano está ativo
        if not plan.is_active:
            raise ValidationError('Plano não está ativo')
        
        # Validar se plano tem preço para o país do tenant
        price = BillingService.get_plan_price_for_tenant(plan, tenant, billing_cycle)
        if price <= 0:
            raise ValidationError(f'Plano não possui preço configurado para o país {tenant.country}')
        
        # Determinar gateway
        if payment_method:
            gateway = payment_method.gateway
        else:
            gateway = 'asaas' if tenant.country == 'BR' else 'stripe'
        
        # Calcular período
        today = timezone.now().date()
        if billing_cycle == 'yearly':
            period_end = today + timedelta(days=365)
        else:
            period_end = today + timedelta(days=30)

        status = 'active'
        if plan.trial_days > 0 and payment_method is None:
            status = 'trialing'

        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            payment_method=payment_method,
            gateway=gateway,
            status=status,
            current_period_start=today,
            current_period_end=period_end,
        )

        if status == 'trialing':
            subscription.trial_start = today
            subscription.trial_end = today + timedelta(days=plan.trial_days)
            subscription.save(update_fields=['trial_start', 'trial_end'])
        
        # Vincular identificadores do gateway já existentes
        gateway_customer_map = {
            'stripe': getattr(tenant, 'stripe_customer_id', None),
            'asaas': getattr(tenant, 'asaas_customer_id', None),
        }
        gateway_customer_id = gateway_customer_map.get(gateway)
        if gateway_customer_id:
            subscription.gateway_customer_id = gateway_customer_id
            subscription.save(update_fields=['gateway_customer_id'])
        
        # Atualizar tenant com novo plano
        tenant.subscription_plan = plan.slug
        tenant.max_projects = plan.max_projects if plan.max_projects > 0 else 999999
        tenant.max_users = plan.max_users if plan.max_users > 0 else 999999
        tenant.save()
        
        logger.info(f'Assinatura criada: {subscription.id} para tenant {tenant.slug}')
        return subscription
    
    @staticmethod
    @transaction.atomic
    def upgrade_subscription(subscription: Subscription, new_plan: Plan) -> Tuple[Subscription, Optional[Invoice]]:
        """
        Faz upgrade de assinatura
        
        Args:
            subscription: Assinatura atual
            new_plan: Novo plano
            
        Returns:
            Tupla (Subscription atualizada, Invoice de ajuste se houver)
            
        Raises:
            ValidationError: Se novo plano não está ativo ou é igual ao atual
        """
        # Validar se novo plano está ativo
        if not new_plan.is_active:
            raise ValidationError('Novo plano não está ativo')
        
        # Validar se não é o mesmo plano
        if subscription.plan == new_plan:
            raise ValidationError('Novo plano é igual ao plano atual')
        
        old_plan = subscription.plan
        
        # Calcular prorata
        days_used = (timezone.now().date() - subscription.current_period_start).days
        total_days = (subscription.current_period_end - subscription.current_period_start).days
        
        old_price = BillingService.get_plan_price_for_tenant(
            old_plan, subscription.tenant, 'monthly'
        )
        new_price = BillingService.get_plan_price_for_tenant(
            new_plan, subscription.tenant, 'monthly'
        )
        
        # Calcular prorata (simplificado)
        prorata_amount = (new_price - old_price) * (Decimal(days_used) / Decimal(total_days))
        
        # Atualizar assinatura
        subscription.plan = new_plan
        subscription.save()
        
        # Atualizar tenant
        tenant = subscription.tenant
        tenant.subscription_plan = new_plan.slug
        tenant.max_projects = new_plan.max_projects if new_plan.max_projects > 0 else 999999
        tenant.max_users = new_plan.max_users if new_plan.max_users > 0 else 999999
        tenant.save()
        
        # Criar invoice de ajuste se necessário
        adjustment_invoice = None
        if prorata_amount > 0:
            adjustment_invoice = InvoiceService.generate_adjustment_invoice(
                subscription, prorata_amount
            )
        
        logger.info(f'Upgrade realizado: {subscription.id} de {old_plan.slug} para {new_plan.slug}')
        return subscription, adjustment_invoice
    
    @staticmethod
    @transaction.atomic
    def cancel_subscription(subscription: Subscription, reason: str = '') -> Subscription:
        """
        Cancela assinatura
        
        Args:
            subscription: Assinatura a cancelar
            reason: Motivo do cancelamento
            
        Returns:
            Subscription cancelada
        """
        subscription.cancel_at_period_end = True
        subscription.cancellation_reason = reason
        subscription.canceled_at = timezone.now()
        subscription.status = 'canceled'
        subscription.save()
        
        logger.info(f'Assinatura cancelada: {subscription.id}')
        return subscription


class InvoiceService:
    """Serviço para gerenciar faturas"""
    
    @staticmethod
    def generate_invoice_number() -> str:
        """
        Gera número único de fatura
        
        Returns:
            Número da fatura (ex: INV-2025-0001)
        """
        year = timezone.now().year
        last_invoice = Invoice.objects.filter(
            invoice_number__startswith=f'INV-{year}-'
        ).order_by('-invoice_number').first()
        
        if last_invoice:
            last_number = int(last_invoice.invoice_number.split('-')[-1])
            new_number = last_number + 1
        else:
            new_number = 1
        
        return f'INV-{year}-{new_number:04d}'
    
    @staticmethod
    @transaction.atomic
    def generate_invoice(
        subscription: Subscription,
        period_start: Optional[date] = None,
        period_end: Optional[date] = None
    ) -> Invoice:
        """
        Gera fatura para assinatura
        
        Args:
            subscription: Assinatura
            period_start: Início do período (opcional)
            period_end: Fim do período (opcional)
            
        Returns:
            Invoice gerada
        """
        if not period_start:
            period_start = subscription.current_period_start
        if not period_end:
            period_end = subscription.current_period_end
        
        # Calcular valores
        plan = subscription.plan
        tenant = subscription.tenant
        billing_cycle = 'yearly' if (period_end - period_start).days >= 365 else 'monthly'
        amount = BillingService.get_plan_price_for_tenant(plan, tenant, billing_cycle)
        
        # Criar fatura
        invoice = Invoice.objects.create(
            tenant=tenant,
            subscription=subscription,
            invoice_number=InvoiceService.generate_invoice_number(),
            amount=amount,
            currency=tenant.currency,
            tax_amount=Decimal('0.00'),  # TODO: Calcular impostos
            total_amount=amount,
            status='open',
            issue_date=timezone.now().date(),
            due_date=period_end,
            line_items=[{
                'description': f'Assinatura {plan.name} - {billing_cycle}',
                'quantity': 1,
                'amount': float(amount)
            }]
        )
        
        logger.info(f'Fatura gerada: {invoice.invoice_number} para tenant {tenant.slug}')
        return invoice
    
    @staticmethod
    @transaction.atomic
    def generate_adjustment_invoice(subscription: Subscription, amount: Decimal) -> Invoice:
        """
        Gera fatura de ajuste (prorata)
        
        Args:
            subscription: Assinatura
            amount: Valor do ajuste
            
        Returns:
            Invoice de ajuste
        """
        tenant = subscription.tenant
        
        invoice = Invoice.objects.create(
            tenant=tenant,
            subscription=subscription,
            invoice_number=InvoiceService.generate_invoice_number(),
            amount=amount,
            currency=tenant.currency,
            tax_amount=Decimal('0.00'),
            total_amount=amount,
            status='open',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
            line_items=[{
                'description': f'Ajuste de plano - Prorata',
                'quantity': 1,
                'amount': float(amount)
            }],
            notes='Fatura de ajuste por mudança de plano'
        )
        
        logger.info(f'Fatura de ajuste gerada: {invoice.invoice_number}')
        return invoice


class PaymentService:
    """Serviço para gerenciar pagamentos"""
    
    @staticmethod
    @transaction.atomic
    def process_payment(
        invoice: Invoice,
        payment_method: Optional[PaymentMethod] = None
    ) -> Payment:
        """
        Processa pagamento de uma fatura
        
        Args:
            invoice: Fatura a pagar
            payment_method: Método de pagamento (opcional, usa padrão se não fornecido)
            
        Returns:
            Payment criado
        """
        if not payment_method:
            payment_method = PaymentMethod.objects.filter(
                tenant=invoice.tenant,
                is_default=True,
                is_active=True
            ).first()

        if not payment_method:
            raise ValidationError('Nenhum método de pagamento disponível')

        # Criar registro de pagamento (ainda pendente)
        payment = Payment.objects.create(
            invoice=invoice,
            tenant=invoice.tenant,
            payment_method=payment_method,
            amount=invoice.total_amount,
            currency=invoice.currency,
            status='pending',
            payment_method_type=payment_method.type,
            gateway=payment_method.gateway,
        )

        gateway_name: GatewayType = payment_method.gateway  # type: ignore[assignment]

        subscription = invoice.subscription
        customer_id: Optional[str] = None

        if subscription:
            update_fields = []

            if subscription.payment_method_id != payment_method.id:
                subscription.payment_method = payment_method
                update_fields.append('payment_method')

            if subscription.gateway != gateway_name:
                subscription.gateway = gateway_name
                update_fields.append('gateway')

            if gateway_name == 'stripe':
                customer_id = subscription.gateway_customer_id or payment_method.tenant.stripe_customer_id
                if customer_id and subscription.gateway_customer_id != customer_id:
                    subscription.gateway_customer_id = customer_id
                    update_fields.append('gateway_customer_id')
            elif gateway_name == 'asaas':
                customer_id = subscription.gateway_customer_id or payment_method.tenant.asaas_customer_id
                if customer_id and subscription.gateway_customer_id != customer_id:
                    subscription.gateway_customer_id = customer_id
                    update_fields.append('gateway_customer_id')

            if update_fields:
                subscription.save(update_fields=update_fields)
        else:
            if gateway_name == 'stripe':
                customer_id = payment_method.tenant.stripe_customer_id
            elif gateway_name == 'asaas':
                customer_id = payment_method.tenant.asaas_customer_id

        # Gateway Asaas ainda não está totalmente integrado com customer/datas,
        # então mantemos comportamento de "processing" por enquanto
        if gateway_name == 'asaas':
            payment.status = 'processing'
            payment.save()
            logger.warning('Processamento Asaas ainda não está totalmente integrado (mantendo status processing).')
        else:
            gateway = get_gateway_service(gateway_name)

            try:
                # Processar pagamento no gateway
                result = gateway.process_payment(
                    amount=payment.amount,
                    currency=payment.currency,
                    payment_method_id=payment_method.gateway_payment_method_id,
                    invoice_id=invoice.invoice_number,
                    customer_id=customer_id,
                )

                # Normalizar status para string simples
                status = str(result.get('status', '')).lower()
                gateway_payment_id = str(result.get('id') or result.get('payment_id') or '')

                # Stripe costuma retornar 'succeeded', Asaas 'CONFIRMED'
                if status in ['succeeded', 'requires_capture', 'processing', 'confirmed', 'confirmado', 'paid']:
                    # Marcar como sucesso
                    payment.gateway_payment_id = gateway_payment_id or payment.gateway_payment_id
                    # Alguns gateways retornam charge_id separado
                    charge_id = result.get('charge_id') or result.get('charge', {}).get('id')
                    if charge_id:
                        payment.gateway_charge_id = str(charge_id)

                    PaymentService.mark_payment_succeeded(payment, payment.gateway_payment_id or '')
                else:
                    reason = f'Status de pagamento no gateway: {status or "desconhecido"}'
                    PaymentService.mark_payment_failed(payment, reason)

            except Exception as e:
                # Qualquer erro na chamada ao gateway marca como falha
                logger.error(f'Erro ao processar pagamento via gateway {gateway_name}: {e}')
                PaymentService.mark_payment_failed(payment, str(e))

        logger.info(f'Pagamento processado: {payment.id} para fatura {invoice.invoice_number} com status {payment.status}')
        return payment
    
    @staticmethod
    @transaction.atomic
    def mark_payment_succeeded(payment: Payment, gateway_payment_id: str) -> Payment:
        """
        Marca pagamento como bem-sucedido
        
        Args:
            payment: Pagamento
            gateway_payment_id: ID do pagamento no gateway
            
        Returns:
            Payment atualizado
        """
        payment.status = 'succeeded'
        payment.gateway_payment_id = gateway_payment_id
        payment.save()
        
        # Atualizar fatura
        payment.invoice.status = 'paid'
        payment.invoice.paid_at = timezone.now()
        payment.invoice.save()
        
        # Atualizar assinatura se necessário
        if payment.invoice.subscription:
            subscription = payment.invoice.subscription
            if subscription.status in ['past_due', 'trialing']:
                subscription.status = 'active'
                subscription.save()
        
        logger.info(f'Pagamento bem-sucedido: {payment.id}')
        return payment
    
    @staticmethod
    @transaction.atomic
    def mark_payment_failed(payment: Payment, reason: str) -> Payment:
        """
        Marca pagamento como falhado
        
        Args:
            payment: Pagamento
            reason: Motivo da falha
            
        Returns:
            Payment atualizado
        """
        payment.status = 'failed'
        payment.failure_reason = reason
        payment.retry_count += 1
        payment.save()
        
        # Atualizar assinatura se necessário
        if payment.invoice.subscription:
            subscription = payment.invoice.subscription
            if subscription.status == 'active':
                subscription.status = 'past_due'
                subscription.save()
        
        logger.info(f'Pagamento falhou: {payment.id} - {reason}')
        return payment

