"""
Stripe Gateway Service
Implementação do gateway Stripe para USA/Internacional
"""
import logging
import stripe
from decimal import Decimal
from typing import Optional, Dict, Any
from django.conf import settings
from .base import GatewayService

logger = logging.getLogger(__name__)


class StripeGatewayService(GatewayService):
    """Implementação do gateway Stripe"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')
        self.webhook_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')
        stripe.api_key = self.api_key
    
    def create_customer(self, tenant) -> str:
        """Cria cliente no Stripe"""
        try:
            customer = stripe.Customer.create(
                name=tenant.name,
                email=tenant.email,
                phone=tenant.phone,
                metadata={
                    'tenant_id': str(tenant.id),
                    'tenant_slug': tenant.slug
                }
            )
            
            logger.info(f'Cliente criado no Stripe: {customer.id}')
            return customer.id
        except Exception as e:
            logger.error(f'Erro ao criar cliente no Stripe: {e}')
            raise
    
    def create_payment_method(self, token: str, customer_id: str) -> Dict[str, Any]:
        """Cria método de pagamento no Stripe"""
        try:
            # No Stripe, o token já é um PaymentMethod
            payment_method = stripe.PaymentMethod.retrieve(token)
            
            # Anexar ao cliente
            payment_method.attach(customer=customer_id)
            
            # Definir como padrão
            stripe.Customer.modify(
                customer_id,
                invoice_settings={'default_payment_method': payment_method.id}
            )
            
            logger.info(f'Método de pagamento criado no Stripe: {payment_method.id}')
            return {
                'id': payment_method.id,
                'type': payment_method.type,
                'card': {
                    'last4': payment_method.card.last4,
                    'brand': payment_method.card.brand,
                    'exp_month': payment_method.card.exp_month,
                    'exp_year': payment_method.card.exp_year
                } if payment_method.type == 'card' else None
            }
        except Exception as e:
            logger.error(f'Erro ao criar método de pagamento no Stripe: {e}')
            raise
    
    def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        payment_method_id: str,
        billing_cycle: str = 'monthly'
    ) -> Dict[str, Any]:
        """Cria assinatura no Stripe"""
        try:
            subscription = stripe.Subscription.create(
                customer=customer_id,
                items=[{'price': plan_id}],  # plan_id deve ser um Price ID do Stripe
                default_payment_method=payment_method_id,
                expand=['latest_invoice.payment_intent']
            )
            
            logger.info(f'Assinatura criada no Stripe: {subscription.id}')
            return {
                'id': subscription.id,
                'status': subscription.status,
                'current_period_start': subscription.current_period_start,
                'current_period_end': subscription.current_period_end,
            }
        except Exception as e:
            logger.error(f'Erro ao criar assinatura no Stripe: {e}')
            raise
    
    def process_payment(
        self,
        amount: Decimal,
        currency: str,
        payment_method_id: str,
        invoice_id: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Processa pagamento no Stripe (TEST MODE)

        - Usa PaymentIntent com automatic_payment_methods desabilitado para redirects,
          para evitar necessidade de return_url em ambiente backend-only.
        """
        try:
            # PaymentIntent simples, limitado a cartão, para evitar meios de pagamento com redirect
            params = {
                "amount": int(amount * 100),  # Stripe usa centavos
                "currency": currency.lower(),
                "payment_method": payment_method_id,
                "payment_method_types": ["card"],
                "confirm": True,
                "metadata": {
                    "invoice_id": invoice_id or "",
                },
            }

            if customer_id:
                params["customer"] = customer_id

            payment_intent = stripe.PaymentIntent.create(**params)

            logger.info(f"Pagamento processado no Stripe: {payment_intent.id}")
            # Nem sempre haverá charges imediatas (dependendo da conta/config),
            # então retornamos apenas o essencial para o service decidir.
            return {
                "id": payment_intent.id,
                "status": payment_intent.status,
            }
        except Exception as e:
            logger.error(f"Erro ao processar pagamento no Stripe: {e}")
            raise
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancela assinatura no Stripe"""
        try:
            subscription = stripe.Subscription.modify(
                subscription_id,
                cancel_at_period_end=True
            )
            
            logger.info(f'Assinatura cancelada no Stripe: {subscription_id}')
            return True
        except Exception as e:
            logger.error(f'Erro ao cancelar assinatura no Stripe: {e}')
            raise
    
    def handle_webhook(self, payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """Processa webhook do Stripe"""
        try:
            # Validar assinatura do webhook
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                self.webhook_secret
            )
            
            event_type = event['type']
            event_data = event['data']['object']
            
            logger.info(f'Webhook recebido do Stripe: {event_type}')
            return {
                'event': event_type,
                'payment_id': event_data.get('id'),
                'status': event_data.get('status'),
                'data': event_data
            }
        except ValueError as e:
            logger.error(f'Erro ao validar webhook do Stripe: {e}')
            raise
        except Exception as e:
            logger.error(f'Erro ao processar webhook do Stripe: {e}')
            raise

