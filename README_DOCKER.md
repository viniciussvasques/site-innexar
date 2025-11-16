# 🐳 Docker Setup - StructurOne

Guia completo para rodar o StructurOne com Docker Compose.

## 📋 Pré-requisitos

- Docker >= 20.10
- Docker Compose >= 2.0

## 🚀 Início Rápido

### 1. Clonar e Configurar

```bash
# Copiar arquivo de exemplo de variáveis
cp backend/.env.example backend/.env

# Editar backend/.env com suas configurações (opcional)
# As configurações padrão funcionam para desenvolvimento
```

### 2. Iniciar Todos os Serviços

```bash
# Construir e iniciar todos os containers
docker-compose up -d --build

# Ver logs
docker-compose logs -f

# Ver logs de um serviço específico
docker-compose logs -f backend
docker-compose logs -f admin
```

### 3. Acessar os Serviços

- **Backend API**: http://localhost:8010/api/
- **Django Admin**: http://localhost:8010/admin/
- **Admin Panel**: http://localhost:3011
- **Frontend**: http://localhost:3010 (quando implementado)
- **PostgreSQL**: localhost:5433

### 4. Criar Superusuário

```bash
# Executar comando no container
docker-compose exec backend python manage.py createsuperuser

# Ou usar o script de teste (cria admin/admin123 automaticamente)
docker-compose exec backend python test_tenant_local.py
```

## 📦 Serviços

### Backend (Django)
- **Container**: `structurone_backend`
- **Porta**: 8000
- **Comando**: `python manage.py runserver` (dev) ou `gunicorn` (prod)

### Admin (Next.js)
- **Container**: `structurone_admin`
- **Porta**: 3001
- **Comando**: `npm run dev`

### Frontend (Next.js)
- **Container**: `structurone_frontend`
- **Porta**: 3000
- **Comando**: `npm run dev`
- **Nota**: Só inicia com `--profile frontend`

### PostgreSQL
- **Container**: `structurone_db`
- **Porta**: 5432
- **Volume**: `postgres_data`

## 🔧 Comandos Úteis

### Gerenciamento de Containers

```bash
# Iniciar serviços
docker-compose up -d

# Parar serviços
docker-compose down

# Parar e remover volumes (⚠️ apaga dados)
docker-compose down -v

# Reiniciar um serviço
docker-compose restart backend

# Reconstruir um serviço
docker-compose up -d --build backend
```

### Executar Comandos

```bash
# Django shell
docker-compose exec backend python manage.py shell

# Criar migrações
docker-compose exec backend python manage.py makemigrations

# Aplicar migrações
docker-compose exec backend python manage.py migrate

# Coletar arquivos estáticos
docker-compose exec backend python manage.py collectstatic

# Testes
docker-compose exec backend python manage.py test

# Criar tenants de teste
docker-compose exec backend python test_tenant_local.py
```

### Logs

```bash
# Todos os logs
docker-compose logs -f

# Logs de um serviço
docker-compose logs -f backend
docker-compose logs -f admin
docker-compose logs -f db
```

### Acessar Container

```bash
# Shell do backend
docker-compose exec backend bash

# Shell do admin
docker-compose exec admin sh

# PostgreSQL
docker-compose exec db psql -U postgres -d structurone
```

## 🧪 Testar Multi-Tenant

### 1. Criar Tenants

```bash
docker-compose exec backend python test_tenant_local.py
```

### 2. Testar API

```bash
# Com header X-Tenant-Slug
curl -H "X-Tenant-Slug: empresa-abc" http://localhost:8000/api/tenants/

# Ou usar o script
docker-compose exec backend bash test_api_tenant.sh
```

## 🔄 Desenvolvimento

### Hot Reload

Os volumes estão configurados para hot reload:
- Backend: Código Python atualiza automaticamente
- Admin: Next.js com hot reload
- Frontend: Next.js com hot reload

### Adicionar Dependências

**Backend:**
```bash
# Editar backend/requirements.txt
# Reconstruir
docker-compose up -d --build backend
```

**Admin/Frontend:**
```bash
# Editar package.json
# Reinstalar dentro do container
docker-compose exec admin npm install
# Ou reconstruir
docker-compose up -d --build admin
```

## 🗄️ Banco de Dados

### Backup

```bash
# Backup
docker-compose exec db pg_dump -U postgres structurone > backup.sql

# Restaurar
docker-compose exec -T db psql -U postgres structurone < backup.sql
```

### Acessar PostgreSQL

```bash
# Via psql
docker-compose exec db psql -U postgres -d structurone

# Via cliente externo
# Host: localhost
# Port: 5433
# User: postgres
# Password: postgres (ou a do .env)
# Database: structurone
```

## 🚀 Produção

### Usar Configuração de Produção

```bash
# Usar docker-compose.prod.yml
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

### Variáveis de Ambiente

Criar arquivo `.env` na raiz:

```env
SECRET_KEY=sua-chave-secreta-aqui
DB_PASSWORD=senha-segura
DEBUG=False
ALLOWED_HOSTS=structurone.com,admin.structurone.com,.structurone.com
```

## 🐛 Troubleshooting

### Container não inicia

```bash
# Ver logs
docker-compose logs backend

# Verificar se porta está em uso
netstat -an | grep 8000
```

### Banco de dados não conecta

```bash
# Verificar se PostgreSQL está rodando
docker-compose ps db

# Ver logs do PostgreSQL
docker-compose logs db

# Testar conexão
docker-compose exec backend python manage.py dbshell
```

### Permissões de arquivos

```bash
# Ajustar permissões (Linux/Mac)
sudo chown -R $USER:$USER backend/media backend/staticfiles
```

### Limpar tudo e recomeçar

```bash
# Parar e remover tudo
docker-compose down -v

# Remover imagens
docker-compose down --rmi all

# Reconstruir do zero
docker-compose up -d --build
```

## 📝 Notas

- **Desenvolvimento**: Usa volumes para hot reload
- **Produção**: Usa imagens otimizadas (sem volumes de código)
- **Dados**: Persistem em volumes Docker
- **Rede**: Todos os serviços na mesma rede `structurone_network`

## 🔗 Links Úteis

- [Docker Compose Docs](https://docs.docker.com/compose/)
- [Django Docker Guide](https://docs.djangoproject.com/en/stable/howto/deployment/docker/)
- [Next.js Docker Guide](https://nextjs.org/docs/deployment#docker-image)

