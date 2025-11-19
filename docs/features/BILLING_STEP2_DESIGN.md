# 🟣 Passo 2: Design da Solução - Sistema de Billing e Pagamentos

**Data**: 2025-01-16  
**Módulo**: Billing e Pagamentos  
**Status**: 🟢 Em Andamento

---

## 📊 1. Modelos de Dados Detalhados

### Plan (Plano)
```python
class Plan(TimeStampedModel):
    """
    Modelo de plano de assinatura
    O preço é determinado pelo país de registro da empresa (tenant.country)
    Uma empresa brasileira paga em BRL via Asaas, mesmo que construa nos EUA
    Uma empresa americana paga em USD via Stripe, mesmo que construa no Brasil
    """
    name = models.CharField(max_length=100)  # "Básico", "Profissional", "Starter"
    slug = models.SlugField(unique=True)      # "basic", "professional", "starter"
    description = models.TextField(blank=True)
    
    # Preços por moeda (baseado no país de registro do tenant)
    # Se tenant.country = 'BR' → usa price_monthly_brl
    # Se tenant.country = 'US' → usa price_monthly_usd
    price_monthly_brl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_yearly_brl = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_monthly_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    price_yearly_usd = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Moeda padrão (para exibição)
    currency = models.CharField(max_length=3, default='BRL')  # BRL, USD, EUR
    
    # Limites
    max_projects = models.IntegerField(default=1)
    max_users = models.IntegerField(default=1)
    max_storage_gb = models.IntegerField(default=1)
    
    # Features (JSON)
    features = models.JSONField(default=list)  # ["Relatórios", "API", "Suporte 24/7"]
    
    # Status
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)  # Destaque na página de planos
    
    # Trial
    trial_days = models.IntegerField(default=0)  # 0 = sem trial
    
    # Ordem de exibição
    display_order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['display_order', 'price_monthly']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active']),
        ]
```

### Subscription (Assinatura)
```python
class Subscription(TimeStampedModel):
    """
    Modelo de assinatura do tenant
    """
    tenant = models.OneToOneField(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='subscription'
    )
    plan = models.ForeignKey(
        'billing.Plan',
        on_delete=models.PROTECT,
        related_name='subscriptions'
    )
    
    # Status
    STATUS_CHOICES = [
        ('trialing', 'Em Trial'),
        ('active', 'Ativa'),
        ('past_due', 'Pagamento Atrasado'),
        ('canceled', 'Cancelada'),
        ('unpaid', 'Não Paga'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='trialing')
    
    # Período
    current_period_start = models.DateField()
    current_period_end = models.DateField()
    
    # Trial
    trial_start = models.DateField(null=True, blank=True)
    trial_end = models.DateField(null=True, blank=True)
    
    # Cancelamento
    cancel_at_period_end = models.BooleanField(default=False)
    canceled_at = models.DateTimeField(null=True, blank=True)
    cancellation_reason = models.TextField(blank=True)
    
    # Gateway
    gateway = models.CharField(max_length=20, default='asaas')  # asaas, stripe
    gateway_subscription_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    gateway_customer_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Método de pagamento
    payment_method = models.ForeignKey(
        'billing.PaymentMethod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='subscriptions'
    )
    
    class Meta:
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['current_period_end']),
        ]
```

### Invoice (Fatura)
```python
class Invoice(TimeStampedModel):
    """
    Modelo de fatura
    """
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='invoices'
    )
    subscription = models.ForeignKey(
        'billing.Subscription',
        on_delete=models.CASCADE,
        related_name='invoices',
        null=True,
        blank=True
    )
    
    # Número único
    invoice_number = models.CharField(max_length=50, unique=True)  # INV-2025-0001
    
    # Valores
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='BRL')
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    
    # Status
    STATUS_CHOICES = [
        ('draft', 'Rascunho'),
        ('open', 'Aberta'),
        ('paid', 'Paga'),
        ('void', 'Cancelada'),
        ('uncollectible', 'Inadimplente'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    
    # Datas
    issue_date = models.DateField()
    due_date = models.DateField()
    paid_at = models.DateTimeField(null=True, blank=True)
    
    # Gateway
    gateway_invoice_id = models.CharField(max_length=255, null=True, blank=True)
    gateway_pdf_url = models.URLField(null=True, blank=True)
    
    # Detalhes
    line_items = models.JSONField(default=list)  # [{description, amount, quantity}]
    notes = models.TextField(blank=True)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['due_date']),
            models.Index(fields=['invoice_number']),
        ]
```

