# Exemplos Práticos - API de Billing

Este documento fornece exemplos práticos de uso da API de Billing em diferentes linguagens.

---

## JavaScript/TypeScript (Fetch API)

### Listar Planos

```javascript
async function listPlans() {
  const response = await fetch('http://localhost:8010/api/billing/plans/', {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });
  
  const data = await response.json();
  console.log('Planos disponíveis:', data.results);
  return data;
}
```

### Criar Assinatura

```javascript
async function createSubscription(planId, paymentMethodId) {
  const response = await fetch('http://localhost:8010/api/billing/subscriptions/create/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      plan_id: planId,
      payment_method_id: paymentMethodId,
      billing_cycle: 'monthly',
    }),
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail);
  }
  
  const subscription = await response.json();
  console.log('Assinatura criada:', subscription);
  return subscription;
}
```

### Adicionar Método de Pagamento

```javascript
async function addPaymentMethod(token, isDefault = false) {
  const response = await fetch('http://localhost:8010/api/billing/payment-methods/', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      type: 'card',
      token: token, // Token obtido do gateway (Stripe/Asaas)
      is_default: isDefault,
      billing_details: {
        name: 'João Silva',
        email: 'joao@example.com',
      },
    }),
  });
  
  const paymentMethod = await response.json();
  console.log('Método de pagamento adicionado:', paymentMethod);
  return paymentMethod;
}
```

### Fazer Upgrade

```javascript
async function upgradeSubscription(subscriptionId, newPlanId) {
  const response = await fetch(
    `http://localhost:8010/api/billing/subscriptions/${subscriptionId}/upgrade/`,
    {
      method: 'PATCH',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        plan_id: newPlanId,
      }),
    }
  );
  
  const result = await response.json();
  console.log('Upgrade realizado:', result);
  
  if (result.adjustment_invoice) {
    console.log('Fatura de ajuste gerada:', result.adjustment_invoice);
  }
  
  return result;
}
```

### Listar Faturas

```javascript
async function listInvoices(status = null, page = 1) {
  let url = `http://localhost:8010/api/billing/invoices/?page=${page}`;
  if (status) {
    url += `&status=${status}`;
  }
  
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Authorization': `Bearer ${accessToken}`,
      'Content-Type': 'application/json',
    },
  });
  
  const data = await response.json();
  console.log('Faturas:', data.results);
  return data;
}
```

---

## JavaScript/TypeScript (Axios)

### Configuração Inicial

```javascript
import axios from 'axios';

const billingAPI = axios.create({
  baseURL: 'http://localhost:8010/api/billing/',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token
billingAPI.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para refresh token
billingAPI.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Tentar refresh token
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const { data } = await axios.post('http://localhost:8010/api/auth/refresh/', {
            refresh: refreshToken,
          });
          localStorage.setItem('access_token', data.access);
          error.config.headers.Authorization = `Bearer ${data.access}`;
          return axios.request(error.config);
        } catch (refreshError) {
          // Redirecionar para login
          window.location.href = '/login';
        }
      }
    }
    return Promise.reject(error);
  }
);
```

### Usar API

```javascript
// Listar planos
const plans = await billingAPI.get('/plans/');

// Criar assinatura
const subscription = await billingAPI.post('/subscriptions/create/', {
  plan_id: 2,
  payment_method_id: 1,
  billing_cycle: 'monthly',
});

// Minha assinatura
const mySubscription = await billingAPI.get('/subscriptions/me/');

// Faturas
const invoices = await billingAPI.get('/invoices/', {
  params: { status: 'paid', page: 1 },
});
```

---

## Python (Requests)

### Configuração Inicial

```python
import requests
from typing import Optional, Dict, Any

class BillingAPI:
    def __init__(self, base_url: str, access_token: str):
        self.base_url = base_url.rstrip('/')
        self.access_token = access_token
        self.headers = {
            'Authorization': f'Bearer {access_token}',
            'Content-Type': 'application/json',
        }
    
    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f'{self.base_url}{endpoint}'
        response = requests.request(method, url, headers=self.headers, **kwargs)
        response.raise_for_status()
        return response.json()
    
    def list_plans(self):
        """Lista todos os planos"""
        return self._request('GET', '/plans/')
    
    def get_plan(self, slug: str):
        """Detalhes de um plano"""
        return self._request('GET', f'/plans/{slug}/')
    
    def get_subscription(self):
        """Minha assinatura"""
        return self._request('GET', '/subscriptions/me/')
    
    def create_subscription(self, plan_id: int, payment_method_id: Optional[int] = None, billing_cycle: str = 'monthly'):
        """Cria assinatura"""
        data = {
            'plan_id': plan_id,
            'billing_cycle': billing_cycle,
        }
        if payment_method_id:
            data['payment_method_id'] = payment_method_id
        return self._request('POST', '/subscriptions/create/', json=data)
    
    def upgrade_subscription(self, subscription_id: int, new_plan_id: int):
        """Faz upgrade de assinatura"""
        return self._request('PATCH', f'/subscriptions/{subscription_id}/upgrade/', json={
            'plan_id': new_plan_id,
        })
    
    def cancel_subscription(self, subscription_id: int, reason: Optional[str] = None):
        """Cancela assinatura"""
        data = {}
        if reason:
            data['reason'] = reason
        return self._request('PATCH', f'/subscriptions/{subscription_id}/cancel/', json=data)
    
    def list_invoices(self, status: Optional[str] = None, page: int = 1):
        """Lista faturas"""
        params = {'page': page}
        if status:
            params['status'] = status
        return self._request('GET', '/invoices/', params=params)
    
    def get_invoice_pdf(self, invoice_id: int):
        """URL do PDF da fatura"""
        return self._request('GET', f'/invoices/{invoice_id}/pdf/')
    
    def list_payment_methods(self):
        """Lista métodos de pagamento"""
        return self._request('GET', '/payment-methods/')
    
    def add_payment_method(self, token: str, is_default: bool = False):
        """Adiciona método de pagamento"""
        return self._request('POST', '/payment-methods/', json={
            'type': 'card',
            'token': token,
            'is_default': is_default,
        })
    
    def set_default_payment_method(self, payment_method_id: int):
        """Define método como padrão"""
        return self._request('PATCH', f'/payment-methods/{payment_method_id}/set-default/')
    
    def delete_payment_method(self, payment_method_id: int):
        """Remove método de pagamento"""
        return self._request('DELETE', f'/payment-methods/{payment_method_id}/')

