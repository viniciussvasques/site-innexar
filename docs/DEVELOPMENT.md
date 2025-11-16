# Guia de Desenvolvimento

## Setup Inicial

### Pré-requisitos

- Node.js >= 18.0.0
- npm >= 9.0.0
- PostgreSQL >= 14.0
- Git

### Instalação

```bash
# Clonar repositório
git clone https://github.com/viniciussvasques/structurone.git
cd structurone

# Instalar dependências
npm install

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações
```

## Scripts Disponíveis

### Root Level

- `npm run dev` - Inicia todos os pacotes em modo desenvolvimento
- `npm run build` - Build de todos os pacotes
- `npm run test` - Executa testes
- `npm run lint` - Executa linter
- `npm run type-check` - Verifica tipos TypeScript
- `npm run format` - Formata código com Prettier

### Por Pacote

Cada pacote possui seus próprios scripts. Consulte o `package.json` de cada um.

## Convenções de Código

### TypeScript

- Sempre use TypeScript
- Evite `any` - use tipos específicos
- Use interfaces para objetos
- Use enums para constantes relacionadas

### Nomenclatura

- **Arquivos**: kebab-case (`user-service.ts`)
- **Componentes**: PascalCase (`UserProfile.tsx`)
- **Funções/Variáveis**: camelCase (`getUserData`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_FILE_SIZE`)
- **Tipos/Interfaces**: PascalCase (`UserData`)

### Estrutura de Pastas

```
src/
├── components/     # Componentes reutilizáveis
├── pages/         # Páginas (Next.js)
├── services/      # Serviços e APIs
├── hooks/         # Custom hooks
├── utils/         # Funções utilitárias
├── types/         # Definições de tipos
└── constants/     # Constantes
```

## Git Workflow

### Branches

- `main` - Produção
- `develop` - Desenvolvimento
- `feature/*` - Novas funcionalidades
- `fix/*` - Correções de bugs
- `hotfix/*` - Correções urgentes

### Commits

Use conventional commits:

```
feat: adiciona autenticação de usuário
fix: corrige cálculo de percentual de conclusão
docs: atualiza documentação da API
refactor: reorganiza estrutura de pastas
test: adiciona testes para módulo de investimentos
```

## Testes

- Unitários: Jest ou Vitest
- Integração: Supertest
- E2E: Playwright ou Cypress

## Code Review

- Todas as mudanças devem passar por code review
- Mantenha PRs pequenos e focados
- Inclua testes para novas funcionalidades
- Atualize documentação quando necessário

## Performance

- Use lazy loading quando apropriado
- Otimize imagens e assets
- Implemente cache quando necessário
- Monitore performance em produção

## Segurança

- Nunca commite secrets ou tokens
- Valide todas as entradas
- Use prepared statements para queries
- Implemente rate limiting
- Mantenha dependências atualizadas

