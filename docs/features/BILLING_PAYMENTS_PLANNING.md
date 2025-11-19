# 💳 Planejamento - Sistema de Faturas e Pagamentos

**Data**: 2025-01-16  
**Módulo**: Billing e Pagamentos  
**Status**: 🟢 Planejamento

---

## 📋 1. Planejamento

### O que a feature resolve

Permitir que construtoras e incorporadoras:
- Escolham e contratem planos de assinatura
- Gerenciem métodos de pagamento (cartão de crédito)
- Visualizem e baixem faturas
- Renovem assinaturas automaticamente
- Gerenciem upgrades/downgrades de planos

### Requisitos Funcionais

#### RF-001: Gestão de Planos
- Criar/editar planos no admin
- Definir limites por plano (projetos, usuários, etc.)
- Preços e períodos (mensal/anual)
- Ativar/desativar planos

#### RF-002: Assinaturas
- Criar assinatura ao escolher plano
- Renovação automática
- Upgrade/downgrade de plano
- Cancelamento de assinatura
- Período de trial (opcional)

#### RF-003: Métodos de Pagamento
- Adicionar cartão de crédito
- Salvar cartão de forma segura (tokenização)
- Gerenciar múltiplos cartões
- Definir cartão padrão
- Remover cartão

#### RF-004: Faturas
- Gerar fatura automaticamente
- Enviar fatura por email
- Visualizar histórico de faturas
- Download de PDF da fatura
- Status: pendente, paga, vencida, cancelada

#### RF-005: Webhooks
- Receber notificações do gateway
- Atualizar status de pagamento
- Processar renovações
- Tratar falhas de pagamento

### Requisitos Não Funcionais

- **Segurança**: PCI-DSS compliance (não armazenar dados de cartão)
- **Performance**: Processamento assíncrono de webhooks
- **Confiabilidade**: Retry automático em falhas
- **Auditoria**: Log de todas as transações
- **Multi-moeda**: Suporte a BRL, USD, EUR

---

## 🎯 2. Design da Solução

### Arquitetura de Pagamentos

**Recomendação: Integração com Gateway**

✅ **Vantagens da Integração:**
- Controle total sobre o fluxo
- Melhor UX (checkout no próprio site)
- Dados centralizados
- Facilita upgrades/downgrades
- Webhooks para automação

❌ **Desvantagens do Site Externo:**
- Experiência fragmentada
- Dificulta integração com sistema
- Menos controle sobre o processo

### Gateway Recomendado

**Para Brasil: Asaas ou Stripe**

**Asaas** (Recomendado para Brasil):
- ✅ Melhor para empresas brasileiras
- ✅ Suporte a boleto bancário
- ✅ PIX integrado
- ✅ Taxas competitivas
- ✅ API robusta
- ✅ Dashboard completo

**Stripe** (Alternativa):
- ✅ Internacional (multi-moeda)
- ✅ Excelente documentação
- ✅ Suporte a múltiplos países
- ⚠️ Taxas mais altas no Brasil

**Decisão**: **Asaas** (principal) + **Stripe** (backup/internacional)

---

## 📊 3. Estrutura de Planos Sugerida

### Plano Gratuito (Free)
- **Preço**: R$ 0,00/mês
- **Projetos**: 1 projeto
- **Usuários**: 1 usuário
- **Armazenamento**: 100 MB
- **Suporte**: Email
- **Ideal para**: Teste e avaliação

### Plano Básico (Basic)
- **Preço**: R$ 297,00/mês ou R$ 2.970,00/ano (2 meses grátis)
- **Projetos**: 5 projetos
- **Usuários**: 5 usuários
- **Armazenamento**: 5 GB
- **Suporte**: Email + Chat
- **Recursos**: Relatórios básicos
- **Ideal para**: Pequenas construtoras

### Plano Profissional (Professional)
- **Preço**: R$ 797,00/mês ou R$ 7.970,00/ano (2 meses grátis)
- **Projetos**: 20 projetos
- **Usuários**: 20 usuários
- **Armazenamento**: 50 GB
- **Suporte**: Email + Chat + Telefone
- **Recursos**: Relatórios avançados, API, Integrações
- **Ideal para**: Médias construtoras

### Plano Enterprise (Enterprise)
- **Preço**: Personalizado (sob consulta)
- **Projetos**: Ilimitados
- **Usuários**: Ilimitados
- **Armazenamento**: Ilimitado
- **Suporte**: Dedicado 24/7
- **Recursos**: Tudo + White-label, SLA, Treinamento
- **Ideal para**: Grandes construtoras/incorporadoras

---

## 🏗️ 4. Modelos de Dados

### Plan (Plano)
```python
- id
- name (ex: "Básico")
- slug (ex: "basic")
- description
- price_monthly (Decimal)
- price_yearly (Decimal)
- max_projects (Integer)
- max_users (Integer)
- max_storage_gb (Integer)
- features (JSONField) # Lista de features
- is_active (Boolean)
- is_featured (Boolean)
- trial_days (Integer, default=0)
- created_at, updated_at
```

### Subscription (Assinatura)
```python
- id
- tenant (ForeignKey -> Tenant)
- plan (ForeignKey -> Plan)
- status (choices: active, canceled, past_due, trialing)
- current_period_start (Date)
- current_period_end (Date)
- cancel_at_period_end (Boolean)
- canceled_at (DateTime, null=True)
- trial_start (Date, null=True)
- trial_end (Date, null=True)
- payment_method_id (String) # ID do método no gateway
- gateway_subscription_id (String) # ID no gateway
- created_at, updated_at
```

