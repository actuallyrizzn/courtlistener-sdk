#!/usr/bin/env python3
"""
Final integration test to verify all fixes work together.
"""

import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_final_integration():
    """Test the final integration of all fixes."""
    
    print("🚀 FINAL INTEGRATION TEST")
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
    
    # Test 2: Case names in opinions
    print("\n2️⃣ Testing case names in opinions...")
    try:
        opinions = client.opinions.list_opinions(page=1)
        if opinions:
            opinion = opinions[0]
            case_name = opinion.case_name
            print(f"✅ Opinion case name: {case_name}")
            if case_name == "Unknown Case":
                print("⚠️  Case name still showing as 'Unknown Case'")
            else:
                print("✅ Case name extracted successfully")
        else:
            print("⚠️  No opinions found")
    except Exception as e:
        if "HTTP 202" in str(e):
            print("⚠️  API returned HTTP 202 (Accepted) - likely rate limiting or async processing")
        else:
            print(f"❌ Opinion case name test failed: {e}")
    
    # Test 3: Case names in dockets
    print("\n3️⃣ Testing case names in dockets...")
    try:
        dockets = client.dockets.list_dockets(page=1)
        if dockets:
            docket = dockets[0]
            case_name = docket.case_name
            case_name_short = docket.case_name_short
            case_name_full = docket.case_name_full
            print(f"✅ Docket case name: {case_name}")
            print(f"✅ Docket case name short: {case_name_short}")
            print(f"✅ Docket case name full: {case_name_full}")
        else:
            print("⚠️  No dockets found")
    except Exception as e:
        if "HTTP 202" in str(e):
            print("⚠️  API returned HTTP 202 (Accepted) - likely rate limiting or async processing")
        else:
            print(f"❌ Docket case name test failed: {e}")
    
    # Test 4: Courts date parsing
    print("\n4️⃣ Testing courts date parsing...")
    try:
        courts = client.courts.list_courts(page=1)
        if courts:
            court = courts[0]
            start_date = court.start_date
            end_date = court.end_date
            print(f"✅ Court start date: {start_date}")
            print(f"✅ Court end date: {end_date}")
        else:
            print("⚠️  No courts found")
    except Exception as e:
        if "HTTP 202" in str(e):
            print("⚠️  API returned HTTP 202 (Accepted) - likely rate limiting or async processing")
        else:
            print(f"❌ Courts date parsing test failed: {e}")
    
    # Test 5: Available endpoints
    print("\n5️⃣ Testing available endpoints...")
    available_endpoints = [
        'courts', 'clusters', 'opinions', 'dockets', 
        'positions', 'financial', 'audio', 'search'
    ]
    
    for endpoint in available_endpoints:
        try:
            api = getattr(client, endpoint)
            # Check for the correct list method name
            if endpoint == 'financial':
                list_method_name = 'list_financial_disclosures'
            else:
                list_method_name = f"list_{endpoint}"
            
            if hasattr(api, list_method_name):
                print(f"✅ {endpoint} endpoint available with {list_method_name}")
            else:
                print(f"⚠️  {endpoint} endpoint available but no {list_method_name} method")
        except Exception as e:
            print(f"❌ {endpoint} endpoint failed: {e}")
    
    # Test 6: Disabled endpoints
    print("\n6️⃣ Testing disabled endpoints...")
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
    
    # Test 7: Search functionality
    print("\n7️⃣ Testing search functionality...")
    try:
        search_results = client.search.search("constitutional", page=1)
        if 'results' in search_results:
            print(f"✅ Search working - {len(search_results.get('results', []))} results")
        else:
            print("⚠️  Search returned unexpected format")
    except Exception as e:
        print(f"❌ Search test failed: {e}")
    
    # Test 8: Audio endpoint
    print("\n8️⃣ Testing audio endpoint...")
    try:
        audio_files = client.audio.list_audio(page=1)
        if audio_files is not None:
            print(f"✅ Audio endpoint working - {len(audio_files)} files")
        else:
            print("⚠️  Audio endpoint returned None")
    except Exception as e:
        print(f"❌ Audio test failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 FINAL INTEGRATION TEST COMPLETE")
    print("=" * 50)

if __name__ == "__main__":
    test_final_integration() 