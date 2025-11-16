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

- **Backend**: Django 5.0+ + Python 3.11+
- **API**: Django REST Framework
- **Frontend**: Next.js (separado) ou Django Templates
- **Database**: PostgreSQL (multi-tenant)
- **CI/CD**: GitHub Actions
- **Multi-tenant**: django-tenants

## Estrutura de Diretórios

```
structurone/
├── structurone/      # Configurações Django
├── apps/             # Aplicações Django
│   ├── core/        # Core app
│   ├── tenants/     # Multi-tenant
│   ├── projects/    # Gestão de projetos
│   ├── investors/   # Portal do investidor
│   ├── financial/    # Gestão financeira
│   ├── documents/   # Upload de documentos
│   └── updates/     # Atualizações de obra
├── static/          # Arquivos estáticos
├── media/           # Arquivos de mídia
├── templates/       # Templates Django
├── locale/          # Traduções i18n
├── .github/
│   └── workflows/   # CI/CD
└── docs/            # Documentação
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

- **Linguagem**: Python 3.11+
- **Formatação**: Black
- **Linting**: Flake8
- **Imports**: isort
- **Commits**: Conventional Commits
- **Branches**: Git Flow
- **Testes**: pytest + pytest-django

## Configurações

- **Python**: >= 3.11
- **Django**: >= 5.0.0
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

