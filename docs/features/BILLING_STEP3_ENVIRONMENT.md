# 🟢 Passo 3: Criar Ambiente + Setup Inicial - Sistema de Billing

**Data**: 2025-01-16  
**Status**: 🟢 Em Andamento

---

## ✅ Tarefas Concluídas

### 1. App Billing Criado
- [x] Estrutura de diretórios criada
- [x] `apps.py` configurado
- [x] `__init__.py` criado

### 2. Models Criados
- [x] `Plan` - Modelo de plano de assinatura
- [x] `Subscription` - Modelo de assinatura do tenant
- [x] `Invoice` - Modelo de fatura
- [x] `Payment` - Modelo de pagamento
- [x] `PaymentMethod` - Modelo de método de pagamento

### 3. Configuração Django
- [x] App adicionado ao `INSTALLED_APPS`

---

## ⏭️ Próximas Tarefas

### 4. Migrations
- [ ] Criar migration inicial
- [ ] Aplicar migrations

### 5. Variáveis de Ambiente
- [ ] Adicionar variáveis para Asaas
- [ ] Adicionar variáveis para Stripe
- [ ] Documentar variáveis necessárias

### 6. Admin Django
- [ ] Registrar models no admin
- [ ] Configurar list_display, list_filter, search_fields

### 7. Estrutura de Gateway
- [ ] Criar diretório `gateway/`
- [ ] Criar `base.py` (interface base)
- [ ] Criar `asaas.py` (implementação Asaas)
- [ ] Criar `stripe.py` (implementação Stripe)

---

## 📝 Variáveis de Ambiente Necessárias

### Asaas (Brasil)
```env
ASAAS_API_KEY=your_asaas_api_key
ASAAS_ENVIRONMENT=sandbox  # ou production
ASAAS_WEBHOOK_TOKEN=your_webhook_token
```

### Stripe (USA/Internacional)
```env
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
STRIPE_ENVIRONMENT=test  # ou live
```

---

## 🏗️ Estrutura de Arquivos Criada

```
backend/apps/billing/
├── __init__.py
├── apps.py
├── models.py          ✅ Criado
├── admin.py           ⏭️ Próximo
├── serializers.py     ⏭️ Passo 4
├── services.py        ⏭️ Passo 4
├── views.py           ⏭️ Passo 4
├── urls.py            ⏭️ Passo 4
├── gateway/           ⏭️ Próximo
│   ├── __init__.py
│   ├── base.py
│   ├── asaas.py
│   └── stripe.py
├── webhooks.py        ⏭️ Passo 4
└── migrations/        ⏭️ Próximo
    └── __init__.py
```

---

## 🎯 Status Atual

**Progresso**: 3/13 passos (23%)

**Próxima ação**: Criar migrations e configurar variáveis de ambiente

