# Estrutura do Projeto StructurOne

## Visão Geral

O projeto StructurOne está **organizado em 3 pastas principais**, cada uma completamente separada:

1. **`backend/`** - Backend API (Django REST Framework)
2. **`admin/`** - Painel Admin (Django Admin customizado)
3. **`frontend/`** - Frontend Web (Next.js)

## 📁 Estrutura de Diretórios

```
structurone/
├── backend/                    # 🔌 Backend API
│   ├── structurone/           # Configurações Django
│   │   ├── settings.py        # Settings do backend
│   │   ├── urls.py            # URLs da API
│   │   ├── wsgi.py            # WSGI
│   │   └── asgi.py            # ASGI
│   ├── apps/                  # Aplicações Django
│   │   ├── core/           # Core app
│   │   ├── core/                # Core app
│   │   ├── tenants/           # Multi-tenant
│   │   ├── projects/          # API: /api/projects/
│   │   ├── investors/         # API: /api/investors/
│   │   ├── financial/         # API: /api/financial/
│   │   ├── documents/         # API: /api/documents/
│   │   └── updates/           # API: /api/updates/
│   ├── manage.py              # Django management
│   ├── requirements.txt        # Dependências Python
│   ├── static/                 # Arquivos estáticos
│   ├── media/                  # Arquivos de mídia
│   └── locale/                 # Traduções i18n
│
├── admin/                      # 👨‍💼 Painel Admin
│   ├── apps/                  # Apps do admin
│   │   └── admin/             # App principal
│   │       ├── urls.py        # URLs do admin
│   │       ├── views.py       # Views do admin
│   │       └── admin.py       # Customização Django Admin
│   ├── templates/              # Templates do admin
│   │   ├── base.html          # Template base
│   │   └── dashboard.html     # Dashboard
│   └── static/                 # Arquivos estáticos do admin
│
├── frontend/                    # 🌐 Frontend Web
│   ├── src/                   # Código fonte (Next.js)
│   ├── public/                # Arquivos públicos
│   ├── package.json           # Dependências Node
│   └── next.config.js         # Configuração Next.js
│
└── docs/                       # 📚 Documentação
    ├── STRUCTURE.md           # Este arquivo
    ├── API_ENDPOINTS.md       # Documentação da API
    ├── ARCHITECTURE.md        # Arquitetura
    └── DEVELOPMENT.md         # Guia de desenvolvimento
```

## 🔌 Backend (API)

### Localização
- **Diretório**: `backend/`
- **URL Base**: `http://localhost:8010/api/`
- **Framework**: Django REST Framework

### Estrutura
```
backend/
├── structurone/          # Configurações Django
├── apps/                 # Aplicações Django
│   ├── core/            # Core app
│   ├── tenants/         # Multi-tenant
│   ├── projects/        # API Projects
│   ├── investors/       # API Investors
│   ├── financial/       # API Financial
│   ├── documents/       # API Documents
│   └── updates/         # API Updates
├── manage.py             # Django management
└── requirements.txt      # Dependências
```

### Comandos
```bash
cd backend
python manage.py runserver
# API: http://localhost:8010/api/
```

## 👨‍💼 Painel Admin

### Localização
- **Diretório**: `admin/`
- **URL**: `http://localhost:8010/admin/` (Django Admin padrão)
- **URL**: `http://localhost:8010/admin-panel/` (Custom Admin)

### Estrutura
```
admin/
├── apps/                # Apps do admin
│   └── admin/           # App principal
├── templates/           # Templates
└── static/              # Arquivos estáticos
```

## 🌐 Frontend (Web)

### Localização
- **Diretório**: `frontend/`
- **URL**: `http://localhost:3010`
- **Framework**: Next.js

### Estrutura
```
frontend/
├── src/                 # Código fonte
├── public/              # Arquivos públicos
└── package.json         # Dependências
```

### Comandos
```bash
cd frontend
npm install
npm run dev
# Frontend: http://localhost:3010
```

## 🔄 Fluxo de Dados

```
┌─────────────┐
│  Frontend   │ (Next.js - frontend/)
│  (Web App)  │
└──────┬──────┘
       │ HTTP/REST
       │ JWT Auth
       ▼
┌─────────────┐
│   Backend   │ (Django REST - backend/)
│     API     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  PostgreSQL │ (Database)
└─────────────┘

┌─────────────┐
│ Admin Panel │ (Django Admin - admin/)
│  (Staff)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │ (Django REST - backend/)
│     API     │
└─────────────┘
```

## 🚀 Desenvolvimento

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
python manage.py runserver
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### Admin
O admin é acessado via backend quando o servidor está rodando.

## 📝 Notas Importantes

1. **Cada parte é independente** - Backend, Admin e Frontend estão em pastas separadas
2. **Backend é a fonte de verdade** - API REST que serve tanto Frontend quanto Admin
3. **Admin pode ser integrado** - Pode rodar junto com o backend ou separado
4. **Frontend consome API** - Next.js faz chamadas HTTP para o backend

## 📚 Documentação Adicional

- [API Endpoints](API_ENDPOINTS.md)
- [Arquitetura](ARCHITECTURE.md)
- [Guia de Desenvolvimento](DEVELOPMENT.md)
