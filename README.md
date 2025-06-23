# CourtListener SDK

A comprehensive Python SDK for the CourtListener REST API (v4.1). Provides easy access to legal data including case law, dockets, judges, opinions, financial disclosures, and citation networks.

## Features

- **Complete API Coverage**: All 14 CourtListener API endpoints implemented
- **Intuitive Interface**: Easy-to-use Python classes and methods
- **Automatic Pagination**: Handle large result sets with built-in pagination
- **Data Models**: Rich data models with automatic parsing and validation
- **Error Handling**: Comprehensive error handling with custom exceptions
- **Type Hints**: Full type annotation support
- **Documentation**: Complete documentation and examples

## Installation

```bash
pip install courtlistener-sdk
```

## Quick Start

```python
from courtlistener import CourtListenerClient

# Initialize client with your API token
client = CourtListenerClient(api_token="your_api_token_here")

# Search for opinions
results = client.search.search("constitutional rights")

# Get a specific docket
docket = client.dockets.get_docket(12345)

# List all courts
courts = client.courts.list_courts()

# Get opinions from Supreme Court
scotus_opinions = client.opinions.list_opinions(filters={'court': 'scotus'})
```

## API Endpoints

The SDK provides access to all CourtListener API endpoints:

- **Search API**: Cross-resource search functionality
- **Dockets**: Case records and metadata
- **Opinions**: Full-text judicial decisions
- **Judges**: Judicial biographical data
- **Courts**: Court information
- **Parties**: Case participants
- **Attorneys**: Legal representation
- **Documents**: PDF filings and downloads
- **Audio**: Oral argument recordings
- **Financial Disclosures**: Judicial financial data
- **Citations**: Citation graph and verification

## Documentation

For detailed documentation, see the [docs/](docs/) directory:

- [Getting Started Guide](docs/getting_started.md)
- [API Reference](docs/api_reference.md)
- [Examples](docs/examples.md)
- [Project Plan](docs/project-plan.md)

## Development

This project is currently in development. See the [project plan](docs/project-plan.md) for the complete roadmap.

## License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please see CONTRIBUTING.md for guidelines. 