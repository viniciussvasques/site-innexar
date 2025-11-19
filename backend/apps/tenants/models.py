"""
Tenant Models
Multi-tenant management models
"""
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from apps.core.models import TimeStampedModel


def get_default_subscription_start_date():
    """Retorna a data atual para subscription_start_date"""
    return timezone.now().date()


class Tenant(TimeStampedModel):
    """
    Tenant model - represents a client/company in the multi-tenant system
    """
    name = models.CharField(
        max_length=255,
        verbose_name='Nome',
        help_text='Nome da empresa/cliente'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='Slug',
        help_text='Identificador único da URL (ex: empresa-abc)',
        validators=[
            RegexValidator(
                regex=r'^[a-z0-9-]+$',
                message='Slug deve conter apenas letras minúsculas, números e hífens'
            )
        ]
    )
    domain = models.CharField(
        max_length=255,
        unique=True,
        verbose_name='Domínio',
        help_text='Domínio do tenant (ex: empresa.structurone.com)'
    )
    email = models.EmailField(
        verbose_name='Email',
        help_text='Email de contato principal'
    )
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone',
        help_text='Telefone de contato'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Ativo',
        help_text='Se o tenant está ativo'
    )
    subscription_plan = models.CharField(
        max_length=50,
        choices=[
            ('free', 'Gratuito'),
            ('basic', 'Básico'),
            ('professional', 'Profissional'),
            ('enterprise', 'Enterprise'),
        ],
        default='basic',
        verbose_name='Plano',
        help_text='Plano de assinatura'
    )
    subscription_start_date = models.DateField(
        default=get_default_subscription_start_date,
        verbose_name='Data de Início',
        help_text='Data de início da assinatura'
    )
    subscription_end_date = models.DateField(
        null=True,
        blank=True,
        verbose_name='Data de Término',
        help_text='Data de término da assinatura (opcional)'
    )
    max_projects = models.IntegerField(
        default=10,
        verbose_name='Máximo de Projetos',
        help_text='Número máximo de projetos permitidos'
    )
    max_users = models.IntegerField(
        default=5,
        verbose_name='Máximo de Usuários',
        help_text='Número máximo de usuários permitidos'
    )
    notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observações',
        help_text='Observações internas sobre o tenant'
    )
    stripe_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Stripe Customer ID',
        help_text='Identificador do cliente no Stripe'
    )
    asaas_customer_id = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name='Asaas Customer ID',
        help_text='Identificador do cliente no Asaas'
    )
    
    # Internacionalização
    language = models.CharField(
        max_length=10,
        choices=[
            ('pt-br', 'Português (Brasil)'),
            ('en-us', 'English (US)'),
            ('es-es', 'Español (España)'),
        ],
        default='pt-br',
        verbose_name='Idioma',
        help_text='Idioma padrão do tenant'
    )
    
    country = models.CharField(
        max_length=2,
        choices=[
            ('BR', 'Brasil'),
            ('US', 'Estados Unidos'),
            ('MX', 'México'),
            ('ES', 'Espanha'),
            ('AR', 'Argentina'),
            ('CO', 'Colômbia'),
            ('CL', 'Chile'),
            ('PE', 'Peru'),
            ('EC', 'Equador'),
            ('VE', 'Venezuela'),
            ('UY', 'Uruguai'),
            ('PY', 'Paraguai'),
            ('BO', 'Bolívia'),
            ('CR', 'Costa Rica'),
            ('PA', 'Panamá'),
            ('GT', 'Guatemala'),
            ('DO', 'República Dominicana'),
            ('CU', 'Cuba'),
            ('HN', 'Honduras'),
            ('NI', 'Nicarágua'),
            ('SV', 'El Salvador'),
        ],
        default='BR',
        verbose_name='País',
        help_text='País do tenant'
    )
    
    currency = models.CharField(
        max_length=3,
        choices=[
            ('BRL', 'Real Brasileiro (R$)'),
            ('USD', 'Dólar Americano ($)'),
            ('EUR', 'Euro (€)'),
            ('MXN', 'Peso Mexicano (MX$)'),
            ('ARS', 'Peso Argentino ($)'),
            ('COP', 'Peso Colombiano ($)'),
            ('CLP', 'Peso Chileno ($)'),
            ('PEN', 'Sol Peruano (S/)'),
            ('UYU', 'Peso Uruguaio ($U)'),
            ('PYG', 'Guarani Paraguaio (₲)'),
            ('BOB', 'Boliviano (Bs.)'),
            ('CRC', 'Colón Costarriquenho (₡)'),
            ('DOP', 'Peso Dominicano (RD$)'),
            ('CUP', 'Peso Cubano ($)'),
            ('GTQ', 'Quetzal Guatemalteco (Q)'),
            ('HNL', 'Lempira Hondurenha (L)'),
            ('NIO', 'Córdoba Nicaraguense (C$)'),
            ('PAB', 'Balboa Panamenho (B/.)'),
            ('SVC', 'Colón Salvadorenho (₡)'),
        ],
        default='BRL',
        verbose_name='Moeda',
        help_text='Moeda padrão do tenant'
    )
    
    timezone = models.CharField(
        max_length=50,
        default='America/Sao_Paulo',
        verbose_name='Fuso Horário',
        help_text='Fuso horário do tenant'
    )
    
    date_format = models.CharField(
        max_length=20,
        choices=[
            ('DD/MM/YYYY', 'DD/MM/YYYY'),
            ('MM/DD/YYYY', 'MM/DD/YYYY'),
            ('YYYY-MM-DD', 'YYYY-MM-DD'),
        ],
        default='DD/MM/YYYY',
        verbose_name='Formato de Data',
        help_text='Formato de exibição de datas'
    )
    
    number_format = models.CharField(
        max_length=20,
        choices=[
            ('1.234,56', '1.234,56 (Brasil/Espanha)'),
            ('1,234.56', '1,234.56 (EUA)'),
        ],
        default='1.234,56',
        verbose_name='Formato de Número',
        help_text='Formato de exibição de números decimais'
    )

    class Meta:
        verbose_name = 'Tenant'
        verbose_name_plural = 'Tenants'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['domain']),
            models.Index(fields=['is_active']),
        ]

    def __str__(self):
        return f"{self.name} ({self.slug})"

    @property
    def is_subscription_active(self):
        """Verifica se a assinatura está ativa"""
        if not self.is_active:
            return False
        if self.subscription_end_date:
            return timezone.now().date() <= self.subscription_end_date
        return True

    def can_create_project(self, current_count):
        """Verifica se pode criar mais projetos"""
        return current_count < self.max_projects

    def can_add_user(self, current_count):
        """Verifica se pode adicionar mais usuários"""
        return current_count < self.max_users

