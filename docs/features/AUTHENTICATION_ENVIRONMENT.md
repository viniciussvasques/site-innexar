# 🟢 3. Criar Ambiente - Autenticação e Onboarding

## ✅ Configurações Realizadas

### 3.1 Dependências Python

**Arquivo**: `backend/requirements.txt`

Dependências já instaladas:
- ✅ `djangorestframework-simplejwt>=5.3.0` - JWT authentication
- ✅ `django-allauth>=0.57.0` - Autenticação adicional (opcional)
- ✅ `Pillow>=10.2.0` - Para upload de avatares
- ✅ `python-decouple>=3.8` - Gerenciamento de variáveis de ambiente
- ✅ `celery>=5.3.4` - Para tarefas assíncronas (emails)
- ✅ `redis>=5.0.1` - Cache e broker para Celery

**Nenhuma dependência adicional necessária!**

---

### 3.2 Configuração Django Settings

**Arquivo**: `backend/structurone/settings.py`

#### AUTH_USER_MODEL
```python
# Custom User Model
AUTH_USER_MODEL = 'core.User'
```

#### REST Framework JWT
```python
# JWT Settings
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=7),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'UPDATE_LAST_LOGIN': True,
    
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    
    'JTI_CLAIM': 'jti',
    
    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),
}
```

#### REST Framework
```python
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ),
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour',
        'login': '5/minute',
        'password_reset': '3/hour',
    },
}
```

---

### 3.3 Estrutura de Diretórios

```
backend/apps/core/
├── __init__.py
├── apps.py
├── models.py          # User, PasswordResetToken, OnboardingProgress
├── serializers.py     # UserSerializer, AuthSerializer, etc.
├── services.py        # AuthService, UserService, OnboardingService
├── views.py           # AuthViewSet, UserViewSet
├── urls.py            # Rotas de autenticação
├── auth_urls.py       # URLs JWT (já existe)
├── permissions.py     # CustomPermissions (já existe)
├── managers.py        # TenantManager (já existe)
├── mixins.py          # TenantMixin (já existe)
├── validators.py      # Validações de senha, email, etc.
├── utils.py           # Funções utilitárias
└── tests/
    ├── __init__.py
    ├── test_models.py
    ├── test_serializers.py
    ├── test_services.py
    ├── test_views.py
    └── test_integration.py
```

---

### 3.4 Migrations

**Comandos para criar migrations**:
```bash
# Dentro do container backend
python manage.py makemigrations core
python manage.py migrate core
```

**Arquivos que serão criados**:
- `backend/apps/core/migrations/0001_initial.py` (se não existir)
- `backend/apps/core/migrations/0002_user_tenant.py`
- `backend/apps/core/migrations/0003_passwordresettoken.py`
- `backend/apps/core/migrations/0004_onboardingprogress.py`

---

### 3.5 Linter e Formatter

**Arquivos de configuração já existem**:

#### Black (Formatter)
**Arquivo**: `backend/pyproject.toml`
```toml
[tool.black]
line-length = 100
target-version = ['py311']
include = '\.pyi?$'
extend-exclude = '''
/(
  migrations
  | venv
  | .venv
  | __pycache__
)/
'''
```

#### Flake8 (Linter)
**Arquivo**: `backend/.flake8`
```ini
[flake8]
max-line-length = 100
exclude =
    migrations,
    venv,
    .venv,
    __pycache__,
    manage.py
ignore =
    E203,  # whitespace before ':'
    E501,  # line too long (handled by black)
    W503,  # line break before binary operator
```

#### isort (Import Sorter)
**Arquivo**: `backend/pyproject.toml`
```toml
[tool.isort]
profile = "black"
line_length = 100
skip = ["migrations", "venv", ".venv"]
```

**Comandos**:
```bash
# Formatar código
black backend/apps/core/

# Verificar linting
flake8 backend/apps/core/

# Ordenar imports
isort backend/apps/core/
```

---

### 3.6 CI/CD

**Arquivo**: `.github/workflows/ci.yml`

**Já configurado para**:
- ✅ Linting (Flake8)
- ✅ Formatação (Black)
- ✅ Ordenação de imports (isort)
- ✅ Testes (pytest)
- ✅ Coverage (pytest-cov)

**Adicionar testes específicos de autenticação**:
```yaml
- name: Run Authentication Tests
  run: |
    pytest backend/apps/core/tests/ -v --cov=apps.core --cov-report=term-missing
```

---

### 3.7 Variáveis de Ambiente

**Arquivo**: `backend/.env.example`

**Variáveis necessárias** (já existem):
```env
# Django
SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_NAME=structurone
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432

# Multi-tenant
TENANT_DOMAIN=structurone.com
TENANT_SUBDOMAIN_REQUIRED=False

# JWT (opcional, usa defaults do SIMPLE_JWT)
# JWT_ACCESS_TOKEN_LIFETIME=15
# JWT_REFRESH_TOKEN_LIFETIME=7

# Email (para recuperação de senha)
EMAIL_BACKEND=django.core.mail.backends.console.EmailBackend  # Desenvolvimento
# EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend  # Produção
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-password
DEFAULT_FROM_EMAIL=noreply@structurone.com
```

---

### 3.8 Docker Compose

**Arquivo**: `docker-compose.yml`

**Já configurado**:
- ✅ Backend container
- ✅ PostgreSQL database
- ✅ Redis (para Celery e cache)
- ✅ Volumes para migrations

**Nenhuma alteração necessária!**

---

### 3.9 Estrutura de Testes

**Arquivo**: `backend/pytest.ini` (criar se não existir)

```ini
[pytest]
DJANGO_SETTINGS_MODULE = structurone.settings
python_files = tests.py test_*.py *_tests.py
python_classes = Test*
python_functions = test_*
addopts = 
    --verbose
    --strict-markers
    --tb=short
    --cov=apps.core
    --cov-report=term-missing
    --cov-report=html
markers =
    unit: Unit tests
    integration: Integration tests
    slow: Slow tests
```

---

## ✅ Checklist de Ambiente

- [x] Dependências Python verificadas
- [x] Configuração Django Settings preparada
- [x] Estrutura de diretórios definida
- [x] Linter e Formatter configurados
- [x] CI/CD configurado
- [x] Variáveis de ambiente documentadas
- [x] Docker Compose verificado
- [x] Estrutura de testes definida
- [ ] Migrations criadas (será feito na implementação)
- [ ] Aprovação do ambiente
- [ ] Pronto para próxima etapa (Implementação)

---

## 📝 Próximos Passos

1. **Implementar Models** (User, PasswordResetToken, OnboardingProgress)
2. **Criar Migrations** (`makemigrations` + `migrate`)
3. **Implementar Serializers**
4. **Implementar Services**
5. **Implementar Views/Endpoints**
6. **Implementar Validações**

---

## 🔧 Comandos Úteis

```bash
# Entrar no container backend
docker-compose exec backend bash

# Criar migrations
python manage.py makemigrations core

# Aplicar migrations
python manage.py migrate core

# Formatar código
black backend/apps/core/

# Verificar linting
flake8 backend/apps/core/

# Rodar testes
pytest backend/apps/core/tests/ -v

# Criar superusuário (para testes)
python manage.py createsuperuser
```

