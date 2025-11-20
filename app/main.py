"""Main FastAPI application with production-ready configuration."""
from datetime import datetime
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from contextlib import asynccontextmanager
import time

from .config import settings
from .database import init_db
from .core.logging import logger
from . import schemas

# Import routers
from .routers import auth, products, categories, cart, orders, reviews, wishlist, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events."""
    # Startup
    logger.info(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"Environment: {settings.ENVIRONMENT}")
    
    # Initialize database
    init_db()
    logger.info("Database initialized")
    
    yield
    
    # Shutdown
    logger.info("Shutting down application")


# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Modern E-Commerce API with FastAPI, SQLAlchemy, and JWT authentication",
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)


# ============ Middleware ============

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request Logging Middleware
@app.middleware("http")
async def log_requests(request: Request, call_next):
    """Log all requests with timing."""
    start_time = time.time()
    
    # Log request
    logger.info(f"Request: {request.method} {request.url.path}")
    
    # Process request
    response = await call_next(request)
    
    # Calculate duration
    duration = time.time() - start_time
    
    # Log response
    logger.info(
        f"Response: {request.method} {request.url.path} "
        f"Status: {response.status_code} Duration: {duration:.3f}s"
    )
    
    # Add custom headers
    response.headers["X-Process-Time"] = str(duration)
    
    return response


# ============ Exception Handlers ============

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle validation errors."""
    logger.error(f"Validation error: {exc.errors()}")
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": exc.errors(),
            "message": "Validation error"
        }
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "message": "Internal server error",
            "detail": str(exc) if settings.DEBUG else "An error occurred"
        }
    )


# ============ API Routes ============

# Include routers with API v1 prefix
API_V1_PREFIX = "/api/v1"

app.include_router(auth.router, prefix=f"{API_V1_PREFIX}/auth", tags=["Authentication"])
app.include_router(products.router, prefix=f"{API_V1_PREFIX}/products", tags=["Products"])
app.include_router(categories.router, prefix=f"{API_V1_PREFIX}/categories", tags=["Categories"])
app.include_router(cart.router, prefix=f"{API_V1_PREFIX}/cart", tags=["Cart"])
app.include_router(orders.router, prefix=f"{API_V1_PREFIX}/orders", tags=["Orders"])
app.include_router(reviews.router, prefix=f"{API_V1_PREFIX}/reviews", tags=["Reviews"])
app.include_router(wishlist.router, prefix=f"{API_V1_PREFIX}/wishlist", tags=["Wishlist"])

# Legacy routes (backwards compatibility)
app.include_router(users.router, prefix="/users", tags=["Users (Legacy)"])


# ============ Root Endpoints ============

@app.get("/", response_model=schemas.MessageResponse)
def read_root():
    """Root endpoint."""
    return {
        "message": f"Welcome to {settings.APP_NAME} API v{settings.APP_VERSION}"
    }


@app.get("/health", response_model=schemas.HealthResponse)
def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow()
    }


@app.get("/api", response_model=schemas.MessageResponse)
def api_info():
    """API information endpoint."""
    return {
        "message": f"{settings.APP_NAME} API",
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
