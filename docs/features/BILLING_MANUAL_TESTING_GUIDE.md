# 🟤 Guia Completo de Testes Manuais - Sistema de Billing

**Data**: 2025-01-16  
**Status**: 🟢 Pronto para Execução

---

## 📊 Status dos 13 Passos

### ✅ Concluídos (9/13)
1. ✅ **Passo 1**: Planejamento completo
2. ✅ **Passo 2**: Design da solução
3. ✅ **Passo 3**: Criar ambiente + setup inicial
4. ✅ **Passo 4**: Implementação da feature
5. ✅ **Passo 5**: Testes unitários (36 testes)
6. ✅ **Passo 6**: Testes de integração (18 testes)
7. 🔄 **Passo 7**: Testes manuais (este guia)
8. ✅ **Passo 8**: Revisão de código
9. ✅ **Passo 9**: Documentação

### ⏭️ Pendentes (4/13)
10. **Passo 10**: Deploy para Staging
11. **Passo 11**: Teste UAT
12. **Passo 12**: Deploy para Produção
13. **Passo 13**: Monitoramento e Feedback

---

## 🎯 Objetivo dos Testes Manuais

Validar o sistema de billing como um usuário real, testando todos os fluxos principais e verificando se a experiência está correta.

---

## 🔧 Pré-requisitos

### Ambiente
- ✅ Backend rodando: `http://localhost:8010`
- ✅ Frontend rodando: `http://localhost:3007`
- ✅ Admin Panel rodando: `http://localhost:3011`
- ✅ Banco de dados com migrations aplicadas
- ✅ Docker containers rodando

### Credenciais de Teste
- **Admin Panel**: `admin@structurone.com` / `admin123`
- **Tenant BR**: Criar via registro ou admin
- **Tenant US**: Criar via registro ou admin

### Dados de Gateway (Sandbox)
- **Asaas**: Usar ambiente sandbox (configurar no `.env`)
- **Stripe**: Usar chaves de teste (configurar no `.env`)

---

## 📋 Checklist de Testes Manuais

### 1. Gestão de Planos (Admin Django)

#### 1.1 Criar Plano Básico (Brasil)
- [ ] Acessar `http://localhost:3011/admin/billing/plan/add/`
- [ ] Preencher:
  - Nome: `Básico`
  - Slug: `basic`
  - Descrição: `Ideal para pequenas construtoras`
  - Preço Mensal (BRL): `297.00`
  - Preço Anual (BRL): `2970.00`
  - Preço Mensal (USD): `49.00`
  - Preço Anual (USD): `490.00`
  - Máximo de Projetos: `5`
  - Máximo de Usuários: `5`
  - Máximo de Armazenamento (GB): `5`
  - Features: `["Relatórios básicos", "Suporte por email"]`
  - Trial (dias): `14`
  - Ativo: ✅
- [ ] Salvar
- [ ] Verificar se aparece na listagem
- [ ] Verificar se está disponível via API: `GET /api/billing/plans/`

#### 1.2 Criar Plano Profissional (Brasil)
- [ ] Criar plano "Profissional"
- [ ] Preço Mensal (BRL): `797.00`
- [ ] Preço Anual (BRL): `7970.00`
- [ ] Máximo de Projetos: `20`
- [ ] Máximo de Usuários: `20`
- [ ] Features: `["Relatórios avançados", "API", "Suporte prioritário"]`

#### 1.3 Criar Plano Starter (USA)
- [ ] Criar plano "Starter"
- [ ] Preço Mensal (USD): `49.00`
- [ ] Preço Anual (USD): `490.00`
- [ ] Máximo de Projetos: `5`
- [ ] Máximo de Usuários: `5`

#### 1.4 Editar Plano
- [ ] Editar plano existente
- [ ] Alterar preço
- [ ] Salvar
- [ ] Verificar se alteração foi aplicada na API

