from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy import String, Float, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    mrp = Column(Float)
    discount = Column(Float)
    selling_price = Column(Float)


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    username = Column(String, unique=True, index=True)
    phone_number = Column(String)
    email = Column(String, unique=True, index=True)
    gender = Column(String)
    date_of_birth = Column(Date)
    address = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    wishlists = relationship("Wishlist", back_populates="user")


class Wishlist(Base):
    __tablename__ = "wishlists"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))

    user = relationship("User", back_populates="wishlists")
    product = relationship("Product", lazy='joined')
