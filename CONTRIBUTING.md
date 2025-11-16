# Guia de Contribuição

## Como Contribuir

### 1. Fork e Clone

```bash
git clone https://github.com/viniciussvasques/structurone.git
cd structurone
```

### 2. Criar Branch

```bash
git checkout -b feature/nova-funcionalidade
# ou
git checkout -b fix/correcao-bug
```

### 3. Desenvolvimento

- Siga as convenções de código definidas em `docs/DEVELOPMENT.md`
- Escreva testes para novas funcionalidades
- Mantenha commits pequenos e descritivos

### 4. Commit

Use conventional commits:

```
feat: adiciona funcionalidade X
fix: corrige bug Y
docs: atualiza documentação
refactor: reorganiza código
test: adiciona testes
```

### 5. Push e Pull Request

```bash
git push origin feature/nova-funcionalidade
```

Crie um Pull Request no GitHub com:
- Descrição clara da mudança
- Referência a issues relacionadas (se houver)
- Screenshots (se aplicável)

## Padrões de Código

- Use TypeScript
- Siga as convenções de nomenclatura
- Mantenha funções pequenas e focadas
- Adicione comentários quando necessário
- Escreva testes

## Code Review

Todas as mudanças passam por code review antes de serem mergeadas.

## Dúvidas?

Abra uma issue no GitHub ou entre em contato com a equipe.

