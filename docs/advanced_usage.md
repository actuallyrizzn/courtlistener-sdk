# CourtListener Python SDK — Advanced Usage (Unofficial)

This guide covers advanced features and power-user tips for the **unofficial** CourtListener Python SDK.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Table of Contents
- [Custom Filtering](#custom-filtering)
- [Iterating with Pagination](#iterating-with-pagination)
- [Handling Rate Limits](#handling-rate-limits)
- [Extending the SDK](#extending-the-sdk)
- [Debugging & Testing](#debugging--testing)

---

## Custom Filtering

All `list()` and `search()` methods accept arbitrary filters as keyword arguments:

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

## Iterating with Pagination

For large result sets, use the provided iterators:

```python
# Iterate through all dockets
for docket in client.dockets.list_all():
    print(docket['case_name'])

# Iterate through all opinions with filtering
for opinion in client.opinions.list_all(court="scotus"):
    print(opinion['case_name'])

# Iterate through financial disclosures
for disclosure in client.financial_disclosures.list_all():
    print(disclosure['id'], disclosure['date_received'])
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
    if case['type'] == 'o':  # Opinion
        opinion = client.opinions.get(case['id'])
        print(f"Case: {opinion['case_name']}")
        
        # Get related docket
        docket = client.dockets.get(opinion['docket'])
        print(f"Court: {docket['court']}")
        
        # Get parties
        parties = client.parties.list(docket=docket['id'])
        for party in parties['results']:
            print(f"Party: {party['name']} ({party['type']})")
        
        # Get attorneys
        attorneys = client.attorneys.list(docket=docket['id'])
        for attorney in attorneys['results']:
            print(f"Attorney: {attorney['name']}")
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

See `tests/manual_debug/` for scripts to:
- Test real API responses
- Debug endpoint availability
- Check model properties
- Run integration tests with real or mock data

You can extend these scripts or add your own for custom workflows. For example, to test a new endpoint, copy an existing script and modify the API calls as needed.

---
For more, see the [User Guide](./user_guide.md) and [API Reference](./api_reference.md). 