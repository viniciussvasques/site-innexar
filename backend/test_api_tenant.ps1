# Script PowerShell para testar API multi-tenant
# Uso: .\test_api_tenant.ps1

Write-Host "🧪 Testando API Multi-Tenant" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se servidor está rodando
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8010/api/" -UseBasicParsing -TimeoutSec 2
    Write-Host "✅ Servidor está rodando" -ForegroundColor Green
} catch {
    Write-Host "❌ Servidor Django não está rodando!" -ForegroundColor Red
    Write-Host "   Execute: python manage.py runserver" -ForegroundColor Yellow
    exit 1
}

Write-Host ""

# Teste 1: Sem header
Write-Host "📋 Teste 1: Requisição sem header" -ForegroundColor Yellow
Write-Host "   Invoke-WebRequest http://localhost:8010/api/tenants/" -ForegroundColor Gray
try {
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/tenants/" -UseBasicParsing
    Write-Host $response.Content.Substring(0, [Math]::Min(200, $response.Content.Length))
} catch {
    Write-Host "   Status: $($_.Exception.Response.StatusCode.value__)"
}
Write-Host ""

# Teste 2: Com header tenant 1
Write-Host "📋 Teste 2: Requisição com header X-Tenant-Slug: empresa-abc" -ForegroundColor Yellow
Write-Host "   Invoke-WebRequest -Headers @{'X-Tenant-Slug'='empresa-abc'} http://localhost:8010/api/tenants/" -ForegroundColor Gray
try {
    $headers = @{'X-Tenant-Slug'='empresa-abc'}
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/tenants/" -Headers $headers -UseBasicParsing
    Write-Host $response.Content.Substring(0, [Math]::Min(200, $response.Content.Length))
} catch {
    Write-Host "   Erro: $($_.Exception.Message)"
}
Write-Host ""

# Teste 3: Com header tenant 2
Write-Host "📋 Teste 3: Requisição com header X-Tenant-Slug: construtora-xyz" -ForegroundColor Yellow
Write-Host "   Invoke-WebRequest -Headers @{'X-Tenant-Slug'='construtora-xyz'} http://localhost:8010/api/tenants/" -ForegroundColor Gray
try {
    $headers = @{'X-Tenant-Slug'='construtora-xyz'}
    $response = Invoke-WebRequest -Uri "http://localhost:8000/api/tenants/" -Headers $headers -UseBasicParsing
    Write-Host $response.Content.Substring(0, [Math]::Min(200, $response.Content.Length))
} catch {
    Write-Host "   Erro: $($_.Exception.Message)"
}
Write-Host ""

Write-Host "✅ Testes concluídos!" -ForegroundColor Green
Write-Host ""
Write-Host "💡 Para testar com subdomínios, configure C:\Windows\System32\drivers\etc\hosts" -ForegroundColor Yellow

