"""
Billing Models
Modelos para planos, assinaturas, faturas e pagamentos
"""
from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.core.models import TimeStampedModel
from apps.tenants.models import Tenant


class Plan(TimeStampedModel):
    """
    Modelo de plano de assinatura
    O preço é determinado pelo país de registro da empresa (tenant.country)
    Uma empresa brasileira paga em BRL via Asaas, mesmo que construa nos EUA
    Uma empresa americana paga em USD via Stripe, mesmo que construa no Brasil
    """
    name = models.CharField(
        max_length=100,
        verbose_name='Nome',
        help_text='Nome do plano (ex: "Básico", "Profissional", "Starter")'
    )
    slug = models.SlugField(
        unique=True,
        verbose_name='Slug',
        help_text='Identificador único do plano (ex: "basic", "professional")'
    )
    description = models.TextField(
        blank=True,
        verbose_name='Descrição',
        help_text='Descrição do plano'
    )
    
    # Preços por moeda (baseado no país de registro do tenant)
    # Se tenant.country = 'BR' → usa price_monthly_brl
    # Se tenant.country = 'US' → usa price_monthly_usd
    price_monthly_brl = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço Mensal (BRL)',
        help_text='Preço mensal em Reais Brasileiros'
    )
    price_yearly_brl = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço Anual (BRL)',
        help_text='Preço anual em Reais Brasileiros'
    )
    price_monthly_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço Mensal (USD)',
        help_text='Preço mensal em Dólares Americanos'
    )
    price_yearly_usd = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Preço Anual (USD)',
        help_text='Preço anual em Dólares Americanos'
    )
    
    # Moeda padrão (para exibição)
    currency = models.CharField(
        max_length=3,
        default='BRL',
        choices=[('BRL', 'Real Brasileiro'), ('USD', 'Dólar Americano'), ('EUR', 'Euro')],
        verbose_name='Moeda Padrão',
        help_text='Moeda padrão para exibição'
    )
    
    # Limites
    max_projects = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Máximo de Projetos',
        help_text='Número máximo de projetos permitidos (0 = ilimitado)'
    )
    max_users = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Máximo de Usuários',
        help_text='Número máximo de usuários permitidos (0 = ilimitado)'
    )
    max_storage_gb = models.IntegerField(
        default=1,
        validators=[MinValueValidator(0)],
        verbose_name='Armazenamento (GB)',
        help_text='Armazenamento máximo em GB (0 = ilimitado)'
    )
    
    # Features (JSON)
    features = models.JSONField(
        default=list,
        verbose_name='Features',
        help_text='Lista de features do plano (ex: ["Relatórios", "API", "Suporte 24/7"])'
    )
    
    # Status
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Se o plano está ativo e disponível para assinatura'
    )
    is_featured = models.BooleanField(
        default=False,
        verbose_name='Destaque',
        help_text='Se o plano deve ser destacado na página de planos'
    )
    
    # Trial
    trial_days = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
        verbose_name='Dias de Trial',
        help_text='Número de dias de trial grátis (0 = sem trial)'
    )
    
    # Ordem de exibição
    display_order = models.IntegerField(
        default=0,
        verbose_name='Ordem de Exibição',
        help_text='Ordem de exibição na página de planos'
    )
    
    class Meta:
        verbose_name = 'Plano'
        verbose_name_plural = 'Planos'
        ordering = ['display_order', 'price_monthly_brl']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} ({self.slug})"
    
    def get_price_for_country(self, country: str, billing_cycle: str = 'monthly') -> Decimal:
        """
        Retorna o preço do plano baseado no país e ciclo de cobrança
        
        Args:
            country: Código do país ('BR', 'US', etc.)
            billing_cycle: 'monthly' ou 'yearly'
            
        Returns:
            Preço em Decimal
        """
        if country == 'BR':
            if billing_cycle == 'yearly':
                return self.price_yearly_brl or Decimal('0.00')
            return self.price_monthly_brl or Decimal('0.00')
        elif country == 'US':
            if billing_cycle == 'yearly':
                return self.price_yearly_usd or Decimal('0.00')
            return self.price_monthly_usd or Decimal('0.00')
        # Default: USD
        if billing_cycle == 'yearly':
            return self.price_yearly_usd or Decimal('0.00')
        return self.price_monthly_usd or Decimal('0.00')


