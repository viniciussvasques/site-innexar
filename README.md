# StructurOne

> Plataforma SaaS para gestão completa de empreendimentos, captação de investimentos e transparência total para construtoras e investidores.

## 🎯 Sobre o Projeto

O **StructurOne** é uma plataforma SaaS desenvolvida pela **Innexar** que centraliza informações, automatiza relatórios e oferece dashboards intuitivos para cada cliente, garantindo confiança e eficiência na gestão de obras e investimentos.

## 🚀 Funcionalidades Principais

- **Multi-tenant**: Cada cliente possui sua própria estrutura, dados e dashboard isolados
- **Gestão de Projetos**: Cadastro e acompanhamento de empreendimentos
- **Portal do Investidor**: Acompanhamento em tempo real de investimentos
- **Gestão Financeira**: Entradas, saídas, fluxo de caixa e orçamentos
- **Documentos**: Upload e gestão de contratos, notas fiscais e comprovantes
- **Atualizações de Obra**: Fotos, vídeos e percentuais de conclusão
- **Relatórios Automáticos**: Relatórios auditáveis e automatizados
- **Internacionalização**: Suporte para Português, Inglês e Espanhol

## 🏗️ Arquitetura

O projeto utiliza Django como framework principal:

```
structurone/
├── structurone/      # Configurações do projeto Django
├── apps/             # Aplicações Django
│   ├── core/        # Core app
│   ├── tenants/      # Multi-tenant
│   ├── projects/     # Gestão de projetos
│   ├── investors/    # Portal do investidor
│   ├── financial/    # Gestão financeira
│   ├── documents/    # Upload de documentos
│   └── updates/      # Atualizações de obra
├── static/           # Arquivos estáticos
├── media/            # Arquivos de mídia
├── templates/        # Templates Django
├── locale/           # Traduções i18n
├── .github/
│   └── workflows/    # CI/CD
└── docs/             # Documentação
```

## 🛠️ Tecnologias

- **Backend**: Django 5.0+, Python 3.11+
- **API**: Django REST Framework
- **Database**: PostgreSQL (multi-tenant)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Multi-tenant**: django-tenants
- **CI/CD**: GitHub Actions
- **Frontend**: Next.js (separado) ou Django Templates

## 📋 Pré-requisitos

- Python >= 3.11
- PostgreSQL >= 14.0
- pip >= 23.0

## 🚀 Instalação

```bash
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

# Executar servidor de desenvolvimento
python manage.py runserver
```

## 🌍 Internacionalização

O projeto suporta três idiomas:
- 🇧🇷 Português (PT-BR)
- 🇺🇸 Inglês (EN-US)
- 🇪🇸 Espanhol (ES-ES)

## 📝 Licença

UNLICENSED - Propriedade da Innexar

## 👥 Desenvolvido por

**Innexar**

---

Para mais informações, consulte a documentação em `/docs`.

