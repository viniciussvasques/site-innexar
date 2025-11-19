# Checklist de Revisão de Código - StructurOne

## 📋 Visão Geral

Este documento define o checklist padrão para revisão de código no StructurOne, seguindo os 13 passos do fluxo de desenvolvimento.

## ✅ Status Atual

- ✅ **Etapa 7**: Testes Manuais concluídos (8/9 testes passando)
- 🔄 **Etapa 8**: Revisão de Código (EM ANDAMENTO)

## 🔍 Checklist de Revisão

### 1. Clareza e Legibilidade

- [ ] Código é fácil de entender?
- [ ] Nomes de variáveis e funções são descritivos?
- [ ] Comentários explicam o "porquê", não o "o quê"?
- [ ] Não há código comentado desnecessário?
- [ ] Magic numbers foram substituídos por constantes?

### 2. Simplicidade

- [ ] Funções fazem apenas uma coisa?
- [ ] Funções são pequenas (< 50 linhas idealmente)?
- [ ] Não há complexidade ciclomática excessiva?
- [ ] Código segue o princípio DRY (Don't Repeat Yourself)?
- [ ] Não há over-engineering?

### 3. Segurança

- [ ] Todas as entradas são validadas?
- [ ] Não há SQL injection (usando ORM)?
- [ ] Não há XSS (sanitização de inputs)?
- [ ] Tokens e secrets não estão hardcoded?
- [ ] Autenticação e autorização estão corretas?
- [ ] Rate limiting está implementado?
- [ ] CORS está configurado corretamente?
- [ ] Dados sensíveis são criptografados?

### 4. Performance

- [ ] Queries ao banco são otimizadas (select_related, prefetch_related)?
- [ ] Não há N+1 queries?
- [ ] Cache está sendo usado quando apropriado?
- [ ] Paginação está implementada?
- [ ] Imagens/assets são otimizados?
- [ ] Não há loops desnecessários?

### 5. Organização

- [ ] Estrutura de pastas segue o padrão do projeto?
- [ ] Arquivos estão nos lugares corretos?
- [ ] Imports estão organizados (isort)?
- [ ] Não há imports não utilizados?

### 6. Nomenclatura

- [ ] Nomes seguem as convenções do projeto?
- [ ] Nomes são consistentes em todo o código?
- [ ] Nomes de classes são PascalCase?
- [ ] Nomes de funções/variáveis são snake_case?
- [ ] Constantes são UPPER_CASE?

### 7. Funções e Classes

- [ ] Funções são pequenas e focadas?
- [ ] Classes têm responsabilidade única?
- [ ] Não há funções com muitos parâmetros (> 5)?
- [ ] Funções retornam valores consistentes?
- [ ] Tratamento de erros está adequado?

### 8. Duplicação

- [ ] Não há código duplicado?
- [ ] Lógica comum foi extraída para funções/classes?
- [ ] Templates/componentes são reutilizáveis?

### 9. Testes

- [ ] Código tem testes unitários?
- [ ] Código tem testes de integração?
- [ ] Testes cobrem casos de sucesso e erro?
- [ ] Cobertura de testes é adequada (> 80%)?
- [ ] Testes são legíveis e mantíveis?

### 10. Tratamento de Erros

- [ ] Erros são tratados adequadamente?
- [ ] Mensagens de erro são claras e úteis?
- [ ] Logs são informativos?
- [ ] Exceções são específicas (não genéricas)?

### 11. Documentação

- [ ] Funções/classes complexas têm docstrings?
- [ ] README está atualizado?
- [ ] Documentação da API está atualizada?
- [ ] Comentários explicam decisões importantes?

### 12. Padrões do Projeto

- [ ] Código segue o style guide (Black, Prettier, ESLint)?
- [ ] Commits seguem Conventional Commits?
- [ ] Branch naming segue o padrão (feature/*, fix/*)?
- [ ] PR tem descrição clara?

### 13. Dependências

- [ ] Dependências são necessárias?
- [ ] Versões de dependências são compatíveis?
- [ ] Dependências estão atualizadas?
- [ ] Não há dependências vulneráveis?

## 🔍 Revisão Específica - Módulo de Autenticação

### Arquivos a Revisar

#### Backend
- [ ] `backend/apps/core/models.py` - Modelos de User, PasswordResetToken, OnboardingProgress
- [ ] `backend/apps/core/serializers.py` - Serializers de autenticação
- [ ] `backend/apps/core/views.py` - ViewSets de autenticação
- [ ] `backend/apps/core/services.py` - Lógica de negócio
- [ ] `backend/apps/core/authentication.py` - Autenticação customizada
- [ ] `backend/apps/core/permissions.py` - Permissões
- [ ] `backend/apps/core/utils.py` - Utilitários de i18n
- [ ] `backend/apps/core/tests/` - Todos os testes

#### Configuração
- [ ] `backend/structurone/settings.py` - Configurações JWT e blacklist
- [ ] `backend/requirements.txt` - Dependências

#### Testes
- [ ] `backend/test_manual_auth.py` - Testes manuais

### Pontos Críticos a Verificar

#### Segurança
- [ ] Tokens JWT são invalidados corretamente no logout?
- [ ] Blacklist de tokens está funcionando?
- [ ] Senhas são hasheadas (não armazenadas em texto)?
- [ ] Rate limiting está ativo?
- [ ] Validação de senha está adequada?

#### Performance
- [ ] Queries ao banco são otimizadas?
- [ ] Não há N+1 queries em serializers?
- [ ] Cache está sendo usado quando apropriado?

#### Qualidade
- [ ] Código segue PEP 8?
- [ ] Type hints estão presentes?
- [ ] Docstrings estão completas?
- [ ] Tratamento de erros é adequado?

## 📝 Template de Revisão

```markdown
## Revisão de Código - [Nome do Módulo]

### Arquivos Revisados
- [ ] arquivo1.py
- [ ] arquivo2.py

### Pontos Positivos
- ✅ ...
- ✅ ...

### Pontos a Melhorar
- ⚠️ ...
- ⚠️ ...

### Problemas Críticos
- 🔴 ...
- 🔴 ...

### Sugestões
- 💡 ...
- 💡 ...

### Aprovação
- [ ] Aprovado
- [ ] Aprovado com ressalvas
- [ ] Rejeitado (requer correções)
```

## 🚀 Próximos Passos Após Revisão

1. **Corrigir problemas identificados**
2. **Atualizar documentação se necessário**
3. **Re-executar testes**
4. **Prosseguir para Etapa 9: Documentação**

## 📚 Referências

- [Fluxo de Desenvolvimento](./DEVELOPMENT_PROCESS.md)
- [Guia de Desenvolvimento](./DEVELOPMENT.md)
- [Testes Manuais](./MANUAL_TESTING_PROCEDURE.md)

