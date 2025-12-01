# CourtListener SDK — API Reference (Unofficial)

This reference documents all major classes, methods, and data models in the **unofficial** CourtListener SDK for both Python and PHP.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Table of Contents
- [Python SDK](#python-sdk)
  - [CourtListenerClient](#courtlistenerclient-python)
  - [API Modules](#api-modules-python)
  - [Data Models](#data-models-python)
  - [Error Classes](#error-classes-python)
- [PHP SDK](#php-sdk)
  - [CourtListenerClient](#courtlistenerclient-php)
  - [API Modules](#api-modules-php)
  - [Data Models](#data-models-php)
  - [Error Classes](#error-classes-php)
- [See Also](#see-also)

---

## Python SDK

### CourtListenerClient (Python)

The main entry point for the Python SDK.

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
print(docket.case_name, docket.docket_number)
```

### Example: List Financial Disclosures
```python
disclosures = client.financial_disclosures.list(page=1)
for disclosure in disclosures:
    print(disclosure.id, disclosure.date_received)
```

### Example: Search with Filters
```python
results = client.search.list(
    q="constitutional law",
    court="scotus",
    date_filed__gte="2020-01-01"
)
for result in results:
    print(result.case_name)
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

### Error Classes (Python)

- `CourtListenerError`: Base error
- `AuthenticationError`: Invalid/missing token
- `NotFoundError`: Resource not found
- `RateLimitError`: Too many requests
- `APIError`: Other API errors

---

## PHP SDK

### CourtListenerClient (PHP)

The main entry point for the PHP SDK.

```php
use CourtListener\CourtListenerClient;

$client = new CourtListenerClient(['api_token' => 'your_token']);
```

#### Arguments
- `api_token` (string): Your API token
- `base_url` (string, optional): Override the API base URL
- `timeout`, `max_retries`, etc.: Advanced options

#### Attributes
All API modules are available as client properties:

**Core Endpoints:**
- `courts`, `dockets`, `opinions`, `clusters`, `judges`, `positions`, `audio`, `search`

**Financial & Disclosure Endpoints:**
- `financial`, `financialDisclosures`, `investments`, `nonInvestmentIncomes`, `gifts`, `reimbursements`, `debts`, `spouseIncomes`, `agreements`

**Case & Legal Endpoints:**
- `docketEntries`, `parties`, `attorneys`, `documents`, `recapDocuments`, `citations`, `opinionsCited`

**People & Education Endpoints:**
- `people`, `schools`, `educations`, `abaRatings`, `politicalAffiliations`

**Alert & Notification Endpoints:**
- `alerts`, `docketAlerts`

**Administrative Endpoints:**
- `sources`, `retentionEvents`, `tag`, `recapFetch`, `recapQuery`, `originatingCourtInformation`, `fjcIntegratedDatabase`, `disclosurePositions`

### API Modules (PHP)

Each module provides methods for a specific resource:

#### Core Modules
- `Courts`: `listCourts()`, `getCourt()`, `searchCourts()`
- `Dockets`: `listDockets()`, `getDocket()`, `searchDockets()`
- `Opinions`: `listOpinions()`, `getOpinion()`, `searchOpinions()`
- `Clusters`: `listClusters()`, `getCluster()`, `searchClusters()`
- `Judges`: `listJudges()`, `getJudge()`, `searchJudges()`
- `Positions`: `listPositions()`, `getPosition()`, `searchPositions()`
- `Audio`: `listAudio()`, `getAudio()`, `searchAudio()`
- `Search`: `search()`, `searchOpinions()`, `searchDockets()`, etc.

#### Financial & Disclosure Modules
- `Financial`: `listFinancial()`, `getFinancial()`, `searchFinancial()`
- `FinancialDisclosures`: `listFinancialDisclosures()`, `getFinancialDisclosure()`, `searchFinancialDisclosures()`
- `Investments`: `listInvestments()`, `getInvestment()`, `searchInvestments()`
- `NonInvestmentIncomes`: `listNonInvestmentIncomes()`, `getNonInvestmentIncome()`, `searchNonInvestmentIncomes()`
- `Gifts`: `listGifts()`, `getGift()`, `searchGifts()`
- `Reimbursements`: `listReimbursements()`, `getReimbursement()`, `searchReimbursements()`
- `Debts`: `listDebts()`, `getDebt()`, `searchDebts()`
- `SpouseIncomes`: `listSpouseIncomes()`, `getSpouseIncome()`, `searchSpouseIncomes()`
- `Agreements`: `listAgreements()`, `getAgreement()`, `searchAgreements()`

#### Case & Legal Modules
- `DocketEntries`: `listDocketEntries()`, `getDocketEntry()`, `searchDocketEntries()`
- `Parties`: `listParties()`, `getParty()`, `searchParties()`
- `Attorneys`: `listAttorneys()`, `getAttorney()`, `searchAttorneys()`
- `Documents`: `listDocuments()`, `getDocument()`, `searchDocuments()`
- `RecapDocuments`: `listRecapDocuments()`, `getRecapDocument()`, `searchRecapDocuments()`
- `Citations`: `listCitations()`, `getCitation()`, `searchCitations()`
- `OpinionsCited`: `listOpinionsCited()`, `getOpinionCited()`, `searchOpinionsCited()`

#### People & Education Modules
- `People`: `listPeople()`, `getPerson()`, `searchPeople()`
- `Schools`: `listSchools()`, `getSchool()`, `searchSchools()`
- `Educations`: `listEducations()`, `getEducation()`, `searchEducations()`
- `AbaRatings`: `listAbaRatings()`, `getAbaRating()`, `searchAbaRatings()`
- `PoliticalAffiliations`: `listPoliticalAffiliations()`, `getPoliticalAffiliation()`, `searchPoliticalAffiliations()`

#### Alert & Notification Modules
- `Alerts`: `listAlerts()`, `getAlert()`, `searchAlerts()`, `createAlert()`, `updateAlert()`, `deleteAlert()`
- `DocketAlerts`: `listDocketAlerts()`, `getDocketAlert()`, `searchDocketAlerts()`, `createDocketAlert()`, `updateDocketAlert()`, `deleteDocketAlert()`

#### Administrative Modules
- `Sources`: `listSources()`, `getSource()`, `searchSources()`
- `RetentionEvents`: `listRetentionEvents()`, `getRetentionEvent()`, `searchRetentionEvents()`
- `Tag`: `listTags()`, `getTag()`, `searchTags()`
- `RecapFetch`: `listRecapFetches()`, `getRecapFetch()`, `searchRecapFetches()`
- `RecapQuery`: `listRecapQueries()`, `getRecapQuery()`, `searchRecapQueries()`
- `OriginatingCourtInformation`: `listOriginatingCourtInformation()`, `getOriginatingCourtInformation()`, `searchOriginatingCourtInformation()`
- `FjcIntegratedDatabase`: `listFjcIntegratedDatabase()`, `getFjcIntegratedDatabase()`, `searchFjcIntegratedDatabase()`
- `DisclosurePositions`: `listDisclosurePositions()`, `getDisclosurePosition()`, `searchDisclosurePositions()`

### Data Models (PHP)

PHP models provide type safety and convenience methods:

#### Core Models
- `Court`: Court information and hierarchy
- `Docket`: Docket records and case information
- `Opinion`: Judicial opinions and decisions
- `Cluster`: Opinion clusters and related cases
- `Judge`: Judicial biographical data
- `Position`: Judicial positions and appointments
- `Audio`: Oral argument audio recordings

#### Financial & Disclosure Models
- `Financial`: Financial disclosure records
- `FinancialDisclosure`: Detailed financial disclosures
- `Investment`: Investment holdings
- `NonInvestmentIncome`: Non-investment income sources
- `Gift`: Gift disclosures
- `Reimbursement`: Reimbursement records
- `Debt`: Debt disclosures
- `SpouseIncome`: Spouse income information
- `Agreement`: Financial agreements

#### Case & Legal Models
- `DocketEntry`: Individual docket entries
- `Party`: Case participants and parties
- `Attorney`: Legal representation
- `Document`: RECAP document management
- `RecapDocument`: RECAP document access
- `Citation`: Citation graph and verification
- `OpinionCited`: Opinion citation relationships

#### People & Education Models
- `Person`: People and biographical data
- `School`: Educational institutions
- `Education`: Educational background
- `AbaRating`: ABA judicial ratings
- `PoliticalAffiliation`: Political affiliations

#### Alert & Notification Models
- `Alert`: Search alerts and notifications
- `DocketAlert`: Docket-specific alerts

#### Administrative Models
- `Source`: Data sources
- `RetentionEvent`: Data retention events
- `Tag`: Tagging system
- `RecapFetch`: RECAP fetch operations
- `RecapQuery`: RECAP query operations
- `OriginatingCourtInformation`: Court origin data
- `FjcIntegratedDatabase`: FJC database integration
- `DisclosurePosition`: Disclosure position data

#### Example: Using Models (PHP)
```php
use CourtListener\Models\Docket;
use CourtListener\Models\Opinion;
use CourtListener\Models\FinancialDisclosure;

// API returns arrays
$docketData = $client->dockets->getDocket(12345);
echo $docketData['case_name'];

// Convert to model for type safety
$docket = new Docket($docketData);
echo $docket['case_name'] . ' ' . $docket['docket_number'];
```

### Error Classes (PHP)

- `CourtListenerException`: Base error
- `AuthenticationException`: Invalid/missing token
- `NotFoundException`: Resource not found
- `RateLimitException`: Too many requests
- `ServerException`: Other API errors

## See Also
- [User Guide](./user_guide.md)
- [Advanced Usage](./advanced_usage.md)
- [Troubleshooting](./troubleshooting.md) 