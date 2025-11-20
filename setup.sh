#!/bin/bash

# Setup script for Unix/Linux/Mac

echo "╔══════════════════════════════════════════════════════════╗"
echo "║     E-Commerce FastAPI - Setup Script                   ║"
echo "║     Production-Ready Configuration                       ║"
echo "╚══════════════════════════════════════════════════════════╝"
echo ""

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Python version: $python_version"

# Create virtual environment
echo ""
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "⚡ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo ""
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
if [ ! -f .env ] && [ -f .env.example ]; then
    echo ""
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "✅ Created .env file"
    echo "⚠️  Please update the SECRET_KEY in .env file!"
fi

# Run migrations
echo ""
echo "🗄️  Running database migrations..."
alembic upgrade head

# Create logs directory
if [ ! -d "logs" ]; then
    mkdir logs
    echo "✅ Created logs directory"
fi

echo ""
echo "╔══════════════════════════════════════════════════════════╗"
echo "║              Setup Complete! 🎉                          ║"
echo "╠══════════════════════════════════════════════════════════╣"
echo "║  Next steps:                                             ║"
echo "║  1. Update SECRET_KEY in .env file                       ║"
echo "║  2. Activate venv: source venv/bin/activate              ║"
echo "║  3. Run: uvicorn app.main:app --reload                   ║"
echo "║  4. Visit: http://localhost:8000/api/docs                ║"
echo "║                                                          ║"
echo "║  For Docker:                                             ║"
echo "║  - Development: docker-compose -f docker-compose.dev.yml up"
echo "║  - Production: docker-compose up                         ║"
echo "╚══════════════════════════════════════════════════════════╝"
