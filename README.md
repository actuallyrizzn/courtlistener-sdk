# CourtListener Python SDK

A robust, production-ready Python SDK for the [CourtListener API](https://www.courtlistener.com/api/).

## Features
- Full support for all public CourtListener endpoints
- Pythonic data models for courts, dockets, opinions, clusters, and more
- Robust error handling, pagination, and filtering
- 100% test coverage with real API integration
- Easy authentication via `.env` file or direct token
- Extensive documentation and examples

## Installation
```bash
pip install -r requirements.txt
```

## Quick Start
```python
from courtlistener import CourtListenerClient
client = CourtListenerClient()
dockets = client.dockets.list_dockets(page=1)
for docket in dockets:
    print(docket.case_name, docket.docket_number)
```

## Authentication
Set your API token in a `.env` file:
```
COURTLISTENER_API_TOKEN=your_token_here
```
Or pass it directly:
```python
client = CourtListenerClient(api_token="your_token_here")
```

## Tests & Debugging
All manual and debug test scripts are now in [`tests/manual_debug/`](./tests/manual_debug/). See the documentation for details on running and extending tests.

## Documentation
Extensive documentation is available in [`docs/`](./docs/), including:
- [User Guide](./docs/user_guide.md)
- [API Reference](./docs/api_reference.md)
- [Advanced Usage](./docs/advanced_usage.md)
- [Troubleshooting](./docs/troubleshooting.md)

## Changelog
See [`CHANGELOG.md`](./CHANGELOG.md) for release notes.

## License
See [`LICENSE`](./LICENSE).

---
For more, see the [full documentation](./docs/user_guide.md). 