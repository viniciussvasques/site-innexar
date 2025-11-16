"""
Tenants API Views
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Q
from .models import Tenant
from .serializers import (
    TenantSerializer,
    TenantListSerializer,
    TenantCreateSerializer,
)


class TenantViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Tenants
    """
    queryset = Tenant.objects.all()
    permission_classes = [IsAuthenticated, IsAdminUser]

    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'create':
            return TenantCreateSerializer
        elif self.action == 'list':
            return TenantListSerializer
        return TenantSerializer

    def get_queryset(self):
        """Filtra tenants baseado em parâmetros"""
        queryset = Tenant.objects.all()
        
        # Filtro por status
        is_active = self.request.query_params.get('is_active', None)
        if is_active is not None:
            queryset = queryset.filter(is_active=is_active.lower() == 'true')
        
        # Filtro por plano
        subscription_plan = self.request.query_params.get('subscription_plan', None)
        if subscription_plan:
            queryset = queryset.filter(subscription_plan=subscription_plan)
        
        # Busca por nome, slug ou email
        search = self.request.query_params.get('search', None)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(slug__icontains=search) |
                Q(email__icontains=search)
            )
        
        return queryset.order_by('-created_at')

    @action(detail=True, methods=['post'])
    def activate(self, request, pk=None):
        """Ativa um tenant"""
        tenant = self.get_object()
        tenant.is_active = True
        tenant.save()
        serializer = self.get_serializer(tenant)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
        """Desativa um tenant"""
        tenant = self.get_object()
        tenant.is_active = False
        tenant.save()
        serializer = self.get_serializer(tenant)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def stats(self, request, pk=None):
        """Estatísticas do tenant"""
        tenant = self.get_object()
        # TODO: Adicionar estatísticas reais quando houver outros módulos
        stats = {
            'id': tenant.id,
            'name': tenant.name,
            'is_active': tenant.is_active,
            'is_subscription_active': tenant.is_subscription_active,
            'projects_count': 0,  # Será implementado quando módulo projects estiver pronto
            'users_count': 0,  # Será implementado quando módulo users estiver pronto
            'max_projects': tenant.max_projects,
            'max_users': tenant.max_users,
        }
        return Response(stats)


@permission_classes([IsAuthenticated, IsAdminUser])
def tenant_stats(request):
    """Estatísticas gerais de todos os tenants"""
    total_tenants = Tenant.objects.count()
    active_tenants = Tenant.objects.filter(is_active=True).count()
    inactive_tenants = total_tenants - active_tenants
    
    # Contagem por plano
    plans = Tenant.objects.values('subscription_plan').annotate(
        count=Count('id')
    )
    
    stats = {
        'total': total_tenants,
        'active': active_tenants,
        'inactive': inactive_tenants,
        'by_plan': {item['subscription_plan']: item['count'] for item in plans},
    }
    
    return Response(stats)

