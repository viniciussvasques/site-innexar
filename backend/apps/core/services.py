"""
Core Services
Serviços com regras de negócio para autenticação e usuários
"""
import logging
from typing import Optional, Tuple
from datetime import timedelta, datetime
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from apps.core.models import User, PasswordResetToken, OnboardingProgress
from apps.tenants.models import Tenant
from apps.core.utils import (
    auto_configure_tenant_i18n,
    detect_locale_from_request,
)

logger = logging.getLogger(__name__)
User = get_user_model()

# Constantes
ACCESS_TOKEN_LIFETIME_MINUTES = 15
ACCESS_TOKEN_LIFETIME = timedelta(minutes=ACCESS_TOKEN_LIFETIME_MINUTES)


def create_outstanding_token_for_access_token(access_token_str: str, user: User) -> None:
    """
    Cria OutstandingToken para access token (simplejwt não faz isso automaticamente)
    
    Args:
        access_token_str: String do access token
        user: Instância do usuário
    """
    try:
        from rest_framework_simplejwt.token_blacklist.models import OutstandingToken
        from rest_framework_simplejwt.tokens import AccessToken
        
        # Decodificar token para obter jti e exp
        access = AccessToken(access_token_str)
        jti = access.get('jti')
        exp = access.get('exp')
        
        if jti:
            # Criar OutstandingToken se não existir
            OutstandingToken.objects.get_or_create(
                jti=jti,
                defaults={
                    'user': user,
                    'token': access_token_str,
                    'created_at': timezone.now(),
                    'expires_at': datetime.fromtimestamp(exp, tz=timezone.utc) if exp else timezone.now() + ACCESS_TOKEN_LIFETIME,
                }
            )
    except (TokenError, ValueError) as e:
        # Token inválido ou erro de validação
        logger.debug(f'Erro ao criar OutstandingToken para access token (token inválido): {e}')
    except Exception as e:
        # Outros erros (pode ser que já existe, etc)
        logger.debug(f'Erro ao criar OutstandingToken para access token: {e}')


