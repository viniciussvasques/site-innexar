#!/bin/bash
# Script para testar API multi-tenant
# Uso: ./test_api_tenant.sh

echo "🧪 Testando API Multi-Tenant"
echo "================================"
echo ""

# Verificar se servidor está rodando
if ! curl -s http://localhost:8010/api/ > /dev/null; then
    echo "❌ Servidor Django não está rodando!"
    echo "   Execute: python manage.py runserver"
    exit 1
fi

echo "✅ Servidor está rodando"
echo ""

# Teste 1: Sem header (deve falhar ou retornar vazio)
echo "📋 Teste 1: Requisição sem header"
echo "   curl http://localhost:8010/api/tenants/"
curl -s http://localhost:8000/api/tenants/ | head -20
echo ""
echo ""

# Teste 2: Com header tenant 1
echo "📋 Teste 2: Requisição com header X-Tenant-Slug: empresa-abc"
echo "   curl -H \"X-Tenant-Slug: empresa-abc\" http://localhost:8000/api/tenants/"
curl -s -H "X-Tenant-Slug: empresa-abc" http://localhost:8000/api/tenants/ | head -20
echo ""
echo ""

# Teste 3: Com header tenant 2
echo "📋 Teste 3: Requisição com header X-Tenant-Slug: construtora-xyz"
echo "   curl -H \"X-Tenant-Slug: construtora-xyz\" http://localhost:8000/api/tenants/"
curl -s -H "X-Tenant-Slug: construtora-xyz" http://localhost:8000/api/tenants/ | head -20
echo ""
echo ""

# Teste 4: Detalhes do tenant
echo "📋 Teste 4: Detalhes do tenant empresa-abc"
echo "   curl -H \"X-Tenant-Slug: empresa-abc\" http://localhost:8000/api/tenants/1/"
curl -s -H "X-Tenant-Slug: empresa-abc" http://localhost:8000/api/tenants/1/ | head -20
echo ""
echo ""

echo "✅ Testes concluídos!"
echo ""
echo "💡 Para testar com subdomínios, configure /etc/hosts primeiro"

