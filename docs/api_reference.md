# CourtListener Python SDK — API Reference (Unofficial)

This reference documents all major classes, methods, and data models in the **unofficial** CourtListener Python SDK.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

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
All API modules are available as client attributes:

**Core Endpoints:**
- `courts`, `dockets`, `opinions`, `clusters`, `judges`, `positions`, `audio`, `search`

**Financial & Disclosure Endpoints:**
- `financial`, `financial_disclosures`, `investments`, `non_investment_incomes`, `gifts`, `reimbursements`, `debts`, `spouse_incomes`, `agreements`

**Case & Legal Endpoints:**
- `docket_entries`, `parties`, `attorneys`, `documents`, `recap_documents`, `citations`, `opinions_cited`

**People & Education Endpoints:**
- `people`, `schools`, `educations`, `aba_ratings`, `political_affiliations`

**Alert & Notification Endpoints:**
- `alerts`, `docket_alerts`

**Administrative Endpoints:**
- `sources`, `retention_events`, `tag`, `recap_fetch`, `recap_query`, `originating_court_information`, `fjc_integrated_database`, `disclosure_positions`

## API Modules

Each module provides methods for a specific resource:

### Core Modules
- `CourtsAPI`: `list()`, `get()`, `search()`
- `DocketsAPI`: `list()`, `get()`, `search()`
- `OpinionsAPI`: `list()`, `get()`, `search()`
- `ClustersAPI`: `list()`, `get()`, `search()`
- `JudgesAPI`: `list()`, `get()`, `search()`
- `PositionsAPI`: `list()`, `get()`, `search()`
- `AudioAPI`: `list()`, `get()`, `search()`
- `SearchAPI`: `list()`, `search_opinions()`, `search_dockets()`, etc.

### Financial & Disclosure Modules
- `FinancialAPI`: `list()`, `get()`, `search()`
- `FinancialDisclosuresAPI`: `list()`, `get()`, `search()`
- `InvestmentsAPI`: `list()`, `get()`, `search()`
- `NonInvestmentIncomesAPI`: `list()`, `get()`, `search()`
- `GiftsAPI`: `list()`, `get()`, `search()`
- `ReimbursementsAPI`: `list()`, `get()`, `search()`
- `DebtsAPI`: `list()`, `get()`, `search()`
- `SpouseIncomesAPI`: `list()`, `get()`, `search()`
- `AgreementsAPI`: `list()`, `get()`, `search()`

### Case & Legal Modules
- `DocketEntriesAPI`: `list()`, `get()`, `search()`
- `PartiesAPI`: `list()`, `get()`, `search()`
- `AttorneysAPI`: `list()`, `get()`, `search()`
- `DocumentsAPI`: `list()`, `get()`, `search()`
- `RecapDocumentsAPI`: `list()`, `get()`, `search()`
- `CitationsAPI`: `list()`, `get()`, `search()`
- `OpinionsCitedAPI`: `list()`, `get()`, `search()`

### People & Education Modules
- `PeopleAPI`: `list()`, `get()`, `search()`
- `SchoolsAPI`: `list()`, `get()`, `search()`
- `EducationsAPI`: `list()`, `get()`, `search()`
- `ABARatingsAPI`: `list()`, `get()`, `search()`
- `PoliticalAffiliationsAPI`: `list()`, `get()`, `search()`

### Alert & Notification Modules
- `AlertsAPI`: `list()`, `get()`, `create()`, `update()`, `delete()`
- `DocketAlertsAPI`: `list()`, `get()`, `create()`, `update()`, `delete()`

### Administrative Modules
- `SourcesAPI`: `list()`, `get()`, `search()`
- `RetentionEventsAPI`: `list()`, `get()`, `search()`
- `TagAPI`: `list()`, `get()`, `search()`
- `RecapFetchAPI`: `list()`, `get()`, `search()`
- `RecapQueryAPI`: `list()`, `get()`, `search()`
- `OriginatingCourtInformationAPI`: `list()`, `get()`, `search()`
- `FJCIntegratedDatabaseAPI`: `list()`, `get()`, `search()`
- `DisclosurePositionsAPI`: `list()`, `get()`, `search()`

### Example: Get a Docket
```python
docket = client.dockets.get(12345)
print(docket['case_name'], docket['docket_number'])
```

### Example: List Financial Disclosures
```python
disclosures = client.financial_disclosures.list(page=1)
for disclosure in disclosures['results']:
    print(disclosure['id'], disclosure['date_received'])
```

### Example: Search with Filters
```python
results = client.search.list(
    q="constitutional law",
    court="scotus",
    date_filed__gte="2020-01-01"
)
for result in results['results']:
    print(result['case_name'])
```

## Data Models

Each API returns dictionaries with fields matching the API response structure. The SDK also provides model classes for type safety and convenience:

### Available Models
- **Core Models**: `Court`, `Docket`, `Opinion`, `OpinionCluster`, `Judge`, `Position`, `Audio`
- **Financial Models**: `FinancialDisclosure`, `Investment`, `Gift`, `Reimbursement`, `Debt`, `SpouseIncome`, `Agreement`
- **Case Models**: `DocketEntry`, `Party`, `Attorney`, `Document`, `RecapDocument`, `Citation`, `OpinionCited`
- **People Models**: `Person`, `School`, `Education`, `ABARating`, `PoliticalAffiliation`
- **Alert Models**: `Alert`, `DocketAlert`
- **Administrative Models**: `Source`, `RetentionEvent`, `Tag`, `RecapFetch`, `RecapQuery`, `OriginatingCourtInformation`, `FJCIntegratedDatabase`, `DisclosurePosition`

### Example: Using Models
```python
from courtlistener.models import Docket, Opinion, FinancialDisclosure

# API returns dictionaries
docket_data = client.dockets.get(12345)
print(docket_data['case_name'])

# Convert to model for type safety
docket = Docket(docket_data)
print(docket.case_name, docket.docket_number)
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