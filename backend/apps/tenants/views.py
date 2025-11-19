"""
Tenants API Views
"""
import secrets
import logging
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from django.db.models import Count, Q
from django.contrib.auth import get_user_model
from django.db import IntegrityError
from .models import Tenant
from .serializers import (
    TenantSerializer,
    TenantListSerializer,
    TenantCreateSerializer,
)

User = get_user_model()
logger = logging.getLogger(__name__)


class TenantViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gerenciamento de Tenants
    """
    queryset = Tenant.objects.all()
    permission_classes = [IsAuthenticated]  # Temporariamente sem IsAdminUser para facilitar desenvolvimento

    def get_serializer_class(self):
        """Retorna o serializer apropriado para cada ação"""
        if self.action == 'create':
            return TenantCreateSerializer
        elif self.action == 'list':
            return TenantListSerializer
        return TenantSerializer

    @action(detail=False, methods=['get'], url_path='check-slug', permission_classes=[])
    def check_slug(self, request):
        """Verifica disponibilidade de slug de tenant (subdomínio)"""
        from django.utils.text import slugify

        raw_slug = request.query_params.get('slug', '').strip().lower()
        if not raw_slug:
            return Response(
                {'detail': 'slug é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        normalized_slug = slugify(raw_slug)
        if not normalized_slug:
            return Response(
                {'detail': 'slug inválido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        exists = Tenant.objects.filter(slug=normalized_slug).exists()
        return Response({
            'slug': normalized_slug,
            'available': not exists,
        })

    def create(self, request, *args, **kwargs):
        """Criar tenant, criar primeiro usuário admin e retornar credenciais"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        tenant = serializer.save()
        
        # Criar primeiro usuário admin do tenant
        admin_email = tenant.email
        admin_password = secrets.token_urlsafe(12)  # Senha aleatória segura
        
        try:
            # Verificar se email já existe (mesmo que em outro tenant)
            if User.objects.filter(email=admin_email).exists():
                # Se já existe, usar um email alternativo
                admin_email = f"admin-{tenant.slug}@structurone.com"
            
            admin_user = User.objects.create_user(
                email=admin_email,
                password=admin_password,
                tenant=tenant,
                first_name='Admin',
                last_name=tenant.name,
                role='admin',
                is_active=True,
            )
        except IntegrityError as e:
            # Email duplicado - tentar com email alternativo
            logger.warning(f'Email {admin_email} já existe, usando alternativo: {e}')
            admin_email = f"admin-{tenant.slug}@structurone.com"
            try:
                admin_user = User.objects.create_user(
                    email=admin_email,
                    password=admin_password,
                    tenant=tenant,
                    first_name='Admin',
                    last_name=tenant.name,
                    role='admin',
                    is_active=True,
                )
            except Exception as e2:
                logger.error(f'Erro ao criar usuário admin com email alternativo: {e2}')
                return Response({
                    'detail': f'Erro ao criar usuário administrador: {str(e2)}'
                }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            logger.error(f'Erro inesperado ao criar usuário admin: {e}')
            return Response({
                'detail': f'Erro ao criar usuário administrador: {str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        # Retornar tenant com credenciais
        response_data = TenantSerializer(tenant).data
        response_data['admin_credentials'] = {
            'email': admin_email,
            'password': admin_password,
            'user_id': admin_user.id,
        }
        
        headers = self.get_success_headers(response_data)
        return Response(response_data, status=status.HTTP_201_CREATED, headers=headers)

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
    
    @action(detail=True, methods=['get'])
    def admin_credentials(self, request, pk=None):
        """Retorna credenciais do primeiro usuário admin do tenant"""
        tenant = self.get_object()
        admin_user = User.objects.filter(tenant=tenant, role='admin').first()
        
        if not admin_user:
            return Response({
                'detail': 'Nenhum usuário admin encontrado para este tenant.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        return Response({
            'email': admin_user.email,
            'user_id': admin_user.id,
            'note': 'A senha não pode ser recuperada. Use o endpoint de reset para definir uma nova senha.'
        })
    
    @action(detail=True, methods=['post'])
    def reset_admin_password(self, request, pk=None):
        """Reseta a senha do primeiro usuário admin do tenant"""
        tenant = self.get_object()
        admin_user = User.objects.filter(tenant=tenant, role='admin').first()
        
        if not admin_user:
            return Response({
                'detail': 'Nenhum usuário admin encontrado para este tenant.'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Gerar nova senha
        new_password = secrets.token_urlsafe(12)
        admin_user.set_password(new_password)
        admin_user.save(update_fields=['password'])
        
        return Response({
            'email': admin_user.email,
            'new_password': new_password,
            'message': 'Senha resetada com sucesso.'
        })


@permission_classes([IsAuthenticated])
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

