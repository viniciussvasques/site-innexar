import axios from 'axios';

// No Next.js, variáveis de ambiente precisam começar com NEXT_PUBLIC_ para serem acessíveis no cliente
let API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8010';

// Remover /api do final se existir para evitar duplicação
API_BASE_URL = API_BASE_URL.replace(/\/api\/?$/, '');

// Criar instância do axios
const api = axios.create({
  baseURL: `${API_BASE_URL}/api`,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Debug: verificar a URL base (remover em produção)
if (typeof window !== 'undefined') {
  console.log('API Base URL:', `${API_BASE_URL}/api`);
}

// Interceptor para adicionar token nas requisições
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('admin_access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    } else {
      console.warn('No access token found in localStorage');
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Interceptor para tratar erros e refresh token
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    // Se receber 401 e não for uma tentativa de refresh
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('admin_refresh_token');
        if (refreshToken) {
          const response = await api.post(
            '/auth/token/refresh/',
            { refresh: refreshToken }
          );

          const { access } = response.data;
          localStorage.setItem('admin_access_token', access);

          originalRequest.headers.Authorization = `Bearer ${access}`;
          return api(originalRequest);
        }
      } catch (refreshError) {
        // Se o refresh falhar, limpar tokens e redirecionar para login
        localStorage.removeItem('admin_access_token');
        localStorage.removeItem('admin_refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Serviços de autenticação
export const authService = {
  async login(email: string, password: string) {
    const response = await api.post('/auth/login/', {
      email,
      password,
    });
    
    const { tokens, user } = response.data;
    localStorage.setItem('admin_access_token', tokens.access);
    localStorage.setItem('admin_refresh_token', tokens.refresh);
    localStorage.setItem('admin_user', JSON.stringify(user));
    
    return { tokens, user };
  },

  async logout() {
    const refreshToken = localStorage.getItem('admin_refresh_token');
    if (refreshToken) {
      try {
        await api.post('/auth/logout/', { refresh: refreshToken });
      } catch (error) {
        console.error('Erro no logout:', error);
      }
    }
    localStorage.removeItem('admin_access_token');
    localStorage.removeItem('admin_refresh_token');
    localStorage.removeItem('admin_user');
  },

  getToken() {
    return localStorage.getItem('admin_access_token');
  },

  getCurrentUser() {
    const userStr = localStorage.getItem('admin_user');
    return userStr ? JSON.parse(userStr) : null;
  },

  isAuthenticated() {
    return !!localStorage.getItem('admin_access_token');
  },
};

// Serviços de tenants
export const tenantsService = {
  async list(params?: any) {
    const response = await api.get('/tenants/', { params });
    return response.data;
  },

  async get(id: string | number) {
    // Garantir que o ID é um número válido
    const tenantId = typeof id === 'string' ? parseInt(id, 10) : id;
    if (isNaN(tenantId)) {
      throw new Error('ID do tenant inválido');
    }
    const response = await api.get(`/tenants/${tenantId}/`);
    return response.data;
  },

  async create(data: any) {
    const response = await api.post('/tenants/', data);
    return response.data;
  },

  async update(id: string | number, data: any) {
    const response = await api.patch(`/tenants/${id}/`, data);
    return response.data;
  },

  async delete(id: string | number) {
    const response = await api.delete(`/tenants/${id}/`);
    return response.data;
  },

  async getAdminCredentials(id: string | number) {
    const response = await api.get(`/tenants/${id}/admin_credentials/`);
    return response.data;
  },

  async resetAdminPassword(id: string | number) {
    const response = await api.post(`/tenants/${id}/reset_admin_password/`);
    return response.data;
  },
};

export default api;

