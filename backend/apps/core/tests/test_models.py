"""
Unit Tests - Models
Testes unitários para os models do core
"""
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta
from apps.core.models import User, PasswordResetToken, OnboardingProgress
from apps.tenants.models import Tenant


class UserModelTest(TestCase):
    """Testes para o modelo User"""
    
    def setUp(self):
        """Setup para testes"""
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
    
    def test_create_user(self):
        """Testa criação de usuário"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        self.assertEqual(user.email, 'user@test.com')
        self.assertEqual(user.tenant, self.tenant)
        self.assertTrue(user.check_password('Test123!@#'))
        self.assertFalse(user.is_superuser)
        self.assertTrue(user.is_active)
    
    def test_user_str(self):
        """Testa representação string do usuário"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        self.assertIn('user@test.com', str(user))
        self.assertIn('Empresa Teste', str(user))
    
    def test_get_full_name(self):
        """Testa método get_full_name"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        self.assertEqual(user.get_full_name(), 'João Silva')
    
    def test_is_first_user_of_tenant(self):
        """Testa se é primeiro usuário do tenant"""
        user1 = User.objects.create_user(
            email='user1@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        self.assertTrue(user1.is_first_user_of_tenant())
        
        user2 = User.objects.create_user(
            email='user2@test.com',
            password='Test123!@#',
            first_name='Maria',
            last_name='Santos',
            tenant=self.tenant,
        )
        self.assertFalse(user2.is_first_user_of_tenant())
    
    def test_is_locked(self):
        """Testa verificação de conta bloqueada"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        self.assertFalse(user.is_locked())
        
        user.locked_until = timezone.now() + timedelta(minutes=5)
        user.save()
        self.assertTrue(user.is_locked())
        
        user.locked_until = timezone.now() - timedelta(minutes=1)
        user.save()
        self.assertFalse(user.is_locked())
    
    def test_increment_failed_login(self):
        """Testa incremento de tentativas falhas"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        self.assertEqual(user.failed_login_attempts, 0)
        
        user.increment_failed_login()
        self.assertEqual(user.failed_login_attempts, 1)
        self.assertFalse(user.is_locked())
        
        user.increment_failed_login()
        user.increment_failed_login()
        self.assertEqual(user.failed_login_attempts, 3)
        self.assertTrue(user.is_locked())
    
    def test_reset_failed_login(self):
        """Testa reset de tentativas falhas"""
        user = User.objects.create_user(
            email='user@test.com',
            password='Test123!@#',
            first_name='João',
            last_name='Silva',
            tenant=self.tenant,
        )
        
        user.failed_login_attempts = 3
        user.locked_until = timezone.now() + timedelta(minutes=5)
        user.save()
        
        user.reset_failed_login()
        self.assertEqual(user.failed_login_attempts, 0)
        self.assertIsNone(user.locked_until)


class PasswordResetTokenModelTest(TestCase):
    """Testes para o modelo PasswordResetToken"""
    
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
    
    def test_create_token(self):
        """Testa criação de token"""
        token = PasswordResetToken.create_for_user(self.user)
        
        self.assertEqual(token.user, self.user)
        self.assertIsNotNone(token.token)
        self.assertEqual(len(token.token), 43)  # token_urlsafe(32) = 43 chars
        self.assertFalse(token.used)
        self.assertGreater(token.expires_at, timezone.now())
    
    def test_is_valid(self):
        """Testa validação de token"""
        token = PasswordResetToken.create_for_user(self.user)
        
        self.assertTrue(token.is_valid())
        
        token.used = True
        token.save()
        self.assertFalse(token.is_valid())
        
        token.used = False
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        self.assertFalse(token.is_valid())


class OnboardingProgressModelTest(TestCase):
    """Testes para o modelo OnboardingProgress"""
    
    def setUp(self):
        """Setup para testes"""
        self.tenant = Tenant.objects.create(
            name='Empresa Teste',
            slug='empresa-teste',
            domain='empresa-teste.structurone.com',
            email='contato@empresa-teste.com',
        )
    
    def test_create_onboarding(self):
        """Testa criação de onboarding"""
        onboarding = OnboardingProgress.objects.create(
            tenant=self.tenant,
            step=0,
            completed=False,
            data={},
        )
        
        self.assertEqual(onboarding.tenant, self.tenant)
        self.assertEqual(onboarding.step, 0)
        self.assertFalse(onboarding.completed)
        self.assertEqual(onboarding.data, {})
    
    def test_update_step(self):
        """Testa atualização de etapa"""
        onboarding = OnboardingProgress.objects.create(
            tenant=self.tenant,
            step=0,
            data={},
        )
        
        onboarding.update_step(2, {'company_name': 'Test Company'})
        
        self.assertEqual(onboarding.step, 2)
        self.assertEqual(onboarding.data['company_name'], 'Test Company')
    
    def test_complete(self):
        """Testa completar onboarding"""
        onboarding = OnboardingProgress.objects.create(
            tenant=self.tenant,
            step=2,
            completed=False,
        )
        
        onboarding.complete()
        
        self.assertTrue(onboarding.completed)
        self.assertEqual(onboarding.step, 4)

