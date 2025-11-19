# 🔵 1. Planejamento - Autenticação e Onboarding

## 📋 O que a feature resolve

### Problema
Os tenants (construtoras) precisam de uma forma segura e intuitiva de:
- Acessar a plataforma com suas credenciais
- Registrar novos usuários vinculados ao seu tenant
- Realizar onboarding inicial para configurar a empresa
- Gerenciar sessões e recuperar senhas

### Objetivo
Criar um sistema completo de autenticação multi-tenant que permita:
- Login seguro com JWT
- Registro de usuários vinculados a tenants
- Onboarding guiado para novos tenants
- Recuperação de senha
- Gestão de sessão e tokens

---

## ✅ Requisitos Funcionais

### RF-001: Autenticação de Usuários
- **Descrição**: Usuários devem poder fazer login usando email/username e senha
- **Prioridade**: Crítica
- **Entrada**: Email/username e senha
- **Saída**: Tokens JWT (access + refresh)
- **Regras**:
  - Usuário deve estar ativo
  - Usuário deve pertencer a um tenant ativo
  - Senha deve ser validada
  - Após 3 tentativas falhas, bloquear temporariamente (5 minutos)

### RF-002: Registro de Usuários
- **Descrição**: Novos usuários podem se registrar vinculados a um tenant
- **Prioridade**: Alta
- **Entrada**: Nome, email, senha, tenant_slug (ou identificação do tenant)
- **Saída**: Usuário criado e tokens JWT
- **Regras**:
  - Email deve ser único por tenant
  - Senha deve ter no mínimo 8 caracteres
  - Tenant deve existir e estar ativo
  - Primeiro usuário do tenant vira admin automaticamente

### RF-003: Recuperação de Senha
- **Descrição**: Usuários podem solicitar reset de senha via email
- **Prioridade**: Média
- **Entrada**: Email
- **Saída**: Email com link de reset
- **Regras**:
  - Link válido por 24 horas
  - Token único e seguro
  - Após reset, invalidar token

### RF-004: Refresh Token
- **Descrição**: Renovar access token sem precisar fazer login novamente
- **Prioridade**: Alta
- **Entrada**: Refresh token válido
- **Saída**: Novo access token
- **Regras**:
  - Refresh token válido por 7 dias
  - Após uso, pode gerar novo refresh token (rotation)
  - Se refresh token expirado, forçar novo login

### RF-005: Dados do Usuário Logado
- **Descrição**: Endpoint para obter dados do usuário autenticado
- **Prioridade**: Alta
- **Entrada**: Access token válido
- **Saída**: Dados do usuário (nome, email, tenant, permissões)
- **Regras**:
  - Retornar apenas dados do próprio usuário
  - Incluir informações do tenant

### RF-006: Onboarding
- **Descrição**: Fluxo guiado para configurar tenant após primeiro login
- **Prioridade**: Alta
- **Etapas**:
  1. Informações da Empresa (nome, CNPJ, endereço)
  2. Configuração Inicial (logo, cores, idioma)
  3. Primeiro Projeto (opcional)
  4. Convidar Usuários (opcional)
- **Regras**:
  - Salvar progresso em cada etapa
  - Permitir pular etapas opcionais
  - Marcar onboarding como completo após finalização

### RF-007: Logout
- **Descrição**: Invalidar tokens e encerrar sessão
- **Prioridade**: Média
- **Entrada**: Access token
- **Saída**: Confirmação de logout
- **Regras**:
  - Invalidar refresh token
  - Limpar tokens do cliente

---

## 🛡️ Requisitos Não Funcionais

### RNF-001: Segurança
- **Criptografia**: Senhas devem ser hasheadas com bcrypt/argon2
- **Tokens**: JWT com expiração curta (15 min access, 7 dias refresh)
- **HTTPS**: Obrigatório em produção
- **Rate Limiting**: Limitar tentativas de login (5 por minuto por IP)
- **CSRF**: Proteção contra CSRF em formulários

### RNF-002: Performance
- **Tempo de resposta**: Login < 500ms
- **Cache**: Cachear dados do usuário por 5 minutos
- **Queries**: Otimizar queries com select_related/prefetch_related

### RNF-003: Escalabilidade
- **Concorrência**: Suportar 1000+ logins simultâneos
- **Banco**: Índices em email, tenant_id
- **Sessões**: Stateless (JWT) para escalabilidade horizontal

### RNF-004: Usabilidade
- **UX**: Interface intuitiva e responsiva
- **Feedback**: Mensagens de erro claras
- **Loading**: Indicadores de carregamento
- **Validação**: Validação em tempo real nos formulários

### RNF-005: Confiabilidade
- **Disponibilidade**: 99.9% uptime
- **Logs**: Registrar todas as tentativas de login (sucesso e falha)
- **Monitoramento**: Alertas para tentativas suspeitas

---

## ⚠️ Pontos Críticos

### PC-001: Isolamento Multi-tenant
- **Risco**: Usuário de um tenant acessar dados de outro
- **Mitigação**: 
  - Sempre validar tenant_id em todas as queries
  - Middleware para garantir tenant correto
  - Testes de isolamento obrigatórios

