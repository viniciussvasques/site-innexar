"""
Tenant Admin
Django Admin configuration for Tenant
"""
from django.contrib import admin
from .models import Tenant


@admin.register(Tenant)
class TenantAdmin(admin.ModelAdmin):
    """Admin configuration for Tenant"""
    list_display = [
        'name',
        'slug',
        'domain',
        'email',
        'is_active',
        'subscription_plan',
        'is_subscription_active',
        'created_at',
    ]
    list_filter = [
        'is_active',
        'subscription_plan',
        'created_at',
    ]
    search_fields = [
        'name',
        'slug',
        'domain',
        'email',
    ]
    readonly_fields = [
        'created_at',
        'updated_at',
        'is_subscription_active',
    ]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('name', 'slug', 'domain', 'email', 'phone')
        }),
        ('Status', {
            'fields': ('is_active', 'subscription_plan')
        }),
        ('Assinatura', {
            'fields': (
                'subscription_start_date',
                'subscription_end_date',
                'is_subscription_active'
            )
        }),
        ('Limites', {
            'fields': ('max_projects', 'max_users')
        }),
        ('Observações', {
            'fields': ('notes',)
        }),
        ('Datas', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

