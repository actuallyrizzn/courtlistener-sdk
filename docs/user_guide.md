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
- [Core Concepts](#core-concepts)
- [API Endpoints](#api-endpoints)
- [Pagination & Filtering](#pagination--filtering)
- [Advanced Pagination](#advanced-pagination)
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

For detailed Python installation and setup, see [Python README](../python/README.md#installation).

### PHP SDK
```bash
cd php
composer install
```

For detailed PHP installation and setup, see [PHP README](../php/README.md#installation).

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

For detailed quick-start guides with more examples:

- **Python**: See [Python Quick Start](../python/README.md#quick-start)
- **PHP**: See [PHP Quick Start](../php/README.md#quick-start)

### Python
```python
from courtlistener import CourtListenerClient
client = CourtListenerClient()
dockets = client.dockets.list(page=1)
for docket in dockets:
    print(docket.case_name, docket.docket_number)
```

### PHP
```php
<?php
use CourtListener\CourtListenerClient;

$client = new CourtListenerClient();
$dockets = $client->dockets->list(['page' => 1]);
foreach ($dockets['results'] as $docket) {
    echo $docket['case_name'] . ' ' . $docket['docket_number'] . "\n";
}
```

## Core Concepts

### Data Models

The SDK returns model objects (Python) or arrays (PHP) that provide easy access to API data.

**Python** - Model objects with attribute access:
```python
docket = client.dockets.get(12345)
print(docket.case_name)  # Attribute access
print(docket.docket_number)
```

**PHP** - Arrays with key access:
```php
$docket = $client->dockets->get(12345);
echo $docket['case_name'];  // Array access
echo $docket['docket_number'];
```

### Standard Methods

All endpoints support these standard methods:
- `list(**kwargs)` - List resources with filtering and pagination
- `get(id)` - Get a specific resource by ID
- `search(**kwargs)` - Search resources with query parameters

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

### Example: List Opinions

**Python:**
```python
opinions = client.opinions.list(page=1, court="scotus")
for opinion in opinions:
    print(opinion.id, opinion.case_name)
```

**PHP:**
```php
$opinions = $client->opinions->list(['page' => 1, 'court' => 'scotus']);
foreach ($opinions['results'] as $opinion) {
    echo $opinion['id'] . ' ' . $opinion['case_name'] . "\n";
}
```

### Example: Search

**Python:**
```python
results = client.search.list(q="first amendment", page=1)
for result in results:
    print(result.case_name)
```

**PHP:**
```php
$results = $client->search->list(['q' => 'first amendment', 'page' => 1]);
foreach ($results['results'] as $result) {
    echo $result['case_name'] . "\n";
}
```

### Example: Financial Disclosures

**Python:**
```python
disclosures = client.financial_disclosures.list(page=1)
for disclosure in disclosures:
    print(disclosure.id, disclosure.date_received)
```

**PHP:**
```php
$disclosures = $client->financialDisclosures->list(['page' => 1]);
foreach ($disclosures['results'] as $disclosure) {
    echo $disclosure['id'] . ' ' . $disclosure['date_received'] . "\n";
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

// Get the second page of dockets for a specific court
$page2 = $client->dockets->list(['page' => 2, 'court' => 'scotus']);

// Filter opinions by date
$opinions = $client->opinions->list(['date_filed__gte' => '2020-01-01']);

// Filter financial disclosures by date range
$disclosures = $client->financialDisclosures->list([
    'date_received__gte' => '2023-01-01',
    'date_received__lte' => '2023-12-31'
]);

// Search with multiple filters
$results = $client->search->list([
    'q' => 'constitutional law',
    'court' => 'scotus',
    'date_filed__gte' => '2020-01-01'
]);
```

## Advanced Pagination

For large datasets, use advanced pagination patterns to efficiently retrieve all results.

### Python: Iterator Pattern

**Using paginate() method:**
```python
from courtlistener import CourtListenerClient

client = CourtListenerClient()

# Iterate through all dockets with automatic pagination
for docket in client.dockets.paginate(court="scotus"):
    print(f"Processing: {docket.case_name}")
    # Process each docket
```

**Manual pagination with progress tracking:**
```python
page = 1
total_processed = 0

while True:
    dockets = client.dockets.list(page=page, court="scotus", page_size=100)
    
    if not dockets:
        break
    
    for docket in dockets:
        # Process docket
        total_processed += 1
    
    print(f"Processed page {page}, total: {total_processed}")
    page += 1
    
    # Respect rate limits
    time.sleep(0.5)
```

**Bulk operations with pagination:**
```python
# Collect all IDs first, then process in batches
all_ids = []
page = 1

while True:
    opinions = client.opinions.list(page=page, court="scotus", page_size=100)
    if not opinions:
        break
    all_ids.extend([op.id for op in opinions])
    page += 1

# Process in batches
batch_size = 50
for i in range(0, len(all_ids), batch_size):
    batch = all_ids[i:i + batch_size]
    # Process batch
    print(f"Processing batch {i // batch_size + 1}")
```

### PHP: Manual Pagination

**Iterate through all results:**
```php
use CourtListener\CourtListenerClient;
use CourtListener\Utils\Pagination;

$client = new CourtListenerClient();
$page = 1;
$totalProcessed = 0;

do {
    $dockets = $client->dockets->list(array_merge(
        ['court' => 'scotus'],
        Pagination::getParams($page, 100)
    ));
    
    if (empty($dockets['results'])) {
        break;
    }
    
    foreach ($dockets['results'] as $docket) {
        // Process docket
        $totalProcessed++;
    }
    
    echo "Processed page $page, total: $totalProcessed\n";
    $page++;
    
    // Respect rate limits
    usleep(500000);  // 0.5 seconds
} while (!empty($dockets['results']));
```

**Bulk operations with pagination:**
```php
// Collect all IDs first, then process in batches
$allIds = [];
$page = 1;

do {
    $opinions = $client->opinions->list(array_merge(
        ['court' => 'scotus'],
        Pagination::getParams($page, 100)
    ));
    
    if (empty($opinions['results'])) {
        break;
    }
    
    foreach ($opinions['results'] as $opinion) {
        $allIds[] = $opinion['id'];
    }
    
    $page++;
} while (!empty($opinions['results']));

// Process in batches
$batchSize = 50;
for ($i = 0; $i < count($allIds); $i += $batchSize) {
    $batch = array_slice($allIds, $i, $batchSize);
    // Process batch
    echo "Processing batch " . (($i / $batchSize) + 1) . "\n";
}
```

For more advanced pagination examples, see [Advanced Usage Guide](./advanced_usage.md#iterating-with-pagination).

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
from courtlistener import CourtListenerClient
from courtlistener.exceptions import (
    CourtListenerError,
    RateLimitError,
    NotFoundError
)
import time

try:
    dockets = client.dockets.list(page=1)
except RateLimitError as e:
    print("Rate limited, waiting...")
    time.sleep(5)  # Wait before retrying
except NotFoundError as e:
    print("Resource not found:", e)
except CourtListenerError as e:
    print("API error:", e)
```

**PHP:**
```php
use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;
use CourtListener\Exceptions\AuthenticationException;
use CourtListener\Exceptions\RateLimitException;
use CourtListener\Exceptions\NotFoundException;

try {
    $dockets = $client->dockets->list(['page' => 1]);
} catch (RateLimitException $e) {
    echo "Rate limited, waiting...\n";
    sleep(5);  // Wait before retrying
} catch (NotFoundException $e) {
    echo "Resource not found: " . $e->getMessage() . "\n";
} catch (CourtListenerException $e) {
    echo "API error: " . $e->getMessage() . "\n";
}
```

## Best Practices

- **Use pagination** for large result sets to avoid memory issues
- **Respect API rate limits** - handle HTTP 202 responses and rate limit errors gracefully
- **Store API tokens securely** - use environment variables or secure configuration
- **Use data models** - leverage model objects (Python) for type safety and better IDE support
- **Handle errors** - always wrap API calls in try/catch blocks
- **Batch operations** - when processing many items, collect IDs first then process in batches
- **Progress tracking** - for long-running operations, track progress and allow for interruption

## Troubleshooting

- **HTTP 202 responses**: The API is rate limiting or processing your request asynchronously. Wait and retry.
- **Attribute errors**: Ensure you are using model objects correctly. In Python, use `obj.attribute` not `obj['key']`.
- **Rate limit errors**: Implement exponential backoff and respect `Retry-After` headers.
- **Not found errors**: Verify the resource ID exists and you have permission to access it.

For more troubleshooting help, see the [Troubleshooting Guide](./troubleshooting.md).

---

For full API details, see the [API Reference](./api_reference.md).  
For advanced usage patterns, see [Advanced Usage Guide](./advanced_usage.md).
