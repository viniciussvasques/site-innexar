# Exemplos Práticos de Uso da API - StructurOne

Este documento contém exemplos práticos de como usar a API StructurOne em diferentes linguagens e cenários.

## 📋 Índice

- [JavaScript/TypeScript (Fetch API)](#javascripttypescript-fetch-api)
- [JavaScript/TypeScript (Axios)](#javascripttypescript-axios)
- [Python (Requests)](#python-requests)
- [cURL](#curl)
- [Fluxos Completos](#fluxos-completos)

---

## JavaScript/TypeScript (Fetch API)

### Configuração Inicial

```typescript
const API_BASE_URL = 'http://localhost:8010/api';

// Helper para fazer requisições autenticadas
async function apiRequest(
  endpoint: string,
  options: RequestInit = {}
): Promise<Response> {
  const token = localStorage.getItem('access_token');
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
    ...options.headers,
  };
  
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });
  
  // Se token expirou, tentar renovar
  if (response.status === 401 && token) {
    const refreshed = await refreshToken();
    if (refreshed) {
      // Repetir requisição com novo token
      headers['Authorization'] = `Bearer ${localStorage.getItem('access_token')}`;
      return fetch(`${API_BASE_URL}${endpoint}`, {
        ...options,
        headers,
      });
    }
  }
  
  return response;
}

// Renovar token
async function refreshToken(): Promise<boolean> {
  const refreshToken = localStorage.getItem('refresh_token');
  if (!refreshToken) return false;
  
  try {
    const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh: refreshToken }),
    });
    
    if (response.ok) {
      const data = await response.json();
      localStorage.setItem('access_token', data.access);
      localStorage.setItem('refresh_token', data.refresh);
      return true;
    }
  } catch (error) {
    console.error('Erro ao renovar token:', error);
  }
  
  // Se falhou, fazer logout
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/login';
  return false;
}
```

### Registro de Usuário

```typescript
async function registerUser(userData: {
  email: string;
  password: string;
  password_confirm: string;
  first_name: string;
  last_name: string;
  phone?: string;
}) {
  try {
    const response = await apiRequest('/auth/register/', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
    
    if (response.ok) {
      const data = await response.json();
      
      // Salvar tokens
      localStorage.setItem('access_token', data.tokens.access);
      localStorage.setItem('refresh_token', data.tokens.refresh);
      
      // Salvar dados do usuário
      localStorage.setItem('user', JSON.stringify(data.user));
      
      return { success: true, user: data.user };
    } else {
      const error = await response.json();
      return { success: false, error };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Uso
const result = await registerUser({
  email: 'usuario@exemplo.com',
  password: 'SenhaSegura123!',
  password_confirm: 'SenhaSegura123!',
  first_name: 'João',
  last_name: 'Silva',
  phone: '+5511999999999',
});

if (result.success) {
  console.log('Usuário registrado:', result.user);
  // Redirecionar para onboarding
  window.location.href = '/onboarding';
} else {
  console.error('Erro no registro:', result.error);
}
```

### Login

```typescript
async function login(email: string, password: string) {
  try {
    const response = await apiRequest('/auth/login/', {
      method: 'POST',
      body: JSON.stringify({ email, password }),
    });
    
    if (response.ok) {
      const data = await response.json();
      
      // Salvar tokens
      localStorage.setItem('access_token', data.tokens.access);
      localStorage.setItem('refresh_token', data.tokens.refresh);
      
      // Salvar dados do usuário
      localStorage.setItem('user', JSON.stringify(data.user));
      
      return { success: true, user: data.user };
    } else {
      const error = await response.json();
      return { success: false, error };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Uso
const result = await login('usuario@exemplo.com', 'SenhaSegura123!');

if (result.success) {
  const user = result.user;
  if (user.onboarding_completed) {
    window.location.href = '/dashboard';
  } else {
    window.location.href = '/onboarding';
  }
} else {
  alert('Erro no login: ' + result.error.detail);
}
```

### Logout

```typescript
async function logout() {
  const refreshToken = localStorage.getItem('refresh_token');
  const accessToken = localStorage.getItem('access_token');
  
  if (!refreshToken) {
    // Limpar local storage mesmo sem token
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
    return;
  }
  
  try {
    const response = await apiRequest('/auth/logout/', {
      method: 'POST',
      body: JSON.stringify({ refresh: refreshToken }),
    });
    
    // Limpar local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    
    // Redirecionar para login
    window.location.href = '/login';
  } catch (error) {
    // Mesmo com erro, limpar local storage
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
}
```

### Obter Dados do Usuário

```typescript
async function getCurrentUser() {
  try {
    const response = await apiRequest('/auth/me/');
    
    if (response.ok) {
      const user = await response.json();
      return { success: true, user };
    } else {
      return { success: false, error: 'Não autenticado' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

### Onboarding - Obter Progresso

```typescript
async function getOnboardingProgress() {
  try {
    const response = await apiRequest('/onboarding/');
    
    if (response.ok) {
      const data = await response.json();
      return { success: true, data };
    } else {
      return { success: false, error: 'Erro ao obter progresso' };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

### Onboarding - Atualizar Etapa

```typescript
async function updateOnboardingStep(step: number, data: any) {
  try {
    const response = await apiRequest('/onboarding/', {
      method: 'POST',
      body: JSON.stringify({ step, data }),
    });
    
    if (response.ok) {
      const result = await response.json();
      return { success: true, data: result };
    } else {
      const error = await response.json();
      return { success: false, error };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Exemplo: Etapa 1 - Informações da Empresa
const result = await updateOnboardingStep(1, {
  company_name: 'Empresa ABC',
  cnpj: '12.345.678/0001-90',
  address: 'Rua Exemplo, 123, São Paulo, SP',
});

// Exemplo: Etapa 2 - Configuração Inicial
const result2 = await updateOnboardingStep(2, {
  primary_color: '#3B82F6',
  country: 'BR',
  language: 'pt-br',
  currency: 'BRL',
  timezone: 'America/Sao_Paulo',
  date_format: 'DD/MM/YYYY',
  number_format: '1.234,56',
});
```

### Onboarding - Completar

```typescript
async function completeOnboarding() {
  try {
    const response = await apiRequest('/onboarding/complete/', {
      method: 'POST',
    });
    
    if (response.ok) {
      const data = await response.json();
      return { success: true, data };
    } else {
      const error = await response.json();
      return { success: false, error };
    }
  } catch (error) {
    return { success: false, error: error.message };
  }
}
```

---

## JavaScript/TypeScript (Axios)

### Configuração Inicial

```typescript
import axios, { AxiosInstance, AxiosError } from 'axios';

const API_BASE_URL = 'http://localhost:8010/api';

// Criar instância do Axios
const api: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptor para adicionar token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Interceptor para renovar token quando expirar
api.interceptors.response.use(
  (response) => response,
  async (error: AxiosError) => {
    const originalRequest = error.config as any;
    
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) {
        // Redirecionar para login
        window.location.href = '/login';
        return Promise.reject(error);
      }
      
      try {
        const response = await axios.post(`${API_BASE_URL}/auth/token/refresh/`, {
          refresh: refreshToken,
        });
        
        const { access, refresh } = response.data;
        localStorage.setItem('access_token', access);
        localStorage.setItem('refresh_token', refresh);
        
        originalRequest.headers.Authorization = `Bearer ${access}`;
        return api(originalRequest);
      } catch (refreshError) {
        // Falhou ao renovar, fazer logout
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }
    
    return Promise.reject(error);
  }
);
```

### Exemplos de Uso com Axios

```typescript
// Registro
async function registerUser(userData: any) {
  try {
    const response = await api.post('/auth/register/', userData);
    const { user, tokens } = response.data;
    
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { success: true, user };
  } catch (error: any) {
    return { success: false, error: error.response?.data };
  }
}

// Login
async function login(email: string, password: string) {
  try {
    const response = await api.post('/auth/login/', { email, password });
    const { user, tokens } = response.data;
    
    localStorage.setItem('access_token', tokens.access);
    localStorage.setItem('refresh_token', tokens.refresh);
    localStorage.setItem('user', JSON.stringify(user));
    
    return { success: true, user };
  } catch (error: any) {
    return { success: false, error: error.response?.data };
  }
}

// Logout
async function logout() {
  try {
    const refreshToken = localStorage.getItem('refresh_token');
    if (refreshToken) {
      await api.post('/auth/logout/', { refresh: refreshToken });
    }
  } catch (error) {
    console.error('Erro no logout:', error);
  } finally {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('user');
    window.location.href = '/login';
  }
}

// Obter usuário atual
async function getCurrentUser() {
  try {
    const response = await api.get('/auth/me/');
    return { success: true, user: response.data };
  } catch (error: any) {
    return { success: false, error: error.response?.data };
  }
}
```

---

## Python (Requests)

### Configuração Inicial

```python
import requests
from typing import Optional, Dict, Any

API_BASE_URL = 'http://localhost:8010/api'

class StructurOneAPI:
    def __init__(self, base_url: str = API_BASE_URL):
        self.base_url = base_url
        self.access_token: Optional[str] = None
        self.refresh_token: Optional[str] = None
        self.session = requests.Session()
    
    def _get_headers(self, include_auth: bool = True) -> Dict[str, str]:
        headers = {'Content-Type': 'application/json'}
        if include_auth and self.access_token:
            headers['Authorization'] = f'Bearer {self.access_token}'
        return headers
    
    def _refresh_access_token(self) -> bool:
        """Renova o access token usando o refresh token"""
        if not self.refresh_token:
            return False
        
        try:
            response = requests.post(
                f'{self.base_url}/auth/token/refresh/',
                json={'refresh': self.refresh_token},
                headers={'Content-Type': 'application/json'}
            )
            
            if response.status_code == 200:
                data = response.json()
                self.access_token = data['access']
                self.refresh_token = data['refresh']
                return True
        except Exception as e:
            print(f'Erro ao renovar token: {e}')
        
        return False
    
    def _request(self, method: str, endpoint: str, **kwargs) -> requests.Response:
        """Faz requisição com retry automático se token expirar"""
        url = f'{self.base_url}{endpoint}'
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))
        
        response = self.session.request(
            method, url, headers=headers, **kwargs
        )
        
        # Se token expirou, tentar renovar
        if response.status_code == 401 and self.refresh_token:
            if self._refresh_access_token():
                # Repetir requisição com novo token
                headers['Authorization'] = f'Bearer {self.access_token}'
                response = self.session.request(
                    method, url, headers=headers, **kwargs
                )
        
        return response
```

### Exemplos de Uso

```python
# Criar instância
api = StructurOneAPI()

# Registro
def register_user(email: str, password: str, first_name: str, last_name: str):
    data = {
        'email': email,
        'password': password,
        'password_confirm': password,
        'first_name': first_name,
        'last_name': last_name,
    }
    
    response = api._request('POST', '/auth/register/', json=data)
    
    if response.status_code == 201:
        result = response.json()
        api.access_token = result['tokens']['access']
        api.refresh_token = result['tokens']['refresh']
        return {'success': True, 'user': result['user']}
    else:
        return {'success': False, 'error': response.json()}

# Login
def login(email: str, password: str):
    response = api._request('POST', '/auth/login/', json={
        'email': email,
        'password': password
    })
    
    if response.status_code == 200:
        result = response.json()
        api.access_token = result['tokens']['access']
        api.refresh_token = result['tokens']['refresh']
        return {'success': True, 'user': result['user']}
    else:
        return {'success': False, 'error': response.json()}

# Logout
def logout():
    if api.refresh_token:
        api._request('POST', '/auth/logout/', json={
            'refresh': api.refresh_token
        })
    
    api.access_token = None
    api.refresh_token = None

# Obter usuário atual
def get_current_user():
    response = api._request('GET', '/auth/me/')
    
    if response.status_code == 200:
        return {'success': True, 'user': response.json()}
    else:
        return {'success': False, 'error': response.json()}

# Onboarding - Obter progresso
def get_onboarding():
    response = api._request('GET', '/onboarding/')
    
    if response.status_code == 200:
        return {'success': True, 'data': response.json()}
    else:
        return {'success': False, 'error': response.json()}

# Onboarding - Atualizar etapa
def update_onboarding(step: int, data: Dict[str, Any]):
    response = api._request('POST', '/onboarding/', json={
        'step': step,
        'data': data
    })
    
    if response.status_code == 200:
        return {'success': True, 'data': response.json()}
    else:
        return {'success': False, 'error': response.json()}

# Exemplo de uso
if __name__ == '__main__':
    # Registrar
    result = register_user(
        email='usuario@exemplo.com',
        password='SenhaSegura123!',
        first_name='João',
        last_name='Silva'
    )
    
    if result['success']:
        print('Usuário registrado:', result['user'])
        
        # Atualizar onboarding - Etapa 1
        onboarding_result = update_onboarding(1, {
            'company_name': 'Empresa ABC',
            'cnpj': '12.345.678/0001-90',
            'address': 'Rua Exemplo, 123'
        })
        
        print('Onboarding atualizado:', onboarding_result)
```

---

## cURL

### Registro

```bash
curl -X POST http://localhost:8010/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com",
    "password": "SenhaSegura123!",
    "password_confirm": "SenhaSegura123!",
    "first_name": "João",
    "last_name": "Silva",
    "phone": "+5511999999999"
  }'
```

### Login

```bash
curl -X POST http://localhost:8010/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "email": "usuario@exemplo.com",
    "password": "SenhaSegura123!"
  }'
```

### Obter Usuário Atual

```bash
# Substituir {access_token} pelo token recebido no login
curl -X GET http://localhost:8010/api/auth/me/ \
  -H "Authorization: Bearer {access_token}"
```

### Renovar Token

```bash
curl -X POST http://localhost:8010/api/auth/token/refresh/ \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "{refresh_token}"
  }'
```

### Logout

```bash
curl -X POST http://localhost:8010/api/auth/logout/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "refresh": "{refresh_token}"
  }'
```

### Onboarding - Obter Progresso

```bash
curl -X GET http://localhost:8010/api/onboarding/ \
  -H "Authorization: Bearer {access_token}"
```

### Onboarding - Atualizar Etapa

```bash
curl -X POST http://localhost:8010/api/onboarding/ \
  -H "Authorization: Bearer {access_token}" \
  -H "Content-Type: application/json" \
  -d '{
    "step": 1,
    "data": {
      "company_name": "Empresa ABC",
      "cnpj": "12.345.678/0001-90",
      "address": "Rua Exemplo, 123"
    }
  }'
```

---

## Fluxos Completos

### Fluxo Completo de Registro e Onboarding

```typescript
async function completeRegistrationAndOnboarding() {
  // 1. Registrar usuário
  const registerResult = await registerUser({
    email: 'usuario@exemplo.com',
    password: 'SenhaSegura123!',
    password_confirm: 'SenhaSegura123!',
    first_name: 'João',
    last_name: 'Silva',
    phone: '+5511999999999',
  });
  
  if (!registerResult.success) {
    console.error('Erro no registro:', registerResult.error);
    return;
  }
  
  // 2. Etapa 1 - Informações da Empresa
  const step1Result = await updateOnboardingStep(1, {
    company_name: 'Empresa ABC',
    cnpj: '12.345.678/0001-90',
    address: 'Rua Exemplo, 123, São Paulo, SP',
  });
  
  if (!step1Result.success) {
    console.error('Erro na etapa 1:', step1Result.error);
    return;
  }
  
  // 3. Etapa 2 - Configuração Inicial
  const step2Result = await updateOnboardingStep(2, {
    primary_color: '#3B82F6',
    country: 'BR',
    language: 'pt-br',
    currency: 'BRL',
    timezone: 'America/Sao_Paulo',
    date_format: 'DD/MM/YYYY',
    number_format: '1.234,56',
  });
  
  if (!step2Result.success) {
    console.error('Erro na etapa 2:', step2Result.error);
    return;
  }
  
  // 4. Completar onboarding
  const completeResult = await completeOnboarding();
  
  if (completeResult.success) {
    console.log('Onboarding concluído com sucesso!');
    window.location.href = '/dashboard';
  } else {
    console.error('Erro ao completar onboarding:', completeResult.error);
  }
}
```

### Fluxo de Login com Renovação Automática de Token

```typescript
class APIClient {
  private accessToken: string | null = null;
  private refreshToken: string | null = null;
  
  async login(email: string, password: string) {
    const response = await fetch(`${API_BASE_URL}/auth/login/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    });
    
    if (response.ok) {
      const data = await response.json();
      this.accessToken = data.tokens.access;
      this.refreshToken = data.tokens.refresh;
      return { success: true, user: data.user };
    }
    
    return { success: false, error: await response.json() };
  }
  
  async request(endpoint: string, options: RequestInit = {}) {
    if (!this.accessToken) {
      throw new Error('Não autenticado');
    }
    
    const response = await fetch(`${API_BASE_URL}${endpoint}`, {
      ...options,
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${this.accessToken}`,
        ...options.headers,
      },
    });
    
    // Se token expirou, renovar
    if (response.status === 401) {
      const refreshed = await this.refreshAccessToken();
      if (refreshed) {
        // Repetir requisição
        return fetch(`${API_BASE_URL}${endpoint}`, {
          ...options,
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.accessToken}`,
            ...options.headers,
          },
        });
      }
    }
    
    return response;
  }
  
  private async refreshAccessToken(): Promise<boolean> {
    if (!this.refreshToken) return false;
    
    try {
      const response = await fetch(`${API_BASE_URL}/auth/token/refresh/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh: this.refreshToken }),
      });
      
      if (response.ok) {
        const data = await response.json();
        this.accessToken = data.access;
        this.refreshToken = data.refresh;
        return true;
      }
    } catch (error) {
      console.error('Erro ao renovar token:', error);
    }
    
    return false;
  }
  
  async logout() {
    if (this.refreshToken) {
      try {
        await this.request('/auth/logout/', {
          method: 'POST',
          body: JSON.stringify({ refresh: this.refreshToken }),
        });
      } catch (error) {
        console.error('Erro no logout:', error);
      }
    }
    
    this.accessToken = null;
    this.refreshToken = null;
  }
}

// Uso
const client = new APIClient();

// Login
await client.login('usuario@exemplo.com', 'SenhaSegura123!');

// Fazer requisições autenticadas (token renovado automaticamente se necessário)
const userResponse = await client.request('/auth/me/');
const user = await userResponse.json();

// Logout
await client.logout();
```

---

**Última atualização**: 2025-01-16

