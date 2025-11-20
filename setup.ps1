# E-Commerce FastAPI Setup (PowerShell)

Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║     E-Commerce FastAPI - Setup Script                   ║" -ForegroundColor Cyan
Write-Host "║     Production-Ready Configuration                       ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
Write-Host ""

# Check Python version
$pythonVersion = python --version 2>&1
Write-Host "✅ $pythonVersion" -ForegroundColor Green

# Create virtual environment
Write-Host ""
Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
python -m venv venv

# Activate virtual environment
Write-Host "⚡ Activating virtual environment..." -ForegroundColor Yellow
& ".\venv\Scripts\Activate.ps1"

# Install dependencies
Write-Host ""
Write-Host "📥 Installing dependencies..." -ForegroundColor Yellow
pip install --upgrade pip
pip install -r requirements.txt

# Create .env file
if ((-not (Test-Path .env)) -and (Test-Path .env.example)) {
    Write-Host ""
    Write-Host "📝 Creating .env file from .env.example..." -ForegroundColor Yellow
    Copy-Item .env.example .env
    Write-Host "✅ Created .env file" -ForegroundColor Green
    Write-Host "⚠️  Please update the SECRET_KEY in .env file!" -ForegroundColor Yellow
}

# Run migrations
Write-Host ""
Write-Host "🗄️  Running database migrations..." -ForegroundColor Yellow
alembic upgrade head

# Create logs directory
if (-not (Test-Path logs)) {
    New-Item -ItemType Directory -Path logs
    Write-Host "✅ Created logs directory" -ForegroundColor Green
}

Write-Host ""
Write-Host "╔══════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║              Setup Complete! 🎉                          ║" -ForegroundColor Cyan
Write-Host "╠══════════════════════════════════════════════════════════╣" -ForegroundColor Cyan
Write-Host "║  Next steps:                                             ║" -ForegroundColor Cyan
Write-Host "║  1. Update SECRET_KEY in .env file                       ║" -ForegroundColor Cyan
Write-Host "║  2. Activate venv: .\venv\Scripts\Activate.ps1           ║" -ForegroundColor Cyan
Write-Host "║  3. Run: uvicorn app.main:app --reload                   ║" -ForegroundColor Cyan
Write-Host "║  4. Visit: http://localhost:8000/api/docs                ║" -ForegroundColor Cyan
Write-Host "║                                                          ║" -ForegroundColor Cyan
Write-Host "║  For Docker:                                             ║" -ForegroundColor Cyan
Write-Host "║  - Development: docker-compose -f docker-compose.dev.yml up" -ForegroundColor Cyan
Write-Host "║  - Production: docker-compose up                         ║" -ForegroundColor Cyan
Write-Host "╚══════════════════════════════════════════════════════════╝" -ForegroundColor Cyan
