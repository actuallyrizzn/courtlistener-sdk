"""
Comprehensive API Endpoints Examples for CourtListener SDK (Unofficial).

This example demonstrates usage of all major API endpoints including:
- Core endpoints (opinions, dockets, courts, judges)
- Financial disclosure endpoints
- RECAP endpoints
- Alert management
- People and education data
- And many more...

⚠️ Important Notice: This is an unofficial SDK developed by the community 
and is not affiliated with, endorsed by, or officially supported by 
CourtListener or Free Law Project.
"""

from courtlistener import CourtListenerClient
from courtlistener.exceptions import ValidationError, APIError, NotFoundError
import json


def demonstrate_core_endpoints(client):
    """Demonstrate core API endpoints."""
    print("\n🏛️ CORE ENDPOINTS")
    print("=" * 50)
    
    # Opinions
    print("\n📜 Opinions API:")
    try:
        opinions = client.opinions.list(page=1, page_size=3)
        print(f"   Found {opinions.get('count', 0)} opinions")
        if opinions.get('results'):
            print(f"   Sample: {opinions['results'][0].get('caseName', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Dockets
    print("\n📁 Dockets API:")
    try:
        dockets = client.dockets.list(page=1, page_size=3)
        print(f"   Found {dockets.get('count', 0)} dockets")
        if dockets.get('results'):
            print(f"   Sample: {dockets['results'][0].get('caseName', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Courts
    print("\n🏛️ Courts API:")
    try:
        courts = client.courts.list(page=1, page_size=3)
        print(f"   Found {courts.get('count', 0)} courts")
        if courts.get('results'):
            print(f"   Sample: {courts['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Judges
    print("\n👨‍⚖️ Judges API:")
    try:
        judges = client.judges.list(page=1, page_size=3)
        print(f"   Found {judges.get('count', 0)} judges")
        if judges.get('results'):
            print(f"   Sample: {judges['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_financial_endpoints(client):
    """Demonstrate financial disclosure endpoints."""
    print("\n💰 FINANCIAL DISCLOSURE ENDPOINTS")
    print("=" * 50)
    
    # Financial Disclosures
    print("\n💼 Financial Disclosures API:")
    try:
        disclosures = client.financial_disclosures.list(page=1, page_size=3)
        print(f"   Found {disclosures.get('count', 0)} financial disclosures")
        if disclosures.get('results'):
            print(f"   Sample: {disclosures['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Investments
    print("\n📈 Investments API:")
    try:
        investments = client.investments.list(page=1, page_size=3)
        print(f"   Found {investments.get('count', 0)} investments")
        if investments.get('results'):
            print(f"   Sample: {investments['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Gifts
    print("\n🎁 Gifts API:")
    try:
        gifts = client.gifts.list(page=1, page_size=3)
        print(f"   Found {gifts.get('count', 0)} gifts")
        if gifts.get('results'):
            print(f"   Sample: {gifts['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Debts
    print("\n💳 Debts API:")
    try:
        debts = client.debts.list(page=1, page_size=3)
        print(f"   Found {debts.get('count', 0)} debts")
        if debts.get('results'):
            print(f"   Sample: {debts['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_recap_endpoints(client):
    """Demonstrate RECAP endpoints."""
    print("\n📄 RECAP ENDPOINTS")
    print("=" * 50)
    
    # RECAP Documents
    print("\n📋 RECAP Documents API:")
    try:
        recap_docs = client.recap_documents.list(page=1, page_size=3)
        print(f"   Found {recap_docs.get('count', 0)} RECAP documents")
        if recap_docs.get('results'):
            print(f"   Sample: {recap_docs['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Docket Entries
    print("\n📝 Docket Entries API:")
    try:
        entries = client.docket_entries.list(page=1, page_size=3)
        print(f"   Found {entries.get('count', 0)} docket entries")
        if entries.get('results'):
            print(f"   Sample: {entries['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Documents
    print("\n📄 Documents API:")
    try:
        documents = client.documents.list(page=1, page_size=3)
        print(f"   Found {documents.get('count', 0)} documents")
        if documents.get('results'):
            print(f"   Sample: {documents['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_people_endpoints(client):
    """Demonstrate people and education endpoints."""
    print("\n👥 PEOPLE & EDUCATION ENDPOINTS")
    print("=" * 50)
    
    # People
    print("\n👤 People API:")
    try:
        people = client.people.list(page=1, page_size=3)
        print(f"   Found {people.get('count', 0)} people")
        if people.get('results'):
            print(f"   Sample: {people['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Schools
    print("\n🎓 Schools API:")
    try:
        schools = client.schools.list(page=1, page_size=3)
        print(f"   Found {schools.get('count', 0)} schools")
        if schools.get('results'):
            print(f"   Sample: {schools['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Educations
    print("\n📚 Educations API:")
    try:
        educations = client.educations.list(page=1, page_size=3)
        print(f"   Found {educations.get('count', 0)} education records")
        if educations.get('results'):
            print(f"   Sample: {educations['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_alert_endpoints(client):
    """Demonstrate alert management endpoints."""
    print("\n🔔 ALERT ENDPOINTS")
    print("=" * 50)
    
    # Alerts
    print("\n📢 Alerts API:")
    try:
        alerts = client.alerts.list(page=1, page_size=3)
        print(f"   Found {alerts.get('count', 0)} alerts")
        if alerts.get('results'):
            print(f"   Sample: {alerts['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Docket Alerts
    print("\n📋 Docket Alerts API:")
    try:
        docket_alerts = client.docket_alerts.list(page=1, page_size=3)
        print(f"   Found {docket_alerts.get('count', 0)} docket alerts")
        if docket_alerts.get('results'):
            print(f"   Sample: {docket_alerts['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_specialized_endpoints(client):
    """Demonstrate specialized endpoints."""
    print("\n🔬 SPECIALIZED ENDPOINTS")
    print("=" * 50)
    
    # Citations
    print("\n📖 Citations API:")
    try:
        citations = client.citations.list(page=1, page_size=3)
        print(f"   Found {citations.get('count', 0)} citations")
        if citations.get('results'):
            print(f"   Sample: {citations['results'][0].get('citation', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Audio
    print("\n🎵 Audio API:")
    try:
        audio = client.audio.list(page=1, page_size=3)
        print(f"   Found {audio.get('count', 0)} audio recordings")
        if audio.get('results'):
            print(f"   Sample: {audio['results'][0].get('caseName', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Clusters
    print("\n🔗 Clusters API:")
    try:
        clusters = client.clusters.list(page=1, page_size=3)
        print(f"   Found {clusters.get('count', 0)} clusters")
        if clusters.get('results'):
            print(f"   Sample: {clusters['results'][0].get('caseName', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Attorneys
    print("\n⚖️ Attorneys API:")
    try:
        attorneys = client.attorneys.list(page=1, page_size=3)
        print(f"   Found {attorneys.get('count', 0)} attorneys")
        if attorneys.get('results'):
            print(f"   Sample: {attorneys['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Parties
    print("\n👥 Parties API:")
    try:
        parties = client.parties.list(page=1, page_size=3)
        print(f"   Found {parties.get('count', 0)} parties")
        if parties.get('results'):
            print(f"   Sample: {parties['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_advanced_endpoints(client):
    """Demonstrate advanced endpoints."""
    print("\n🚀 ADVANCED ENDPOINTS")
    print("=" * 50)
    
    # ABA Ratings
    print("\n⭐ ABA Ratings API:")
    try:
        aba_ratings = client.aba_ratings.list(page=1, page_size=3)
        print(f"   Found {aba_ratings.get('count', 0)} ABA ratings")
        if aba_ratings.get('results'):
            print(f"   Sample: {aba_ratings['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Political Affiliations
    print("\n🏛️ Political Affiliations API:")
    try:
        political_affiliations = client.political_affiliations.list(page=1, page_size=3)
        print(f"   Found {political_affiliations.get('count', 0)} political affiliations")
        if political_affiliations.get('results'):
            print(f"   Sample: {political_affiliations['results'][0].get('id', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Tags
    print("\n🏷️ Tags API:")
    try:
        tags = client.tag.list(page=1, page_size=3)
        print(f"   Found {tags.get('count', 0)} tags")
        if tags.get('results'):
            print(f"   Sample: {tags['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Sources
    print("\n📚 Sources API:")
    try:
        sources = client.sources.list(page=1, page_size=3)
        print(f"   Found {sources.get('count', 0)} sources")
        if sources.get('results'):
            print(f"   Sample: {sources['results'][0].get('name', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def demonstrate_get_operations(client):
    """Demonstrate GET operations for specific items."""
    print("\n🎯 GET OPERATIONS")
    print("=" * 50)
    
    # Get a specific opinion
    print("\n📜 Getting a specific opinion:")
    try:
        # First get a list to find an ID
        opinions = client.opinions.list(page=1, page_size=1)
        if opinions.get('results'):
            opinion_id = opinions['results'][0].get('id')
            if opinion_id:
                opinion = client.opinions.get(opinion_id)
                print(f"   Retrieved opinion: {opinion.get('caseName', 'N/A')}")
                print(f"   Court: {opinion.get('court', 'N/A')}")
                print(f"   Date Filed: {opinion.get('dateFiled', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")
    
    # Get a specific court
    print("\n🏛️ Getting a specific court:")
    try:
        courts = client.courts.list(page=1, page_size=1)
        if courts.get('results'):
            court_id = courts['results'][0].get('id')
            if court_id:
                court = client.courts.get(court_id)
                print(f"   Retrieved court: {court.get('name', 'N/A')}")
                print(f"   Jurisdiction: {court.get('jurisdiction', 'N/A')}")
    except APIError as e:
        print(f"   ❌ Error: {e}")


def main():
    """Demonstrate all major API endpoints."""
    
    print("🚀 CourtListener SDK (Unofficial) - API Endpoints Examples")
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
    
    # Demonstrate all endpoint categories
    demonstrate_core_endpoints(client)
    demonstrate_financial_endpoints(client)
    demonstrate_recap_endpoints(client)
    demonstrate_people_endpoints(client)
    demonstrate_alert_endpoints(client)
    demonstrate_specialized_endpoints(client)
    demonstrate_advanced_endpoints(client)
    demonstrate_get_operations(client)
    
    print("\n🎉 API endpoints examples completed!")
    print("This demonstrates the comprehensive coverage of the CourtListener API.")
    print("For more specific examples, check the other example files.")


if __name__ == "__main__":
    main()
