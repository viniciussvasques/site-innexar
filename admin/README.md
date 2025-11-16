# Painel Admin - StructurOne

Painel administrativo customizado para gestão da plataforma StructurOne.

## 🚀 Início Rápido

O painel admin é uma aplicação Django separada que consome a API do backend.

```bash
# Entrar na pasta admin
cd admin

# O admin usa o mesmo ambiente virtual do backend
# Ativar ambiente virtual (do backend)
cd ../backend
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Voltar para admin
cd ../admin

# Executar servidor (se configurado separadamente)
# Ou acessar via backend: http://localhost:8000/admin/
```

## 📁 Estrutura

```
admin/
├── apps/                 # Apps do admin
│   └── admin/           # App principal do admin
│       ├── urls.py      # URLs do admin
│       ├── views.py     # Views do admin
│       └── admin.py     # Customização Django Admin
├── templates/            # Templates do admin
│   ├── base.html        # Template base
│   └── dashboard.html   # Dashboard
└── static/              # Arquivos estáticos
```

## 🔗 URLs

- Django Admin padrão: `http://localhost:8000/admin/`
- Admin customizado: `http://localhost:8000/admin-panel/`

## 👨‍💼 Funcionalidades

1. **Dashboard** - Visão geral do sistema
2. **Gestão de Tenants** - Gerenciar clientes
3. **Gestão de Usuários** - Gerenciar usuários do sistema
4. **Configurações** - Configurações do sistema

## 🔐 Acesso

Requer permissão de staff (`is_staff=True`).

## 📝 Nota

O admin pode ser integrado ao backend ou rodar como aplicação separada, dependendo da arquitetura escolhida.

