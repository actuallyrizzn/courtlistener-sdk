# CourtListener Python SDK — API Reference

This reference documents all major classes, methods, and data models in the SDK.

## Table of Contents
- [CourtListenerClient](#courtlistenerclient)
- [API Modules](#api-modules)
- [Data Models](#data-models)
- [Error Classes](#error-classes)
- [See Also](#see-also)

---

## CourtListenerClient

The main entry point for the SDK.

```python
from courtlistener import CourtListenerClient
client = CourtListenerClient(api_token="your_token")
```

### Arguments
- `api_token` (str): Your API token
- `base_url` (str, optional): Override the API base URL
- `timeout`, `max_retries`, etc.: Advanced options

### Attributes
- `courts`, `dockets`, `opinions`, `clusters`, `positions`, `financial`, `audio`, `search`: API modules

## API Modules

Each module provides methods for a specific resource:

- `CourtsAPI`: `list_courts`, `get_court`, `search_courts`
- `DocketsAPI`: `list_dockets`, `get_docket`, `search_dockets`, etc.
- `OpinionsAPI`: `list_opinions`, `get_opinion`, `search_opinions`
- `ClustersAPI`: `list_clusters`, `get_cluster`, `search_clusters`
- `PositionsAPI`: `list_positions`, `get_position`, `search_positions`
- `FinancialAPI`: `list_financial_disclosures`, `get_disclosure`, `search_financial_disclosures`
- `AudioAPI`: `list_audio`, `get_audio`, `search_audio`
- `SearchAPI`: `search`, `search_opinions`, `search_dockets`, etc.

### Example: Get a Docket
```python
docket = client.dockets.get_docket(12345)
print(docket.case_name, docket.docket_number)
```

## Data Models

Each API returns model objects with properties matching the API fields:
- `Court`, `Docket`, `Opinion`, `OpinionCluster`, `Position`, `FinancialDisclosure`, `Audio`, etc.

### Example: Docket Model
```python
docket = client.dockets.get_docket(12345)
print(docket.case_name, docket.docket_number, docket.court_id)
```

## Error Classes

- `CourtListenerError`: Base error
- `AuthenticationError`: Invalid/missing token
- `NotFoundError`: Resource not found
- `RateLimitError`: Too many requests
- `APIError`: Other API errors

## See Also
- [User Guide](./user_guide.md)
- [Advanced Usage](./advanced_usage.md)
- [Troubleshooting](./troubleshooting.md) 