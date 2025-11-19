#!/usr/bin/env python
"""Script para criar superusuário admin"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'structurone.settings')
django.setup()

from django.contrib.auth import get_user_model
from apps.tenants.models import Tenant

User = get_user_model()

# Criar ou obter tenant padrão
tenant, _ = Tenant.objects.get_or_create(
    slug='structurone',
    defaults={
        'name': 'StructurOne',
        'domain': 'structurone.com',
        'email': 'admin@structurone.com',
    }
)

# Verificar se admin já existe
admin = User.objects.filter(email='admin@structurone.com').first()

if not admin:
    # Criar superusuário
    admin = User.objects.create_superuser(
        'admin@structurone.com',
        'admin123',
        tenant=tenant
    )
    print('✅ Superusuário criado com sucesso!')
    print(f'   Email: admin@structurone.com')
    print(f'   Senha: admin123')
else:
    print('ℹ️  Superusuário já existe!')
    print(f'   Email: {admin.email}')
    print(f'   É superusuário: {admin.is_superuser}')

