# 🌍 Lógica de País para Billing

**Data**: 2025-01-16  
**Conceito**: País de Registro vs País de Operação

---

## 🎯 Princípio Fundamental

**O billing é baseado no país onde a empresa está REGISTRADA, não onde ela constrói.**

### Exemplos Reais:

1. **Empresa Brasileira construindo nos EUA**
   - País de registro: Brasil (BR)
   - País de construção: Estados Unidos (US)
   - **Billing**: BRL via Asaas (gateway brasileiro)
   - **Projetos**: Podem ser criados nos EUA, mas billing em BRL

2. **Empresa Americana construindo no Brasil**
   - País de registro: Estados Unidos (US)
   - País de construção: Brasil (BR)
   - **Billing**: USD via Stripe (gateway americano)
   - **Projetos**: Podem ser criados no Brasil, mas billing em USD

---

## 📊 Como Funciona

### 1. Onboarding
```
Usuário seleciona país no onboarding
    ↓
Sistema define tenant.country (país de registro)
    ↓
Sistema configura automaticamente:
- Moeda (BRL para BR, USD para US)
- Gateway (Asaas para BR, Stripe para US)
- Idioma padrão
- Formato de data/número
```

### 2. Seleção de Plano
```
Sistema verifica tenant.country
    ↓
Se tenant.country == 'BR':
    - Mostra preços em BRL
    - Gateway: Asaas
    - Métodos: Cartão, Boleto, PIX
    
Se tenant.country == 'US':
    - Mostra preços em USD
    - Gateway: Stripe
    - Métodos: Cartão, ACH, Apple Pay
```

### 3. Criação de Projetos
```
Empresa pode criar projetos em QUALQUER país
    ↓
Projeto tem campo project.country (país de construção)
    ↓
Billing continua baseado em tenant.country (país de registro)
```

---

## 🏗️ Estrutura de Dados

### Tenant (Empresa)
```python
tenant.country = 'BR'  # País de REGISTRO (determina billing)
tenant.currency = 'BRL'  # Moeda de billing
tenant.language = 'pt-br'  # Idioma padrão
```

### Project (Projeto)
```python
project.country = 'US'  # País de CONSTRUÇÃO (pode ser diferente)
project.address = {...}  # Endereço no país de construção
```

### Subscription (Assinatura)
```python
subscription.tenant.country = 'BR'  # Herda do tenant
subscription.currency = 'BRL'  # Herda do tenant
subscription.gateway = 'asaas'  # Determinado pelo país do tenant
```

---

## 💡 Vantagens Desta Abordagem

### ✅ Simplicidade
- Um único país de registro por empresa
- Billing unificado em uma moeda
- Gateway único por empresa

### ✅ Compliance
- Impostos baseados no país de registro
- Faturas na moeda do país de registro
- Compliance com leis do país de registro

### ✅ Flexibilidade
- Empresa pode construir em múltiplos países
- Cada projeto pode ter seu próprio país
- Billing permanece centralizado

### ✅ Experiência do Usuário
- Preços na moeda que a empresa conhece
- Gateway do país de registro (mais familiar)
- Métodos de pagamento locais

---

## 🔄 Fluxo Completo

### Cenário: Empresa Brasileira construindo nos EUA

```
1. Onboarding
   - Usuário seleciona: País = Brasil
   - Sistema configura: currency = BRL, gateway = Asaas

2. Assinatura
   - Plano escolhido: Professional
   - Preço exibido: R$ 797,00/mês (BRL)
   - Gateway usado: Asaas
   - Método de pagamento: Cartão brasileiro ou PIX

3. Criação de Projeto
   - Projeto criado: "Residencial Miami"
   - project.country = 'US' (construção nos EUA)
   - tenant.country = 'BR' (billing continua em BRL)

4. Fatura
   - Fatura gerada em BRL
   - Gateway: Asaas
   - Projeto pode estar nos EUA, mas billing em BRL
```

---

## 🎯 Regras de Negócio

### RN-001: País de Registro
- Definido no onboarding (tenant.country)
- Não pode ser alterado facilmente (requer suporte)
- Determina moeda, gateway e métodos de pagamento

### RN-002: País de Construção
- Definido por projeto (project.country)
- Pode ser diferente do país de registro
- Não afeta o billing

### RN-003: Gateway
- BR → Asaas (BRL, PIX, Boleto)
- US → Stripe (USD, ACH, Apple Pay)
- Outros → Stripe (padrão internacional)

### RN-004: Moeda
- BR → BRL
- US → USD
- Outros → USD (padrão)

---

## 📝 Exceções e Casos Especiais

### Empresa Multinacional
- **Solução**: Criar tenant separado por país de registro
- Exemplo: "Construtora BR Ltda" (tenant BR) e "Construction USA Inc" (tenant US)

### Mudança de País
- **Processo**: Requer suporte manual
- Migração de dados
- Nova configuração de gateway
- Conversão de assinatura

### Projetos em Múltiplos Países
- **Permitido**: Sim, sem restrições
- Cada projeto tem seu próprio país
- Billing permanece no país de registro

---

## ✅ Conclusão

**Mantemos a arquitetura original:**
- País de registro (tenant.country) determina billing
- Projetos podem ser em qualquer país
- Simples, claro e compliance-friendly

