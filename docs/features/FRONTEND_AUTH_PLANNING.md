# Planejamento - Frontend: Módulo de Autenticação/Login

**Data**: 2025-01-16  
**Módulo**: Autenticação e Login  
**Parte**: Frontend (Next.js)  
**Status**: 🟢 Planejamento

---

## 📋 Etapa 1: Planejamento

### O que a feature resolve

O frontend precisa permitir que usuários finais (construtoras e investidores) se registrem, façam login, gerenciem suas contas e completem o onboarding inicial.

### Requisitos Funcionais

1. **Registro de Usuário**
   - Formulário de registro com validação
   - Criação automática de tenant
   - Feedback visual de erros
   - Redirecionamento para onboarding após registro

2. **Login**
   - Formulário de login com email/senha
   - Validação de credenciais
   - Armazenamento seguro de tokens
   - Redirecionamento baseado em status de onboarding

3. **Logout**
   - Botão de logout
   - Limpeza de tokens
   - Invalidação no backend
   - Redirecionamento para login

4. **Renovação Automática de Token**
   - Interceptor para renovar token expirado
   - Retry automático de requisições
   - Logout automático se refresh falhar

5. **Onboarding Multi-step**
   - Wizard de 4 etapas
   - Salvamento de progresso
   - Validação de cada etapa
   - Finalização do onboarding

6. **Reset de Senha**
   - Solicitação de reset
   - Página de confirmação
   - Formulário de nova senha

7. **Proteção de Rotas**
   - Middleware de autenticação
   - Redirecionamento automático
   - Verificação de onboarding

### Requisitos Não Funcionais

- **Performance**: Carregamento inicial < 2s
- **Responsividade**: Mobile-first design
- **Acessibilidade**: WCAG 2.1 AA
- **Segurança**: Tokens em httpOnly cookies ou localStorage seguro
- **UX**: Feedback visual claro, mensagens de erro amigáveis
- **Internacionalização**: Suporte a pt-BR (preparado para expansão)

### Pontos Críticos

1. **Segurança de Tokens**: Armazenamento seguro, renovação automática
2. **Experiência do Usuário**: Fluxo intuitivo, feedback claro
3. **Onboarding**: Processo guiado, salvamento de progresso
4. **Multitenancy**: Isolamento correto de dados por tenant

### Critérios de Aceite

- [ ] Usuário consegue se registrar com sucesso
- [ ] Usuário consegue fazer login
- [ ] Tokens são armazenados e renovados automaticamente
- [ ] Rotas protegidas redirecionam não autenticados
- [ ] Onboarding completo funciona (4 etapas)
- [ ] Logout invalida tokens no backend
- [ ] Reset de senha funciona end-to-end
- [ ] Interface responsiva em mobile e desktop
- [ ] Mensagens de erro são claras e amigáveis
- [ ] Loading states em todas as ações assíncronas

---

## 🎨 Etapa 2: Design da Solução

### Arquitetura

```
Frontend (Next.js)
├── Pages
│   ├── /login
│   ├── /register
│   ├── /forgot-password
│   ├── /reset-password
│   ├── /onboarding
│   └── /dashboard (protegida)
├── Components
│   ├── Auth/
│   │   ├── LoginForm
│   │   ├── RegisterForm
│   │   ├── ForgotPasswordForm
│   │   └── ResetPasswordForm
│   ├── Onboarding/
│   │   ├── OnboardingWizard
│   │   ├── Step1CompanyInfo
│   │   ├── Step2Configuration
│   │   ├── Step3FirstProject
│   │   └── Step4InviteUsers
│   └── Layout/
│       ├── AuthLayout
│       └── DashboardLayout
├── Services
│   ├── api.ts (cliente HTTP)
│   ├── auth.ts (lógica de autenticação)
│   └── storage.ts (gerenciamento de tokens)
├── Hooks
│   ├── useAuth.ts
│   ├── useOnboarding.ts
│   └── useApi.ts
├── Middleware
│   └── auth.ts (proteção de rotas)
└── Utils
    ├── validators.ts
    └── constants.ts
```

### Fluxos de Estado

#### Fluxo de Login
```
[Página Login]
  ↓
[Preencher email/senha]
  ↓
[Validar campos]
  ↓
[POST /api/auth/login/]
  ↓
  ├─ [Erro] → [Mostrar mensagem]
  └─ [Sucesso] → [Salvar tokens]
         ↓
    [Verificar onboarding_completed]
         ↓
    ├─ [false] → [Redirecionar /onboarding]
    └─ [true] → [Redirecionar /dashboard]
```

#### Fluxo de Registro
```
[Página Registro]
  ↓
[Preencher formulário]
  ↓
[Validar campos]
  ↓
[POST /api/auth/register/]
  ↓
  ├─ [Erro] → [Mostrar mensagens]
  └─ [Sucesso] → [Salvar tokens]
         ↓
    [Redirecionar /onboarding]
```

