# Procedimento de Testes Manuais - StructurOne

## 📋 Visão Geral

Este documento descreve o procedimento padrão para realizar testes manuais no StructurOne, seguindo o fluxo de desenvolvimento estabelecido.

## 🎯 Objetivo

Garantir que todas as funcionalidades implementadas funcionem corretamente através de testes manuais que simulam o comportamento de um usuário real.

## 🔧 Pré-requisitos

1. **Servidor Backend rodando**
   - Local: `http://localhost:8010`
   - Docker: `http://localhost:8000`

2. **Banco de dados configurado e migrado**
   ```bash
   cd backend
   python manage.py migrate
   ```

3. **Dependências instaladas**
   ```bash
   pip install -r requirements.txt
   ```

4. **Token Blacklist configurado**
   - App `rest_framework_simplejwt.token_blacklist` instalado
   - Migrações do blacklist executadas:
   ```bash
   python manage.py migrate
   ```

5. **Python 3.10+ instalado**

## 📝 Script de Testes Manuais

### Localização
- **Arquivo**: `backend/test_manual_auth.py`
- **Descrição**: Script automatizado que testa o fluxo completo de autenticação e onboarding

### Execução

#### Windows (PowerShell)
```powershell
cd "C:\Saas contrutora e incorporadora\backend"
python test_manual_auth.py
```

#### Linux/Mac
```bash
cd backend
python test_manual_auth.py
```

## 🧪 Fluxo de Testes Completo

O script executa os seguintes testes na ordem:

### 1. ✅ API Root
- **Endpoint**: `GET /api/`
- **Verifica**: API está acessível e retorna informações básicas
- **Resultado esperado**: Status 200 com informações da API
- **Critérios de sucesso**:
  - API responde
  - Retorna nome, versão e endpoints disponíveis

### 2. ✅ Registro de Usuário
- **Endpoint**: `POST /api/auth/register/`
- **Verifica**: Criação de novo usuário e tenant
- **Dados testados**:
  - Email único (timestamp)
  - Senha válida (mínimo 8 caracteres, maiúscula, minúscula, número, caractere especial)
  - Dados pessoais (nome, sobrenome, telefone)
  - Criação automática de tenant
- **Resultado esperado**: Status 201 com tokens JWT
- **Critérios de sucesso**:
  - Usuário criado
  - Tenant criado automaticamente
  - Tokens (access e refresh) retornados
  - Role definido como "user"

### 3. ✅ Login
- **Endpoint**: `POST /api/auth/login/`
- **Verifica**: Autenticação com credenciais válidas
- **Dados testados**:
  - Email e senha do usuário registrado
- **Resultado esperado**: Status 200 com tokens JWT
- **Critérios de sucesso**:
  - Autenticação bem-sucedida
  - Tokens retornados
  - Dados do usuário retornados
  - Status de onboarding retornado

### 4. ✅ Obter Dados do Usuário
- **Endpoint**: `GET /api/auth/me/`
- **Verifica**: Acesso autenticado aos dados do usuário
- **Headers**: `Authorization: Bearer <access_token>`
- **Resultado esperado**: Status 200 com dados completos do usuário e tenant
- **Critérios de sucesso**:
  - Dados do usuário retornados
  - Dados do tenant retornados
  - Configurações de i18n (idioma, moeda, timezone) presentes

### 5. ✅ Onboarding - Obter Progresso
- **Endpoint**: `GET /api/onboarding/`
- **Verifica**: Progresso do onboarding
- **Resultado esperado**: Status 200 com etapa atual e dados
- **Critérios de sucesso**:
  - Etapa atual retornada (1-4)
  - Status de conclusão retornado
  - Dados salvos retornados

### 6. ✅ Atualizar Onboarding - Etapa 1
- **Endpoint**: `POST /api/onboarding/`
- **Dados**: Informações da empresa
  - Nome da empresa
  - CNPJ
  - Endereço
- **Verifica**: Salvamento de dados da etapa 1
- **Resultado esperado**: Status 200 com etapa atualizada
- **Critérios de sucesso**:
  - Etapa atualizada para 1
  - Dados salvos corretamente

### 7. ✅ Atualizar Onboarding - Etapa 2
- **Endpoint**: `POST /api/onboarding/`
- **Dados**: Configuração visual e país
  - Logo (URL)
  - Cor primária
  - País (código ISO)
- **Verifica**: 
  - Salvamento de dados da etapa 2
  - Configuração automática de i18n (idioma, moeda, timezone)
- **Resultado esperado**: Status 200 com i18n configurado automaticamente
- **Critérios de sucesso**:
  - Etapa atualizada para 2
  - Idioma detectado automaticamente
  - Moeda detectada automaticamente
  - Timezone detectado automaticamente
  - Formato de data detectado automaticamente

### 8. ⚠️ Completar Onboarding
- **Endpoint**: `POST /api/onboarding/complete/`
- **Verifica**: Finalização do processo de onboarding
- **Resultado esperado**: Status 200 com confirmação
- **Nota**: Pode falhar se onboarding já estiver completo (comportamento esperado)
- **Critérios de sucesso**:
  - Onboarding marcado como completo
  - Mensagem de sucesso retornada

### 9. ✅ Refresh Token
- **Endpoint**: `POST /api/auth/token/refresh/`
- **Verifica**: Renovação de tokens JWT
- **Dados**: Refresh token atual
- **Resultado esperado**: Status 200 com novos tokens
- **Critérios de sucesso**:
  - Novo access token retornado
  - Novo refresh token retornado (rotação)
  - Token antigo invalidado (blacklist)

