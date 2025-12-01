# CourtListener SDK — Advanced Usage (Unofficial)

This guide covers advanced features and power-user tips for the **unofficial** CourtListener SDK for both Python and PHP.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Table of Contents
- [Custom Filtering](#custom-filtering)
- [Iterating with Pagination](#iterating-with-pagination)
- [Handling Rate Limits](#handling-rate-limits)
- [Extending the SDK](#extending-the-sdk)
- [Debugging & Testing](#debugging--testing)
- [Language-Specific Features](#language-specific-features)

---

## Custom Filtering

All `list()` and `search()` methods accept arbitrary filters as parameters:

**Python:**
```python
# Filter dockets by court and date
results = client.dockets.list(court="scotus", date_filed__gte="2020-01-01")

# Filter financial disclosures by date range
disclosures = client.financial_disclosures.list(
    date_received__gte="2023-01-01",
    date_received__lte="2023-12-31"
)

# Complex search with multiple filters
results = client.search.list(
    q="constitutional law",
    court="scotus",
    date_filed__gte="2020-01-01",
    type="o"  # opinions only
)
```

**PHP:**
```php
// Filter dockets by court and date
$results = $client->dockets->listDockets(['court' => 'scotus', 'date_filed__gte' => '2020-01-01']);

// Filter financial disclosures by date range
$disclosures = $client->financialDisclosures->listFinancialDisclosures([
    'date_received__gte' => '2023-01-01',
    'date_received__lte' => '2023-12-31'
]);

// Complex search with multiple filters
$results = $client->search->search([
    'q' => 'constitutional law',
    'court' => 'scotus',
    'date_filed__gte' => '2020-01-01',
    'type' => 'o'  // opinions only
]);
```

## Iterating with Pagination

For large result sets, use pagination to iterate through all results:

**Python:**
```python
# Iterate through all dockets
for docket in client.dockets.list_all():
    print(docket.case_name)

# Iterate through all opinions with filtering
for opinion in client.opinions.list_all(court="scotus"):
    print(opinion.case_name)

# Iterate through financial disclosures
for disclosure in client.financial_disclosures.list_all():
    print(disclosure.id, disclosure.date_received)
```

**PHP:**
```php
use CourtListener\Utils\Pagination;

// Iterate through all dockets with manual pagination
$page = 1;
do {
    $dockets = $client->dockets->listDockets(Pagination::getParams($page, 100));
    foreach ($dockets['results'] as $docket) {
        echo $docket['case_name'] . "\n";
    }
    $page++;
} while (!empty($dockets['results']));

// Iterate through all opinions with filtering
$page = 1;
do {
    $opinions = $client->opinions->listOpinions(array_merge(
        ['court' => 'scotus'],
        Pagination::getParams($page, 100)
    ));
    foreach ($opinions['results'] as $opinion) {
        echo $opinion['case_name'] . "\n";
    }
    $page++;
} while (!empty($opinions['results']));
```

## Handling Rate Limits

If you receive HTTP 202 responses, the API is rate limiting or processing your request asynchronously. Best practices:
- Wait and retry after a delay
- Use exponential backoff for repeated requests
- Catch `RateLimitError` and handle gracefully

## Extending the SDK

You can add new endpoints or customize models by subclassing:

```python
from courtlistener.models.docket import Docket
class MyDocket(Docket):
    @property
    def custom_field(self):
        return self._data.get('custom_field')
```

## Advanced Examples

### Financial Disclosure Analysis
```python
# Get all financial disclosures for a specific year
disclosures = client.financial_disclosures.list(
    date_received__gte="2023-01-01",
    date_received__lte="2023-12-31"
)

# Analyze investment holdings
for disclosure in disclosures['results']:
    investments = client.investments.list(disclosure=disclosure['id'])
    for investment in investments['results']:
        print(f"Investment: {investment['description']} - ${investment['amount']}")

# Check for gifts
gifts = client.gifts.list(disclosure=disclosure['id'])
for gift in gifts['results']:
    print(f"Gift: {gift['description']} from {gift['source']}")
```

### Case Research Workflow
```python
# Search for cases
cases = client.search.list(q="first amendment", court="scotus")

for case in cases['results']:
    if case.type == 'o':  # Opinion
        opinion = client.opinions.get(case.id)
        print(f"Case: {opinion.case_name}")
        
        # Get related docket
        docket = client.dockets.get(opinion.docket)
        print(f"Court: {docket.court}")
        
        # Get parties
        parties = client.parties.list(docket=docket.id)
        for party in parties:
            print(f"Party: {party.name} ({party.type})")
        
        # Get attorneys
        attorneys = client.attorneys.list(docket=docket.id)
        for attorney in attorneys:
            print(f"Attorney: {attorney.name}")
```

### Alert Management
```python
# Create a search alert
alert = client.alerts.create({
    'name': 'Constitutional Law Alert',
    'query': 'constitutional law',
    'rate': 'daily'
})

# Create a docket alert
docket_alert = client.docket_alerts.create({
    'docket': 12345,
    'alert_type': 'docket'
})

# List all alerts
alerts = client.alerts.list()
for alert in alerts['results']:
    print(f"Alert: {alert['name']} - {alert['rate']}")
```

## Debugging & Testing

**Python:**
See `python/tests/manual_debug/` for scripts to:
- Test real API responses
- Debug endpoint availability
- Check model properties
- Run integration tests with real or mock data

**PHP:**
See `php/tests/` for comprehensive test suites:
- Unit tests (1,786 tests)
- Integration tests (12 tests)
- Mock tests (6 tests)
- Live tests (367 tests)
- E2E tests (3 tests)

Run tests with:
```bash
# Python
cd python && python -m pytest

# PHP
cd php && composer test
```

## Language-Specific Features

### Python Features
- **Iterator Support**: Built-in `list_all()` methods for easy pagination
- **Data Models**: Rich object-oriented models with properties and methods
- **Type Hints**: Full type annotation support for better IDE integration
- **Context Managers**: Automatic resource cleanup and error handling

### PHP Features
- **PSR-4 Autoloading**: Modern PHP autoloading standards
- **Array Access**: Models implement `ArrayAccess` for flexible data access
- **Utility Classes**: Dedicated `Pagination`, `Filters`, and `Validators` utilities
- **Composer Integration**: Easy dependency management and autoloading
- **Static Analysis**: PHPStan integration for code quality

### Performance Tips
- **Python**: Use `list_all()` for large datasets, cache frequently accessed data
- **PHP**: Use pagination utilities, implement proper error handling, leverage Composer's autoloading

---
For more, see the [User Guide](./user_guide.md) and [API Reference](./api_reference.md). 