#### Fluxo de Onboarding
```
[Página Onboarding]
  ↓
[Carregar progresso atual]
  ↓
[Etapa 1: Informações da Empresa]
  ↓
[Salvar etapa 1]
  ↓
[Etapa 2: Configuração Inicial]
  ↓
[Salvar etapa 2]
  ↓
[Etapa 3: Primeiro Projeto (opcional)]
  ↓
[Etapa 4: Convidar Usuários (opcional)]
  ↓
[Completar onboarding]
  ↓
[Redirecionar /dashboard]
```

### Diagrama de Componentes

```
┌─────────────────────────────────────┐
│         AuthLayout                  │
│  ┌───────────────────────────────┐ │
│  │      LoginForm                 │ │
│  │  - Email input                 │ │
│  │  - Password input              │ │
│  │  - Submit button               │ │
│  │  - Error messages              │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘

┌─────────────────────────────────────┐
│      OnboardingWizard               │
│  ┌───────────────────────────────┐ │
│  │      StepIndicator             │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │      Step1CompanyInfo         │ │
│  │  - Company name               │ │
│  │  - CNPJ                       │ │
│  │  - Address                    │ │
│  │  - Logo upload                │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │      Step2Configuration       │ │
│  │  - Primary color              │ │
│  │  - Country/Language           │ │
│  │  - Currency/Timezone         │ │
│  │  - Date/Number format         │ │
│  └───────────────────────────────┘ │
│  ┌───────────────────────────────┐ │
│  │      NavigationButtons        │ │
│  │  - Previous                   │ │
│  │  - Next/Save                  │ │
│  │  - Complete                   │ │
│  └───────────────────────────────┘ │
└─────────────────────────────────────┘
```

### Regras de Segurança

1. **Armazenamento de Tokens**
   - Preferir httpOnly cookies (mais seguro)
   - Fallback para localStorage se necessário
   - Nunca expor tokens em logs ou URLs

2. **Renovação de Tokens**
   - Interceptor automático em 401
   - Retry transparente para o usuário
   - Logout automático se refresh falhar

3. **Proteção de Rotas**
   - Middleware Next.js para rotas protegidas
   - Verificação de token em cada requisição
   - Redirecionamento automático

4. **Validação de Formulários**
   - Validação client-side (UX)
   - Validação server-side (segurança)
   - Mensagens de erro claras

---

## 🔧 Etapa 3: Criar Ambiente

### Configuração Inicial

1. **Estrutura de Pastas**
   ```bash
   frontend/
   ├── src/
   │   ├── app/              # Next.js App Router
   │   ├── components/        # Componentes React
   │   ├── services/         # Serviços (API, Auth)
   │   ├── hooks/            # Custom hooks
   │   ├── middleware/       # Middleware Next.js
   │   └── utils/            # Utilitários
   ├── public/              # Arquivos estáticos
   └── package.json
   ```

2. **Dependências Necessárias**
   ```json
   {
     "dependencies": {
       "next": "^14.0.0",
       "react": "^18.0.0",
       "react-dom": "^18.0.0",
       "axios": "^1.6.0",
       "react-hook-form": "^7.48.0",
       "zod": "^3.22.0",
       "@hookform/resolvers": "^3.3.0"
     },
     "devDependencies": {
       "@types/node": "^20.0.0",
       "@types/react": "^18.0.0",
       "typescript": "^5.0.0",
       "tailwindcss": "^3.3.0",
       "eslint": "^8.0.0"
     }
   }
   ```

3. **Variáveis de Ambiente**
   ```env
   NEXT_PUBLIC_API_URL=http://localhost:8010/api
   NEXT_PUBLIC_APP_URL=http://localhost:3010
   ```

4. **Configuração TypeScript**
   - `tsconfig.json` com paths configurados
   - Tipos para API responses

5. **Linter e Formatter**
   - ESLint configurado
   - Prettier configurado
   - Husky para pre-commit hooks (opcional)

---

## 📝 Próximas Etapas

- [ ] **Etapa 4**: Implementação da feature
- [ ] **Etapa 5**: Testes unitários
- [ ] **Etapa 6**: Testes de integração
- [ ] **Etapa 7**: Testes manuais
- [ ] **Etapa 8**: Revisão de código
- [ ] **Etapa 9**: Documentação
- [ ] **Etapa 10**: Deploy para staging
- [ ] **Etapa 11**: Teste UAT
- [ ] **Etapa 12**: Deploy para produção

---

**Próximo passo**: Iniciar Etapa 3 (Criar Ambiente) e depois Etapa 4 (Implementação)

