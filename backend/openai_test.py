"""
OpenAI API Test Script

This script tests the OpenAI API connection and validates the configuration.
Run this to verify your API key and settings before starting the application.

Usage:
    python backend/openai_test.py
"""

import sys
from pathlib import Path

# Add parent directory to path to allow imports when running directly
if __name__ == "__main__":
    sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from openai import OpenAI
from backend.config import Config
from backend.utils import setup_logger

logger = setup_logger(__name__)


def test_configuration():
    """Test if configuration is valid."""
    print("\n" + "=" * 60)
    print("🔧 Testing Configuration...")
    print("=" * 60)
    
    try:
        Config.validate()
        print("✅ Configuration validation successful")
        print(f"   - OpenAI Model: {Config.OPENAI_MODEL}")
        print(f"   - Temperature: {Config.TEMPERATURE}")
        print(f"   - Max Tokens: {Config.MAX_TOKENS}")
        print(f"   - Data Directory: {Config.DATA_DIR}")
        return True
    except Exception as e:
        print(f"❌ Configuration validation failed: {e}")
        return False


def test_api_connection():
    """Test the OpenAI API connection."""
    print("\n" + "=" * 60)
    print("🔌 Testing OpenAI API Connection...")
    print("=" * 60)
    
    try:
        client = OpenAI(api_key=Config.OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model=Config.OPENAI_MODEL,
            messages=[
                {"role": "system", "content": "Du bist ein hilfreicher politischer Chatbot."},
                {"role": "user", "content": "Was hält die Ökologische Partei von Atomkraft?"}
            ],
            temperature=Config.TEMPERATURE,
            max_tokens=Config.MAX_TOKENS
        )
        
        print("✅ OpenAI API connection successful!\n")
        print("📝 Test Response:")
        print("-" * 60)
        print(response.choices[0].message.content)
        print("-" * 60)
        print(f"\n📊 Usage: {response.usage.total_tokens} tokens")
        return True
        
    except Exception as e:
        print(f"❌ OpenAI API connection failed:")
        print(f"   Error: {str(e)}")
        logger.error(f"API test failed: {e}", exc_info=True)
        return False


def test_data_files():
    """Test if all required data files exist and are valid."""
    print("\n" + "=" * 60)
    print("📁 Testing Data Files...")
    print("=" * 60)
    
    import json
    
    files_to_check = {
        "Knowledge Base": Config.KNOWLEDGE_BASE_PATH,
        "Parties Info": Config.PARTIES_INFO_PATH,
        "System Prompt": Config.SYSTEM_PROMPT_PATH,
        "FAQs": Config.FAQS_PATH
    }
    
    all_valid = True
    
    for name, path in files_to_check.items():
        if path.exists():
            try:
                if path.suffix == '.json':
                    with open(path, 'r', encoding='utf-8') as f:
                        json.load(f)
                else:
                    with open(path, 'r', encoding='utf-8') as f:
                        f.read()
                print(f"✅ {name}: {path.name}")
            except Exception as e:
                print(f"❌ {name}: Invalid - {e}")
                all_valid = False
        else:
            print(f"❌ {name}: Not found at {path}")
            all_valid = False
    
    return all_valid


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("🚀 Wahl-Chatbot OpenAI Configuration Test")
    print("=" * 60)
    
    results = {
        "Configuration": test_configuration(),
        "Data Files": test_data_files(),
        "API Connection": test_api_connection()
    }
    
    print("\n" + "=" * 60)
    print("📋 Test Summary")
    print("=" * 60)
    
    for test_name, passed in results.items():
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{test_name}: {status}")
    
    all_passed = all(results.values())
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 All tests passed! Your application is ready to run.")
        print("   Run: python backend/app.py")
    else:
        print("⚠️  Some tests failed. Please fix the issues above.")
    print("=" * 60 + "\n")
    
    return 0 if all_passed else 1


if __name__ == "__main__":
    exit(main())
