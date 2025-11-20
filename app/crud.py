"""CRUD operations for database models."""
from typing import Optional, List
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_, func
from decimal import Decimal

from . import models, schemas
from .core.security import get_password_hash
from .core.pagination import PaginationParams


# ============ User CRUD ============
def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """Get user by ID."""
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username."""
    return db.query(models.User).filter(models.User.username == username).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email."""
    return db.query(models.User).filter(models.User.email == email).first()


def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create a new user."""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        name=user.name,
        username=user.username,
        phone_number=user.phone_number,
        email=user.email,
        gender=user.gender,
        date_of_birth=user.date_of_birth,
        address=user.address,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user(db: Session, user_id: int, user_update: schemas.UserUpdate) -> Optional[models.User]:
    """Update user profile."""
    db_user = get_user(db, user_id)
    if db_user:
        update_data = user_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_user, field, value)
        db.commit()
        db.refresh(db_user)
    return db_user


# ============ Product CRUD ============
def create_product(db: Session, product: schemas.ProductCreate) -> models.Product:
    """Create a new product."""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int) -> Optional[models.Product]:
    """Get product by ID with optimized query."""
    return db.query(models.Product).options(
        joinedload(models.Product.category)
    ).filter(models.Product.id == product_id).first()


def get_products(
    db: Session,
    params: PaginationParams,
    search: Optional[str] = None,
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None
):
    """Get products with filters and pagination."""
    query = db.query(models.Product).filter(models.Product.is_active == True)
    
    # Apply filters
    if search:
        query = query.filter(
            or_(
                models.Product.name.ilike(f"%{search}%"),
                models.Product.description.ilike(f"%{search}%")
            )
        )
    
    if category_id:
        query = query.filter(models.Product.category_id == category_id)
    
    if min_price is not None:
        query = query.filter(models.Product.selling_price >= min_price)
    
    if max_price is not None:
        query = query.filter(models.Product.selling_price <= max_price)
    
    # Order by created_at descending
    query = query.order_by(models.Product.created_at.desc())
    
    return query


def update_product(db: Session, product_id: int, product: schemas.ProductUpdate) -> Optional[models.Product]:
    """Update a product."""
    db_product = get_product(db, product_id)
    if db_product:
        update_data = product.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


def delete_product(db: Session, product_id: int) -> bool:
    """Soft delete a product."""
    db_product = get_product(db, product_id)
    if db_product:
        db_product.is_active = False
        db.commit()
        return True
    return False


# ============ Category CRUD ============
def create_category(db: Session, category: schemas.CategoryCreate) -> models.Category:
    """Create a new category."""
    db_category = models.Category(**category.model_dump())
    db.add(db_category)
    db.commit()
    db.refresh(db_category)
    return db_category


def get_category(db: Session, category_id: int) -> Optional[models.Category]:
    """Get category by ID."""
    return db.query(models.Category).filter(models.Category.id == category_id).first()


def get_categories(db: Session) -> List[models.Category]:
    """Get all active categories."""
    return db.query(models.Category).filter(models.Category.is_active == True).all()


# ============ Wishlist CRUD ============
def get_wishlist(db: Session, wishlist_id: int) -> Optional[models.Wishlist]:
    """Get wishlist item by ID."""
    return db.query(models.Wishlist).filter(models.Wishlist.id == wishlist_id).first()


def get_wishlists_by_user(db: Session, user_id: int, params: PaginationParams):
    """Get user's wishlist with pagination."""
    query = db.query(models.Wishlist).filter(
        models.Wishlist.user_id == user_id
    ).order_by(models.Wishlist.created_at.desc())
    return query


def create_wishlist(db: Session, user_id: int, product_id: int) -> models.Wishlist:
    """Add item to wishlist."""
    # Check if already exists
    existing = db.query(models.Wishlist).filter(
        models.Wishlist.user_id == user_id,
        models.Wishlist.product_id == product_id
    ).first()
    
    if existing:
        return existing
    
    db_wishlist = models.Wishlist(user_id=user_id, product_id=product_id)
    db.add(db_wishlist)
    db.commit()
    db.refresh(db_wishlist)
    return db_wishlist


def delete_wishlist(db: Session, wishlist_id: int) -> bool:
    """Remove item from wishlist."""
    db_wishlist = get_wishlist(db, wishlist_id)
    if db_wishlist:
        db.delete(db_wishlist)
        db.commit()
        return True
    return False


# ============ Cart CRUD ============
def get_or_create_cart(db: Session, user_id: int) -> models.Cart:
    """Get or create user's cart."""
    cart = db.query(models.Cart).filter(models.Cart.user_id == user_id).first()
    if not cart:
        cart = models.Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


