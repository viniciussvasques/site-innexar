"""
Testes unitários para Gateway Services
"""
import pytest
from decimal import Decimal
from unittest.mock import Mock, patch
from apps.billing.gateway.asaas import AsaasGatewayService
from apps.billing.gateway.stripe import StripeGatewayService
from apps.tenants.models import Tenant


@pytest.mark.django_db
class TestAsaasGatewayService:
    """Testes para AsaasGatewayService"""
    
    @pytest.fixture
    def gateway(self):
        """Fixture para gateway Asaas"""
        with patch('apps.billing.gateway.asaas.settings') as mock_settings:
            mock_settings.ASAAS_API_KEY = 'test_key'
            mock_settings.ASAAS_ENVIRONMENT = 'sandbox'
            mock_settings.ASAAS_WEBHOOK_TOKEN = 'test_token'
            return AsaasGatewayService()
    
    @pytest.fixture
    def tenant(self):
        """Fixture para tenant"""
        return Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
    
    @patch('apps.billing.gateway.asaas.requests.post')
    def test_create_customer(self, mock_post, gateway, tenant):
        """Testa criação de cliente no Asaas"""
        mock_response = Mock()
        mock_response.json.return_value = {'id': 'cus_123456'}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        customer_id = gateway.create_customer(tenant)
        
        assert customer_id == 'cus_123456'
        mock_post.assert_called_once()
    
    def test_create_payment_method(self, gateway):
        """Testa criação de método de pagamento no Asaas"""
        result = gateway.create_payment_method('token_123', 'cus_123456')
        
        assert result['id'] == 'token_123'
        assert result['customer_id'] == 'cus_123456'
    
    @patch('apps.billing.gateway.asaas.requests.post')
    def test_create_subscription(self, mock_post, gateway):
        """Testa criação de assinatura no Asaas"""
        mock_response = Mock()
        mock_response.json.return_value = {'id': 'sub_123456', 'status': 'ACTIVE'}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = gateway.create_subscription(
            customer_id='cus_123456',
            plan_id='plan_123',
            payment_method_id='pm_123',
            billing_cycle='monthly'
        )
        
        assert result['id'] == 'sub_123456'
        mock_post.assert_called_once()
    
    @patch('apps.billing.gateway.asaas.requests.post')
    def test_process_payment(self, mock_post, gateway):
        """Testa processamento de pagamento no Asaas"""
        mock_response = Mock()
        mock_response.json.return_value = {'id': 'pay_123456', 'status': 'CONFIRMED'}
        mock_response.raise_for_status = Mock()
        mock_post.return_value = mock_response
        
        result = gateway.process_payment(
            amount=Decimal('297.00'),
            currency='BRL',
            payment_method_id='pm_123',
            invoice_id='INV-2025-0001'
        )
        
        assert result['id'] == 'pay_123456'
        mock_post.assert_called_once()
    
    @patch('apps.billing.gateway.asaas.requests.delete')
    def test_cancel_subscription(self, mock_delete, gateway):
        """Testa cancelamento de assinatura no Asaas"""
        mock_response = Mock()
        mock_response.raise_for_status = Mock()
        mock_delete.return_value = mock_response
        
        result = gateway.cancel_subscription('sub_123456')
        
        assert result is True
        mock_delete.assert_called_once()
    
    def test_handle_webhook(self, gateway):
        """Testa processamento de webhook do Asaas"""
        payload = {
            'event': 'PAYMENT_CONFIRMED',
            'payment': {
                'id': 'pay_123456',
                'status': 'CONFIRMED'
            }
        }
        
        with patch('apps.billing.gateway.asaas.settings') as mock_settings:
            mock_settings.ASAAS_WEBHOOK_TOKEN = 'test_token'
            result = gateway.handle_webhook(payload, 'test_token')
            
            assert result['event'] == 'PAYMENT_CONFIRMED'
            assert result['payment_id'] == 'pay_123456'