class Subscription(TimeStampedModel):
    """
    Modelo de assinatura do tenant
    """
    tenant = models.OneToOneField(
        Tenant,
        on_delete=models.CASCADE,
        related_name='subscription',
        verbose_name='Tenant',
        help_text='Tenant que possui esta assinatura'
    )
    plan = models.ForeignKey(
        Plan,
        on_delete=models.PROTECT,
        related_name='subscriptions',
        verbose_name='Plano',
        help_text='Plano de assinatura'
    )
    
    # Status
    STATUS_CHOICES = [
        ('trialing', 'Em Trial'),
        ('active', 'Ativa'),
        ('past_due', 'Pagamento Atrasado'),
        ('canceled', 'Cancelada'),
        ('unpaid', 'Não Paga'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='trialing',
        verbose_name='Status',
        help_text='Status da assinatura'
    )
    
    # Período
    current_period_start = models.DateField(
        verbose_name='Início do Período',
        help_text='Data de início do período atual'
    )
    current_period_end = models.DateField(
        verbose_name='Fim do Período',
        help_text='Data de fim do período atual'
    )
    
    # Trial
    trial_start = models.DateField(
        null=True,
        blank=True,
        verbose_name='Início do Trial',
        help_text='Data de início do trial'
    )
    trial_end = models.DateField(
        null=True,
        blank=True,
        verbose_name='Fim do Trial',
        help_text='Data de fim do trial'
    )
    
    # Cancelamento
    cancel_at_period_end = models.BooleanField(
        default=False,
        verbose_name='Cancelar ao Fim do Período',
        help_text='Se a assinatura será cancelada ao fim do período atual'
    )
    canceled_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Cancelada em',
        help_text='Data e hora do cancelamento'
    )
    cancellation_reason = models.TextField(
        blank=True,
        verbose_name='Motivo do Cancelamento',
        help_text='Motivo do cancelamento'
    )
    
    # Gateway
    gateway = models.CharField(
        max_length=20,
        default='asaas',
        choices=[('asaas', 'Asaas'), ('stripe', 'Stripe')],
        verbose_name='Gateway',
        help_text='Gateway de pagamento usado'
    )
    gateway_subscription_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='ID da Assinatura no Gateway',
        help_text='ID da assinatura no gateway de pagamento'
    )
    gateway_customer_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ID do Cliente no Gateway',
        help_text='ID do cliente no gateway de pagamento'
    )
    
    # Método de pagamento
    payment_method = models.ForeignKey(
        'billing.PaymentMethod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions',
        verbose_name='Método de Pagamento',
        help_text='Método de pagamento padrão'
    )
    
    class Meta:
        verbose_name = 'Assinatura'
        verbose_name_plural = 'Assinaturas'
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['current_period_end']),
        ]
    
    def __str__(self):
        return f"{self.tenant.name} - {self.plan.name} ({self.status})"
    
    @property
    def is_active(self) -> bool:
        """Verifica se a assinatura está ativa"""
        return self.status in ['trialing', 'active']
    
    @property
    def is_trial(self) -> bool:
        """Verifica se está em trial"""
        if not self.trial_end:
            return False
        return timezone.now().date() <= self.trial_end


