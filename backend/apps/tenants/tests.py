"""
Tests for Tenants app
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Tenant

User = get_user_model()


class TenantModelTest(TestCase):
    """Testes para o modelo Tenant"""
    
    def setUp(self):
        """Setup para testes"""
        self.tenant_data = {
            'name': 'Empresa Teste',
            'slug': 'empresa-teste',
            'domain': 'empresa-teste.structurone.com',
            'email': 'contato@empresa-teste.com',
            'phone': '+5511999999999',
            'subscription_plan': 'basic',
            'max_projects': 10,
            'max_users': 5,
        }
    
    def test_create_tenant(self):
        """Testa criação de tenant"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.assertEqual(tenant.name, 'Empresa Teste')
        self.assertEqual(tenant.slug, 'empresa-teste')
        self.assertTrue(tenant.is_active)
    
    def test_tenant_str(self):
        """Testa representação string do tenant"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.assertIn('Empresa Teste', str(tenant))
        self.assertIn('empresa-teste', str(tenant))
    
    def test_tenant_unique_slug(self):
        """Testa que slug deve ser único"""
        Tenant.objects.create(**self.tenant_data)
        with self.assertRaises(Exception):
            Tenant.objects.create(**self.tenant_data)
    
    def test_is_subscription_active(self):
        """Testa verificação de assinatura ativa"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.assertTrue(tenant.is_subscription_active)
        
        tenant.is_active = False
        tenant.save()
        self.assertFalse(tenant.is_subscription_active)
    
    def test_can_create_project(self):
        """Testa verificação de limite de projetos"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.assertTrue(tenant.can_create_project(5))
        self.assertFalse(tenant.can_create_project(10))
        self.assertFalse(tenant.can_create_project(15))


class TenantAPITest(TestCase):
    """Testes para API de Tenants"""
    
    def setUp(self):
        """Setup para testes de API"""
        self.client = APIClient()
        # Criar usuário admin
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            is_staff=True,
            is_superuser=True
        )
        # Criar usuário normal
        self.normal_user = User.objects.create_user(
            username='user',
            email='user@test.com',
            password='testpass123'
        )
        self.tenant_data = {
            'name': 'Empresa Teste',
            'slug': 'empresa-teste',
            'domain': 'empresa-teste.structurone.com',
            'email': 'contato@empresa-teste.com',
            'subscription_plan': 'basic',
            'max_projects': 10,
            'max_users': 5,
        }
    
    def test_list_tenants_requires_auth(self):
        """Testa que listar tenants requer autenticação"""
        response = self.client.get('/api/tenants/')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_list_tenants_requires_admin(self):
        """Testa que listar tenants requer permissão de admin"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.get('/api/tenants/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
    
    def test_list_tenants_as_admin(self):
        """Testa listagem de tenants como admin"""
        Tenant.objects.create(**self.tenant_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/tenants/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)
    
    def test_create_tenant(self):
        """Testa criação de tenant via API"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post('/api/tenants/', self.tenant_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Tenant.objects.count(), 1)
        self.assertEqual(Tenant.objects.get().name, 'Empresa Teste')
    
    def test_get_tenant_detail(self):
        """Testa obter detalhes de um tenant"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/tenants/{tenant.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Empresa Teste')
    
    def test_update_tenant(self):
        """Testa atualização de tenant"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.client.force_authenticate(user=self.admin_user)
        update_data = {'name': 'Empresa Atualizada'}
        response = self.client.patch(f'/api/tenants/{tenant.id}/', update_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tenant.refresh_from_db()
        self.assertEqual(tenant.name, 'Empresa Atualizada')
    
    def test_delete_tenant(self):
        """Testa exclusão de tenant"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/tenants/{tenant.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Tenant.objects.count(), 0)
    
    def test_activate_tenant(self):
        """Testa ativação de tenant"""
        self.tenant_data['is_active'] = False
        tenant = Tenant.objects.create(**self.tenant_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'/api/tenants/{tenant.id}/activate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tenant.refresh_from_db()
        self.assertTrue(tenant.is_active)
    
    def test_deactivate_tenant(self):
        """Testa desativação de tenant"""
        tenant = Tenant.objects.create(**self.tenant_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(f'/api/tenants/{tenant.id}/deactivate/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        tenant.refresh_from_db()
        self.assertFalse(tenant.is_active)
    
    def test_tenant_stats(self):
        """Testa endpoint de estatísticas"""
        Tenant.objects.create(**self.tenant_data)
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/tenants/stats/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total', response.data)
        self.assertIn('active', response.data)

