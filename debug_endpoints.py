#!/usr/bin/env python3
"""
Debug script to test all API endpoints and identify which ones are available.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_endpoints():
    """Test all API endpoints to see which ones are available."""
    
    api_token = os.getenv('COURTLISTENER_API_TOKEN')
    if not api_token:
        print("❌ No API token found in .env file")
        return
    
    base_url = "https://www.courtlistener.com/api/rest/v4"
    headers = {
        "Authorization": f"Token {api_token}",
        "Content-Type": "application/json",
        "User-Agent": "CourtListener-SDK-Debug/0.1.0"
    }
    
    # List of all endpoints to test
    endpoints = [
        "courts/",
        "clusters/",
        "opinions/",
        "dockets/",
        "docket-entries/",
        "documents/",
        "attorneys/",
        "judges/",
        "parties/",
        "positions/",
        "financial-disclosures/",
        "citations/",
        "audio/",
        "search/",
    ]
    
    print("🔍 Testing all API endpoints...")
    print("=" * 60)
    
    results = {}
    
    for endpoint in endpoints:
        print(f"\n📡 Testing {endpoint}...")
        try:
            response = requests.get(f"{base_url}/{endpoint}", headers=headers, params={"page": 1}, timeout=10)
            status = response.status_code
            print(f"  Status: {status}")
            
            if status == 200:
                data = response.json()
                count = data.get('count', 0) if isinstance(data, dict) else 0
                print(f"  ✅ Available - {count} results")
                results[endpoint] = {"status": "available", "count": count}
            elif status == 403:
                print(f"  🔒 Forbidden - Requires permissions")
                results[endpoint] = {"status": "forbidden", "count": 0}
            elif status == 404:
                print(f"  ❌ Not Found - Endpoint doesn't exist")
                results[endpoint] = {"status": "not_found", "count": 0}
            else:
                print(f"  ⚠️  Other error: {response.text[:100]}...")
                results[endpoint] = {"status": f"error_{status}", "count": 0}
                
        except Exception as e:
            print(f"  💥 Exception: {e}")
            results[endpoint] = {"status": "exception", "count": 0}
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 ENDPOINT SUMMARY")
    print("=" * 60)
    
    available = []
    forbidden = []
    not_found = []
    errors = []
    
    for endpoint, result in results.items():
        if result["status"] == "available":
            available.append(f"{endpoint} ({result['count']} results)")
        elif result["status"] == "forbidden":
            forbidden.append(endpoint)
        elif result["status"] == "not_found":
            not_found.append(endpoint)
        else:
            errors.append(f"{endpoint} ({result['status']})")
    
    print(f"\n✅ AVAILABLE ({len(available)}):")
    for endpoint in available:
        print(f"  • {endpoint}")
    
    print(f"\n🔒 FORBIDDEN ({len(forbidden)}):")
    for endpoint in forbidden:
        print(f"  • {endpoint}")
    
    print(f"\n❌ NOT FOUND ({len(not_found)}):")
    for endpoint in not_found:
        print(f"  • {endpoint}")
    
    if errors:
        print(f"\n⚠️  ERRORS ({len(errors)}):")
        for endpoint in errors:
            print(f"  • {endpoint}")

if __name__ == "__main__":
    test_endpoints() 