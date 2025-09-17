#!/usr/bin/env python3
import sys
import importlib.metadata
import subprocess

def check_environment():
    print("🔍 Checking your Python environment...")
    
    # Check Python version
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    # Check installed packages using importlib.metadata (modern approach)
    print("\n📦 Checking essential packages:")
    
    essential_packages = [
        'flask', 'flask-sqlalchemy', 'flask-login', 
        'werkzeug', 'requests', 'python-dotenv', 'nltk'
    ]
    
    for package in essential_packages:
        try:
            version = importlib.metadata.version(package)
            print(f"  ✅ {package}=={version}")
        except importlib.metadata.PackageNotFoundError:
            print(f"  ❌ {package}: NOT installed")
        except Exception as e:
            print(f"  ⚠️  {package}: Error - {e}")
    
    # Test imports
    print("\n🧪 Testing imports:")
    modules_to_test = {
        'flask': 'Flask',
        'flask_sqlalchemy': 'SQLAlchemy',
        'flask_login': 'LoginManager',
        'werkzeug.security': 'generate_password_hash',
        'requests': 'get',
        'dotenv': 'load_dotenv',
        'nltk': 'download'
    }
    
    for module, attribute in modules_to_test.items():
        try:
            imported_module = __import__(module, fromlist=[attribute])
            print(f"  ✅ {module}")
        except ImportError as e:
            print(f"  ❌ {module}: {e}")
        except Exception as e:
            print(f"  ⚠️  {module}: {e}")
    
    print("\n🎯 Environment check complete!")

if __name__ == "__main__":
    check_environment()