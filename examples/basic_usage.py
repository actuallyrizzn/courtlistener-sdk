"""
Basic usage example for CourtListener SDK.
This example demonstrates how to use the SDK with real CourtListener API data.
"""

from courtlistener import CourtListenerClient
from courtlistener.exceptions import ValidationError, NotFoundError


def main():
    """Demonstrate basic SDK usage with real API data."""
    
    print("🚀 CourtListener SDK Basic Usage Example")
    print("=" * 50)
    
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
        search_results = client.search.search_opinions(q="constitutional rights", page=1)
        print(f"   Found {len(search_results)} opinions")
        if search_results:
            print(f"   Sample: {search_results[0].case_name}")
    except Exception as e:
        print(f"   ❌ Search error: {e}")
    
    # Example 2: Get courts list
    print("\n🏛️ Example 2: Fetching courts list...")
    try:
        courts = client.courts.list_courts(page=1)
        print(f"   Found {len(courts)} courts")
        if courts:
            print(f"   Sample: {courts[0].name} ({courts[0].id})")
    except Exception as e:
        print(f"   ❌ Courts error: {e}")
    
    # Example 3: Get Supreme Court opinions
    print("\n⚖️ Example 3: Fetching recent Supreme Court opinions...")
    try:
        scotus_opinions = client.opinions.list_opinions(page=1, court="scotus")
        print(f"   Found {len(scotus_opinions)} Supreme Court opinions")
        if scotus_opinions:
            print(f"   Sample: {scotus_opinions[0].case_name}")
    except Exception as e:
        print(f"   ❌ Supreme Court opinions error: {e}")
    
    # Example 4: Get a specific opinion by ID
    print("\n🎯 Example 4: Getting a specific opinion...")
    try:
        # First get a list to find an ID
        opinions = client.opinions.list_opinions(page=1)
        if opinions:
            opinion_id = opinions[0].id
            specific_opinion = client.opinions.get_opinion(opinion_id)
            print(f"   Retrieved opinion: {specific_opinion.case_name}")
            print(f"   Filed: {specific_opinion.date_filed}")
            print(f"   Court: {specific_opinion.court_name}")
    except Exception as e:
        print(f"   ❌ Get opinion error: {e}")
    
    # Example 5: Search for dockets
    print("\n📁 Example 5: Searching for dockets...")
    try:
        dockets = client.dockets.list_dockets(page=1)
        print(f"   Found {len(dockets)} dockets")
        if dockets:
            print(f"   Sample: {dockets[0].case_name}")
    except Exception as e:
        print(f"   ❌ Dockets error: {e}")
    
    # Example 6: Get judges
    print("\n👨‍⚖️ Example 6: Fetching judges...")
    try:
        judges = client.judges.list_judges(page=1)
        print(f"   Found {len(judges)} judges")
        if judges:
            print(f"   Sample: {judges[0].name}")
    except Exception as e:
        print(f"   ❌ Judges error: {e}")
    
    print("\n🎉 Basic usage example completed!")
    print("For more examples, check the test files and documentation.")


if __name__ == "__main__":
    main() 