"""
Tenant Serializers
DRF serializers for Tenant API
"""
from rest_framework import serializers
from .models import Tenant


class TenantSerializer(serializers.ModelSerializer):
    """Serializer para Tenant"""
    is_subscription_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
            'slug',
            'domain',
            'email',
            'phone',
            'is_active',
            'subscription_plan',
            'subscription_start_date',
            'subscription_end_date',
            'max_projects',
            'max_users',
            'notes',
            'is_subscription_active',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'is_subscription_active']

    def validate_slug(self, value):
        """Valida o slug"""
        if self.instance and self.instance.slug == value:
            return value
        if Tenant.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Um tenant com este slug já existe.")
        return value

    def validate_domain(self, value):
        """Valida o domínio"""
        if self.instance and self.instance.domain == value:
            return value
        if Tenant.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Um tenant com este domínio já existe.")
        return value


class TenantListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de tenants"""
    is_subscription_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
            'slug',
            'domain',
            'email',
            'is_active',
            'subscription_plan',
            'is_subscription_active',
            'created_at',
        ]


class TenantCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de tenant"""
    
    class Meta:
        model = Tenant
        fields = [
            'name',
            'slug',
            'domain',
            'email',
            'phone',
            'subscription_plan',
            'max_projects',
            'max_users',
            'notes',
        ]

    def validate_slug(self, value):
        """Valida o slug"""
        if Tenant.objects.filter(slug=value).exists():
            raise serializers.ValidationError("Um tenant com este slug já existe.")
        return value

    def validate_domain(self, value):
        """Valida o domínio"""
        if Tenant.objects.filter(domain=value).exists():
            raise serializers.ValidationError("Um tenant com este domínio já existe.")
        return value

