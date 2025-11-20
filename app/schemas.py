"""Pydantic schemas for request/response validation."""
from datetime import date, datetime
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, EmailStr, Field, ConfigDict, field_validator
from .models import OrderStatus


# ============ Product Schemas ============
class ProductBase(BaseModel):
    """Base product schema."""
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    mrp: float = Field(..., gt=0)
    discount: float = Field(default=0, ge=0, le=100)
    selling_price: float = Field(..., gt=0)
    stock_quantity: int = Field(default=0, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = None


class ProductCreate(ProductBase):
    """Schema for creating a product."""
    pass


class ProductUpdate(BaseModel):
    """Schema for updating a product."""
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    mrp: Optional[float] = Field(None, gt=0)
    discount: Optional[float] = Field(None, ge=0, le=100)
    selling_price: Optional[float] = Field(None, gt=0)
    stock_quantity: Optional[int] = Field(None, ge=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class Product(ProductBase):
    """Product response schema."""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ Category Schemas ============
class CategoryBase(BaseModel):
    """Base category schema."""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None


class CategoryCreate(CategoryBase):
    """Schema for creating a category."""
    pass


class CategoryUpdate(BaseModel):
    """Schema for updating a category."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    description: Optional[str] = None
    parent_id: Optional[int] = None
    is_active: Optional[bool] = None


class Category(CategoryBase):
    """Category response schema."""
    id: int
    is_active: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ User Schemas ============
class UserBase(BaseModel):
    """Base user schema."""
    name: str = Field(..., min_length=1, max_length=100)
    username: str = Field(..., min_length=3, max_length=50)
    phone_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    email: EmailStr
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    """Schema for user registration."""
    password: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    """Schema for updating user profile."""
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone_number: Optional[str] = Field(None, pattern=r'^\+?1?\d{9,15}$')
    email: Optional[EmailStr] = None
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None


class User(UserBase):
    """User response schema."""
    id: int
    is_active: bool
    is_admin: bool
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ Authentication Schemas ============
class Token(BaseModel):
    """Token response schema."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    """Token payload data."""
    username: Optional[str] = None


class RefreshTokenRequest(BaseModel):
    """Refresh token request."""
    refresh_token: str


# ============ Wishlist Schemas ============
class WishlistCreate(BaseModel):
    """Schema for adding to wishlist."""
    product_id: int


class Wishlist(BaseModel):
    """Wishlist response schema."""
    id: int
    user_id: int
    product_id: int
    created_at: datetime
    product: Product
    
    model_config = ConfigDict(from_attributes=True)


# ============ Cart Schemas ============
class CartItemCreate(BaseModel):
    """Schema for adding item to cart."""
    product_id: int
    quantity: int = Field(default=1, gt=0)


class CartItemUpdate(BaseModel):
    """Schema for updating cart item."""
    quantity: int = Field(..., gt=0)


class CartItem(BaseModel):
    """Cart item response schema."""
    id: int
    cart_id: int
    product_id: int
    quantity: int
    product: Product
    
    model_config = ConfigDict(from_attributes=True)


class Cart(BaseModel):
    """Cart response schema."""
    id: int
    user_id: int
    items: List[CartItem]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ Order Schemas ============
class OrderItemCreate(BaseModel):
    """Schema for order item creation."""
    product_id: int
    quantity: int = Field(..., gt=0)


class OrderCreate(BaseModel):
    """Schema for creating an order."""
    items: List[OrderItemCreate]
    shipping_address: str = Field(..., min_length=10)
    payment_method: Optional[str] = "COD"
    notes: Optional[str] = None


class OrderItem(BaseModel):
    """Order item response schema."""
    id: int
    product_id: int
    quantity: int
    price: Decimal
    product: Product
    
    model_config = ConfigDict(from_attributes=True)


class Order(BaseModel):
    """Order response schema."""
    id: int
    user_id: int
    total_amount: Decimal
    status: OrderStatus
    shipping_address: str
    payment_method: Optional[str]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime
    items: List[OrderItem]
    
    model_config = ConfigDict(from_attributes=True)


class OrderUpdate(BaseModel):
    """Schema for updating order status."""
    status: OrderStatus


# ============ Review Schemas ============
class ReviewCreate(BaseModel):
    """Schema for creating a review."""
    product_id: int
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None


class ReviewUpdate(BaseModel):
    """Schema for updating a review."""
    rating: Optional[int] = Field(None, ge=1, le=5)
    comment: Optional[str] = None


class Review(BaseModel):
    """Review response schema."""
    id: int
    product_id: int
    user_id: int
    rating: int
    comment: Optional[str]
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ============ Common Response Schemas ============
class MessageResponse(BaseModel):
    """Generic message response."""
    message: str


class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    version: str
    timestamp: datetime
