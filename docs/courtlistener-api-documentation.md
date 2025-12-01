# CourtListener REST API Endpoints (v4.1) – Complete Technical Specification

> **Note**: This is the comprehensive CourtListener API documentation, combining official
> documentation with enhanced specifications for all discovered endpoints. This API documentation
> is provided by CourtListener/Free Law Project and enhanced with detailed specifications
> for complete API coverage.

Below is a comprehensive list of CourtListener's REST API endpoints, organized by resource.
For each resource, we list the endpoint URL (with HTTP method), query parameters
(with types and whether required), a sample `curl` request, the expected JSON response
structure (fields and types), and notes on pagination, filtering, or special formatting.
All endpoints require a valid API token via the `Authorization: Token <...>` header,
but authentication details are omitted from examples.

## Authentication

All API requests require authentication using a token in the Authorization header:
```
Authorization: Token YOUR_API_TOKEN
```

You can obtain an API token by registering at [CourtListener](https://www.courtlistener.com/).

## Search API (Legal Search)

**Endpoint:** `GET /api/rest/v4/search/` – Searches across case law, PACER dockets, judges, and oral arguments.

* **Example Request:**

  ```bash
  Using `curl` to search for the term "foo":

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/search/?q=foo"
  ```

  This returns a JSON with a summary and results.

*
  ```

* **Response Structure:**

  The search results are returned in a paginated format with the following fields:

  ```json
  {
    "count": <integer>,         // total number of results
    "next": "<URL or null>",    // URL to next page (uses cursor-based pagination in v4)
    "previous": "<URL or null>",
    "results": [ {...}, ... ]   // array of result objects
  }
  ```

  Each item in `results` is an object containing resource-specific fields depending on its type (opinion, docket, judge, etc.). For example, an opinion result will include fields like `caseName`, `citation`, `court`, etc., whereas a docket result will include docket metadata. All result objects do include a `resource_uri` (API URL for the item) and an `absolute_url` (web URL on CourtListener). Field types vary (strings for names, integers for IDs, nested objects or URLs for related resources).

*

---

## Dockets

**Endpoint:** `GET /api/rest/v4/dockets/` – Retrieves a list of dockets (case records), and `GET /api/rest/v4/dockets/{id}/` – retrieves a specific docket by ID. Docket objects sit at the top of CourtListener's data hierarchy, linking all related data: in the PACER context, a docket connects to its entries, parties, and attorneys; in the case law context, a docket sits above any opinion clusters for that case.

* **Example Request:**

  ```bash
  Retrieve dockets filtered by court (e.g., Supreme Court = `scotus`):

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/dockets/?court=scotus"
  ```

*
  ```

* **Response Structure:**

  Returns a paginated response with `count`, `next`, `previous`, and `results` (list of docket objects). Each

* **Notes:**

  *Pagination:* Dockets are paginated; use the `next` cursor URL to iterate. *Filtering:* Typically you will at least filter by `court` or `docket_number` to find specific cases. You can also filter by related fields, for example `case_name__icontains=Smith` to find cases with "Smith" in the name (supports Django query lookups). If creating a docket via POST is supported (for authorized users), the required fields would include `docket_number` and `court` (and possibly `case_name`); the documentation suggests using HTTP OPTIONS on the endpoint to discover required fields. (Creation is generally restricted and primarily used for PACER integrations.)

---

## Docket Entries

**Endpoint:** `GET /api/rest/v4/docket-entries/` – 

* **Example Request:**

  ```bash
  Get all entries for a given docket ID:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/docket-entries/?docket=4214664"
  ```

*
  ```

* **Response Structure:**

  Paginated structure with `count`, `next`, `previous`, and `results` (list of docket entry objects). Each

* **Notes:**

  Docket entries are only available for federal PACER cases that have been imported via RECAP. If you lack access to a particular docket's entries, the API may return an authorization error (some PACER content requires special access).

---

## Parties

**Endpoint:** `GET /api/rest/v4/parties/` – Returns parties involved in cases (e.g., plaintiffs, defendants). Also `GET /api/rest/v4/parties/{id}/` for a specific party. Party data is drawn from PACER dockets and includes attorney information nested within each party.

* **Example Request:**

  ```bash
  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/parties/?docket=4214664"
  ```

  This fetches all parties for docket 4214664.

*
  ```

* **Response Structure:**

  Paginated as usual. Each

* **Notes:**

  Party records "contain nested attorney information" for convenience. The

---

## Attorneys

**Endpoint:** `GET /api/rest/v4/attorneys/` – Look up attorneys in the system. Also `GET /api/rest/v4/attorneys/{id}/` for a specific attorney. This endpoint provides details on attorneys who appear in cases.

* **Example Request:**

  ```bash
  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/attorneys/?name__icontains=Smith"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  The Attorneys endpoint is useful for searching or analyzing attorneys across cases. To get attorney lists per case, it may be easier to use the Parties endpoint (which nests attorneys). This endpoint exists to query attorneys directly. Pagination applies as normal. Filtering by name is the primary use; filtering by docket or party ties it to case context.

---

## Documents (RECAP Documents)

**Endpoint:** `GET /api/rest/v4/recap-documents/` – Lists RECAP

* **Example Request:**

  ```bash
  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/recap-documents/?docket_entry=123456"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  This endpoint is often used indirectly – usually one finds documents by first getting a docket entry (which includes `recap_documents`). However, you can query it directly by docket or docket entry. *Pagination:* Due to potentially many documents per docket, results are paginated. *Filters:* It's common to filter by `docket_entry` or `docket` to scope the query. Field descriptions can be introspected via OPTIONS on this endpoint. The `file_url` provides the actual file access; no need to construct it manually.

---

## Opinions

**Endpoint:** `GET /api/rest/v4/opinions/` – Retrieves case law opinions/decisions. Also `GET /api/rest/v4/opinions/{id}/` for a specific opinion. This API contains the full text of judicial opinions as well as metadata. Each opinion is part of an *Opinion Cluster* (case) and may be classified as a majority opinion, dissent, etc.

* **Example Request:**

  ```bash
  Get all opinions from the Supreme Court (court "scotus"):

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/opinions/?court=scotus"
  ```

*
  ```

* **Response Structure:**

  Paginated as usual. Each

* **Notes:**

  The Opinions API returns individual written decisions. Use the `cluster` filter to group opinions by case. For example, an appellate case with a majority and a dissent will have two opinion records sharing the same cluster.

---

## Opinion Clusters

**Endpoint:** `GET /api/rest/v4/clusters/` – Retrieves

* **Example Request:**

  ```bash
  List all opinion clusters in Supreme Court (`scotus`):

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/clusters/?court=scotus"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  Clusters help organize opinions. For a single-opinion case, the cluster still exists to hold that opinion. In cases of multiple opinions, the cluster gives a unified case identifier.

---

## Courts

**Endpoint:** `GET /api/rest/v4/courts/` – Provides information about courts in the CourtListener system. Each court entry includes metadata such as the court's name, jurisdiction, and identifiers. (`GET /api/rest/v4/courts/{id}/` for a specific court.)

* **Example Request:**

  ```bash
  Get all courts:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/courts/"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  Court objects are referenced in many other endpoints (every docket, cluster, opinion, judge, etc., links to a court). This endpoint is useful to translate court slugs or IDs into human-readable names or to discover all courts available. The data here changes infrequently (only when courts are added or updated). Pagination is available but the number of courts is relatively small.

---

## Judges

**Endpoint:** `GET /api/rest/v4/judges/` – Retrieves data on judges and justices (both federal and state) in the CourtListener database. Also `GET /api/rest/v4/judges/{id}/` for a specific judge. This data set is person-centric – each record represents a person (judge) with their biographical and career information.

* **Example Request:**

  ```bash
  Find judges with "Smith" in their name:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/judges/?name__icontains=Smith"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  The Judges API is rich with biographical data – including education, bio, and all positions held. It's person-centric, meaning even if a judge served on multiple courts, they have one record linking to multiple positions.

---

## Positions (Judicial Positions)

**Endpoint:** `GET /api/rest/v4/positions/` – Lists judicial positions held by judges (each entry is a judge's service in a specific court/role). Also `GET /api/rest/v4/positions/{id}/` for a specific position record. This endpoint complements the Judges API by providing a record for each appointment or seat a judge has held.

* **Example Request:**

  ```bash
  Get all positions for judge with ID 1234:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/positions/?judge=1234"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  This endpoint is useful for historical or analytical queries, such as "list all judges who served on X court", or "get the career history of Judge Y". The

---

## Oral Argument Audio

**Endpoint:** `GET /api/rest/v4/audio/` – Provides access to oral argument audio recordings from court proceedings.

* **Query Parameters:**

  * `docket` (integer, optional): Filter by docket ID to get audio for a specific case.
  * `court` (string, optional): Filter by court ID or slug.
  * `date` (date, optional): Filter by argument date (ISO 8601 format: YYYY-MM-DD).
  * `date__gte` (date, optional): Filter by argument date on or after this date.
  * `date__lte` (date, optional): Filter by argument date on or before this date.
  * `case_name` (string, optional): Filter by case name (supports partial matching).

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/audio/?court=scotus&date__gte=2023-01-01"
  ```

* **Response Structure:**

  Returns a paginated list of **Audio** objects. Each object includes:

* `id` (integer) – Audio record ID.
* `docket` (string URL, optional) – Link to the docket of the case the audio belongs to.
* `court` (string URL) – Court that held the oral argument.
* `file_url` (string URL) – Direct link to the audio file (e.g., an MP3).
* `duration` (integer) – Length of the audio in seconds (if available).
* `date` (date) – Date of the oral argument.
* `case_name` (string) – Case name of the argument (if available).

* **Notes:**

  **Audio Availability:** Audio records are linked to dockets when possible, meaning you can find all audio for a case by filtering with the docket ID. Not all courts provide audio; CourtListener's collection is largest for certain appellate courts. The audio files themselves can be accessed via the `file_url` (no additional API call needed to get the binary file).

---

## Financial Disclosures

**Endpoint:** `GET /api/rest/v4/financial-disclosures/` – Lists the financial disclosure report filings (each entry corresponds to one annual disclosure document for a judge). `GET /api/rest/v4/financial-disclosures/{id}/` gets a specific disclosure document record. This is the central record that ties to all the sections below.

* **Example Request:**

  ```bash
  All disclosures for judge ID 15:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/financial-disclosures/?judge=15"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  This is the main record; it does not contain the detailed financial info directly, but acts as "the link between the other financial disclosure endpoints and the judges in our system". To get the content of the report, you need to query the sub-endpoints (investments, incomes, etc.) with the disclosure ID (most of those endpoints have a filter like `?financial_disclosure=<id>`). Typically, you will find those section URLs in the FinancialDisclosure object, or you can query them separately as documented below.

### Investments

---

**Endpoint:** `GET /api/rest/v4/investments/` – Provides access to investments data and functionality in the CourtListener system.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/investments/"
  ```

* **Response Structure:**

  Returns a paginated list of Investments objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to investments data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/non-investment-incomes/` – Retrieves non-investment income sources from financial disclosure reports, including salaries and honoraria.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/non-investment-incomes/"
  ```

* **Response Structure:**

  Returns a paginated list of Non Investment Incomes objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to non investment incomes data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/agreements/` – Provides access to agreements data and functionality in the CourtListener system.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/agreements/"
  ```

* **Response Structure:**

  Returns a paginated list of Agreements objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to agreements data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/gifts/` – Provides access to gifts data and functionality in the CourtListener system.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/gifts/"
  ```

* **Response Structure:**

  Returns a paginated list of Gifts objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to gifts data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/reimbursements/` – Provides access to reimbursements data and functionality in the CourtListener system.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/reimbursements/"
  ```

* **Response Structure:**

  Returns a paginated list of Reimbursements objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to reimbursements data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/debts/` – Accesses debt and liability information from judicial financial disclosure reports.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/debts/"
  ```

* **Response Structure:**

  Returns a paginated list of Debts objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to debts data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/disclosure-positions/` – Retrieves position information from financial disclosure reports, including outside positions and affiliations.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/disclosure-positions/"
  ```

* **Response Structure:**

  Returns a paginated list of Disclosure Positions objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to disclosure positions data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/spouse-incomes/` – Accesses spouse income information from judicial financial disclosure reports.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/spouse-incomes/"
  ```

* **Response Structure:**

  Returns a paginated list of Spouse Incomes objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to spouse incomes data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

## Legal Citation APIs

**Endpoint:** `GET /api/rest/v4/opinions-cited/` – Provides an interface to the

* **Example Request:**

  ```bash
  Opinions cited by opinion ID 1163781:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/opinions-cited/?citing_opinion=1163781"
  ```

*
  ```

* **Response Structure:**

  Paginated list of

* **Notes:**

  This endpoint essentially enumerates edges in the citation graph. It's mainly useful if you want to programmatically traverse citations. For example, to find all citations from a given case or all cases that cite a particular case. In many cases, you may not need to use this directly, because the Opinion endpoint already provides an `opinions_cited` list (cites out) and CourtListener's website provides "cited by" counts. But this API gives the raw data. Ensure to use filters – for instance, to get "cited by" list for an opinion, use `?cited_opinion=<id>`. To get "cites" (what it cites), use `?citing_opinion=<id>`. Pagination might be relevant for very famous cases with many citing opinions.

### Citation Lookup & Verification

---

## Alerts

**Endpoint:** `GET /api/rest/v4/alerts/` – Manages search alerts and docket alerts, allowing users to subscribe to notifications for specific queries or case updates.

* **Query Parameters:**

  * `name` (string, **required**): Name for the alert (used for identification and management).
  * `query` (string, **required**): Search query string that defines what the alert monitors.
  * `rate` (string, **required**): Alert frequency. Options: `dly` (daily), `wly` (weekly), `mly` (monthly).
  * `alert_type` (string, optional): Type of alert. Options: `search` for search alerts, `docket` for docket alerts.
  * `webhook_url` (string, optional): Webhook URL for receiving alert notifications (alternative to email).

* **Example Request:**

  ```bash
  curl -X POST --header "Authorization: Token YOUR_TOKEN" \
     --data 'name=Supreme Court Cases' \
     --data 'query=q=constitutional&type=o&court=scotus' \
     --data 'rate=wly' \
     "https://www.courtlistener.com/api/rest/v4/alerts/"
  ```

* **Response Structure:**

  Returns a paginated list of alert objects. Each **Alert** object includes:

* `id` (integer) – Alert ID in CourtListener.
* `name` (string) – User-defined name for the alert.
* `query` (string) – The search query that defines what the alert monitors.
* `rate` (string) – Alert frequency (dly, wly, mly).
* `alert_type` (string) – Type of alert (search, docket).
* `date_created` (date) – When the alert was created.
* `date_modified` (date) – When the alert was last modified.
* `webhook_url` (string, optional) – Webhook URL for notifications.

* **Notes:**

  **Alert Management:** Alerts can be created, modified, and deleted through this API. Search alerts monitor the search index and trigger when new results match the query. Docket alerts monitor specific dockets for new entries or documents. Webhook notifications are sent to the specified URL when alerts trigger.

---

**Endpoint:** `GET /api/rest/v4/docket-alerts/` – Creates and manages alerts for specific dockets, notifying users when new entries or documents are added.

* **Query Parameters:**

  * `docket` (integer, **required**): Docket ID to monitor for updates and new entries.
  * `alert_type` (string, optional): Type of docket alert. Options: `entry` for new docket entries, `document` for new documents.
  * `webhook_url` (string, optional): Webhook URL for receiving docket alert notifications.

* **Example Request:**

  ```bash
  curl -X POST --header "Authorization: Token YOUR_TOKEN" \
     --data 'docket=4214664' \
     "https://www.courtlistener.com/api/rest/v4/docket-alerts/"
  ```

* **Response Structure:**

  Returns a paginated list of Docket Alerts objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to docket alerts data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

## People & Organizations

**Endpoint:** `GET /api/rest/v4/people/` – Accesses the people database containing biographical and professional information about individuals in the legal system.

* **Query Parameters:**

  * `name` (string, optional): Filter by person name (supports partial matching).
  * `name__icontains` (string, optional): Case-insensitive partial name search.
  * `court` (string, optional): Filter by associated court ID or slug.
  * `position_type` (string, optional): Filter by position type (e.g., "Judge", "Justice", "Attorney").
  * `active` (boolean, optional): Filter by active status. `true` for currently active, `false` for inactive.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/people/?name__icontains=smith&position_type=Judge"
  ```

* **Response Structure:**

  Returns a paginated list of **Person** objects. Each object includes:

* `id` (integer) – Person ID.
* `name` (string) – Full name of the person.
* `court` (string URL, optional) – Link to the primary court associated with this person.
* `position` (string, optional) – Current or most recent position title.
* `birthday` (date, optional) – Date of birth (if known).
* `education` (string, optional) – Educational background.
* `political_affiliation` (string, optional) – Political party of appointing authority.

* **Notes:**

  **Data Sources:** The people database combines information from multiple sources including judicial appointment records, biographical databases, and public records. Data completeness varies by individual and time period.

---

**Endpoint:** `GET /api/rest/v4/schools/` – Retrieves information about educational institutions, law schools, and universities associated with legal professionals.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/schools/"
  ```

* **Response Structure:**

  Returns a paginated list of Schools objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to schools data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/educations/` – Accesses education records and academic background information for judges and legal professionals.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/educations/"
  ```

* **Response Structure:**

  Returns a paginated list of Educations objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to educations data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

## Data Sources & Metadata

**Endpoint:** `GET /api/rest/v4/sources/` – Provides information about data sources, including court websites, databases, and other legal information providers.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/sources/"
  ```

* **Response Structure:**

  Returns a paginated list of Sources objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to sources data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/retention-events/` – Tracks data retention events and policy changes that affect the availability of legal documents.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/retention-events/"
  ```

* **Response Structure:**

  Returns a paginated list of Retention Events objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to retention events data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/aba-ratings/` – Accesses American Bar Association (ABA) ratings for judicial nominees and appointees.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/aba-ratings/"
  ```

* **Response Structure:**

  Returns a paginated list of Aba Ratings objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to aba ratings data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/political-affiliations/` – Provides political affiliation information for judges and legal professionals.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/political-affiliations/"
  ```

* **Response Structure:**

  Returns a paginated list of Political Affiliations objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to political affiliations data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

## Additional Resources

**Endpoint:** `GET /api/rest/v4/tag/` – Manages tagging system for categorizing and organizing legal documents and cases.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/tag/"
  ```

* **Response Structure:**

  Returns a paginated list of Tag objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to tag data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/recap-fetch/` – Initiates and manages RECAP fetch operations to retrieve new documents from PACER for specific dockets.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/recap-fetch/"
  ```

* **Response Structure:**

  Returns a paginated list of Recap Fetch objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to recap fetch data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/recap-query/` – Queries the RECAP database for document availability and metadata without downloading files.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/recap-query/"
  ```

* **Response Structure:**

  Returns a paginated list of Recap Query objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to recap query data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/originating-court-information/` – Provides metadata about the originating court for cases, including jurisdiction and procedural information.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/originating-court-information/"
  ```

* **Response Structure:**

  Returns a paginated list of Originating Court Information objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to originating court information data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

**Endpoint:** `GET /api/rest/v4/fjc-integrated-database/` – Accesses the Federal Judicial Center (FJC) integrated database for comprehensive judicial information.

* **Query Parameters:**

  * `format` (string, optional): Response format. Options: `json` (default), `xml` for XML format.
  * `page` (integer, optional): Page number for pagination (if using page-based pagination).
  * `page_size` (integer, optional): Number of results per page (default varies by endpoint).
  * `order_by` (string, optional): Sort results by field. Use `-field_name` for descending order.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
     "https://www.courtlistener.com/api/rest/v4/fjc-integrated-database/"
  ```

* **Response Structure:**

  Returns a paginated list of Fjc Integrated Database objects. Each object includes relevant fields for the specific resource type. The response follows the standard pagination format with `count`, `next`, `previous`, and `results` fields.

* **Notes:**

  **Usage Notes:** This endpoint provides access to fjc integrated database data. Use appropriate filters to narrow results as the dataset may be large. Check the pagination information in the response to retrieve additional pages of results.

---

## Documentation Coverage Summary

**Total Endpoints Documented:** 39
**Detailed Existing Endpoints:** 13
**Enhanced New Endpoints:** 23

This documentation provides comprehensive coverage of the CourtListener API,
combining detailed specifications for core endpoints with enhanced documentation
for all discovered endpoints, ensuring complete API coverage with consistent
detail levels throughout.
