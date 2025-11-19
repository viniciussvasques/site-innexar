"""
Core Models
Models principais do sistema incluindo User customizado
"""
import secrets
from datetime import timedelta
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.core.validators import RegexValidator
from apps.core.mixins import TenantMixin
from apps.core.managers import TenantManager, UserManager


class TimeStampedModel(models.Model):
    """
    Abstract base model with created_at and updated_at fields
    """
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, TimeStampedModel, TenantMixin):
    """
    Custom User model vinculado a um tenant
    Usa email como username principal
    """
    # Remover username, usar email como login
    username = None
    
    email = models.EmailField(
        unique=True,  # Único globalmente (mas validaremos por tenant no serializer/service)
        verbose_name='Email',
        help_text='Email usado para login'
    )
    
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Tenant',
        help_text='Tenant ao qual este usuário pertence'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone',
        help_text='Telefone de contato'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar',
        help_text='Foto de perfil do usuário'
    )
    
    role = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Administrador'),
            ('manager', 'Gerente'),
            ('user', 'Usuário'),
            ('viewer', 'Visualizador'),
        ],
        default='user',
        verbose_name='Função',
        help_text='Função/permissão do usuário no tenant'
    )
    
    onboarding_completed = models.BooleanField(
        default=False,
        verbose_name='Onboarding Completo',
        help_text='Indica se o usuário completou o onboarding'
    )
    
    onboarding_step = models.IntegerField(
        default=0,
        verbose_name='Etapa do Onboarding',
        help_text='Etapa atual do onboarding (0-4)'
    )
    
    failed_login_attempts = models.IntegerField(
        default=0,
        verbose_name='Tentativas de Login Falhas',
        help_text='Número de tentativas de login falhas consecutivas'
    )
    
    locked_until = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Bloqueado até',
        help_text='Data/hora até a qual a conta está bloqueada'
    )
    
    objects = UserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'tenant']
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        # Nota: Email é único globalmente, mas validaremos por tenant no service
        indexes = [
            models.Index(fields=['email', 'tenant']),
            models.Index(fields=['tenant', 'is_active']),
            models.Index(fields=['tenant', 'role']),
        ]
        ordering = ['email']
    
    def __str__(self):
        return f"{self.email} ({self.tenant.name})"
    
    def get_full_name(self):
        """Retorna nome completo"""
        return f"{self.first_name} {self.last_name}".strip() or self.email
    
    def get_short_name(self):
        """Retorna primeiro nome"""
        return self.first_name or self.email.split('@')[0]
    
    def is_locked(self):
        """Verifica se a conta está bloqueada"""
        if self.locked_until:
            return timezone.now() < self.locked_until
        return False
    
    def increment_failed_login(self):
        """Incrementa tentativas falhas e bloqueia se necessário"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 3:
            self.locked_until = timezone.now() + timedelta(minutes=5)
        self.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    def reset_failed_login(self):
        """Reseta tentativas falhas após login bem-sucedido"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    def is_first_user_of_tenant(self):
        """Verifica se é o primeiro usuário do tenant"""
        return User.objects.filter(tenant=self.tenant).count() == 1


class PasswordResetToken(TimeStampedModel):
    """
    Token para reset de senha
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name='Usuário',
        help_text='Usuário que solicitou o reset de senha'
    )
    
    token = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Token',
        help_text='Token único para reset de senha'
    )
    
    expires_at = models.DateTimeField(
        verbose_name='Expira em',
        help_text='Data/hora de expiração do token'
    )
    
    used = models.BooleanField(
        default=False,
        verbose_name='Usado',
        help_text='Indica se o token já foi usado'
    )
    
    class Meta:
        verbose_name = 'Token de Reset de Senha'
        verbose_name_plural = 'Tokens de Reset de Senha'
        indexes = [
            models.Index(fields=['token', 'used']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['user', 'used']),
        ]
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Token para {self.user.email} (expira em {self.expires_at})"
    
    def is_valid(self):
        """Verifica se o token é válido"""
        return not self.used and timezone.now() < self.expires_at
    
    @classmethod
    def generate_token(cls):
        """Gera um token único"""
        return secrets.token_urlsafe(32)
    
    @classmethod
    def create_for_user(cls, user):
        """Cria um token de reset para o usuário"""
        token = cls.generate_token()
        expires_at = timezone.now() + timedelta(hours=24)
        return cls.objects.create(
            user=user,
            token=token,
            expires_at=expires_at
        )


class OnboardingProgress(TimeStampedModel, TenantMixin):
    """
    Progresso do onboarding do tenant
    """
    tenant = models.OneToOneField(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='onboarding',
        verbose_name='Tenant',
        help_text='Tenant que está fazendo onboarding'
    )
    
    step = models.IntegerField(
        default=0,
        verbose_name='Etapa Atual',
        help_text='Etapa atual do onboarding (0-4)'
    )
    
    completed = models.BooleanField(
        default=False,
        verbose_name='Completo',
        help_text='Indica se o onboarding foi completado'
    )
    
    data = models.JSONField(
        default=dict,
        verbose_name='Dados Coletados',
        help_text='Dados coletados durante o onboarding'
    )
    
    objects = TenantManager()
    
    class Meta:
        verbose_name = 'Progresso do Onboarding'
        verbose_name_plural = 'Progressos de Onboarding'
        indexes = [
            models.Index(fields=['tenant', 'completed']),
        ]
    
    def __str__(self):
        status = "Completo" if self.completed else f"Etapa {self.step}/4"
        return f"Onboarding {self.tenant.name} - {status}"
    
    def update_step(self, step, data=None):
        """Atualiza a etapa do onboarding"""
        self.step = step
        if data:
            self.data.update(data)
        self.save(update_fields=['step', 'data', 'updated_at'])
    
    def complete(self):
        """Marca o onboarding como completo"""
        self.completed = True
        self.step = 4
        self.save(update_fields=['completed', 'step', 'updated_at'])

