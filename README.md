# CourtListener SDK (Unofficial)

Multi-language SDKs for the [CourtListener API](https://www.courtlistener.com/api/).

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Available Languages

### Python SDK
- **Location**: [`python/`](./python/)
- **Status**: ✅ Complete and Production Ready
- **Features**: 100% API coverage, comprehensive models, robust error handling
- **Installation**: `pip install -r python/requirements.txt`

### PHP SDK
- **Location**: [`php/`](./php/)
- **Status**: ✅ Complete and Production Ready
- **Features**: 100% API coverage, comprehensive models, robust error handling
- **Installation**: `composer install` (in `php/` directory)

## Features
- **100% API Coverage**: Complete support for all 36+ CourtListener API endpoints
- **Multi-Language Support**: Python (complete) and PHP (complete)
- **Comprehensive Data Models**: Language-specific models for all data types including financial disclosures, alerts, people, and more
- **Robust Error Handling**: Production-ready error handling with retry logic and rate limiting
- **Advanced Pagination**: Cursor-based pagination support for efficient data retrieval
- **Full CRUD Support**: Create, read, update, and delete operations for alerts and docket alerts
- **Comprehensive Test Coverage**: 2,174+ tests across both languages with real API integration tests
- **Easy Authentication**: Simple authentication via `.env` file or direct token
- **Extensive Documentation**: Complete API reference and usage examples

## Quick Start

### Python
```bash
cd python
pip install -r requirements.txt
```

```python
from courtlistener import CourtListenerClient
client = CourtListenerClient()
dockets = client.dockets.list(page=1)
for docket in dockets['results']:
    print(docket['case_name'], docket['docket_number'])
```

### PHP
```bash
cd php
composer install
```

```php
<?php
use CourtListener\CourtListenerClient;

$client = new CourtListenerClient();
$dockets = $client->dockets->list(['page' => 1]);
foreach ($dockets['results'] as $docket) {
    echo $docket['case_name'] . ' ' . $docket['docket_number'] . "\n";
}
```

## Development Tooling

Run these repo-root targets to keep both SDKs in sync:

| Command | Purpose |
|---------|---------|
| `make bootstrap` | Install Python dev extras (`pip install -e ".[dev]"`) and PHP Composer deps. |
| `make lint` | Run `black`, `flake8`, `mypy`, and `phpstan` in one go. Use `python-lint`/`php-lint` for individual SDKs. |
| `make test` | Execute `pytest` and `composer test`. |
| `make build` | Produce Python sdists/wheels (`python -m build`) and optimize Composer autoloaders. |
| `make docs` | Validate Markdown links across `docs/` plus each language README via `tools/check_docs.py`. |
| `make release` | Sanity-check Python artifacts with `twine check` and package the PHP SDK as a zip via `composer archive`. |
| `make clean` | Remove virtualenv caches, build artifacts, and Composer vendor installs. |

All targets accept the usual overrides (e.g., `PYTHON=python3.12 make python-test`). Use `make help` to list every available command.

## Available Endpoints

Both Python and PHP SDKs provide access to all CourtListener API endpoints:

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

### Python
```python
client = CourtListenerClient(api_token="your_token_here")
```

### PHP
```php
$client = new CourtListenerClient(['api_token' => 'your_token_here']);
```

## Tests & Debugging

### Python
All manual and debug test scripts are in [`python/tests/manual_debug/`](./python/tests/manual_debug/). See the documentation for details on running and extending tests.

### PHP
Comprehensive test suite with 2,174+ tests including unit, integration, mock, live, and E2E tests. Run with:
```bash
cd php
composer test
```

## Documentation
Extensive documentation is available in [`docs/`](./docs/), including:
- [User Guide](./docs/user_guide.md)
- [API Reference](./docs/api_reference.md)
- [Advanced Usage](./docs/advanced_usage.md)
- [Troubleshooting](./docs/troubleshooting.md)

### Language-Specific Documentation
- **Python**: See [`python/README.md`](./python/README.md) for Python-specific details
- **PHP**: See [`php/README.md`](./php/README.md) for PHP-specific details

## Changelog
See [`CHANGELOG.md`](./CHANGELOG.md) for release notes.

## License
See [`LICENSE`](./LICENSE).

---
For more, see the [full documentation](./docs/user_guide.md). 