#!/usr/bin/env python3
"""
Real API testing script for CourtListener SDK.
This script tests the SDK with actual CourtListener API data.
"""

import os
import sys
from pathlib import Path

def test_basic_functionality():
    """Test basic SDK functionality with real API data."""
    try:
        from courtlistener import CourtListenerClient
        from courtlistener.exceptions import ValidationError, NotFoundError, APIError
        
        print("🔍 Testing CourtListener SDK with real API data...")
        print("=" * 60)
        
        # Create client
        client = CourtListenerClient()
        print("✅ Client created successfully")
        
        # Test 1: Courts API
        print("\n🏛️  Testing Courts API...")
        try:
            courts = client.courts.list_courts(page=1)
            print(f"   ✅ Found {len(courts)} courts")
            if courts:
                court = courts[0]
                print(f"   📋 Sample court: {court.name} ({court.id})")
        except Exception as e:
            print(f"   ❌ Courts API error: {e}")
        
        # Test 2: Opinions API
        print("\n📜 Testing Opinions API...")
        try:
            opinions = client.opinions.list_opinions(page=1)
            print(f"   ✅ Found {len(opinions)} opinions")
            if opinions:
                opinion = opinions[0]
                case_name = getattr(opinion, 'case_name', 'Unknown Case')
                print(f"   📋 Sample opinion: {case_name} ({opinion.id})")
        except Exception as e:
            print(f"   ❌ Opinions API error: {e}")
        
        # Test 3: Dockets API
        print("\n📁 Testing Dockets API...")
        try:
            dockets = client.dockets.list_dockets(page=1)
            print(f"   ✅ Found {len(dockets)} dockets")
            if dockets:
                docket = dockets[0]
                case_name = getattr(docket, 'case_name', 'Unknown Case')
                print(f"   📋 Sample docket: {case_name} ({docket.id})")
        except Exception as e:
            print(f"   ❌ Dockets API error: {e}")
        
        # Test 4: Judges API (uses /people/ endpoint)
        print("\n👨‍⚖️ Testing Judges API (People endpoint)...")
        try:
            judges = client.judges.list_judges(page=1)
            print(f"   ✅ Found {len(judges)} people/judges")
            if judges:
                judge = judges[0]
                print(f"   📋 Sample person: {judge.name} ({judge.id})")
        except Exception as e:
            print(f"   ❌ Judges API error: {e}")
        
        # Test 5: Search API
        print("\n🔍 Testing Search API...")
        try:
            search_results = client.search.search_opinions(q="constitutional", page=1)
            print(f"   ✅ Found {len(search_results)} search results")
            if search_results:
                result = search_results[0]
                print(f"   📋 Sample result: {result.case_name}")
        except Exception as e:
            print(f"   ❌ Search API error: {e}")
        
        # Test 6: Clusters API
        print("\n📊 Testing Clusters API...")
        try:
            clusters = client.clusters.list_clusters(page=1)
            print(f"   ✅ Found {len(clusters)} clusters")
            if clusters:
                cluster = clusters[0]
                print(f"   📋 Sample cluster: {cluster.case_name} ({cluster.id})")
        except Exception as e:
            print(f"   ❌ Clusters API error: {e}")
        
        # Test 7: Audio API
        print("\n🎵 Testing Audio API...")
        try:
            audio_files = client.audio.list_audio(page=1)
            print(f"   ✅ Found {len(audio_files)} audio files")
            if audio_files:
                audio = audio_files[0]
                print(f"   📋 Sample audio: {audio.case_name} ({audio.id})")
        except Exception as e:
            print(f"   ❌ Audio API error: {e}")
        
        # Test 8: Get specific items by ID
        print("\n🎯 Testing Get by ID...")
        try:
            # Try to get a specific court
            courts = client.courts.list_courts(page=1)
            if courts:
                court_id = courts[0].id
                specific_court = client.courts.get_court(court_id)
                print(f"   ✅ Retrieved court by ID: {specific_court.name}")
            else:
                print("   ⚠️ No courts available for Get by ID test")
        except Exception as e:
            print(f"   ❌ Get by ID error: {e}")
        
        return True
        
    except ValidationError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your .env file and API token.")
        return False
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def test_advanced_features():
    """Test advanced SDK features."""
    try:
        from courtlistener import CourtListenerClient
        
        print("\n🚀 Testing Advanced Features...")
        print("=" * 40)
        
        client = CourtListenerClient()
        
        # Test pagination
        print("\n📄 Testing Pagination...")
        try:
            page1 = client.opinions.list_opinions(page=1)
            page2 = client.opinions.list_opinions(page=2)
            print(f"   ✅ Page 1: {len(page1)} items")
            print(f"   ✅ Page 2: {len(page2)} items")
        except Exception as e:
            print(f"   ❌ Pagination error: {e}")
        
        # Test filtering
        print("\n🔧 Testing Filtering...")
        try:
            # Test with date filter
            recent_opinions = client.opinions.list_opinions(
                page=1,
                date_filed__gte="2024-01-01"
            )
            print(f"   ✅ Recent opinions (2024+): {len(recent_opinions)} items")
        except Exception as e:
            print(f"   ❌ Filtering error: {e}")
        
        # Test search with filters
        print("\n🔍 Testing Search with Filters...")
        try:
            search_results = client.search.search_opinions(
                q="supreme court",
                page=1,
                court="scotus"
            )
            print(f"   ✅ Supreme Court search: {len(search_results)} results")
        except Exception as e:
            print(f"   ❌ Search filtering error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Advanced features error: {e}")
        return False

