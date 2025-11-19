# 🔵 Passo 1: Planejamento - Sistema de Billing e Pagamentos

**Data**: 2025-01-16  
**Módulo**: Billing e Pagamentos  
**Status**: 🟢 Em Andamento

---

## 📋 O que a feature resolve

### Problema

Construtoras e incorporadoras precisam de:

- Planos de assinatura claros e flexíveis
- Forma segura de pagar mensalidade/anualidade
- Controle sobre faturas e histórico de pagamentos
- Renovação automática de assinaturas
- Upgrade/downgrade de planos conforme necessidade

### Objetivo

Criar um sistema completo de billing que permita:

- Gestão de planos de assinatura (Free, Basic, Professional, Enterprise)
- Processamento de pagamentos via gateway (Asaas/Stripe)
- Geração automática de faturas
- Renovação automática de assinaturas
- Gestão de métodos de pagamento (cartão de crédito)
- Histórico completo de transações

---

## ✅ Requisitos Funcionais

### RF-001: Gestão de Planos

- **Descrição**: Admin pode criar, editar e desativar planos
- **Prioridade**: Crítica
- **Entrada**: Nome, preço, limites (projetos, usuários, storage), features
- **Saída**: Plano criado/editado
- **Regras**:
  - Preço mensal e anual obrigatórios
  - Limites devem ser números positivos
  - Não pode deletar plano com assinaturas ativas
  - Slug único e imutável

### RF-002: Assinatura de Plano

- **Descrição**: Tenant pode assinar um plano
- **Prioridade**: Crítica
- **Entrada**: Plano escolhido, método de pagamento
- **Saída**: Assinatura criada, tenant atualizado
- **Regras**:
  - Um tenant só pode ter uma assinatura ativa
  - Trial de 14 dias para novos planos (opcional)
  - Renovação automática ao final do período
  - Upgrade aplica imediatamente, downgrade no próximo ciclo

### RF-003: Métodos de Pagamento

- **Descrição**: Tenant pode adicionar/remover cartões de crédito
- **Prioridade**: Alta
- **Entrada**: Dados do cartão (tokenizado via gateway)
- **Saída**: Método de pagamento salvo
- **Regras**:
  - Dados do cartão nunca armazenados (PCI-DSS)
  - Apenas token do gateway armazenado
  - Últimos 4 dígitos e bandeira para exibição
  - Um método pode ser marcado como padrão

### RF-004: Geração de Faturas

- **Descrição**: Sistema gera faturas automaticamente
- **Prioridade**: Crítica
- **Entrada**: Assinatura ativa, período de cobrança
- **Saída**: Fatura criada com número único
- **Regras**:
  - Fatura gerada no início de cada ciclo
  - Número sequencial único (ex: INV-2025-0001)
  - PDF gerado automaticamente
  - Email enviado ao tenant

### RF-005: Processamento de Pagamento

- **Descrição**: Sistema processa pagamento via gateway
- **Prioridade**: Crítica
- **Entrada**: Fatura, método de pagamento
- **Saída**: Pagamento processado
- **Regras**:
  - Tentativa automática no vencimento
  - Retry em caso de falha (3 tentativas)
  - Notificação em caso de falha
  - Suspensão após 7 dias sem pagamento

### RF-006: Webhooks do Gateway

- **Descrição**: Sistema recebe notificações do gateway
- **Prioridade**: Alta
- **Entrada**: Webhook do gateway (Asaas/Stripe)
- **Saída**: Status atualizado (pagamento, assinatura)
- **Regras**:
  - Validar assinatura do webhook
  - Processar de forma idempotente
  - Log de todas as notificações
  - Retry em caso de erro

### RF-007: Upgrade/Downgrade

- **Descrição**: Tenant pode mudar de plano
- **Prioridade**: Média
- **Entrada**: Novo plano escolhido
- **Saída**: Assinatura atualizada
- **Regras**:
  - Upgrade: aplica imediatamente, cobra prorata
  - Downgrade: aplica no próximo ciclo
  - Fatura de ajuste gerada para upgrade

### RF-008: Cancelamento

- **Descrição**: Tenant pode cancelar assinatura
- **Prioridade**: Média
- **Entrada**: Solicitação de cancelamento
- **Saída**: Assinatura cancelada ao final do período
- **Regras**:
  - Cancelamento não imediato (mantém acesso até fim do período)
  - Opção de cancelamento imediato (sem reembolso)
  - Dados preservados por 90 dias

---

## 🔒 Requisitos Não Funcionais

### RNF-001: Segurança

- **PCI-DSS Compliance**: Nunca armazenar dados de cartão
- **Tokenização**: Apenas tokens do gateway armazenados
- **HTTPS**: Obrigatório em produção
- **Validação de Webhooks**: Assinatura verificada

### RNF-002: Performance

- **Processamento Assíncrono**: Webhooks processados em background
- **Cache**: Planos em cache (Redis)
- **Timeout**: Resposta de API < 2s (p95)

### RNF-003: Confiabilidade

- **Retry**: 3 tentativas em falhas de pagamento
- **Idempotência**: Webhooks processados de forma idempotente
- **Auditoria**: Log de todas as transações

### RNF-004: Escalabilidade

- **Suporte Multi-moeda**: BRL, USD, EUR
- **Multi-gateway**: Suporte a Asaas e Stripe
- **Horizontal**: Processamento distribuído

---

## ⚠️ Pontos Críticos

### 1. Segurança de Dados de Cartão

