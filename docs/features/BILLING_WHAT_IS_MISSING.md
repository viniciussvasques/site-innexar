# 🔍 O que Falta - Sistema de Billing

**Data**: 2025-11-17  
**Status**: Análise de Pendências

---

## ✅ O que JÁ ESTÁ PRONTO

### Implementado e Funcionando
- ✅ Models (Plan, Subscription, Invoice, Payment, PaymentMethod)
- ✅ Serializers completos
- ✅ Services básicos (BillingService, InvoiceService, PaymentService)
- ✅ ViewSets e endpoints da API
- ✅ Gateway base (Asaas e Stripe - estrutura)
- ✅ Testes unitários (36 testes - 100% passando)
- ✅ Testes de integração (18 testes - 100% passando)
- ✅ Testes manuais (11 testes - 100% passando)
- ✅ Documentação da API
- ✅ Admin Django configurado

---

## ⚠️ O que FALTA IMPLEMENTAR

### 1. 🔴 Integração Completa com Gateways

#### 1.1 Gateway Asaas - TODOs
**Arquivo**: `backend/apps/billing/gateway/asaas.py`

- [ ] **Linha 98**: `'value': 0,  # TODO: Obter do plano`
  - Implementar cálculo do valor do plano baseado no billing_cycle
  
- [ ] **Linha 99**: `'nextDueDate': '',  # TODO: Calcular data`
  - Implementar cálculo da próxima data de vencimento
  
- [ ] **Linha 124**: `'customer': '',  # TODO: Obter do tenant`
  - Implementar obtenção do customer_id do tenant
  
- [ ] **Linha 127**: `'dueDate': '',  # TODO: Calcular data`
  - Implementar cálculo da data de vencimento do pagamento

**Impacto**: Assinaturas não são criadas corretamente no Asaas

#### 1.2 Gateway Stripe - Verificar
- [ ] Verificar se todos os métodos estão implementados
- [ ] Testar integração real com Stripe (sandbox)

#### 1.3 PaymentService - Integração
**Arquivo**: `backend/apps/billing/services.py`

- [ ] **Linha 346**: `# TODO: Integrar com gateway para processar pagamento`
  - Implementar chamada real ao gateway
  - Processar resposta do gateway
  - Atualizar status do pagamento baseado na resposta

**Impacto**: Pagamentos não são processados realmente

---

### 2. 🟡 Funcionalidades de Negócio

#### 2.1 Cálculo de Impostos
**Arquivo**: `backend/apps/billing/services.py`

- [ ] **Linha 252**: `tax_amount=Decimal('0.00'),  # TODO: Calcular impostos`
  - Implementar cálculo de impostos baseado no país
  - Brasil: Calcular ICMS, PIS, COFINS se aplicável
  - USA: Calcular sales tax baseado no estado

**Impacto**: Faturas não incluem impostos

#### 2.2 Renovação Automática
**Arquivo**: Não existe ainda

- [ ] Criar comando Django `manage.py renew_subscriptions`
- [ ] Implementar lógica de renovação:
  - Verificar assinaturas com período expirando
  - Gerar nova fatura
  - Processar pagamento automaticamente
  - Atualizar período da assinatura
- [ ] Configurar cron job (Celery Beat ou sistema de cron)

**Impacto**: Assinaturas não são renovadas automaticamente

#### 2.3 Retry de Pagamentos Falhados
**Arquivo**: Não existe ainda

- [ ] Criar comando Django `manage.py retry_failed_payments`
- [ ] Implementar lógica:
  - Identificar pagamentos falhados há mais de 3 dias
  - Tentar processar novamente
  - Atualizar status
  - Suspender tenant após 7 dias sem pagamento
- [ ] Configurar cron job

**Impacto**: Pagamentos falhados não são retentados automaticamente

---

### 3. 🟢 Funcionalidades de Interface

#### 3.1 Download de PDF de Fatura
**Arquivo**: `backend/apps/billing/views.py` (linha 203)

- [ ] Endpoint `/api/billing/invoices/{id}/pdf/` existe mas precisa:
  - [ ] Gerar PDF real (usar reportlab ou weasyprint)
  - [ ] Template de fatura profissional
  - [ ] Incluir logo da empresa
  - [ ] Incluir todos os dados da fatura

**Impacto**: PDF não é gerado, apenas endpoint existe

#### 3.2 Email de Notificações
**Arquivo**: Não existe ainda

- [ ] Configurar Django Email Backend
- [ ] Criar templates de email:
  - [ ] Confirmação de assinatura
  - [ ] Nova fatura gerada
  - [ ] Pagamento confirmado
  - [ ] Pagamento falhado
  - [ ] Assinatura cancelada
  - [ ] Renovação automática
- [ ] Integrar envio de emails nos services