### Payment (Pagamento)
```python
class Payment(TimeStampedModel):
    """
    Modelo de pagamento
    """
    invoice = models.ForeignKey(
        'billing.Invoice',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='payments'
    )
    payment_method = models.ForeignKey(
        'billing.PaymentMethod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )
    
    # Valores
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3, default='BRL')
    
    # Status
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('processing', 'Processando'),
        ('succeeded', 'Sucesso'),
        ('failed', 'Falhou'),
        ('refunded', 'Reembolsado'),
        ('canceled', 'Cancelado'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Método
    METHOD_CHOICES = [
        ('card', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
        ('pix', 'PIX'),
        ('bank_transfer', 'Transferência Bancária'),
    ]
    payment_method_type = models.CharField(max_length=20, choices=METHOD_CHOICES)
    
    # Gateway
    gateway = models.CharField(max_length=20, default='asaas')
    gateway_payment_id = models.CharField(max_length=255, unique=True, null=True, blank=True)
    gateway_charge_id = models.CharField(max_length=255, null=True, blank=True)
    
    # Falhas
    failure_reason = models.TextField(null=True, blank=True)
    retry_count = models.IntegerField(default=0)
    max_retries = models.IntegerField(default=3)
    
    # Metadata
    metadata = models.JSONField(default=dict)
    
    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['invoice']),
            models.Index(fields=['tenant']),
            models.Index(fields=['status']),
            models.Index(fields=['gateway_payment_id']),
        ]
```

### PaymentMethod (Método de Pagamento)
```python
class PaymentMethod(TimeStampedModel):
    """
    Modelo de método de pagamento (cartão, etc.)
    """
    tenant = models.ForeignKey(
        'tenants.Tenant',
        on_delete=models.CASCADE,
        related_name='payment_methods'
    )
    
    # Tipo
    TYPE_CHOICES = [
        ('card', 'Cartão de Crédito'),
        ('boleto', 'Boleto Bancário'),
        ('pix', 'PIX'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='card')
    
    # Gateway
    gateway = models.CharField(max_length=20, default='asaas')
    gateway_payment_method_id = models.CharField(max_length=255, unique=True)
    
    # Status
    is_default = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    
    # Dados do cartão (apenas para exibição)
    card_last4 = models.CharField(max_length=4, null=True, blank=True)
    card_brand = models.CharField(max_length=20, null=True, blank=True)  # visa, mastercard
    card_exp_month = models.IntegerField(null=True, blank=True)
    card_exp_year = models.IntegerField(null=True, blank=True)
    
    # Billing details
    billing_details = models.JSONField(default=dict)  # {name, email, address}
    
    class Meta:
        ordering = ['-is_default', '-created_at']
        indexes = [
            models.Index(fields=['tenant']),
            models.Index(fields=['is_default']),
        ]
```

---

## 🔌 2. API Endpoints

### Planos

