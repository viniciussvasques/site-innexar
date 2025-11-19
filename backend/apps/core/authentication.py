"""
Custom JWT Authentication with Blacklist Support
"""
import logging
from typing import Any
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework_simplejwt.tokens import AccessToken

logger = logging.getLogger(__name__)


class JWTAuthenticationWithBlacklist(JWTAuthentication):
    """
    JWT Authentication que verifica blacklist antes de autenticar
    """
    
    def get_validated_token(self, raw_token: str) -> Any:
        """
        Valida o token e verifica se está na blacklist
        
        Args:
            raw_token: Token JWT em formato string
            
        Returns:
            Token validado
            
        Raises:
            InvalidToken: Se token está na blacklist ou é inválido
        """
        # Primeiro, validar o token normalmente
        validated_token = super().get_validated_token(raw_token)
        
        # Verificar se o token está na blacklist
        if isinstance(validated_token, AccessToken):
            jti = validated_token.get('jti')
            
            if jti:
                # Verificar se existe um OutstandingToken com este jti
                outstanding_token = OutstandingToken.objects.filter(jti=jti).first()
                
                if outstanding_token:
                    # Verificar se está na blacklist
                    is_blacklisted = BlacklistedToken.objects.filter(token=outstanding_token).exists()
                    
                    if is_blacklisted:
                        logger.warning(f'Token {jti} está na blacklist - acesso negado')
                        raise InvalidToken('Token está na blacklist')
        
        return validated_token