**Impacto**: Usuários não recebem notificações por email

---

### 4. 🔵 Webhooks Completos

#### 4.1 Handlers de Webhook
**Arquivo**: `backend/apps/billing/views.py` (não existe ainda)

- [ ] Criar endpoint `/api/billing/webhooks/asaas/`
  - [ ] Validar assinatura do webhook
  - [ ] Processar eventos:
    - [ ] `payment.created`
    - [ ] `payment.confirmed`
    - [ ] `payment.refused`
    - [ ] `subscription.created`
    - [ ] `subscription.cancelled`
  - [ ] Processar de forma idempotente
  - [ ] Log de todas as notificações

- [ ] Criar endpoint `/api/billing/webhooks/stripe/`
  - [ ] Validar assinatura do webhook
  - [ ] Processar eventos:
    - [ ] `payment_intent.succeeded`
    - [ ] `payment_intent.payment_failed`
    - [ ] `customer.subscription.created`
    - [ ] `customer.subscription.deleted`
  - [ ] Processar de forma idempotente
  - [ ] Log de todas as notificações

**Impacto**: Status não é atualizado automaticamente via webhooks

---

### 5. 🟣 Frontend (Interface do Usuário)

#### 5.1 Página de Planos
- [ ] Criar página `/pricing` ou `/billing/plans`
- [ ] Exibir planos disponíveis
- [ ] Mostrar preços na moeda correta
- [ ] Botão "Assinar" para cada plano

#### 5.2 Checkout
- [ ] Criar página de checkout
- [ ] Integrar SDK do gateway (Asaas/Stripe)
- [ ] Formulário de cartão de crédito
- [ ] Processar assinatura

#### 5.3 Área de Billing
- [ ] Página `/billing/subscription` - Minha assinatura
- [ ] Página `/billing/invoices` - Minhas faturas
- [ ] Página `/billing/payment-methods` - Métodos de pagamento
- [ ] Página `/billing/payments` - Histórico de pagamentos

#### 5.4 Funcionalidades
- [ ] Upgrade/Downgrade de plano (UI)
- [ ] Cancelar assinatura (UI)
- [ ] Adicionar método de pagamento (UI)
- [ ] Download de PDF de fatura (UI)
- [ ] Visualizar detalhes da fatura (UI)

**Impacto**: Usuários não podem gerenciar billing pelo frontend

---

### 6. ⚪ Passos do Processo (Sem Deploy)

#### 6.1 Passo 11: Teste UAT
- [ ] Criar cenários de teste UAT
- [ ] Executar testes com usuários reais
- [ ] Coletar feedback
- [ ] Documentar problemas encontrados

#### 6.2 Passo 13: Monitoramento e Feedback
- [ ] Configurar logs estruturados
- [ ] Configurar métricas (Prometheus/Grafana ou similar)
- [ ] Configurar alertas:
  - [ ] Falhas de pagamento
  - [ ] Webhooks não recebidos
  - [ ] Renovações falhadas
- [ ] Dashboard de métricas de billing
- [ ] Coletar feedback dos usuários

---

## 📊 Priorização

### 🔴 Crítico (Bloqueia uso em produção)
1. **Integração completa com gateways** (Asaas/Stripe)
2. **Processamento real de pagamentos**
3. **Renovação automática de assinaturas**

### 🟡 Importante (Melhora experiência)
4. **Cálculo de impostos**
5. **Retry de pagamentos falhados**
6. **Webhooks completos**
7. **Download de PDF de faturas**

### 🟢 Desejável (Nice to have)
8. **Emails de notificações**
9. **Frontend completo**
10. **Monitoramento e métricas**

---

## 🎯 Plano de Ação Sugerido

### Fase 1: Funcionalidades Críticas (1-2 semanas)
1. Completar integração com gateways
2. Implementar processamento real de pagamentos
3. Implementar renovação automática

### Fase 2: Funcionalidades Importantes (1 semana)
4. Implementar cálculo de impostos
5. Implementar retry de pagamentos
6. Implementar webhooks completos
7. Implementar geração de PDF

### Fase 3: Melhorias (1 semana)
8. Implementar emails
9. Criar frontend básico
10. Configurar monitoramento

---

## 📝 Notas

- O sistema **já funciona** para testes básicos
- A estrutura está **completa e bem arquitetada**
- Faltam principalmente **integrações reais** com gateways
- Frontend pode ser feito **paralelamente** ao backend

---

## ✅ Conclusão

**Status Atual**: Sistema funcional para desenvolvimento e testes, mas precisa de integrações reais para produção.

**Próximos Passos Recomendados**:
1. Completar integração com gateways (Asaas primeiro, depois Stripe)
2. Implementar renovação automática
3. Implementar processamento real de pagamentos
4. Criar frontend básico para usuários testarem

