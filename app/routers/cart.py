"""Cart router."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..database import get_db
from ..core.security import get_current_active_user

router = APIRouter()


@router.get("/", response_model=schemas.Cart)
async def get_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get current user's cart with items."""
    cart = crud.get_cart_with_items(db, current_user.id)
    if not cart:
        cart = crud.get_or_create_cart(db, current_user.id)
    return cart


@router.post("/items", response_model=schemas.CartItem, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item: schemas.CartItemCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Add an item to cart."""
    # Verify product exists
    product = crud.get_product(db, item.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    if not product.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Product is not available"
        )
    
    return crud.add_to_cart(db, current_user.id, item.product_id, item.quantity)


@router.put("/items/{item_id}", response_model=schemas.CartItem)
async def update_cart_item(
    item_id: int,
    item_update: schemas.CartItemUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update cart item quantity."""
    cart_item = crud.update_cart_item(db, item_id, item_update.quantity)
    if not cart_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    return cart_item


@router.delete("/items/{item_id}", response_model=schemas.MessageResponse)
async def remove_from_cart(
    item_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Remove an item from cart."""
    success = crud.remove_from_cart(db, item_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item not found"
        )
    return {"message": "Item removed from cart"}


@router.delete("/", response_model=schemas.MessageResponse)
async def clear_cart(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Clear all items from cart."""
    crud.clear_cart(db, current_user.id)
    return {"message": "Cart cleared successfully"}