### Invoice (Fatura)
```python
- id
- tenant (ForeignKey -> Tenant)
- subscription (ForeignKey -> Subscription)
- invoice_number (String, unique)
- amount (Decimal)
- currency (String, default='BRL')
- status (choices: draft, open, paid, void, uncollectible)
- due_date (Date)
- paid_at (DateTime, null=True)
- gateway_invoice_id (String)
- pdf_url (URL, null=True)
- line_items (JSONField) # Detalhes da fatura
- created_at, updated_at
```

### Payment (Pagamento)
```python
- id
- invoice (ForeignKey -> Invoice)
- tenant (ForeignKey -> Tenant)
- amount (Decimal)
- currency (String)
- status (choices: pending, processing, succeeded, failed, refunded)
- payment_method (String) # card, boleto, pix
- gateway_payment_id (String)
- gateway_charge_id (String)
- failure_reason (String, null=True)
- metadata (JSONField)
- created_at, updated_at
```

### PaymentMethod (Método de Pagamento)
```python
- id
- tenant (ForeignKey -> Tenant)
- type (choices: card, boleto, pix)
- gateway_payment_method_id (String)
- is_default (Boolean)
- card_last4 (String, null=True) # Últimos 4 dígitos
- card_brand (String, null=True) # visa, mastercard, etc
- card_exp_month (Integer, null=True)
- card_exp_year (Integer, null=True)
- billing_details (JSONField) # Nome, email, endereço
- created_at, updated_at
```

---

## 🔄 5. Fluxos

### Fluxo de Assinatura
```
1. Usuário escolhe plano no frontend
2. Redireciona para checkout
3. Adiciona método de pagamento (cartão)
4. Cria assinatura no gateway
5. Cria Subscription no backend
6. Atualiza Tenant com plano
7. Envia email de confirmação
```

### Fluxo de Renovação
```
1. Gateway envia webhook (próximo ciclo)
2. Gera nova Invoice
3. Tenta cobrar método padrão
4. Se sucesso: marca como paga, renova Subscription
5. Se falha: marca como past_due, notifica usuário
6. Após X dias sem pagamento: suspende tenant
```

### Fluxo de Upgrade/Downgrade
```
1. Usuário escolhe novo plano
2. Calcula prorata
3. Cria Invoice de ajuste
4. Atualiza Subscription
5. Aplica novo plano imediatamente
6. Próxima fatura com novo valor
```

---

## 🔌 6. Integração com Gateway

### Asaas (Recomendado)
- **Documentação**: https://docs.asaas.com
- **SDK Python**: `asaas-python-sdk` ou requests direto
- **Webhooks**: Configurar URL de callback
- **Recursos**: Cartão, Boleto, PIX, Split de pagamento

### Stripe (Alternativa)
- **Documentação**: https://stripe.com/docs
- **SDK Python**: `stripe`
- **Webhooks**: Configurar no dashboard
- **Recursos**: Cartão, múltiplas moedas, Subscriptions

---

## 📁 7. Estrutura de Arquivos

```
backend/apps/billing/
├── __init__.py
├── models.py          # Plan, Subscription, Invoice, Payment, PaymentMethod
├── serializers.py
├── views.py           # ViewSets para CRUD
├── services.py        # Lógica de negócio
├── gateway/           # Integrações com gateways
│   ├── __init__.py
│   ├── asaas.py
│   ├── stripe.py
│   └── base.py        # Interface base
├── webhooks.py        # Handlers de webhooks
├── urls.py
└── tests/

admin/src/app/
├── billing/
│   ├── plans/
│   │   ├── page.tsx      # Lista de planos
│   │   ├── new/page.tsx  # Criar plano
│   │   └── [id]/page.tsx # Editar plano
│   ├── subscriptions/
│   │   └── page.tsx      # Assinaturas dos tenants
│   └── invoices/
│       └── page.tsx      # Faturas

frontend/src/app/
├── pricing/
│   └── page.tsx          # Página de planos
├── checkout/
│   └── page.tsx          # Checkout
└── account/
    ├── subscription/
    │   └── page.tsx      # Minha assinatura
    └── invoices/
        └── page.tsx      # Minhas faturas
```

---

## ✅ 8. Checklist de Implementação

### Backend
- [ ] Criar app `billing`
- [ ] Models: Plan, Subscription, Invoice, Payment, PaymentMethod
- [ ] Migrations
- [ ] Serializers
- [ ] Services (lógica de negócio)
- [ ] Gateway integration (Asaas)
- [ ] Webhooks handlers
- [ ] ViewSets/Views
- [ ] URLs
- [ ] Testes unitários
- [ ] Testes de integração

### Admin Panel
- [ ] CRUD de Planos
- [ ] Visualização de assinaturas
- [ ] Visualização de faturas
- [ ] Gerenciar métodos de pagamento
- [ ] Cancelar/reativar assinaturas

### Frontend
- [ ] Página de planos (pricing)
- [ ] Checkout
- [ ] Área de assinatura
- [ ] Histórico de faturas
- [ ] Gerenciar cartão

---

## 🚀 Próximos Passos

1. ✅ Planejamento (este documento)
2. ⏭️ Design detalhado (diagramas)
3. ⏭️ Implementação Backend
4. ⏭️ Implementação Admin
5. ⏭️ Implementação Frontend
6. ⏭️ Testes
7. ⏭️ Deploy

