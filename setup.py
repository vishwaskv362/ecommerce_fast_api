"""Setup script to initialize the application."""
import sys
import subprocess
from pathlib import Path


def run_command(command, description):
    """Run a shell command and print the result."""
    print(f"\n{'='*60}")
    print(f"⚡ {description}")
    print(f"{'='*60}")
    
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if result.stdout:
        print(result.stdout)
    
    if result.returncode != 0:
        print(f"❌ Error: {result.stderr}")
        return False
    else:
        print(f"✅ Success!")
    
    return True


def main():
    """Main setup function."""
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║     E-Commerce FastAPI - Setup Script                   ║
    ║     Production-Ready Configuration                       ║
    ╚══════════════════════════════════════════════════════════╝
    """)
    
    # Check Python version
    if sys.version_info < (3, 11):
        print("❌ Python 3.11 or higher is required!")
        sys.exit(1)
    
    print(f"✅ Python version: {sys.version}")
    
    # Install dependencies
    if not run_command(
        "pip install -r requirements.txt",
        "Installing dependencies"
    ):
        print("❌ Failed to install dependencies!")
        sys.exit(1)
    
    # Create .env file if it doesn't exist
    env_file = Path(".env")
    env_example = Path(".env.example")
    
    if not env_file.exists() and env_example.exists():
        print("\n📝 Creating .env file from .env.example")
        env_file.write_text(env_example.read_text())
        print("✅ Created .env file")
        print("⚠️  Please update the SECRET_KEY in .env file!")
    
    # Run Alembic migrations
    run_command(
        "alembic upgrade head",
        "Running database migrations"
    )
    
    # Create logs directory
    logs_dir = Path("logs")
    if not logs_dir.exists():
        logs_dir.mkdir()
        print("\n✅ Created logs directory")
    
    print("""
    ╔══════════════════════════════════════════════════════════╗
    ║              Setup Complete! 🎉                          ║
    ╠══════════════════════════════════════════════════════════╣
    ║  Next steps:                                             ║
    ║  1. Update SECRET_KEY in .env file                       ║
    ║  2. Run: uvicorn app.main:app --reload                   ║
    ║  3. Visit: http://localhost:8000/api/docs                ║
    ║                                                          ║
    ║  For Docker:                                             ║
    ║  - Development: docker-compose -f docker-compose.dev.yml up
    ║  - Production: docker-compose up                         ║
    ╚══════════════════════════════════════════════════════════╝
    """)


if __name__ == "__main__":
    main()
