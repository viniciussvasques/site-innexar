# Frontend Next.js - Dockerfile
FROM node:18-alpine

WORKDIR /app

# Copiar arquivos de dependências
COPY package.json package-lock.json* ./

# Instalar dependências
RUN npm install

# Copiar código
COPY . .

# Variáveis de ambiente
ENV NEXT_TELEMETRY_DISABLED=1
ENV NODE_ENV=development

EXPOSE 3000

# Comando para desenvolvimento
CMD ["npm", "run", "dev"]

