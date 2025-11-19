"""
Testes unitários para Models de Billing
"""
import pytest
from decimal import Decimal
from django.utils import timezone
from datetime import timedelta
from apps.billing.models import Plan, Subscription, Invoice, Payment, PaymentMethod
from apps.tenants.models import Tenant


@pytest.mark.django_db
class TestPlan:
    """Testes para modelo Plan"""
    
    def test_create_plan(self):
        """Testa criação de plano"""
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            description='Plano básico',
            price_monthly_brl=Decimal('297.00'),
            price_yearly_brl=Decimal('2970.00'),
            price_monthly_usd=Decimal('49.00'),
            price_yearly_usd=Decimal('490.00'),
            max_projects=5,
            max_users=5,
            max_storage_gb=5,
            features=['Relatórios básicos'],
            trial_days=14
        )
        
        assert plan.name == 'Básico'
        assert plan.slug == 'basic'
        assert plan.price_monthly_brl == Decimal('297.00')
        assert plan.is_active is True
        assert plan.trial_days == 14
    
    def test_get_price_for_country_br_monthly(self):
        """Testa obtenção de preço para Brasil mensal"""
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
            price_yearly_brl=Decimal('2970.00'),
        )
        
        price = plan.get_price_for_country('BR', 'monthly')
        assert price == Decimal('297.00')
    
    def test_get_price_for_country_br_yearly(self):
        """Testa obtenção de preço para Brasil anual"""
        plan = Plan.objects.create(
            name='Básico',
            slug='basic',
            price_monthly_brl=Decimal('297.00'),
            price_yearly_brl=Decimal('2970.00'),
        )
        
        price = plan.get_price_for_country('BR', 'yearly')
        assert price == Decimal('2970.00')
    
    def test_get_price_for_country_us_monthly(self):
        """Testa obtenção de preço para USA mensal"""
        plan = Plan.objects.create(
            name='Starter',
            slug='starter',
            price_monthly_usd=Decimal('49.00'),
            price_yearly_usd=Decimal('490.00'),
        )
        
        price = plan.get_price_for_country('US', 'monthly')
        assert price == Decimal('49.00')
    
    def test_get_price_for_country_default(self):
        """Testa obtenção de preço padrão (USD)"""
        plan = Plan.objects.create(
            name='Starter',
            slug='starter',
            price_monthly_usd=Decimal('49.00'),
        )
        
        price = plan.get_price_for_country('MX', 'monthly')  # País não configurado
        assert price == Decimal('49.00')  # Default USD


@pytest.mark.django_db
class TestSubscription:
    """Testes para modelo Subscription"""
    
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
        )
        
        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status='active',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
            gateway='asaas'
        )
        
        assert subscription.tenant == tenant
        assert subscription.plan == plan
        assert subscription.status == 'active'
        assert subscription.gateway == 'asaas'
    
    def test_is_active_property(self):
        """Testa propriedade is_active"""
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
        
        assert subscription.is_active is True
        
        subscription.status = 'canceled'
        subscription.save()
        assert subscription.is_active is False
    
    def test_is_trial_property(self):
        """Testa propriedade is_trial"""
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
        
        subscription = Subscription.objects.create(
            tenant=tenant,
            plan=plan,
            status='trialing',
            current_period_start=timezone.now().date(),
            current_period_end=timezone.now().date() + timedelta(days=30),
            trial_start=timezone.now().date(),
            trial_end=timezone.now().date() + timedelta(days=14),
        )
        
        assert subscription.is_trial is True
        
        subscription.trial_end = timezone.now().date() - timedelta(days=1)
        subscription.save()
        assert subscription.is_trial is False


@pytest.mark.django_db
class TestInvoice:
    """Testes para modelo Invoice"""
    
    def test_create_invoice(self):
        """Testa criação de fatura"""
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
        
        assert invoice.invoice_number == 'INV-2025-0001'
        assert invoice.amount == Decimal('297.00')
        assert invoice.status == 'open'
        assert invoice.tenant == tenant


@pytest.mark.django_db
class TestPayment:
    """Testes para modelo Payment"""
    
    def test_create_payment(self):
        """Testa criação de pagamento"""
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
            status='pending',
            payment_method_type='card',
            gateway='asaas'
        )
        
        assert payment.invoice == invoice
        assert payment.amount == Decimal('297.00')
        assert payment.status == 'pending'
        assert payment.gateway == 'asaas'


@pytest.mark.django_db
class TestPaymentMethod:
    """Testes para modelo PaymentMethod"""
    
    def test_create_payment_method(self):
        """Testa criação de método de pagamento"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        payment_method = PaymentMethod.objects.create(
            tenant=tenant,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_123456',
            card_last4='4242',
            card_brand='visa',
            card_exp_month=12,
            card_exp_year=2025,
            is_default=True
        )
        
        assert payment_method.tenant == tenant
        assert payment_method.type == 'card'
        assert payment_method.card_last4 == '4242'
        assert payment_method.is_default is True
    
    def test_payment_method_str(self):
        """Testa string representation do método de pagamento"""
        tenant = Tenant.objects.create(
            name='Test Tenant',
            slug='test-tenant',
            domain='test.structurone.com',
            email='test@example.com',
            country='BR'
        )
        
        payment_method = PaymentMethod.objects.create(
            tenant=tenant,
            type='card',
            gateway='asaas',
            gateway_payment_method_id='pm_123456',
            card_last4='4242',
            card_brand='visa',
        )
        
        assert '4242' in str(payment_method)
        assert 'visa' in str(payment_method).lower()