class Invoice(TimeStampedModel):
    """
    Modelo de fatura
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='invoices',
        verbose_name='Tenant',
        help_text='Tenant que recebeu esta fatura'
    )
    subscription = models.ForeignKey(
        Subscription,
        on_delete=models.CASCADE,
        related_name='invoices',
        null=True,
        blank=True,
        verbose_name='Assinatura',
        help_text='Assinatura relacionada a esta fatura'
    )
    
    # Número único
    invoice_number = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Número da Fatura',
        help_text='Número único da fatura (ex: INV-2025-0001)'
    )
    
    # Valores
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor',
        help_text='Valor da fatura (sem impostos)'
    )
    currency = models.CharField(
        max_length=3,
        default='BRL',
        choices=[('BRL', 'Real Brasileiro'), ('USD', 'Dólar Americano'), ('EUR', 'Euro')],
        verbose_name='Moeda',
        help_text='Moeda da fatura'
    )
    tax_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=Decimal('0.00'),
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor de Impostos',
        help_text='Valor de impostos'
    )
    total_amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor Total',
        help_text='Valor total da fatura (com impostos)'
    )
    
    # Status
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('open', 'Aberta'),
        ('paid', 'Paga'),
        ('void', 'Cancelada'),
        ('uncollectible', 'Inadimplente'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='draft',
        verbose_name='Status',
        help_text='Status da fatura'
    )
    
    # Datas
    issue_date = models.DateField(
        verbose_name='Data de Emissão',
        help_text='Data de emissão da fatura'
    )
    due_date = models.DateField(
        verbose_name='Data de Vencimento',
        help_text='Data de vencimento da fatura'
    )
    paid_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='Paga em',
        help_text='Data e hora do pagamento'
    )
    
    # Gateway
    gateway_invoice_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ID da Fatura no Gateway',
        help_text='ID da fatura no gateway de pagamento'
    )
    gateway_pdf_url = models.URLField(
        null=True,
        blank=True,
        verbose_name='URL do PDF',
        help_text='URL do PDF da fatura no gateway'
    )
    
    # Detalhes
    line_items = models.JSONField(
        default=list,
        verbose_name='Itens da Fatura',
        help_text='Lista de itens da fatura'
    )
    notes = models.TextField(
        blank=True,
        verbose_name='Observações',
        help_text='Observações da fatura'
    )
    
    class Meta:
        verbose_name = 'Fatura'
        verbose_name_plural = 'Faturas'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['invoice_number']),
        ]
    
    def __str__(self):
        return f"{self.invoice_number} - {self.tenant.name} ({self.status})"


class Payment(TimeStampedModel):
    """
    Modelo de pagamento
    """
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Fatura',
        help_text='Fatura relacionada a este pagamento'
    )
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='payments',
        verbose_name='Tenant',
        help_text='Tenant que realizou este pagamento'
    )
    payment_method = models.ForeignKey(
        'billing.PaymentMethod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='Método de Pagamento',
        help_text='Método de pagamento usado'
    )
    
    # Valores
    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.00'))],
        verbose_name='Valor',
        help_text='Valor do pagamento'
    )
    currency = models.CharField(
        max_length=3,
        default='BRL',
        choices=[('BRL', 'Real Brasileiro'), ('USD', 'Dólar Americano'), ('EUR', 'Euro')],
        verbose_name='Moeda',
        help_text='Moeda do pagamento'
    )
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('succeeded', 'Sucesso'),
        ('failed', 'Falhou'),
        ('refunded', 'Reembolsado'),
        ('canceled', 'Cancelado'),
    ]
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Status',
        help_text='Status do pagamento'
    )
    
    # Método
    METHOD_CHOICES = [
        ('card', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
        ('ach', 'ACH (Transferência Bancária)'),
    ]
    payment_method_type = models.CharField(
        max_length=20,
        choices=METHOD_CHOICES,
        verbose_name='Tipo de Método',
        help_text='Tipo de método de pagamento'
    )
    
    # Gateway
    gateway = models.CharField(
        max_length=20,
        default='asaas',
        choices=[('asaas', 'Asaas'), ('stripe', 'Stripe')],
        verbose_name='Gateway',
        help_text='Gateway de pagamento usado'
    )
    gateway_payment_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True,
        verbose_name='ID do Pagamento no Gateway',
        help_text='ID do pagamento no gateway'
    )
    gateway_charge_id = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name='ID da Cobrança no Gateway',
        help_text='ID da cobrança no gateway'
    )
    
    # Falhas
    failure_reason = models.TextField(
        null=True,
        blank=True,
        verbose_name='Motivo da Falha',
        help_text='Motivo da falha no pagamento'
    )
    retry_count = models.IntegerField(
        default=0,
        verbose_name='Tentativas',
        help_text='Número de tentativas de pagamento'
    )
    max_retries = models.IntegerField(
        default=3,
        verbose_name='Máximo de Tentativas',
        help_text='Número máximo de tentativas'
    )
    
    # Metadata
    metadata = models.JSONField(
        default=dict,
        verbose_name='Metadados',
        help_text='Metadados adicionais do pagamento'
    )
    
    class Meta:
        verbose_name = 'Pagamento'
        verbose_name_plural = 'Pagamentos'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice']),
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['gateway_payment_id']),
        ]
    
    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.amount} {self.currency} ({self.status})"


class PaymentMethod(TimeStampedModel):
    """
    Modelo de método de pagamento (cartão, etc.)
    """
    tenant = models.ForeignKey(
        Tenant,
        on_delete=models.CASCADE,
        related_name='payment_methods',
        verbose_name='Tenant',
        help_text='Tenant que possui este método de pagamento'
    )
    
    # Tipo
    TYPE_CHOICES = [
        ('card', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
        ('pix', 'PIX'),
    ]
    type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        default='card',
        verbose_name='Tipo',
        help_text='Tipo de método de pagamento'
    )
    
    # Gateway
    gateway = models.CharField(
        max_length=20,
        default='asaas',
        choices=[('asaas', 'Asaas'), ('stripe', 'Stripe')],
        verbose_name='Gateway',
        help_text='Gateway de pagamento usado'
    )
    gateway_payment_method_id = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='ID do Método no Gateway',
        help_text='ID do método de pagamento no gateway'
    )
    
    # Status
    is_default = models.BooleanField(
        default=False,
        verbose_name='Padrão',
        help_text='Se este é o método de pagamento padrão'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Se o método de pagamento está ativo'
    )
    
    # Dados do cartão (apenas para exibição - nunca dados completos)
    card_last4 = models.CharField(
        max_length=4,
        null=True,
        blank=True,
        verbose_name='Últimos 4 Dígitos',
        help_text='Últimos 4 dígitos do cartão (apenas para exibição)'
    )
    card_brand = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        choices=[('visa', 'Visa'), ('mastercard', 'Mastercard'), ('amex', 'American Express'), ('discover', 'Discover')],
        verbose_name='Bandeira',
        help_text='Bandeira do cartão'
    )
    card_exp_month = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)],
        verbose_name='Mês de Expiração',
        help_text='Mês de expiração do cartão'
    )
    card_exp_year = models.IntegerField(
        null=True,
        blank=True,
        validators=[MinValueValidator(2020)],
        verbose_name='Ano de Expiração',
        help_text='Ano de expiração do cartão'
    )
    
    # Billing details
    billing_details = models.JSONField(
        default=dict,
        verbose_name='Detalhes de Cobrança',
        help_text='Detalhes de cobrança (nome, email, endereço)'
    )
    
    class Meta:
        verbose_name = 'Método de Pagamento'
        verbose_name_plural = 'Métodos de Pagamento'
        ordering = ['-is_default', '-created_at']
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['is_default']),
        ]
    
    def __str__(self):
        if self.type == 'card' and self.card_last4:
            return f"{self.get_card_brand_display()} •••• {self.card_last4}"
        return f"{self.get_type_display()} ({self.tenant.name})"

