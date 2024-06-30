from datetime import date
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class ProductBase(BaseModel):
    name: str
    description: str
    mrp: float
    discount: float
    selling_price: float


class ProductCreate(ProductBase):
    pass


class ProductUpdate(ProductBase):
    pass


class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    username: str
    phone_number: str = Field(pattern=r'^\+?1?\d{9,15}$')
    email: EmailStr
    gender: Optional[str] = None
    date_of_birth: Optional[date] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class WishlistBase(BaseModel):
    user_id: int
    product_id: int


class WishlistCreate(WishlistBase):
    pass


class Wishlist(WishlistBase):
    id: int
    product: Product

    class Config:
        orm_mode = True
