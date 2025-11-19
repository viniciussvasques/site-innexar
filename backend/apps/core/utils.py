"""
Core Utilities
Funções utilitárias para internacionalização e detecção automática
"""
import locale
from typing import Optional, Tuple
from django.conf import settings
from django.utils import translation


# Mapeamento de países para idiomas padrão
COUNTRY_TO_LANGUAGE = {
    'BR': 'pt-br',
    'US': 'en-us',
    'MX': 'es-es',
    'ES': 'es-es',
    'AR': 'es-es',
    'CO': 'es-es',
    'CL': 'es-es',
    'PE': 'es-es',
    'EC': 'es-es',
    'VE': 'es-es',
    'UY': 'es-es',
    'PY': 'es-es',
    'BO': 'es-es',
    'CR': 'es-es',
    'PA': 'es-es',
    'GT': 'es-es',
    'DO': 'es-es',
    'CU': 'es-es',
    'HN': 'es-es',
    'NI': 'es-es',
    'SV': 'es-es',
}

# Mapeamento de países para moedas
COUNTRY_TO_CURRENCY = {
    'BR': 'BRL',
    'US': 'USD',
    'MX': 'MXN',
    'ES': 'EUR',
    'AR': 'ARS',
    'CO': 'COP',
    'CL': 'CLP',
    'PE': 'PEN',
    'UY': 'UYU',
    'PY': 'PYG',
    'BO': 'BOB',
    'CR': 'CRC',
    'PA': 'PAB',
    'DO': 'DOP',
    'CU': 'CUP',
    'GT': 'GTQ',
    'HN': 'HNL',
    'NI': 'NIO',
    'SV': 'SVC',
    'EC': 'USD',  # Equador usa dólar
}

# Mapeamento de países para timezones
COUNTRY_TO_TIMEZONE = {
    'BR': 'America/Sao_Paulo',
    'US': 'America/New_York',
    'MX': 'America/Mexico_City',
    'ES': 'Europe/Madrid',
    'AR': 'America/Argentina/Buenos_Aires',
    'CO': 'America/Bogota',
    'CL': 'America/Santiago',
    'PE': 'America/Lima',
    'UY': 'America/Montevideo',
    'PY': 'America/Asuncion',
    'BO': 'America/La_Paz',
    'CR': 'America/Costa_Rica',
    'PA': 'America/Panama',
    'DO': 'America/Santo_Domingo',
    'CU': 'America/Havana',
    'GT': 'America/Guatemala',
    'HN': 'America/Tegucigalpa',
    'NI': 'America/Managua',
    'SV': 'America/El_Salvador',
    'EC': 'America/Guayaquil',
}

# Mapeamento de países para formato de número
COUNTRY_TO_NUMBER_FORMAT = {
    'BR': '1.234,56',
    'US': '1,234.56',
    'MX': '1,234.56',
    'ES': '1.234,56',
    'AR': '1.234,56',
    'CO': '1.234,56',
    'CL': '1.234,56',
    'PE': '1.234,56',
    'UY': '1.234,56',
    'PY': '1.234,56',
    'BO': '1.234,56',
    'CR': '1.234,56',
    'PA': '1.234,56',
    'DO': '1.234,56',
    'CU': '1.234,56',
    'GT': '1.234,56',
    'HN': '1.234,56',
    'NI': '1.234,56',
    'SV': '1.234,56',
    'EC': '1.234,56',
}

# Mapeamento de países para formato de data
COUNTRY_TO_DATE_FORMAT = {
    'BR': 'DD/MM/YYYY',
    'US': 'MM/DD/YYYY',
    'MX': 'DD/MM/YYYY',
    'ES': 'DD/MM/YYYY',
    'AR': 'DD/MM/YYYY',
    'CO': 'DD/MM/YYYY',
    'CL': 'DD/MM/YYYY',
    'PE': 'DD/MM/YYYY',
    'UY': 'DD/MM/YYYY',
    'PY': 'DD/MM/YYYY',
    'BO': 'DD/MM/YYYY',
    'CR': 'DD/MM/YYYY',
    'PA': 'MM/DD/YYYY',
    'DO': 'DD/MM/YYYY',
    'CU': 'DD/MM/YYYY',
    'GT': 'DD/MM/YYYY',
    'HN': 'DD/MM/YYYY',
    'NI': 'DD/MM/YYYY',
    'SV': 'DD/MM/YYYY',
    'EC': 'DD/MM/YYYY',
}


