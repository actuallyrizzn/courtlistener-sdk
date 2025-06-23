#!/usr/bin/env python3
"""
Debug script to test CourtListener API endpoints and see what's available.
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_api_endpoints():
    """Test various API endpoints to see what's available."""
    
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
    
    print("🔍 Testing CourtListener API endpoints...")
    print(f"Base URL: {base_url}")
    print(f"Token: {api_token[:10]}...")
    print("=" * 60)
    
    # Test different endpoint variations
    endpoints_to_test = [
        "/courts/",
        "/opinions/",
        "/dockets/",
        "/judges/",
        "/clusters/",
        "/documents/",
        "/audio/",
        "/attorneys/",
        "/parties/",
        "/positions/",
        "/citations/",
        "/financial-disclosures/",
        "/docket-entries/",
        "/search/",
        "/",  # Root endpoint
    ]
    
    for endpoint in endpoints_to_test:
        url = base_url + endpoint
        print(f"\n🔗 Testing: {endpoint}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            print(f"   Status: {response.status_code}")
            print(f"   Content-Type: {response.headers.get('content-type', 'unknown')}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if isinstance(data, dict):
                        if 'count' in data:
                            print(f"   ✅ Found {data['count']} items")
                        elif 'results' in data:
                            print(f"   ✅ Found {len(data['results'])} results")
                        else:
                            print(f"   ✅ Response keys: {list(data.keys())}")
                    elif isinstance(data, list):
                        print(f"   ✅ Found {len(data)} items")
                    else:
                        print(f"   ✅ Response type: {type(data)}")
                except:
                    print(f"   ✅ Response length: {len(response.text)} chars")
            elif response.status_code == 404:
                print(f"   ❌ Not found")
            elif response.status_code == 401:
                print(f"   ❌ Unauthorized - check API token")
            elif response.status_code == 403:
                print(f"   ❌ Forbidden - check API permissions")
            else:
                print(f"   ⚠️ Unexpected status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"   ❌ Request error: {e}")
        except Exception as e:
            print(f"   ❌ Unexpected error: {e}")

def test_api_root():
    """Test the API root to see available endpoints."""
    
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
    
    print("\n🌐 Testing API root endpoint...")
    try:
        response = requests.get(base_url, headers=headers, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            try:
                data = response.json()
                print("Available endpoints:")
                for key, value in data.items():
                    print(f"  - {key}: {value}")
            except:
                print(f"Response: {response.text[:500]}...")
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
    test_api_root() 