# CourtListener Python SDK (Unofficial)

An **unofficial**, robust, production-ready Python SDK for the [CourtListener API](https://www.courtlistener.com/api/).

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Features
- **100% API Coverage**: Complete support for all 36+ CourtListener API endpoints
- **Comprehensive Data Models**: Pythonic models for all data types including financial disclosures, alerts, people, and more
- **Robust Error Handling**: Production-ready error handling with retry logic and rate limiting
- **Advanced Pagination**: Cursor-based pagination support for efficient data retrieval
- **Full CRUD Support**: Create, read, update, and delete operations for alerts and docket alerts
- **97.31% Test Coverage**: Comprehensive test suite with real API integration tests
- **Easy Authentication**: Simple authentication via `.env` file or direct token
- **Extensive Documentation**: Complete API reference and usage examples

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start
```python
from courtlistener import CourtListenerClient
client = CourtListenerClient()
dockets = client.dockets.list(page=1)
for docket in dockets['results']:
    print(docket['case_name'], docket['docket_number'])
```

## Available Endpoints

The SDK provides access to all CourtListener API endpoints:

### Core Endpoints
- `client.courts` — Court information and hierarchy
- `client.dockets` — Docket records and case information
- `client.opinions` — Judicial opinions and decisions
- `client.clusters` — Opinion clusters and related cases
- `client.judges` — Judicial biographical data
- `client.positions` — Judicial positions and appointments
- `client.audio` — Oral argument audio recordings
- `client.search` — Cross-resource search functionality

### Financial & Disclosure Endpoints
- `client.financial` — Financial disclosure records
- `client.financial_disclosures` — Detailed financial disclosures
- `client.investments` — Investment holdings
- `client.non_investment_incomes` — Non-investment income sources
- `client.gifts` — Gift disclosures
- `client.reimbursements` — Reimbursement records
- `client.debts` — Debt disclosures
- `client.spouse_incomes` — Spouse income information
- `client.agreements` — Financial agreements

### Case & Legal Endpoints
- `client.docket_entries` — Individual docket entries
- `client.parties` — Case participants and parties
- `client.attorneys` — Legal representation
- `client.documents` — RECAP document management
- `client.recap_documents` — RECAP document access
- `client.citations` — Citation graph and verification
- `client.opinions_cited` — Opinion citation relationships

### People & Education Endpoints
- `client.people` — People and biographical data
- `client.schools` — Educational institutions
- `client.educations` — Educational background
- `client.aba_ratings` — ABA judicial ratings
- `client.political_affiliations` — Political affiliations

### Alert & Notification Endpoints
- `client.alerts` — Search alerts and notifications
- `client.docket_alerts` — Docket-specific alerts

### Administrative Endpoints
- `client.sources` — Data sources
- `client.retention_events` — Data retention events
- `client.tag` — Tagging system
- `client.recap_fetch` — RECAP fetch operations
- `client.recap_query` — RECAP query operations
- `client.originating_court_information` — Court origin data
- `client.fjc_integrated_database` — FJC database integration
- `client.disclosure_positions` — Disclosure position data

## Authentication
Set your API token in a `.env` file:
```
COURTLISTENER_API_TOKEN=your_token_here
```
Or pass it directly:
```python
client = CourtListenerClient(api_token="your_token_here")
```

## Tests & Debugging
All manual and debug test scripts are in [`tests/manual_debug/`](./tests/manual_debug/). See the documentation for details on running and extending tests.

## Documentation
Extensive documentation is available in [`../docs/`](../docs/), including:
- [User Guide](../docs/user_guide.md)
- [API Reference](../docs/api_reference.md)
- [Advanced Usage](../docs/advanced_usage.md)
- [Troubleshooting](../docs/troubleshooting.md)

## Changelog
See [`../CHANGELOG.md`](../CHANGELOG.md) for release notes.

## License
See [`../LICENSE`](../LICENSE).

---

For more, see the [full documentation](../docs/user_guide.md).
