"""
Core Serializers
Serializers para autenticação, usuários e onboarding
"""
from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from apps.core.models import User, PasswordResetToken, OnboardingProgress
from apps.tenants.models import Tenant
from apps.core.utils import (
    auto_configure_tenant_i18n,
    detect_locale_from_request,
)


class TenantSerializer(serializers.ModelSerializer):
    """Serializer básico para Tenant (usado em respostas)"""
    
    class Meta:
        model = Tenant
        fields = [
            'id',
            'name',
            'slug',
            'domain',
            'email',
            'language',
            'country',
            'currency',
            'timezone',
            'date_format',
            'number_format',
        ]
        read_only_fields = ['id', 'slug', 'domain']


class UserSerializer(serializers.ModelSerializer):
    """Serializer completo para User"""
    tenant = TenantSerializer(read_only=True)
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'first_name',
            'last_name',
            'full_name',
            'phone',
            'avatar',
            'role',
            'tenant',
            'onboarding_completed',
            'onboarding_step',
            'is_active',
            'date_joined',
            'last_login',
        ]
        read_only_fields = [
            'id',
            'date_joined',
            'last_login',
            'onboarding_completed',
            'onboarding_step',
        ]


class UserListSerializer(serializers.ModelSerializer):
    """Serializer simplificado para listagem de usuários"""
    full_name = serializers.CharField(source='get_full_name', read_only=True)
    
    class Meta:
        model = User
        fields = [
            'id',
            'email',
            'full_name',
            'role',
            'is_active',
            'last_login',
        ]


class UserCreateSerializer(serializers.ModelSerializer):
    """Serializer para criação de usuário"""
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={"input_type": "password"},
    )
    tenant_slug = serializers.CharField(write_only=True, required=False)
    company_name = serializers.CharField(write_only=True, required=False, allow_blank=True)
    desired_slug = serializers.CharField(write_only=True, required=False, allow_blank=True)
    
    class Meta:
        model = User
        fields = [
            "email",
            "password",
            "password_confirm",
            "first_name",
            "last_name",
            "phone",
            "tenant_slug",
            "company_name",
            "desired_slug",
        ]
    
    def validate(self, attrs):
        """Valida se as senhas coincidem"""
        if attrs["password"] != attrs["password_confirm"]:
            raise serializers.ValidationError(
                {"password_confirm": _("As senhas não coincidem.")}
            )
        return attrs
    
    def validate_email(self, value):
        """Valida email único (globalmente, mas verificaremos tenant depois)"""
        # Verificação será feita no service considerando o tenant
        return value.lower()
    
    def create(self, validated_data):
        """Cria usuário e define role baseado em ser primeiro usuário"""
        from django.utils.text import slugify

        validated_data.pop("password_confirm")
        tenant_slug = validated_data.pop("tenant_slug", None)
        company_name = validated_data.pop("company_name", "").strip()
        desired_slug = validated_data.pop("desired_slug", "").strip().lower()
        password = validated_data.pop("password")

        # Obter ou criar tenant
        if tenant_slug:
            try:
                tenant = Tenant.objects.get(slug=tenant_slug, is_active=True)
            except Tenant.DoesNotExist:
                raise serializers.ValidationError(
                    {"tenant_slug": _("Tenant não encontrado ou inativo.")}
                )
        else:
            # Criar tenant automaticamente a partir do nome da empresa ou email
            base_name = company_name or f"{validated_data.get('first_name', '')} {validated_data.get('last_name', '')}".strip()
            if not base_name:
                # fallback para parte do email antes do @
                base_name = validated_data["email"].split("@")[0]

            base_slug = desired_slug or slugify(base_name)
            if not base_slug:
                base_slug = slugify(validated_data["email"].split("@")[0])

            slug = base_slug
            idx = 2
            while Tenant.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{idx}"
                idx += 1

            domain = f"{slug}.structurone.com"

            # Garantir domínio único
            domain_base = domain
            idx_domain = 2
            while Tenant.objects.filter(domain=domain).exists():
                domain = domain_base.replace(".structurone.com", f"-{idx_domain}.structurone.com")
                idx_domain += 1

            tenant = Tenant.objects.create(
                name=base_name or slug,
                slug=slug,
                domain=domain,
                email=validated_data["email"],
            )
        
        # Verificar se email já existe no tenant
        if User.objects.filter(email=validated_data["email"], tenant=tenant).exists():
            raise serializers.ValidationError(
                {"email": _("Um usuário com este email já existe neste tenant.")}
            )
        
        # Criar usuário
        user = User.objects.create_user(
            tenant=tenant, password=password, **validated_data
        )
        
        # Se for o primeiro usuário do tenant, tornar admin
        if user.is_first_user_of_tenant():
            user.role = 'admin'
            user.save(update_fields=['role'])
        
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer para login"""
    email = serializers.EmailField(required=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Valida credenciais"""
        email = attrs.get('email')
        password = attrs.get('password')
        
        if email and password:
            # Buscar usuário por email (pode haver múltiplos com mesmo email em tenants diferentes)
            try:
                user = User.objects.get(email=email.lower())
            except User.DoesNotExist:
                raise serializers.ValidationError({
                    'email': _('Credenciais inválidas.')
                })
            except User.MultipleObjectsReturned:
                # Se houver múltiplos usuários com mesmo email, precisamos do tenant
                # Por enquanto, pegar o primeiro ativo
                user = User.objects.filter(email=email.lower(), is_active=True).first()
                if not user:
                    raise serializers.ValidationError({
                        'email': _('Credenciais inválidas.')
                    })
            
            # Verificar se conta está bloqueada
            if user.is_locked():
                raise serializers.ValidationError({
                    'email': _('Conta bloqueada. Tente novamente mais tarde.')
                })
            
            # Verificar se usuário está ativo
            if not user.is_active:
                raise serializers.ValidationError({
                    'email': _('Conta desativada.')
                })
            
            # Verificar se tenant está ativo
            if not user.tenant.is_active:
                raise serializers.ValidationError({
                    'email': _('Tenant inativo.')
                })
            
            # Autenticar
            user_auth = authenticate(
                request=self.context.get('request'),
                username=email.lower(),
                password=password
            )
            
            if not user_auth or user_auth != user:
                # Incrementar tentativas falhas
                user.increment_failed_login()
                raise serializers.ValidationError({
                    'email': _('Credenciais inválidas.')
                })
            
            # Resetar tentativas falhas após login bem-sucedido
            user.reset_failed_login()
            
            attrs['user'] = user
        else:
            raise serializers.ValidationError({
                'email': _('Email e senha são obrigatórios.')
            })
        
        return attrs


