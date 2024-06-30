from passlib.context import CryptContext
from sqlalchemy.orm import Session

from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password):
    return pwd_context.hash(password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


# User CRUD operations
def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()


def create_user(db: Session, user: schemas.UserCreate):
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


# Product CRUD operations
def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


def get_product(db: Session, product_id: int):
    return db.query(models.Product).filter(models.Product.id == product_id).first()


def get_products(db: Session):
    return db.query(models.Product).all()


def update_product(db: Session, product: schemas.ProductUpdate, product_id: int):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if db_product:
        for key, value in product.dict().items():
            setattr(db_product, key, value)
        db.commit()
        db.refresh(db_product)
    return db_product


# Wishlist CRUD operations
def get_wishlist(db: Session, wishlist_id: int):
    return db.query(models.Wishlist).filter(models.Wishlist.id == wishlist_id).first()


def get_wishlists_by_user(db: Session, user_id: int):
    return db.query(models.Wishlist).filter(models.Wishlist.user_id == user_id).all()


def create_wishlist(db: Session, user_id: int, product_id: int):
    db_wishlist = models.Wishlist(user_id=user_id, product_id=product_id)
    db.add(db_wishlist)
    db.commit()
    db.refresh(db_wishlist)
    return db_wishlist


def delete_wishlist(db: Session, wishlist_id: int):
    db_wishlist = db.query(models.Wishlist).filter(models.Wishlist.id == wishlist_id).first()
    import logging
    logging.info("============")
    logging.info(db_wishlist)
    if db_wishlist:
        db.delete(db_wishlist)
        db.commit()
    return db_wishlist
