# API Endpoints - StructurOne

## Base URL
```
http://localhost:8010/api/
```

## Autenticação

Todos os endpoints (exceto login) requerem autenticação JWT.

### Obter Token
```http
POST /api/auth/token/
Content-Type: application/json

{
  "username": "usuario",
  "password": "senha"
}
```

### Atualizar Token
```http
POST /api/auth/token/refresh/
Content-Type: application/json

{
  "refresh": "refresh_token_aqui"
}
```

### Usar Token
```http
Authorization: Bearer {access_token}
```

## Endpoints

### Projetos

#### Listar Projetos
```http
GET /api/projects/
Authorization: Bearer {token}
```

#### Criar Projeto
```http
POST /api/projects/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Nome do Projeto",
  "description": "Descrição",
  "status": "planning"
}
```

#### Detalhes do Projeto
```http
GET /api/projects/{id}/
Authorization: Bearer {token}
```

#### Atualizar Projeto
```http
PUT /api/projects/{id}/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Nome Atualizado",
  "completion_percentage": 50
}
```

#### Deletar Projeto
```http
DELETE /api/projects/{id}/
Authorization: Bearer {token}
```

### Investidores

#### Listar Investidores
```http
GET /api/investors/
Authorization: Bearer {token}
```

#### Criar Investidor
```http
POST /api/investors/
Authorization: Bearer {token}
Content-Type: application/json

{
  "name": "Nome do Investidor",
  "email": "investidor@email.com",
  "phone": "+5511999999999"
}
```

#### Detalhes do Investidor
```http
GET /api/investors/{id}/
Authorization: Bearer {token}
```

#### Investimentos do Investidor
```http
GET /api/investors/{id}/investments/
Authorization: Bearer {token}
```

### Financeiro

#### Listar Transações
```http
GET /api/financial/transactions/
Authorization: Bearer {token}
```

#### Criar Transação
```http
POST /api/financial/transactions/
Authorization: Bearer {token}
Content-Type: application/json

{
  "type": "income",
  "amount": 1000000,
  "currency": "BRL",
  "description": "Receita do projeto X",
  "date": "2025-01-15"
}
```

#### Fluxo de Caixa
```http
GET /api/financial/cashflow/
Authorization: Bearer {token}
```

### Documentos

#### Listar Documentos
```http
GET /api/documents/
Authorization: Bearer {token}
```

#### Upload de Documento
```http
POST /api/documents/upload/
Authorization: Bearer {token}
Content-Type: multipart/form-data

{
  "file": {arquivo},
  "name": "Nome do Documento",
  "type": "contract",
  "project_id": 1
}
```

#### Detalhes do Documento
```http
GET /api/documents/{id}/
Authorization: Bearer {token}
```

### Atualizações

#### Listar Atualizações
```http
GET /api/updates/
Authorization: Bearer {token}
```

#### Criar Atualização
```http
POST /api/updates/
Authorization: Bearer {token}
Content-Type: application/json

{
  "project_id": 1,
  "title": "Atualização da Obra",
  "description": "Progresso da construção",
  "completion_percentage": 45
}
```

#### Atualizações do Projeto
```http
GET /api/updates/project/{project_id}/
Authorization: Bearer {token}
```

## Códigos de Status

- `200 OK` - Sucesso
- `201 Created` - Criado com sucesso
- `400 Bad Request` - Erro na requisição
- `401 Unauthorized` - Não autenticado
- `403 Forbidden` - Sem permissão
- `404 Not Found` - Recurso não encontrado
- `500 Internal Server Error` - Erro do servidor

## Paginação

Todos os endpoints de listagem suportam paginação:

```
GET /api/projects/?page=1&page_size=20
```

## Filtros

Suporte a filtros e busca:

```
GET /api/projects/?search=nome&status=in_progress
```

## Respostas

### Sucesso
```json
{
  "id": 1,
  "name": "Projeto Exemplo",
  "status": "in_progress",
  "created_at": "2025-01-15T10:00:00Z"
}
```

### Erro
```json
{
  "error": "Mensagem de erro",
  "details": {
    "field": ["Erro específico do campo"]
  }
}
```

