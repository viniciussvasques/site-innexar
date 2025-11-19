# 🟣 2. Design da Solução - Autenticação e Onboarding

## 📊 Modelos de Dados

### Model: User
```python
class User(AbstractUser, TimeStampedModel, TenantMixin):
    """
    Usuário do sistema vinculado a um tenant
    """
    # Campos herdados de AbstractUser:
    # - username (não usado, usamos email)
    # - email (usado como login)
    # - password (hasheado)
    # - first_name, last_name
    # - is_active, is_staff, is_superuser
    # - date_joined, last_login
    
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='users',
        verbose_name='Tenant'
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Telefone'
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name='Avatar'
    )
    
    role = models.CharField(
        max_length=50,
        choices=[
            ('admin', 'Administrador'),
            ('manager', 'Gerente'),
            ('user', 'Usuário'),
            ('viewer', 'Visualizador'),
        ],
        default='user',
        verbose_name='Função'
    )
    
    onboarding_completed = models.BooleanField(
        default=False,
        verbose_name='Onboarding Completo'
    )
    
    onboarding_step = models.IntegerField(
        default=0,
        verbose_name='Etapa do Onboarding'
    )
    
    failed_login_attempts = models.IntegerField(
        default=0,
        verbose_name='Tentativas de Login Falhas'
    )
    
    locked_until = models.DateTimeField(
        blank=True,
        null=True,
        verbose_name='Bloqueado até'
    )
    
    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        unique_together = [['email', 'tenant']]  # Email único por tenant
        indexes = [
            models.Index(fields=['email', 'tenant']),
            models.Index(fields=['tenant', 'is_active']),
        ]
    
    def __str__(self):
        return f"{self.email} ({self.tenant.name})"
    
    def is_locked(self):
        """Verifica se a conta está bloqueada"""
        if self.locked_until:
            return timezone.now() < self.locked_until
        return False
    
    def increment_failed_login(self):
        """Incrementa tentativas falhas e bloqueia se necessário"""
        self.failed_login_attempts += 1
        if self.failed_login_attempts >= 3:
            self.locked_until = timezone.now() + timedelta(minutes=5)
        self.save(update_fields=['failed_login_attempts', 'locked_until'])
    
    def reset_failed_login(self):
        """Reseta tentativas falhas após login bem-sucedido"""
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_login_attempts', 'locked_until'])
```

### Model: PasswordResetToken
```python
class PasswordResetToken(TimeStampedModel):
    """
    Token para reset de senha
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name='Usuário'
    )
    
    token = models.CharField(
        max_length=64,
        unique=True,
        verbose_name='Token'
    )
    
    expires_at = models.DateTimeField(
        verbose_name='Expira em'
    )
    
    used = models.BooleanField(
        default=False,
        verbose_name='Usado'
    )
    
    class Meta:
        verbose_name = 'Token de Reset de Senha'
        verbose_name_plural = 'Tokens de Reset de Senha'
        indexes = [
            models.Index(fields=['token', 'used']),
            models.Index(fields=['expires_at']),
        ]
    
    def is_valid(self):
        """Verifica se o token é válido"""
        return not self.used and timezone.now() < self.expires_at
```

### Model: OnboardingProgress
```python
class OnboardingProgress(TimeStampedModel, TenantMixin):
    """
    Progresso do onboarding do tenant
    """
    tenant = models.OneToOneField(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='onboarding',
        verbose_name='Tenant'
    )
    
    step = models.IntegerField(
        default=0,
        verbose_name='Etapa Atual'
    )
    
    completed = models.BooleanField(
        default=False,
        verbose_name='Completo'
    )
    
    data = models.JSONField(
        default=dict,
        verbose_name='Dados Coletados'
    )
    
    class Meta:
        verbose_name = 'Progresso do Onboarding'
        verbose_name_plural = 'Progressos de Onboarding'
```

---

## 🔌 API Endpoints

### Autenticação

