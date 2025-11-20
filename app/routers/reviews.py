"""Review router with pagination."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..database import get_db
from ..core.security import get_current_active_user
from ..core.pagination import PaginationParams, paginate, PageResponse

router = APIRouter()


@router.post("/", response_model=schemas.Review, status_code=status.HTTP_201_CREATED)
async def create_review(
    review: schemas.ReviewCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a product review."""
    # Verify product exists
    product = crud.get_product(db, review.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    
    return crud.create_review(db, current_user.id, review)


@router.get("/product/{product_id}", response_model=PageResponse[schemas.Review])
async def get_product_reviews(
    product_id: int,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get all reviews for a product with pagination."""
    params = PaginationParams(page=page, page_size=page_size)
    query = crud.get_product_reviews(db, product_id, params)
    return paginate(query, params)


@router.put("/{review_id}", response_model=schemas.Review)
async def update_review(
    review_id: int,
    review_update: schemas.ReviewUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update a review (only by review author)."""
    db_review = crud.get_review(db, review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Verify review belongs to current user
    if db_review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this review"
        )
    
    return crud.update_review(db, review_id, review_update)


@router.delete("/{review_id}", response_model=schemas.MessageResponse)
async def delete_review(
    review_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete a review (only by review author)."""
    db_review = crud.get_review(db, review_id)
    if not db_review:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Review not found"
        )
    
    # Verify review belongs to current user
    if db_review.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this review"
        )
    
    crud.delete_review(db, review_id)
    return {"message": "Review deleted successfully"}
