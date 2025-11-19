"""
Testes de Integração para Billing
Testam o sistema conectado (API, banco, autenticação)
"""
import pytest
import json
from decimal import Decimal
from django.urls import reverse
from django.utils import timezone
from datetime import timedelta
from rest_framework import status
from rest_framework.test import APIClient
from apps.billing.models import Plan, Subscription, Invoice, Payment, PaymentMethod
from apps.core.models import User
from apps.tenants.models import Tenant


@pytest.mark.django_db
class TestBillingAPI:
    """Testes de integração para API de Billing"""
    
    @pytest.fixture
    def client(self):
        """Fixture para APIClient"""
        return APIClient()
    
    @pytest.fixture
    def tenant_br(self):
        """Fixture para tenant brasileiro"""
        return Tenant.objects.create(
            name='Construtora BR',
            slug='construtora-br',
            domain='construtora-br.structurone.com',
            email='contato@construtora-br.com',
            country='BR',
            currency='BRL'
        )
    
    @pytest.fixture
    def tenant_us(self):
        """Fixture para tenant americano"""
        return Tenant.objects.create(
            name='Construction USA',
            slug='construction-usa',
            domain='construction-usa.structurone.com',
            email='contact@construction-usa.com',
            country='US',
            currency='USD'
        )
    
    @pytest.fixture
    def user_br(self, tenant_br):
        """Fixture para usuário brasileiro"""
        return User.objects.create_user(
            email='user@construtora-br.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=tenant_br
        )
    
    @pytest.fixture
    def user_us(self, tenant_us):
        """Fixture para usuário americano"""
        return User.objects.create_user(
            email='user@construction-usa.com',
            password='Test123!@#',
            first_name='John',
            last_name='Doe',
            tenant=tenant_us
        )
    
    @pytest.fixture
    def plan_basic_br(self):
        """Fixture para plano básico (Brasil)"""
        return Plan.objects.create(
            name='Básico',
            slug='basic',
            description='Plano básico para pequenas construtoras',
            price_monthly_brl=Decimal('297.00'),
            price_yearly_brl=Decimal('2970.00'),
            max_projects=5,
            max_users=5,
            max_storage_gb=5,
            features=['Relatórios básicos', 'Suporte por email'],
            is_active=True
        )
    
    @pytest.fixture
    def plan_starter_us(self):
        """Fixture para plano starter (USA)"""
        return Plan.objects.create(
            name='Starter',
            slug='starter',
            description='Starter plan for small construction companies',
            price_monthly_usd=Decimal('49.00'),
            price_yearly_usd=Decimal('490.00'),
            max_projects=5,
            max_users=5,
            max_storage_gb=5,
            features=['Basic reports', 'Email support'],
            is_active=True
        )
    
    def test_list_plans_authenticated(self, client, user_br, plan_basic_br):
        """Testa listagem de planos (autenticado)"""
        client.force_authenticate(user=user_br)
        url = reverse('plan-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Planos não são paginados (pagination_class = None)
        plans = response.data if isinstance(response.data, list) else response.data.get('results', [])
        assert len(plans) > 0
        assert any(p['slug'] == 'basic' for p in plans)
    
    def test_list_plans_unauthenticated(self, client):
        """Testa listagem de planos (não autenticado)"""
        url = reverse('plan-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_get_plan_detail(self, client, user_br, plan_basic_br):
        """Testa detalhes de um plano"""
        client.force_authenticate(user=user_br)
        url = reverse('plan-detail', kwargs={'slug': plan_basic_br.slug})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['slug'] == 'basic'
        assert response.data['name'] == 'Básico'
        assert 'price_monthly_brl' in response.data
    
    def test_get_subscription_me(self, client, user_br, tenant_br, plan_basic_br):
        """Testa obtenção de assinatura atual"""
        client.force_authenticate(user=user_br)
        
        # Criar assinatura
        subscription = Subscription.objects.create(
            tenant=tenant_br,
            plan=plan_basic_br,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
            gateway='asaas'
        )
        
        url = reverse('subscription-me')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == subscription.id
        assert response.data['status'] == 'active'
    
    def test_get_subscription_me_not_found(self, client, user_br):
        """Testa obtenção de assinatura quando não existe"""
        client.force_authenticate(user=user_br)
        url = reverse('subscription-me')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_404_NOT_FOUND
    
    def test_create_subscription(self, client, user_br, tenant_br, plan_basic_br):
        """Testa criação de assinatura via API"""
        client.force_authenticate(user=user_br)
        url = reverse('subscription-create-subscription')
        
        data = {
            'plan_id': plan_basic_br.id,
            'billing_cycle': 'monthly'
        }
        
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['status'] in ['active', 'trialing']
        assert response.data['plan']['id'] == plan_basic_br.id
        
        # Verificar se assinatura foi criada no banco
        subscription = Subscription.objects.get(tenant=tenant_br)
        assert subscription.plan == plan_basic_br
        assert subscription.gateway == 'asaas'  # BR usa Asaas
        
        # Verificar se tenant foi atualizado
        tenant_br.refresh_from_db()
        assert tenant_br.subscription_plan == 'basic'
    
    def test_create_subscription_duplicate(self, client, user_br, tenant_br, plan_basic_br):
        """Testa erro ao criar assinatura duplicada"""
        client.force_authenticate(user=user_br)
        
        # Criar primeira assinatura
        Subscription.objects.create(
            tenant=tenant_br,
            plan=plan_basic_br,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        url = reverse('subscription-create-subscription')
        data = {
            'plan_id': plan_basic_br.id,
            'billing_cycle': 'monthly'
        }
        
        response = client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    def test_upgrade_subscription(self, client, user_br, tenant_br, plan_basic_br):
        """Testa upgrade de assinatura via API"""
        client.force_authenticate(user=user_br)
        
        # Criar plano profissional
        plan_professional = Plan.objects.create(
            name='Profissional',
            slug='professional',
            price_monthly_brl=Decimal('797.00'),
            max_projects=20,
            max_users=20,
            is_active=True
        )
        
        # Criar assinatura básica
        subscription = Subscription.objects.create(
            tenant=tenant_br,
            plan=plan_basic_br,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        url = reverse('subscription-upgrade', kwargs={'pk': subscription.id})
        data = {
            'plan_id': plan_professional.id
        }
        
        response = client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['plan']['id'] == plan_professional.id
        
        # Verificar se tenant foi atualizado
        tenant_br.refresh_from_db()
        assert tenant_br.subscription_plan == 'professional'
        assert tenant_br.max_projects == 20
    
    def test_cancel_subscription(self, client, user_br, tenant_br, plan_basic_br):
        """Testa cancelamento de assinatura via API"""
        client.force_authenticate(user=user_br)
        
        subscription = Subscription.objects.create(
            tenant=tenant_br,
            plan=plan_basic_br,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        url = reverse('subscription-cancel', kwargs={'pk': subscription.id})
        data = {
            'reason': 'Não estou mais usando o sistema'
        }
        
        response = client.patch(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['status'] == 'canceled'
        assert response.data['cancel_at_period_end'] is True
        
        # Verificar no banco
        subscription.refresh_from_db()
        assert subscription.status == 'canceled'
        assert subscription.cancellation_reason == 'Não estou mais usando o sistema'
    
    def test_list_invoices(self, client, user_br, tenant_br, plan_basic_br):
        """Testa listagem de faturas"""
        client.force_authenticate(user=user_br)
        
        subscription = Subscription.objects.create(
            tenant=tenant_br,
            plan=plan_basic_br,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        # Criar faturas
        invoice1 = Invoice.objects.create(
            tenant=tenant_br,
            subscription=subscription,
            invoice_number='INV-2025-0001',
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='paid',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
            paid_at=timezone.now()
        )
        
        invoice2 = Invoice.objects.create(
            tenant=tenant_br,
            subscription=subscription,
            invoice_number='INV-2025-0002',
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='open',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
        )
        
        url = reverse('invoice-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        assert any(inv['invoice_number'] == 'INV-2025-0001' for inv in response.data['results'])
    
    def test_get_invoice_pdf(self, client, user_br, tenant_br, plan_basic_br):
        """Testa download de PDF da fatura"""
        client.force_authenticate(user=user_br)
        
        subscription = Subscription.objects.create(
            tenant=tenant_br,
            plan=plan_basic_br,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
        )
        
        invoice = Invoice.objects.create(
            tenant=tenant_br,
            subscription=subscription,
            invoice_number='INV-2025-0001',
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='paid',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
            gateway_pdf_url='https://example.com/invoice.pdf'
        )
        
        url = reverse('invoice-pdf', kwargs={'pk': invoice.id})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert 'pdf_url' in response.data
        assert response.data['pdf_url'] == 'https://example.com/invoice.pdf'
    
    def test_list_payment_methods(self, client, user_br, tenant_br):
        """Testa listagem de métodos de pagamento"""
        client.force_authenticate(user=user_br)
        
        # Criar métodos de pagamento
        pm1 = PaymentMethod.objects.create(
            tenant=tenant_br,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_123456',
            card_last4='4242',
            card_brand='visa',
            is_default=True
        )
        
        pm2 = PaymentMethod.objects.create(
            tenant=tenant_br,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_789012',
            card_last4='5555',
            card_brand='mastercard',
            is_default=False
        )
        
        url = reverse('payment-method-list')
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data['results']) == 2
        # Método padrão deve vir primeiro
        assert response.data['results'][0]['id'] == pm1.id
        assert response.data['results'][0]['is_default'] is True
    
    def test_set_default_payment_method(self, client, user_br, tenant_br):
        """Testa definir método de pagamento como padrão"""
        client.force_authenticate(user=user_br)
        
        pm1 = PaymentMethod.objects.create(
            tenant=tenant_br,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_123456',
            card_last4='4242',
            is_default=True
        )
        
        pm2 = PaymentMethod.objects.create(
            tenant=tenant_br,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_789012',
            card_last4='5555',
            is_default=False
        )
        
        url = reverse('payment-method-set-default', kwargs={'pk': pm2.id})
        response = client.patch(url)
        
        assert response.status_code == status.HTTP_200_OK
        assert response.data['is_default'] is True
        
        # Verificar que pm1 não é mais padrão
        pm1.refresh_from_db()
        assert pm1.is_default is False
        
        # Verificar que pm2 é padrão
        pm2.refresh_from_db()
        assert pm2.is_default is True
    
    def test_delete_payment_method(self, client, user_br, tenant_br):
        """Testa remoção de método de pagamento"""
        client.force_authenticate(user=user_br)
        
        pm = PaymentMethod.objects.create(
            tenant=tenant_br,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_123456',
            card_last4='4242',
        )
        
        url = reverse('payment-method-detail', kwargs={'pk': pm.id})
        response = client.delete(url)
        
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        # Verificar que foi removido
        assert not PaymentMethod.objects.filter(id=pm.id).exists()
    
    def test_plan_pricing_by_country_br(self, client, user_br, plan_basic_br):
        """Testa que planos mostram preço correto para Brasil"""
        client.force_authenticate(user=user_br)
        url = reverse('plan-detail', kwargs={'slug': plan_basic_br.slug})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Deve mostrar preço em BRL
        assert 'price_monthly_brl' in response.data
        assert response.data['price_monthly_brl'] == '297.00'
    
    def test_plan_pricing_by_country_us(self, client, user_us, plan_starter_us):
        """Testa que planos mostram preço correto para USA"""
        client.force_authenticate(user=user_us)
        url = reverse('plan-detail', kwargs={'slug': plan_starter_us.slug})
        response = client.get(url)
        
        assert response.status_code == status.HTTP_200_OK
        # Deve mostrar preço em USD
        assert 'price_monthly_usd' in response.data
        assert response.data['price_monthly_usd'] == '49.00'


@pytest.mark.django_db
class TestBillingWebhooks:
    """Testes de integração para webhooks"""
    
    @pytest.fixture
    def tenant_br(self):
        """Fixture para tenant brasileiro"""
        return Tenant.objects.create(
            name='Construtora BR',
            slug='construtora-br',
            domain='construtora-br.structurone.com',
            email='contato@construtora-br.com',
            country='BR'
        )
    
    @pytest.fixture
    def subscription(self, tenant_br):
        """Fixture para assinatura"""
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
        )
        
        return Subscription.objects.create(
            tenant=tenant_br,
            plan=plan,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
            gateway='asaas',
            gateway_subscription_id='sub_123456'
        )
    
    @pytest.fixture
    def invoice(self, tenant_br, subscription):
        """Fixture para fatura"""
        return Invoice.objects.create(
            tenant=tenant_br,
            subscription=subscription,
            invoice_number='INV-2025-0001',
            amount=Decimal('297.00'),
            currency='BRL',
            total_amount=Decimal('297.00'),
            status='open',
            issue_date=timezone.now().date(),
            due_date=timezone.now().date() + timedelta(days=7),
            gateway_invoice_id='inv_123456'
        )
    
    @pytest.fixture
    def payment(self, tenant_br, invoice):
        """Fixture para pagamento"""
        return Payment.objects.create(
            invoice=invoice,
            tenant=tenant_br,
            amount=Decimal('297.00'),
            currency='BRL',
            status='processing',
            payment_method_type='card',
            gateway='asaas',
            gateway_payment_id='pay_123456'
        )
    
    def test_webhook_payment_confirmed(self, payment, invoice, subscription):
        """Testa webhook de pagamento confirmado"""
        # Simular webhook do Asaas
        from apps.billing.services import PaymentService
        
        payment = PaymentService.mark_payment_succeeded(
            payment,
            gateway_payment_id='pay_123456'
        )
        
        assert payment.status == 'succeeded'
        
        # Verificar se fatura foi atualizada
        invoice.refresh_from_db()
        assert invoice.status == 'paid'
        assert invoice.paid_at is not None
        
        # Verificar se assinatura continua ativa
        subscription.refresh_from_db()
        assert subscription.status == 'active'
    
    def test_webhook_payment_failed(self, payment, invoice, subscription):
        """Testa webhook de pagamento falhado"""
        from apps.billing.services import PaymentService
        
        payment = PaymentService.mark_payment_failed(
            payment,
            reason='Cartão recusado'
        )
        
        assert payment.status == 'failed'
        assert payment.failure_reason == 'Cartão recusado'
        
        # Verificar se assinatura foi marcada como past_due
        subscription.refresh_from_db()
        assert subscription.status == 'past_due'


@pytest.mark.django_db
class TestBillingFlows:
    """Testes de fluxos completos de billing"""
    
    @pytest.fixture
    def tenant_br(self):
        """Fixture para tenant brasileiro"""
        return Tenant.objects.create(
            name='Construtora BR',
            slug='construtora-br',
            domain='construtora-br.structurone.com',
            email='contato@construtora-br.com',
            country='BR',
            currency='BRL'
        )
    
    @pytest.fixture
    def user_br(self, tenant_br):
        """Fixture para usuário brasileiro"""
        return User.objects.create_user(
            email='user@construtora-br.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=tenant_br
        )
    
    @pytest.fixture
    def plan_basic(self):
        """Fixture para plano básico"""
        return Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
            price_yearly_brl=Decimal('2970.00'),
            max_projects=5,
            max_users=5,
            trial_days=14,
            is_active=True
        )
    
    def test_complete_subscription_flow(self, tenant_br, plan_basic):
        """Testa fluxo completo de assinatura"""
        from apps.billing.services import BillingService, InvoiceService, PaymentService
        
        # 1. Criar assinatura
        subscription = BillingService.create_subscription(
            tenant=tenant_br,
            plan=plan_basic,
            billing_cycle='monthly'
        )
        
        assert subscription.status == 'trialing'  # Com trial
        assert subscription.gateway == 'asaas'
        
        # 2. Gerar fatura
        invoice = InvoiceService.generate_invoice(subscription)
        
        assert invoice.amount == Decimal('297.00')
        assert invoice.status == 'open'
        assert invoice.invoice_number.startswith('INV-')
        
        # 3. Criar método de pagamento
        payment_method = PaymentMethod.objects.create(
            tenant=tenant_br,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_123456',
            card_last4='4242',
            is_default=True
        )
        
        # 4. Processar pagamento
        payment = PaymentService.process_payment(invoice, payment_method)
        
        assert payment.status == 'processing'
        assert payment.payment_method == payment_method
        
        # 5. Marcar como sucesso (simulando webhook)
        payment = PaymentService.mark_payment_succeeded(
            payment,
            gateway_payment_id='pay_123456'
        )
        
        assert payment.status == 'succeeded'
        
        # Verificar fatura
        invoice.refresh_from_db()
        assert invoice.status == 'paid'
        
        # Verificar assinatura
        subscription.refresh_from_db()
        # Se plano tem trial, status será 'trialing', senão 'active'
        expected_status = 'trialing' if plan_basic.trial_days > 0 else 'active'
        assert subscription.status == expected_status
    
    def test_upgrade_flow(self, tenant_br, plan_basic):
        """Testa fluxo completo de upgrade"""
        from apps.billing.services import BillingService
        
        # Criar plano profissional
        plan_professional = Plan.objects.create(
            name='Profissional',
            slug='professional',
            price_monthly_brl=Decimal('797.00'),
            max_projects=20,
            max_users=20,
            is_active=True
        )
        
        # Criar assinatura básica
        subscription = BillingService.create_subscription(
            tenant=tenant_br,
            plan=plan_basic,
            billing_cycle='monthly'
        )
        
        # Verificar limites iniciais
        tenant_br.refresh_from_db()
        assert tenant_br.max_projects == 5
        
        # Fazer upgrade
        subscription, adjustment_invoice = BillingService.upgrade_subscription(
            subscription,
            plan_professional
        )
        
        # Verificar novos limites
        tenant_br.refresh_from_db()
        assert tenant_br.max_projects == 20
        assert tenant_br.subscription_plan == 'professional'
        
        # Verificar se invoice de ajuste foi criada
        if adjustment_invoice:
            assert adjustment_invoice.amount > 0

