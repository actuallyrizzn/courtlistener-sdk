"""
Comprehensive Search Examples for CourtListener SDK (Unofficial).

This example demonstrates advanced search capabilities including:
- Text search across all content types
- Filtered searches by court, date, and other criteria
- Search result processing and analysis
- Pagination and result iteration

⚠️ Important Notice: This is an unofficial SDK developed by the community 
and is not affiliated with, endorsed by, or officially supported by 
CourtListener or Free Law Project.
"""

from courtlistener import CourtListenerClient
from courtlistener.exceptions import ValidationError, APIError
from courtlistener.utils.filters import build_date_range_filter, build_court_filter
from datetime import datetime, timedelta
import json


def search_all_content(client, query, page=1):
    """Search across all content types."""
    print(f"\n🔍 Searching for '{query}' across all content...")
    try:
        results = client.search.list(q=query, page=page)
        print(f"   Found {results.get('count', 0)} total results")
        
        if results.get('results'):
            print("   Sample results:")
            for i, result in enumerate(results['results'][:3]):
                result_type = result.get('resource_uri', '').split('/')[-2] if result.get('resource_uri') else 'unknown'
                case_name = result.get('caseName', 'N/A')
                print(f"     {i+1}. [{result_type}] {case_name}")
        
        return results
    except APIError as e:
        print(f"   ❌ Search error: {e}")
        return None


def search_opinions_with_filters(client, query, court=None, date_from=None, date_to=None):
    """Search opinions with advanced filters."""
    print(f"\n📜 Searching opinions for '{query}' with filters...")
    
    try:
        # Build filters
        filters = {}
        if court:
            filters['court'] = court
        if date_from and date_to:
            filters.update(build_date_range_filter('dateFiled', date_from, date_to))
        
        # Search opinions specifically
        results = client.search.list(
            q=query, 
            result_type='o',  # 'o' for opinions
            filters=filters,
            page=1
        )
        
        print(f"   Found {results.get('count', 0)} opinion results")
        
        if results.get('results'):
            print("   Sample opinions:")
            for i, opinion in enumerate(results['results'][:3]):
                case_name = opinion.get('caseName', 'N/A')
                date_filed = opinion.get('dateFiled', 'N/A')
                court_name = opinion.get('court', 'N/A')
                print(f"     {i+1}. {case_name} ({date_filed}) - {court_name}")
        
        return results
    except APIError as e:
        print(f"   ❌ Opinion search error: {e}")
        return None


def search_dockets_with_filters(client, query, court=None, case_type=None):
    """Search dockets with specific filters."""
    print(f"\n📁 Searching dockets for '{query}' with filters...")
    
    try:
        filters = {}
        if court:
            filters['court'] = court
        if case_type:
            filters['nature_of_suit'] = case_type
        
        results = client.search.list(
            q=query,
            result_type='d',  # 'd' for dockets
            filters=filters,
            page=1
        )
        
        print(f"   Found {results.get('count', 0)} docket results")
        
        if results.get('results'):
            print("   Sample dockets:")
            for i, docket in enumerate(results['results'][:3]):
                case_name = docket.get('caseName', 'N/A')
                docket_number = docket.get('docketNumber', 'N/A')
                court_name = docket.get('court', 'N/A')
                print(f"     {i+1}. {case_name} ({docket_number}) - {court_name}")
        
        return results
    except APIError as e:
        print(f"   ❌ Docket search error: {e}")
        return None


def search_judges_with_filters(client, query, court=None, position=None):
    """Search judges with specific filters."""
    print(f"\n👨‍⚖️ Searching judges for '{query}' with filters...")
    
    try:
        filters = {}
        if court:
            filters['court'] = court
        if position:
            filters['position'] = position
        
        results = client.search.list(
            q=query,
            result_type='j',  # 'j' for judges
            filters=filters,
            page=1
        )
        
        print(f"   Found {results.get('count', 0)} judge results")
        
        if results.get('results'):
            print("   Sample judges:")
            for i, judge in enumerate(results['results'][:3]):
                name = judge.get('name', 'N/A')
                position = judge.get('position', 'N/A')
                court_name = judge.get('court', 'N/A')
                print(f"     {i+1}. {name} ({position}) - {court_name}")
        
        return results
    except APIError as e:
        print(f"   ❌ Judge search error: {e}")
        return None


