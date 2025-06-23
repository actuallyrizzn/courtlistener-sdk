#!/usr/bin/env python3
"""
Test script to verify all imports and API modules are working correctly.
"""

def test_imports():
    """Test all imports and API modules."""
    print("Testing imports...")
    
    # Test main package import
    try:
        import courtlistener
        print("✅ Main package import successful")
    except Exception as e:
        print(f"❌ Main package import failed: {e}")
        return False
    
    # Test client creation
    try:
        from courtlistener import CourtListenerClient
        client = CourtListenerClient(api_token="test_token")
        print("✅ Client creation successful")
    except Exception as e:
        print(f"❌ Client creation failed: {e}")
        return False
    
    # Test API modules
    api_modules = [
        'search', 'dockets', 'opinions', 'judges', 'courts',
        'parties', 'attorneys', 'documents', 'audio', 'financial',
        'citations', 'docket_entries', 'clusters', 'positions'
    ]
    
    for module in api_modules:
        try:
            api = getattr(client, module)
            print(f"✅ {module} API module accessible")
        except Exception as e:
            print(f"❌ {module} API module failed: {e}")
            return False
    
    # Test model imports
    try:
        from courtlistener.models import (
            DocketEntry, OpinionCluster, Position,
            Docket, Opinion, Judge, Court, Party, Attorney,
            Document, Audio, FinancialDisclosure, Citation
        )
        print("✅ All model imports successful")
    except Exception as e:
        print(f"❌ Model imports failed: {e}")
        return False
    
    print("\n🎉 All tests passed! All API endpoints are now available.")
    return True

if __name__ == "__main__":
    test_imports() 