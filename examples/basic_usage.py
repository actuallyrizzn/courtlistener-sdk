"""
Basic usage example for CourtListener SDK.
"""

from courtlistener import CourtListenerClient


def main():
    """Demonstrate basic SDK usage."""
    
    # Initialize client
    client = CourtListenerClient(api_token="your_api_token_here")
    
    # Test connection
    try:
        client.test_connection()
        print("✓ Connection successful!")
    except Exception as e:
        print(f"✗ Connection failed: {e}")
        return
    
    # Search for opinions
    print("\nSearching for opinions about 'constitutional rights'...")
    search_results = client.search.search("constitutional rights", result_type="o")
    print(f"Found {search_results['count']} opinions")
    
    # Get courts list
    print("\nFetching courts list...")
    courts = client.courts.list_courts()
    print(f"Found {courts['count']} courts")
    
    # Get Supreme Court opinions
    print("\nFetching recent Supreme Court opinions...")
    scotus_opinions = client.opinions.list_opinions(filters={'court': 'scotus'})
    print(f"Found {scotus_opinions['count']} Supreme Court opinions")


if __name__ == "__main__":
    main() 