- **Risco**: Vazamento de dados de cartão
- **Mitigação**: Nunca armazenar, apenas tokens do gateway
- **Validação**: Auditoria de código, PCI-DSS compliance

### 2. Falhas de Pagamento

- **Risco**: Tenant perde acesso por falha técnica
- **Mitigação**: Retry automático, período de graça (7 dias)
- **Validação**: Testes de falha simulada

### 3. Webhooks Perdidos

- **Risco**: Status desatualizado
- **Mitigação**: Polling periódico como backup
- **Validação**: Monitoramento de webhooks recebidos

### 4. Renovação Automática

- **Risco**: Cobrança indevida
- **Mitigação**: Validação de assinatura ativa, notificação prévia
- **Validação**: Testes de renovação

### 5. Upgrade/Downgrade

- **Risco**: Cálculo incorreto de prorata
- **Mitigação**: Validação matemática, testes unitários
- **Validação**: Testes de casos extremos

---

## ✅ Critérios de Aceite

### CA-001: Criação de Plano

- [ ] Admin pode criar plano com todos os campos
- [ ] Validação de campos obrigatórios
- [ ] Slug único gerado automaticamente
- [ ] Plano aparece na listagem

### CA-002: Assinatura de Plano

- [ ] Tenant escolhe plano no frontend
- [ ] Checkout funcional com método de pagamento
- [ ] Assinatura criada no backend
- [ ] Tenant atualizado com novo plano
- [ ] Email de confirmação enviado

### CA-003: Adição de Cartão

- [ ] Formulário seguro de cartão
- [ ] Tokenização via gateway
- [ ] Cartão salvo como método padrão
- [ ] Últimos 4 dígitos exibidos

### CA-004: Geração de Fatura

- [ ] Fatura gerada automaticamente no início do ciclo
- [ ] Número único sequencial
- [ ] PDF gerado e disponível para download
- [ ] Email enviado ao tenant

### CA-005: Processamento de Pagamento

- [ ] Pagamento processado automaticamente no vencimento
- [ ] Retry em caso de falha (3 tentativas)
- [ ] Status atualizado corretamente
- [ ] Notificação em caso de falha

### CA-006: Webhooks

- [ ] Webhook recebido e validado
- [ ] Status atualizado corretamente
- [ ] Processamento idempotente
- [ ] Log de todas as notificações

### CA-007: Upgrade/Downgrade

- [ ] Upgrade aplica imediatamente
- [ ] Downgrade aplica no próximo ciclo
- [ ] Prorata calculado corretamente
- [ ] Fatura de ajuste gerada

### CA-008: Cancelamento

- [ ] Cancelamento marca fim do período
- [ ] Acesso mantido até fim do período
- [ ] Dados preservados por 90 dias
- [ ] Email de confirmação enviado

---

## 📝 User Stories

### US-001: Como Admin, quero criar planos para que tenants possam assinar

**Critérios de Aceite**:

- Posso definir nome, preço mensal/anual, limites e features
- Plano fica disponível para assinatura após criação
- Posso editar/desativar planos sem assinaturas ativas

### US-002: Como Tenant, quero assinar um plano para usar o sistema

**Critérios de Aceite**:

- Vejo todos os planos disponíveis com preços e features
- Posso escolher plano e adicionar método de pagamento
- Assinatura é criada e meu plano é atualizado
- Recebo email de confirmação

### US-003: Como Tenant, quero adicionar cartão de crédito para pagar assinatura

**Critérios de Aceite**:

- Formulário seguro para adicionar cartão
- Cartão é salvo como método de pagamento
- Posso definir qual cartão é padrão
- Vejo últimos 4 dígitos e bandeira

### US-004: Como Sistema, quero gerar faturas automaticamente para cobrar tenants

**Critérios de Aceite**:

- Fatura gerada no início de cada ciclo
- Número único sequencial
- PDF gerado automaticamente
- Email enviado ao tenant

### US-005: Como Tenant, quero ver minhas faturas para acompanhar pagamentos

**Critérios de Aceite**:

- Vejo histórico completo de faturas
- Posso baixar PDF de cada fatura
- Vejo status (paga, pendente, vencida)
- Posso filtrar por período

### US-006: Como Sistema, quero processar pagamentos automaticamente para manter assinaturas ativas

**Critérios de Aceite**:

- Pagamento processado no vencimento
- Retry automático em caso de falha
- Tenant notificado em caso de falha
- Assinatura suspensa após 7 dias sem pagamento

### US-007: Como Tenant, quero fazer upgrade de plano para ter mais recursos

**Critérios de Aceite**:

- Posso escolher novo plano
- Upgrade aplica imediatamente
- Prorata calculado e cobrado
- Novo limite aplicado imediatamente

### US-008: Como Tenant, quero cancelar assinatura quando não precisar mais

**Critérios de Aceite**:

- Posso solicitar cancelamento
- Acesso mantido até fim do período pago
- Dados preservados por 90 dias
- Recebo confirmação por email

---

## 📊 Métricas de Sucesso

- **Taxa de Conversão**: % de tenants que assinam plano pago
- **Taxa de Renovação**: % de assinaturas renovadas automaticamente
- **Taxa de Falha de Pagamento**: % de pagamentos que falham
- **Tempo de Resolução**: Tempo médio para resolver problemas de pagamento
- **Satisfação**: NPS relacionado a billing

---

## 🎯 Próximo Passo

**Passo 2: Design da Solução**

- Modelos de dados detalhados
- Diagramas de arquitetura
- Endpoints da API
- Fluxos de estado
- Regras de segurança