#### `GET /api/billing/plans/`
Lista todos os planos ativos
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
      "price_monthly": "297.00",
      "price_yearly": "2970.00",
      "currency": "BRL",
      "max_projects": 5,
      "max_users": 5,
      "max_storage_gb": 5,
      "features": ["Relatórios básicos", "Suporte por email"],
      "trial_days": 14,
      "is_featured": false
    }
  ]
}
```

#### `GET /api/billing/plans/{id}/`
Detalhes de um plano
**Response 200**: Objeto de plano completo

### Assinaturas

#### `GET /api/billing/subscriptions/me/`
Minha assinatura atual (tenant autenticado)
**Response 200**:
```json
{
  "id": 1,
  "plan": {
    "id": 2,
    "name": "Profissional",
    "slug": "professional"
  },
  "status": "active",
  "current_period_start": "2025-01-01",
  "current_period_end": "2025-02-01",
  "trial_end": null,
  "cancel_at_period_end": false
}
```

#### `POST /api/billing/subscriptions/`
Criar nova assinatura
**Request Body**:
```json
{
  "plan_id": 2,
  "payment_method_id": 1,
  "billing_cycle": "monthly"  // ou "yearly"
}
```
**Response 201**: Assinatura criada

#### `PATCH /api/billing/subscriptions/{id}/upgrade/`
Fazer upgrade de plano
**Request Body**:
```json
{
  "plan_id": 3
}
```
**Response 200**: Assinatura atualizada

#### `PATCH /api/billing/subscriptions/{id}/cancel/`
Cancelar assinatura
**Request Body**:
```json
{
  "reason": "Não estou mais usando o sistema"
}
```
**Response 200**: Assinatura cancelada

### Métodos de Pagamento

#### `GET /api/billing/payment-methods/`
Lista métodos de pagamento do tenant
**Response 200**:
```json
{
  "count": 2,
  "results": [
    {
      "id": 1,
      "type": "card",
      "card_last4": "4242",
      "card_brand": "visa",
      "card_exp_month": 12,
      "card_exp_year": 2025,
      "is_default": true,
      "is_active": true
    }
  ]
}
```

#### `POST /api/billing/payment-methods/`
Adicionar método de pagamento
**Request Body**:
```json
{
  "type": "card",
  "token": "tok_xxx",  // Token do gateway (frontend obtém)
  "is_default": true
}
```
**Response 201**: Método criado

#### `DELETE /api/billing/payment-methods/{id}/`
Remover método de pagamento
**Response 204**: Removido

#### `PATCH /api/billing/payment-methods/{id}/set-default/`
Definir como padrão
**Response 200**: Atualizado

### Faturas

#### `GET /api/billing/invoices/`
Lista faturas do tenant
**Query Params**: `status`, `page`, `page_size`
**Response 200**:
```json
{
  "count": 10,
  "results": [
    {
      "id": 1,
      "invoice_number": "INV-2025-0001",
      "amount": "297.00",
      "currency": "BRL",
      "status": "paid",
      "issue_date": "2025-01-01",
      "due_date": "2025-01-10",
      "paid_at": "2025-01-05T10:30:00Z",
      "gateway_pdf_url": "https://..."
    }
  ]
}
```

#### `GET /api/billing/invoices/{id}/`
Detalhes de uma fatura
**Response 200**: Fatura completa com line_items

#### `GET /api/billing/invoices/{id}/pdf/`
Download do PDF da fatura
**Response 200**: Arquivo PDF

### Webhooks

#### `POST /api/billing/webhooks/asaas/`
Webhook do Asaas
**Headers**: `asaas-access-token` (validação)
**Request Body**: Payload do Asaas
**Response 200**: Processado

#### `POST /api/billing/webhooks/stripe/`
Webhook do Stripe
**Headers**: `stripe-signature` (validação)
**Request Body**: Payload do Stripe
**Response 200**: Processado

---

## 🔄 3. Fluxos de Estado

### Fluxo de Assinatura
```
[Usuário escolhe plano]
    ↓
[Frontend: POST /api/billing/subscriptions/]
    ↓
[Backend: Valida plano e tenant]
    ↓
[Backend: Cria PaymentMethod no gateway]
    ↓
[Backend: Cria Subscription no gateway]
    ↓
[Backend: Cria Subscription no banco]
    ↓
[Backend: Atualiza Tenant com novo plano]
    ↓
[Backend: Gera primeira Invoice]
    ↓
[Backend: Processa pagamento]
    ↓
[Webhook: Confirma pagamento]
    ↓
[Backend: Atualiza status para 'active']
    ↓
[Email: Confirmação de assinatura]
```

### Fluxo de Renovação Automática
```
[Cron Job: Verifica assinaturas próximas do vencimento]
    ↓
[Backend: Identifica Subscription com current_period_end = hoje]
    ↓
[Backend: Gera nova Invoice]
    ↓
[Backend: Tenta processar pagamento com método padrão]
    ↓
    ├─ [Sucesso] → [Atualiza Invoice para 'paid']
    │                [Renova Subscription (novo período)]
    │                [Email: Fatura paga]
    │
    └─ [Falha] → [Marca Invoice como 'open']
                  [Marca Subscription como 'past_due']
                  [Email: Falha no pagamento]
                  [Retry após 3 dias]
                  [Após 7 dias: Suspende tenant]
```

### Fluxo de Upgrade
```
[Usuário escolhe novo plano]
    ↓
[Frontend: PATCH /api/billing/subscriptions/{id}/upgrade/]
    ↓
[Backend: Calcula prorata]
    ↓
[Backend: Cria Invoice de ajuste]
    ↓
[Backend: Atualiza Subscription com novo plano]
    ↓
[Backend: Atualiza Tenant com novos limites]
    ↓
[Backend: Processa pagamento do prorata]
    ↓
[Email: Upgrade confirmado]
```

### Fluxo de Webhook (Asaas)
```
[Asaas: Evento de pagamento]
    ↓
[POST /api/billing/webhooks/asaas/]
    ↓
[Backend: Valida assinatura do webhook]
    ↓