def detect_language_from_country(country_code: str) -> str:
    """
    Detecta o idioma padrão baseado no código do país
    
    Args:
        country_code: Código ISO 3166-1 alpha-2 do país (ex: 'BR', 'US')
    
    Returns:
        Código do idioma (ex: 'pt-br', 'en-us', 'es-es')
    """
    return COUNTRY_TO_LANGUAGE.get(country_code.upper(), 'pt-br')


def detect_currency_from_country(country_code: str) -> str:
    """
    Detecta a moeda padrão baseado no código do país
    
    Args:
        country_code: Código ISO 3166-1 alpha-2 do país
    
    Returns:
        Código da moeda ISO 4217 (ex: 'BRL', 'USD')
    """
    return COUNTRY_TO_CURRENCY.get(country_code.upper(), 'BRL')


def detect_timezone_from_country(country_code: str) -> str:
    """
    Detecta o fuso horário padrão baseado no código do país
    
    Args:
        country_code: Código ISO 3166-1 alpha-2 do país
    
    Returns:
        Nome do timezone (ex: 'America/Sao_Paulo')
    """
    return COUNTRY_TO_TIMEZONE.get(country_code.upper(), 'America/Sao_Paulo')


def detect_number_format_from_country(country_code: str) -> str:
    """
    Detecta o formato de número padrão baseado no código do país
    
    Args:
        country_code: Código ISO 3166-1 alpha-2 do país
    
    Returns:
        Formato de número (ex: '1.234,56' ou '1,234.56')
    """
    return COUNTRY_TO_NUMBER_FORMAT.get(country_code.upper(), '1.234,56')


def detect_date_format_from_country(country_code: str) -> str:
    """
    Detecta o formato de data padrão baseado no código do país
    
    Args:
        country_code: Código ISO 3166-1 alpha-2 do país
    
    Returns:
        Formato de data (ex: 'DD/MM/YYYY' ou 'MM/DD/YYYY')
    """
    return COUNTRY_TO_DATE_FORMAT.get(country_code.upper(), 'DD/MM/YYYY')


def detect_locale_from_request(request) -> Optional[str]:
    """
    Detecta o idioma preferido do usuário baseado no header Accept-Language
    
    Args:
        request: Objeto HttpRequest do Django
    
    Returns:
        Código do idioma ou None
    """
    accept_language = request.META.get('HTTP_ACCEPT_LANGUAGE', '')
    if not accept_language:
        return None
    
    # Parse do header Accept-Language
    # Exemplo: "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7"
    languages = []
    for lang in accept_language.split(','):
        lang = lang.strip().split(';')[0]
        lang = lang.lower()
        
        # Normalizar para nossos códigos
        if lang.startswith('pt'):
            return 'pt-br'
        elif lang.startswith('en'):
            return 'en-us'
        elif lang.startswith('es'):
            return 'es-es'
    
    return None


def get_tenant_locale_settings(tenant) -> dict:
    """
    Retorna as configurações de localização do tenant
    
    Args:
        tenant: Instância do modelo Tenant
    
    Returns:
        Dicionário com configurações de localização
    """
    return {
        'language': tenant.language,
        'country': tenant.country,
        'currency': tenant.currency,
        'timezone': tenant.timezone,
        'date_format': tenant.date_format,
        'number_format': tenant.number_format,
    }


def auto_configure_tenant_i18n(tenant, country_code: str):
    """
    Configura automaticamente as opções de internacionalização do tenant
    baseado no país
    
    Args:
        tenant: Instância do modelo Tenant
        country_code: Código ISO 3166-1 alpha-2 do país
    """
    tenant.country = country_code.upper()
    tenant.language = detect_language_from_country(country_code)
    tenant.currency = detect_currency_from_country(country_code)
    tenant.timezone = detect_timezone_from_country(country_code)
    tenant.number_format = detect_number_format_from_country(country_code)
    tenant.date_format = detect_date_format_from_country(country_code)
    tenant.save(update_fields=[
        'country', 'language', 'currency', 'timezone',
        'number_format', 'date_format'
    ])

