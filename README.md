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

O projeto utiliza uma arquitetura monorepo com workspaces:

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

## 🛠️ Tecnologias

- **Backend**: Node.js, TypeScript
- **Frontend**: React/Next.js
- **Database**: PostgreSQL (multi-tenant)
- **CI/CD**: GitHub Actions
- **Package Manager**: npm workspaces + Turbo

## 📋 Pré-requisitos

- Node.js >= 18.0.0
- npm >= 9.0.0
- PostgreSQL >= 14.0

## 🚀 Instalação

```bash
# Instalar dependências
npm install

# Desenvolvimento
npm run dev

# Build
npm run build

# Testes
npm run test

# Lint
npm run lint
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