class AuthService:
    """Serviço para autenticação"""
    
    @staticmethod
    def register_user(email: str, password: str, first_name: str, last_name: str,
                     tenant_slug: Optional[str] = None, tenant: Optional[Tenant] = None,
                     phone: Optional[str] = None, request=None) -> Tuple[User, dict]:
        """
        Registra um novo usuário
        
        Args:
            email: Email do usuário
            password: Senha
            first_name: Primeiro nome
            last_name: Sobrenome
            tenant_slug: Slug do tenant (opcional se tenant for fornecido)
            tenant: Instância do tenant (opcional)
            phone: Telefone (opcional)
            request: Objeto request (para detecção de locale)
        
        Returns:
            Tupla (User, tokens_dict)
        
        Raises:
            ValueError: Se tenant não encontrado ou email já existe
        """
        # Obter tenant
        if not tenant:
            if tenant_slug:
                try:
                    tenant = Tenant.objects.get(slug=tenant_slug, is_active=True)
                except Tenant.DoesNotExist:
                    raise ValueError('Tenant não encontrado ou inativo.')
            else:
                raise ValueError('Tenant é obrigatório.')
        
        # Verificar se email já existe no tenant
        if User.objects.filter(email=email.lower(), tenant=tenant).exists():
            raise ValueError('Um usuário com este email já existe neste tenant.')
        
        # Criar usuário
        user = User.objects.create_user(
            email=email.lower(),
            password=password,
            first_name=first_name,
            last_name=last_name,
            tenant=tenant,
            phone=phone,
        )
        
        # Se for o primeiro usuário do tenant, tornar admin
        if user.is_first_user_of_tenant():
            user.role = 'admin'
            user.save(update_fields=['role'])
            logger.info(f'Primeiro usuário do tenant {tenant.slug} criado como admin: {user.email}')
        
        # Detectar idioma do request se disponível
        if request:
            detected_language = detect_locale_from_request(request)
            if detected_language and not tenant.language:
                tenant.language = detected_language
                tenant.save(update_fields=['language'])
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token_str = str(refresh.access_token)
        tokens = {
            'access': access_token_str,
            'refresh': str(refresh),
        }
        
        # Criar OutstandingToken para access token
        create_outstanding_token_for_access_token(access_token_str, user)
        
        logger.info(f'Usuário registrado: {user.email} (tenant: {tenant.slug})')
        return user, tokens
    
    @staticmethod
    def login_user(email: str, password: str, request=None) -> Tuple[User, dict]:
        """
        Autentica um usuário
        
        Args:
            email: Email do usuário
            password: Senha
            request: Objeto request (para autenticação)
        
        Returns:
            Tupla (User, tokens_dict)
        
        Raises:
            ValueError: Se credenciais inválidas ou conta bloqueada
        """
        email = email.lower()
        
        # Buscar usuário
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            raise ValueError('Credenciais inválidas.')
        except User.MultipleObjectsReturned:
            # Se houver múltiplos, pegar o primeiro ativo
            user = User.objects.filter(email=email, is_active=True).first()
            if not user:
                raise ValueError('Credenciais inválidas.')
        
        # Verificar se conta está bloqueada
        if user.is_locked():
            raise ValueError('Conta bloqueada. Tente novamente mais tarde.')
        
        # Verificar se tenant está ativo
        if not user.tenant.is_active:
            raise ValueError('Tenant inativo.')
        
        # Autenticar
        from django.contrib.auth import authenticate
        user_auth = authenticate(
            request=request,
            username=email,
            password=password
        )
        
        if not user_auth or user_auth != user:
            # Incrementar tentativas falhas
            user.increment_failed_login()
            raise ValueError('Credenciais inválidas.')
        
        # Resetar tentativas falhas após login bem-sucedido
        user.reset_failed_login()
        
        # Atualizar last_login
        user.last_login = timezone.now()
        user.save(update_fields=['last_login'])
        
        # Gerar tokens JWT
        refresh = RefreshToken.for_user(user)
        access_token_str = str(refresh.access_token)
        tokens = {
            'access': access_token_str,
            'refresh': str(refresh),
        }
        
        # Criar OutstandingToken para access token
        create_outstanding_token_for_access_token(access_token_str, user)
        
        logger.info(f'Usuário autenticado: {user.email} (tenant: {user.tenant.slug})')
        return user, tokens
    
    @staticmethod
    def logout_user(refresh_token: str, access_token: str = None) -> bool:
        """
        Faz logout do usuário (invalida refresh token e access token)
        
        Args:
            refresh_token: Token de refresh
            access_token: Token de acesso (opcional, mas recomendado)
        
        Returns:
            True se logout bem-sucedido
        """
        try:
            # Invalidar refresh token (isso também invalida o access token relacionado)
            try:
                refresh = RefreshToken(refresh_token)
                refresh.blacklist()
            except (TokenError, InvalidToken) as e:
                logger.warning(f'Erro ao invalidar refresh token (token inválido): {e}')
                # Tentar continuar com invalidação do access token se fornecido
            except Exception as e:
                logger.error(f'Erro inesperado ao invalidar refresh token: {e}')
                raise
            
            # Invalidar access token diretamente se fornecido
            if access_token:
                try:
                    from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
                    from rest_framework_simplejwt.tokens import AccessToken
                    from django.utils import timezone
                    from django.contrib.auth import get_user_model
                    
                    # Decodificar access token para obter jti e user_id
                    access = AccessToken(access_token)
                    jti = access.get('jti')
                    user_id = access.get('user_id')
                    
                    if jti:
                        # Encontrar o outstanding token (deve existir se foi criado no login/register)
                        outstanding_token = OutstandingToken.objects.filter(jti=jti).first()
                        
                        if outstanding_token:
                            # Criar entrada na blacklist se não existir
                            BlacklistedToken.objects.get_or_create(token=outstanding_token)
                        else:
                            # Se não existir, criar agora (fallback)
                            User = get_user_model()
                            user = User.objects.filter(id=user_id).first()
                            
                            if user:
                                outstanding_token = OutstandingToken.objects.create(
                                    jti=jti,
                                    user=user,
                                    token=str(access_token),
                                    created_at=timezone.now(),
                                    expires_at=timezone.now() + ACCESS_TOKEN_LIFETIME,
                                )
                                BlacklistedToken.objects.get_or_create(token=outstanding_token)
                except (TokenError, InvalidToken) as e:
                    # Token inválido ou já expirado
                    logger.warning(f'Erro ao invalidar access token (token inválido): {e}')
                except Exception as e:
                    # Outros erros - continua (refresh já foi invalidado)
                    logger.warning(f'Erro ao invalidar access token: {e}')
            
            logger.info('Usuário fez logout (tokens invalidados)')
            return True
        except (TokenError, InvalidToken) as e:
            logger.error(f'Erro ao fazer logout (token inválido): {e}')
            return False
        except Exception as e:
            logger.error(f'Erro inesperado ao fazer logout: {e}')
            return False
    
    @staticmethod
    def refresh_access_token(refresh_token: str) -> dict:
        """
        Renova access token
        
        Args:
            refresh_token: Token de refresh
        
        Returns:
            Dicionário com novos tokens
            
        Raises:
            TokenError: Se refresh token for inválido
        """
        try:
            refresh = RefreshToken(refresh_token)
            access_token_str = str(refresh.access_token)
            tokens = {
                'access': access_token_str,
                'refresh': str(refresh),  # Novo refresh token (rotation)
            }
            
            # Criar OutstandingToken para o novo access token
            user_id = refresh.access_token.get('user_id')
            user = User.objects.filter(id=user_id).first()
            if user:
                create_outstanding_token_for_access_token(access_token_str, user)
            
            return tokens
        except (TokenError, InvalidToken) as e:
            logger.error(f'Erro ao renovar token (token inválido): {e}')
            raise
        except Exception as e:
            logger.error(f'Erro inesperado ao renovar token: {e}')
            raise


