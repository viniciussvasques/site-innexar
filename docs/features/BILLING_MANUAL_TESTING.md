# 🟤 Passo 7: Testes Manuais - Sistema de Billing

**Data**: 2025-01-16  
**Status**: 🟢 Em Andamento

---

## 📋 Procedimento de Testes Manuais

Este documento descreve os testes manuais a serem realizados no sistema de billing e pagamentos, testando como um usuário real.

---

## 🔧 Pré-requisitos

### Ambiente
- Backend rodando em `http://localhost:8010`
- Frontend rodando em `http://localhost:3007`
- Banco de dados com migrations aplicadas
- Credenciais de gateway configuradas (Asaas/Stripe)

### Dados de Teste
- Tenant brasileiro criado
- Tenant americano criado
- Usuário autenticado em cada tenant

---

## ✅ Checklist de Testes Manuais

### 1. Gestão de Planos (Admin)

#### 1.1 Criar Plano
- [ ] Acessar admin Django (`/admin/billing/plan/add/`)
- [ ] Preencher campos:
  - Nome: "Básico"
  - Slug: "basic"
  - Preço Mensal (BRL): 297.00
  - Preço Anual (BRL): 2970.00
  - Preço Mensal (USD): 49.00
  - Preço Anual (USD): 490.00
  - Máximo de Projetos: 5
  - Máximo de Usuários: 5
  - Features: ["Relatórios básicos", "Suporte por email"]
- [ ] Salvar plano
- [ ] Verificar se plano aparece na listagem
- [ ] Verificar se plano está disponível via API

#### 1.2 Editar Plano
- [ ] Acessar plano existente
- [ ] Alterar preço
- [ ] Salvar alterações
- [ ] Verificar se alterações foram aplicadas

#### 1.3 Desativar Plano
- [ ] Desativar plano existente
- [ ] Verificar se plano não aparece mais na API (apenas ativos)
- [ ] Verificar se assinaturas existentes continuam funcionando

---

### 2. Assinatura de Plano (Frontend)

#### 2.1 Visualizar Planos
- [ ] Acessar `/pricing` (ou página de planos)
- [ ] Verificar se planos são exibidos corretamente
- [ ] Verificar se preços estão na moeda correta (BRL para BR, USD para US)
- [ ] Verificar se features são exibidas
- [ ] Verificar se botão "Assinar" está presente

#### 2.2 Criar Assinatura (Brasil)
- [ ] Fazer login como usuário de tenant brasileiro
- [ ] Acessar página de planos
- [ ] Selecionar plano "Básico"
- [ ] Clicar em "Assinar"
- [ ] Verificar redirecionamento para checkout
- [ ] Adicionar método de pagamento (cartão)
- [ ] Preencher dados do cartão
- [ ] Confirmar assinatura
- [ ] Verificar se assinatura foi criada
- [ ] Verificar se tenant foi atualizado com novo plano
- [ ] Verificar se primeira fatura foi gerada
- [ ] Verificar email de confirmação (se configurado)

#### 2.3 Criar Assinatura (USA)
- [ ] Fazer login como usuário de tenant americano
- [ ] Acessar página de planos
- [ ] Verificar se preços estão em USD
- [ ] Selecionar plano "Starter"
- [ ] Adicionar método de pagamento
- [ ] Confirmar assinatura
- [ ] Verificar se gateway usado é Stripe (não Asaas)
- [ ] Verificar se assinatura foi criada corretamente

#### 2.4 Assinatura com Trial
- [ ] Criar plano com trial de 14 dias
- [ ] Assinar plano
- [ ] Verificar se status é "trialing"
- [ ] Verificar se trial_start e trial_end foram definidos
- [ ] Verificar se acesso está ativo durante trial

---

### 3. Métodos de Pagamento

#### 3.1 Adicionar Cartão de Crédito
- [ ] Acessar área de métodos de pagamento
- [ ] Clicar em "Adicionar Cartão"
- [ ] Preencher dados do cartão (via gateway)
- [ ] Salvar método
- [ ] Verificar se cartão aparece na listagem
- [ ] Verificar se últimos 4 dígitos são exibidos
- [ ] Verificar se bandeira é exibida corretamente

#### 3.2 Definir Cartão como Padrão
- [ ] Ter múltiplos cartões cadastrados
- [ ] Selecionar um cartão
- [ ] Clicar em "Definir como Padrão"
- [ ] Verificar se cartão foi marcado como padrão
- [ ] Verificar se outros cartões não são mais padrão

#### 3.3 Remover Cartão
- [ ] Selecionar cartão não padrão
- [ ] Clicar em "Remover"
- [ ] Confirmar remoção
- [ ] Verificar se cartão foi removido
- [ ] Verificar se não é possível remover cartão padrão (se for o único)

---

### 4. Faturas

#### 4.1 Visualizar Faturas
- [ ] Acessar área de faturas
- [ ] Verificar se faturas são listadas
- [ ] Verificar se informações estão corretas:
  - Número da fatura
  - Valor
  - Data de vencimento
  - Status
- [ ] Verificar ordenação (mais recente primeiro)

#### 4.2 Download de PDF
- [ ] Selecionar fatura paga
- [ ] Clicar em "Download PDF"
- [ ] Verificar se PDF é baixado
- [ ] Verificar se PDF contém informações corretas

#### 4.3 Filtros de Faturas
- [ ] Filtrar por status (paga, pendente, vencida)
- [ ] Filtrar por período
- [ ] Verificar se filtros funcionam corretamente

---

### 5. Pagamentos

#### 5.1 Processamento Automático
- [ ] Criar assinatura com método de pagamento
- [ ] Aguardar vencimento da fatura
- [ ] Verificar se pagamento foi processado automaticamente
- [ ] Verificar se fatura foi marcada como paga
- [ ] Verificar se assinatura continua ativa

