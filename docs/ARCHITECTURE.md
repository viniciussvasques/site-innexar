# Arquitetura do StructurOne

## Visão Geral

O StructurOne utiliza uma arquitetura **monorepo** com **multi-tenant** para suportar múltiplos clientes de forma isolada e segura.

## Estrutura do Projeto

```
structurone/
├── structurone/          # Configurações do projeto Django
│   ├── settings.py      # Configurações
│   ├── urls.py          # URLs principais
│   ├── wsgi.py          # WSGI config
│   └── asgi.py          # ASGI config
├── apps/                 # Aplicações Django
│   ├── core/            # Core app (autenticação, utils)
│   ├── tenants/         # Multi-tenant
│   ├── projects/        # Gestão de projetos
│   ├── investors/       # Portal do investidor
│   ├── financial/       # Gestão financeira
│   ├── documents/       # Upload de documentos
│   └── updates/         # Atualizações de obra
├── static/              # Arquivos estáticos
├── media/               # Arquivos de mídia
├── templates/           # Templates Django
├── locale/              # Traduções i18n
├── .github/
│   └── workflows/       # CI/CD pipelines
└── docs/                # Documentação
```

## Multi-Tenant Strategy

### Opções de Implementação

1. **Schema-based**: Cada tenant possui seu próprio schema no PostgreSQL
2. **Row-based**: Todos os tenants compartilham o mesmo schema, com isolamento por `tenant_id`

### Recomendação Inicial

Para o MVP, recomenda-se **Row-based** por simplicidade, com migração futura para **Schema-based** se necessário para escalabilidade.

## Stack Tecnológica

### Backend
- **Runtime**: Python 3.11+
- **Framework**: Django 5.0+
- **API**: Django REST Framework
- **Database**: PostgreSQL
- **ORM**: Django ORM
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Multi-tenant**: django-tenants

### Frontend
- **Opção 1**: Next.js 14+ (separado, consumindo API REST)
- **Opção 2**: Django Templates + HTMX/Alpine.js
- **Styling**: Tailwind CSS ou Bootstrap
- **i18n**: Django i18n (gettext)

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Deployment**: VPS (conforme preferência do usuário)
- **WSGI Server**: Gunicorn

## Fluxo de Dados

```
User → Frontend (Next.js ou Django Templates) → Django REST API → Database (PostgreSQL)
                                                          ↓
                                                  Multi-tenant Middleware
                                                          ↓
                                                  Tenant Isolation Layer
```

## Segurança

- Autenticação JWT (djangorestframework-simplejwt)
- Isolamento de dados por tenant (django-tenants)
- Validação de entrada (Django Forms/Serializers)
- Rate limiting (django-ratelimit)
- CORS configurado (django-cors-headers)
- CSRF protection (Django built-in)
- HTTPS obrigatório em produção

## Internacionalização

- Suporte para PT-BR, EN-US, ES-ES
- Arquivos de tradução .po (gettext)
- Detecção automática de idioma (Django i18n)
- Seleção manual no dashboard
- Middleware de locale configurado

## Próximos Passos

1. ✅ Estrutura Django criada
2. Definir estratégia de multi-tenant (row vs schema)
3. Setup do banco de dados e migrações
4. Implementar autenticação JWT
5. Criar serializers e viewsets da API
6. Desenvolver modelos (Projects, Investors, Financial, etc.)
7. Configurar django-tenants
8. Desenvolver frontend (Next.js ou Django Templates)

