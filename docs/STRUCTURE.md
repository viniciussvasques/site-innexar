# Estrutura do Projeto StructurOne

## Visão Geral

O projeto StructurOne está organizado em **3 partes principais**:

1. **Backend (API)** - Django REST Framework
2. **Frontend (Web)** - Next.js ou Django Templates
3. **Painel Admin** - Django Admin customizado

## 📁 Estrutura de Diretórios

```
structurone/
├── structurone/              # Configurações Django
│   ├── settings.py          # Configurações principais
│   ├── urls.py              # URLs principais (roteamento)
│   ├── wsgi.py              # WSGI config
│   └── asgi.py              # ASGI config
│
├── apps/                     # Aplicações Django
│   ├── core/                # Core app
│   │   ├── urls.py         # API URLs
│   │   ├── views.py        # API Views
│   │   ├── frontend_urls.py # Frontend URLs (Django templates)
│   │   └── frontend_views.py # Frontend Views (Django templates)
│   │
│   ├── admin/               # Painel Admin Customizado
│   │   ├── urls.py         # Admin URLs
│   │   ├── views.py        # Admin Views
│   │   └── admin.py        # Admin customization
│   │
│   ├── tenants/             # Multi-tenant
│   ├── projects/            # Gestão de Projetos
│   │   ├── urls.py         # API: /api/projects/
│   │   └── views.py        # API Views
│   │
│   ├── investors/           # Portal do Investidor
│   │   ├── urls.py         # API: /api/investors/
│   │   └── views.py        # API Views
│   │
│   ├── financial/           # Gestão Financeira
│   │   ├── urls.py         # API: /api/financial/
│   │   └── views.py        # API Views
│   │
│   ├── documents/           # Upload de Documentos
│   │   ├── urls.py         # API: /api/documents/
│   │   └── views.py        # API Views
│   │
│   └── updates/             # Atualizações de Obra
│       ├── urls.py         # API: /api/updates/
│       └── views.py        # API Views
│
├── frontend/                 # Frontend Web (Next.js)
│   ├── src/                 # Código fonte
│   ├── public/              # Arquivos públicos
│   └── package.json          # Dependências
│
├── templates/                # Templates Django (se usar Django templates)
│   ├── admin/               # Templates do Admin
│   └── frontend/            # Templates do Frontend
│
├── static/                   # Arquivos estáticos
├── media/                    # Arquivos de mídia
├── locale/                   # Traduções i18n
└── docs/                     # Documentação
```

## 🔌 Backend (API)

### Localização
- **Diretório**: `apps/*/`
- **URL Base**: `http://localhost:8000/api/`
- **Framework**: Django REST Framework

### Endpoints Principais

#### Autenticação
- `POST /api/auth/token/` - Obter token JWT
- `POST /api/auth/token/refresh/` - Atualizar token

#### Projetos
- `GET /api/projects/` - Listar projetos
- `POST /api/projects/` - Criar projeto
- `GET /api/projects/{id}/` - Detalhes do projeto
- `PUT /api/projects/{id}/` - Atualizar projeto
- `DELETE /api/projects/{id}/` - Deletar projeto

#### Investidores
- `GET /api/investors/` - Listar investidores
- `POST /api/investors/` - Criar investidor
- `GET /api/investors/{id}/` - Detalhes do investidor
- `GET /api/investors/{id}/investments/` - Investimentos do investidor

#### Financeiro
- `GET /api/financial/transactions/` - Listar transações
- `POST /api/financial/transactions/` - Criar transação
- `GET /api/financial/cashflow/` - Fluxo de caixa

#### Documentos
- `GET /api/documents/` - Listar documentos
- `POST /api/documents/upload/` - Upload de documento
- `GET /api/documents/{id}/` - Detalhes do documento

#### Atualizações
- `GET /api/updates/` - Listar atualizações
- `POST /api/updates/` - Criar atualização
- `GET /api/updates/project/{id}/` - Atualizações do projeto

### Desenvolvimento Backend

```bash
# Executar servidor
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser
```

## 🌐 Frontend (Web)

### Opção 1: Next.js (Recomendado)

**Localização**: `frontend/`

**Características**:
- Frontend separado do backend
- Consome API REST do Django
- Autenticação via JWT
- React + Next.js

**Setup**:
```bash
cd frontend
npm install
npm run dev
# Acessa em http://localhost:3000
```

### Opção 2: Django Templates

**Localização**: `templates/frontend/` e `apps/core/frontend_views.py`

**Características**:
- Frontend integrado ao Django
- Templates server-side
- Pode usar HTMX/Alpine.js para interatividade

**URLs**: Configuradas em `apps/core/frontend_urls.py`

## 👨‍💼 Painel Admin

### Localização
- **URL**: `http://localhost:8000/admin/`
- **Custom Admin**: `http://localhost:8000/admin-panel/`
- **Código**: `apps/admin/`

### Funcionalidades

1. **Dashboard Admin** (`/admin-panel/`)
   - Visão geral do sistema
   - Estatísticas

2. **Gestão de Tenants** (`/admin-panel/tenants/`)
   - Listar todos os tenants
   - Detalhes do tenant
   - Criar/editar tenants

3. **Gestão de Usuários** (`/admin-panel/users/`)
   - Listar usuários
   - Gerenciar permissões

4. **Configurações** (`/admin-panel/settings/`)
   - Configurações do sistema

### Acesso
- Requer permissão de staff (`is_staff=True`)
- Usa Django Admin padrão + customizações

## 🔄 Fluxo de Dados

```
┌─────────────┐
│   Frontend  │ (Next.js ou Django Templates)
│  (Web App)  │
└──────┬──────┘
       │ HTTP/REST
       │ JWT Auth
       ▼
┌─────────────┐
│   Backend   │ (Django REST API)
│     API     │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│  PostgreSQL │ (Database)
└─────────────┘

┌─────────────┐
│ Admin Panel │ (Django Admin)
│  (Staff)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│   Backend   │ (Django REST API)
│     API     │
└─────────────┘
```

## 🚀 Desenvolvimento

### Backend
```bash
# Ativar ambiente virtual
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt

# Executar servidor
python manage.py runserver
# API disponível em http://localhost:8000/api/
```

### Frontend (Next.js)
```bash
cd frontend
npm install
npm run dev
# Frontend disponível em http://localhost:3000
```

### Admin Panel
```bash
# Acessar Django Admin
# http://localhost:8000/admin/

# Acessar Custom Admin
# http://localhost:8000/admin-panel/
```

## 📝 Próximos Passos

1. ✅ Estrutura criada
2. ⏳ Implementar modelos (Models)
3. ⏳ Implementar serializers (DRF)
4. ⏳ Implementar viewsets completos
5. ⏳ Setup do frontend Next.js
6. ⏳ Customizar painel admin
7. ⏳ Implementar autenticação JWT
8. ⏳ Configurar multi-tenant