class PasswordResetService:
    """Serviço para reset de senha"""
    
    @staticmethod
    def request_password_reset(email: str) -> bool:
        """
        Solicita reset de senha
        
        Args:
            email: Email do usuário
        
        Returns:
            True se email foi enviado (sempre retorna True por segurança)
        """
        email = email.lower()
        
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            # Não expor se email existe ou não
            logger.warning(f'Tentativa de reset de senha para email inexistente: {email}')
            return True
        
        # Criar token de reset
        reset_token = PasswordResetToken.create_for_user(user)
        
        # Enviar email (em produção, usar Celery)
        try:
            reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token.token}"
            send_mail(
                subject='Reset de Senha - StructurOne',
                message=f'Clique no link para resetar sua senha: {reset_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[user.email],
                fail_silently=False,
            )
            logger.info(f'Email de reset de senha enviado para: {user.email}')
        except Exception as e:
            logger.error(f'Erro ao enviar email de reset: {e}')
            # Em desenvolvimento, logar o token
            if settings.DEBUG:
                logger.info(f'Token de reset (DEBUG): {reset_token.token}')
        
        return True
    
    @staticmethod
    def confirm_password_reset(token: str, new_password: str) -> bool:
        """
        Confirma reset de senha
        
        Args:
            token: Token de reset
            new_password: Nova senha
        
        Returns:
            True se senha foi alterada
        """
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            raise ValueError('Token inválido.')
        
        if not reset_token.is_valid():
            raise ValueError('Token expirado ou já utilizado.')
        
        # Alterar senha
        user = reset_token.user
        user.set_password(new_password)
        user.save(update_fields=['password'])
        
        # Marcar token como usado
        reset_token.used = True
        reset_token.save(update_fields=['used'])
        
        # Resetar tentativas falhas
        user.reset_failed_login()
        
        logger.info(f'Senha alterada para usuário: {user.email}')
        return True


class OnboardingService:
    """Serviço para onboarding"""
    
    @staticmethod
    def get_or_create_onboarding(tenant: Tenant) -> OnboardingProgress:
        """
        Obtém ou cria progresso de onboarding para o tenant
        
        Args:
            tenant: Instância do tenant
        
        Returns:
            OnboardingProgress
        """
        onboarding, created = OnboardingProgress.objects.get_or_create(
            tenant=tenant,
            defaults={
                'step': 0,
                'completed': False,
                'data': {},
            }
        )
        return onboarding
    
    @staticmethod
    def update_onboarding_step(tenant: Tenant, step: int, data: dict) -> OnboardingProgress:
        """
        Atualiza etapa do onboarding
        
        Args:
            tenant: Instância do tenant
            step: Etapa atual (0-4)
            data: Dados coletados
        
        Returns:
            OnboardingProgress atualizado
        """
        onboarding = OnboardingService.get_or_create_onboarding(tenant)
        
        # Se país foi selecionado, configurar i18n automaticamente
        if 'country' in data:
            country_code = data.get('country')
            auto_configure_tenant_i18n(tenant, country_code)
            # Atualizar data com configurações aplicadas
            data.update({
                'language': tenant.language,
                'currency': tenant.currency,
                'timezone': tenant.timezone,
                'date_format': tenant.date_format,
                'number_format': tenant.number_format,
            })
        
        onboarding.update_step(step, data)
        logger.info(f'Onboarding atualizado para tenant {tenant.slug}: etapa {step}')
        return onboarding
    
    @staticmethod
    def complete_onboarding(tenant: Tenant) -> Tuple[OnboardingProgress, Optional[User]]:
        """
        Completa o onboarding do tenant
        
        Args:
            tenant: Instância do tenant
        
        Returns:
            Tupla (OnboardingProgress, User admin)
        """
        onboarding = OnboardingService.get_or_create_onboarding(tenant)
        
        if onboarding.completed:
            raise ValueError('Onboarding já foi completado.')
        
        # Marcar como completo
        onboarding.complete()
        
        # Marcar usuário admin como tendo completado onboarding
        admin_user = User.objects.filter(tenant=tenant, role='admin').first()
        if admin_user:
            admin_user.onboarding_completed = True
            admin_user.save(update_fields=['onboarding_completed'])
        
        logger.info(f'Onboarding completado para tenant: {tenant.slug}')
        return onboarding, admin_user