#### `POST /api/auth/register/`
**Descrição**: Registrar novo usuário

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "senhaSegura123",
  "first_name": "João",
  "last_name": "Silva",
  "tenant_slug": "empresa-abc",
  "phone": "+5511999999999"
}
```

**Response 201**:
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "João",
    "last_name": "Silva",
    "tenant": {
      "id": 1,
      "name": "Empresa ABC",
      "slug": "empresa-abc"
    },
    "role": "admin",
    "onboarding_completed": false
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Errors**:
- `400`: Dados inválidos
- `400`: Email já existe no tenant
- `404`: Tenant não encontrado
- `400`: Tenant inativo

---

#### `POST /api/auth/login/`
**Descrição**: Fazer login

**Request Body**:
```json
{
  "email": "user@example.com",
  "password": "senhaSegura123"
}
```

**Response 200**:
```json
{
  "user": {
    "id": 1,
    "email": "user@example.com",
    "first_name": "João",
    "last_name": "Silva",
    "tenant": {
      "id": 1,
      "name": "Empresa ABC",
      "slug": "empresa-abc"
    },
    "role": "admin",
    "onboarding_completed": false
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
  }
}
```

**Errors**:
- `400`: Credenciais inválidas
- `423`: Conta bloqueada (locked_until)
- `400`: Usuário inativo
- `400`: Tenant inativo

---

#### `POST /api/auth/logout/`
**Descrição**: Fazer logout (invalidar refresh token)

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response 200**:
```json
{
  "message": "Logout realizado com sucesso"
}
```

---

#### `POST /api/auth/token/refresh/`
**Descrição**: Renovar access token

**Request Body**:
```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."
}
```

**Response 200**:
```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGc..."  // Novo refresh token (rotation)
}
```

---

#### `GET /api/auth/me/`
**Descrição**: Obter dados do usuário logado

**Headers**: `Authorization: Bearer <access_token>`

**Response 200**:
```json
{
  "id": 1,
  "email": "user@example.com",
  "first_name": "João",
  "last_name": "Silva",
  "phone": "+5511999999999",
  "avatar": "https://example.com/media/avatars/user.jpg",
  "role": "admin",
  "tenant": {
    "id": 1,
    "name": "Empresa ABC",
    "slug": "empresa-abc",
    "domain": "empresa-abc.structurone.com"
  },
  "onboarding_completed": false,
  "onboarding_step": 2,
  "date_joined": "2024-01-15T10:30:00Z",
  "last_login": "2024-01-16T14:20:00Z"
}
```

---

#### `POST /api/auth/password/reset/`
**Descrição**: Solicitar reset de senha

**Request Body**:
```json
{
  "email": "user@example.com"
}
```

**Response 200**:
```json
{
  "message": "Email de recuperação enviado"
}
```

**Errors**:
- `400`: Email não encontrado
- `429`: Muitas solicitações (rate limit)

---

#### `POST /api/auth/password/reset/confirm/`
**Descrição**: Confirmar reset de senha

**Request Body**:
```json
{
  "token": "abc123...",
  "new_password": "novaSenhaSegura123"
}
```

**Response 200**:
```json
{
  "message": "Senha alterada com sucesso"
}
```

**Errors**:
- `400`: Token inválido ou expirado
- `400`: Senha não atende critérios

---

### Onboarding

#### `GET /api/onboarding/`
**Descrição**: Obter progresso do onboarding

**Headers**: `Authorization: Bearer <access_token>`

**Response 200**:
```json
{
  "step": 2,
  "completed": false,
  "data": {
    "company_name": "Empresa ABC",
    "cnpj": "12.345.678/0001-90",
    "address": "Rua Exemplo, 123"
  }
}
```

---

#### `POST /api/onboarding/`
**Descrição**: Salvar progresso do onboarding

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "step": 2,
  "data": {
    "company_name": "Empresa ABC",
    "cnpj": "12.345.678/0001-90",
    "address": "Rua Exemplo, 123",
    "logo": "base64_image_or_url",
    "primary_color": "#3B82F6",
    "country": "BR",
    "language": "pt-br",
    "currency": "BRL",
    "timezone": "America/Sao_Paulo",
    "date_format": "DD/MM/YYYY",
    "number_format": "1.234,56"
  }
}
```

