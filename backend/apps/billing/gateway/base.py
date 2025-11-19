"""
Base Gateway Interface
Interface base para gateways de pagamento
"""
from abc import ABC, abstractmethod
from decimal import Decimal
from typing import Optional, Dict, Any
from apps.billing.models import Subscription, Invoice, Payment, PaymentMethod


class GatewayService(ABC):
    """Interface base para serviços de gateway"""
    
    @abstractmethod
    def create_customer(self, tenant) -> str:
        """
        Cria cliente no gateway
        
        Args:
            tenant: Instância do tenant
            
        Returns:
            ID do cliente no gateway
        """
        pass
    
    @abstractmethod
    def create_payment_method(self, token: str, customer_id: str) -> Dict[str, Any]:
        """
        Cria método de pagamento no gateway
        
        Args:
            token: Token do método de pagamento (obtido no frontend)
            customer_id: ID do cliente no gateway
            
        Returns:
            Dados do método de pagamento criado
        """
        pass
    
    @abstractmethod
    def create_subscription(
        self,
        customer_id: str,
        plan_id: str,
        payment_method_id: str,
        billing_cycle: str = 'monthly'
    ) -> Dict[str, Any]:
        """
        Cria assinatura no gateway
        
        Args:
            customer_id: ID do cliente
            plan_id: ID do plano no gateway
            payment_method_id: ID do método de pagamento
            billing_cycle: 'monthly' ou 'yearly'
            
        Returns:
            Dados da assinatura criada
        """
        pass
    
    @abstractmethod
    def process_payment(
        self,
        amount: Decimal,
        currency: str,
        payment_method_id: str,
        invoice_id: Optional[str] = None,
        customer_id: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Processa pagamento
        
        Args:
            amount: Valor do pagamento
            currency: Moeda
            payment_method_id: ID do método de pagamento
            invoice_id: ID da fatura (opcional)
            
        Returns:
            Dados do pagamento processado
        """
        pass
    
    @abstractmethod
    def cancel_subscription(self, subscription_id: str) -> bool:
        """
        Cancela assinatura no gateway
        
        Args:
            subscription_id: ID da assinatura no gateway
            
        Returns:
            True se cancelado com sucesso
        """
        pass
    
    @abstractmethod
    def handle_webhook(self, payload: Dict[str, Any], signature: str) -> Dict[str, Any]:
        """
        Processa webhook do gateway
        
        Args:
            payload: Payload do webhook
            signature: Assinatura do webhook (para validação)
            
        Returns:
            Dados processados do webhook
        """
        pass

