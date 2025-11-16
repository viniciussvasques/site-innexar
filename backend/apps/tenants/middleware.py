"""
Tenant Middleware
Middleware para detectar tenant baseado no subdomínio
"""
from django.http import Http404
from django.utils.deprecation import MiddlewareMixin
from .models import Tenant


class TenantMiddleware(MiddlewareMixin):
    """
    Middleware que identifica o tenant baseado no subdomínio da requisição
    """
    def process_request(self, request):
        """
        Processa a requisição e identifica o tenant
        """
        host = request.get_host().split(':')[0]  # Remove porta se houver
        
        # Em desenvolvimento, pode usar localhost com header
        if 'localhost' in host or '127.0.0.1' in host:
            # Para desenvolvimento, pode usar header X-Tenant-Slug
            tenant_slug = request.headers.get('X-Tenant-Slug')
            if tenant_slug:
                try:
                    tenant = Tenant.objects.get(slug=tenant_slug, is_active=True)
                    request.tenant = tenant
                    return None
                except Tenant.DoesNotExist:
                    pass
        
        # Em produção, extrai subdomínio
        # Exemplo: cliente1.structurone.com -> cliente1
        parts = host.split('.')
        
        # Se tiver mais de 2 partes, assume que a primeira é o subdomínio
        if len(parts) >= 3:
            subdomain = parts[0]
            
            # Ignora 'www'
            if subdomain == 'www':
                if len(parts) >= 4:
                    subdomain = parts[1]
                else:
                    # Sem subdomínio, pode ser admin ou API principal
                    request.tenant = None
                    return None
            
            try:
                tenant = Tenant.objects.get(slug=subdomain, is_active=True)
                request.tenant = tenant
            except Tenant.DoesNotExist:
                # Tenant não encontrado - pode ser admin ou API principal
                # Em produção, pode retornar 404 ou redirecionar
                request.tenant = None
                # Para desenvolvimento, permite continuar
                # Em produção, descomente a linha abaixo:
                # raise Http404("Tenant não encontrado")
        else:
            # Sem subdomínio - pode ser admin ou API principal
            request.tenant = None
        
        return None

