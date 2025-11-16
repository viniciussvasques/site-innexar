"""
Model Mixins
Mixins para modelos que precisam de isolamento por tenant
"""
from django.db import models
from apps.core.managers import TenantManager


class TenantMixin(models.Model):
    """
    Mixin que adiciona campo tenant e filtragem automática
    """
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='%(class)s_set',
        verbose_name='Tenant',
        help_text='Tenant ao qual este registro pertence'
    )
    
    objects = TenantManager()
    
    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['tenant']),
        ]

