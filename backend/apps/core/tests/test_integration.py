"""
Integration Tests
Testes de integração para API, autenticação, multi-tenant e permissões
"""
from datetime import timedelta
from django.test import TestCase
from django.utils import timezone
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from apps.core.models import User, OnboardingProgress, PasswordResetToken
from apps.tenants.models import Tenant

User = get_user_model()


class AuthAPITest(TestCase):
    """Testes de integração para API de autenticação"""
    
    def setUp(self):
        """Setup para testes"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
    
    def test_register_user_api(self):
        """Testa registro via API"""
        data = {
            'email': 'newuser@test.com',
            'password': 'Test123!@#',
            'password_confirm': 'Test123!@#',
            'first_name': 'João',
            'last_name': 'Silva',
            'tenant_slug': 'empresa-teste',
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], 'newuser@test.com')
        self.assertIn('access', response.data['tokens'])
        self.assertIn('refresh', response.data['tokens'])
    
    def test_register_user_duplicate_email(self):
        """Testa registro com email duplicado"""
        User.objects.create_user(
            email='existing@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        data = {
            'email': 'existing@test.com',
            'password': 'Test123!@#',
            'password_confirm': 'Test123!@#',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'tenant_slug': 'empresa-teste',
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_register_user_password_mismatch(self):
        """Testa registro com senhas não coincidindo"""
        data = {
            'email': 'user@test.com',
            'password': 'Test123!@#',
            'password_confirm': 'Different123!@#',
            'first_name': 'João',
            'last_name': 'Silva',
            'tenant_slug': 'empresa-teste',
        }
        
        response = self.client.post('/api/auth/register/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password_confirm', str(response.data))
    
    def test_login_api(self):
        """Testa login via API"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        data = {
            'email': 'user@test.com',
            'password': 'Test123!@#',
        }
        
        response = self.client.post('/api/auth/login/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('tokens', response.data)
        self.assertEqual(response.data['user']['email'], 'user@test.com')
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        data = {
            'email': 'user@test.com',
            'password': 'WrongPassword123!',
        }
        
        response = self.client.post('/api/auth/login/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_locked_account(self):
        """Testa login com conta bloqueada"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        # Bloquear conta
        user.failed_login_attempts = 3
        user.locked_until = timezone.now() + timedelta(minutes=5)
        user.save()
        
        data = {
            'email': 'user@test.com',
            'password': 'Test123!@#',
        }
        
        response = self.client.post('/api/auth/login/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_me_api(self):
        """Testa obter dados do usuário logado"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        # Autenticar
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = self.client.get('/api/auth/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user@test.com')
        self.assertEqual(response.data['first_name'], 'João')
        self.assertIn('tenant', response.data)
    
    def test_get_me_unauthorized(self):
        """Testa obter dados sem autenticação"""
        response = self.client.get('/api/auth/me/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_logout_api(self):
        """Testa logout via API"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        refresh = RefreshToken.for_user(user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        data = {
            'refresh': str(refresh),
        }
        
        response = self.client.post('/api/auth/logout/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class PasswordResetAPITest(TestCase):
    """Testes de integração para API de reset de senha"""
    
    def setUp(self):
        """Setup para testes"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
        self.user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
    
    def test_request_password_reset_api(self):
        """Testa solicitar reset de senha via API"""
        data = {
            'email': 'user@test.com',
        }
        
        response = self.client.post('/api/password-reset/request/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(PasswordResetToken.objects.filter(user=self.user).exists())
    
    def test_confirm_password_reset_api(self):
        """Testa confirmar reset de senha via API"""
        token_obj = PasswordResetToken.create_for_user(self.user)
        
        data = {
            'token': token_obj.token,
            'new_password': 'NewPassword123!@#',
            'new_password_confirm': 'NewPassword123!@#',
        }
        
        response = self.client.post('/api/password-reset/confirm/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se senha foi alterada
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123!@#'))
        
        # Verificar se token foi marcado como usado
        token_obj.refresh_from_db()
        self.assertTrue(token_obj.used)
    
    def test_confirm_password_reset_invalid_token(self):
        """Testa confirmar reset com token inválido"""
        data = {
            'token': 'invalid-token',
            'new_password': 'NewPassword123!@#',
            'new_password_confirm': 'NewPassword123!@#',
        }
        
        response = self.client.post('/api/password-reset/confirm/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_confirm_password_reset_password_mismatch(self):
        """Testa confirmar reset com senhas não coincidindo"""
        token_obj = PasswordResetToken.create_for_user(self.user)
        
        data = {
            'token': token_obj.token,
            'new_password': 'NewPassword123!@#',
            'new_password_confirm': 'DifferentPassword123!@#',
        }
        
        response = self.client.post('/api/password-reset/confirm/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class OnboardingAPITest(TestCase):
    """Testes de integração para API de onboarding"""
    
    def setUp(self):
        """Setup para testes"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
        self.user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
            role='admin',
        )
        
        # Autenticar
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
    
    def test_get_onboarding_progress(self):
        """Testa obter progresso do onboarding"""
        response = self.client.get('/api/onboarding/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('step', response.data)
        self.assertIn('completed', response.data)
        self.assertIn('data', response.data)
    
    def test_update_onboarding_progress(self):
        """Testa atualizar progresso do onboarding"""
        data = {
            'step': 2,
            'data': {
                'company_name': 'Test Company',
                'cnpj': '12.345.678/0001-90',
            }
        }
        
        response = self.client.post('/api/onboarding/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['step'], 2)
        self.assertEqual(response.data['data']['company_name'], 'Test Company')
    
    def test_update_onboarding_with_country(self):
        """Testa atualizar onboarding com país (deve configurar i18n automaticamente)"""
        data = {
            'step': 1,
            'data': {
                'company_name': 'Test Company',
                'country': 'US',
            }
        }
        
        response = self.client.post('/api/onboarding/', data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verificar se i18n foi configurado automaticamente
        self.tenant.refresh_from_db()
        self.assertEqual(self.tenant.country, 'US')
        self.assertEqual(self.tenant.language, 'en-us')
        self.assertEqual(self.tenant.currency, 'USD')
    
    def test_complete_onboarding(self):
        """Testa completar onboarding"""
        # Criar onboarding
        OnboardingProgress.objects.create(
            tenant=self.tenant,
            step=3,
            completed=False,
        )
        
        response = self.client.post('/api/onboarding/complete/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['onboarding_completed'])
        
        # Verificar se foi marcado como completo
        onboarding = OnboardingProgress.objects.get(tenant=self.tenant)
        self.assertTrue(onboarding.completed)
        self.assertEqual(onboarding.step, 4)
        
        # Verificar se usuário foi marcado
        self.user.refresh_from_db()
        self.assertTrue(self.user.onboarding_completed)


class MultiTenantIsolationTest(TestCase):
    """Testes de isolamento multi-tenant"""
    
    def setUp(self):
        """Setup para testes"""
        self.client = APIClient()
        
        # Criar dois tenants
        self.tenant1 = Tenant.objects.create(
            name='Empresa 1',
            slug='empresa-1',
            domain='empresa-1.structurone.com',
            email='contato@empresa-1.com',
        )
        self.tenant2 = Tenant.objects.create(
            name='Empresa 2',
            slug='empresa-2',
            domain='empresa-2.structurone.com',
            email='contato@empresa-2.com',
        )
        
        # Criar usuários em cada tenant
        self.user1 = User.objects.create_user(
            email='user1@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant1,
        )
        self.user2 = User.objects.create_user(
            email='user2@test.com',
            password='Test123!@#',
            first_name='Maria',
            last_name='Santos',
            tenant=self.tenant2,
        )
    
    def test_user_cannot_access_other_tenant_data(self):
        """Testa que usuário não pode acessar dados de outro tenant"""
        # Autenticar como user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Tentar acessar dados do usuário (deve retornar apenas do próprio tenant)
        response = self.client.get('/api/users/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve retornar apenas usuários do tenant1
        user_emails = [user['email'] for user in response.data['results']]
        self.assertIn('user1@test.com', user_emails)
        self.assertNotIn('user2@test.com', user_emails)
    
    def test_same_email_different_tenants(self):
        """Testa que mesmo email pode existir em tenants diferentes"""
        # Nota: Como email é único globalmente no modelo atual,
        # este teste verifica que o sistema previne duplicação
        # Em produção, isso seria tratado com unique_together (email, tenant)
        
        # Verificar que user1 existe no tenant1
        self.assertTrue(User.objects.filter(email='user1@test.com', tenant=self.tenant1).exists())
        
        # Tentar criar com mesmo email em tenant diferente deve falhar
        # (devido à constraint única no email)
        with self.assertRaises(Exception):
            User.objects.create_user(
                email='user1@test.com',  # Mesmo email do user1
                password='Test123!@#',
                first_name='Pedro',
                last_name='Costa',
                tenant=self.tenant2,
            )
    
    def test_onboarding_isolation(self):
        """Testa que onboarding é isolado por tenant"""
        # Criar onboarding para tenant1
        onboarding1 = OnboardingProgress.objects.create(
            tenant=self.tenant1,
            step=2,
            data={'company_name': 'Company 1'},
        )
        
        # Criar onboarding para tenant2
        onboarding2 = OnboardingProgress.objects.create(
            tenant=self.tenant2,
            step=1,
            data={'company_name': 'Company 2'},
        )
        
        # Autenticar como user1
        refresh = RefreshToken.for_user(self.user1)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        # Obter onboarding (deve retornar apenas do tenant1)
        response = self.client.get('/api/onboarding/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['step'], 2)
        self.assertEqual(response.data['data']['company_name'], 'Company 1')


class PermissionsTest(TestCase):
    """Testes de permissões"""
    
    def setUp(self):
        """Setup para testes"""
        self.client = APIClient()
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
        
        # Criar usuários com diferentes roles
        self.admin = User.objects.create_user(
            email='admin@test.com',
            password='Test123!@#',
            first_name='Admin',
            last_name='User',
            tenant=self.tenant,
            role='admin',
        )
        self.user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='Regular',
            last_name='User',
            tenant=self.tenant,
            role='user',
        )
    
    def test_authenticated_user_can_access_me(self):
        """Testa que usuário autenticado pode acessar /me"""
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = self.client.get('/api/auth/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_unauthenticated_user_cannot_access_me(self):
        """Testa que usuário não autenticado não pode acessar /me"""
        response = self.client.get('/api/auth/me/')
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_user_can_access_own_data(self):
        """Testa que usuário pode acessar seus próprios dados"""
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        
        response = self.client.get('/api/users/me/')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], 'user@test.com')

