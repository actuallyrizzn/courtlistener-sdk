# CourtListener Python SDK — User Guide

Welcome to the CourtListener Python SDK! This guide will help you get started, use all major features, and follow best practices for working with the CourtListener API.

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

Install dependencies:
```bash
pip install -r requirements.txt
```

## Authentication

Set your API token in a `.env` file:
```
COURTLISTENER_API_TOKEN=your_token_here
```
Or pass it directly:
```python
from courtlistener import CourtListenerClient
client = CourtListenerClient(api_token="your_token_here")
```

## Quick Start

```python
from courtlistener import CourtListenerClient
client = CourtListenerClient()
dockets = client.dockets.list_dockets(page=1)
for docket in dockets:
    print(docket.case_name, docket.docket_number)
```

## API Endpoints

The SDK provides access to all public CourtListener endpoints:
- `client.courts` — Court information
- `client.dockets` — Docket records
- `client.opinions` — Judicial opinions
- `client.clusters` — Opinion clusters
- `client.positions` — Judicial positions
- `client.financial` — Financial disclosures
- `client.audio` — Oral argument audio
- `client.search` — Cross-resource search

Each endpoint provides methods like `list_*`, `get_*`, and `search_*` for flexible access.

### Example: List Opinions
```python
opinions = client.opinions.list_opinions(page=1, court="scotus")
for opinion in opinions:
    print(opinion.id, opinion.case_name)
```

### Example: Search
```python
results = client.search.search("first amendment", page=1)
for result in results.get('results', []):
    print(result)
```

## Pagination & Filtering

All `list_*` and `search_*` methods support pagination and filtering:
```python
# Get the second page of dockets for a specific court
page2 = client.dockets.list_dockets(page=2, court="scotus")

# Filter opinions by date
opinions = client.opinions.list_opinions(date_filed__gte="2020-01-01")
```

## Error Handling

The SDK raises custom exceptions for API errors:
- `CourtListenerError` — Base error
- `AuthenticationError` — Invalid/missing token
- `NotFoundError` — Resource not found
- `RateLimitError` — Too many requests
- `APIError` — Other API errors

Use try/except blocks to handle errors gracefully:
```python
try:
    dockets = client.dockets.list_dockets(page=1)
except CourtListenerError as e:
    print("API error:", e)
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