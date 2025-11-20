# 🛒 E-Commerce FastAPI - Production Ready

A modern, production-ready e-commerce REST API built with FastAPI, featuring JWT authentication, caching, pagination, and comprehensive CRUD operations.

## ✨ Features

### Core Features
- 🔐 **JWT Authentication** with access and refresh tokens
- 📦 **Product Management** with categories and filtering
- 🛍️ **Shopping Cart** functionality
- 📋 **Order Management** with status tracking
- ⭐ **Product Reviews** and ratings
- ❤️ **Wishlist** functionality
- 👤 **User Profile Management**

### Technical Features
- ⚡ **Redis Caching** for improved performance
- 📄 **Pagination** for all list endpoints
- 🔍 **Advanced Filtering** and search
- 🔒 **Password Hashing** with bcrypt
- 📝 **Request Logging** and monitoring
- 🐳 **Docker** containerization
- 🔄 **Database Migrations** with Alembic
- ✅ **Pydantic V2** for validation
- 🏗️ **Repository Pattern** for clean architecture
- 🚦 **Error Handling** with custom exceptions

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose (optional)
- Redis (optional, for caching)

### Installation

#### Option 1: Local Development

1. **Clone the repository**
```bash
git clone https://github.com/vishwaskv362/ecommerce_fast_api.git
cd ecommerce_fast_api
```

2. **Create and activate virtual environment**
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your configuration
```

5. **Run database migrations**
```bash
alembic upgrade head
```

6. **Start the application**
```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

#### Option 2: Docker Deployment

**Development Mode** (with hot reload):
```bash
docker-compose -f docker-compose.dev.yml up --build
```

**Production Mode**:
```bash
docker-compose up --build
```

**With Nginx Reverse Proxy**:
```bash
docker-compose --profile production up --build
```

## 📚 API Documentation

Once the application is running, access:
- **Swagger UI**: http://localhost:8000/api/docs
- **ReDoc**: http://localhost:8000/api/redoc
- **OpenAPI JSON**: http://localhost:8000/api/openapi.json

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/auth/register` | Register new user | ❌ |
| POST | `/api/v1/auth/login` | Login and get tokens | ❌ |
| POST | `/api/v1/auth/refresh` | Refresh access token | ❌ |
| GET | `/api/v1/auth/me` | Get current user | ✅ |
| PUT | `/api/v1/auth/me` | Update user profile | ✅ |

### Products
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/products` | List products (paginated) | ✅ |
| GET | `/api/v1/products/{id}` | Get product details | ✅ |
| POST | `/api/v1/products` | Create product | ✅ |
| PUT | `/api/v1/products/{id}` | Update product | ✅ |
| DELETE | `/api/v1/products/{id}` | Delete product | ✅ |

**Query Parameters for List:**
- `page` - Page number (default: 1)
- `page_size` - Items per page (default: 20, max: 100)
- `search` - Search in name/description
- `category_id` - Filter by category
- `min_price` - Minimum price filter
- `max_price` - Maximum price filter

### Categories
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/categories` | List all categories | ✅ |
| GET | `/api/v1/categories/{id}` | Get category details | ✅ |
| POST | `/api/v1/categories` | Create category | ✅ |

### Shopping Cart
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/cart` | Get user's cart | ✅ |
| POST | `/api/v1/cart/items` | Add item to cart | ✅ |
| PUT | `/api/v1/cart/items/{id}` | Update cart item quantity | ✅ |
| DELETE | `/api/v1/cart/items/{id}` | Remove item from cart | ✅ |
| DELETE | `/api/v1/cart` | Clear entire cart | ✅ |

### Orders
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/orders` | Create new order | ✅ |
| GET | `/api/v1/orders` | List user's orders (paginated) | ✅ |
| GET | `/api/v1/orders/{id}` | Get order details | ✅ |
| PATCH | `/api/v1/orders/{id}/status` | Update order status | ✅ |

### Reviews
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/v1/reviews` | Create product review | ✅ |
| GET | `/api/v1/reviews/product/{id}` | Get product reviews (paginated) | ✅ |
| PUT | `/api/v1/reviews/{id}` | Update review | ✅ |
| DELETE | `/api/v1/reviews/{id}` | Delete review | ✅ |

### Wishlist
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/v1/wishlist` | Get user's wishlist (paginated) | ✅ |
| POST | `/api/v1/wishlist` | Add item to wishlist | ✅ |
| DELETE | `/api/v1/wishlist/{id}` | Remove item from wishlist | ✅ |

### Health & Info
| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Root message | ❌ |
| GET | `/health` | Health check | ❌ |
| GET | `/api` | API info | ❌ |

## 🔐 Authentication

The API uses JWT (JSON Web Tokens) for authentication.

### Getting Tokens

1. **Register a new user:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/register" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "username": "johndoe",
    "email": "john@example.com",
    "password": "securepassword123",
    "phone_number": "+1234567890"
  }'
```

