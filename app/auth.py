"""Legacy auth module - kept for backwards compatibility.

This module is deprecated. Use app.core.security instead.
"""
from .core.security import (
    verify_password,
    get_password_hash,
    authenticate_user,
    create_access_token,
    get_current_user,
    get_current_active_user
)
from .config import settings

# Export for backwards compatibility
SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

__all__ = [
    'verify_password',
    'get_password_hash',
    'authenticate_user',
    'create_access_token',
    'get_current_user',
    'get_current_active_user',
    'SECRET_KEY',
    'ALGORITHM',
    'ACCESS_TOKEN_EXPIRE_MINUTES'
]
