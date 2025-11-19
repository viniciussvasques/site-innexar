"""
Testes unitários para Services de Billing
"""
import pytest
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from apps.billing.models import Plan, Subscription, Invoice, Payment, PaymentMethod
from apps.billing.services import BillingService, InvoiceService, PaymentService
from apps.tenants.models import Tenant


@pytest.mark.django_db
class TestBillingService:
    """Testes para BillingService"""
    
    def test_get_plan_price_for_tenant_br(self):
        """Testa obtenção de preço para tenant brasileiro"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
            price_yearly_brl=Decimal('2970.00'),
        )
        
        price = BillingService.get_plan_price_for_tenant(plan, tenant, 'monthly')
        assert price == Decimal('297.00')
        
        price = BillingService.get_plan_price_for_tenant(plan, tenant, 'yearly')
        assert price == Decimal('2970.00')
    
    def test_get_plan_price_for_tenant_us(self):
        """Testa obtenção de preço para tenant americano"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='US'
        )
        
        plan = Plan.objects.create(
            name='Starter',
            slug='starter',
            price_monthly_usd=Decimal('49.00'),
            price_yearly_usd=Decimal('490.00'),
        )
        
        price = BillingService.get_plan_price_for_tenant(plan, tenant, 'monthly')
        assert price == Decimal('49.00')
    
    def test_create_subscription(self):
        """Testa criação de assinatura"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
            max_projects=5,
            max_users=5,
        )
        
        subscription = BillingService.create_subscription(
            tenant=tenant,
            plan=plan,
            billing_cycle='monthly'
        )
        
        assert subscription.tenant == tenant
        assert subscription.plan == plan
        assert subscription.status == 'active'
        assert subscription.gateway == 'asaas'  # BR usa Asaas
        
        # Verificar se tenant foi atualizado
        tenant.refresh_from_db()
        assert tenant.subscription_plan == 'basic'
        assert tenant.max_projects == 5
    
    def test_create_subscription_with_trial(self):
        """Testa criação de assinatura com trial"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
            trial_days=14
        )
        
        subscription = BillingService.create_subscription(
            tenant=tenant,
            plan=plan,
            billing_cycle='monthly'
        )
        
        assert subscription.status == 'trialing'
        assert subscription.trial_start is not None
        assert subscription.trial_end is not None
        assert (subscription.trial_end - subscription.trial_start).days == 14
    
    def test_create_subscription_already_exists(self):
        """Testa erro ao criar assinatura quando já existe"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        # Criar primeira assinatura
        BillingService.create_subscription(tenant=tenant, plan=plan)
        
        # Tentar criar segunda (deve falhar)
        with pytest.raises(ValidationError):
            BillingService.create_subscription(tenant=tenant, plan=plan)
    
    def test_upgrade_subscription(self):
        """Testa upgrade de assinatura"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        old_plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
            max_projects=5,
        )
        
        new_plan = Plan.objects.create(
            name='Profissional',
            slug='professional',
            price_monthly_brl=Decimal('797.00'),
            max_projects=20,
        )
        
        subscription = BillingService.create_subscription(
            tenant=tenant,
            plan=old_plan,
            billing_cycle='monthly'
        )
        
        subscription, adjustment_invoice = BillingService.upgrade_subscription(
            subscription, new_plan
        )
        
        assert subscription.plan == new_plan
        
        # Verificar se tenant foi atualizado
        tenant.refresh_from_db()
        assert tenant.subscription_plan == 'professional'
        assert tenant.max_projects == 20
    
    def test_cancel_subscription(self):
        """Testa cancelamento de assinatura"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        subscription = BillingService.create_subscription(
            tenant=tenant,
            plan=plan,
            billing_cycle='monthly'
        )
        
        subscription = BillingService.cancel_subscription(
            subscription,
            reason='Não estou mais usando'
        )
        
        assert subscription.status == 'canceled'
        assert subscription.cancel_at_period_end is True
        assert subscription.cancellation_reason == 'Não estou mais usando'
        assert subscription.canceled_at is not None


@pytest.mark.django_db
class TestInvoiceService:
    """Testes para InvoiceService"""
    
    def test_generate_invoice_number(self):
        """Testa geração de número de fatura"""
        number1 = InvoiceService.generate_invoice_number()
        assert number1.startswith('INV-')
        assert str(timezone.now().year) in number1
        
        # Criar uma fatura para testar sequência
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        Invoice.objects.create(
            tenant=tenant,
            subscription=subscription,
            invoice_number=number1,
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='open',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
        )
        
        number2 = InvoiceService.generate_invoice_number()
        assert number2 != number1
        # Número deve ser sequencial
        num1 = int(number1.split('-')[-1])
        num2 = int(number2.split('-')[-1])
        assert num2 == num1 + 1
    
    def test_generate_invoice(self):
        """Testa geração de fatura"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        invoice = InvoiceService.generate_invoice(subscription)
        
        assert invoice.tenant == tenant
        assert invoice.subscription == subscription
        assert invoice.amount == Decimal('297.00')
        assert invoice.currency == 'BRL'
        assert invoice.status == 'open'
        assert invoice.invoice_number.startswith('INV-')
        assert len(invoice.line_items) > 0


@pytest.mark.django_db
class TestPaymentService:
    """Testes para PaymentService"""
    
    def test_process_payment(self):
        """Testa processamento de pagamento"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        invoice = Invoice.objects.create(
            tenant=tenant,
            subscription=subscription,
            invoice_number='INV-2025-0001',
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='open',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
        )
        
        payment_method = PaymentMethod.objects.create(
            tenant=tenant,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_123456',
            card_last4='4242',
            is_default=True
        )
        
        payment = PaymentService.process_payment(invoice, payment_method)
        
        assert payment.invoice == invoice
        assert payment.payment_method == payment_method
        assert payment.amount == Decimal('297.00')
        assert payment.status == 'processing'
    
    def test_mark_payment_succeeded(self):
        """Testa marcação de pagamento como bem-sucedido"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        invoice = Invoice.objects.create(
            tenant=tenant,
            subscription=subscription,
            invoice_number='INV-2025-0001',
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='open',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
        )
        
        payment = Payment.objects.create(
            invoice=invoice,
            tenant=tenant,
            amount=Decimal('297.00'),
            currency='BRL',
            status='processing',
            payment_method_type='card',
            gateway='asaas'
        )
        
        payment = PaymentService.mark_payment_succeeded(
            payment,
            gateway_payment_id='pay_123456'
        )
        
        assert payment.status == 'succeeded'
        assert payment.gateway_payment_id == 'pay_123456'
        
        # Verificar se fatura foi atualizada
        invoice.refresh_from_db()
        assert invoice.status == 'paid'
        assert invoice.paid_at is not None
    
    def test_mark_payment_failed(self):
        """Testa marcação de pagamento como falhado"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        invoice = Invoice.objects.create(
            tenant=tenant,
            subscription=subscription,
            invoice_number='INV-2025-0001',
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='open',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
        )
        
        payment = Payment.objects.create(
            invoice=invoice,
            tenant=tenant,
            amount=Decimal('297.00'),
            currency='BRL',
            status='processing',
            payment_method_type='card',
            gateway='asaas'
        )
        
        payment = PaymentService.mark_payment_failed(
            payment,
            reason='Cartão recusado'
        )
        
        assert payment.status == 'failed'
        assert payment.failure_reason == 'Cartão recusado'
        assert payment.retry_count == 1
        
        # Verificar se assinatura foi atualizada
        subscription.refresh_from_db()
        assert subscription.status == 'past_due'