2. **Login to get tokens:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/login" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=johndoe&password=securepassword123"
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer"
}
```

3. **Use the access token in requests:**
```bash
curl -X GET "http://localhost:8000/api/v1/products" \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

4. **Refresh expired access token:**
```bash
curl -X POST "http://localhost:8000/api/v1/auth/refresh" \
  -H "Content-Type: application/json" \
  -d '{"refresh_token": "YOUR_REFRESH_TOKEN"}'
```

## 🗄️ Database

The application uses SQLite by default for easy setup. For production, consider PostgreSQL or MySQL.

### Database Migrations

**Create a new migration:**
```bash
alembic revision --autogenerate -m "description"
```

**Apply migrations:**
```bash
alembic upgrade head
```

**Rollback migration:**
```bash
alembic downgrade -1
```

## ⚙️ Configuration

Configuration is managed through environment variables. Copy `.env.example` to `.env` and customize:

```env
# Security
SECRET_KEY=your-super-secret-key-min-32-characters

# Database
DATABASE_URL=sqlite:///./ecommerce.db

# Redis Cache
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_ENABLED=false

# JWT
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

# Pagination
DEFAULT_PAGE_SIZE=20
MAX_PAGE_SIZE=100
```

## 🏗️ Project Structure

```
ecommerce_fast_api/
├── app/
│   ├── core/                  # Core functionality
│   │   ├── cache.py          # Redis caching
│   │   ├── logging.py        # Logging configuration
│   │   ├── pagination.py     # Pagination utilities
│   │   └── security.py       # Authentication & security
│   ├── routers/              # API route handlers
│   │   ├── auth.py           # Authentication endpoints
│   │   ├── products.py       # Product endpoints
│   │   ├── categories.py     # Category endpoints
│   │   ├── cart.py           # Shopping cart endpoints
│   │   ├── orders.py         # Order endpoints
│   │   ├── reviews.py        # Review endpoints
│   │   └── wishlist.py       # Wishlist endpoints
│   ├── config.py             # Configuration management
│   ├── crud.py               # Database operations
│   ├── database.py           # Database connection
│   ├── main.py               # FastAPI application
│   ├── models.py             # SQLAlchemy models
│   └── schemas.py            # Pydantic schemas
├── alembic/                  # Database migrations
├── logs/                     # Application logs
├── .env                      # Environment variables
├── .env.example              # Example environment file
├── docker-compose.yml        # Production Docker setup
├── docker-compose.dev.yml    # Development Docker setup
├── Dockerfile                # Docker image definition
├── nginx.conf                # Nginx configuration
├── requirements.txt          # Python dependencies
└── README.md                 # This file
```

## 🔧 Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black app/
isort app/
```

### Linting
```bash
flake8 app/
pylint app/
```

## 🚢 Deployment

### Docker Production Deployment

1. **Build and start services:**
```bash
docker-compose up -d --build
```

2. **View logs:**
```bash
docker-compose logs -f api
```

3. **Stop services:**
```bash
docker-compose down
```

### Environment Variables for Production

Ensure these are set in your production environment:
- `SECRET_KEY` - Strong secret key (min 32 characters)
- `DATABASE_URL` - Production database URL
- `REDIS_ENABLED=true` - Enable caching
- `DEBUG=false` - Disable debug mode
- `ENVIRONMENT=production`

## 📊 Performance Optimizations

- **Database Indexing**: Indexed on frequently queried fields
- **Query Optimization**: Using joinedload for relationships
- **Redis Caching**: Reduces database load
- **Connection Pooling**: Efficient database connections
- **Pagination**: Limits data transfer
- **Lazy Loading**: Optimized relationship loading

## 🔒 Security Features

- ✅ Password hashing with bcrypt
- ✅ JWT token authentication
- ✅ Token expiration and refresh
- ✅ CORS configuration
- ✅ SQL injection protection (SQLAlchemy ORM)
- ✅ Input validation with Pydantic
- ✅ Rate limiting ready
- ✅ Foreign key constraints

## 📝 Logging

Logs are stored in the `logs/` directory:
- `app.log` - All application logs
- `error.log` - Error logs only

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👤 Author

**Vishwas KV**
- GitHub: [@vishwaskv362](https://github.com/vishwaskv362)

## 🙏 Acknowledgments

- FastAPI for the amazing framework
- SQLAlchemy for robust ORM
- Pydantic for data validation
- Redis for caching capabilities

---

Made with ❤️ using FastAPI
