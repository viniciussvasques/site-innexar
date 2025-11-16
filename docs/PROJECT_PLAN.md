# Plano do Projeto StructurOne

## Informações do Projeto

- **Empresa**: Innexar
- **Produto**: StructurOne
- **Tipo**: Plataforma SaaS Multi-tenant
- **Repositório**: https://github.com/viniciussvasques/structurone

## Objetivo

Plataforma SaaS para gestão completa de empreendimentos, captação de investimentos e transparência total para construtoras e investidores.

## Público-alvo

- Construtoras e incorporadoras (pequeno, médio e grande porte)
- Investidores que desejam acompanhar seus aportes de forma transparente

## Funcionalidades Principais

1. **Multi-tenant**: Isolamento completo de dados por cliente
2. **Gestão de Projetos**: Cadastro e acompanhamento de empreendimentos
3. **Portal do Investidor**: Acompanhamento em tempo real
4. **Gestão Financeira**: Entradas, saídas, fluxo de caixa, orçamentos
5. **Documentos**: Upload e gestão de contratos, notas fiscais, comprovantes
6. **Atualizações de Obra**: Fotos, vídeos, percentuais de conclusão
7. **Relatórios Automáticos**: Relatórios auditáveis e automatizados
8. **Internacionalização**: PT-BR, EN-US, ES-ES

## Arquitetura

- **Monorepo** com workspaces (npm)
- **Backend**: Node.js + TypeScript + Express
- **Frontend**: Next.js + React + TypeScript
- **Database**: PostgreSQL (multi-tenant)
- **CI/CD**: GitHub Actions
- **Build Tool**: Turbo

## Estrutura de Diretórios

```
structurone/
├── packages/
│   ├── api/          # Backend API
│   ├── web/          # Frontend Web
│   ├── shared/       # Código compartilhado
│   └── database/     # Schemas e migrações
├── .github/
│   └── workflows/    # CI/CD
└── docs/             # Documentação
```

## Roadmap MVP

### Fase 1: Fundação (Semanas 1-2)
- Setup do projeto
- Configuração do banco de dados
- Autenticação básica
- Estrutura multi-tenant

### Fase 2: Core Features (Semanas 3-4)
- Cadastro de projetos
- Dashboard da empresa
- Portal do investidor básico

### Fase 3: Funcionalidades (Semanas 5-6)
- Atualizações de obra
- Gestão financeira simplificada
- Upload de documentos básico

### Fase 4: Polimento (Semanas 7-8)
- Internacionalização
- Testes básicos
- Ajustes de UI/UX
- Documentação

## Padrões e Convenções

- **Linguagem**: TypeScript
- **Formatação**: Prettier
- **Linting**: ESLint
- **Commits**: Conventional Commits
- **Branches**: Git Flow
- **Testes**: Jest/Vitest

## Configurações

- **Node.js**: >= 18.0.0
- **npm**: >= 9.0.0
- **PostgreSQL**: >= 14.0
- **Deployment**: VPS (conforme preferência)

## Próximos Passos

1. ✅ Estrutura do projeto criada
2. ✅ CI/CD configurado
3. ⏳ Setup do banco de dados
4. ⏳ Implementação da autenticação
5. ⏳ Desenvolvimento do MVP

## Links Úteis

- [Arquitetura](./ARCHITECTURE.md)
- [Guia de Desenvolvimento](./DEVELOPMENT.md)
- [MVP](./MVP.md)

