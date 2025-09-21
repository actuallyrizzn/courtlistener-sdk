#!/usr/bin/env python3
"""
Debug script to examine case name fields in opinions and dockets.
"""

import requests
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def examine_case_names():
    """Examine the actual case name fields in API responses."""
    
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
    
    print("🔍 Examining case name fields...")
    print("=" * 50)
    
    # Test opinions endpoint
    print("\n📜 Testing Opinions endpoint for case names...")
    try:
        response = requests.get(f"{base_url}/opinions/", headers=headers, params={"page": 1}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and data['results']:
                first_opinion = data['results'][0]
                print(f"Opinion keys: {list(first_opinion.keys())}")
                print(f"Case name related fields:")
                for key, value in first_opinion.items():
                    if 'case' in key.lower() or 'name' in key.lower():
                        print(f"  {key}: {value}")
                print(f"Full opinion sample: {json.dumps(first_opinion, indent=2)[:1000]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Test dockets endpoint
    print("\n📁 Testing Dockets endpoint for case names...")
    try:
        response = requests.get(f"{base_url}/dockets/", headers=headers, params={"page": 1}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and data['results']:
                first_docket = data['results'][0]
                print(f"Docket keys: {list(first_docket.keys())}")
                print(f"Case name related fields:")
                for key, value in first_docket.items():
                    if 'case' in key.lower() or 'name' in key.lower():
                        print(f"  {key}: {value}")
                print(f"Full docket sample: {json.dumps(first_docket, indent=2)[:1000]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")
    
    # Test clusters endpoint (which should have case names)
    print("\n📊 Testing Clusters endpoint for case names...")
    try:
        response = requests.get(f"{base_url}/clusters/", headers=headers, params={"page": 1}, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if 'results' in data and data['results']:
                first_cluster = data['results'][0]
                print(f"Cluster keys: {list(first_cluster.keys())}")
                print(f"Case name related fields:")
                for key, value in first_cluster.items():
                    if 'case' in key.lower() or 'name' in key.lower():
                        print(f"  {key}: {value}")
                print(f"Full cluster sample: {json.dumps(first_cluster, indent=2)[:1000]}...")
        else:
            print(f"Error response: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    examine_case_names() 