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
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verifica se o usuário tem tenant
        if not hasattr(request.user, 'tenant') or not request.user.tenant:
            return False
        
        # Usuário autenticado com tenant tem permissão
        return True
    
    def has_object_permission(self, request, view, obj):
        """Verifica permissão no objeto"""
        # Verifica se o usuário está autenticado
        if not request.user or not request.user.is_authenticated:
            return False
        
        # Verifica se o usuário tem tenant
        if not hasattr(request.user, 'tenant') or not request.user.tenant:
            return False
        
        # Verifica se o objeto pertence ao tenant do usuário
        if hasattr(obj, 'tenant'):
            return obj.tenant == request.user.tenant
        
        # Se objeto não tem tenant, permite (ex: Plan)
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

