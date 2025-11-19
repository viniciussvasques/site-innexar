"""
Asaas Gateway Service
Implementação do gateway Asaas para Brasil
"""
import logging
import requests
from decimal import Decimal
from typing import Optional, Dict, Any
from django.conf import settings
from .base import GatewayService

# Timeout para requisições (segundos)
REQUEST_TIMEOUT = 10

logger = logging.getLogger(__name__)


class AsaasGatewayService(GatewayService):
    """Implementação do gateway Asaas"""
    
    def __init__(self):
        self.api_key = getattr(settings, 'ASAAS_API_KEY', '')
        self.environment = getattr(settings, 'ASAAS_ENVIRONMENT', 'sandbox')
        self.base_url = 'https://sandbox.asaas.com/api/v3' if self.environment == 'sandbox' else 'https://www.asaas.com/api/v3'
        self.headers = {
            'access_token': self.api_key,
            'Content-Type': 'application/json'
        }
    
    def create_customer(self, tenant) -> str:
        """Cria cliente no Asaas"""
        try:
            url = f'{self.base_url}/customers'
            
            # Obter dados do onboarding se disponível
            onboarding_data = {}
            if hasattr(tenant, 'onboarding_progress') and tenant.onboarding_progress.data:
                onboarding_data = tenant.onboarding_progress.data
            
            data = {
                'name': tenant.name,
                'email': tenant.email,
                'phone': tenant.phone or '',
                'cpfCnpj': onboarding_data.get('tax_id', ''),
                'postalCode': onboarding_data.get('zipcode', ''),
                'address': onboarding_data.get('street', ''),
                'addressNumber': onboarding_data.get('number', ''),
                'complement': onboarding_data.get('complement', ''),
                'province': onboarding_data.get('neighborhood', ''),
                'city': onboarding_data.get('city', ''),
                'state': onboarding_data.get('state', ''),
            }
            
            response = requests.post(url, json=data, headers=self.headers, timeout=10)
            response.raise_for_status()
            result = response.json()
            
            customer_id = result.get('id')
            if not customer_id:
                raise ValueError('Asaas não retornou ID do cliente')
            
            logger.info(f'Cliente criado no Asaas: {customer_id}')
            return customer_id
        except requests.exceptions.RequestException as e:
            logger.error(f'Erro de requisição ao criar cliente no Asaas: {e}')
            raise
        except Exception as e:
            logger.error(f'Erro ao criar cliente no Asaas: {e}')
            raise
    
    def create_payment_method(self, token: str, customer_id: str) -> Dict[str, Any]:
        """Cria método de pagamento no Asaas"""
        try:
            # No Asaas, métodos de pagamento são criados junto com a cobrança
            # Por enquanto, retornamos o token
            return {
                'id': token,  # Token do frontend
                'type': 'credit_card',
                'customer_id': customer_id
            }
        except Exception as e:
            logger.error(f'Erro ao criar método de pagamento no Asaas: {e}')
            raise
    
    def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        payment_method_id: str,
        billing_cycle: str = 'monthly'
    ) -> Dict[str, Any]:
        """Cria assinatura no Asaas"""
        try:
            url = f'{self.base_url}/subscriptions'
            data = {
                'customer': customer_id,
                'billingType': 'CREDIT_CARD',  # ou BOLETO, PIX
                'value': 0,  # TODO: Obter do plano
                'nextDueDate': '',  # TODO: Calcular data
                'cycle': 'MONTHLY' if billing_cycle == 'monthly' else 'YEARLY',
            }
            
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            result = response.json()
            
            logger.info(f'Assinatura criada no Asaas: {result.get("id")}')
            return result
        except Exception as e:
            logger.error(f'Erro ao criar assinatura no Asaas: {e}')
            raise
    
    def process_payment(
        self,
        amount: Decimal,
        currency: str,
        payment_method_id: str,
        invoice_id: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """Processa pagamento no Asaas"""
        try:
            url = f'{self.base_url}/payments'
            data = {
                'customer': '',  # TODO: Obter do tenant
                'billingType': 'CREDIT_CARD',
                'value': float(amount),
                'dueDate': '',  # TODO: Calcular data
                'description': f'Pagamento - {invoice_id}' if invoice_id else 'Pagamento',
            }
            
            response = requests.post(url, json=data, headers=self.headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            result = response.json()
            
            payment_id = result.get('id')
            if not payment_id:
                raise ValueError('Asaas não retornou ID do pagamento')
            
            logger.info(f'Pagamento processado no Asaas: {payment_id}')
            return result
        except requests.exceptions.RequestException as e:
            logger.error(f'Erro de requisição ao processar pagamento no Asaas: {e}')
            raise
        except Exception as e:
            logger.error(f'Erro ao processar pagamento no Asaas: {e}')
            raise
    
    def cancel_subscription(self, subscription_id: str) -> bool:
        """Cancela assinatura no Asaas"""
        try:
            url = f'{self.base_url}/subscriptions/{subscription_id}'
            response = requests.delete(url, headers=self.headers, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            
            logger.info(f'Assinatura cancelada no Asaas: {subscription_id}')
            return True
        except Exception as e:
            logger.error(f'Erro ao cancelar assinatura no Asaas: {e}')
            raise
    
    def handle_webhook(self, payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """Processa webhook do Asaas"""
        try:
            # Validar assinatura do webhook
            webhook_token = getattr(settings, 'ASAAS_WEBHOOK_TOKEN', '')
            if signature != webhook_token:
                raise ValueError('Assinatura do webhook inválida')
            
            event = payload.get('event')
            payment = payload.get('payment', {})
            
            return {
                'event': event,
                'payment_id': payment.get('id'),
                'status': payment.get('status'),
                'data': payload
            }
        except Exception as e:
            logger.error(f'Erro ao processar webhook do Asaas: {e}')
            raise