def search_audio_with_filters(client, query, court=None, date_from=None, date_to=None):
    """Search audio recordings with filters."""
    print(f"\n🎵 Searching audio for '{query}' with filters...")
    
    try:
        filters = {}
        if court:
            filters['court'] = court
        if date_from and date_to:
            filters.update(build_date_range_filter('dateArgued', date_from, date_to))
        
        results = client.search.list(
            q=query,
            result_type='a',  # 'a' for audio
            filters=filters,
            page=1
        )
        
        print(f"   Found {results.get('count', 0)} audio results")
        
        if results.get('results'):
            print("   Sample audio recordings:")
            for i, audio in enumerate(results['results'][:3]):
                case_name = audio.get('caseName', 'N/A')
                date_argued = audio.get('dateArgued', 'N/A')
                court_name = audio.get('court', 'N/A')
                print(f"     {i+1}. {case_name} ({date_argued}) - {court_name}")
        
        return results
    except APIError as e:
        print(f"   ❌ Audio search error: {e}")
        return None


def demonstrate_pagination(client, query, max_pages=3):
    """Demonstrate pagination through search results."""
    print(f"\n📄 Demonstrating pagination for '{query}'...")
    
    try:
        total_results = 0
        page = 1
        
        while page <= max_pages:
            results = client.search.list(q=query, page=page)
            page_results = results.get('results', [])
            total_results += len(page_results)
            
            print(f"   Page {page}: {len(page_results)} results")
            
            if not page_results or not results.get('next'):
                break
                
            page += 1
        
        print(f"   Total results across {page-1} pages: {total_results}")
        return total_results
        
    except APIError as e:
        print(f"   ❌ Pagination error: {e}")
        return 0


def analyze_search_results(results):
    """Analyze and categorize search results."""
    if not results or not results.get('results'):
        return
    
    print(f"\n📊 Analyzing search results...")
    
    # Categorize by result type
    categories = {}
    for result in results['results']:
        resource_uri = result.get('resource_uri', '')
        if 'opinions' in resource_uri:
            category = 'Opinions'
        elif 'dockets' in resource_uri:
            category = 'Dockets'
        elif 'judges' in resource_uri:
            category = 'Judges'
        elif 'audio' in resource_uri:
            category = 'Audio'
        else:
            category = 'Other'
        
        categories[category] = categories.get(category, 0) + 1
    
    print("   Result breakdown:")
    for category, count in categories.items():
        print(f"     {category}: {count}")
    
    # Analyze courts
    courts = {}
    for result in results['results']:
        court = result.get('court', 'Unknown')
        courts[court] = courts.get(court, 0) + 1
    
    print("   Top courts:")
    sorted_courts = sorted(courts.items(), key=lambda x: x[1], reverse=True)
    for court, count in sorted_courts[:5]:
        print(f"     {court}: {count}")


def main():
    """Demonstrate comprehensive search capabilities."""
    
    print("🔍 CourtListener SDK (Unofficial) - Comprehensive Search Examples")
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
    
    # Example 1: Basic search across all content
    search_all_content(client, "first amendment")
    
    # Example 2: Search opinions with filters
    search_opinions_with_filters(
        client, 
        "constitutional rights", 
        court="scotus",
        date_from="2020-01-01",
        date_to="2024-01-01"
    )
    
    # Example 3: Search dockets with filters
    search_dockets_with_filters(
        client,
        "civil rights",
        court="ca9",  # 9th Circuit
        case_type="Civil Rights"
    )
    
    # Example 4: Search judges with filters
    search_judges_with_filters(
        client,
        "Supreme Court",
        court="scotus",
        position="Chief Justice"
    )
    
    # Example 5: Search audio recordings
    search_audio_with_filters(
        client,
        "oral argument",
        court="scotus",
        date_from="2023-01-01",
        date_to="2024-01-01"
    )
    
    # Example 6: Demonstrate pagination
    demonstrate_pagination(client, "Supreme Court", max_pages=2)
    
    # Example 7: Analyze search results
    results = search_all_content(client, "Miranda rights")
    if results:
        analyze_search_results(results)
    
    print("\n🎉 Comprehensive search examples completed!")
    print("For more advanced examples, check the other example files.")


if __name__ == "__main__":
    main()
