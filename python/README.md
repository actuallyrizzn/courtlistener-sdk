# CourtListener Python SDK (Unofficial)

An **unofficial**, robust, production-ready Python SDK for the [CourtListener API](https://www.courtlistener.com/api/).

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Features
- **100% API Coverage**: Complete support for all 36+ CourtListener API endpoints
- **Async/Await Support**: AsyncClient with httpx for concurrent requests and non-blocking I/O
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

### Synchronous Client
```python
from courtlistener import CourtListenerClient
client = CourtListenerClient()
dockets = client.dockets.list(page=1)
for docket in dockets['results']:
    print(docket['case_name'], docket['docket_number'])
```

### Async Client
```python
import asyncio
from courtlistener import AsyncCourtListenerClient

async def main():
    async with AsyncCourtListenerClient() as client:
        dockets = await client.dockets.list(page=1)
        for docket in dockets['results']:
            print(docket['case_name'], docket['docket_number'])

asyncio.run(main())
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
# Synchronous
client = CourtListenerClient(api_token="your_token_here")

# Async
async with AsyncCourtListenerClient(api_token="your_token_here") as client:
    # ... use client
```

## Async/Concurrent Usage

The SDK provides full async support through `AsyncCourtListenerClient` using httpx:

### Basic Async Usage
```python
import asyncio
from courtlistener import AsyncCourtListenerClient

async def fetch_data():
    async with AsyncCourtListenerClient() as client:
        # Make async requests
        courts = await client.courts.list(page=1)
        docket = await client.dockets.get(123456)
        return courts, docket

asyncio.run(fetch_data())
```

### Concurrent Requests
```python
import asyncio
from courtlistener import AsyncCourtListenerClient

async def fetch_multiple():
    async with AsyncCourtListenerClient() as client:
        # Run multiple requests concurrently
        results = await asyncio.gather(
            client.courts.list(page=1),
            client.dockets.list(page=1),
            client.opinions.list(page=1),
        )
        courts, dockets, opinions = results
        return results

asyncio.run(fetch_multiple())
```

### Limitations
- **Context Manager Required**: AsyncClient must be used with `async with` to properly manage connections
- **Python 3.7+**: Requires Python 3.7 or higher for async/await support
- **httpx Dependency**: AsyncClient uses httpx instead of requests
- **No Sync Fallback**: AsyncClient methods cannot be called from synchronous code without an event loop

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
