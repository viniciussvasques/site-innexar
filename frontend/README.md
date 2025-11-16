# Frontend - StructurOne

Frontend web application for StructurOne platform.

## Opções de Implementação

### Opção 1: Next.js (Recomendado)
Frontend separado usando Next.js que consome a API REST do backend Django.

### Opção 2: Django Templates
Frontend integrado usando Django templates (já configurado em `apps/core/frontend_views.py`).

## Estrutura

```
frontend/
├── src/              # Código fonte (se Next.js)
├── public/           # Arquivos públicos
├── components/       # Componentes React
├── pages/            # Páginas/rotas
├── services/         # Serviços de API
├── hooks/            # Custom hooks
└── utils/            # Utilitários
```

## Setup Next.js (quando implementado)

```bash
cd frontend
npm install
npm run dev
```

## API Endpoints

O frontend consome a API REST do backend Django:

- Base URL: `http://localhost:8000/api/`
- Authentication: JWT tokens
- CORS: Configurado para `http://localhost:3000`