[Backend: Identifica tipo de evento]
    ↓
    ├─ [PAYMENT_CONFIRMED] → [Atualiza Payment para 'succeeded']
    │                         [Atualiza Invoice para 'paid']
    │                         [Renova Subscription se necessário]
    │
    ├─ [PAYMENT_REFUSED] → [Atualiza Payment para 'failed']
    │                      [Atualiza Invoice para 'open']
    │                      [Marca Subscription como 'past_due']
    │
    └─ [SUBSCRIPTION_CANCELED] → [Atualiza Subscription para 'canceled']
```

---

## 🏗️ 4. Diagrama de Classes

```
┌─────────────┐
│    Tenant   │
└──────┬──────┘
       │ 1
       │
       │ 1
┌──────▼──────────┐
│  Subscription   │
└──────┬──────────┘
       │
       │ N
       │
┌──────▼──────┐      ┌──────────────┐
│   Invoice   │──────│    Plan      │
└──────┬──────┘      └──────────────┘
       │
       │ N
       │
┌──────▼──────┐
│  Payment    │
└──────┬──────┘
       │
       │ N
       │
┌──────▼──────────────┐
│  PaymentMethod      │
└─────────────────────┘
```

---

## 🔐 5. Regras de Segurança e Permissões

### Permissões

#### Planos
- **Listar**: Qualquer usuário autenticado
- **Criar/Editar/Deletar**: Apenas superusuário/admin

#### Assinaturas
- **Ver própria**: Tenant autenticado
- **Criar**: Tenant autenticado (sem assinatura ativa)
- **Upgrade/Cancelar**: Tenant autenticado (dono da assinatura)
- **Ver todas**: Apenas admin

#### Faturas
- **Ver próprias**: Tenant autenticado
- **Ver todas**: Apenas admin
- **Download PDF**: Tenant autenticado (dono da fatura)

#### Métodos de Pagamento
- **Ver próprios**: Tenant autenticado
- **Adicionar/Remover**: Tenant autenticado
- **Ver todos**: Apenas admin

#### Webhooks
- **Receber**: Apenas gateway (validação por assinatura)
- **Ver logs**: Apenas admin

### Validações de Segurança

1. **PCI-DSS Compliance**
   - Nunca armazenar dados completos de cartão
   - Apenas tokens do gateway
   - Últimos 4 dígitos apenas para exibição

2. **Validação de Webhooks**
   - Verificar assinatura (Asaas: header `asaas-access-token`)
   - Verificar assinatura (Stripe: header `stripe-signature`)
   - Processar de forma idempotente

3. **Rate Limiting**
   - Webhooks: 1000/hora
   - Criação de assinatura: 10/hora por tenant
   - Adição de método de pagamento: 5/hora por tenant

4. **Auditoria**
   - Log de todas as transações
   - Log de tentativas de pagamento
   - Log de webhooks recebidos

---

## 📦 6. Estrutura de Serviços

### BillingService
```python
class BillingService:
    - create_subscription(tenant, plan_id, payment_method_id, billing_cycle)
    - upgrade_subscription(subscription, new_plan_id)
    - cancel_subscription(subscription, reason)
    - renew_subscription(subscription)
    - calculate_prorata(old_plan, new_plan, days_used)
```

### InvoiceService
```python
class InvoiceService:
    - generate_invoice(subscription, period_start, period_end)
    - generate_invoice_number()
    - generate_pdf(invoice)
    - send_invoice_email(invoice)
```

### PaymentService
```python
class PaymentService:
    - process_payment(invoice, payment_method)
    - retry_payment(payment)
    - refund_payment(payment, amount)
```

### GatewayService (Interface)
```python
class GatewayService:
    - create_customer(tenant)
    - create_payment_method(token)
    - create_subscription(customer_id, plan_id, payment_method_id)
    - process_payment(amount, payment_method_id)
    - cancel_subscription(subscription_id)
    - handle_webhook(payload, signature)
```

### AsaasGatewayService (Implementação)
```python
class AsaasGatewayService(GatewayService):
    - Implementa todos os métodos usando API do Asaas
```

### StripeGatewayService (Implementação)
```python
class StripeGatewayService(GatewayService):
    - Implementa todos os métodos usando API do Stripe
```

---

## 🎯 Próximo Passo

**Passo 3: Criar Ambiente + Setup Inicial**
- Configurar app `billing` no Django
- Criar migrations
- Configurar variáveis de ambiente
- Setup de gateway (Asaas/Stripe)

