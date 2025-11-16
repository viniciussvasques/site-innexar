"""
Custom Permissions
Permissões customizadas para multi-tenant
"""
from rest_framework import permissions


class IsTenantOwner(permissions.BasePermission):
    """
    Permissão que verifica se o usuário pertence ao tenant da requisição
    """
    def has_permission(self, request, view):
        """Verifica se o usuário tem permissão"""
        tenant = getattr(request, 'tenant', None)
        if not tenant:
            return False
        
        # Verifica se o usuário pertence ao tenant
        # TODO: Implementar quando modelo User estiver pronto
        # user_tenant = request.user.tenant
        # return user_tenant == tenant
        
        # Por enquanto, permite se houver tenant na requisição
        return True
    
    def has_object_permission(self, request, view, obj):
        """Verifica permissão no objeto"""
        tenant = getattr(request, 'tenant', None)
        if not tenant:
            return False
        
        # Verifica se o objeto pertence ao tenant
        if hasattr(obj, 'tenant'):
            return obj.tenant == tenant
        
        return True


class IsAdminOrTenantOwner(permissions.BasePermission):
    """
    Permissão que permite admin ou owner do tenant
    """
    def has_permission(self, request, view):
        """Verifica se é admin ou owner do tenant"""
        # Admin sempre tem permissão
        if request.user and request.user.is_staff:
            return True
        
        # Verifica se é owner do tenant
        return IsTenantOwner().has_permission(request, view)

