"""
Basic usage example for CourtListener SDK (Unofficial).
This example demonstrates how to use the unofficial SDK with real CourtListener API data.

⚠️ Important Notice: This is an unofficial SDK developed by the community 
and is not affiliated with, endorsed by, or officially supported by 
CourtListener or Free Law Project.
"""

from courtlistener import CourtListenerClient
from courtlistener.exceptions import ValidationError, NotFoundError


def main():
    """Demonstrate basic SDK usage with real API data."""
    
    print("🚀 CourtListener SDK (Unofficial) Basic Usage Example")
    print("=" * 60)
    print("⚠️  This is an unofficial SDK not endorsed by CourtListener")
    print("=" * 60)
    
    # Initialize client (will use API token from environment)
    try:
        client = CourtListenerClient()
        print("✅ Client initialized successfully")
    except ValidationError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set your API token in the .env file")
        return
    
    # Example 1: Search for opinions
    print("\n📜 Example 1: Searching for opinions about 'constitutional rights'...")
    try:
        search_results = client.search.list(q="constitutional rights", page=1)
        print(f"   Found {search_results.get('count', 0)} results")
        if search_results.get('results'):
            print(f"   Sample: {search_results['results'][0].get('caseName', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Search error: {e}")
    
    # Example 2: Get courts list
    print("\n🏛️ Example 2: Fetching courts list...")
    try:
        courts_response = client.courts.list(page=1)
        courts = courts_response.get('results', [])
        print(f"   Found {courts_response.get('count', 0)} courts")
        if courts:
            print(f"   Sample: {courts[0].get('name', 'N/A')} ({courts[0].get('id', 'N/A')})")
    except Exception as e:
        print(f"   ❌ Courts error: {e}")
    
    # Example 3: Get Supreme Court opinions
    print("\n⚖️ Example 3: Fetching recent Supreme Court opinions...")
    try:
        scotus_response = client.opinions.list(page=1, court="scotus")
        opinions = scotus_response.get('results', [])
        print(f"   Found {scotus_response.get('count', 0)} Supreme Court opinions")
        if opinions:
            print(f"   Sample: {opinions[0].get('caseName', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Supreme Court opinions error: {e}")
    
    # Example 4: Get a specific opinion by ID
    print("\n🎯 Example 4: Getting a specific opinion...")
    try:
        # First get a list to find an ID
        opinions_response = client.opinions.list(page=1)
        opinions = opinions_response.get('results', [])
        if opinions:
            opinion_id = opinions[0].get('id')
            specific_opinion = client.opinions.get(opinion_id)
            print(f"   Retrieved opinion: {specific_opinion.get('caseName', 'N/A')}")
            print(f"   Filed: {specific_opinion.get('dateFiled', 'N/A')}")
            print(f"   Court: {specific_opinion.get('court', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Get opinion error: {e}")
    
    # Example 5: Search for dockets
    print("\n📁 Example 5: Searching for dockets...")
    try:
        dockets_response = client.dockets.list(page=1)
        dockets = dockets_response.get('results', [])
        print(f"   Found {dockets_response.get('count', 0)} dockets")
        if dockets:
            print(f"   Sample: {dockets[0].get('caseName', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Dockets error: {e}")
    
    # Example 6: Get judges
    print("\n👨‍⚖️ Example 6: Fetching judges...")
    try:
        judges_response = client.judges.list(page=1)
        judges = judges_response.get('results', [])
        print(f"   Found {judges_response.get('count', 0)} judges")
        if judges:
            print(f"   Sample: {judges[0].get('name', 'N/A')}")
    except Exception as e:
        print(f"   ❌ Judges error: {e}")
    
    print("\n🎉 Basic usage example completed!")
    print("For more examples, check the test files and documentation.")


if __name__ == "__main__":
    main() 