### 10. ✅ Logout
- **Endpoint**: `POST /api/auth/logout/`
- **Verifica**: Encerramento de sessão e invalidação de tokens
- **Headers**: `Authorization: Bearer <access_token>`
- **Dados**: Refresh token
- **Resultado esperado**: Status 200 com confirmação
- **Critérios de sucesso**:
  - Refresh token invalidado (blacklist)
  - Access token invalidado (blacklist)
  - Mensagem de sucesso retornada

### 11. ✅ Verificação de Logout
- **Endpoint**: `GET /api/auth/me/`
- **Verifica**: Token invalidado após logout
- **Headers**: `Authorization: Bearer <access_token_invalidado>`
- **Resultado esperado**: Status 401 (Unauthorized)
- **Critérios de sucesso**:
  - Acesso negado após logout
  - Token não pode ser usado para autenticação
  - Mensagem de erro apropriada

## 📊 Resultados Esperados

### Teste Completo Bem-Sucedido
```
Total: 9/9 testes passaram
✓ Todos os testes manuais passaram!
```

### Resultados Típicos
- **8-9/9 testes passando**: Funcionalidade principal OK
- **< 8 testes passando**: Requer investigação

### Distribuição de Testes
- **Autenticação**: 5 testes (API Root, Registro, Login, GET /me, Logout)
- **Onboarding**: 3 testes (Obter, Atualizar, Completar)
- **Tokens**: 2 testes (Refresh, Verificação de Logout)

## 🐛 Problemas Conhecidos e Soluções

### 1. ✅ Token não invalidado após logout (CORRIGIDO)
- **Status**: Resolvido
- **Solução**: 
  - Adicionado `rest_framework_simplejwt.token_blacklist` ao projeto
  - Modificado logout para invalidar refresh token e access token
  - Usa OutstandingToken e BlacklistedToken para invalidação imediata
- **Arquivos modificados**:
  - `backend/requirements.txt`
  - `backend/structurone/settings.py`
  - `backend/apps/core/services.py`
  - `backend/apps/core/views.py`

### 2. ✅ Encoding no Windows (CORRIGIDO)
- **Status**: Resolvido
- **Solução**: Script configurado com UTF-8 para Windows
- **Arquivo**: `backend/test_manual_auth.py` (linhas 5-11)

### 3. Complete Onboarding pode falhar
- **Status**: Comportamento esperado
- **Descrição**: Se onboarding já estiver completo, retorna erro 400
- **Solução**: Não é um bug, é validação de negócio

## 📋 Checklist de Testes Manuais

Antes de considerar um módulo completo, verificar:

### Autenticação
- [ ] API Root acessível
- [ ] Registro de usuário funciona
- [ ] Login funciona
- [ ] Obter dados do usuário funciona
- [ ] Refresh token funciona
- [ ] Logout funciona
- [ ] Token invalidado após logout (verificação)

### Onboarding
- [ ] Obter progresso do onboarding funciona
- [ ] Atualizar etapas funciona
- [ ] Configuração automática de i18n funciona
- [ ] Completar onboarding funciona

### Integração
- [ ] Tokens JWT válidos
- [ ] Multi-tenant isolado
- [ ] Dados persistidos corretamente
- [ ] Erros tratados adequadamente
- [ ] Blacklist de tokens funcionando

## 🔄 Quando Executar Testes Manuais

### Obrigatório
1. **Após implementar novo módulo**
2. **Antes de fazer merge para main**
3. **Após mudanças significativas na API**
4. **Antes de deploy em produção**
5. **Após correções de bugs críticos**

### Recomendado
1. **Após correções de bugs**
2. **Após refatorações**
3. **Periodicamente durante desenvolvimento**
4. **Após atualizar dependências**

## 📈 Melhorias Futuras

1. **Testes para outros módulos**
   - Projetos
   - Investidores
   - Financeiro
   - Documentos
   - Atualizações

2. **Testes de interface**
   - Admin (Next.js)
   - Frontend (Next.js)

3. **Testes de integração completa**
   - Fluxos end-to-end
   - Multi-tenant completo
   - Permissões e roles

4. **Automação**
   - Integração com CI/CD
   - Relatórios automatizados
   - Notificações de falhas

5. **Cobertura**
   - Testes de carga
   - Testes de segurança
   - Testes de acessibilidade

## 🔧 Configuração do Ambiente

### Instalar Dependências
```bash
cd backend
pip install -r requirements.txt
```

### Executar Migrações
```bash
python manage.py migrate
```

### Verificar Token Blacklist
```bash
python manage.py showmigrations token_blacklist
```

Se não estiver migrado:
```bash
python manage.py migrate token_blacklist
```

## 📚 Referências

- [Fluxo de Desenvolvimento](./DEVELOPMENT_PROCESS.md)
- [Testes Locais](./TESTING_LOCAL.md)
- [Arquitetura](./ARCHITECTURE.md)
- [Documentação JWT](https://django-rest-framework-simplejwt.readthedocs.io/)

## ✅ Última Execução

**Data**: 16/11/2024
**Versão do Fluxo**: 2.0
**Resultado**: 7/8 testes passaram (antes da correção)
**Status**: ✅ Bug corrigido, fluxo redefinido
**Observações**: 
- Bug de invalidação de token após logout corrigido
- Fluxo completo redefinido com 9 testes
- Verificação de logout adicionada
- Documentação atualizada

## 🎯 Próximos Passos

1. ✅ Executar migrações do token_blacklist
2. ✅ Testar correção do logout
3. ✅ Validar todos os 9 testes
4. ⏳ Expandir testes para outros módulos
5. ⏳ Adicionar testes de interface
