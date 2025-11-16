#!/usr/bin/env python
"""
Script para testar multi-tenant no ambiente local
Execute: python test_tenant_local.py
"""
import os
import sys
import django

# Setup Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'structurone.settings')
django.setup()

from apps.tenants.models import Tenant
from django.test import RequestFactory
from apps.tenants.middleware import TenantMiddleware


def create_test_tenants():
    """Cria tenants de teste"""
    print("📦 Criando tenants de teste...")
    
    tenant1, created1 = Tenant.objects.get_or_create(
        slug='empresa-abc',
        defaults={
            'name': 'Empresa ABC',
            'domain': 'empresa-abc.structurone.com',
            'email': 'contato@empresa-abc.com',
            'subscription_plan': 'professional',
            'max_projects': 50,
            'max_users': 20,
        }
    )
    
    tenant2, created2 = Tenant.objects.get_or_create(
        slug='construtora-xyz',
        defaults={
            'name': 'Construtora XYZ',
            'domain': 'construtora-xyz.structurone.com',
            'email': 'contato@construtora-xyz.com',
            'subscription_plan': 'basic',
            'max_projects': 10,
            'max_users': 5,
        }
    )
    
    if created1:
        print(f"✅ Tenant 1 criado: {tenant1.slug} ({tenant1.name})")
    else:
        print(f"ℹ️  Tenant 1 já existe: {tenant1.slug} ({tenant1.name})")
    
    if created2:
        print(f"✅ Tenant 2 criado: {tenant2.slug} ({tenant2.name})")
    else:
        print(f"ℹ️  Tenant 2 já existe: {tenant2.slug} ({tenant2.name})")
    
    return tenant1, tenant2


def test_middleware_with_header():
    """Testa middleware com header X-Tenant-Slug"""
    print("\n🧪 Testando middleware com header X-Tenant-Slug...")
    
    factory = RequestFactory()
    middleware = TenantMiddleware(lambda r: None)
    
    # Teste 1: Tenant 1
    request = factory.get('/api/tenants/')
    request.META['HTTP_HOST'] = 'localhost:8000'
    request.META['HTTP_X_TENANT_SLUG'] = 'empresa-abc'
    middleware.process_request(request)
    
    if hasattr(request, 'tenant') and request.tenant:
        print(f"✅ Header detectado: {request.tenant.slug} ({request.tenant.name})")
    else:
        print("❌ Header não detectado")
    
    # Teste 2: Tenant 2
    request = factory.get('/api/tenants/')
    request.META['HTTP_HOST'] = 'localhost:8000'
    request.META['HTTP_X_TENANT_SLUG'] = 'construtora-xyz'
    middleware.process_request(request)
    
    if hasattr(request, 'tenant') and request.tenant:
        print(f"✅ Header detectado: {request.tenant.slug} ({request.tenant.name})")
    else:
        print("❌ Header não detectado")
    
    # Teste 3: Tenant inexistente
    request = factory.get('/api/tenants/')
    request.META['HTTP_HOST'] = 'localhost:8000'
    request.META['HTTP_X_TENANT_SLUG'] = 'inexistente'
    middleware.process_request(request)
    
    if hasattr(request, 'tenant') and request.tenant:
        print("❌ Tenant inexistente foi detectado (erro!)")
    else:
        print("✅ Tenant inexistente corretamente ignorado")


def test_middleware_with_subdomain():
    """Testa middleware com subdomínio"""
    print("\n🧪 Testando middleware com subdomínio...")
    
    factory = RequestFactory()
    middleware = TenantMiddleware(lambda r: None)
    
    # Teste 1: Subdomínio tenant 1
    request = factory.get('/api/tenants/')
    request.META['HTTP_HOST'] = 'empresa-abc.localhost:8000'
    middleware.process_request(request)
    
    if hasattr(request, 'tenant') and request.tenant:
        print(f"✅ Subdomínio detectado: {request.tenant.slug} ({request.tenant.name})")
    else:
        print("❌ Subdomínio não detectado")
    
    # Teste 2: Subdomínio tenant 2
    request = factory.get('/api/tenants/')
    request.META['HTTP_HOST'] = 'construtora-xyz.localhost:8000'
    middleware.process_request(request)
    
    if hasattr(request, 'tenant') and request.tenant:
        print(f"✅ Subdomínio detectado: {request.tenant.slug} ({request.tenant.name})")
    else:
        print("❌ Subdomínio não detectado")
    
    # Teste 3: Sem subdomínio (admin)
    request = factory.get('/admin/')
    request.META['HTTP_HOST'] = 'localhost:8000'
    middleware.process_request(request)
    
    if hasattr(request, 'tenant') and request.tenant:
        print("❌ Tenant detectado quando não deveria (erro!)")
    else:
        print("✅ Sem subdomínio corretamente ignorado (admin/API principal)")


def print_test_commands():
    """Imprime comandos para testar manualmente"""
    print("\n📋 Comandos para testar manualmente:")
    print("\n1. Testar com cURL (header):")
    print("   curl -H \"X-Tenant-Slug: empresa-abc\" http://localhost:8000/api/tenants/")
    print("   curl -H \"X-Tenant-Slug: construtora-xyz\" http://localhost:8000/api/tenants/")
    
    print("\n2. Testar com cURL (subdomínio - requer /etc/hosts):")
    print("   curl http://empresa-abc.localhost:8000/api/tenants/")
    print("   curl http://construtora-xyz.localhost:8000/api/tenants/")
    
    print("\n3. Testar no navegador (JavaScript console):")
    print("   fetch('http://localhost:8000/api/tenants/', {")
    print("     headers: { 'X-Tenant-Slug': 'empresa-abc' }")
    print("   }).then(r => r.json()).then(console.log)")
    
    print("\n4. Configurar /etc/hosts (Windows):")
    print("   C:\\Windows\\System32\\drivers\\etc\\hosts")
    print("   Adicionar:")
    print("   127.0.0.1 empresa-abc.localhost")
    print("   127.0.0.1 construtora-xyz.localhost")
    
    print("\n5. Configurar /etc/hosts (Linux/Mac):")
    print("   sudo nano /etc/hosts")
    print("   Adicionar:")
    print("   127.0.0.1 empresa-abc.localhost")
    print("   127.0.0.1 construtora-xyz.localhost")


def main():
    """Função principal"""
    print("=" * 60)
    print("🧪 Teste de Multi-Tenant - Ambiente Local")
    print("=" * 60)
    
    # Criar tenants
    tenant1, tenant2 = create_test_tenants()
    
    # Testar middleware
    test_middleware_with_header()
    test_middleware_with_subdomain()
    
    # Imprimir comandos
    print_test_commands()
    
    print("\n" + "=" * 60)
    print("✅ Testes concluídos!")
    print("=" * 60)
    print("\n💡 Dica: Execute o servidor Django e teste os comandos acima")
    print("   python manage.py runserver")


if __name__ == '__main__':
    main()

