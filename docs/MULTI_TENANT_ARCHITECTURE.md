# Arquitetura Multi-Tenant - StructurOne

## 🏗️ Estratégia Escolhida: Row-Based com Subdomínios

### Decisão Arquitetural

**Estratégia**: Row-based (mesmo banco, mesmo backend, isolamento por `tenant_id`)

**Por quê?**
- ✅ Mais simples de gerenciar e manter
- ✅ Escalável horizontalmente
- ✅ Backup e manutenção mais fáceis
- ✅ Mesmo código para todos os tenants
- ✅ Fácil migrar para schema-based depois se necessário
- ✅ Custo menor (um banco, um servidor)

## 🌐 Subdomínios

Cada cliente terá seu próprio subdomínio:

- **Admin/API Principal**: `structurone.com` ou `admin.structurone.com`
- **Cliente 1**: `cliente1.structurone.com`
- **Cliente 2**: `cliente2.structurone.com`
- **Cliente 3**: `cliente3.structurone.com`

## 🔧 Como Funciona

### 1. Middleware de Tenant

O `TenantMiddleware` detecta automaticamente o tenant baseado no subdomínio:

```python
# Requisição para: cliente1.structurone.com
# Middleware identifica: tenant com slug "cliente1"
# Adiciona request.tenant automaticamente
```

### 2. Isolamento de Dados

Todos os modelos que precisam de isolamento herdam de `TenantMixin`:

```python
class Project(TenantMixin, TimeStampedModel):
    name = models.CharField(max_length=255)
    # tenant é adicionado automaticamente
```

### 3. Filtragem Automática

O `TenantManager` filtra automaticamente por tenant:

```python
# Automaticamente filtra pelo tenant da requisição
projects = Project.objects.for_request(request).all()
```

## 📊 Estrutura do Banco de Dados

```
PostgreSQL Database: structurone_db
├── tenants_tenant          # Tabela de tenants
├── projects_project        # Projetos (com tenant_id)
├── investors_investor      # Investidores (com tenant_id)
├── financial_transaction   # Transações (com tenant_id)
└── ...                     # Outras tabelas (com tenant_id)
```

## 🔐 Segurança

### Isolamento Garantido

1. **Middleware**: Detecta tenant antes de processar requisição
2. **Manager**: Filtra automaticamente por tenant
3. **Permissions**: Verifica se objeto pertence ao tenant
4. **Serializers**: Validam tenant_id

### Proteções

- ✅ Impossível acessar dados de outro tenant
- ✅ Validação em múltiplas camadas
- ✅ Queries sempre filtradas por tenant
- ✅ Admin pode ver todos (com permissão)

## 🚀 Deploy no VPS

### Configuração Nginx

```nginx
# /etc/nginx/sites-available/structurone

# API Principal / Admin
server {
    server_name structurone.com admin.structurone.com;
    
    location / {
        proxy_pass http://localhost:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

# Subdomínios dinâmicos (wildcard)
server {
    server_name *.structurone.com;
    
    location / {
        proxy_pass http://localhost:8010;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Configuração Django

```python
# settings.py
ALLOWED_HOSTS = [
    'structurone.com',
    'admin.structurone.com',
    '.structurone.com',  # Permite todos os subdomínios
]

TENANT_DOMAIN = 'structurone.com'
```

## 🧪 Desenvolvimento Local

### Opção 1: Header Custom

```bash
# Usar header X-Tenant-Slug
curl -H "X-Tenant-Slug: cliente1" http://localhost:8010/api/projects/
```

### Opção 2: /etc/hosts

```bash
# Adicionar ao /etc/hosts (Linux/Mac) ou C:\Windows\System32\drivers\etc\hosts (Windows)
127.0.0.1 cliente1.localhost
127.0.0.1 cliente2.localhost

# Acessar: http://cliente1.localhost:8010
```

## 📈 Escalabilidade Futura

Se necessário escalar para schema-based no futuro:

1. **Fase 1 (Atual)**: Row-based - todos no mesmo schema
2. **Fase 2 (Se necessário)**: Schema-based - cada tenant com seu schema
3. **Fase 3 (Se necessário)**: Database-based - cada tenant com seu banco

A migração é facilitada pela abstração do `TenantMixin`.

## 🔄 Fluxo de Requisição

```
1. Cliente acessa: cliente1.structurone.com/api/projects/
   ↓
2. Nginx recebe requisição
   ↓
3. Nginx encaminha para Django (localhost:8010)
   ↓
4. TenantMiddleware detecta subdomínio "cliente1"
   ↓
5. Busca Tenant com slug "cliente1"
   ↓
6. Adiciona request.tenant
   ↓
7. View processa requisição
   ↓
8. Query filtra automaticamente por tenant
   ↓
9. Retorna apenas dados do tenant
```

## ✅ Vantagens da Abordagem

1. **Simplicidade**: Um banco, um backend, fácil de gerenciar
2. **Performance**: Queries otimizadas com índices em tenant_id
3. **Backup**: Backup único cobre todos os tenants
4. **Manutenção**: Atualizações aplicadas a todos de uma vez
5. **Custo**: Menor custo de infraestrutura
6. **Escalabilidade**: Pode migrar para schema-based depois se necessário

## ⚠️ Considerações

- **Limite de tenants**: Depende do tamanho do banco e performance
- **Isolamento**: Garantido por código, não por banco
- **Backup**: Backup único (mas pode exportar tenant específico)
- **Performance**: Índices em tenant_id são essenciais

## 📝 Próximos Passos

1. ✅ Middleware implementado
2. ✅ TenantMixin criado
3. ⏳ Aplicar TenantMixin em todos os modelos
4. ⏳ Configurar Nginx no VPS
5. ⏳ Testes de isolamento
6. ⏳ Documentação de deploy