**Response 200**:
```json
{
  "step": 2,
  "completed": false,
  "data": {
    "company_name": "Empresa ABC",
    "cnpj": "12.345.678/0001-90",
    "address": "Rua Exemplo, 123"
  }
}
```

---

#### `POST /api/onboarding/complete/`
**Descrição**: Marcar onboarding como completo

**Headers**: `Authorization: Bearer <access_token>`

**Response 200**:
```json
{
  "message": "Onboarding concluído com sucesso",
  "onboarding_completed": true
}
```

---

## 🔄 Fluxos de Estado

### Fluxo de Login
```
[Usuário] → [Frontend: /login]
    ↓
[Preencher email/senha]
    ↓
[POST /api/auth/login/]
    ↓
[Backend: Validar credenciais]
    ↓
    ├─ [Erro] → [Mostrar mensagem de erro]
    └─ [Sucesso] → [Gerar tokens JWT]
            ↓
    [Salvar tokens no localStorage]
            ↓
    [Verificar onboarding_completed]
            ↓
        ├─ [false] → [Redirecionar para /onboarding]
        └─ [true] → [Redirecionar para /dashboard]
```

### Fluxo de Registro
```
[Usuário] → [Frontend: /register]
    ↓
[Preencher formulário]
    ↓
[POST /api/auth/register/]
    ↓
[Backend: Validar dados]
    ↓
    ├─ [Erro] → [Mostrar mensagem de erro]
    └─ [Sucesso] → [Criar usuário]
            ↓
    [Verificar se é primeiro usuário do tenant]
            ↓
        ├─ [Sim] → [role = 'admin']
        └─ [Não] → [role = 'user']
            ↓
    [Gerar tokens JWT]
            ↓
    [Salvar tokens no localStorage]
            ↓
    [Redirecionar para /onboarding]
```

### Fluxo de Recuperação de Senha
```
[Usuário] → [Frontend: /forgot-password]
    ↓
[Preencher email]
    ↓
[POST /api/auth/password/reset/]
    ↓
[Backend: Gerar token único]
    ↓
[Salvar PasswordResetToken]
    ↓
[Enviar email com link]
    ↓
[Usuário clica no link]
    ↓
[Frontend: /reset-password?token=abc123]
    ↓
[Preencher nova senha]
    ↓
[POST /api/auth/password/reset/confirm/]
    ↓
[Backend: Validar token]
    ↓
    ├─ [Erro] → [Token inválido/expirado]
    └─ [Sucesso] → [Atualizar senha]
            ↓
    [Marcar token como usado]
            ↓
    [Redirecionar para /login]
```

### Fluxo de Onboarding
```
[Usuário logado] → [Verificar onboarding_completed]
    ↓
    ├─ [true] → [Redirecionar para /dashboard]
    └─ [false] → [Redirecionar para /onboarding]
            ↓
[Frontend: Wizard multi-step]
    ↓
[Etapa 1: Informações da Empresa]
    ↓
[POST /api/onboarding/ {step: 1, data: {...}}]
    ↓
[Etapa 2: Configuração Inicial]
    ↓
[POST /api/onboarding/ {step: 2, data: {...}}]
    ↓
[Etapa 3: Primeiro Projeto (opcional)]
    ↓
    ├─ [Pular] → [Ir para etapa 4]
    └─ [Preencher] → [Criar projeto]
            ↓
[Etapa 4: Convidar Usuários (opcional)]
    ↓
    ├─ [Pular] → [Finalizar]
    └─ [Preencher] → [Enviar convites]
            ↓
[POST /api/onboarding/complete/]
    ↓
[Backend: Marcar onboarding_completed = true]
    ↓
[Redirecionar para /dashboard]
```

---

## 🔐 Regras de Segurança + Permissões

### Permissões por Role

