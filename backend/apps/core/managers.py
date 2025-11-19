"""
Custom Managers
Managers customizados para filtrar por tenant automaticamente
"""
from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.db.models import QuerySet


class TenantQuerySet(QuerySet):
    """
    QuerySet que filtra automaticamente por tenant
    """
    def filter_by_tenant(self, tenant):
        """Filtra por tenant"""
        if tenant:
            return self.filter(tenant=tenant)
        return self.none()
    
    def for_request(self, request):
        """Filtra automaticamente pelo tenant da requisição"""
        tenant = getattr(request, 'tenant', None)
        if tenant:
            return self.filter(tenant=tenant)
        return self.none()


class TenantManager(models.Manager):
    """
    Manager que filtra automaticamente por tenant
    """
    def get_queryset(self):
        """Retorna QuerySet customizado"""
        return TenantQuerySet(self.model, using=self._db)
    
    def filter_by_tenant(self, tenant):
        """Filtra por tenant"""
        return self.get_queryset().filter_by_tenant(tenant)
    
    def for_request(self, request):
        """Filtra automaticamente pelo tenant da requisição"""
        return self.get_queryset().for_request(request)


class UserManager(BaseUserManager):
    """
    Manager customizado para User model com suporte a multi-tenant
    """
    use_in_migrations = True
    
    def _create_user(self, email, password, tenant, **extra_fields):
        """Cria e salva um usuário com email e senha"""
        if not email:
            raise ValueError('O email deve ser fornecido')
        if not tenant:
            raise ValueError('O tenant deve ser fornecido')
        
        email = self.normalize_email(email)
        user = self.model(email=email, tenant=tenant, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_user(self, email, password=None, tenant=None, **extra_fields):
        """Cria um usuário normal"""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, tenant, **extra_fields)
    
    def create_superuser(self, email, password=None, tenant=None, **extra_fields):
        """Cria um superusuário"""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self._create_user(email, password, tenant, **extra_fields)
    
    def get_by_natural_key(self, email):
        """Permite buscar usuário por email (sem tenant)"""
        return self.get(email=email)