### PC-002: Segurança de Senhas
- **Risco**: Senhas fracas ou vazamento
- **Mitigação**:
  - Validação de força de senha
  - Hash seguro (bcrypt/argon2)
  - Não logar senhas em nenhum lugar

### PC-003: Tokens JWT
- **Risco**: Token comprometido ou expirado
- **Mitigação**:
  - Expiração curta (15 min)
  - Refresh token rotation
  - Blacklist de tokens (opcional, usar Redis)

### PC-004: Onboarding Incompleto
- **Risco**: Tenant não configurar informações essenciais
- **Mitigação**:
  - Marcar campos obrigatórios
  - Permitir completar depois
  - Dashboard mostrar pendências

### PC-005: Email de Recuperação
- **Risco**: Email não entregue ou spam
- **Mitigação**:
  - Usar serviço confiável (SendGrid, AWS SES)
  - Templates profissionais
  - Rate limiting para evitar spam

---

## ✅ Critérios de Aceite

### CA-001: Login
- [ ] Usuário consegue fazer login com email e senha válidos
- [ ] Recebe tokens JWT (access + refresh)
- [ ] Após 3 tentativas falhas, conta é bloqueada por 5 minutos
- [ ] Mensagens de erro são claras e não expõem informações sensíveis
- [ ] Funciona em diferentes navegadores e dispositivos

### CA-002: Registro
- [ ] Novo usuário pode se registrar com email único no tenant
- [ ] Senha deve ter no mínimo 8 caracteres
- [ ] Primeiro usuário do tenant vira admin automaticamente
- [ ] Email de confirmação é enviado (opcional)
- [ ] Após registro, usuário é redirecionado para onboarding

### CA-003: Recuperação de Senha
- [ ] Usuário pode solicitar reset de senha
- [ ] Email com link de reset é enviado
- [ ] Link é válido por 24 horas
- [ ] Após reset, token é invalidado
- [ ] Nova senha deve seguir regras de validação

### CA-004: Refresh Token
- [ ] Access token expira em 15 minutos
- [ ] Refresh token pode renovar access token
- [ ] Refresh token expira em 7 dias
- [ ] Após expiração, usuário deve fazer login novamente

### CA-005: Dados do Usuário
- [ ] Endpoint `/api/auth/me/` retorna dados do usuário logado
- [ ] Inclui informações do tenant
- [ ] Não expõe informações sensíveis (senha, tokens)
- [ ] Resposta em < 200ms

### CA-006: Onboarding
- [ ] Fluxo tem 4 etapas (2 obrigatórias, 2 opcionais)
- [ ] Progresso é salvo em cada etapa
- [ ] Usuário pode pular etapas opcionais
- [ ] Após completar, onboarding é marcado como feito
- [ ] Interface é intuitiva e responsiva

### CA-007: Logout
- [ ] Logout invalida refresh token
- [ ] Cliente limpa tokens do localStorage
- [ ] Usuário é redirecionado para login
- [ ] Não é possível usar tokens após logout

### CA-008: Multi-tenant
- [ ] Usuário só acessa dados do seu tenant
- [ ] Middleware identifica tenant corretamente
- [ ] Queries sempre filtram por tenant_id
- [ ] Testes de isolamento passam

---

## 📊 User Stories

### US-001: Como usuário, quero fazer login para acessar a plataforma
**Critérios de aceite**: CA-001

### US-002: Como novo usuário, quero me registrar para criar minha conta
**Critérios de aceite**: CA-002

### US-003: Como usuário, quero recuperar minha senha caso esqueça
**Critérios de aceite**: CA-003

### US-004: Como usuário, quero que minha sessão seja mantida sem precisar fazer login constantemente
**Critérios de aceite**: CA-004

### US-005: Como usuário, quero ver meus dados de perfil
**Critérios de aceite**: CA-005

### US-006: Como novo tenant, quero fazer onboarding para configurar minha empresa
**Critérios de aceite**: CA-006

### US-007: Como usuário, quero fazer logout para encerrar minha sessão
**Critérios de aceite**: CA-007

---

## 📝 Notas de Implementação

### Ordem de Desenvolvimento
1. Backend: Models e Migrations
2. Backend: Serializers e Validações
3. Backend: Services (regras de negócio)
4. Backend: Endpoints
5. Backend: Testes
6. Frontend: Estrutura e Layout
7. Frontend: Páginas de Autenticação
8. Frontend: Onboarding
9. Frontend: Integração com API
10. Frontend: Testes

### Dependências
- Django REST Framework
- djangorestframework-simplejwt
- django-allauth (opcional, para email)
- Celery + Redis (para emails assíncronos)

### Integrações Futuras
- OAuth2 (Google, Microsoft)
- 2FA (Two-Factor Authentication)
- SSO (Single Sign-On)

---

## ✅ Checklist de Entrega

- [x] Documento de planejamento completo
- [ ] User stories definidas
- [ ] Acceptance criteria definidos
- [ ] Aprovação do planejamento
- [ ] Pronto para próxima etapa (Design da Solução)

