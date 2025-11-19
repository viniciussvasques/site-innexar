# API Endpoints - StructurOne

## 📋 Índice

- [Base URL](#base-url)
- [Autenticação](#autenticação)
- [Endpoints de Autenticação](#endpoints-de-autenticação)
- [Endpoints de Onboarding](#endpoints-de-onboarding)
- [Endpoints de Reset de Senha](#endpoints-de-reset-de-senha)
- [Endpoints de Usuários](#endpoints-de-usuários)
- [Códigos de Status HTTP](#códigos-de-status-http)
- [Tratamento de Erros](#tratamento-de-erros)
- [Segurança e Tokens](#segurança-e-tokens)

---

## Base URL

```
http://localhost:8010/api/
```

**Produção**: `https://api.structurone.com/api/`

---

## Autenticação

A API utiliza **JWT (JSON Web Tokens)** para autenticação. Todos os endpoints (exceto registro, login e reset de senha) requerem um token de acesso válido.

### Como usar tokens

1. **Obter tokens**: Faça login ou registro para receber `access` e `refresh` tokens
2. **Usar access token**: Inclua no header `Authorization` de todas as requisições autenticadas
3. **Renovar access token**: Use o `refresh` token quando o `access` token expirar
4. **Fazer logout**: Invalide os tokens para garantir segurança

### Formato do Header

```http
Authorization: Bearer {access_token}
```

### Validade dos Tokens

- **Access Token**: 15 minutos (padrão)
- **Refresh Token**: 7 dias (padrão)
- **Token Blacklist**: Tokens invalidados via logout são imediatamente bloqueados

---

## Endpoints de Autenticação

### `POST /api/auth/register/`

Registra um novo usuário no sistema. Se for o primeiro usuário do tenant, recebe role `admin`, caso contrário recebe `user`.

**Permissão**: Público (não requer autenticação)

**Request Body**:

```json
{
  "email": "usuario@exemplo.com",
  "password": "SenhaSegura123!",
  "password_confirm": "SenhaSegura123!",
  "first_name": "João",
  "last_name": "Silva",
  "phone": "+5511999999999",
  "tenant_slug": "empresa-abc"
}
```

**Campos Obrigatórios**:

- `email`: Email válido e único no tenant
- `password`: Mínimo 8 caracteres, deve conter maiúscula, minúscula, número e caractere especial
- `password_confirm`: Deve ser igual a `password`
- `first_name`: Nome do usuário
- `last_name`: Sobrenome do usuário

**Campos Opcionais**:

- `phone`: Telefone com código do país
- `tenant_slug`: Slug do tenant (se não fornecido, será criado automaticamente baseado no email)

**Response 201 Created**:

```json
{
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "last_name": "Silva",
    "full_name": "João Silva",
    "phone": "+5511999999999",
    "avatar": null,
    "role": "admin",
    "tenant": {
      "id": 1,
      "name": "Empresa ABC",
      "slug": "empresa-abc",
      "domain": "empresa-abc.structurone.com",
      "email": "contato@empresa-abc.com",
      "language": "pt-br",
      "country": "BR",
      "currency": "BRL",
      "timezone": "America/Sao_Paulo",
      "date_format": "DD/MM/YYYY",
      "number_format": "1.234,56"
    },
    "onboarding_completed": false,
    "onboarding_step": 0,
    "is_active": true,
    "date_joined": "2025-01-15T10:30:00Z",
    "last_login": null
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Erros**:

- `400 Bad Request`: Dados inválidos ou senha não atende critérios
- `400 Bad Request`: Email já existe no tenant
- `400 Bad Request`: Senhas não coincidem
- `404 Not Found`: Tenant não encontrado (se `tenant_slug` fornecido)
- `400 Bad Request`: Tenant inativo

**Exemplo de Erro**:

```json
{
  "email": ["Este email já está em uso."],
  "password": ["A senha deve conter pelo menos 8 caracteres."]
}
```

---

### `POST /api/auth/login/`

Autentica um usuário existente e retorna tokens JWT.

**Permissão**: Público (não requer autenticação)

**Request Body**:

```json
{
  "email": "usuario@exemplo.com",
  "password": "SenhaSegura123!"
}
```

**Response 200 OK**:

```json
{
  "user": {
    "id": 1,
    "email": "usuario@exemplo.com",
    "first_name": "João",
    "last_name": "Silva",
    "full_name": "João Silva",
    "phone": "+5511999999999",
    "avatar": null,
    "role": "admin",
    "tenant": {
      "id": 1,
      "name": "Empresa ABC",
      "slug": "empresa-abc",
      "domain": "empresa-abc.structurone.com",
      "email": "contato@empresa-abc.com",
      "language": "pt-br",
      "country": "BR",
      "currency": "BRL",
      "timezone": "America/Sao_Paulo",
      "date_format": "DD/MM/YYYY",
      "number_format": "1.234,56"
    },
    "onboarding_completed": false,
    "onboarding_step": 2,
    "is_active": true,
    "date_joined": "2025-01-15T10:30:00Z",
    "last_login": "2025-01-16T14:20:00Z"
  },
  "tokens": {
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
}
```

**Erros**:

- `400 Bad Request`: Credenciais inválidas
- `423 Locked`: Conta bloqueada temporariamente (após múltiplas tentativas falhas)
- `400 Bad Request`: Usuário inativo
- `400 Bad Request`: Tenant inativo

**Exemplo de Erro**:

```json
{
  "detail": "Credenciais inválidas."
}
```

---

### `POST /api/auth/logout/`

Invalida o refresh token e o access token atual, colocando-os na blacklist. Após o logout, os tokens não podem mais ser usados.

**Permissão**: Requer autenticação

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Request Body**:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response 200 OK**:

```json
{
  "message": "Logout realizado com sucesso"
}
```

**Erros**:

- `400 Bad Request`: Refresh token não fornecido
- `400 Bad Request`: Token inválido ou já invalidado
- `401 Unauthorized`: Token de acesso inválido ou expirado

**Importante**: Após o logout, qualquer tentativa de usar os tokens invalidados resultará em `401 Unauthorized`.

---

### `POST /api/auth/token/refresh/`

Renova o access token usando o refresh token. O refresh token também é rotacionado (novo refresh token é retornado).

**Permissão**: Público (não requer autenticação)

**Request Body**:

```json
{
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response 200 OK**:

```json
{
  "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
  "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Nota**: O refresh token antigo é automaticamente invalidado (token rotation).

**Erros**:

- `400 Bad Request`: Refresh token não fornecido
- `401 Unauthorized`: Refresh token inválido ou expirado
- `401 Unauthorized`: Refresh token está na blacklist

---

### `GET /api/auth/me/`

Retorna os dados completos do usuário autenticado, incluindo informações do tenant e configurações de i18n.

**Permissão**: Requer autenticação

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Response 200 OK**:

```json
{
  "id": 1,
  "email": "usuario@exemplo.com",
  "first_name": "João",
  "last_name": "Silva",
  "full_name": "João Silva",
  "phone": "+5511999999999",
  "avatar": "https://example.com/media/avatars/user.jpg",
  "role": "admin",
  "tenant": {
    "id": 1,
    "name": "Empresa ABC",
    "slug": "empresa-abc",
    "domain": "empresa-abc.structurone.com",
    "email": "contato@empresa-abc.com",
    "language": "pt-br",
    "country": "BR",
    "currency": "BRL",
    "timezone": "America/Sao_Paulo",
    "date_format": "DD/MM/YYYY",
    "number_format": "1.234,56"
  },
  "onboarding_completed": false,
  "onboarding_step": 2,
  "is_active": true,
  "date_joined": "2025-01-15T10:30:00Z",
  "last_login": "2025-01-16T14:20:00Z"
}
```

**Erros**:

- `401 Unauthorized`: Token inválido, expirado ou na blacklist

---

## Endpoints de Onboarding

### `GET /api/onboarding/`

Obtém o progresso atual do onboarding do tenant do usuário autenticado.

**Permissão**: Requer autenticação

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Response 200 OK**:

```json
{
  "step": 2,
  "completed": false,
  "data": {
    "company_name": "Empresa ABC",
    "cnpj": "12.345.678/0001-90",
    "address": "Rua Exemplo, 123, São Paulo, SP",
    "logo": "https://example.com/media/logos/empresa-abc.png",
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

**Etapas do Onboarding**:

- `step: 0`: Não iniciado
- `step: 1`: Informações da Empresa
- `step: 2`: Configuração Inicial (i18n)
- `step: 3`: Primeiro Projeto (opcional)
- `step: 4`: Convidar Usuários (opcional)
- `completed: true`: Onboarding concluído

---

### `POST /api/onboarding/`

Atualiza o progresso do onboarding. Pode ser usado para salvar dados de qualquer etapa.

**Permissão**: Requer autenticação

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Request Body** (Etapa 1 - Informações da Empresa):

```json
{
  "step": 1,
  "data": {
    "company_name": "Empresa ABC",
    "cnpj": "12.345.678/0001-90",
    "address": "Rua Exemplo, 123, São Paulo, SP",
    "logo": "base64_image_or_url"
  }
}
```

**Request Body** (Etapa 2 - Configuração Inicial):

```json
{
  "step": 2,
  "data": {
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

**Response 200 OK**:

```json
{
  "step": 2,
  "completed": false,
  "data": {
    "company_name": "Empresa ABC",
    "cnpj": "12.345.678/0001-90",
    "address": "Rua Exemplo, 123, São Paulo, SP",
    "logo": "https://example.com/media/logos/empresa-abc.png",
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

**Erros**:

- `400 Bad Request`: Dados inválidos
- `400 Bad Request`: Etapa inválida (deve ser entre 1 e 4)
- `401 Unauthorized`: Token inválido ou expirado

---

### `POST /api/onboarding/complete/`

Marca o onboarding como completo. Apenas usuários com role `admin` podem completar o onboarding.

**Permissão**: Requer autenticação (role: admin)

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Request Body**: Vazio (não requer body)

**Response 200 OK**:

```json
{
  "message": "Onboarding concluído com sucesso",
  "onboarding_completed": true
}
```

**Erros**:

- `400 Bad Request`: Onboarding já está completo
- `400 Bad Request`: Etapas obrigatórias não foram concluídas
- `403 Forbidden`: Apenas administradores podem completar o onboarding
- `401 Unauthorized`: Token inválido ou expirado

---

## Endpoints de Reset de Senha

### `POST /api/password-reset/request/`

Solicita o reset de senha. Envia um email com link de recuperação.

**Permissão**: Público (não requer autenticação)

**Request Body**:

```json
{
  "email": "usuario@exemplo.com"
}
```

**Response 200 OK**:

```json
{
  "message": "Email de recuperação enviado"
}
```

**Nota**: Por segurança, a resposta sempre será de sucesso, mesmo se o email não existir no sistema.

**Erros**:

- `400 Bad Request`: Email não fornecido ou inválido
- `429 Too Many Requests`: Muitas solicitações (rate limit)

---

### `POST /api/password-reset/confirm/`

Confirma o reset de senha usando o token recebido por email.

**Permissão**: Público (não requer autenticação)

**Request Body**:

```json
{
  "token": "abc123def456...",
  "new_password": "NovaSenhaSegura123!",
  "new_password_confirm": "NovaSenhaSegura123!"
}
```

**Response 200 OK**:

```json
{
  "message": "Senha alterada com sucesso"
}
```

**Erros**:

- `400 Bad Request`: Token inválido ou expirado
- `400 Bad Request`: Senha não atende critérios
- `400 Bad Request`: Senhas não coincidem

**Exemplo de Erro**:

```json
{
  "detail": "Token inválido ou expirado."
}
```

---

## Endpoints de Usuários

### `GET /api/users/`

Lista todos os usuários do tenant do usuário autenticado.

**Permissão**: Requer autenticação

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Query Parameters**:

- `page`: Número da página (padrão: 1)
- `page_size`: Itens por página (padrão: 20)
- `search`: Busca por email ou nome
- `role`: Filtrar por role (`admin`, `user`)
- `is_active`: Filtrar por status ativo (`true`, `false`)

**Response 200 OK**:

```json
{
  "count": 10,
  "next": "http://localhost:8010/api/users/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "email": "usuario@exemplo.com",
      "full_name": "João Silva",
      "role": "admin",
      "is_active": true,
      "last_login": "2025-01-16T14:20:00Z"
    }
  ]
}
```

---

### `GET /api/users/{id}/`

Retorna os dados completos de um usuário específico.

**Permissão**: Requer autenticação

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Response 200 OK**:

```json
{
  "id": 1,
  "email": "usuario@exemplo.com",
  "first_name": "João",
  "last_name": "Silva",
  "full_name": "João Silva",
  "phone": "+5511999999999",
  "avatar": null,
  "role": "admin",
  "tenant": {
    "id": 1,
    "name": "Empresa ABC",
    "slug": "empresa-abc"
  },
  "onboarding_completed": true,
  "onboarding_step": 4,
  "is_active": true,
  "date_joined": "2025-01-15T10:30:00Z",
  "last_login": "2025-01-16T14:20:00Z"
}
```

**Erros**:

- `404 Not Found`: Usuário não encontrado
- `403 Forbidden`: Usuário não pertence ao mesmo tenant

---

### `POST /api/users/`

Cria um novo usuário no tenant do usuário autenticado.

**Permissão**: Requer autenticação (role: admin)

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Request Body**:

```json
{
  "email": "novo@exemplo.com",
  "password": "SenhaSegura123!",
  "password_confirm": "SenhaSegura123!",
  "first_name": "Maria",
  "last_name": "Santos",
  "phone": "+5511888888888",
  "role": "user"
}
```

**Response 201 Created**:

```json
{
  "id": 2,
  "email": "novo@exemplo.com",
  "first_name": "Maria",
  "last_name": "Santos",
  "full_name": "Maria Santos",
  "phone": "+5511888888888",
  "avatar": null,
  "role": "user",
  "tenant": {
    "id": 1,
    "name": "Empresa ABC",
    "slug": "empresa-abc"
  },
  "onboarding_completed": false,
  "onboarding_step": 0,
  "is_active": true,
  "date_joined": "2025-01-16T15:00:00Z",
  "last_login": null
}
```

**Erros**:

- `400 Bad Request`: Dados inválidos
- `400 Bad Request`: Email já existe no tenant
- `403 Forbidden`: Apenas administradores podem criar usuários

---

### `PUT /api/users/{id}/` ou `PATCH /api/users/{id}/`

Atualiza os dados de um usuário.

**Permissão**: Requer autenticação (próprio usuário ou admin)

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Request Body** (PATCH - atualização parcial):

```json
{
  "first_name": "João",
  "last_name": "Silva Santos",
  "phone": "+5511999999999"
}
```

**Response 200 OK**:

```json
{
  "id": 1,
  "email": "usuario@exemplo.com",
  "first_name": "João",
  "last_name": "Silva Santos",
  "full_name": "João Silva Santos",
  "phone": "+5511999999999",
  "avatar": null,
  "role": "admin",
  "tenant": {
    "id": 1,
    "name": "Empresa ABC",
    "slug": "empresa-abc"
  },
  "onboarding_completed": true,
  "onboarding_step": 4,
  "is_active": true,
  "date_joined": "2025-01-15T10:30:00Z",
  "last_login": "2025-01-16T14:20:00Z"
}
```

**Erros**:

- `400 Bad Request`: Dados inválidos
- `404 Not Found`: Usuário não encontrado
- `403 Forbidden`: Sem permissão para atualizar este usuário

---

### `DELETE /api/users/{id}/`

Desativa um usuário (soft delete).

**Permissão**: Requer autenticação (role: admin)

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Response 204 No Content**: Sem corpo de resposta

**Erros**:

- `404 Not Found`: Usuário não encontrado
- `403 Forbidden`: Apenas administradores podem desativar usuários
- `400 Bad Request`: Não é possível desativar o último administrador do tenant

---

### `GET /api/users/me/`

Retorna os dados do usuário autenticado (alias para `/api/auth/me/`).

**Permissão**: Requer autenticação

**Headers**:

```http
Authorization: Bearer {access_token}
```

**Response**: Mesmo formato de `GET /api/auth/me/`

---

## Códigos de Status HTTP

| Código                      | Significado         | Descrição                                          |
| --------------------------- | ------------------- | -------------------------------------------------- |
| `200 OK`                    | Sucesso             | Requisição bem-sucedida                            |
| `201 Created`               | Criado              | Recurso criado com sucesso                         |
| `204 No Content`            | Sem conteúdo        | Requisição bem-sucedida, sem corpo de resposta     |
| `400 Bad Request`           | Requisição inválida | Dados inválidos ou erro na requisição              |
| `401 Unauthorized`          | Não autenticado     | Token ausente, inválido, expirado ou na blacklist  |
| `403 Forbidden`             | Sem permissão       | Usuário autenticado, mas sem permissão para a ação |
| `404 Not Found`             | Não encontrado      | Recurso não encontrado                             |
| `423 Locked`                | Bloqueado           | Conta bloqueada temporariamente                    |
| `429 Too Many Requests`     | Muitas requisições  | Rate limit excedido                                |
| `500 Internal Server Error` | Erro do servidor    | Erro interno do servidor                           |

---

## Tratamento de Erros

### Formato Padrão de Erro

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Erros de Validação

```json
{
  "field_name": ["Erro específico do campo 1", "Erro específico do campo 2"],
  "other_field": ["Outro erro"]
}
```

### Exemplos de Erros Comuns

**Token Inválido**:

```json
{
  "detail": "Token inválido ou expirado."
}
```

**Credenciais Inválidas**:

```json
{
  "detail": "Credenciais inválidas."
}
```

**Sem Permissão**:

```json
{
  "detail": "Você não tem permissão para realizar esta ação."
}
```

**Recurso Não Encontrado**:

```json
{
  "detail": "Não encontrado."
}
```

---

## Segurança e Tokens

### Token Blacklist

O sistema implementa **token blacklist** para invalidar tokens imediatamente após logout:

- **Access tokens** são rastreados e podem ser invalidados
- **Refresh tokens** são automaticamente invalidados no logout
- Tokens na blacklist retornam `401 Unauthorized` em qualquer tentativa de uso

### Boas Práticas

1. **Armazenar tokens com segurança**: Use `httpOnly` cookies ou `localStorage` com cuidado
2. **Renovar tokens proativamente**: Renove o access token antes de expirar
3. **Fazer logout adequadamente**: Sempre chame o endpoint de logout ao sair
4. **Não compartilhar tokens**: Tokens são pessoais e não devem ser compartilhados
5. **Usar HTTPS**: Sempre use HTTPS em produção para proteger tokens em trânsito

### Fluxo de Autenticação Recomendado

```
1. Login/Registro → Recebe access + refresh tokens
2. Armazenar tokens com segurança
3. Usar access token em todas as requisições
4. Quando access token expirar (401):
   a. Usar refresh token para obter novos tokens
   b. Atualizar tokens armazenados
   c. Repetir requisição original
5. Ao fazer logout:
   a. Chamar endpoint de logout
   b. Remover tokens do armazenamento
   c. Redirecionar para login
```

### Rate Limiting

Alguns endpoints possuem rate limiting para prevenir abuso:

- **Login**: Máximo 5 tentativas por minuto por IP
- **Reset de Senha**: Máximo 3 solicitações por hora por email
- **Registro**: Máximo 3 registros por hora por IP

---

## Paginação

Endpoints de listagem suportam paginação usando query parameters:

```
GET /api/users/?page=2&page_size=50
```

**Query Parameters**:

- `page`: Número da página (padrão: 1)
- `page_size`: Itens por página (padrão: 20, máximo: 100)

**Response Format**:

```json
{
  "count": 100,
  "next": "http://localhost:8010/api/users/?page=3",
  "previous": "http://localhost:8010/api/users/?page=1",
  "results": [...]
}
```

---

## Filtros e Busca

Endpoints de listagem suportam filtros e busca:

```
GET /api/users/?search=joão&role=admin&is_active=true
```

**Operadores Comuns**:

- `search`: Busca textual (email, nome)
- `role`: Filtro exato (`admin`, `user`)
- `is_active`: Filtro booleano (`true`, `false`)

---

## Versão da API

A versão atual da API é **0.1.0**.

Para verificar a versão e endpoints disponíveis:

```http
GET /api/
```

**Response**:

```json
{
  "name": "StructurOne API",
  "version": "0.1.0",
  "endpoints": {
    "auth": "/api/auth/",
    "onboarding": "/api/onboarding/",
    "users": "/api/users/",
    "password-reset": "/api/password-reset/",
    "projects": "/api/projects/",
    "investors": "/api/investors/",
    "financial": "/api/financial/"
  }
}
```

---

## Suporte

Para dúvidas ou problemas com a API:

- **Documentação**: `/docs/` (quando disponível)
- **Issues**: GitHub Issues
- **Email**: suporte@structurone.com

---

**Última atualização**: 2025-01-16
