"""Product router with pagination and filtering."""
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from .. import schemas, crud, models
from ..database import get_db
from ..core.security import get_current_active_user
from ..core.pagination import PaginationParams, paginate, PageResponse

router = APIRouter()


@router.post("/", response_model=schemas.Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Create a new product (admin only in production)."""
    return crud.create_product(db=db, product=product)


@router.get("/", response_model=PageResponse[schemas.Product])
async def list_products(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    search: Optional[str] = Query(None),
    category_id: Optional[int] = Query(None),
    min_price: Optional[float] = Query(None, ge=0),
    max_price: Optional[float] = Query(None, ge=0),
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """
    Get all products with pagination and filtering.
    
    - **page**: Page number (default: 1)
    - **page_size**: Items per page (default: 20, max: 100)
    - **search**: Search in product name and description
    - **category_id**: Filter by category
    - **min_price**: Minimum price filter
    - **max_price**: Maximum price filter
    """
    params = PaginationParams(page=page, page_size=page_size)
    query = crud.get_products(
        db,
        params,
        search=search,
        category_id=category_id,
        min_price=min_price,
        max_price=max_price
    )
    return paginate(query, params)


@router.get("/{product_id}", response_model=schemas.Product)
async def get_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Get a specific product by ID."""
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return db_product


@router.put("/{product_id}", response_model=schemas.Product)
async def update_product(
    product_id: int,
    product: schemas.ProductUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Update a product (admin only in production)."""
    db_product = crud.get_product(db, product_id=product_id)
    if db_product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return crud.update_product(db=db, product_id=product_id, product=product)


@router.delete("/{product_id}", response_model=schemas.MessageResponse)
async def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    """Delete (deactivate) a product (admin only in production)."""
    success = crud.delete_product(db, product_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )
    return {"message": "Product deleted successfully"}
