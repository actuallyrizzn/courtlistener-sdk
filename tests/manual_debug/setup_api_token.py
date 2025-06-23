#!/usr/bin/env python3
"""
Setup script for CourtListener API token and real data testing.
"""

import os
import sys
from pathlib import Path

def create_env_file():
    """Create .env file with API token prompt."""
    env_content = """# CourtListener API Configuration
# Fill in your actual API token from https://www.courtlistener.com/api/

# Your CourtListener API token (required)
# Get your token from: https://www.courtlistener.com/api/
COURTLISTENER_API_TOKEN=your_api_token_here

# Optional configuration
# COURTLISTENER_BASE_URL=https://www.courtlistener.com/api/rest/v4
# COURTLISTENER_TIMEOUT=30
# COURTLISTENER_MAX_RETRIES=3
"""
    
    env_path = Path('.env')
    if env_path.exists():
        print("⚠️  .env file already exists!")
        response = input("Do you want to overwrite it? (y/N): ")
        if response.lower() != 'y':
            print("Skipping .env file creation.")
            return
    
    print("📝 Creating .env file...")
    with open(env_path, 'w') as f:
        f.write(env_content)
    
    print("✅ .env file created!")
    print("\n🔑 Next steps:")
    print("1. Edit the .env file and replace 'your_api_token_here' with your actual API token")
    print("2. Get your API token from: https://www.courtlistener.com/api/")
    print("3. Run: python test_real_api.py")

def test_api_connection():
    """Test the API connection with real data."""
    try:
        from courtlistener import CourtListenerClient
        from courtlistener.exceptions import ValidationError, NotFoundError
        
        print("🔍 Testing API connection...")
        
        # Try to create client
        try:
            client = CourtListenerClient()
            print("✅ Client created successfully!")
        except ValidationError as e:
            print(f"❌ Configuration error: {e}")
            print("Please check your .env file and API token.")
            return False
        
        # Test a simple API call
        print("🌐 Testing API endpoints...")
        
        # Test courts endpoint
        try:
            courts = client.courts.list_courts(page=1)
            print(f"✅ Courts API: Found {len(courts)} courts")
        except Exception as e:
            print(f"❌ Courts API error: {e}")
        
        # Test opinions endpoint
        try:
            opinions = client.opinions.list_opinions(page=1)
            print(f"✅ Opinions API: Found {len(opinions)} opinions")
        except Exception as e:
            print(f"❌ Opinions API error: {e}")
        
        # Test dockets endpoint
        try:
            dockets = client.dockets.list_dockets(page=1)
            print(f"✅ Dockets API: Found {len(dockets)} dockets")
        except Exception as e:
            print(f"❌ Dockets API error: {e}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def main():
    """Main setup function."""
    print("🚀 CourtListener SDK Setup")
    print("=" * 40)
    
    # Check if .env exists
    if not Path('.env').exists():
        create_env_file()
    else:
        print("📁 .env file found!")
        response = input("Do you want to test the API connection now? (Y/n): ")
        if response.lower() == 'n':
            print("Run 'python test_real_api.py' when ready to test.")
            return
    
    # Test API connection
    if test_api_connection():
        print("\n🎉 Setup complete! You can now run tests with real data:")
        print("python -m pytest tests/ -v")
    else:
        print("\n⚠️  Setup incomplete. Please check your API token and try again.")

if __name__ == "__main__":
    main() 