@pytest.mark.django_db
class TestStripeGatewayService:
    """Testes para StripeGatewayService"""
    
    @pytest.fixture
    def gateway(self):
        """Fixture para gateway Stripe"""
        with patch('apps.billing.gateway.stripe.settings') as mock_settings:
            mock_settings.STRIPE_SECRET_KEY = 'sk_test_123'
            mock_settings.STRIPE_WEBHOOK_SECRET = 'whsec_123'
            return StripeGatewayService()
    
    @pytest.fixture
    def tenant(self):
        """Fixture para tenant"""
        return Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='US'
        )
    
    @patch('apps.billing.gateway.stripe.stripe.Customer.create')
    def test_create_customer(self, mock_create, gateway, tenant):
        """Testa criação de cliente no Stripe"""
        mock_customer = Mock()
        mock_customer.id = 'cus_123456'
        mock_create.return_value = mock_customer
        
        customer_id = gateway.create_customer(tenant)
        
        assert customer_id == 'cus_123456'
        mock_create.assert_called_once()
    
    @patch('apps.billing.gateway.stripe.stripe.PaymentMethod.retrieve')
    @patch('apps.billing.gateway.stripe.stripe.PaymentMethod.attach')
    @patch('apps.billing.gateway.stripe.stripe.Customer.modify')
    def test_create_payment_method(self, mock_modify, mock_attach, mock_retrieve, gateway):
        """Testa criação de método de pagamento no Stripe"""
        mock_pm = Mock()
        mock_pm.id = 'pm_123456'
        mock_pm.type = 'card'
        mock_pm.card = Mock()
        mock_pm.card.last4 = '4242'
        mock_pm.card.brand = 'visa'
        mock_pm.card.exp_month = 12
        mock_pm.card.exp_year = 2025
        mock_retrieve.return_value = mock_pm
        
        result = gateway.create_payment_method('pm_123456', 'cus_123456')
        
        assert result['id'] == 'pm_123456'
        assert result['type'] == 'card'
        mock_retrieve.assert_called_once()
    
    @patch('apps.billing.gateway.stripe.stripe.Subscription.create')
    def test_create_subscription(self, mock_create, gateway):
        """Testa criação de assinatura no Stripe"""
        mock_sub = Mock()
        mock_sub.id = 'sub_123456'
        mock_sub.status = 'active'
        mock_sub.current_period_start = 1609459200
        mock_sub.current_period_end = 1612137600
        mock_create.return_value = mock_sub
        
        result = gateway.create_subscription(
            customer_id='cus_123456',
            plan_id='price_123',
            payment_method_id='pm_123',
            billing_cycle='monthly'
        )
        
        assert result['id'] == 'sub_123456'
        mock_create.assert_called_once()
    
    @patch('apps.billing.gateway.stripe.stripe.PaymentIntent.create')
    def test_process_payment(self, mock_create, gateway):
        """Testa processamento de pagamento no Stripe"""
        mock_pi = Mock()
        mock_pi.id = 'pi_123456'
        mock_pi.status = 'succeeded'
        mock_charge = Mock()
        mock_charge.id = 'ch_123456'
        mock_pi.charges.data = [mock_charge]
        mock_create.return_value = mock_pi
        
        result = gateway.process_payment(
            amount=Decimal('49.00'),
            currency='USD',
            payment_method_id='pm_123',
            invoice_id='INV-2025-0001'
        )
        
        assert result['id'] == 'pi_123456'
        mock_create.assert_called_once()
    
    @patch('apps.billing.gateway.stripe.stripe.Subscription.modify')
    def test_cancel_subscription(self, mock_modify, gateway):
        """Testa cancelamento de assinatura no Stripe"""
        mock_sub = Mock()
        mock_modify.return_value = mock_sub
        
        result = gateway.cancel_subscription('sub_123456')
        
        assert result is True
        mock_modify.assert_called_once()
    
    @patch('apps.billing.gateway.stripe.stripe.Webhook.construct_event')
    def test_handle_webhook(self, mock_construct, gateway):
        """Testa processamento de webhook do Stripe"""
        mock_event = {
            'type': 'payment_intent.succeeded',
            'data': {
                'object': {
                    'id': 'pi_123456',
                    'status': 'succeeded'
                }
            }
        }
        mock_construct.return_value = mock_event
        
        result = gateway.handle_webhook({}, 'signature')
        
        assert result['event'] == 'payment_intent.succeeded'
        assert result['payment_id'] == 'pi_123456'
        mock_construct.assert_called_once()

