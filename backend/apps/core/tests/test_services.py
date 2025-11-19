"""
Unit Tests - Services
Testes unitários para os services do core
"""
from django.test import TestCase
from django.contrib.auth import get_user_model
from apps.core.services import AuthService, PasswordResetService, OnboardingService
from apps.core.models import PasswordResetToken, OnboardingProgress
from apps.tenants.models import Tenant

User = get_user_model()


class AuthServiceTest(TestCase):
    """Testes para AuthService"""
    
    def setUp(self):
        """Setup para testes"""
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
    
    def test_register_user(self):
        """Testa registro de usuário"""
        user, tokens = AuthService.register_user(
            email='newuser@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        self.assertEqual(user.email, 'newuser@test.com')
        self.assertEqual(user.tenant, self.tenant)
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)
        self.assertTrue(user.is_first_user_of_tenant())
        self.assertEqual(user.role, 'admin')  # Primeiro usuário vira admin
    
    def test_register_duplicate_email(self):
        """Testa registro com email duplicado"""
        User.objects.create_user(
            email='existing@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        with self.assertRaises(ValueError):
            AuthService.register_user(
                email='existing@test.com',
                password='Test123!@#',
                first_name='Maria',
                last_name='Santos',
                tenant=self.tenant,
            )
    
    def test_login_user(self):
        """Testa login de usuário"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        logged_user, tokens = AuthService.login_user(
            email='user@test.com',
            password='Test123!@#',
        )
        
        self.assertEqual(logged_user, user)
        self.assertIn('access', tokens)
        self.assertIn('refresh', tokens)
    
    def test_login_invalid_credentials(self):
        """Testa login com credenciais inválidas"""
        User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        with self.assertRaises(ValueError):
            AuthService.login_user(
                email='user@test.com',
                password='WrongPassword123!',
            )


class PasswordResetServiceTest(TestCase):
    """Testes para PasswordResetService"""
    
    def setUp(self):
        """Setup para testes"""
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
    
    def test_request_password_reset(self):
        """Testa solicitação de reset de senha"""
        result = PasswordResetService.request_password_reset('user@test.com')
        
        self.assertTrue(result)
        self.assertTrue(
            PasswordResetToken.objects.filter(user=self.user).exists()
        )
    
    def test_confirm_password_reset(self):
        """Testa confirmação de reset de senha"""
        token_obj = PasswordResetToken.create_for_user(self.user)
        
        result = PasswordResetService.confirm_password_reset(
            token_obj.token,
            'NewPassword123!@#'
        )
        
        self.assertTrue(result)
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('NewPassword123!@#'))
        
        token_obj.refresh_from_db()
        self.assertTrue(token_obj.used)


class OnboardingServiceTest(TestCase):
    """Testes para OnboardingService"""
    
    def setUp(self):
        """Setup para testes"""
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
    
    def test_get_or_create_onboarding(self):
        """Testa obter ou criar onboarding"""
        onboarding = OnboardingService.get_or_create_onboarding(self.tenant)
        
        self.assertEqual(onboarding.tenant, self.tenant)
        self.assertEqual(onboarding.step, 0)
        self.assertFalse(onboarding.completed)
    
    def test_update_onboarding_step(self):
        """Testa atualização de etapa do onboarding"""
        onboarding = OnboardingService.update_onboarding_step(
            self.tenant,
            step=2,
            data={'company_name': 'Test Company'}
        )
        
        self.assertEqual(onboarding.step, 2)
        self.assertEqual(onboarding.data['company_name'], 'Test Company')
    
    def test_complete_onboarding(self):
        """Testa completar onboarding"""
        user = User.objects.create_user(
            email='admin@test.com',
            password='Test123!@#',
            first_name='Admin',
            last_name='User',
            tenant=self.tenant,
            role='admin',
        )
        
        onboarding, admin_user = OnboardingService.complete_onboarding(self.tenant)
        
        self.assertTrue(onboarding.completed)
        self.assertEqual(onboarding.step, 4)
        self.assertEqual(admin_user, user)
        admin_user.refresh_from_db()
        self.assertTrue(admin_user.onboarding_completed)

