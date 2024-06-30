from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.products import router as product_router
from .routers.users import router as user_router
from .routers.wishlist import router as wishlist_router

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user_router, prefix="/users", tags=["users"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(wishlist_router, prefix="/wishlists", tags=["wishlists"])


@app.get("/")
def read_root():
    return {"message": "Backend is alive and kicking"}