#### 1.5 Desativar Plano
- [ ] Desativar um plano
- [ ] Verificar se não aparece mais na API (apenas ativos)
- [ ] Verificar se assinaturas existentes continuam funcionando

---

### 2. Assinatura de Plano (Frontend)

#### 2.1 Visualizar Planos
- [ ] Fazer login no frontend (`http://localhost:3007/login`)
- [ ] Acessar página de planos (criar rota `/pricing` se não existir)
- [ ] Verificar se planos são exibidos
- [ ] Verificar se preços estão na moeda correta:
  - Tenant BR: Preços em BRL (R$)
  - Tenant US: Preços em USD ($)
- [ ] Verificar se features são exibidas
- [ ] Verificar se botão "Assinar" está presente

#### 2.2 Criar Assinatura (Brasil - Com Trial)
- [ ] Fazer login como usuário de tenant brasileiro
- [ ] Acessar página de planos
- [ ] Selecionar plano "Básico" (com trial de 14 dias)
- [ ] Clicar em "Assinar"
- [ ] Verificar redirecionamento para checkout
- [ ] Adicionar método de pagamento (cartão)
- [ ] Preencher dados do cartão (usar cartão de teste)
- [ ] Confirmar assinatura
- [ ] **Verificar**:
  - [ ] Assinatura foi criada
  - [ ] Status é `trialing` (por causa do trial)
  - [ ] Tenant foi atualizado com novo plano
  - [ ] Primeira fatura foi gerada (mas não cobrada ainda)
  - [ ] `trial_start` e `trial_end` foram definidos
  - [ ] Acesso está ativo durante trial

#### 2.3 Criar Assinatura (USA - Sem Trial)
- [ ] Fazer login como usuário de tenant americano
- [ ] Acessar página de planos
- [ ] Verificar se preços estão em USD
- [ ] Selecionar plano "Starter"
- [ ] Adicionar método de pagamento
- [ ] Confirmar assinatura
- [ ] **Verificar**:
  - [ ] Gateway usado é Stripe (não Asaas)
  - [ ] Assinatura foi criada
  - [ ] Status é `active` (sem trial)
  - [ ] Primeira fatura foi gerada e paga

---

### 3. Métodos de Pagamento

#### 3.1 Adicionar Cartão de Crédito
- [ ] Acessar área de métodos de pagamento (`/billing/payment-methods`)
- [ ] Clicar em "Adicionar Cartão"
- [ ] Preencher dados do cartão (via gateway SDK)
- [ ] Salvar método
- [ ] **Verificar**:
  - [ ] Cartão aparece na listagem
  - [ ] Últimos 4 dígitos são exibidos
  - [ ] Bandeira é exibida corretamente
  - [ ] Data de expiração é exibida

#### 3.2 Definir Cartão como Padrão
- [ ] Ter múltiplos cartões cadastrados
- [ ] Selecionar um cartão
- [ ] Clicar em "Definir como Padrão"
- [ ] **Verificar**:
  - [ ] Cartão foi marcado como padrão
  - [ ] Outros cartões não são mais padrão
  - [ ] Cartão padrão aparece primeiro na listagem

#### 3.3 Remover Cartão
- [ ] Selecionar cartão não padrão
- [ ] Clicar em "Remover"
- [ ] Confirmar remoção
- [ ] **Verificar**:
  - [ ] Cartão foi removido
  - [ ] Não é possível remover cartão padrão se for o único

---

### 4. Faturas

#### 4.1 Visualizar Faturas
- [ ] Acessar área de faturas (`/billing/invoices`)
- [ ] **Verificar**:
  - [ ] Faturas são listadas
  - [ ] Informações corretas:
    - Número da fatura
    - Valor
    - Data de vencimento
    - Status
  - [ ] Ordenação (mais recente primeiro)
  - [ ] Paginação funciona

