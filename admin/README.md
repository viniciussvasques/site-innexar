# Painel Admin - StructurOne

Painel administrativo desenvolvido com **Next.js** (mesma tecnologia do frontend).

## 🚀 Início Rápido

```bash
# Entrar na pasta admin
cd admin

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env.local
# Editar .env.local com suas configurações

# Executar em desenvolvimento
npm run dev

# Acessar em http://localhost:3001
```

## 📁 Estrutura

```
admin/
├── src/
│   └── app/              # Next.js App Router
│       ├── layout.tsx    # Layout principal
│       ├── page.tsx      # Página inicial
│       ├── tenants/      # Gerenciamento de Tenants
│       │   ├── page.tsx  # Lista de tenants
│       │   └── [id]/     # Detalhes do tenant
│       └── dashboard/    # Dashboard (futuro)
├── package.json          # Dependências
├── tsconfig.json         # TypeScript config
└── next.config.js        # Next.js config
```

## 🔌 Integração com API

O admin consome a API REST do backend:

- **Base URL**: `http://localhost:8000/api/`
- **Autenticação**: JWT tokens (a implementar)
- **CORS**: Configurado no backend

## 📋 Funcionalidades

### ✅ Implementado

1. **Gerenciamento de Tenants**
   - Listar tenants
   - Ver detalhes do tenant
   - Ativar/Desativar tenant
   - Criar novo tenant (a implementar)

### 🚧 Em Desenvolvimento

1. **Autenticação JWT**
2. **Dashboard com estatísticas**
3. **Gestão de usuários**
4. **Configurações do sistema**

## 🧪 Testes

Os testes do backend cobrem a API de tenants. Testes do frontend podem ser adicionados com Jest/React Testing Library.

## 📚 Documentação

- [API Endpoints](../docs/API_ENDPOINTS.md)
- [Estrutura do Projeto](../docs/STRUCTURE.md)
