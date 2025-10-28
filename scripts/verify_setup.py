#!/usr/bin/env python3
"""
Verify API keys and system setup
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_var(var_name, required=True):
    """Check if environment variable is set"""
    value = os.getenv(var_name)
    if value and not value.startswith("your_"):
        print(f"✓ {var_name}: Set")
        return True
    elif required:
        print(f"✗ {var_name}: Not set (REQUIRED)")
        return False
    else:
        print(f"⊘ {var_name}: Not set (optional)")
        return True

def check_n8n_connection():
    """Check if n8n is accessible"""
    import requests

    n8n_url = os.getenv("N8N_BASE_URL")
    if not n8n_url:
        print("✗ N8N_BASE_URL not set")
        return False

    try:
        response = requests.get(n8n_url, timeout=5)
        print(f"✓ n8n is running at {n8n_url}")
        return True
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to n8n at {n8n_url}")
        print("  Make sure n8n is running. Start it with: n8n start")
        return False
    except Exception as e:
        print(f"✗ Error connecting to n8n: {e}")
        return False

def check_openai_key():
    """Verify OpenAI API key"""
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

        # Try to list models to verify key
        models = client.models.list()
        print("✓ OpenAI API key is valid")
        return True
    except ImportError:
        print("⊘ OpenAI library not installed (run: pip install openai)")
        return False
    except Exception as e:
        print(f"✗ OpenAI API key error: {str(e)[:100]}")
        return False

def check_n8n_api():
    """Test n8n API connection"""
    try:
        import requests

        n8n_url = os.getenv("N8N_BASE_URL")
        n8n_key = os.getenv("N8N_API_KEY")

        if not n8n_url or not n8n_key:
            return False

        headers = {
            "X-N8N-API-KEY": n8n_key,
            "Content-Type": "application/json"
        }

        response = requests.get(
            f"{n8n_url}/api/v1/workflows",
            headers=headers,
            timeout=5
        )

        if response.status_code == 200:
            workflows = response.json().get("data", [])
            print(f"✓ n8n API key is valid ({len(workflows)} workflows found)")
            return True
        else:
            print(f"✗ n8n API error: {response.status_code}")
            return False

    except Exception as e:
        print(f"⊘ Cannot verify n8n API: {str(e)[:100]}")
        return False

def main():
    """Run all verification checks"""
    print("=" * 60)
    print("N8N Agent Builder - Setup Verification")
    print("=" * 60)

    print("\n1. Checking Required Environment Variables:")
    print("-" * 60)
    checks = []
    checks.append(check_env_var("N8N_API_KEY", required=True))
    checks.append(check_env_var("N8N_BASE_URL", required=True))
    checks.append(check_env_var("OPENAI_API_KEY", required=True))

    print("\n2. Checking Optional Environment Variables:")
    print("-" * 60)
    check_env_var("ANTHROPIC_API_KEY", required=False)
    check_env_var("OPENROUTER_API_KEY", required=False)
    check_env_var("PINECONE_API_KEY", required=False)

    print("\n3. Checking n8n Connection:")
    print("-" * 60)
    n8n_running = check_n8n_connection()

    print("\n4. Checking API Connections:")
    print("-" * 60)
    if n8n_running:
        check_n8n_api()
    else:
        print("⊘ Skipping n8n API check (n8n not running)")

    check_openai_key()

    print("\n" + "=" * 60)
    print("Summary:")
    print("=" * 60)

    if all(checks):
        print("✓ All required environment variables are set!")
    else:
        print("✗ Some required environment variables are missing.")
        print("  Please edit .env file and add missing keys.")

    if not n8n_running:
        print("\n⚠ n8n is not running!")
        print("\nTo start n8n:")
        print("  Option 1 (Docker): docker run -d -p 5678:5678 n8nio/n8n")
        print("  Option 2 (npm):    npx n8n")
        print("  Option 3 (global): n8n start")

    print("\n" + "=" * 60)
    print("Next Steps:")
    print("=" * 60)
    print("1. Make sure n8n is running")
    print("2. Run examples: python examples/basic_usage.py")
    print("3. Read the docs: README.md")
    print("=" * 60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nVerification cancelled.")
        sys.exit(0)
    except Exception as e:
        print(f"\nError during verification: {e}")
        sys.exit(1)
