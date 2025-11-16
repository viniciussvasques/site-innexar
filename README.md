# StructurOne

> Plataforma SaaS para gestão completa de empreendimentos, captação de investimentos e transparência total para construtoras e investidores.

## 🎯 Sobre o Projeto

O **StructurOne** é uma plataforma SaaS desenvolvida pela **Innexar** que centraliza informações, automatiza relatórios e oferece dashboards intuitivos para cada cliente, garantindo confiança e eficiência na gestão de obras e investimentos.

## 🚀 Funcionalidades Principais

- **Multi-tenant**: Cada cliente possui sua própria estrutura, dados e dashboard isolados
- **Gestão de Projetos**: Cadastro e acompanhamento de empreendimentos
- **Portal do Investidor**: Acompanhamento em tempo real de investimentos
- **Gestão Financeira**: Entradas, saídas, fluxo de caixa e orçamentos
- **Documentos**: Upload e gestão de contratos, notas fiscais e comprovantes
- **Atualizações de Obra**: Fotos, vídeos e percentuais de conclusão
- **Relatórios Automáticos**: Relatórios auditáveis e automatizados
- **Internacionalização**: Suporte para Português, Inglês e Espanhol

## 🏗️ Arquitetura

O projeto está **separado em 3 partes principais**:

### 1. 🔌 Backend (API)
- **Framework**: Django REST Framework
- **URL**: `http://localhost:8000/api/`
- **Localização**: `apps/*/`
- **Autenticação**: JWT

### 2. 🌐 Frontend (Web)
- **Opção 1**: Next.js (recomendado) - `frontend/`
- **Opção 2**: Django Templates - `templates/frontend/`
- **URL**: `http://localhost:3000` (Next.js) ou integrado ao Django

### 3. 👨‍💼 Painel Admin
- **Framework**: Django Admin customizado
- **URL**: `http://localhost:8000/admin/` (Django Admin padrão)
- **URL**: `http://localhost:8000/admin-panel/` (Custom Admin)
- **Localização**: `apps/admin/`

```
structurone/
├── structurone/          # Configurações Django
├── apps/                 # Aplicações Django
│   ├── core/            # Core app (API + Frontend URLs)
│   ├── admin/           # Painel Admin Customizado
│   ├── tenants/         # Multi-tenant
│   ├── projects/        # API: /api/projects/
│   ├── investors/       # API: /api/investors/
│   ├── financial/       # API: /api/financial/
│   ├── documents/       # API: /api/documents/
│   └── updates/         # API: /api/updates/
├── frontend/             # Frontend Next.js (quando implementado)
├── templates/            # Templates Django
│   ├── admin/           # Templates do Admin
│   └── frontend/        # Templates do Frontend
├── static/               # Arquivos estáticos
├── media/                # Arquivos de mídia
└── docs/                 # Documentação
```

📖 **Documentação completa**: Veja [docs/STRUCTURE.md](docs/STRUCTURE.md)

## 🛠️ Tecnologias

- **Backend**: Django 5.0+, Python 3.11+
- **API**: Django REST Framework
- **Database**: PostgreSQL (multi-tenant)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Multi-tenant**: django-tenants
- **CI/CD**: GitHub Actions
- **Frontend**: Next.js (separado) ou Django Templates

## 📋 Pré-requisitos

- Python >= 3.11
- PostgreSQL >= 14.0
- pip >= 23.0

## 🚀 Instalação

### Backend (API)

```bash
# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor de desenvolvimento
python manage.py runserver
# API disponível em http://localhost:8000/api/
# Admin disponível em http://localhost:8000/admin/
```

### Frontend (Next.js - quando implementado)

```bash
cd frontend
npm install
npm run dev
# Frontend disponível em http://localhost:3000
```

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

Para mais informações, consulte a documentação em `/docs`.