| Ação | Admin | Manager | User | Viewer |
|------|-------|---------|------|--------|
| Ver próprio perfil | ✅ | ✅ | ✅ | ✅ |
| Editar próprio perfil | ✅ | ✅ | ✅ | ❌ |
| Ver usuários do tenant | ✅ | ✅ | ✅ | ✅ |
| Criar usuários | ✅ | ✅ | ❌ | ❌ |
| Editar usuários | ✅ | ✅ | ❌ | ❌ |
| Deletar usuários | ✅ | ❌ | ❌ | ❌ |
| Ver projetos | ✅ | ✅ | ✅ | ✅ |
| Criar projetos | ✅ | ✅ | ✅ | ❌ |
| Editar projetos | ✅ | ✅ | ✅ | ❌ |
| Deletar projetos | ✅ | ✅ | ❌ | ❌ |
| Ver financeiro | ✅ | ✅ | ✅ | ❌ |
| Editar financeiro | ✅ | ✅ | ❌ | ❌ |

### Regras de Segurança

1. **Isolamento Multi-tenant**
   - Todas as queries devem filtrar por `tenant_id`
   - Middleware garante tenant correto
   - Usuário não pode acessar dados de outro tenant

2. **Validação de Senha**
   - Mínimo 8 caracteres
   - Pelo menos 1 letra maiúscula
   - Pelo menos 1 letra minúscula
   - Pelo menos 1 número
   - Pelo menos 1 caractere especial

3. **Rate Limiting**
   - Login: 5 tentativas por minuto por IP
   - Reset de senha: 3 solicitações por hora por email
   - Registro: 10 por hora por IP

4. **Tokens JWT**
   - Access token: 15 minutos
   - Refresh token: 7 dias
   - Refresh token rotation: Gerar novo refresh token a cada uso
   - Blacklist: Invalidar tokens em logout

5. **Bloqueio de Conta**
   - 3 tentativas falhas = bloqueio por 5 minutos
   - Admin pode desbloquear manualmente
   - Log de todas as tentativas

---

## 📐 Diagrama de Classes

```
┌─────────────────┐
│   AbstractUser  │
│  (Django Base)  │
└────────┬────────┘
         │
         │ extends
         │
┌────────▼────────┐
│      User       │
├─────────────────┤
│ + tenant (FK)   │
│ + phone         │
│ + avatar        │
│ + role          │
│ + onboarding_*  │
│ + failed_login_*│
└────────┬────────┘
         │
         │ 1:N
         │
┌────────▼──────────────┐
│ PasswordResetToken    │
├───────────────────────┤
│ + user (FK)           │
│ + token               │
│ + expires_at          │
│ + used                │
└───────────────────────┘

┌─────────────────┐
│     Tenant      │
└────────┬────────┘
         │
         │ 1:1
         │
┌────────▼──────────────┐
│ OnboardingProgress   │
├───────────────────────┤
│ + tenant (FK)        │
│ + step               │
│ + completed          │
│ + data (JSON)        │
└───────────────────────┘
```

---

## 🔄 Diagrama de Serviços

```
┌─────────────┐
│   Frontend  │
│  (Next.js)  │
└──────┬──────┘
       │
       │ HTTP/REST
       │
┌──────▼──────────────────┐
│   Backend API           │
│   (Django REST)         │
├─────────────────────────┤
│ - AuthService           │
│ - UserService           │
│ - OnboardingService     │
│ - PasswordResetService  │
└──────┬──────────────────┘
       │
       ├─────────┬─────────┐
       │         │         │
┌──────▼──┐ ┌───▼────┐ ┌──▼──────┐
│PostgreSQL│ │ Redis │ │ Celery  │
│          │ │       │ │ (Email) │
└──────────┘ └───────┘ └─────────┘
```

---

## ✅ Checklist de Entrega

- [x] Modelos de dados definidos
- [x] API endpoints documentados
- [x] Fluxos de estado mapeados
- [x] Diagrama de classes criado
- [x] Diagrama de serviços criado
- [x] Regras de segurança definidas
- [x] Permissões por role definidas
- [ ] Aprovação do design
- [ ] Pronto para próxima etapa (Criar Ambiente)

