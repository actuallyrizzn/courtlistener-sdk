# CourtListener SDK — User Guide (Unofficial)

Welcome to the **unofficial** CourtListener SDK! This guide covers both Python and PHP implementations and will help you get started, use all major features, and follow best practices for working with the CourtListener API.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Language Support

- **Python SDK**: ✅ Complete and Production Ready (see [`python/`](../python/))
- **PHP SDK**: ✅ Complete and Production Ready (see [`php/`](../php/))

## Table of Contents
- [Installation](#installation)
- [Authentication](#authentication)
- [Quick Start](#quick-start)
- [API Endpoints](#api-endpoints)
- [Pagination & Filtering](#pagination--filtering)
- [Error Handling](#error-handling)
- [Best Practices](#best-practices)
- [Troubleshooting](#troubleshooting)

---

## Installation

### Python SDK
```bash
cd python
pip install -r requirements.txt
```

### PHP SDK
```bash
cd php
composer install
```

## Authentication

Set your API token in a `.env` file:
```
COURTLISTENER_API_TOKEN=your_token_here
```

### Python
```python
from courtlistener import CourtListenerClient
client = CourtListenerClient(api_token="your_token_here")
```

### PHP
```php
<?php
use CourtListener\CourtListenerClient;
$client = new CourtListenerClient(['api_token' => 'your_token_here']);
```

## Quick Start

### Python
```python
from courtlistener import CourtListenerClient
client = CourtListenerClient()
dockets = client.dockets.list_dockets(page=1)
for docket in dockets:
    print(docket.case_name, docket.docket_number)
```

### PHP
```php
<?php
use CourtListener\CourtListenerClient;

$client = new CourtListenerClient();
$dockets = $client->dockets->listDockets(['page' => 1]);
foreach ($dockets['results'] as $docket) {
    echo $docket['case_name'] . ' ' . $docket['docket_number'] . "\n";
}
```

## API Endpoints

The SDK provides access to all 39 CourtListener API endpoints, organized by category:

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

Each endpoint provides methods like `list()`, `get()`, and `search()` for flexible access.

### Example: List Opinions

**Python:**
```python
opinions = client.opinions.list(page=1, court="scotus")
for opinion in opinions['results']:
    print(opinion['id'], opinion['case_name'])
```

**PHP:**
```php
$opinions = $client->opinions->listOpinions(['page' => 1, 'court' => 'scotus']);
foreach ($opinions['results'] as $opinion) {
    echo $opinion['id'] . ' ' . $opinion['case_name'] . "\n";
}
```

### Example: Search

**Python:**
```python
results = client.search.list(q="first amendment", page=1)
for result in results['results']:
    print(result['case_name'])
```

**PHP:**
```php
$results = $client->search->search(['q' => 'first amendment', 'page' => 1]);
foreach ($results['results'] as $result) {
    echo $result['case_name'] . "\n";
}
```

### Example: Financial Disclosures

**Python:**
```python
disclosures = client.financial_disclosures.list(page=1)
for disclosure in disclosures['results']:
    print(disclosure['id'], disclosure['date_received'])
```

**PHP:**
```php
$disclosures = $client->financialDisclosures->listFinancialDisclosures(['page' => 1]);
foreach ($disclosures['results'] as $disclosure) {
    echo $disclosure['id'] . ' ' . $disclosure['date_received'] . "\n";
}
```

### Example: Docket Entries

**Python:**
```python
entries = client.docket_entries.list(docket=12345, page=1)
for entry in entries['results']:
    print(entry['entry_number'], entry['description'])
```

**PHP:**
```php
$entries = $client->docketEntries->listDocketEntries(['docket' => 12345, 'page' => 1]);
foreach ($entries['results'] as $entry) {
    echo $entry['entry_number'] . ' ' . $entry['description'] . "\n";
}
```

## Pagination & Filtering

All `list()` and `search()` methods support pagination and filtering:

**Python:**
```python
# Get the second page of dockets for a specific court
page2 = client.dockets.list(page=2, court="scotus")

# Filter opinions by date
opinions = client.opinions.list(date_filed__gte="2020-01-01")

# Filter financial disclosures by date range
disclosures = client.financial_disclosures.list(
    date_received__gte="2023-01-01",
    date_received__lte="2023-12-31"
)

# Search with multiple filters
results = client.search.list(
    q="constitutional law",
    court="scotus",
    date_filed__gte="2020-01-01"
)
```

**PHP:**
```php
use CourtListener\Utils\Pagination;
use CourtListener\Utils\Filters;

// Get the second page of dockets for a specific court
$page2 = $client->dockets->listDockets(['page' => 2, 'court' => 'scotus']);

// Filter opinions by date
$opinions = $client->opinions->listOpinions(['date_filed__gte' => '2020-01-01']);

// Filter financial disclosures by date range
$disclosures = $client->financialDisclosures->listFinancialDisclosures([
    'date_received__gte' => '2023-01-01',
    'date_received__lte' => '2023-12-31'
]);

// Search with multiple filters
$results = $client->search->search([
    'q' => 'constitutional law',
    'court' => 'scotus',
    'date_filed__gte' => '2020-01-01'
]);
```

## Error Handling

The SDK raises custom exceptions for API errors:

**Python:**
- `CourtListenerError` — Base error
- `AuthenticationError` — Invalid/missing token
- `NotFoundError` — Resource not found
- `RateLimitError` — Too many requests
- `APIError` — Other API errors

**PHP:**
- `CourtListenerException` — Base error
- `AuthenticationException` — Invalid/missing token
- `NotFoundException` — Resource not found
- `RateLimitException` — Too many requests
- `ServerException` — Other API errors

Use try/catch blocks to handle errors gracefully:

**Python:**
```python
try:
    dockets = client.dockets.list(page=1)
except CourtListenerError as e:
    print("API error:", e)
except RateLimitError as e:
    print("Rate limited, waiting...")
    time.sleep(5)  # Wait before retrying
except NotFoundError as e:
    print("Resource not found:", e)
```

**PHP:**
```php
use CourtListener\Exceptions\CourtListenerException;
use CourtListener\Exceptions\AuthenticationException;
use CourtListener\Exceptions\RateLimitException;
use CourtListener\Exceptions\NotFoundException;

try {
    $dockets = $client->dockets->listDockets(['page' => 1]);
} catch (CourtListenerException $e) {
    echo "API error: " . $e->getMessage();
} catch (RateLimitException $e) {
    echo "Rate limited, waiting...";
    sleep(5);  // Wait before retrying
} catch (NotFoundException $e) {
    echo "Resource not found: " . $e->getMessage();
}
```

## Best Practices
- Use pagination for large result sets
- Respect API rate limits (handle HTTP 202 responses)
- Store your API token securely
- Use the provided data models for type safety
- See `tests/manual_debug/` for advanced test scripts

## Troubleshooting
- If you see HTTP 202 responses, wait and retry (API is rate limiting or processing)
- For attribute errors, ensure you are using the correct data model
- See [Troubleshooting Guide](./troubleshooting.md) for more

---
For full API details, see the [API Reference](./api_reference.md). 