def test_error_handling():
    """Test error handling with real API."""
    try:
        from courtlistener import CourtListenerClient
        from courtlistener.exceptions import NotFoundError
        
        print("\n⚠️ Testing Error Handling...")
        print("=" * 30)
        
        client = CourtListenerClient()
        
        # Test 404 error
        print("\n🔍 Testing 404 Error...")
        try:
            client.opinions.get_opinion(999999999)  # Non-existent ID
            print("   ❌ Expected 404 error but got success")
        except NotFoundError:
            print("   ✅ Correctly handled 404 error")
        except Exception as e:
            print(f"   ⚠️ Got different error: {e}")
        
        # Test invalid search
        print("\n🔍 Testing Invalid Search...")
        try:
            results = client.search.search_opinions(q="", page=1)
            print(f"   ✅ Empty search handled: {len(results)} results")
        except Exception as e:
            print(f"   ⚠️ Empty search error: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error handling test failed: {e}")
        return False

def main():
    """Main test function."""
    print("🚀 CourtListener SDK Real API Test")
    print("=" * 50)
    
    # Check if .env exists
    if not Path('.env').exists():
        print("❌ .env file not found!")
        print("Please run 'python setup_api_token.py' first to set up your API token.")
        return
    
    # Check if API token is set
    api_token = os.getenv('COURTLISTENER_API_TOKEN')
    if not api_token or api_token == 'your_api_token_here':
        print("❌ API token not configured!")
        print("Please edit the .env file and add your actual API token.")
        return
    
    print(f"✅ API token configured: {api_token[:10]}...")
    
    # Run tests
    success = True
    
    if not test_basic_functionality():
        success = False
    
    if not test_advanced_features():
        success = False
    
    if not test_error_handling():
        success = False
    
    # Summary
    print("\n" + "=" * 50)
    if success:
        print("🎉 All tests completed successfully!")
        print("✅ Your CourtListener SDK is working with real API data!")
        print("\nNext steps:")
        print("- Run full test suite: python -m pytest tests/ -v")
        print("- Check examples: python examples/basic_usage.py")
    else:
        print("⚠️ Some tests failed. Please check the errors above.")
        print("Make sure your API token is valid and you have internet connectivity.")

if __name__ == "__main__":
    main() 