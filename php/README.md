# CourtListener PHP SDK (Unofficial)

An **unofficial**, robust, production-ready PHP SDK for the [CourtListener API](https://www.courtlistener.com/api/rest/v4/).

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Features
- **100% API Coverage**: Complete support for all 39 CourtListener API endpoints
- **Comprehensive Data Models**: PHP classes for all data types including financial disclosures, alerts, people, and more
- **Robust Error Handling**: Production-ready error handling with retry logic and rate limiting
- **Advanced Pagination**: Cursor-based pagination support for efficient data retrieval
- **Full CRUD Support**: Create, read, update, and delete operations for alerts and docket alerts
- **Easy Authentication**: Simple authentication via environment variables or direct token
- **Extensive Documentation**: Complete API reference and usage examples
- **PSR-4 Autoloading**: Modern PHP autoloading standards
- **Comprehensive Testing**: 2,174+ tests including unit, integration, mock, live, and E2E tests
- **Code Quality Tools**: PHPStan, PHP_CodeSniffer, and PHP-CS-Fixer integration
- **Production Ready**: Battle-tested with real API integration and comprehensive error handling

## Installation

```bash
composer install
```

## Quick Start

```php
<?php
require_once 'vendor/autoload.php';

use CourtListener\CourtListenerClient;

$client = new CourtListenerClient(['api_token' => 'your_token_here']);
$dockets = $client->dockets->listDockets(['page' => 1]);
foreach ($dockets['results'] as $docket) {
    echo $docket['case_name'] . ' ' . $docket['docket_number'] . "\n";
}
```

## Authentication

Set your API token in a `.env` file:
```
COURTLISTENER_API_TOKEN=your_token_here
```

Or pass it directly:
```php
$client = new CourtListenerClient(['api_token' => 'your_token_here']);
```

## Available Endpoints

The SDK provides access to all CourtListener API endpoints:

### Core Endpoints
- `$client->courts` — Court information and hierarchy
- `$client->dockets` — Docket records and case information
- `$client->opinions` — Judicial opinions and decisions
- `$client->clusters` — Opinion clusters and related cases
- `$client->judges` — Judicial biographical data
- `$client->positions` — Judicial positions and appointments
- `$client->audio` — Oral argument audio recordings
- `$client->search` — Cross-resource search functionality

### Financial & Disclosure Endpoints
- `$client->financial` — Financial disclosure records
- `$client->financialDisclosures` — Detailed financial disclosures
- `$client->investments` — Investment holdings
- `$client->nonInvestmentIncomes` — Non-investment income sources
- `$client->gifts` — Gift disclosures
- `$client->reimbursements` — Reimbursement records
- `$client->debts` — Debt disclosures
- `$client->spouseIncomes` — Spouse income information
- `$client->agreements` — Financial agreements

### Case & Legal Endpoints
- `$client->docketEntries` — Individual docket entries
- `$client->parties` — Case participants and parties
- `$client->attorneys` — Legal representation
- `$client->documents` — RECAP document management
- `$client->recapDocuments` — RECAP document access
- `$client->citations` — Citation graph and verification
- `$client->opinionsCited` — Opinion citation relationships

### People & Education Endpoints
- `$client->people` — People and biographical data
- `$client->schools` — Educational institutions
- `$client->educations` — Educational background
- `$client->abaRatings` — ABA judicial ratings
- `$client->politicalAffiliations` — Political affiliations

### Alert & Notification Endpoints
- `$client->alerts` — Search alerts and notifications
- `$client->docketAlerts` — Docket-specific alerts

### Administrative Endpoints
- `$client->sources` — Data sources
- `$client->retentionEvents` — Data retention events
- `$client->tag` — Tagging system
- `$client->recapFetch` — RECAP fetch operations
- `$client->recapQuery` — RECAP query operations
- `$client->originatingCourtInformation` — Court origin data
- `$client->fjcIntegratedDatabase` — FJC database integration
- `$client->disclosurePositions` — Disclosure position data

## Usage Examples

### Basic Usage
```php
<?php
use CourtListener\CourtListenerClient;
use CourtListener\Utils\Pagination;

$client = new CourtListenerClient();

// List dockets
$dockets = $client->dockets->listDockets(Pagination::getParams(1, 10));

// Search opinions
$opinions = $client->opinions->searchOpinions([
    'q' => 'copyright',
    'order_by' => '-date_filed'
]);

// Get specific docket
$docket = $client->dockets->getDocket(12345);
```

### Advanced Usage
```php
<?php
use CourtListener\CourtListenerClient;
use CourtListener\Utils\Filters;
use CourtListener\Utils\Pagination;

$client = new CourtListenerClient();

// Complex search with filters
$filters = array_merge(
    Filters::dateRange('2023-01-01', '2023-12-31'),
    Filters::contains('patent', 'case_name'),
    Filters::orderBy('date_filed', 'desc'),
    Pagination::getParams(1, 20)
);

$results = $client->dockets->searchDockets($filters);
```

## Error Handling

```php
<?php
use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\AuthenticationException;
use CourtListener\Exceptions\RateLimitException;
use CourtListener\Exceptions\NotFoundException;

try {
    $client = new CourtListenerClient();
    $dockets = $client->dockets->listDockets();
} catch (AuthenticationException $e) {
    echo "Authentication failed: " . $e->getMessage();
} catch (RateLimitException $e) {
    echo "Rate limit exceeded: " . $e->getMessage();
} catch (NotFoundException $e) {
    echo "Resource not found: " . $e->getMessage();
}
```

## Testing

The PHP SDK includes a comprehensive test suite with 2,174+ tests across multiple categories:

### Test Categories
- **Unit Tests**: 1,786 tests covering individual components
- **Integration Tests**: 12 tests for component integration
- **Mock Tests**: 6 tests using mocked dependencies
- **Live Tests**: 367 tests against real CourtListener API
- **E2E Tests**: 3 end-to-end workflow tests

### Running Tests

Run all tests:
```bash
composer test
```

Run specific test suites:
```bash
composer test-unit          # Unit tests only
composer test-integration   # Integration tests only
composer test-mock          # Mock tests only
composer test-live          # Live API tests only
composer test-e2e           # E2E tests only
```

Run with coverage:
```bash
composer test-coverage      # All tests with HTML coverage report
composer test-coverage-unit # Unit tests with coverage
composer test-coverage-all  # All tests with coverage
```

### Live API Testing

Live tests require a valid CourtListener API token. Set it in your environment:
```bash
export COURTLISTENER_API_TOKEN=your_token_here
```

Or create a `.env` file:
```
COURTLISTENER_API_TOKEN=your_token_here
```

## Code Quality

Check code style:
```bash
composer cs-check
```

Fix code style issues:
```bash
composer cs-fix
```

Run static analysis:
```bash
composer stan
```

Run all quality checks:
```bash
composer quality
```

## Examples

See the `examples/` directory for comprehensive usage examples:
- `basic_usage.php` - Basic SDK usage
- `advanced_usage.php` - Advanced features and patterns

## Requirements

- PHP 8.1 or higher
- Composer
- GuzzleHttp 7.0+
- vlucas/phpdotenv 5.0+

## Development

### Project Structure
```
src/
├── CourtListener/
│   ├── Api/           # API endpoint classes
│   ├── Models/        # Data model classes
│   ├── Utils/         # Utility classes
│   └── Exceptions/    # Exception classes
tests/
├── Unit/              # Unit tests
examples/              # Usage examples
```

### Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run quality checks
6. Submit a pull request

## Documentation

Extensive documentation is available in the [`../docs/`](../docs/) directory, including:
- [User Guide](../docs/user_guide.md)
- [API Reference](../docs/api_reference.md)
- [Advanced Usage](../docs/advanced_usage.md)
- [Troubleshooting](../docs/troubleshooting.md)

## Changelog

See [`../CHANGELOG.md`](../CHANGELOG.md) for release notes.

## License

See [`../LICENSE`](../LICENSE).

---

For more information about the overall project, see the [main README](../README.md).
