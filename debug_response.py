#!/usr/bin/env python3
"""
Debug script to examine actual API response structure.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def examine_api_response():
    """Examine the actual API response structure."""
    
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
    
    print("🔍 Examining API response structure...")
    print("=" * 50)
    
    # Test courts endpoint
    print("\n🏛️ Testing Courts endpoint...")
    try:
        response = requests.get(f"{base_url}/courts/", headers=headers, params={"page": 1}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'results' in data and data['results']:
                    first_court = data['results'][0]
                    print(f"First court keys: {list(first_court.keys())}")
                    print(f"First court sample: {json.dumps(first_court, indent=2)[:500]}...")
            elif isinstance(data, list) and data:
                print(f"First court keys: {list(data[0].keys())}")
                print(f"First court sample: {json.dumps(data[0], indent=2)[:500]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Test opinions endpoint
    print("\n📜 Testing Opinions endpoint...")
    try:
        response = requests.get(f"{base_url}/opinions/", headers=headers, params={"page": 1}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'results' in data and data['results']:
                    first_opinion = data['results'][0]
                    print(f"First opinion keys: {list(first_opinion.keys())}")
                    print(f"First opinion sample: {json.dumps(first_opinion, indent=2)[:500]}...")
            elif isinstance(data, list) and data:
                print(f"First opinion keys: {list(data[0].keys())}")
                print(f"First opinion sample: {json.dumps(data[0], indent=2)[:500]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Test people endpoint
    print("\n👥 Testing People endpoint...")
    try:
        response = requests.get(f"{base_url}/people/", headers=headers, params={"page": 1}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print(f"Response type: {type(data)}")
            
            if isinstance(data, dict):
                print(f"Keys: {list(data.keys())}")
                if 'results' in data and data['results']:
                    first_person = data['results'][0]
                    print(f"First person keys: {list(first_person.keys())}")
                    print(f"First person sample: {json.dumps(first_person, indent=2)[:500]}...")
            elif isinstance(data, list) and data:
                print(f"First person keys: {list(data[0].keys())}")
                print(f"First person sample: {json.dumps(data[0], indent=2)[:500]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    examine_api_response() 