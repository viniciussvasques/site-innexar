# StructurOne

> Plataforma SaaS para gestão completa de empreendimentos, captação de investimentos e transparência total para construtoras e investidores.

## 🎯 Sobre o Projeto

O **StructurOne** é uma plataforma SaaS desenvolvida pela **Innexar** que centraliza informações, automatiza relatórios e oferece dashboards intuitivos para cada cliente, garantindo confiança e eficiência na gestão de obras e investimentos.

## 🏗️ Estrutura do Projeto

O projeto está **organizado em 3 partes principais**, cada uma em sua própria pasta:

### 1. 🔌 Backend (API)
- **Localização**: `backend/`
- **Framework**: Django REST Framework
- **URL**: `http://localhost:8000/api/`
- **Documentação**: [backend/README.md](backend/README.md)

### 2. 👨‍💼 Painel Admin
- **Localização**: `admin/`
- **Framework**: Django Admin customizado
- **URL**: `http://localhost:8000/admin/`
- **Documentação**: [admin/README.md](admin/README.md)

### 3. 🌐 Frontend (Web)
- **Localização**: `frontend/`
- **Framework**: Next.js
- **URL**: `http://localhost:3000`
- **Documentação**: [frontend/README.md](frontend/README.md)

```
structurone/
├── backend/              # Backend API (Django REST)
│   ├── structurone/     # Configurações Django
│   ├── apps/            # Aplicações Django
│   ├── manage.py        # Django management
│   └── requirements.txt # Dependências Python
│
├── admin/                # Painel Admin
│   ├── apps/            # Apps do admin
│   └── templates/       # Templates do admin
│
├── frontend/             # Frontend Web (Next.js)
│   ├── src/             # Código fonte
│   ├── public/          # Arquivos públicos
│   └── package.json     # Dependências Node
│
└── docs/                 # Documentação
```

## 🚀 Início Rápido

### Opção 1: Docker Compose (Recomendado) 🐳

```bash
# Construir e iniciar todos os serviços
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Criar superusuário
docker-compose exec backend python manage.py createsuperuser

# Criar tenants de teste
docker-compose exec backend python test_tenant_local.py
```

**Serviços disponíveis:**
- Backend API: http://localhost:8000/api/
- Django Admin: http://localhost:8000/admin/
- Admin Panel: http://localhost:3001
- Frontend: http://localhost:3000 (quando implementado)

📖 **Guia completo**: Veja [README_DOCKER.md](README_DOCKER.md)

### Opção 2: Instalação Manual

#### 1. Backend (API)

```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt
cp .env.example .env
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
# API: http://localhost:8000/api/
```

#### 2. Frontend (Web)

```bash
cd frontend
npm install
npm run dev
# Frontend: http://localhost:3000
```

#### 3. Admin Panel (Next.js)

```bash
cd admin
npm install
cp .env.example .env.local
npm run dev
# Admin: http://localhost:3001
```

## 🛠️ Tecnologias

- **Backend**: Django 5.0+, Python 3.11+
- **API**: Django REST Framework
- **Frontend**: Next.js 14+, React, TypeScript
- **Database**: PostgreSQL (multi-tenant)
- **Authentication**: JWT
- **CI/CD**: GitHub Actions

## 📋 Pré-requisitos

- Python >= 3.11
- Node.js >= 18.0.0
- PostgreSQL >= 14.0
- npm >= 9.0.0

## 📚 Documentação

- [Estrutura do Projeto](docs/STRUCTURE.md)
- [API Endpoints](docs/API_ENDPOINTS.md)
- [Arquitetura](docs/ARCHITECTURE.md)
- [Guia de Desenvolvimento](docs/DEVELOPMENT.md)
- [MVP](docs/MVP.md)

## 🌍 Internacionalização

O projeto suporta três idiomas:
- 🇧🇷 Português (PT-BR)
- 🇺🇸 Inglês (EN-US)
- 🇪🇸 Espanhol (ES-ES)

## 📝 Licença

UNLICENSED - Propriedade da Innexar

## 👥 Desenvolvido por

**Innexar**

---

Para mais informações, consulte a documentação em `/docs` ou os READMEs de cada parte do projeto.
