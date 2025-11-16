# Testando Multi-Tenant no Ambiente Local

## 🧪 Métodos de Teste

Existem 3 formas de testar multi-tenant localmente:

### Método 1: Header X-Tenant-Slug (Mais Fácil) ⭐

### Método 2: /etc/hosts (Mais Realista)

### Método 3: Postman/Insomnia (Para APIs)

---

## 📋 Método 1: Header X-Tenant-Slug

### Como Funciona

O middleware detecta quando está em `localhost` e permite usar um header customizado.

### Passo 1: Criar Tenants no Banco

```bash
cd backend
python manage.py shell
```

```python
from apps.tenants.models import Tenant

# Criar tenant 1
tenant1 = Tenant.objects.create(
    name='Empresa ABC',
    slug='empresa-abc',
    domain='empresa-abc.structurone.com',
    email='contato@empresa-abc.com',
    subscription_plan='professional',
    max_projects=50,
    max_users=20
)

# Criar tenant 2
tenant2 = Tenant.objects.create(
    name='Construtora XYZ',
    slug='construtora-xyz',
    domain='construtora-xyz.structurone.com',
    email='contato@construtora-xyz.com',
    subscription_plan='basic',
    max_projects=10,
    max_users=5
)

print(f"Tenant 1 criado: {tenant1.slug}")
print(f"Tenant 2 criado: {tenant2.slug}")
```

### Passo 2: Testar com cURL

```bash
# Testar com tenant 1
curl -H "X-Tenant-Slug: empresa-abc" http://localhost:8000/api/tenants/

# Testar com tenant 2
curl -H "X-Tenant-Slug: construtora-xyz" http://localhost:8000/api/tenants/
```

### Passo 3: Testar no Navegador (JavaScript)

```javascript
// No console do navegador (F12)
fetch('http://localhost:8000/api/tenants/', {
  headers: {
    'X-Tenant-Slug': 'empresa-abc'
  }
})
.then(r => r.json())
.then(console.log);
```

### Passo 4: Testar no Admin (Next.js)

Edite `admin/src/app/tenants/page.tsx` para adicionar o header:

```typescript
const response = await axios.get(`${API_URL}/tenants/`, {
  headers: {
    'X-Tenant-Slug': 'empresa-abc'  // Adicionar este header
  }
});
```

---

## 📋 Método 2: /etc/hosts (Mais Realista)

Este método simula subdomínios reais.

### Windows

1. Abrir como Administrador: `C:\Windows\System32\drivers\etc\hosts`
2. Adicionar linhas:

```
127.0.0.1 empresa-abc.localhost
127.0.0.1 construtora-xyz.localhost
127.0.0.1 admin.localhost
```

### Linux/Mac

```bash
sudo nano /etc/hosts
```

Adicionar:

```
127.0.0.1 empresa-abc.localhost
127.0.0.1 construtora-xyz.localhost
127.0.0.1 admin.localhost
```

### Testar

```bash
# Acessar no navegador
http://empresa-abc.localhost:8000/api/tenants/
http://construtora-xyz.localhost:8000/api/tenants/
http://admin.localhost:8000/admin/
```

### Ajustar Middleware (se necessário)

Se usar `.localhost`, pode precisar ajustar o middleware:

```python
# backend/apps/tenants/middleware.py
# Já está configurado para funcionar com .localhost
```

---

## 📋 Método 3: Postman/Insomnia

### Postman

1. Criar nova requisição
2. URL: `http://localhost:8000/api/tenants/`
3. Headers:
   - Key: `X-Tenant-Slug`
   - Value: `empresa-abc`

### Insomnia

1. Nova requisição GET
2. URL: `http://localhost:8000/api/tenants/`
3. Headers → Add Header:
   - Name: `X-Tenant-Slug`
   - Value: `empresa-abc`

---

## 🧪 Script de Teste Completo

Crie um script Python para testar:

