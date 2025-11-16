# Deploy no VPS - StructurOne

## 🌐 Configuração de Subdomínios

### 1. Configuração DNS

No seu provedor de DNS, configure:

```
A Record: structurone.com -> IP_DO_VPS
A Record: *.structurone.com -> IP_DO_VPS (wildcard para subdomínios)
```

### 2. Configuração Nginx

```nginx
# /etc/nginx/sites-available/structurone

# Upstream para Django
upstream django_backend {
    server 127.0.0.1:8010;
}

# Servidor principal (admin/API)
server {
    listen 80;
    server_name structurone.com admin.structurone.com;

    location / {
        proxy_pass http://django_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/structurone/backend/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /path/to/structurone/backend/media/;
    }
}

# Servidor para subdomínios (tenants)
server {
    listen 80;
    server_name *.structurone.com;

    location / {
        proxy_pass http://django_backend;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Static files
    location /static/ {
        alias /path/to/structurone/backend/staticfiles/;
    }

    # Media files
    location /media/ {
        alias /path/to/structurone/backend/media/;
    }
}
```

### 3. Configuração SSL (Let's Encrypt)

```bash
# Instalar Certbot
sudo apt install certbot python3-certbot-nginx

# Obter certificado (wildcard requer DNS challenge)
sudo certbot --nginx -d structurone.com -d *.structurone.com

# Renovação automática
sudo certbot renew --dry-run
```

### 4. Configuração Django

```python
# backend/structurone/settings.py (produção)

ALLOWED_HOSTS = [
    'structurone.com',
    'admin.structurone.com',
    '.structurone.com',  # Permite todos os subdomínios
]

TENANT_DOMAIN = 'structurone.com'
DEBUG = False
```

### 5. Gunicorn

```bash
# Instalar Gunicorn
pip install gunicorn

# Executar
gunicorn structurone.wsgi:application \
    --bind 127.0.0.1:8010 \
    --workers 4 \
    --timeout 120
```

### 6. Systemd Service

```ini
# /etc/systemd/system/structurone.service

[Unit]
Description=StructurOne Django Backend
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/path/to/structurone/backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/gunicorn structurone.wsgi:application \
    --bind 127.0.0.1:8010 \
    --workers 4 \
    --timeout 120

[Install]
WantedBy=multi-user.target
```

```bash
# Ativar serviço
sudo systemctl enable structurone
sudo systemctl start structurone
sudo systemctl status structurone
```

## 📊 Banco de Dados

### PostgreSQL

```bash
# Instalar PostgreSQL
sudo apt install postgresql postgresql-contrib

# Criar banco e usuário
sudo -u postgres psql
CREATE DATABASE structurone_db;
CREATE USER structurone_user WITH PASSWORD 'senha_segura';
GRANT ALL PRIVILEGES ON DATABASE structurone_db TO structurone_user;
\q
```

### Migrações

```bash
cd backend
python manage.py migrate
python manage.py collectstatic --noinput
```

## 🔒 Segurança

1. **Firewall**
   ```bash
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable
   ```

2. **Variáveis de Ambiente**
   - Nunca commitar `.env`
   - Usar secrets no VPS
   - Rotacionar SECRET_KEY

3. **Backup Automático**
   ```bash
   # Script de backup
   #!/bin/bash
   pg_dump structurone_db > /backups/structurone_$(date +%Y%m%d).sql
   ```

## 🚀 Deploy Checklist

- [ ] DNS configurado
- [ ] Nginx configurado
- [ ] SSL configurado
- [ ] PostgreSQL instalado e configurado
- [ ] Django migrado
- [ ] Gunicorn rodando
- [ ] Systemd service ativo
- [ ] Firewall configurado
- [ ] Backup configurado
- [ ] Monitoramento configurado