def get_cart_with_items(db: Session, user_id: int) -> Optional[models.Cart]:
    """Get cart with items."""
    return db.query(models.Cart).options(
        joinedload(models.Cart.items).joinedload(models.CartItem.product)
    ).filter(models.Cart.user_id == user_id).first()


def add_to_cart(db: Session, user_id: int, product_id: int, quantity: int) -> models.CartItem:
    """Add item to cart or update quantity."""
    cart = get_or_create_cart(db, user_id)
    
    # Check if item already in cart
    cart_item = db.query(models.CartItem).filter(
        models.CartItem.cart_id == cart.id,
        models.CartItem.product_id == product_id
    ).first()
    
    if cart_item:
        cart_item.quantity += quantity
    else:
        cart_item = models.CartItem(
            cart_id=cart.id,
            product_id=product_id,
            quantity=quantity
        )
        db.add(cart_item)
    
    db.commit()
    db.refresh(cart_item)
    return cart_item


def update_cart_item(db: Session, cart_item_id: int, quantity: int) -> Optional[models.CartItem]:
    """Update cart item quantity."""
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if cart_item:
        cart_item.quantity = quantity
        db.commit()
        db.refresh(cart_item)
    return cart_item


def remove_from_cart(db: Session, cart_item_id: int) -> bool:
    """Remove item from cart."""
    cart_item = db.query(models.CartItem).filter(models.CartItem.id == cart_item_id).first()
    if cart_item:
        db.delete(cart_item)
        db.commit()
        return True
    return False


def clear_cart(db: Session, user_id: int) -> bool:
    """Clear all items from cart."""
    cart = get_or_create_cart(db, user_id)
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()
    return True


# ============ Order CRUD ============
def create_order(db: Session, user_id: int, order_data: schemas.OrderCreate) -> models.Order:
    """Create a new order from cart or items."""
    # Calculate total
    total_amount = Decimal('0')
    order_items_data = []
    
    for item in order_data.items:
        product = get_product(db, item.product_id)
        if not product or not product.is_active:
            continue
        
        item_total = Decimal(str(product.selling_price)) * item.quantity
        total_amount += item_total
        
        order_items_data.append({
            'product_id': product.id,
            'quantity': item.quantity,
            'price': Decimal(str(product.selling_price))
        })
    
    # Create order
    db_order = models.Order(
        user_id=user_id,
        total_amount=total_amount,
        shipping_address=order_data.shipping_address,
        payment_method=order_data.payment_method,
        notes=order_data.notes
    )
    db.add(db_order)
    db.flush()
    
    # Create order items
    for item_data in order_items_data:
        order_item = models.OrderItem(
            order_id=db_order.id,
            **item_data
        )
        db.add(order_item)
    
    db.commit()
    db.refresh(db_order)
    return db_order


def get_order(db: Session, order_id: int) -> Optional[models.Order]:
    """Get order by ID with items."""
    return db.query(models.Order).options(
        joinedload(models.Order.items).joinedload(models.OrderItem.product)
    ).filter(models.Order.id == order_id).first()


def get_user_orders(db: Session, user_id: int, params: PaginationParams):
    """Get user's orders with pagination."""
    query = db.query(models.Order).filter(
        models.Order.user_id == user_id
    ).order_by(models.Order.created_at.desc())
    return query


def update_order_status(db: Session, order_id: int, status: models.OrderStatus) -> Optional[models.Order]:
    """Update order status."""
    db_order = get_order(db, order_id)
    if db_order:
        db_order.status = status
        db.commit()
        db.refresh(db_order)
    return db_order


# ============ Review CRUD ============
def create_review(db: Session, user_id: int, review: schemas.ReviewCreate) -> models.Review:
    """Create a product review."""
    db_review = models.Review(
        user_id=user_id,
        **review.model_dump()
    )
    db.add(db_review)
    db.commit()
    db.refresh(db_review)
    return db_review


def get_product_reviews(db: Session, product_id: int, params: PaginationParams):
    """Get product reviews with pagination."""
    query = db.query(models.Review).filter(
        models.Review.product_id == product_id
    ).order_by(models.Review.created_at.desc())
    return query


def get_review(db: Session, review_id: int) -> Optional[models.Review]:
    """Get review by ID."""
    return db.query(models.Review).filter(models.Review.id == review_id).first()


def update_review(db: Session, review_id: int, review_update: schemas.ReviewUpdate) -> Optional[models.Review]:
    """Update a review."""
    db_review = get_review(db, review_id)
    if db_review:
        update_data = review_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_review, field, value)
        db.commit()
        db.refresh(db_review)
    return db_review


def delete_review(db: Session, review_id: int) -> bool:
    """Delete a review."""
    db_review = get_review(db, review_id)
    if db_review:
        db.delete(db_review)
        db.commit()
        return True
    return False
