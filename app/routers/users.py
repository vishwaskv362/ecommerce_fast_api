"""User router (legacy - prefer using /auth endpoints)."""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from .. import schemas, models
from ..database import get_db
from ..core.security import get_current_active_user

router = APIRouter()


@router.get("/me", response_model=schemas.User)
async def get_current_user_profile(
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user profile (use /auth/me instead)."""
    return current_user
