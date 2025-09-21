"""
Advanced Usage Examples for CourtListener SDK (Unofficial).

This example demonstrates advanced features including:
- Pagination and iteration
- Complex filtering and querying
- Error handling and retries
- Data processing and analysis
- Real-world workflows
- Performance optimization

⚠️ Important Notice: This is an unofficial SDK developed by the community 
and is not affiliated with, endorsed by, or officially supported by 
CourtListener or Free Law Project.
"""

from courtlistener import CourtListenerClient
from courtlistener.exceptions import ValidationError, APIError, RateLimitError, NotFoundError
from courtlistener.utils.filters import build_date_range_filter, build_court_filter
from courtlistener.utils.pagination import Paginator
from datetime import datetime, timedelta
import time
import json


def demonstrate_pagination(client):
    """Demonstrate advanced pagination techniques."""
    print("\n📄 ADVANCED PAGINATION")
    print("=" * 50)
    
    # Method 1: Manual pagination
    print("\n1️⃣ Manual Pagination:")
    try:
        page = 1
        total_results = 0
        max_pages = 3
        
        while page <= max_pages:
            results = client.opinions.list(page=page, page_size=5)
            page_results = results.get('results', [])
            total_results += len(page_results)
            
            print(f"   Page {page}: {len(page_results)} results")
            
            if not page_results or not results.get('next'):
                break
                
            page += 1
        
        print(f"   Total results across {page-1} pages: {total_results}")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Method 2: Using Paginator
    print("\n2️⃣ Using Paginator Class:")
    try:
        paginator = Paginator(client, 'opinions/', {'page_size': 5})
        
        count = 0
        for opinion in paginator:
            count += 1
            if count >= 10:  # Limit for demo
                break
            print(f"   Opinion {count}: {opinion.get('caseName', 'N/A')}")
        
        print(f"   Processed {count} opinions using Paginator")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_complex_filtering(client):
    """Demonstrate complex filtering and querying."""
    print("\n🔍 COMPLEX FILTERING")
    print("=" * 50)
    
    # Date range filtering
    print("\n📅 Date Range Filtering:")
    try:
        # Search for opinions from the last year
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        
        filters = build_date_range_filter('dateFiled', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        
        results = client.search.list(
            q="constitutional law",
            result_type='o',
            filters=filters,
            page=1
        )
        
        print(f"   Found {results.get('count', 0)} constitutional law opinions from the last year")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Court-specific filtering
    print("\n🏛️ Court-Specific Filtering:")
    try:
        # Search for Supreme Court opinions
        results = client.opinions.list(
            court="scotus",
            page=1,
            page_size=5
        )
        
        print(f"   Found {results.get('count', 0)} Supreme Court opinions")
        
        if results.get('results'):
            print("   Recent SCOTUS opinions:")
            for opinion in results['results'][:3]:
                case_name = opinion.get('caseName', 'N/A')
                date_filed = opinion.get('dateFiled', 'N/A')
                print(f"     - {case_name} ({date_filed})")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Multi-criteria filtering
    print("\n🎯 Multi-Criteria Filtering:")
    try:
        # Search for civil rights cases in federal courts
        filters = {
            'court': 'ca9',  # 9th Circuit
            'nature_of_suit': 'Civil Rights'
        }
        
        results = client.dockets.list(
            filters=filters,
            page=1,
            page_size=5
        )
        
        print(f"   Found {results.get('count', 0)} civil rights cases in 9th Circuit")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_error_handling(client):
    """Demonstrate comprehensive error handling."""
    print("\n⚠️ ERROR HANDLING")
    print("=" * 50)
    
    # Rate limit handling
    print("\n🚦 Rate Limit Handling:")
    try:
        # Make multiple requests to potentially trigger rate limiting
        for i in range(5):
            results = client.opinions.list(page=1, page_size=1)
            print(f"   Request {i+1}: Success")
            time.sleep(0.1)  # Small delay to be respectful
            
    except RateLimitError as e:
        print(f"   ⚠️ Rate limit hit: {e}")
        print("   Waiting before retry...")
        time.sleep(1)
    except APIError as e:
        print(f"   ❌ API Error: {e}")
    
    # Not found handling
    print("\n🔍 Not Found Handling:")
    try:
        # Try to get a non-existent opinion
        opinion = client.opinions.get(999999999)
        print(f"   Retrieved: {opinion.get('caseName', 'N/A')}")
    except NotFoundError as e:
        print(f"   ⚠️ Not found: {e}")
    except APIError as e:
        print(f"   ❌ API Error: {e}")
    
    # Validation error handling
    print("\n✅ Validation Error Handling:")
    try:
        # Try with invalid parameters
        results = client.opinions.list(page=-1)  # Invalid page
        print(f"   Results: {len(results.get('results', []))}")
    except ValidationError as e:
        print(f"   ⚠️ Validation error: {e}")
    except APIError as e:
        print(f"   ❌ API Error: {e}")


def demonstrate_data_processing(client):
    """Demonstrate data processing and analysis."""
    print("\n📊 DATA PROCESSING")
    print("=" * 50)
    
    # Analyze court distribution
    print("\n🏛️ Court Distribution Analysis:")
    try:
        results = client.opinions.list(page=1, page_size=50)
        opinions = results.get('results', [])
        
        court_counts = {}
        for opinion in opinions:
            court = opinion.get('court', 'Unknown')
            court_counts[court] = court_counts.get(court, 0) + 1
        
        print("   Court distribution (top 5):")
        sorted_courts = sorted(court_counts.items(), key=lambda x: x[1], reverse=True)
        for court, count in sorted_courts[:5]:
            print(f"     {court}: {count} opinions")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Analyze date patterns
    print("\n📅 Date Pattern Analysis:")
    try:
        results = client.opinions.list(page=1, page_size=50)
        opinions = results.get('results', [])
        
        year_counts = {}
        for opinion in opinions:
            date_filed = opinion.get('dateFiled', '')
            if date_filed:
                year = date_filed.split('-')[0] if '-' in date_filed else 'Unknown'
                year_counts[year] = year_counts.get(year, 0) + 1
        
        print("   Year distribution (top 5):")
        sorted_years = sorted(year_counts.items(), key=lambda x: x[1], reverse=True)
        for year, count in sorted_years[:5]:
            print(f"     {year}: {count} opinions")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Extract key information
    print("\n🔑 Key Information Extraction:")
    try:
        results = client.opinions.list(page=1, page_size=5)
        opinions = results.get('results', [])
        
        for i, opinion in enumerate(opinions, 1):
            case_name = opinion.get('caseName', 'N/A')
            court = opinion.get('court', 'N/A')
            date_filed = opinion.get('dateFiled', 'N/A')
            absolute_url = opinion.get('absolute_url', 'N/A')
            
            print(f"   Opinion {i}:")
            print(f"     Case: {case_name}")
            print(f"     Court: {court}")
            print(f"     Date: {date_filed}")
            print(f"     URL: {absolute_url}")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_real_world_workflows(client):
    """Demonstrate real-world workflows."""
    print("\n🌍 REAL-WORLD WORKFLOWS")
    print("=" * 50)
    
    # Workflow 1: Research a specific legal topic
    print("\n📚 Legal Topic Research:")
    try:
        topic = "Miranda rights"
        print(f"   Researching: {topic}")
        
        # Search for opinions
        opinions = client.search.list(q=topic, result_type='o', page=1, page_size=10)
        print(f"   Found {opinions.get('count', 0)} opinions about {topic}")
        
        # Search for dockets
        dockets = client.search.list(q=topic, result_type='d', page=1, page_size=10)
        print(f"   Found {dockets.get('count', 0)} dockets about {topic}")
        
        # Search for audio
        audio = client.search.list(q=topic, result_type='a', page=1, page_size=10)
        print(f"   Found {audio.get('count', 0)} audio recordings about {topic}")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Workflow 2: Track a specific court's activity
    print("\n🏛️ Court Activity Tracking:")
    try:
        court = "scotus"
        print(f"   Tracking activity for: {court}")
        
        # Get recent opinions
        opinions = client.opinions.list(court=court, page=1, page_size=5)
        print(f"   Recent opinions: {len(opinions.get('results', []))}")
        
        # Get recent dockets
        dockets = client.dockets.list(court=court, page=1, page_size=5)
        print(f"   Recent dockets: {len(dockets.get('results', []))}")
        
        # Get recent audio
        audio = client.audio.list(court=court, page=1, page_size=5)
        print(f"   Recent audio: {len(audio.get('results', []))}")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Workflow 3: Monitor specific cases
    print("\n📋 Case Monitoring:")
    try:
        # Search for cases with specific keywords
        case_keywords = "Supreme Court"
        results = client.search.list(q=case_keywords, result_type='d', page=1, page_size=5)
        
        print(f"   Found {results.get('count', 0)} cases matching '{case_keywords}'")
        
        if results.get('results'):
            print("   Monitoring these cases:")
            for docket in results['results'][:3]:
                case_name = docket.get('caseName', 'N/A')
                docket_number = docket.get('docketNumber', 'N/A')
                print(f"     - {case_name} ({docket_number})")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_performance_optimization(client):
    """Demonstrate performance optimization techniques."""
    print("\n⚡ PERFORMANCE OPTIMIZATION")
    print("=" * 50)
    
    # Batch processing
    print("\n📦 Batch Processing:")
    try:
        start_time = time.time()
        
        # Process multiple pages in sequence
        total_results = 0
        for page in range(1, 4):  # Process 3 pages
            results = client.opinions.list(page=page, page_size=10)
            page_results = results.get('results', [])
            total_results += len(page_results)
            
            print(f"   Page {page}: {len(page_results)} results")
        
        end_time = time.time()
        print(f"   Processed {total_results} results in {end_time - start_time:.2f} seconds")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Efficient filtering
    print("\n🎯 Efficient Filtering:")
    try:
        start_time = time.time()
        
        # Use specific filters to reduce data transfer
        results = client.opinions.list(
            court="scotus",
            page=1,
            page_size=20
        )
        
        end_time = time.time()
        print(f"   Retrieved {len(results.get('results', []))} SCOTUS opinions in {end_time - start_time:.2f} seconds")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Caching strategy
    print("\n💾 Caching Strategy:")
    try:
        # Simulate caching by storing results
        cache = {}
        
        # First request (cache miss)
        start_time = time.time()
        results = client.opinions.list(page=1, page_size=5)
        cache['opinions_page_1'] = results
        end_time = time.time()
        print(f"   First request (cache miss): {end_time - start_time:.2f} seconds")
        
        # Second request (cache hit)
        start_time = time.time()
        cached_results = cache.get('opinions_page_1')
        end_time = time.time()
        print(f"   Second request (cache hit): {end_time - start_time:.2f} seconds")
        
    except APIError as e:
        print(f"   ❌ Error: {e}")


def main():
    """Demonstrate advanced usage patterns."""
    
    print("🚀 CourtListener SDK (Unofficial) - Advanced Usage Examples")
    print("=" * 70)
    print("⚠️  This is an unofficial SDK not endorsed by CourtListener")
    print("=" * 70)
    
    # Initialize client
    try:
        client = CourtListenerClient()
        print("✅ Client initialized successfully")
    except ValidationError as e:
        print(f"❌ Configuration error: {e}")
        print("Please set your API token in the .env file")
        return
    
    # Demonstrate advanced features
    demonstrate_pagination(client)
    demonstrate_complex_filtering(client)
    demonstrate_error_handling(client)
    demonstrate_data_processing(client)
    demonstrate_real_world_workflows(client)
    demonstrate_performance_optimization(client)
    
    print("\n🎉 Advanced usage examples completed!")
    print("These patterns can be adapted for your specific use cases.")
    print("For more examples, check the other example files.")


if __name__ == "__main__":
    main()
