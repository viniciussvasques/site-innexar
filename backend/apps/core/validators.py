"""
Core Validators
Validações customizadas para autenticação e usuários
"""
import re
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def validate_password_strength(password):
    """
    Valida força da senha
    
    Requisitos:
    - Mínimo 8 caracteres
    - Pelo menos 1 letra maiúscula
    - Pelo menos 1 letra minúscula
    - Pelo menos 1 número
    - Pelo menos 1 caractere especial
    """
    if len(password) < 8:
        raise ValidationError(
            _('A senha deve ter no mínimo 8 caracteres.'),
            code='password_too_short'
        )
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError(
            _('A senha deve conter pelo menos uma letra maiúscula.'),
            code='password_no_uppercase'
        )
    
    if not re.search(r'[a-z]', password):
        raise ValidationError(
            _('A senha deve conter pelo menos uma letra minúscula.'),
            code='password_no_lowercase'
        )
    
    if not re.search(r'\d', password):
        raise ValidationError(
            _('A senha deve conter pelo menos um número.'),
            code='password_no_digit'
        )
    
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        raise ValidationError(
            _('A senha deve conter pelo menos um caractere especial (!@#$%^&*(),.?":{}|<>)'),
            code='password_no_special'
        )


def validate_phone(phone):
    """
    Valida formato de telefone
    
    Aceita formatos:
    - +5511999999999
    - (11) 99999-9999
    - 11 99999-9999
    - 11999999999
    """
    if not phone:
        return
    
    # Remover caracteres não numéricos (exceto + no início)
    cleaned = re.sub(r'[^\d+]', '', phone)
    
    # Verificar se tem pelo menos 10 dígitos
    digits = re.sub(r'\+', '', cleaned)
    if len(digits) < 10 or len(digits) > 15:
        raise ValidationError(
            _('Telefone deve ter entre 10 e 15 dígitos.'),
            code='invalid_phone'
        )


def validate_country_code(country_code):
    """
    Valida código de país ISO 3166-1 alpha-2
    """
    valid_codes = [
        'BR', 'US', 'MX', 'ES', 'AR', 'CO', 'CL', 'PE', 'EC', 'VE',
        'UY', 'PY', 'BO', 'CR', 'PA', 'GT', 'DO', 'CU', 'HN', 'NI', 'SV'
    ]
    
    if country_code.upper() not in valid_codes:
        raise ValidationError(
            _('Código de país inválido.'),
            code='invalid_country'
        )


def validate_currency_code(currency_code):
    """
    Valida código de moeda ISO 4217
    """
    valid_codes = [
        'BRL', 'USD', 'EUR', 'MXN', 'ARS', 'COP', 'CLP', 'PEN', 'UYU',
        'PYG', 'BOB', 'CRC', 'DOP', 'CUP', 'GTQ', 'HNL', 'NIO', 'PAB', 'SVC'
    ]
    
    if currency_code.upper() not in valid_codes:
        raise ValidationError(
            _('Código de moeda inválido.'),
            code='invalid_currency'
        )


def validate_language_code(language_code):
    """
    Valida código de idioma
    """
    valid_codes = ['pt-br', 'en-us', 'es-es']
    
    if language_code.lower() not in valid_codes:
        raise ValidationError(
            _('Código de idioma inválido. Use: pt-br, en-us ou es-es'),
            code='invalid_language'
        )