#### 5.2 Falha de Pagamento
- [ ] Usar cartão inválido ou sem saldo
- [ ] Tentar processar pagamento
- [ ] Verificar se erro é exibido
- [ ] Verificar se assinatura foi marcada como "past_due"
- [ ] Verificar se email de notificação foi enviado (se configurado)
- [ ] Verificar retry automático (após 3 dias)

#### 5.3 Suspensão por Não Pagamento
- [ ] Simular múltiplas falhas de pagamento
- [ ] Aguardar 7 dias sem pagamento
- [ ] Verificar se tenant foi suspenso
- [ ] Verificar se acesso foi bloqueado

---

### 6. Upgrade/Downgrade

#### 6.1 Upgrade de Plano
- [ ] Ter assinatura ativa (plano básico)
- [ ] Acessar área de assinatura
- [ ] Selecionar plano superior (profissional)
- [ ] Clicar em "Fazer Upgrade"
- [ ] Confirmar upgrade
- [ ] Verificar se upgrade foi aplicado imediatamente
- [ ] Verificar se limites foram atualizados (projetos, usuários)
- [ ] Verificar se fatura de ajuste (prorata) foi gerada
- [ ] Verificar se prorata foi calculado corretamente

#### 6.2 Downgrade de Plano
- [ ] Ter assinatura ativa (plano profissional)
- [ ] Selecionar plano inferior (básico)
- [ ] Clicar em "Fazer Downgrade"
- [ ] Confirmar downgrade
- [ ] Verificar se downgrade será aplicado no próximo ciclo
- [ ] Verificar se acesso atual continua com limites do plano atual
- [ ] Aguardar próximo ciclo e verificar se downgrade foi aplicado

---

### 7. Cancelamento

#### 7.1 Cancelar Assinatura
- [ ] Acessar área de assinatura
- [ ] Clicar em "Cancelar Assinatura"
- [ ] Preencher motivo (opcional)
- [ ] Confirmar cancelamento
- [ ] Verificar se assinatura foi marcada para cancelar ao fim do período
- [ ] Verificar se acesso continua até fim do período
- [ ] Verificar se email de confirmação foi enviado

#### 7.2 Cancelamento Imediato
- [ ] Solicitar cancelamento imediato
- [ ] Confirmar (sem reembolso)
- [ ] Verificar se acesso foi bloqueado imediatamente
- [ ] Verificar se assinatura foi cancelada

---

### 8. Renovação Automática

#### 8.1 Renovação Bem-sucedida
- [ ] Ter assinatura ativa com método de pagamento válido
- [ ] Aguardar vencimento do período
- [ ] Verificar se nova fatura foi gerada automaticamente
- [ ] Verificar se pagamento foi processado automaticamente
- [ ] Verificar se assinatura foi renovada
- [ ] Verificar se novo período foi definido

#### 8.2 Renovação com Falha
- [ ] Ter assinatura ativa com método de pagamento inválido
- [ ] Aguardar vencimento do período
- [ ] Verificar se fatura foi gerada
- [ ] Verificar se pagamento falhou
- [ ] Verificar se assinatura foi marcada como "past_due"
- [ ] Verificar se retry foi agendado

---

### 9. Webhooks

#### 9.1 Webhook Asaas - Pagamento Confirmado
- [ ] Configurar webhook do Asaas
- [ ] Simular pagamento confirmado
- [ ] Enviar webhook para `/api/billing/webhooks/asaas/`
- [ ] Verificar se pagamento foi atualizado
- [ ] Verificar se fatura foi marcada como paga
- [ ] Verificar se assinatura continua ativa

#### 9.2 Webhook Asaas - Pagamento Recusado
- [ ] Simular pagamento recusado
- [ ] Enviar webhook
- [ ] Verificar se pagamento foi marcado como falhado
- [ ] Verificar se assinatura foi marcada como "past_due"

#### 9.3 Webhook Stripe - Pagamento Confirmado
- [ ] Configurar webhook do Stripe
- [ ] Simular evento `payment_intent.succeeded`
- [ ] Enviar webhook para `/api/billing/webhooks/stripe/`
- [ ] Verificar se pagamento foi atualizado
- [ ] Verificar se fatura foi marcada como paga

---

### 10. Multi-moeda e Multi-país

#### 10.1 Preços por País
- [ ] Tenant brasileiro: verificar se preços são em BRL
- [ ] Tenant americano: verificar se preços são em USD
- [ ] Verificar se gateway correto é usado (BR → Asaas, US → Stripe)

#### 10.2 Faturas por Moeda
- [ ] Tenant brasileiro: verificar se faturas são em BRL
- [ ] Tenant americano: verificar se faturas são em USD

---

## 🐛 Problemas Conhecidos e Soluções

### Problema: Assinatura não é criada
**Solução**: Verificar se tenant possui país configurado corretamente

### Problema: Gateway incorreto
**Solução**: Verificar `tenant.country` - BR deve usar Asaas, US deve usar Stripe

### Problema: Preço incorreto
**Solução**: Verificar se plano tem preço configurado para o país do tenant

---

## 📝 Relatório de Testes

Após executar todos os testes, preencher:

- [ ] Data dos testes: ___________
- [ ] Testador: ___________
- [ ] Ambiente: ___________
- [ ] Testes passaram: ___ / ___
- [ ] Problemas encontrados: ___________
- [ ] Observações: ___________

---

## ⏭️ Próximos Passos

Após testes manuais:
- [ ] Documentar problemas encontrados
- [ ] Corrigir bugs identificados
- [ ] Re-executar testes após correções
- [ ] Passo 8: Revisão de Código

