# Arquitetura do StructurOne

## Visão Geral

O StructurOne utiliza uma arquitetura **monorepo** com **multi-tenant** para suportar múltiplos clientes de forma isolada e segura.

## Estrutura do Projeto

```
structurone/
├── packages/
│   ├── api/              # Backend API (Node.js + Express)
│   ├── web/              # Frontend (Next.js)
│   ├── shared/           # Código compartilhado (types, utils)
│   └── database/         # Schemas e migrações
├── .github/
│   └── workflows/        # CI/CD pipelines
└── docs/                 # Documentação
```

## Multi-Tenant Strategy

### Opções de Implementação

1. **Schema-based**: Cada tenant possui seu próprio schema no PostgreSQL
2. **Row-based**: Todos os tenants compartilham o mesmo schema, com isolamento por `tenant_id`

### Recomendação Inicial

Para o MVP, recomenda-se **Row-based** por simplicidade, com migração futura para **Schema-based** se necessário para escalabilidade.

## Stack Tecnológica

### Backend
- **Runtime**: Node.js 18+
- **Language**: TypeScript
- **Framework**: Express.js (ou Fastify)
- **Database**: PostgreSQL
- **ORM**: Prisma ou TypeORM
- **Authentication**: JWT + OAuth2

### Frontend
- **Framework**: Next.js 14+
- **Language**: TypeScript
- **Styling**: Tailwind CSS ou styled-components
- **State Management**: Zustand ou React Query
- **i18n**: next-i18next ou react-i18next

### DevOps
- **CI/CD**: GitHub Actions
- **Containerization**: Docker
- **Deployment**: VPS (conforme preferência do usuário)

## Fluxo de Dados

```
User → Frontend (Next.js) → API (Express) → Database (PostgreSQL)
                                    ↓
                            Multi-tenant Middleware
                                    ↓
                            Tenant Isolation Layer
```

## Segurança

- Autenticação JWT
- Isolamento de dados por tenant
- Validação de entrada (Zod ou Yup)
- Rate limiting
- CORS configurado
- HTTPS obrigatório em produção

## Internacionalização

- Suporte para PT-BR, EN-US, ES-ES
- Arquivos de tradução em JSON
- Detecção automática de idioma
- Seleção manual no dashboard

## Próximos Passos

1. Definir estratégia de multi-tenant (row vs schema)
2. Setup do banco de dados
3. Implementar autenticação
4. Criar estrutura de rotas da API
5. Desenvolver componentes base do frontend

