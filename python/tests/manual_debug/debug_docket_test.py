#!/usr/bin/env python3
"""
Debug script to test the Docket model directly.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_docket_model():
    """Test the Docket model directly."""
    
    print("🔍 Testing Docket model directly...")
    print("=" * 40)
    
    # Test 1: Import
    try:
        from courtlistener.models.docket import Docket
        print("✅ Docket model imported successfully")
    except Exception as e:
        print(f"❌ Docket model import failed: {e}")
        return
    
    # Test 2: Create Docket with sample data
    try:
        sample_data = {
            'id': 12345,
            'case_name': 'Test Case Name',
            'case_name_short': 'Test Case',
            'case_name_full': 'Test Case Full Name',
            'docket_number': '1:23-cv-456',
            'court_id': 'test-court'
        }
        
        docket = Docket(sample_data)
        print("✅ Docket created successfully")
        
        # Test 3: Access properties
        print(f"✅ Docket ID: {docket.id}")
        print(f"✅ Case name: {docket.case_name}")
        print(f"✅ Case name short: {docket.case_name_short}")
        print(f"✅ Case name full: {docket.case_name_full}")
        print(f"✅ Docket number: {docket.docket_number}")
        
        # Test 4: Check if properties exist
        print(f"✅ Has id property: {hasattr(docket, 'id')}")
        print(f"✅ Has case_name property: {hasattr(docket, 'case_name')}")
        print(f"✅ Has case_name_short property: {hasattr(docket, 'case_name_short')}")
        print(f"✅ Has case_name_full property: {hasattr(docket, 'case_name_full')}")
        
    except Exception as e:
        print(f"❌ Docket model test failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_docket_model() 