class PasswordResetRequestSerializer(serializers.Serializer):
    """Serializer para solicitar reset de senha"""
    email = serializers.EmailField(required=True)
    
    def validate_email(self, value):
        """Valida se email existe"""
        # Não expor se email existe ou não por segurança
        return value.lower()


class PasswordResetConfirmSerializer(serializers.Serializer):
    """Serializer para confirmar reset de senha"""
    token = serializers.CharField(required=True)
    new_password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password],
        style={'input_type': 'password'}
    )
    new_password_confirm = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    
    def validate(self, attrs):
        """Valida se as senhas coincidem e se token é válido"""
        if attrs['new_password'] != attrs['new_password_confirm']:
            raise serializers.ValidationError({
                'new_password_confirm': _('As senhas não coincidem.')
            })
        
        # Validar token
        token = attrs.get('token')
        try:
            reset_token = PasswordResetToken.objects.get(token=token)
        except PasswordResetToken.DoesNotExist:
            raise serializers.ValidationError({
                'token': _('Token inválido.')
            })
        
        if not reset_token.is_valid():
            raise serializers.ValidationError({
                'token': _('Token expirado ou já utilizado.')
            })
        
        attrs['reset_token'] = reset_token
        return attrs


class OnboardingProgressSerializer(serializers.ModelSerializer):
    """Serializer para progresso do onboarding"""
    
    class Meta:
        model = OnboardingProgress
        fields = [
            'step',
            'completed',
            'data',
        ]
        read_only_fields = ['completed']
    
    def validate_data(self, value):
        """Valida estrutura dos dados do onboarding"""
        if not isinstance(value, dict):
            raise serializers.ValidationError(_('Dados devem ser um objeto JSON.'))
        return value
    
    def validate_step(self, value):
        """Valida etapa do onboarding"""
        if value < 0 or value > 4:
            raise serializers.ValidationError(_('Etapa deve estar entre 0 e 4.'))
        return value
    
    def update(self, instance, validated_data):
        """Atualiza progresso e aplica configurações de i18n se país for selecionado"""
        step = validated_data.get('step', instance.step)
        data = validated_data.get('data', {})
        
        # Se país foi selecionado, configurar i18n automaticamente
        if 'country' in data and instance.tenant:
            country_code = data.get('country')
            auto_configure_tenant_i18n(instance.tenant, country_code)
            # Atualizar data com configurações aplicadas
            data.update({
                'language': instance.tenant.language,
                'currency': instance.tenant.currency,
                'timezone': instance.tenant.timezone,
                'date_format': instance.tenant.date_format,
                'number_format': instance.tenant.number_format,
            })
        
        instance.update_step(step, data)
        return instance


class OnboardingCompleteSerializer(serializers.Serializer):
    """Serializer para completar onboarding"""
    
    def validate(self, attrs):
        """Valida se onboarding pode ser completado"""
        request = self.context.get('request')
        if not request or not request.user:
            raise serializers.ValidationError(_('Usuário não autenticado.'))
        
        user = request.user
        if not hasattr(user.tenant, 'onboarding'):
            raise serializers.ValidationError(_('Onboarding não encontrado.'))
        
        onboarding = user.tenant.onboarding
        if onboarding.completed:
            raise serializers.ValidationError(_('Onboarding já foi completado.'))
        
        attrs['onboarding'] = onboarding
        return attrs

