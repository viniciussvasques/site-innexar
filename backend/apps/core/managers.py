"""
Custom Managers
Managers customizados para filtrar por tenant automaticamente
"""
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

