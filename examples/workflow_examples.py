"""
Real-World Workflow Examples for CourtListener SDK (Unofficial).

This example demonstrates practical workflows including:
- Legal research workflows
- Case monitoring and tracking
- Data analysis and reporting
- Integration with other tools
- Automated monitoring systems

⚠️ Important Notice: This is an unofficial SDK developed by the community 
and is not affiliated with, endorsed by, or officially supported by 
CourtListener or Free Law Project.
"""

from courtlistener import CourtListenerClient
from courtlistener.exceptions import ValidationError, APIError, RateLimitError
from courtlistener.utils.filters import build_date_range_filter
from datetime import datetime, timedelta
import json
import csv
import time


def legal_research_workflow(client, research_topic, court=None, date_range_days=365):
    """Complete legal research workflow for a specific topic."""
    print(f"\n📚 LEGAL RESEARCH WORKFLOW: {research_topic}")
    print("=" * 60)
    
    # Calculate date range
    end_date = datetime.now()
    start_date = end_date - timedelta(days=date_range_days)
    
    print(f"📅 Research period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    if court:
        print(f"🏛️ Court filter: {court}")
    
    research_data = {
        'topic': research_topic,
        'date_range': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'court': court,
        'opinions': [],
        'dockets': [],
        'audio': [],
        'citations': []
    }
    
    try:
        # Step 1: Search for opinions
        print("\n1️⃣ Searching for opinions...")
        filters = build_date_range_filter('dateFiled', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        if court:
            filters['court'] = court
        
        opinions = client.search.list(
            q=research_topic,
            result_type='o',
            filters=filters,
            page=1,
            page_size=20
        )
        
        opinion_count = opinions.get('count', 0)
        print(f"   Found {opinion_count} opinions")
        research_data['opinions'] = opinions.get('results', [])
        
        # Step 2: Search for related dockets
        print("\n2️⃣ Searching for related dockets...")
        dockets = client.search.list(
            q=research_topic,
            result_type='d',
            filters=filters,
            page=1,
            page_size=20
        )
        
        docket_count = dockets.get('count', 0)
        print(f"   Found {docket_count} dockets")
        research_data['dockets'] = dockets.get('results', [])
        
        # Step 3: Search for audio recordings
        print("\n3️⃣ Searching for audio recordings...")
        audio = client.search.list(
            q=research_topic,
            result_type='a',
            filters=filters,
            page=1,
            page_size=20
        )
        
        audio_count = audio.get('count', 0)
        print(f"   Found {audio_count} audio recordings")
        research_data['audio'] = audio.get('results', [])
        
        # Step 4: Search for citations
        print("\n4️⃣ Searching for citations...")
        citations = client.citations.list(page=1, page_size=20)
        
        citation_count = citations.get('count', 0)
        print(f"   Found {citation_count} citations")
        research_data['citations'] = citations.get('results', [])
        
        # Step 5: Generate summary report
        print("\n📊 RESEARCH SUMMARY:")
        print(f"   Topic: {research_topic}")
        print(f"   Opinions: {opinion_count}")
        print(f"   Dockets: {docket_count}")
        print(f"   Audio: {audio_count}")
        print(f"   Citations: {citation_count}")
        
        return research_data
        
    except APIError as e:
        print(f"   ❌ Research error: {e}")
        return research_data


def case_monitoring_workflow(client, case_keywords, court=None, monitoring_days=30):
    """Monitor specific cases or legal topics over time."""
    print(f"\n📋 CASE MONITORING WORKFLOW: {case_keywords}")
    print("=" * 60)
    
    # Calculate monitoring period
    end_date = datetime.now()
    start_date = end_date - timedelta(days=monitoring_days)
    
    print(f"📅 Monitoring period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    monitoring_data = {
        'keywords': case_keywords,
        'monitoring_period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'court': court,
        'daily_updates': []
    }
    
    try:
        # Search for recent cases
        filters = build_date_range_filter('dateFiled', start_date.strftime('%Y-%m-%d'), end_date.strftime('%Y-%m-%d'))
        if court:
            filters['court'] = court
        
        cases = client.search.list(
            q=case_keywords,
            result_type='d',
            filters=filters,
            page=1,
            page_size=50
        )
        
        case_count = cases.get('count', 0)
        print(f"   Found {case_count} cases matching keywords")
        
        if cases.get('results'):
            print("\n📋 Recent cases:")
            for i, case in enumerate(cases['results'][:10], 1):
                case_name = case.get('caseName', 'N/A')
                docket_number = case.get('docketNumber', 'N/A')
                date_filed = case.get('dateFiled', 'N/A')
                court_name = case.get('court', 'N/A')
                
                print(f"   {i}. {case_name}")
                print(f"      Docket: {docket_number}")
                print(f"      Filed: {date_filed}")
                print(f"      Court: {court_name}")
                print()
        
        monitoring_data['daily_updates'] = cases.get('results', [])
        return monitoring_data
        
    except APIError as e:
        print(f"   ❌ Monitoring error: {e}")
        return monitoring_data


def court_activity_analysis(client, court_id, analysis_days=90):
    """Analyze activity patterns for a specific court."""
    print(f"\n🏛️ COURT ACTIVITY ANALYSIS: {court_id}")
    print("=" * 60)
    
    # Calculate analysis period
    end_date = datetime.now()
    start_date = end_date - timedelta(days=analysis_days)
    
    print(f"📅 Analysis period: {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}")
    
    analysis_data = {
        'court_id': court_id,
        'analysis_period': f"{start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}",
        'opinions': [],
        'dockets': [],
        'audio': [],
        'statistics': {}
    }
    
    try:
        # Get court information
        court_info = client.courts.get(court_id)
        court_name = court_info.get('name', 'Unknown Court')
        print(f"🏛️ Analyzing: {court_name}")
        
        # Analyze opinions
        print("\n📜 Analyzing opinions...")
        opinions = client.opinions.list(
            court=court_id,
            page=1,
            page_size=100
        )
        
        opinion_count = opinions.get('count', 0)
        print(f"   Total opinions: {opinion_count}")
        analysis_data['opinions'] = opinions.get('results', [])
        
        # Analyze dockets
        print("\n📁 Analyzing dockets...")
        dockets = client.dockets.list(
            court=court_id,
            page=1,
            page_size=100
        )
        
        docket_count = dockets.get('count', 0)
        print(f"   Total dockets: {docket_count}")
        analysis_data['dockets'] = dockets.get('results', [])
        
        # Analyze audio
        print("\n🎵 Analyzing audio recordings...")
        audio = client.audio.list(
            court=court_id,
            page=1,
            page_size=100
        )
        
        audio_count = audio.get('count', 0)
        print(f"   Total audio recordings: {audio_count}")
        analysis_data['audio'] = audio.get('results', [])
        
        # Generate statistics
        print("\n📊 COURT STATISTICS:")
        print(f"   Court: {court_name}")
        print(f"   Opinions: {opinion_count}")
        print(f"   Dockets: {docket_count}")
        print(f"   Audio: {audio_count}")
        
        # Analyze opinion types
        if analysis_data['opinions']:
            opinion_types = {}
            for opinion in analysis_data['opinions']:
                opinion_type = opinion.get('type', 'Unknown')
                opinion_types[opinion_type] = opinion_types.get(opinion_type, 0) + 1
            
            print("\n📜 Opinion types:")
            for opinion_type, count in sorted(opinion_types.items(), key=lambda x: x[1], reverse=True):
                print(f"   {opinion_type}: {count}")
        
        analysis_data['statistics'] = {
            'opinions': opinion_count,
            'dockets': docket_count,
            'audio': audio_count
        }
        
        return analysis_data
        
    except APIError as e:
        print(f"   ❌ Analysis error: {e}")
        return analysis_data


def data_export_workflow(client, export_type='opinions', court=None, limit=100):
    """Export data for external analysis."""
    print(f"\n📤 DATA EXPORT WORKFLOW: {export_type}")
    print("=" * 60)
    
    export_data = {
        'export_type': export_type,
        'court': court,
        'limit': limit,
        'data': [],
        'export_time': datetime.now().isoformat()
    }
    
    try:
        if export_type == 'opinions':
            print("📜 Exporting opinions...")
            results = client.opinions.list(court=court, page=1, page_size=limit)
            export_data['data'] = results.get('results', [])
            
        elif export_type == 'dockets':
            print("📁 Exporting dockets...")
            results = client.dockets.list(court=court, page=1, page_size=limit)
            export_data['data'] = results.get('results', [])
            
        elif export_type == 'judges':
            print("👨‍⚖️ Exporting judges...")
            results = client.judges.list(page=1, page_size=limit)
            export_data['data'] = results.get('results', [])
            
        elif export_type == 'courts':
            print("🏛️ Exporting courts...")
            results = client.courts.list(page=1, page_size=limit)
            export_data['data'] = results.get('results', [])
        
        data_count = len(export_data['data'])
        print(f"   Exported {data_count} {export_type}")
        
        # Save to JSON file
        filename = f"courtlistener_{export_type}_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, ensure_ascii=False)
        
        print(f"   Data saved to: {filename}")
        
        return export_data
        
    except APIError as e:
        print(f"   ❌ Export error: {e}")
        return export_data
    except Exception as e:
        print(f"   ❌ File error: {e}")
        return export_data


def automated_monitoring_system(client, monitoring_configs):
    """Simulate an automated monitoring system."""
    print(f"\n🤖 AUTOMATED MONITORING SYSTEM")
    print("=" * 60)
    
    monitoring_results = {
        'timestamp': datetime.now().isoformat(),
        'configs': monitoring_configs,
        'results': []
    }
    
    for config in monitoring_configs:
        print(f"\n🔍 Monitoring: {config['name']}")
        print(f"   Keywords: {config['keywords']}")
        print(f"   Court: {config.get('court', 'All')}")
        
        try:
            # Search for new content
            filters = {}
            if config.get('court'):
                filters['court'] = config['court']
            
            results = client.search.list(
                q=config['keywords'],
                filters=filters,
                page=1,
                page_size=10
            )
            
            result_count = results.get('count', 0)
            print(f"   Found {result_count} results")
            
            monitoring_results['results'].append({
                'config': config,
                'result_count': result_count,
                'results': results.get('results', [])
            })
            
            # Simulate alert generation
            if result_count > config.get('alert_threshold', 5):
                print(f"   🚨 ALERT: {result_count} results exceed threshold of {config.get('alert_threshold', 5)}")
            
        except APIError as e:
            print(f"   ❌ Monitoring error: {e}")
            monitoring_results['results'].append({
                'config': config,
                'error': str(e)
            })
    
    return monitoring_results


def main():
    """Demonstrate real-world workflows."""
    
    print("🌍 CourtListener SDK (Unofficial) - Workflow Examples")
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
    
    # Workflow 1: Legal Research
    print("\n" + "="*70)
    print("WORKFLOW 1: LEGAL RESEARCH")
    print("="*70)
    
    research_data = legal_research_workflow(
        client, 
        research_topic="Miranda rights",
        court="scotus",
        date_range_days=365
    )
    
    # Workflow 2: Case Monitoring
    print("\n" + "="*70)
    print("WORKFLOW 2: CASE MONITORING")
    print("="*70)
    
    monitoring_data = case_monitoring_workflow(
        client,
        case_keywords="Supreme Court constitutional",
        court="scotus",
        monitoring_days=30
    )
    
    # Workflow 3: Court Activity Analysis
    print("\n" + "="*70)
    print("WORKFLOW 3: COURT ACTIVITY ANALYSIS")
    print("="*70)
    
    analysis_data = court_activity_analysis(
        client,
        court_id="scotus",
        analysis_days=90
    )
    
    # Workflow 4: Data Export
    print("\n" + "="*70)
    print("WORKFLOW 4: DATA EXPORT")
    print("="*70)
    
    export_data = data_export_workflow(
        client,
        export_type='opinions',
        court='scotus',
        limit=50
    )
    
    # Workflow 5: Automated Monitoring
    print("\n" + "="*70)
    print("WORKFLOW 5: AUTOMATED MONITORING")
    print("="*70)
    
    monitoring_configs = [
        {
            'name': 'Constitutional Law',
            'keywords': 'constitutional law',
            'court': 'scotus',
            'alert_threshold': 5
        },
        {
            'name': 'Civil Rights',
            'keywords': 'civil rights',
            'alert_threshold': 10
        },
        {
            'name': 'First Amendment',
            'keywords': 'first amendment',
            'alert_threshold': 3
        }
    ]
    
    monitoring_results = automated_monitoring_system(client, monitoring_configs)
    
    print("\n🎉 Workflow examples completed!")
    print("These workflows can be adapted and automated for your specific needs.")
    print("For more examples, check the other example files.")


if __name__ == "__main__":
    main()
