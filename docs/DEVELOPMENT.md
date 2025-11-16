# Guia de Desenvolvimento

## Setup Inicial

### Pré-requisitos

- Python >= 3.11
- pip >= 23.0
- PostgreSQL >= 14.0
- Git

### Instalação

```bash
# Clonar repositório
git clone https://github.com/viniciussvasques/structurone.git
cd structurone

# Criar ambiente virtual
python -m venv venv

# Ativar ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env
# Editar .env com suas configurações

# Executar migrações
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Executar servidor
python manage.py runserver
```

## Comandos Disponíveis

### Django Management

- `python manage.py runserver` - Inicia servidor de desenvolvimento
- `python manage.py migrate` - Executa migrações
- `python manage.py makemigrations` - Cria migrações
- `python manage.py createsuperuser` - Cria superusuário
- `python manage.py collectstatic` - Coleta arquivos estáticos
- `python manage.py compilemessages` - Compila traduções

### Desenvolvimento

- `black .` - Formata código
- `flake8 .` - Verifica estilo de código
- `isort .` - Organiza imports
- `pytest` - Executa testes
- `pytest --cov=.` - Executa testes com cobertura

## Convenções de Código

### Python/Django

- Siga PEP 8
- Use type hints quando possível
- Use docstrings para funções e classes
- Mantenha linhas com máximo de 100 caracteres

### Nomenclatura

- **Arquivos**: snake_case (`user_service.py`)
- **Classes**: PascalCase (`UserProfile`)
- **Funções/Variáveis**: snake_case (`get_user_data`)
- **Constantes**: UPPER_SNAKE_CASE (`MAX_FILE_SIZE`)
- **Models**: PascalCase (`Project`, `Investor`)
- **Views**: snake_case (`project_list`, `create_investor`)

### Estrutura de Apps Django

```
apps/projects/
├── __init__.py
├── admin.py          # Admin configuration
├── apps.py           # App config
├── models.py         # Models
├── views.py          # Views/ViewSets
├── serializers.py    # DRF Serializers
├── urls.py           # URL routing
├── tests.py          # Tests
└── migrations/       # Database migrations
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

- Framework: pytest + pytest-django
- Cobertura: pytest-cov
- Fixtures: pytest fixtures
- Mocks: unittest.mock ou pytest-mock

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

