# API Endpoints - Billing e Pagamentos

## 📋 Índice

- [Base URL](#base-url)
- [Autenticação](#autenticação)
- [Endpoints de Planos](#endpoints-de-planos)
- [Endpoints de Assinaturas](#endpoints-de-assinaturas)
- [Endpoints de Faturas](#endpoints-de-faturas)
- [Endpoints de Pagamentos](#endpoints-de-pagamentos)
- [Endpoints de Métodos de Pagamento](#endpoints-de-métodos-de-pagamento)
- [Webhooks](#webhooks)
- [Códigos de Status HTTP](#códigos-de-status-http)
- [Tratamento de Erros](#tratamento-de-erros)

---

## Base URL

```
http://localhost:8010/api/billing/
```

**Produção**: `https://api.structurone.com/api/billing/`

---

## Autenticação

Todos os endpoints de billing requerem autenticação JWT. O token deve ser enviado no header:

```
Authorization: Bearer <access_token>
```

---

## Endpoints de Planos

### `GET /api/billing/plans/`

Lista todos os planos ativos disponíveis.

**Headers**: `Authorization: Bearer <access_token>`

**Response 200**:
```json
{
  "count": 4,
  "results": [
    {
      "id": 1,
      "name": "Básico",
      "slug": "basic",
      "description": "Ideal para pequenas construtoras",
      "price_monthly_brl": "297.00",
      "price_yearly_brl": "2970.00",
      "price_monthly_usd": "49.00",
      "price_yearly_usd": "490.00",
      "price_monthly_display": "R$ 297,00",
      "price_yearly_display": "R$ 2.970,00",
      "currency": "BRL",
      "max_projects": 5,
      "max_users": 5,
      "max_storage_gb": 5,
      "features": [
        "Relatórios básicos",
        "Suporte por email"
      ],
      "trial_days": 14,
      "is_featured": false,
      "created_at": "2025-01-16T10:00:00Z",
      "updated_at": "2025-01-16T10:00:00Z"
    }
  ]
}
```

**Notas**:
- Apenas planos ativos são retornados
- Preços são exibidos na moeda do país do tenant
- Ordenados por `display_order` e preço

---

### `GET /api/billing/plans/{slug}/`

Detalhes de um plano específico.

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `slug` (string): Slug do plano (ex: "basic", "professional")

**Response 200**: Objeto de plano completo (mesmo formato do item da listagem)

**Response 404**: Plano não encontrado

---

## Endpoints de Assinaturas

### `GET /api/billing/subscriptions/me/`

Retorna a assinatura atual do tenant do usuário autenticado.

**Headers**: `Authorization: Bearer <access_token>`

**Response 200**:
```json
{
  "id": 1,
  "plan": {
    "id": 2,
    "name": "Profissional",
    "slug": "professional",
    "price_monthly_brl": "797.00",
    "price_yearly_brl": "7970.00"
  },
  "status": "active",
  "current_period_start": "2025-01-01",
  "current_period_end": "2025-02-01",
  "trial_start": null,
  "trial_end": null,
  "is_trial": false,
  "cancel_at_period_end": false,
  "canceled_at": null,
  "gateway": "asaas",
  "payment_method": {
    "id": 1,
    "type": "card",
    "card_last4": "4242",
    "card_brand": "visa",
    "is_default": true
  },
  "is_active": true,
  "created_at": "2025-01-01T10:00:00Z",
  "updated_at": "2025-01-01T10:00:00Z"
}
```

**Response 404**: Nenhuma assinatura encontrada

---

### `POST /api/billing/subscriptions/create/`

Cria uma nova assinatura para o tenant do usuário autenticado.

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "plan_id": 2,
  "payment_method_id": 1,
  "billing_cycle": "monthly"
}
```

**Campos**:
- `plan_id` (integer, obrigatório): ID do plano
- `payment_method_id` (integer, opcional): ID do método de pagamento
- `billing_cycle` (string, opcional): "monthly" ou "yearly" (padrão: "monthly")

**Response 201**: Assinatura criada (mesmo formato de `/me/`)

**Response 400**: Erro de validação
```json
{
  "detail": "Tenant já possui uma assinatura ativa"
}
```

**Notas**:
- Se `payment_method_id` não for fornecido, primeira fatura ficará pendente
- Gateway é determinado automaticamente pelo país do tenant (BR → Asaas, US → Stripe)
- Primeira fatura é gerada automaticamente

---

### `PATCH /api/billing/subscriptions/{id}/upgrade/`

Faz upgrade de assinatura para um plano superior.

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `id` (integer): ID da assinatura

**Request Body**:
```json
{
  "plan_id": 3
}
```

**Response 200**:
```json
{
  "id": 1,
  "plan": {
    "id": 3,
    "name": "Enterprise",
    "slug": "enterprise"
  },
  "status": "active",
  "adjustment_invoice": {
    "id": 5,
    "invoice_number": "INV-2025-0005",
    "amount": "150.00",
    "status": "open"
  }
}
```

**Response 400**: Erro de validação
```json
{
  "detail": "Novo plano não está ativo"
}
```

**Notas**:
- Upgrade aplica imediatamente
- Fatura de ajuste (prorata) é gerada se necessário
- Limites do tenant são atualizados imediatamente

---

### `PATCH /api/billing/subscriptions/{id}/cancel/`

Cancela assinatura (ao fim do período atual).

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `id` (integer): ID da assinatura

**Request Body**:
```json
{
  "reason": "Não estou mais usando o sistema"
}
```

**Campos**:
- `reason` (string, opcional): Motivo do cancelamento

**Response 200**: Assinatura cancelada (mesmo formato de `/me/`)

**Notas**:
- Cancelamento não é imediato
- Acesso continua até fim do período pago
- Assinatura será cancelada em `current_period_end`

---

## Endpoints de Faturas

### `GET /api/billing/invoices/`

Lista todas as faturas do tenant do usuário autenticado.

**Headers**: `Authorization: Bearer <access_token>`

**Query Parameters**:
- `status` (string, opcional): Filtrar por status (draft, open, paid, void, uncollectible)
- `page` (integer, opcional): Número da página
- `page_size` (integer, opcional): Itens por página (máx: 100)

**Response 200**:
```json
{
  "count": 10,
  "next": "http://localhost:8010/api/billing/invoices/?page=2",
  "previous": null,
  "results": [
    {
      "id": 1,
      "subscription": {
        "id": 1,
        "plan": {
          "name": "Profissional",
          "slug": "professional"
        }
      },
      "invoice_number": "INV-2025-0001",
      "amount": "797.00",
      "currency": "BRL",
      "tax_amount": "0.00",
      "total_amount": "797.00",
      "status": "paid",
      "status_display": "Paga",
      "issue_date": "2025-01-01",
      "due_date": "2025-01-10",
      "paid_at": "2025-01-05T10:30:00Z",
      "gateway_pdf_url": "https://asaas.com/invoices/123.pdf",
      "line_items": [
        {
          "description": "Assinatura Profissional - monthly",
          "quantity": 1,
          "amount": 797.00
        }
      ],
      "notes": "",
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-05T10:30:00Z"
    }
  ]
}
```

---

### `GET /api/billing/invoices/{id}/`

Detalhes de uma fatura específica.

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `id` (integer): ID da fatura

**Response 200**: Fatura completa (mesmo formato do item da listagem)

**Response 404**: Fatura não encontrada ou não pertence ao tenant

---

### `GET /api/billing/invoices/{id}/pdf/`

Retorna URL do PDF da fatura (quando disponível).

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `id` (integer): ID da fatura

**Response 200**:
```json
{
  "pdf_url": "https://asaas.com/invoices/123.pdf"
}
```

**Response 404**: PDF não disponível

---

## Endpoints de Pagamentos

### `GET /api/billing/payments/`

Lista todos os pagamentos do tenant do usuário autenticado.

**Headers**: `Authorization: Bearer <access_token>`

**Query Parameters**:
- `status` (string, opcional): Filtrar por status (pending, processing, succeeded, failed, refunded, canceled)
- `page` (integer, opcional): Número da página
- `page_size` (integer, opcional): Itens por página

**Response 200**:
```json
{
  "count": 5,
  "next": null,
  "previous": null,
  "results": [
    {
      "id": 1,
      "invoice": {
        "id": 1,
        "invoice_number": "INV-2025-0001"
      },
      "payment_method": {
        "id": 1,
        "type": "card",
        "card_last4": "4242",
        "card_brand": "visa"
      },
      "amount": "797.00",
      "currency": "BRL",
      "status": "succeeded",
      "status_display": "Sucesso",
      "payment_method_type": "card",
      "payment_method_type_display": "Cartão de Crédito",
      "gateway": "asaas",
      "gateway_payment_id": "pay_123456",
      "failure_reason": null,
      "retry_count": 0,
      "max_retries": 3,
      "metadata": {},
      "created_at": "2025-01-05T10:30:00Z",
      "updated_at": "2025-01-05T10:30:00Z"
    }
  ]
}
```

---

### `GET /api/billing/payments/{id}/`

Detalhes de um pagamento específico.

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `id` (integer): ID do pagamento

**Response 200**: Pagamento completo (mesmo formato do item da listagem)

---

## Endpoints de Métodos de Pagamento

### `GET /api/billing/payment-methods/`

Lista todos os métodos de pagamento do tenant do usuário autenticado.

**Headers**: `Authorization: Bearer <access_token>`

**Response 200**:
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "type": "card",
      "gateway": "asaas",
      "is_default": true,
      "is_active": true,
      "card_last4": "4242",
      "card_brand": "visa",
      "card_exp_month": 12,
      "card_exp_year": 2025,
      "card_display": "Visa •••• 4242",
      "billing_details": {
        "name": "João Silva",
        "email": "joao@example.com"
      },
      "created_at": "2025-01-01T10:00:00Z",
      "updated_at": "2025-01-01T10:00:00Z"
    }
  ]
}
```

**Notas**:
- Métodos padrão aparecem primeiro
- Apenas métodos ativos são retornados

---

### `POST /api/billing/payment-methods/`

Adiciona um novo método de pagamento.

**Headers**: `Authorization: Bearer <access_token>`

**Request Body**:
```json
{
  "type": "card",
  "token": "tok_xxx",
  "is_default": true,
  "billing_details": {
    "name": "João Silva",
    "email": "joao@example.com"
  }
}
```

**Campos**:
- `type` (string, obrigatório): "card", "boleto" ou "pix"
- `token` (string, obrigatório): Token do gateway (obtido no frontend)
- `is_default` (boolean, opcional): Se é o método padrão (padrão: false)
- `billing_details` (object, opcional): Detalhes de cobrança

**Response 201**: Método de pagamento criado

**Response 400**: Erro de validação
```json
{
  "detail": "Token inválido"
}
```

**Notas**:
- Token deve ser obtido no frontend via SDK do gateway
- Se `is_default=true`, outros métodos são desmarcados como padrão

---

### `DELETE /api/billing/payment-methods/{id}/`

Remove um método de pagamento.

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `id` (integer): ID do método de pagamento

**Response 204**: Método removido

**Response 400**: Não é possível remover método padrão se for o único

---

### `PATCH /api/billing/payment-methods/{id}/set-default/`

Define um método de pagamento como padrão.

**Headers**: `Authorization: Bearer <access_token>`

**Path Parameters**:
- `id` (integer): ID do método de pagamento

**Response 200**: Método atualizado (agora é padrão)

---

## Webhooks

### `POST /api/billing/webhooks/asaas/`

Endpoint para receber webhooks do Asaas.

**Headers**:
- `asaas-access-token`: Token de validação do webhook

**Request Body**: Payload do Asaas (formato específico do Asaas)

**Response 200**: Webhook processado

**Notas**:
- Webhook deve ser configurado no dashboard do Asaas
- URL: `https://api.structurone.com/api/billing/webhooks/asaas/`
- Validação de assinatura é obrigatória

---

### `POST /api/billing/webhooks/stripe/`

Endpoint para receber webhooks do Stripe.

**Headers**:
- `stripe-signature`: Assinatura do webhook (validação)

**Request Body**: Payload do Stripe (formato específico do Stripe)

**Response 200**: Webhook processado

**Notas**:
- Webhook deve ser configurado no dashboard do Stripe
- URL: `https://api.structurone.com/api/billing/webhooks/stripe/`
- Validação de assinatura é obrigatória

---

## Códigos de Status HTTP

- `200 OK`: Requisição bem-sucedida
- `201 Created`: Recurso criado com sucesso
- `204 No Content`: Recurso removido com sucesso
- `400 Bad Request`: Erro de validação ou requisição inválida
- `401 Unauthorized`: Token ausente ou inválido
- `403 Forbidden`: Sem permissão para acessar o recurso
- `404 Not Found`: Recurso não encontrado
- `429 Too Many Requests`: Rate limit excedido
- `500 Internal Server Error`: Erro interno do servidor

---

## Tratamento de Erros

### Formato Padrão de Erro

```json
{
  "detail": "Mensagem de erro descritiva"
}
```

### Erros Comuns

#### Assinatura Duplicada
```json
{
  "detail": "Tenant já possui uma assinatura ativa"
}
```

#### Plano Não Ativo
```json
{
  "detail": "Plano não está ativo"
}
```

#### Preço Não Configurado
```json
{
  "detail": "Plano não possui preço configurado para o país BR"
}
```

#### Método de Pagamento Inválido
```json
{
  "detail": "Token inválido"
}
```

---

## Segurança e Tokens

### Autenticação
- Todos os endpoints requerem token JWT válido
- Token deve estar no header `Authorization: Bearer <token>`
- Token expira em 15 minutos (renovar via `/api/auth/refresh/`)

### Permissões
- Usuário só pode acessar dados do seu próprio tenant
- Admin pode acessar todos os dados (via Django Admin)

### Dados Sensíveis
- Dados de cartão nunca são armazenados
- Apenas tokens do gateway são armazenados
- Últimos 4 dígitos apenas para exibição

---

## Exemplos Práticos

### Exemplo: Criar Assinatura Completa

```bash
# 1. Listar planos
curl -X GET http://localhost:8010/api/billing/plans/ \
  -H "Authorization: Bearer <token>"

# 2. Adicionar método de pagamento
curl -X POST http://localhost:8010/api/billing/payment-methods/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "card",
    "token": "tok_xxx",
    "is_default": true
  }'

# 3. Criar assinatura
curl -X POST http://localhost:8010/api/billing/subscriptions/create/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": 2,
    "payment_method_id": 1,
    "billing_cycle": "monthly"
  }'
```

### Exemplo: Fazer Upgrade

```bash
curl -X PATCH http://localhost:8010/api/billing/subscriptions/1/upgrade/ \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": 3
  }'
```

### Exemplo: Listar Faturas com Filtro

```bash
curl -X GET "http://localhost:8010/api/billing/invoices/?status=paid&page=1" \
  -H "Authorization: Bearer <token>"
```

---

## Notas Importantes

1. **País do Tenant**: O país do tenant determina:
   - Moeda exibida (BRL para BR, USD para US)
   - Gateway usado (Asaas para BR, Stripe para US)
   - Métodos de pagamento disponíveis

2. **Renovação Automática**: Faturas são geradas automaticamente no início de cada ciclo

3. **Trial**: Planos com `trial_days > 0` entram em trial ao criar assinatura

4. **Upgrade vs Downgrade**:
   - Upgrade: Aplica imediatamente, cobra prorata
   - Downgrade: Aplica no próximo ciclo

5. **Cancelamento**: Não é imediato, acesso continua até fim do período