#### 4.2 Filtrar Faturas
- [ ] Filtrar por status (paga, pendente, vencida)
- [ ] Filtrar por período
- [ ] **Verificar** se filtros funcionam corretamente

#### 4.3 Download de PDF
- [ ] Selecionar fatura paga
- [ ] Clicar em "Download PDF"
- [ ] **Verificar**:
  - [ ] PDF é baixado
  - [ ] PDF contém informações corretas
  - [ ] Layout está correto

---

### 5. Pagamentos

#### 5.1 Processamento Automático
- [ ] Criar assinatura com método de pagamento válido
- [ ] Aguardar vencimento da fatura (ou simular)
- [ ] **Verificar**:
  - [ ] Pagamento foi processado automaticamente
  - [ ] Fatura foi marcada como paga
  - [ ] Assinatura continua ativa
  - [ ] Nova fatura foi gerada para próximo período

#### 5.2 Falha de Pagamento
- [ ] Usar cartão inválido ou sem saldo
- [ ] Tentar processar pagamento
- [ ] **Verificar**:
  - [ ] Erro é exibido
  - [ ] Assinatura foi marcada como `past_due`
  - [ ] Email de notificação foi enviado (se configurado)
  - [ ] Retry automático é agendado (após 3 dias)

#### 5.3 Suspensão por Não Pagamento
- [ ] Simular múltiplas falhas de pagamento
- [ ] Aguardar 7 dias sem pagamento
- [ ] **Verificar**:
  - [ ] Tenant foi suspenso
  - [ ] Acesso foi bloqueado
  - [ ] Mensagem de suspensão é exibida

---

### 6. Upgrade/Downgrade

#### 6.1 Upgrade de Plano
- [ ] Ter assinatura ativa (plano básico)
- [ ] Acessar área de assinatura (`/billing/subscription`)
- [ ] Selecionar plano superior (profissional)
- [ ] Clicar em "Fazer Upgrade"
- [ ] Confirmar upgrade
- [ ] **Verificar**:
  - [ ] Upgrade foi aplicado imediatamente
  - [ ] Limites foram atualizados (projetos, usuários)
  - [ ] Fatura de ajuste (prorata) foi gerada
  - [ ] Prorata foi calculado corretamente
  - [ ] Tenant foi atualizado

#### 6.2 Downgrade de Plano
- [ ] Ter assinatura ativa (plano profissional)
- [ ] Selecionar plano inferior (básico)
- [ ] Clicar em "Fazer Downgrade"
- [ ] Confirmar downgrade
- [ ] **Verificar**:
  - [ ] Downgrade será aplicado no próximo ciclo
  - [ ] Acesso atual continua com limites do plano atual
  - [ ] Aguardar próximo ciclo e verificar se downgrade foi aplicado

---

### 7. Cancelamento

#### 7.1 Cancelar Assinatura
- [ ] Acessar área de assinatura
- [ ] Clicar em "Cancelar Assinatura"
- [ ] Preencher motivo (opcional)
- [ ] Confirmar cancelamento
- [ ] **Verificar**:
  - [ ] Assinatura foi marcada para cancelar ao fim do período
  - [ ] Acesso continua até fim do período
  - [ ] Email de confirmação foi enviado
  - [ ] `cancel_at_period_end = True`
  - [ ] `cancellation_reason` foi salvo

#### 7.2 Cancelamento Imediato
- [ ] Solicitar cancelamento imediato
- [ ] Confirmar (sem reembolso)
- [ ] **Verificar**:
  - [ ] Acesso foi bloqueado imediatamente
  - [ ] Assinatura foi cancelada
  - [ ] Status é `canceled`

---

### 8. Renovação Automática

#### 8.1 Renovação Bem-sucedida
- [ ] Ter assinatura ativa com método de pagamento válido
- [ ] Aguardar vencimento do período (ou simular)
- [ ] **Verificar**:
  - [ ] Nova fatura foi gerada automaticamente
  - [ ] Pagamento foi processado automaticamente
  - [ ] Assinatura foi renovada
  - [ ] Novo período foi definido
  - [ ] Status continua `active`

