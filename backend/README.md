# Backend API - StructurOne

Backend Django REST Framework para a plataforma StructurOne.

## 🚀 Início Rápido

```bash
# Entrar na pasta backend
cd backend

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

# Executar servidor
python manage.py runserver
```

## 📡 API Endpoints

Base URL: `http://localhost:8010/api/`

### Autenticação
- `POST /api/auth/token/` - Obter token JWT
- `POST /api/auth/token/refresh/` - Atualizar token

### Projetos
- `GET /api/projects/` - Listar projetos
- `POST /api/projects/` - Criar projeto
- `GET /api/projects/{id}/` - Detalhes do projeto

### Investidores
- `GET /api/investors/` - Listar investidores
- `POST /api/investors/` - Criar investidor

### Financeiro
- `GET /api/financial/transactions/` - Listar transações
- `GET /api/financial/cashflow/` - Fluxo de caixa

### Documentos
- `GET /api/documents/` - Listar documentos
- `POST /api/documents/upload/` - Upload de documento

### Atualizações
- `GET /api/updates/` - Listar atualizações
- `POST /api/updates/` - Criar atualização

## 📁 Estrutura

```
backend/
├── structurone/          # Configurações Django
│   ├── settings.py      # Settings
│   ├── urls.py          # URLs da API
│   ├── wsgi.py          # WSGI
│   └── asgi.py          # ASGI
├── apps/                 # Aplicações Django
│   ├── core/            # Core app
│   ├── tenants/         # Multi-tenant
│   ├── projects/        # API Projects
│   ├── investors/       # API Investors
│   ├── financial/       # API Financial
│   ├── documents/       # API Documents
│   └── updates/         # API Updates
├── manage.py             # Django management
├── requirements.txt      # Dependências
└── .env.example          # Exemplo de variáveis
```

## 🔧 Comandos

```bash
# Executar servidor
python manage.py runserver

# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Shell Django
python manage.py shell
```

## 📚 Documentação

Veja a documentação completa da API em `../docs/API_ENDPOINTS.md`

