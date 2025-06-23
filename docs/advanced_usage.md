# CourtListener Python SDK — Advanced Usage

This guide covers advanced features and power-user tips for the SDK.

## Table of Contents
- [Custom Filtering](#custom-filtering)
- [Iterating with Pagination](#iterating-with-pagination)
- [Handling Rate Limits](#handling-rate-limits)
- [Extending the SDK](#extending-the-sdk)
- [Debugging & Testing](#debugging--testing)

---

## Custom Filtering

All `list_*` and `search_*` methods accept arbitrary filters as keyword arguments:

```python
# Filter dockets by court and date
results = client.dockets.list_dockets(court="scotus", date_filed__gte="2020-01-01")
```

## Iterating with Pagination

For large result sets, use the provided iterators:

```python
for docket in client.dockets.list_all_dockets():
    print(docket.case_name)
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

## Debugging & Testing

See `tests/manual_debug/` for scripts to:
- Test real API responses
- Debug endpoint availability
- Check model properties
- Run integration tests with real or mock data

You can extend these scripts or add your own for custom workflows. For example, to test a new endpoint, copy an existing script and modify the API calls as needed.

---
For more, see the [User Guide](./user_guide.md) and [API Reference](./api_reference.md). 