#### 8.2 Renovação com Falha
- [ ] Ter assinatura ativa com método de pagamento inválido
- [ ] Aguardar vencimento do período
- [ ] **Verificar**:
  - [ ] Fatura foi gerada
  - [ ] Pagamento falhou
  - [ ] Assinatura foi marcada como `past_due`
  - [ ] Retry foi agendado

---

### 9. Webhooks

#### 9.1 Webhook Asaas - Pagamento Confirmado
- [ ] Configurar webhook do Asaas (sandbox)
- [ ] Simular pagamento confirmado
- [ ] Enviar webhook para `/api/billing/webhooks/asaas/`
- [ ] **Verificar**:
  - [ ] Pagamento foi atualizado
  - [ ] Fatura foi marcada como paga
  - [ ] Assinatura continua ativa
  - [ ] Logs foram registrados

#### 9.2 Webhook Asaas - Pagamento Recusado
- [ ] Simular pagamento recusado
- [ ] Enviar webhook
- [ ] **Verificar**:
  - [ ] Pagamento foi marcado como falhado
  - [ ] Assinatura foi marcada como `past_due`
  - [ ] `failure_reason` foi salvo

#### 9.3 Webhook Stripe - Pagamento Confirmado
- [ ] Configurar webhook do Stripe (test mode)
- [ ] Simular evento `payment_intent.succeeded`
- [ ] Enviar webhook para `/api/billing/webhooks/stripe/`
- [ ] **Verificar**:
  - [ ] Pagamento foi atualizado
  - [ ] Fatura foi marcada como paga

---

### 10. Multi-moeda e Multi-país

#### 10.1 Preços por País
- [ ] Tenant brasileiro: verificar se preços são em BRL
- [ ] Tenant americano: verificar se preços são em USD
- [ ] **Verificar**:
  - [ ] Gateway correto é usado (BR → Asaas, US → Stripe)
  - [ ] Formatação de moeda está correta

#### 10.2 Faturas por Moeda
- [ ] Tenant brasileiro: verificar se faturas são em BRL
- [ ] Tenant americano: verificar se faturas são em USD
- [ ] **Verificar**:
  - [ ] Símbolo de moeda está correto
  - [ ] Formatação numérica está correta

---

## 🐛 Problemas Conhecidos e Soluções

### Problema: Assinatura não é criada
**Solução**: Verificar se tenant possui país configurado corretamente

### Problema: Gateway incorreto
**Solução**: Verificar `tenant.country` - BR deve usar Asaas, US deve usar Stripe

### Problema: Preço incorreto
**Solução**: Verificar se plano tem preço configurado para o país do tenant

### Problema: 403 Forbidden
**Solução**: Verificar se usuário está autenticado e tem tenant associado

---

## 📝 Relatório de Testes

Após executar todos os testes, preencher:

- [ ] **Data dos testes**: ___________
- [ ] **Testador**: ___________
- [ ] **Ambiente**: ___________
- [ ] **Testes passaram**: ___ / ___
- [ ] **Problemas encontrados**: ___________
- [ ] **Observações**: ___________

---

## ✅ Critérios de Sucesso

Para considerar os testes manuais como aprovados:

- [ ] Todos os fluxos principais funcionam
- [ ] Não há erros críticos
- [ ] UX está adequada
- [ ] Performance está aceitável
- [ ] Segurança está garantida

---

## ⏭️ Próximos Passos Após Testes Manuais

1. **Documentar problemas encontrados**
2. **Corrigir bugs identificados**
3. **Re-executar testes após correções**
4. **Passo 10: Deploy para Staging**

---

## 🎯 Status

**Progresso**: 7/13 passos concluídos (54%)

**Próxima ação**: Executar testes manuais seguindo este guia

