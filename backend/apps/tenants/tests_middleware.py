"""
Tests for Tenant Middleware
"""
from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from .models import Tenant
from .middleware import TenantMiddleware

User = get_user_model()


class TenantMiddlewareTest(TestCase):
    """Testes para o middleware de tenant"""
    
    def setUp(self):
        """Setup para testes"""
        self.factory = RequestFactory()
        self.middleware = TenantMiddleware(lambda request: None)
        self.tenant = Tenant.objects.create(
            name='Cliente Teste',
            slug='cliente-teste',
            domain='cliente-teste.structurone.com',
            email='contato@cliente-teste.com',
        )
    
    def test_middleware_detects_subdomain(self):
        """Testa que middleware detecta subdomínio"""
        request = self.factory.get('/api/projects/')
        request.META['HTTP_HOST'] = 'cliente-teste.structurone.com'
        
        self.middleware.process_request(request)
        
        self.assertIsNotNone(request.tenant)
        self.assertEqual(request.tenant.slug, 'cliente-teste')
    
    def test_middleware_ignores_www(self):
        """Testa que middleware ignora www"""
        request = self.factory.get('/api/projects/')
        request.META['HTTP_HOST'] = 'www.structurone.com'
        
        self.middleware.process_request(request)
        
        self.assertIsNone(request.tenant)
    
    def test_middleware_handles_main_domain(self):
        """Testa que middleware lida com domínio principal"""
        request = self.factory.get('/api/projects/')
        request.META['HTTP_HOST'] = 'structurone.com'
        
        self.middleware.process_request(request)
        
        self.assertIsNone(request.tenant)
    
    def test_middleware_handles_inactive_tenant(self):
        """Testa que middleware não retorna tenant inativo"""
        self.tenant.is_active = False
        self.tenant.save()
        
        request = self.factory.get('/api/projects/')
        request.META['HTTP_HOST'] = 'cliente-teste.structurone.com'
        
        self.middleware.process_request(request)
        
        self.assertIsNone(request.tenant)
    
    def test_middleware_handles_nonexistent_tenant(self):
        """Testa que middleware lida com tenant inexistente"""
        request = self.factory.get('/api/projects/')
        request.META['HTTP_HOST'] = 'inexistente.structurone.com'
        
        self.middleware.process_request(request)
        
        self.assertIsNone(request.tenant)
    
    def test_middleware_uses_header_in_development(self):
        """Testa que middleware usa header em desenvolvimento"""
        request = self.factory.get('/api/projects/')
        request.META['HTTP_HOST'] = 'localhost:8010'
        request.META['HTTP_X_TENANT_SLUG'] = 'cliente-teste'
        
        self.middleware.process_request(request)
        
        self.assertIsNotNone(request.tenant)
        self.assertEqual(request.tenant.slug, 'cliente-teste')

