#!/usr/bin/env python3
"""
Debug script to investigate the Docket API response structure.
"""

import os
import json
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def debug_docket_api():
    """Debug the Docket API response structure."""
    
    print("🔍 Debugging Docket API response structure...")
    print("=" * 50)
    
    try:
        from courtlistener import CourtListenerClient
        client = CourtListenerClient()
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return
    
    # Test 1: Try to get dockets and examine the response
    print("\n1️⃣ Testing Docket API response...")
    try:
        dockets = client.dockets.list_dockets(page=1)
        print(f"✅ Got {len(dockets) if dockets else 0} dockets")
        
        if dockets and len(dockets) > 0:
            docket = dockets[0]
            print(f"✅ First docket ID: {docket.id}")
            print(f"✅ First docket type: {type(docket)}")
            print(f"✅ First docket dir: {dir(docket)[:10]}...")  # First 10 attributes
            
            # Try to access case_name
            try:
                case_name = docket.case_name
                print(f"✅ Case name accessed: {case_name}")
            except Exception as e:
                print(f"❌ Case name access failed: {e}")
                print(f"   Available attributes: {[attr for attr in dir(docket) if not attr.startswith('_')]}")
                
            # Try to access _data directly
            try:
                print(f"✅ _data keys: {list(docket._data.keys())}")
                if 'case_name' in docket._data:
                    print(f"✅ case_name in _data: {docket._data['case_name']}")
                else:
                    print("❌ case_name not in _data")
            except Exception as e:
                print(f"❌ _data access failed: {e}")
                
        else:
            print("⚠️  No dockets returned")
            
    except Exception as e:
        print(f"❌ Docket API test failed: {e}")
        if "HTTP 202" in str(e):
            print("   This is expected - API is rate limiting or processing asynchronously")
    
    # Test 2: Create a mock docket to verify the model works
    print("\n2️⃣ Testing Docket model with mock data...")
    try:
        from courtlistener.models.docket import Docket
        
        mock_data = {
            'id': 12345,
            'case_name': 'Mock Case Name',
            'case_name_short': 'Mock Case',
            'case_name_full': 'Mock Case Full Name',
            'docket_number': '1:23-cv-456'
        }
        
        mock_docket = Docket(mock_data)
        print(f"✅ Mock docket created: {mock_docket.case_name}")
        print(f"✅ Mock docket has case_name: {hasattr(mock_docket, 'case_name')}")
        
    except Exception as e:
        print(f"❌ Mock docket test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_docket_api() 