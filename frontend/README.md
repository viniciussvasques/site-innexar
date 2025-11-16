# Frontend - StructurOne

Frontend web application para a plataforma StructurOne.

## 🚀 Início Rápido

### Setup Next.js

```bash
# Entrar na pasta frontend
cd frontend

# Instalar dependências
npm install

# Executar em desenvolvimento
npm run dev

# Build para produção
npm run build

# Executar produção
npm start
```

## 📁 Estrutura

```
frontend/
├── src/                  # Código fonte
│   ├── app/             # App Router (Next.js 13+)
│   ├── components/      # Componentes React
│   ├── services/        # Serviços de API
│   ├── hooks/           # Custom hooks
│   ├── utils/           # Utilitários
│   └── styles/          # Estilos
├── public/               # Arquivos públicos
├── package.json          # Dependências
└── next.config.js        # Configuração Next.js
```

## 🔌 Integração com API

O frontend consome a API REST do backend:

- **Base URL**: `http://localhost:8000/api/`
- **Autenticação**: JWT tokens
- **CORS**: Configurado no backend

### Exemplo de uso da API

```typescript
// services/api.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api';

export async function getProjects(token: string) {
  const response = await fetch(`${API_BASE_URL}/projects/`, {
    headers: {
      'Authorization': `Bearer ${token}`,
      'Content-Type': 'application/json',
    },
  });
  return response.json();
}
```

## 🌍 Variáveis de Ambiente

Criar arquivo `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000/api
NEXT_PUBLIC_APP_URL=http://localhost:3000
```

## 📦 Tecnologias

- **Framework**: Next.js 14+
- **Language**: TypeScript
- **Styling**: Tailwind CSS (ou styled-components)
- **State Management**: Zustand ou React Query
- **HTTP Client**: Fetch API ou Axios

## 🎨 Funcionalidades

1. **Autenticação** - Login/Logout com JWT
2. **Dashboard** - Visão geral para empresas
3. **Gestão de Projetos** - CRUD de projetos
4. **Portal do Investidor** - Visualização para investidores
5. **Gestão Financeira** - Visualização financeira
6. **Upload de Documentos** - Upload e visualização
7. **Atualizações de Obra** - Timeline de atualizações

## 🚀 Deploy

```bash
# Build
npm run build

# Deploy para Vercel, Netlify, ou VPS
```

## 📚 Documentação

- [Next.js Docs](https://nextjs.org/docs)
- [API Endpoints](../docs/API_ENDPOINTS.md)
