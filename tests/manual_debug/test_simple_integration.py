#!/usr/bin/env python3
"""
Simple integration test that doesn't make API calls.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_simple_integration():
    """Test the SDK without making API calls."""
    
    print("🚀 SIMPLE INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: Import and initialization
    print("\n1️⃣ Testing imports and initialization...")
    try:
        from courtlistener import CourtListenerClient
        client = CourtListenerClient()
        print("✅ Client initialized successfully")
    except Exception as e:
        print(f"❌ Client initialization failed: {e}")
        return
    
    # Test 2: Check available endpoints
    print("\n2️⃣ Testing available endpoints...")
    available_endpoints = [
        'courts', 'clusters', 'opinions', 'dockets', 
        'positions', 'financial', 'audio', 'search'
    ]
    
    for endpoint in available_endpoints:
        try:
            api = getattr(client, endpoint)
            print(f"✅ {endpoint} endpoint available")
            
            # Check for list methods
            list_method_name = f"list_{endpoint.split('_')[0]}s"
            if hasattr(api, list_method_name):
                print(f"  ✅ {list_method_name} method available")
            else:
                print(f"  ⚠️  {list_method_name} method not found")
                
        except Exception as e:
            print(f"❌ {endpoint} endpoint failed: {e}")
    
    # Test 3: Check disabled endpoints
    print("\n3️⃣ Testing disabled endpoints...")
    disabled_endpoints = [
        'docket_entries', 'attorneys', 'parties', 
        'documents', 'judges', 'citations'
    ]
    
    for endpoint in disabled_endpoints:
        try:
            api = getattr(client, endpoint)
            # This should raise an exception
            api.some_method()
            print(f"❌ {endpoint} should be disabled but isn't")
        except Exception as e:
            if "disabled" in str(e).lower():
                print(f"✅ {endpoint} properly disabled")
            else:
                print(f"⚠️  {endpoint} error: {e}")
    
    # Test 4: Test model creation with sample data
    print("\n4️⃣ Testing model creation...")
    try:
        from courtlistener.models.docket import Docket
        from courtlistener.models.opinion import Opinion
        from courtlistener.models.court import Court
        
        # Test Docket model
        docket_data = {
            'id': 12345,
            'case_name': 'Test Case Name',
            'case_name_short': 'Test Case',
            'case_name_full': 'Test Case Full Name',
            'docket_number': '1:23-cv-456'
        }
        docket = Docket(docket_data)
        print(f"✅ Docket model: {docket.case_name}")
        
        # Test Opinion model
        opinion_data = {
            'id': 67890,
            'cluster': 'https://www.courtlistener.com/api/rest/v4/clusters/12345/',
            'author_str': 'Test Judge'
        }
        opinion = Opinion(opinion_data)
        print(f"✅ Opinion model: {opinion.case_name}")
        
        # Test Court model
        court_data = {
            'id': 'test-court',
            'short_name': 'Test Court',
            'full_name': 'Test Court Full Name'
        }
        court = Court(court_data)
        print(f"✅ Court model: {court.name}")
        
    except Exception as e:
        print(f"❌ Model creation test failed: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n" + "=" * 50)
    print("🎉 SIMPLE INTEGRATION TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    test_simple_integration() 