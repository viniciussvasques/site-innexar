# 🗺️ Roadmap de Desenvolvimento - StructurOne

## 📊 Status Atual

### ✅ Concluído

- [x] Estrutura do projeto (Backend, Admin, Frontend)
- [x] Sistema Multi-tenant completo
- [x] Gerenciador de Tenants (Backend + Admin)
- [x] Autenticação JWT no Admin
- [x] Docker Compose configurado
- [x] CI/CD básico

---

## 🎯 Próxima Fase: Frontend do Tenant (Prioridade 1)

### Por que começar pelo Frontend?

1. **Experiência do Usuário**: É a primeira interface que os tenants (construtoras) vão usar
2. **Base para tudo**: Autenticação e onboarding são fundamentais
3. **Validação rápida**: Permite testar o fluxo completo desde o início
4. **Dependências**: Outros módulos dependem de usuários autenticados

### 📋 Fase 1: Autenticação e Onboarding (Sprint 1)

#### 1.1 Backend - Autenticação de Usuários do Tenant

- [ ] Model `User` com relacionamento com `Tenant`
- [ ] Serializers para registro/login
- [ ] Endpoints:
  - `POST /api/auth/register/` - Registro de usuário do tenant
  - `POST /api/auth/login/` - Login (já existe, ajustar para tenants)
  - `POST /api/auth/logout/` - Logout
  - `POST /api/auth/refresh/` - Refresh token
  - `GET /api/auth/me/` - Dados do usuário logado
  - `POST /api/auth/password/reset/` - Reset de senha
- [ ] Middleware para identificar tenant do usuário
- [ ] Permissões baseadas em tenant
- [ ] Testes completos

#### 1.2 Frontend - Páginas de Autenticação

- [ ] Estrutura Next.js do frontend
- [ ] Layout base (Header, Sidebar, Footer)
- [ ] Página de Login (`/login`)
  - Design moderno e responsivo
  - Integração com API
  - Tratamento de erros
  - Loading states
- [ ] Página de Registro (`/register`)
  - Formulário de cadastro
  - Validação de campos
  - Seleção/validação de tenant (slug)
- [ ] Página de Recuperação de Senha (`/forgot-password`)
- [ ] Proteção de rotas (middleware/componente)
- [ ] Context/Provider para autenticação
- [ ] Integração com API (usar mesma estrutura do admin)

#### 1.3 Frontend - Onboarding

- [ ] Página de Onboarding (`/onboarding`)
  - Passo 1: Informações da Empresa
  - Passo 2: Configuração Inicial
  - Passo 3: Primeiro Projeto (opcional)
  - Passo 4: Convidar Usuários (opcional)
- [ ] Wizard multi-step
- [ ] Validação em cada etapa
- [ ] Progress indicator
- [ ] Salvar progresso (localStorage/API)
- [ ] Pular etapas opcionais

#### 1.4 Frontend - Dashboard Inicial

- [ ] Dashboard básico (`/dashboard`)
  - Cards de resumo
  - Gráficos simples (Chart.js ou similar)
  - Ações rápidas
  - Últimas atualizações
- [ ] Layout responsivo
- [ ] Loading states
- [ ] Empty states

---

### 📋 Fase 2: Módulo de Projetos (Sprint 2)

#### 2.1 Backend - Projetos

- [ ] Model `Project` com relacionamento com `Tenant`
- [ ] Serializers (List, Detail, Create, Update)
- [ ] ViewSet com CRUD completo
- [ ] Endpoints:
  - `GET /api/projects/` - Listar projetos
  - `POST /api/projects/` - Criar projeto
  - `GET /api/projects/{id}/` - Detalhes do projeto
  - `PUT /api/projects/{id}/` - Atualizar projeto
  - `DELETE /api/projects/{id}/` - Deletar projeto
  - `GET /api/projects/{id}/stats/` - Estatísticas
- [ ] Filtros (status, tipo, data)
- [ ] Busca
- [ ] Testes completos

#### 2.2 Admin - Gestão de Projetos

- [ ] Lista de projetos
- [ ] Formulário de criação/edição
- [ ] Visualização de detalhes
- [ ] Filtros e busca

#### 2.3 Frontend - Gestão de Projetos

- [ ] Lista de projetos (`/projects`)
- [ ] Detalhes do projeto (`/projects/[id]`)
- [ ] Criar projeto (`/projects/new`)
- [ ] Editar projeto (`/projects/[id]/edit`)
- [ ] Cards/Grid responsivo
- [ ] Filtros e busca
- [ ] Paginação

---

### 📋 Fase 3: Portal do Investidor (Sprint 3)

