"""
Unit Tests - Utils
Testes unitários para funções utilitárias
"""
from django.test import TestCase
from apps.core.utils import (
    detect_language_from_country,
    detect_currency_from_country,
    detect_timezone_from_country,
    detect_number_format_from_country,
    detect_date_format_from_country,
    auto_configure_tenant_i18n,
    get_tenant_locale_settings,
)
from apps.tenants.models import Tenant


class UtilsTest(TestCase):
    """Testes para funções utilitárias"""
    
    def setUp(self):
        """Setup para testes"""
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
    
    def test_detect_language_from_country(self):
        """Testa detecção de idioma por país"""
        self.assertEqual(detect_language_from_country('BR'), 'pt-br')
        self.assertEqual(detect_language_from_country('US'), 'en-us')
        self.assertEqual(detect_language_from_country('MX'), 'es-es')
        self.assertEqual(detect_language_from_country('ES'), 'es-es')
        self.assertEqual(detect_language_from_country('AR'), 'es-es')
        # Fallback
        self.assertEqual(detect_language_from_country('XX'), 'pt-br')
    
    def test_detect_currency_from_country(self):
        """Testa detecção de moeda por país"""
        self.assertEqual(detect_currency_from_country('BR'), 'BRL')
        self.assertEqual(detect_currency_from_country('US'), 'USD')
        self.assertEqual(detect_currency_from_country('MX'), 'MXN')
        self.assertEqual(detect_currency_from_country('ES'), 'EUR')
        # Fallback
        self.assertEqual(detect_currency_from_country('XX'), 'BRL')
    
    def test_detect_timezone_from_country(self):
        """Testa detecção de timezone por país"""
        self.assertEqual(detect_timezone_from_country('BR'), 'America/Sao_Paulo')
        self.assertEqual(detect_timezone_from_country('US'), 'America/New_York')
        self.assertEqual(detect_timezone_from_country('MX'), 'America/Mexico_City')
        self.assertEqual(detect_timezone_from_country('ES'), 'Europe/Madrid')
        # Fallback
        self.assertEqual(detect_timezone_from_country('XX'), 'America/Sao_Paulo')
    
    def test_detect_number_format_from_country(self):
        """Testa detecção de formato de número por país"""
        self.assertEqual(detect_number_format_from_country('BR'), '1.234,56')
        self.assertEqual(detect_number_format_from_country('US'), '1,234.56')
        self.assertEqual(detect_number_format_from_country('MX'), '1,234.56')
        self.assertEqual(detect_number_format_from_country('ES'), '1.234,56')
    
    def test_detect_date_format_from_country(self):
        """Testa detecção de formato de data por país"""
        self.assertEqual(detect_date_format_from_country('BR'), 'DD/MM/YYYY')
        self.assertEqual(detect_date_format_from_country('US'), 'MM/DD/YYYY')
        self.assertEqual(detect_date_format_from_country('MX'), 'DD/MM/YYYY')
        self.assertEqual(detect_date_format_from_country('ES'), 'DD/MM/YYYY')
    
    def test_auto_configure_tenant_i18n(self):
        """Testa configuração automática de i18n"""
        auto_configure_tenant_i18n(self.tenant, 'BR')
        
        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.country, 'BR')
        self.assertEqual(self.tenant.language, 'pt-br')
        self.assertEqual(self.tenant.currency, 'BRL')
        self.assertEqual(self.tenant.timezone, 'America/Sao_Paulo')
        self.assertEqual(self.tenant.number_format, '1.234,56')
        self.assertEqual(self.tenant.date_format, 'DD/MM/YYYY')
        
        # Testar com outro país
        auto_configure_tenant_i18n(self.tenant, 'US')
        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.country, 'US')
        self.assertEqual(self.tenant.language, 'en-us')
        self.assertEqual(self.tenant.currency, 'USD')
    
    def test_get_tenant_locale_settings(self):
        """Testa obter configurações de localização do tenant"""
        self.tenant.country = 'BR'
        self.tenant.language = 'pt-br'
        self.tenant.currency = 'BRL'
        self.tenant.timezone = 'America/Sao_Paulo'
        self.tenant.date_format = 'DD/MM/YYYY'
        self.tenant.number_format = '1.234,56'
        self.tenant.save()
        
        settings = get_tenant_locale_settings(self.tenant)
        
        self.assertEqual(settings['country'], 'BR')
        self.assertEqual(settings['language'], 'pt-br')
        self.assertEqual(settings['currency'], 'BRL')
        self.assertEqual(settings['timezone'], 'America/Sao_Paulo')
        self.assertEqual(settings['date_format'], 'DD/MM/YYYY')
        self.assertEqual(settings['number_format'], '1.234,56')