```python
# backend/test_tenant.py
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'structurone.settings')
django.setup()

from apps.tenants.models import Tenant
from django.test import RequestFactory
from apps.tenants.middleware import TenantMiddleware

# Criar tenants de teste
tenant1, _ = Tenant.objects.get_or_create(
    slug='empresa-abc',
    defaults={
        'name': 'Empresa ABC',
        'domain': 'empresa-abc.structurone.com',
        'email': 'contato@empresa-abc.com',
    }
)

tenant2, _ = Tenant.objects.get_or_create(
    slug='construtora-xyz',
    defaults={
        'name': 'Construtora XYZ',
        'domain': 'construtora-xyz.structurone.com',
        'email': 'contato@construtora-xyz.com',
    }
)

print(f"✅ Tenant 1: {tenant1.slug}")
print(f"✅ Tenant 2: {tenant2.slug}")

# Testar middleware
factory = RequestFactory()
middleware = TenantMiddleware(lambda r: None)

# Teste 1: Header
request = factory.get('/api/tenants/')
request.META['HTTP_HOST'] = 'localhost:8000'
request.META['HTTP_X_TENANT_SLUG'] = 'empresa-abc'
middleware.process_request(request)
print(f"✅ Middleware detectou: {request.tenant.slug if hasattr(request, 'tenant') and request.tenant else 'None'}")

# Teste 2: Subdomínio
request = factory.get('/api/tenants/')
request.META['HTTP_HOST'] = 'empresa-abc.localhost:8000'
middleware.process_request(request)
print(f"✅ Subdomínio detectado: {request.tenant.slug if hasattr(request, 'tenant') and request.tenant else 'None'}")

print("\n✅ Testes concluídos!")
```

Executar:

```bash
cd backend
python test_tenant.py
```

---

## 🔍 Verificar se Está Funcionando

### 1. Testar API Diretamente

```bash
# Sem header (deve retornar erro ou vazio)
curl http://localhost:8000/api/tenants/

# Com header (deve retornar dados do tenant)
curl -H "X-Tenant-Slug: empresa-abc" http://localhost:8000/api/tenants/
```

### 2. Verificar no Django Admin

```bash
# Acessar http://localhost:8000/admin/
# Verificar se tenants foram criados
```

### 3. Testar Isolamento

```python
# backend/test_isolation.py
from apps.tenants.models import Tenant
from apps.core.mixins import TenantMixin
from django.db import models

# Criar modelo de teste
class TestModel(TenantMixin, models.Model):
    name = models.CharField(max_length=100)
    
    class Meta:
        app_label = 'tenants'

# Criar dados para tenant 1
tenant1 = Tenant.objects.get(slug='empresa-abc')
obj1 = TestModel.objects.create(tenant=tenant1, name='Objeto 1')

# Criar dados para tenant 2
tenant2 = Tenant.objects.get(slug='construtora-xyz')
obj2 = TestModel.objects.create(tenant=tenant2, name='Objeto 2')

# Verificar isolamento
print(f"Tenant 1 vê: {TestModel.objects.filter(tenant=tenant1).count()} objetos")
print(f"Tenant 2 vê: {TestModel.objects.filter(tenant=tenant2).count()} objetos")
```

---

## 🐛 Troubleshooting

### Problema: Middleware não detecta tenant

**Solução**: Verificar se o header está correto:
```bash
curl -v -H "X-Tenant-Slug: empresa-abc" http://localhost:8000/api/tenants/
```

### Problema: /etc/hosts não funciona

**Solução Windows**: 
- Verificar se arquivo hosts não tem extensão `.txt`
- Executar editor como Administrador

**Solução Linux/Mac**:
```bash
sudo chmod 644 /etc/hosts
```

### Problema: Tenant não encontrado

**Solução**: Verificar se tenant existe e está ativo:
```python
from apps.tenants.models import Tenant
print(Tenant.objects.all())
```

---

## ✅ Checklist de Teste

- [ ] Tenants criados no banco
- [ ] Middleware configurado em settings.py
- [ ] Teste com header X-Tenant-Slug funcionando
- [ ] Teste com /etc/hosts funcionando (opcional)
- [ ] Isolamento de dados funcionando
- [ ] API retorna apenas dados do tenant correto

---

## 📚 Próximos Passos

Depois de testar localmente:
1. Aplicar TenantMixin nos modelos (Projects, Investors, etc.)
2. Testar isolamento completo
3. Preparar para deploy no VPS

