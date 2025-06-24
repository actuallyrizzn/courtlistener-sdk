# Changelog - CourtListener SDK (Unofficial)

All notable changes to this **unofficial** CourtListener Python SDK project will be documented in this file.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Initial project scaffolding
- Complete API endpoint structure for all 14 CourtListener APIs
- Base client with authentication and error handling
- Comprehensive data models with automatic parsing
- Pagination utilities for cursor-based pagination
- Filter utilities for Django-style query building
- Input validation for all data types
- Custom exception hierarchy
- Configuration management with environment variable support
- Retry logic with exponential backoff
- Rate limiting support
- Type hints throughout the codebase
- Moved all manual/debug test scripts to `tests/manual_debug/` for better organization
- Added extensive documentation in `docs/` (User Guide, API Reference, Advanced Usage, Troubleshooting)
- Updated README to reflect new structure and documentation

### Changed
- Switched license from MIT to Creative Commons Attribution-ShareAlike 4.0 International

### Fixed
- N/A
- Ensured all test and debug files are organized and referenced in documentation

### Deprecated
- N/A

### Removed
- N/A

### Security
- N/A

## [0.1.0] - 2024-01-XX

### Added
- **Core Infrastructure**
  - Main `CourtListenerClient` class with full API integration
  - Configuration management with environment variable support
  - Comprehensive exception handling with custom error types
  - Session management with automatic retry logic
  - Rate limiting and timeout handling

- **API Modules** (14 endpoints)
  - Search API with cross-resource search functionality
  - Dockets API with filtering and pagination
  - Opinions API for judicial decisions
  - Judges API for judicial biographical data
  - Courts API for court information
  - Parties API for case participants
  - Attorneys API for legal representation
  - Documents API for RECAP document management
  - Audio API for oral argument recordings
  - Financial API for judicial financial disclosures
  - Citations API for citation graph and verification

- **Data Models**
  - Base model with JSON serialization and date parsing
  - Complete model hierarchy for all API entities
  - Automatic relationship parsing and model instantiation
  - Type-safe data access with validation

- **Utility Functions**
  - Pagination utilities for cursor-based pagination
  - Filter building utilities for Django-style queries
  - Input validation for dates, citations, IDs, and URLs
  - Date range filtering and formatting

- **Development Tools**
  - Comprehensive test framework with pytest
  - Code quality tools configuration (black, flake8, mypy)
  - Documentation structure and examples
  - Project packaging with setuptools

### Technical Details
- **Python Version**: 3.8+
- **Dependencies**: requests>=2.28.0, typing-extensions>=4.0.0
- **License**: Creative Commons Attribution-ShareAlike 4.0 International
- **Development Status**: Alpha (3 - Alpha)

### API Coverage
- ✅ Search API (`/api/rest/v4/search/`)
- ✅ Dockets API (`/api/rest/v4/dockets/`)
- ✅ Docket Entries API (`/api/rest/v4/docket-entries/`)
- ✅ Parties API (`/api/rest/v4/parties/`)
- ✅ Attorneys API (`/api/rest/v4/attorneys/`)
- ✅ RECAP Documents API (`/api/rest/v4/recap-documents/`)
- ✅ Opinions API (`/api/rest/v4/opinions/`)
- ✅ Opinion Clusters API (`/api/rest/v4/clusters/`)
- ✅ Courts API (`/api/rest/v4/courts/`)
- ✅ Judges API (`/api/rest/v4/judges/`)
- ✅ Positions API (`/api/rest/v4/positions/`)
- ✅ Oral Arguments API (`/api/rest/v3/audio/`)
- ✅ Financial Disclosures API (`/api/rest/v4/financial-disclosures/`)
- ✅ Citation APIs (`/api/rest/v4/opinions-cited/`, `/api/rest/v3/citation-lookup/`)

### Features
- **Authentication**: Token-based API authentication
- **Pagination**: Cursor-based pagination for all endpoints
- **Filtering**: Django-style filters with advanced query building
- **Error Handling**: Comprehensive exception hierarchy
- **Retry Logic**: Automatic retry with exponential backoff
- **Rate Limiting**: Built-in rate limit detection and handling
- **Type Safety**: Full type annotation support
- **Data Validation**: Input validation for all parameters
- **Model Serialization**: JSON serialization and deserialization
- **Date Parsing**: Automatic date and datetime parsing

---

## Version History

### Version 0.1.0 (Current)
- **Status**: Alpha
- **Release Date**: 2024-01-XX
- **Description**: Initial release with complete project scaffolding and basic API integration
- **Key Features**: All 14 API endpoints implemented, comprehensive data models, pagination, filtering, error handling

### Future Versions
- **0.2.0**: Enhanced API functionality and comprehensive testing
- **0.3.0**: Advanced features and performance optimizations
- **0.4.0**: Documentation completion and example applications
- **1.0.0**: Production-ready release with full feature set

---

## Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details on how to submit pull requests, report issues, and contribute to the project.

## License

This project is licensed under the Creative Commons Attribution-ShareAlike 4.0 International License. See the [LICENSE](LICENSE) file for details. 