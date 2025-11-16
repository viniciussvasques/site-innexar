#!/bin/bash
set -e

echo "🚀 Iniciando backend Django..."

# Aguardar PostgreSQL estar pronto
echo "⏳ Aguardando PostgreSQL..."
while ! nc -z db 5432; do
  sleep 0.1
done
echo "✅ PostgreSQL está pronto!"

# Executar migrações
echo "📦 Executando migrações..."
python manage.py migrate --noinput

# Coletar arquivos estáticos
echo "📦 Coletando arquivos estáticos..."
python manage.py collectstatic --noinput || true

# Criar superusuário se não existir (apenas em desenvolvimento)
if [ "$DJANGO_ENV" = "development" ]; then
  echo "👤 Verificando superusuário..."
  python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@structurone.com', 'admin123')
    print('✅ Superusuário criado: admin/admin123')
else:
    print('ℹ️  Superusuário já existe')
EOF
fi

echo "✅ Backend pronto!"
exec "$@"

