"""
Core Views
Views para autenticação, usuários e onboarding
"""
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import api_view, action, permission_classes
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils.translation import gettext_lazy as _
from apps.core.models import User, OnboardingProgress
from apps.core.serializers import (
    UserSerializer,
    UserListSerializer,
    UserCreateSerializer,
    LoginSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    OnboardingProgressSerializer,
    OnboardingCompleteSerializer,
)
from apps.core.services import (
    AuthService,
    PasswordResetService,
    OnboardingService,
)


@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def api_root(request):
    """
    API root endpoint
    """
    return Response({
        'name': 'StructurOne API',
        'version': '0.1.0',
        'endpoints': {
            'auth': '/api/auth/',
            'onboarding': '/api/onboarding/',
            'users': '/api/users/',
            'password-reset': '/api/password-reset/',
            'billing': '/api/billing/',
            'projects': '/api/projects/',
            'investors': '/api/investors/',
            'financial': '/api/financial/',
        }
    })


class AuthViewSet(viewsets.ViewSet):
    """ViewSet para autenticação"""
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'], url_path='register')
    def register(self, request):
        """Registra novo usuário"""
        serializer = UserCreateSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        try:
            user = serializer.save()
            
            # Gerar tokens
            from rest_framework_simplejwt.tokens import RefreshToken
            from apps.core.services import create_outstanding_token_for_access_token
            
            refresh = RefreshToken.for_user(user)
            access_token_str = str(refresh.access_token)
            tokens = {
                'access': access_token_str,
                'refresh': str(refresh),
            }
            
            # Criar OutstandingToken para access token
            create_outstanding_token_for_access_token(access_token_str, user)
            
            # Serializar resposta
            user_serializer = UserSerializer(user)
            
            return Response({
                'user': user_serializer.data,
                'tokens': tokens,
            }, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['post'], url_path='login')
    def login(self, request):
        """Faz login do usuário"""
        serializer = LoginSerializer(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        user = serializer.validated_data['user']
        
        # Gerar tokens
        from rest_framework_simplejwt.tokens import RefreshToken
        from apps.core.services import create_outstanding_token_for_access_token
        
        refresh = RefreshToken.for_user(user)
        access_token_str = str(refresh.access_token)
        tokens = {
            'access': access_token_str,
            'refresh': str(refresh),
        }
        
        # Criar OutstandingToken para access token
        create_outstanding_token_for_access_token(access_token_str, user)
        
        # Serializar resposta
        user_serializer = UserSerializer(user)
        
        return Response({
            'user': user_serializer.data,
            'tokens': tokens,
        }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='logout', permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """Faz logout do usuário (invalida refresh token e access token)"""
        refresh_token = request.data.get('refresh')
        
        if not refresh_token:
            return Response({
                'detail': _('Refresh token é obrigatório.')
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Extrair access token do header Authorization
        access_token = None
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Bearer '):
            access_token = auth_header.split(' ')[1]
        
        try:
            AuthService.logout_user(refresh_token, access_token)
            return Response({
                'message': _('Logout realizado com sucesso')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=False, methods=['get'], url_path='me', permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Retorna dados do usuário logado"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class PasswordResetViewSet(viewsets.ViewSet):
    """ViewSet para reset de senha"""
    permission_classes = [permissions.AllowAny]
    
    @action(detail=False, methods=['post'], url_path='request')
    def request_reset(self, request):
        """Solicita reset de senha"""
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        
        try:
            PasswordResetService.request_password_reset(email)
            return Response({
                'message': _('Email de recuperação enviado')
            }, status=status.HTTP_200_OK)
        except Exception as e:
            # Sempre retornar sucesso por segurança
            return Response({
                'message': _('Email de recuperação enviado')
            }, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='confirm')
    def confirm_reset(self, request):
        """Confirma reset de senha"""
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        token = serializer.validated_data['token']
        new_password = serializer.validated_data['new_password']
        
        try:
            PasswordResetService.confirm_password_reset(token, new_password)
            return Response({
                'message': _('Senha alterada com sucesso')
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class OnboardingViewSet(viewsets.ViewSet):
    """ViewSet para onboarding"""
    permission_classes = [permissions.IsAuthenticated]
    
    def list(self, request):
        """Obtém progresso do onboarding"""
        tenant = request.user.tenant
        onboarding = OnboardingService.get_or_create_onboarding(tenant)
        serializer = OnboardingProgressSerializer(onboarding)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def create(self, request):
        """Atualiza progresso do onboarding"""
        tenant = request.user.tenant
        onboarding = OnboardingService.get_or_create_onboarding(tenant)
        
        serializer = OnboardingProgressSerializer(
            onboarding,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['post'], url_path='complete')
    def complete(self, request):
        """Completa o onboarding"""
        tenant = request.user.tenant
        
        serializer = OnboardingCompleteSerializer(
            data={},
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        
        try:
            onboarding, admin_user = OnboardingService.complete_onboarding(tenant)
            
            # Atualizar usuário
            request.user.onboarding_completed = True
            request.user.save(update_fields=['onboarding_completed'])
            
            return Response({
                'message': _('Onboarding concluído com sucesso'),
                'onboarding_completed': True
            }, status=status.HTTP_200_OK)
        except ValueError as e:
            return Response({
                'detail': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    """ViewSet para gerenciamento de usuários"""
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    
    def get_serializer_class(self):
        """Retorna serializer apropriado"""
        if self.action == 'list':
            return UserListSerializer
        elif self.action == 'create':
            return UserCreateSerializer
        return UserSerializer
    
    def get_queryset(self):
        """Filtra usuários do tenant do usuário logado"""
        return User.objects.filter(tenant=self.request.user.tenant)
    
    @action(detail=False, methods=['get'], url_path='me')
    def me(self, request):
        """Retorna dados do usuário logado"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
