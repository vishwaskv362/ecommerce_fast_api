"""Wishlist router with pagination."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..database import get_db
from ..core.security import get_current_active_user
from ..core.pagination import PaginationParams, paginate, PageResponse

router = APIRouter()


@router.post("/", response_model=schemas.Wishlist, status_code=status.HTTP_201_CREATED)
async def add_to_wishlist(
    wishlist_item: schemas.WishlistCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add a product to wishlist."""
    # Verify product exists
    product = crud.get_product(db, wishlist_item.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return crud.create_wishlist(db=db, user_id=current_user.id, product_id=wishlist_item.product_id)


@router.get("/", response_model=PageResponse[schemas.Wishlist])
async def get_wishlist(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user's wishlist with pagination."""
    params = PaginationParams(page=page, page_size=page_size)
    query = crud.get_wishlists_by_user(db, current_user.id, params)
    return paginate(query, params)


@router.delete("/{wishlist_id}", response_model=schemas.MessageResponse)
async def remove_from_wishlist(
    wishlist_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Remove a product from wishlist."""
    wishlist_item = crud.get_wishlist(db, wishlist_id=wishlist_id)
    
    if not wishlist_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Wishlist item not found"
        )
    
    # Verify wishlist item belongs to current user
    if wishlist_item.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to remove this item"
        )
    
    crud.delete_wishlist(db=db, wishlist_id=wishlist_id)
    return {"message": "Item removed from wishlist"}
