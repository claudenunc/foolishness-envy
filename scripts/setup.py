#!/usr/bin/env python3
"""
Setup script for N8N Agent Builder
"""

import os
import sys
import shutil


def check_python_version():
    """Check Python version"""
    if sys.version_info < (3, 8):
        print("Error: Python 3.8+ required")
        sys.exit(1)
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}")


def create_env_file():
    """Create .env file from template"""
    if os.path.exists(".env"):
        print("✓ .env file already exists")
        return

    if os.path.exists(".env.example"):
        shutil.copy(".env.example", ".env")
        print("✓ Created .env file from template")
        print("  Please edit .env and add your API keys")
    else:
        print("✗ .env.example not found")


def create_directories():
    """Create necessary directories"""
    dirs = [
        "data",
        "logs",
        "chroma_db",
        "templates/workflows"
    ]

    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)

    print(f"✓ Created {len(dirs)} directories")


def check_dependencies():
    """Check if dependencies are installed"""
    try:
        import dotenv
        import requests
        print("✓ Core dependencies installed")
        return True
    except ImportError:
        print("✗ Dependencies not installed")
        print("  Run: pip install -r requirements.txt")
        return False


def main():
    """Run setup"""
    print("=== N8N Agent Builder Setup ===\n")

    # Check Python version
    check_python_version()

    # Create directories
    create_directories()

    # Create .env file
    create_env_file()

    # Check dependencies
    deps_ok = check_dependencies()

    print("\n=== Setup Summary ===")
    print("Next steps:")
    print("1. Edit .env file and add your API keys:")
    print("   - N8N_API_KEY: Your n8n API key")
    print("   - N8N_BASE_URL: Your n8n instance URL")
    print("   - OPENAI_API_KEY: Your OpenAI API key")

    if not deps_ok:
        print("2. Install dependencies:")
        print("   pip install -r requirements.txt")

    print("3. Run examples:")
    print("   python examples/basic_usage.py")
    print("\n=== Setup complete ===")


if __name__ == "__main__":
    main()