# Uso
api = BillingAPI('http://localhost:8010/api/billing', 'seu_token_aqui')

# Listar planos
plans = api.list_plans()
print(f"Planos disponíveis: {len(plans['results'])}")

# Criar assinatura
subscription = api.create_subscription(plan_id=2, payment_method_id=1)
print(f"Assinatura criada: {subscription['id']}")

# Minha assinatura
my_subscription = api.get_subscription()
print(f"Status: {my_subscription['status']}")

# Faturas
invoices = api.list_invoices(status='paid')
print(f"Faturas pagas: {len(invoices['results'])}")
```

---

## cURL

### Listar Planos

```bash
curl -X GET http://localhost:8010/api/billing/plans/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json"
```

### Criar Assinatura

```bash
curl -X POST http://localhost:8010/api/billing/subscriptions/create/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": 2,
    "payment_method_id": 1,
    "billing_cycle": "monthly"
  }'
```

### Minha Assinatura

```bash
curl -X GET http://localhost:8010/api/billing/subscriptions/me/ \
  -H "Authorization: Bearer <access_token>"
```

### Fazer Upgrade

```bash
curl -X PATCH http://localhost:8010/api/billing/subscriptions/1/upgrade/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "plan_id": 3
  }'
```

### Cancelar Assinatura

```bash
curl -X PATCH http://localhost:8010/api/billing/subscriptions/1/cancel/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "reason": "Não estou mais usando"
  }'
```

### Listar Faturas

```bash
curl -X GET "http://localhost:8010/api/billing/invoices/?status=paid&page=1" \
  -H "Authorization: Bearer <access_token>"
```

### Adicionar Método de Pagamento

```bash
curl -X POST http://localhost:8010/api/billing/payment-methods/ \
  -H "Authorization: Bearer <access_token>" \
  -H "Content-Type: application/json" \
  -d '{
    "type": "card",
    "token": "tok_xxx",
    "is_default": true
  }'
```

---

## Fluxo Completo: Assinatura

### 1. Autenticar

```javascript
// Login
const loginResponse = await fetch('http://localhost:8010/api/auth/login/', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'senha123',
  }),
});

const { tokens, user } = await loginResponse.json();
const accessToken = tokens.access;
```

### 2. Listar Planos

```javascript
const plansResponse = await fetch('http://localhost:8010/api/billing/plans/', {
  headers: { 'Authorization': `Bearer ${accessToken}` },
});

const plans = await plansResponse.json();
const selectedPlan = plans.results.find(p => p.slug === 'professional');
```

### 3. Obter Token do Gateway (Frontend)

```javascript
// Stripe (exemplo)
const stripe = Stripe('pk_test_...');
const { token } = await stripe.createToken(cardElement);

// Ou Asaas (exemplo)
// Token obtido via SDK do Asaas
```

### 4. Adicionar Método de Pagamento

```javascript
const pmResponse = await fetch('http://localhost:8010/api/billing/payment-methods/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    type: 'card',
    token: token.id, // Token do Stripe/Asaas
    is_default: true,
  }),
});

const paymentMethod = await pmResponse.json();
```

### 5. Criar Assinatura

```javascript
const subscriptionResponse = await fetch('http://localhost:8010/api/billing/subscriptions/create/', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    plan_id: selectedPlan.id,
    payment_method_id: paymentMethod.id,
    billing_cycle: 'monthly',
  }),
});

const subscription = await subscriptionResponse.json();
console.log('Assinatura criada!', subscription);
```

### 6. Verificar Faturas

```javascript
const invoicesResponse = await fetch('http://localhost:8010/api/billing/invoices/', {
  headers: { 'Authorization': `Bearer ${accessToken}` },
});

const invoices = await invoicesResponse.json();
console.log('Faturas:', invoices.results);
```

---

## Tratamento de Erros

### JavaScript

```javascript
async function createSubscription(planId, paymentMethodId) {
  try {
    const response = await fetch('http://localhost:8010/api/billing/subscriptions/create/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${accessToken}`,
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        plan_id: planId,
        payment_method_id: paymentMethodId,
      }),
    });
    
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || 'Erro ao criar assinatura');
    }
    
    return await response.json();
  } catch (error) {
    console.error('Erro:', error.message);
    // Tratar erro (ex: mostrar mensagem ao usuário)
    throw error;
  }
}
```

### Python

```python
try:
    subscription = api.create_subscription(plan_id=2, payment_method_id=1)
    print(f"Assinatura criada: {subscription['id']}")
except requests.exceptions.HTTPError as e:
    error_data = e.response.json()
    print(f"Erro: {error_data.get('detail', 'Erro desconhecido')}")
except Exception as e:
    print(f"Erro inesperado: {e}")
```

---

## Notas Importantes

1. **Token de Autenticação**: Sempre incluir no header `Authorization`
2. **Refresh Token**: Renovar quando expirar (401)
3. **Rate Limiting**: Respeitar limites de requisições
4. **Tratamento de Erros**: Sempre verificar status da resposta
5. **Validação**: Validar dados antes de enviar

