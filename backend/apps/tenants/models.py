"""
Tenant Models
Multi-tenant management models
"""
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from apps.core.models import TimeStampedModel


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
        default=timezone.now,
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