#### 3.1 Backend - Investidores

- [ ] Model `Investor` com relacionamento com `Tenant` e `Project`
- [ ] Serializers
- [ ] ViewSet
- [ ] Endpoints para investidor visualizar seus projetos
- [ ] Permissões específicas para investidores
- [ ] Testes

#### 3.2 Frontend - Portal do Investidor

- [ ] Dashboard do investidor (`/investor/dashboard`)
- [ ] Lista de projetos investidos
- [ ] Detalhes do projeto (visualização)
- [ ] Relatórios e gráficos

---

### 📋 Fase 4: Atualizações de Obra (Sprint 4)

#### 4.1 Backend - Atualizações

- [ ] Model `Update` com relacionamento com `Project`
- [ ] Upload de fotos/vídeos
- [ ] Serializers
- [ ] ViewSet
- [ ] Endpoints
- [ ] Testes

#### 4.2 Frontend - Atualizações

- [ ] Timeline de atualizações
- [ ] Criar atualização
- [ ] Upload de mídia
- [ ] Galeria de fotos

---

### 📋 Fase 5: Gestão Financeira (Sprint 5)

#### 5.1 Backend - Financeiro

- [ ] Model `Transaction` (entrada/saída)
- [ ] Model `Budget`
- [ ] Serializers
- [ ] ViewSet
- [ ] Cálculos automáticos
- [ ] Relatórios
- [ ] Testes

#### 5.2 Frontend - Financeiro

- [ ] Dashboard financeiro
- [ ] Registro de transações
- [ ] Fluxo de caixa
- [ ] Gráficos e relatórios

---

### 📋 Fase 6: Documentos (Sprint 6)

#### 6.1 Backend - Documentos

- [ ] Model `Document`
- [ ] Upload de arquivos
- [ ] Categorização
- [ ] Serializers
- [ ] ViewSet
- [ ] Testes

#### 6.2 Frontend - Documentos

- [ ] Lista de documentos
- [ ] Upload
- [ ] Visualização
- [ ] Download

---

## 🎨 Padrões e Boas Práticas

### Frontend (Next.js)

- **Estrutura de pastas**:

  ```
  frontend/
  ├── src/
  │   ├── app/              # App Router (Next.js 14+)
  │   │   ├── (auth)/       # Rotas de autenticação
  │   │   ├── (dashboard)/  # Rotas protegidas
  │   │   └── layout.tsx
  │   ├── components/       # Componentes reutilizáveis
  │   ├── lib/              # Utilitários, API client
  │   ├── hooks/            # Custom hooks
  │   ├── contexts/         # React Contexts
  │   ├── types/            # TypeScript types
  │   └── styles/           # Estilos globais
  ├── public/               # Arquivos estáticos
  └── package.json
  ```

- **Componentes**:

  - Reutilizáveis e modulares
  - TypeScript para type safety
  - Styled Components ou Tailwind CSS
  - Responsive design

- **API Client**:

  - Centralizar chamadas API (similar ao admin)
  - Interceptors para JWT
  - Error handling
  - Loading states

- **Autenticação**:
  - Context API para estado global
  - Proteção de rotas
  - Refresh token automático
  - Logout em caso de erro 401

### Backend (Django)

- **Padrões existentes**:
  - Seguir estrutura do módulo `tenants`
  - Serializers separados (List, Detail, Create)
  - ViewSets com permissões
  - Testes para cada módulo
  - Multi-tenant em todos os models

---

## 📅 Estimativa de Tempo

### Sprint 1 (Autenticação + Onboarding)

- **Backend**: 2-3 dias
- **Frontend**: 3-4 dias
- **Total**: ~1 semana

### Sprint 2 (Projetos)

- **Backend**: 2-3 dias
- **Admin**: 1-2 dias
- **Frontend**: 3-4 dias
- **Total**: ~1 semana

### Sprint 3-6

- Cada sprint: ~1 semana
- Total estimado: ~6 semanas para MVP completo

---

## 🚀 Próximos Passos Imediatos

1. **Decisão**: Confirmar se começamos pelo Frontend (recomendado)
2. **Backend - Autenticação**: Implementar User model e endpoints
3. **Frontend - Estrutura**: Criar estrutura base do Next.js
4. **Frontend - Login**: Implementar página de login
5. **Frontend - Onboarding**: Criar fluxo de onboarding

---

## 📝 Notas

- Cada módulo deve ser 100% funcional antes de passar para o próximo
- Testes são obrigatórios em cada etapa
- Documentação deve ser atualizada conforme desenvolvimento
- Commits seguem Conventional Commits
- Code review antes de merge
