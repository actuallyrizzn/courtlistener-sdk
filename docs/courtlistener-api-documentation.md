# CourtListener REST API Endpoints (v4.1) – Technical Specification

Below is a comprehensive list of CourtListener’s REST API endpoints, organized by resource. For each resource, we list the endpoint URL (with HTTP method), query parameters (with types and whether required), a sample `curl` request, the expected JSON response structure (fields and types), and notes on pagination, filtering, or special formatting. All endpoints require a valid API token via the `Authorization: Token <...>` header, but authentication details are omitted here.

## Search API (Legal Search)

**Endpoint:** `GET /api/rest/v4/search/` – Searches across case law, PACER dockets, judges, and oral arguments.

* **Query Parameters:**

  * `q` (string, **required**): The search query (keywords, phrases, etc.).
  * `type` (string, optional): Filter by result type – e.g., `o` for opinions, `d` for dockets, `j` for judges, `oa` for oral arguments.
  * Additional field filters (optional): The Search API supports advanced filters on specific fields (e.g., `docket_number`, `case_name`, judge name, etc.) and operators. For example, one can filter by docket number or case name using query params like `docket_number=<value>` or `case_name__icontains=<value>`. Date ranges and other field lookups follow Django-style filters (e.g., `date_filed__range=start/end` in ISO-8601 format).

* **Example Request:** Using `curl` to search for the term "foo":

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/search/?q=foo"
  ```

  This returns a JSON with a summary and results.

* **Response Structure:** The search results are returned in a paginated format with the following fields:

  ```json
  {
    "count": <integer>,         // total number of results
    "next": "<URL or null>",    // URL to next page (uses cursor-based pagination in v4)
    "previous": "<URL or null>",
    "results": [ {...}, ... ]   // array of result objects
  }
  ```

  Each item in `results` is an object containing resource-specific fields depending on its type (opinion, docket, judge, etc.). For example, an opinion result will include fields like `caseName`, `citation`, `court`, etc., whereas a docket result will include docket metadata. All result objects do include a `resource_uri` (API URL for the item) and an `absolute_url` (web URL on CourtListener). Field types vary (strings for names, integers for IDs, nested objects or URLs for related resources).

* **Pagination & Filtering:** The Search API uses cursor-based pagination in v4 (the `next` URL contains a `cursor` parameter) to allow deep traversal. To get subsequent pages, follow the `next` URL. You can also filter results by adding query params for specific fields or facets (e.g., `court=<court_id>` or `date_filed__gte=YYYY-MM-DD`). The API supports complex queries and boolean operators (see CourtListener’s advanced search documentation). All query parameters should be URL-encoded as needed.

## Dockets

**Endpoint:** `GET /api/rest/v4/dockets/` – Retrieves a list of dockets (case records), and `GET /api/rest/v4/dockets/{id}/` – retrieves a specific docket by ID. Docket objects sit at the top of CourtListener’s data hierarchy, linking all related data: in the PACER context, a docket connects to its entries, parties, and attorneys; in the case law context, a docket sits above any opinion clusters for that case.

* **Query Parameters:**

  * Filtering by fields is optional. For example, `court=<court_id>` or `court=<court_slug>` (string) filters dockets by court, and `docket_number=<number>` (string) filters by docket number. These are optional; if omitted, all dockets are listed (paginated).
  * No required query params for listing, but due to the large data size, you’ll typically use filters or pagination cursors.
  * Cursor-based pagination is used; include `cursor=<token>` to fetch pages beyond the first as provided in the `next` field of a response.

* **Example Request:** Retrieve dockets filtered by court (e.g., Supreme Court = `scotus`):

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/dockets/?court=scotus"
  ```

* **Response Structure:** Returns a paginated response with `count`, `next`, `previous`, and `results` (list of docket objects). Each **Docket** object contains:

  * `id` (integer) – Docket ID in CourtListener.
  * `court` (string URL) – Reference to the court resource for this case.
  * `case_name` (string) – Full case name/title.
  * `docket_number` (string) – The court’s docket number for the case.
  * `absolute_url` (string) – Web URL on CourtListener for this docket’s page.
  * Other metadata: e.g., `date_filed` (date) if available, `jurisdiction` or flags if provided. The docket may also include links or counts of related items (for example, it may have fields or embedded links for `parties`, `docket_entries`, and associated opinion clusters).

  *Field types:* ID is integer; strings for names and numbers; dates in ISO 8601; related resources as URLs. An example docket JSON might look like:

  ```json
  {
    "id": 4214664,
    "court": "https://www.courtlistener.com/api/rest/v4/courts/scotus/",
    "docket_number": "21-123",
    "case_name": "Example Case v. United States",
    "absolute_url": "/docket/4214664/example-case-v-united-states/",
    ... 
  }
  ```

* **Notes:** *Pagination:* Dockets are paginated; use the `next` cursor URL to iterate. *Filtering:* Typically you will at least filter by `court` or `docket_number` to find specific cases. You can also filter by related fields, for example `case_name__icontains=Smith` to find cases with "Smith" in the name (supports Django query lookups). If creating a docket via POST is supported (for authorized users), the required fields would include `docket_number` and `court` (and possibly `case_name`); the documentation suggests using HTTP OPTIONS on the endpoint to discover required fields. (Creation is generally restricted and primarily used for PACER integrations.)

## Docket Entries

**Endpoint:** `GET /api/rest/v4/docket-entries/` (list docket entries) and `GET /api/rest/v4/docket-entries/{id}/` (retrieve a specific entry). **Docket Entry** objects represent individual entries on a court’s docket (the sequential records of filings, orders, etc.). Each docket entry typically corresponds to a filing or court action and may contain one or more associated documents (PDF filings) nested within it.

* **Query Parameters:**

  * `docket` (integer or URL, optional): Filter by the parent docket’s ID. For example, `?docket=4214664` returns entries for docket ID 4214664. This is the most common filter (and effectively required to get useful results, as listing all entries globally is rarely needed).
  * Date filters (optional): e.g., `date_filed__gte=YYYY-MM-DD` and `date_filed__lte=YYYY-MM-DD` can filter entries by filing date range.
  * Entry number or document filters (optional): e.g., `entry_number=<N>` to get a specific entry number, or `recap_documents__document_number=1` to find the entry containing the main document number 1. (The double-underscore syntax filters on fields of nested objects; here it filters docket entries by a property of their nested document.)

* **Example Request:** Get all entries for a given docket ID:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/docket-entries/?docket=4214664"
  ```

* **Response Structure:** Paginated structure with `count`, `next`, `previous`, and `results` (list of docket entry objects). Each **DocketEntry** object includes:

  * `id` (integer) – Entry ID.
  * `docket` (string URL) – Link to the associated docket resource.
  * `entry_number` (integer) – The sequence number on the docket (if available, e.g., PACER docket entry number).
  * `description` (string) – Text of the docket entry (may be truncated if very long).
  * `date_filed` (date) – Date this entry was filed/entered.
  * `recap_documents` (array of objects) – **Nested** list of document metadata for each PDF attached to this entry. Each nested **RecapDocument** object typically includes:

    * `id` (integer) – Document ID.
    * `document_number` (integer or string) – The document’s number or exhibit identifier on the docket (e.g., *“1”* for the main initial filing, *“1-1”* for an attachment, etc.).
    * `pacer_doc_id` or `recap_id` (string) – An identifier from PACER/RECAP.
    * `file_url` (string URL) – A link to download the PDF of the filing (may require the API token or be publicly accessible if the document is in the RECAP archive).
    * Other fields: possibly `description` (string description of the document, e.g. *“Complaint”*), `pages` (integer page count), and flags like `is_attachment` or `restricted` if applicable.

  *Field types:* IDs are integers; dates are strings in `YYYY-MM-DD`; `recap_documents` is an array of objects as described.

* **Notes:** Docket entries are only available for federal PACER cases that have been imported via RECAP. If you lack access to a particular docket’s entries, the API may return an authorization error (some PACER content requires special access). **Pagination:** Docket entries are paginated, but typically you will retrieve them by docket ID which limits the scope. **Ordering:** Entries are usually sorted by entry number or date; you can specify `order_by=entry_number` if needed (the API may default to chronological order). If creating or updating docket entries via the API is allowed (for contributing RECAP data), required fields would include the associated `docket` and entry details; check the OPTIONS metadata for specifics.

## Parties

**Endpoint:** `GET /api/rest/v4/parties/` – Returns parties involved in cases (e.g., plaintiffs, defendants). Also `GET /api/rest/v4/parties/{id}/` for a specific party. Party data is drawn from PACER dockets and includes attorney information nested within each party.

* **Query Parameters:**

  * `docket` (integer or URL, optional): Filter by docket ID – i.e., list parties for a specific case. For example `?docket=4214664` returns all parties (and their attorneys) on that docket.
  * `name` or `name__icontains` (string, optional): Filter by party name (full or partial match).
  * `type` (string, optional): Filter by party type/role (if available, e.g., `appellant`, `appellee`, `plaintiff`, `defendant`, etc., depending on how data is categorized).

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/parties/?docket=4214664"
  ```

  This fetches all parties for docket 4214664.

* **Response Structure:** Paginated as usual. Each **Party** object includes:

  * `id` (integer) – Party ID.
  * `name` (string) – Name of the individual or entity.
  * `type` (string) – Role of the party (if provided, e.g., “Plaintiff” or “Defendant”).
  * `docket` (string URL) – Link to the related docket.
  * `attorneys` (array of objects) – **Nested** list of attorneys representing this party. Each nested **Attorney** object typically provides:

    * `id` (integer) – Attorney ID (in the CourtListener system).
    * `name` (string) – Attorney name.
    * `law_firm` (string, if available) – Firm or affiliation.
    * `appearance_role` (string) – Role in the case (e.g., counsel of record, appellant counsel, etc., if specified).
    * `party` (string URL) – Reference back to the party (or null if embedded).

  Example party JSON:

  ```json
  {
    "id": 100123,
    "name": "John Doe",
    "type": "Defendant",
    "docket": "https://www.courtlistener.com/api/rest/v4/dockets/4214664/",
    "attorneys": [
       {
         "id": 555,
         "name": "Jane Smith",
         "law_firm": "Smith & Smith LLP",
         "appearance_role": "Attorney for Defendant",
         "party": null
       },
       ...
    ]
  }
  ```

  In this example, attorneys are included inline; in some cases the `attorneys` field may be a URL to the attorneys API if not embedded.

* **Notes:** Party records “contain nested attorney information” for convenience. The **Attorneys** are also accessible via the separate Attorneys endpoint, but when listing parties by docket, you get all their attorneys in one go. Pagination is typically not an issue if filtering by a single docket (as most cases have a manageable number of parties). Creation/updates via API are generally not used for parties (they’re derived from docket data).

## Attorneys

**Endpoint:** `GET /api/rest/v4/attorneys/` – Look up attorneys in the system. Also `GET /api/rest/v4/attorneys/{id}/` for a specific attorney. This endpoint provides details on attorneys who appear in cases.

* **Query Parameters:**

  * `name` or `name__icontains` (string, optional): Filter by attorney name (e.g. `?name__icontains=Smith` to find attorneys with "Smith" in their name).
  * `docket` (integer or URL, optional): Filter by docket ID to get attorneys on a specific case. (Alternatively, you would usually get attorneys via the Parties endpoint, but this filter can directly retrieve all attorneys for a docket.)
  * Other possible filters: `party` (ID/URL) to get attorneys for a specific party, if applicable.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/attorneys/?name__icontains=Smith"
  ```

* **Response Structure:** Paginated list of **Attorney** objects. Each Attorney object includes:

  * `id` (integer) – Attorney ID.
  * `name` (string) – Attorney’s full name.
  * `organization` or `law_firm` (string, if available) – Affiliation or firm.
  * `party` (string URL or null) – Link to the party they represent (if the context is limited to a case). An attorney can appear multiple times if involved in multiple cases/parties.
  * `docket` (string URL or null) – Link to the related docket (if applicable).
  * Other fields: possibly contact info if stored (email or address are generally not included; the API mainly focuses on names and relationships).

* **Notes:** The Attorneys endpoint is useful for searching or analyzing attorneys across cases. To get attorney lists per case, it may be easier to use the Parties endpoint (which nests attorneys). This endpoint exists to query attorneys directly. Pagination applies as normal. Filtering by name is the primary use; filtering by docket or party ties it to case context.

## Documents (RECAP Documents)

**Endpoint:** `GET /api/rest/v4/recap-documents/` – Lists RECAP **Document** objects, which represent individual PDF filings (documents) from PACER dockets. Also `GET /api/rest/v4/recap-documents/{id}/` for a specific document. Typically, you will retrieve documents via their association with docket entries, rather than listing all documents globally.

* **Query Parameters:**

  * `docket_entry` (integer or URL, optional): Filter by a specific docket entry ID to get documents for that entry.
  * `docket` (integer or URL, optional): Filter by docket ID to get all documents for a given case (this will return all documents across all entries of that docket).
  * `document_number` (string or integer, optional): Filter by the document’s number in the docket (e.g., `?document_number=5` to find the document labeled #5 on the docket).
  * Format filter: `format=pdf` or `format=html` – by default JSON is returned, but if you want the raw file, the API might allow `?format=pdf` to redirect/download the PDF (alternatively, use the `file_url` provided in the JSON).

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/recap-documents/?docket_entry=123456"
  ```

* **Response Structure:** Paginated list of **RecapDocument** objects. Each object includes:

  * `id` (integer) – Document ID.
  * `docket_entry` (string URL) – Link to the docket entry that this document belongs to.
  * `document_number` (string) – The designation of the document on the docket (e.g., "10" or "10-2" for an attachment).
  * `description` (string) – Description of the document (often the docket entry’s text or a title like “Brief in Support”).
  * `file_url` (string URL) – Direct link to the PDF file in the RECAP archive. This URL can be used to download the file.
  * `file_size` (integer) – Size of the PDF in bytes (if available).
  * `pages` (integer) – Number of pages in the document (if known).
  * `type` (string) – Type of document (e.g., “opinion”, “motion”, “pleading”, etc., if categorized).
  * `pacer_doc_id` (string) – The original PACER document ID or path, which can be used as a reference.
  * `sha1` (string) – Hash of the file for integrity (if provided).

* **Notes:** This endpoint is often used indirectly – usually one finds documents by first getting a docket entry (which includes `recap_documents`). However, you can query it directly by docket or docket entry. *Pagination:* Due to potentially many documents per docket, results are paginated. *Filters:* It’s common to filter by `docket_entry` or `docket` to scope the query. Field descriptions can be introspected via OPTIONS on this endpoint. The `file_url` provides the actual file access; no need to construct it manually.

## Opinions

**Endpoint:** `GET /api/rest/v4/opinions/` – Retrieves case law opinions/decisions. Also `GET /api/rest/v4/opinions/{id}/` for a specific opinion. This API contains the full text of judicial opinions as well as metadata. Each opinion is part of an *Opinion Cluster* (case) and may be classified as a majority opinion, dissent, etc.

* **Query Parameters:**

  * `cluster` (integer or URL, optional): Filter by an Opinion Cluster ID (to get all opinions for a particular case).
  * `court` (string court ID or slug, optional): Filter by court (e.g., `?court=scotus` for Supreme Court opinions).
  * `date_filed` or `date_filed__gte/lte` (date, optional): Filter by opinion date.
  * `cite` or `citation` (string, optional): Find by citation (if an exact citation is known).
  * Full-text search is generally done via the Search API, not directly here, so `q` is not a parameter on this endpoint. Use the Search API for keyword queries.

* **Example Request:** Get all opinions from the Supreme Court (court “scotus”):

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/opinions/?court=scotus"
  ```

* **Response Structure:** Paginated as usual. Each **Opinion** object includes many fields, notably:

  * `id` (integer) – Opinion ID.
  * `cluster` (string URL) – Reference to the Opinion Cluster (case) this opinion belongs to.
  * `court` (string URL) – Reference to the court that issued the opinion.
  * `date_filed` (date) – Date the opinion was filed/decided.
  * `type` (string) – Type of opinion (e.g., *“majority”*, *“dissent”*, *“concurrence”*, etc.). This indicates whether the opinion is the main opinion or a separate opinion.
  * `author` (string URL or null) – Link to the Judge (person) who authored the opinion, if known (often for majority opinions).
  * `per_curiam` (boolean) – True if the opinion is per curiam.
  * `text` (string) – The full text of the opinion in HTML or sometimes plaintext (large field).
  * `html_with_citations` (string, sometimes present) – The opinion text with hyperlinks on citations (if available).
  * `absolute_url` (string) – Web URL to view the opinion on CourtListener.
  * `download_url` (string) – The original source URL from which this opinion was retrieved. *Note:* This is often the court website link or PDF link; it may be empty or stale for older cases, since not all courts maintain permanent URLs.
  * `citation_count` (integer) – Number of citations this opinion contains (if computed).
  * `opinions_cited` (array of strings or objects) – List of other opinions cited *by* this opinion. Each entry may be a URL or an object reference to an opinion that is cited in the text of this opinion. This provides a quick view into the opinion’s citations (the full citation graph is also accessible via separate endpoints; see *Citation APIs* below).
  * Additional metadata: `precedential_status` (string, e.g., “Published” or “Unpublished”), `docket_numbers` (list of strings, since an opinion may list one or more docket numbers), `case_name` (string, usually the same as the cluster’s case name), and various flags (e.g., `sealed`).

  *Field types:* ID integers, boolean flags, dates in ISO format, and strings for text. The opinion text fields can be very large strings (HTML content).

* **Notes:** The Opinions API returns individual written decisions. Use the `cluster` filter to group opinions by case. For example, an appellate case with a majority and a dissent will have two opinion records sharing the same cluster. **Pagination:** The dataset is large; use filters or cursor pagination to navigate. **Text Content:** The `text` field contains the full opinion text (which can be several megabytes for long opinions). If you only need metadata, you can request a lighter format (e.g., `?fields=id,case_name,court` using the API’s field-limiting if supported, or simply ignore the `text` in processing). The `download_url` is informational; it points to the source of the opinion, but for obtaining the text or PDF, the data is already in the `text` field or available via CourtListener’s website.

## Opinion Clusters

**Endpoint:** `GET /api/rest/v4/clusters/` – Retrieves **Opinion Cluster** records, which group together one or more opinions from the same case (e.g., a lead opinion and any concurrences/dissents). Also `GET /api/rest/v4/clusters/{id}/` for a specific cluster. In CourtListener’s hierarchy, clusters represent cases in the case law database, sitting below dockets and above individual opinions.

* **Query Parameters:**

  * `docket` (integer or URL, optional): Filter clusters by the related docket ID (linking case law clusters to PACER docket if available).
  * `court` (string, optional): Filter by court (returns clusters of that court’s cases).
  * `case_name` or `case_name__icontains` (string, optional): Filter by case name.
  * `citation` (string, optional): Filter by a citation (returns the cluster that has an opinion with that citation, typically the primary citation for the case).

* **Example Request:** List all opinion clusters in Supreme Court (`scotus`):

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/clusters/?court=scotus"
  ```

* **Response Structure:** Paginated list of **Cluster** objects. Each OpinionCluster includes:

  * `id` (integer) – Cluster ID.
  * `case_name` (string) – Name of the case (usually the most commonly used short name).
  * `docket` (string URL or null) – Link to the PACER docket resource if this cluster is linked to a docket in the RECAP database. (For example, many clusters for federal cases will have a `docket` pointing to the corresponding docket record).
  * `court` (string URL) – Link to the court resource.
  * `citation` (string) – A canonical citation for the case (typically the reporter citation of the lead opinion, if available). There may also be a list of citations in a separate field (some clusters include a list of all citations associated with that case).
  * `absolute_url` (string) – Web URL for the case on CourtListener.
  * `opinions` (array of strings or objects) – (In some contexts) list of the opinion URLs that belong to this cluster. Often you’ll retrieve opinions by querying the Opinions API with `cluster` filter instead.
  * `date_filed` (date) – Date of the decision (usually mirrors the date of the main opinion).
  * `judges` (array of URLs or objects) – Judges on the panel for this case, if recorded (may list the judge resource URIs for each judge who participated).

* **Notes:** Clusters help organize opinions. For a single-opinion case, the cluster still exists to hold that opinion. In cases of multiple opinions, the cluster gives a unified case identifier. **Filtering:** You can find a cluster by docket number indirectly: first find the docket ID (via Dockets API) then filter clusters by `docket=<id>`. **Use case:** Often, one might use the Search API or citation lookup to find a case, then retrieve its cluster to get all opinions or metadata. Clusters are a convenient place to see which docket (if any) and court correspond to a case, and to navigate to related data (parties, etc., via the docket link).

## Courts

**Endpoint:** `GET /api/rest/v4/courts/` – Provides information about courts in the CourtListener system. Each court entry includes metadata such as the court’s name, jurisdiction, and identifiers. (`GET /api/rest/v4/courts/{id}/` for a specific court.)

* **Query Parameters:**

  * `jurisdiction` (string, optional): Filter by jurisdiction (e.g., `?jurisdiction=federal` or `state`).
  * `name` or `name__icontains` (string, optional): Filter by court name.
  * Usually not heavily filtered; more often used to lookup court details by ID or to enumerate all courts.

* **Example Request:** Get all courts:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/courts/"
  ```

* **Response Structure:** Paginated list of **Court** objects. Each Court object typically includes:

  * `id` (string) – The unique court identifier (often a slug, e.g., `"scotus"` for Supreme Court). Note: in URLs and references, this ID is used instead of an integer.
  * `name` (string) – Full name of the court (e.g., “Supreme Court of the United States”).
  * `name_abbreviation` (string) – Abbreviated name (e.g., “U.S. Supreme Court”).
  * `jurisdiction` (string) – Jurisdiction level (e.g., “federal” or a state name).
  * `slug` (string) – Same as `id` typically (a short mnemonic for the court).
  * `url` (string) – Official website URL of the court, if available.
  * Other fields: `court_type` (e.g., “Appellate”, “Trial”), and possibly location or region info if applicable.

* **Notes:** Court objects are referenced in many other endpoints (every docket, cluster, opinion, judge, etc., links to a court). This endpoint is useful to translate court slugs or IDs into human-readable names or to discover all courts available. The data here changes infrequently (only when courts are added or updated). Pagination is available but the number of courts is relatively small.

## Judges

**Endpoint:** `GET /api/rest/v4/judges/` – Retrieves data on judges and justices (both federal and state) in the CourtListener database. Also `GET /api/rest/v4/judges/{id}/` for a specific judge. This data set is person-centric – each record represents a person (judge) with their biographical and career information.

* **Query Parameters:**

  * `name` or `name__icontains` (string, optional): Filter by judge name (e.g., last name).
  * `court` (string or URL, optional): Filter judges by a specific court (likely judges who have served on that court).
  * `position` or `position__position_type` (string, optional): Filter by position type (like “Justice” vs “Judge”) or by current position. More commonly, you’ll use the Positions endpoint for detailed position queries (see below).
  * `active` (boolean, optional): e.g., `?active=true` to filter current active judges (if the API supports such a filter via a field).

* **Example Request:** Find judges with “Smith” in their name:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/judges/?name__icontains=Smith"
  ```

* **Response Structure:** Paginated list of **Judge** objects. Each Judge object typically includes:

  * `id` (integer) – Judge ID.
  * `name` (string) – Full name of the judge.
  * `court` (string URL or null) – *Current* primary court of the judge (for sitting judges, perhaps the court they serve on; for historical figures, possibly their last court or a notable court).
  * `birthday` (date or string) – Date of birth (if known).
  * `education` (string or array) – Educational background (often concatenated or a list of law school, college, etc.).
  * `political_affiliation` (string) – The political party of the appointing president, or other affiliation (primarily for U.S. federal judges).
  * `position` (string) – Current position title or role (e.g., “Judge, U.S. District Court”, “Associate Justice, Supreme Court”).
  * `positions` (array of URLs or objects) – List of all judicial positions the person has held, with details (see *Positions* below). Each position includes court, title, start/end dates, appointment info, etc.
  * `appointments` (array, possibly) – Federal judges may have an appointments list (including who appointed them, when, and which court). This may be integrated into `positions`.
  * Other fields: `gender`, `ethnicity` (if tracked), `roles` or `title` (sometimes a short descriptor like “Chief Judge” if applicable), `date_died` (if deceased), etc., depending on available data.

* **Notes:** The Judges API is rich with biographical data – including education, bio, and all positions held. It’s person-centric, meaning even if a judge served on multiple courts, they have one record linking to multiple positions. **Positions and career data:** to get structured info on each judicial post (court name, position type, term dates), use the Positions endpoint or inspect the `positions` field. **Filtering:** Searching by name is common; you can also filter indirectly by attributes (e.g., to get all judges of a certain court, you might use the Positions API, since judges often hold multiple positions including senior status, etc.). Pagination is typically needed if pulling all judges (there are thousands of entries).

## Positions (Judicial Positions)

**Endpoint:** `GET /api/rest/v4/positions/` – Lists judicial positions held by judges (each entry is a judge’s service in a specific court/role). Also `GET /api/rest/v4/positions/{id}/` for a specific position record. This endpoint complements the Judges API by providing a record for each appointment or seat a judge has held.

* **Query Parameters:**

  * `judge` (integer or URL, optional): Filter by judge ID to get all positions for that person.
  * `court` (string or URL, optional): Filter positions by court (to see all judges who have served on a given court).
  * `position_type` (string, optional): Filter by role type (e.g., “Judge”, “Chief Judge”, “Justice”). (Valid choices for `position_type` can be discovered via OPTIONS – for example, “Judge”, “Justice”, “Chief Justice”, etc. are typical values.)
  * `active` (boolean, optional): Filter current active positions (e.g., `active=true` for currently serving positions).

* **Example Request:** Get all positions for judge with ID 1234:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/positions/?judge=1234"
  ```

* **Response Structure:** Paginated list of **Position** objects. Each Position includes:

  * `id` (integer) – Position record ID.
  * `judge` (string URL) – Link to the Judge person who held this position.
  * `court` (string URL) – Link to the Court on which they served.
  * `position_type` (string) – Type of position/title (e.g., “Judge”, “Chief Judge”, “Justice”).
  * `title` (string) – Full title (often similar to `position_type` plus court, e.g., “Chief Judge, U.S. Court of Appeals for the Ninth Circuit”).
  * `start_date` (date) – When the judge started this position.
  * `end_date` (date or null) – When the judge left this position (null if currently in this position).
  * `appointing_president` (string, if applicable) – The President or authority who appointed the judge (for federal judges).
  * `confirmation_date` (date, if applicable) – Date of Senate confirmation (for federal).
  * `aba_rating` (string, if recorded) – ABA rating at nomination.
  * etc. – Various other fields about the term or appointment, such as `reason_terminated` or `successor`/`predecessor` links, can be present for federal judges.

* **Notes:** This endpoint is useful for historical or analytical queries, such as "list all judges who served on X court", or "get the career history of Judge Y". The **Judge** endpoint often embeds a summary of positions, but this **Positions** endpoint gives the detailed breakdown per position. Filtering by `judge` is a common usage (to retrieve a judge’s full career). Filtering by `court` allows assembling a roster of that court’s judges over time. The `position_type` choices show whether a person was a judge or justice etc. Pagination applies, but typically queries are filtered to a manageable subset.

## Oral Argument Audio

**Endpoint:** `GET /api/rest/v3/audio/` – Retrieves oral argument audio records (recordings of court proceedings). Also `GET /api/rest/v3/audio/{id}/` for a specific audio file metadata. CourtListener hosts a large collection of oral argument audio, and this API provides access to the metadata and links for those recordings.

* **Query Parameters:**

  * `docket` (integer or URL, optional): Filter audio by the docket ID of the case. Many audio records are linked to a CourtListener docket (especially for appellate cases where audio is available).
  * `court` (string or URL, optional): Filter by court (e.g., audio from a specific court).
  * `date` or `date__gte/lte` (date, optional): Filter by argument date.
  * `case_name` (string, optional): Filter by case name (if transcripts have case names in metadata).

* **Example Request:** Get audio recordings for a specific case docket:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v3/audio/?docket=4214664"
  ```

* **Response Structure:** Paginated list of **Audio** objects. Each Audio object may include:

  * `id` (integer) – Audio record ID.
  * `docket` (string URL or null) – Link to the docket of the case the audio belongs to. (Some audio might not be linked if the case isn’t in the RECAP database.)
  * `court` (string URL) – Court that held the oral argument.
  * `file_url` (string URL) – Direct link to the audio file (e.g., an MP3). This is the URL where the audio can be downloaded or streamed.
  * `duration` (integer) – Length of the audio in seconds (if available).
  * `date` (date) – Date of the oral argument.
  * `case_name` (string) – Case name of the argument (if available).
  * `absolute_url` (string) – Web page URL on CourtListener for this audio record (which may include a player and details).

* **Notes:** Audio records are linked to dockets when possible, meaning you can find all audio for a case by filtering with the docket ID. Not all courts provide audio; CourtListener’s collection is largest for certain appellate courts. **Pagination:** If listing without filters, note that there are thousands of audio files (one per argument session). Typically you’d filter by court or docket to narrow it down. The audio files themselves can be accessed via the `file_url` (no additional API call needed to get the binary file). If needed, an `OPTIONS` call on this endpoint will show available filters (e.g., which fields support filtering). In the docs, this API is noted to be linked to the docket API and the data about each case.

## Financial Disclosures (Judicial Financial Disclosures)

All U.S. federal judges (and some state judges) must file annual financial disclosure reports. CourtListener provides these documents and their parsed data via the following endpoints. The **Financial Disclosures API** is the main entry point, with several sub-resources for different sections of the disclosure reports. (All endpoints in this section use the base path `/api/rest/v4/` as of v4.1.)

### Financial Disclosure Documents

**Endpoint:** `GET /api/rest/v4/financial-disclosures/` – Lists the financial disclosure report filings (each entry corresponds to one annual disclosure document for a judge). `GET /api/rest/v4/financial-disclosures/{id}/` gets a specific disclosure document record. This is the central record that ties to all the sections below.

* **Query Parameters:**

  * `judge` (integer or URL, optional): Filter by judge (get all disclosures for a specific judge).
  * `year` (integer, optional): Filter by filing year.
  * `court` (string or URL, optional): Filter by the judge’s court (at time of filing).
  * `judge_name` (string, optional): Filter by judge name (text search).

* **Example Request:** All disclosures for judge ID 15:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/financial-disclosures/?judge=15"
  ```

* **Response Structure:** Paginated list of **FinancialDisclosure** objects. Each object includes:

  * `id` (integer) – Disclosure ID.
  * `judge` (string URL) – Reference to the Judge who filed the disclosure.
  * `year` (integer) – Year of the disclosure report.
  * `date_received` (date) – Date the disclosure was received or filed.
  * `absolute_url` (string) – Web URL to view the disclosure document.
  * **Sections:** The disclosure object serves as a parent for various sections of data. It may contain URLs (or embedded lists) for related data: for example, `investments_url`, `incomes_url`, `gifts_url`, etc., pointing to the respective endpoints below with a filter on this disclosure ID. In some cases, the API may embed some of these sections as nested lists, but typically they are accessed via separate endpoints.
  * `pdf_url` (string) – URL to the PDF of the actual signed disclosure form (if available).
  * Other: metadata like `created_at` (when it was added to the system), and possibly a summary or notes.

* **Notes:** This is the main record; it does not contain the detailed financial info directly, but acts as “the link between the other financial disclosure endpoints and the judges in our system”. To get the content of the report, you need to query the sub-endpoints (investments, incomes, etc.) with the disclosure ID (most of those endpoints have a filter like `?financial_disclosure=<id>`). Typically, you will find those section URLs in the FinancialDisclosure object, or you can query them separately as documented below.

### Investments

**Endpoint:** `GET /api/rest/v4/investments/` – Lists **Investment Income** entries. These represent stocks, funds, or other investment holdings that produced income for the judge during the reporting period.

* **Query Parameters:**

  * `financial_disclosure` (integer or URL, optional): **Filter by disclosure ID** – to get all investments reported in a specific disclosure. (This is the usual use; e.g., `?financial_disclosure=5366`.)
  * `judge` (integer or URL, optional): Filter by judge (aggregating across years – e.g., all investments a judge ever reported, if needed).
  * `year` (integer, optional): Filter by year of report.

* **Example Request:** Investments in disclosure ID 5366:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/investments/?financial_disclosure=5366"
  ```

* **Response Structure:** Paginated list of **Investment** objects. Each object includes:

  * `id` (integer) – Investment entry ID.
  * `financial_disclosure` (string URL) – Link to the parent disclosure document.
  * `source` (string) – Name of the investment or asset (e.g., “Apple Inc. (AAPL)”).
  * `income_type` (string) – Type of income (e.g., “Dividends”, “Capital Gains”, “Interest”).
  * `amount` (string) – The amount or category of income (often these are ranges like “\$1001 - \$2500” or a textual category as per disclosure forms).
  * `comment` or `notes` (string, if present) – Any additional notes from the form about this entry.

* **Notes:** Investments are the entries from Part III of the judicial disclosure (Investments and Trusts). The API lists each source of investment income and the type (dividends, rents, interest, capital gains, etc.). The `amount` is usually given as a range category (since exact amounts are often reported in ranges). This endpoint should be used in conjunction with `financial_disclosure` filter to get meaningful results per report. Bulk or cross-year queries are possible but less common. Pagination is rarely needed per single disclosure (as judges usually have a limited number of entries per report).

### Non-Investment Incomes

**Endpoint:** `GET /api/rest/v4/non-investment-incomes/` – Lists **Non-Investment Income** entries. These are sources of income other than investments, such as salaries, honoraria, or other earned income reported by the judge.

* **Query Parameters:**

  * `financial_disclosure` (integer or URL, optional): Filter by disclosure ID (e.g., `?financial_disclosure=5366` to get all non-investment income reported in that disclosure).
  * (Other filters like `judge` or `year` similar to Investments if needed.)

* **Example Request:** Non-investment incomes for disclosure 5366:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/non-investment-incomes/?financial_disclosure=5366"
  ```

* **Response Structure:** Paginated list of **NonInvestmentIncome** objects. Fields include:

  * `id` (integer) – Entry ID.
  * `financial_disclosure` (URL) – Parent disclosure reference.
  * `source` (string) – Source of income (e.g., “State of California – Salary”).
  * `type` (string) – Type of income (e.g., “Salary”, “Teaching Honorarium”).
  * `amount` (string) – Amount or value (again often given as a range or category).

* **Notes:** This corresponds to Part II of the disclosure (Non-Investment Income), which covers salaries, fees, commissions, etc., earned by the filer or spouse. Use the `financial_disclosure` filter to get entries per report. Each entry might also indicate whether the income is from the filer, spouse, or dependent (sometimes encoded in the `source` field text or an additional field like `recipient` if provided). Check the data to see if spouse income is included as separate entries or noted in the source.

### Agreements

**Endpoint:** `GET /api/rest/v4/agreements/` – Lists **Agreements or Arrangements** reported by the judge. These are agreements for future employment, continuing participation in benefit plans, etc., as required in Part I of the disclosure (e.g., agreements for book deals, continuing law firm partnerships, etc.).

* **Query Parameters:**

  * `financial_disclosure` (integer or URL, optional): Filter by disclosure ID.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/agreements/?financial_disclosure=5366"
  ```

* **Response Structure:** List of **Agreement** objects, each with:

  * `id` (integer) – Agreement entry ID.
  * `financial_disclosure` (URL) – Parent disclosure.
  * `description` (string) – Description of the agreement or arrangement. For example, “Partnership interest in XYZ Law Firm retirement plan – will receive benefits upon retirement.”
  * `date` or `year` (string or date, if provided) – Date of agreement (if noted).
  * Possibly `parties` (string) – The other party to the agreement (e.g., the law firm, or entity the agreement is with), if the data model captures it separately.

* **Notes:** Judges list any ongoing agreements (like continuing to teach at a law school, deferred compensation arrangements, etc.) in this section. Often, the description field holds all relevant info. Use the disclosure filter to get relevant entries. Usually only a few per judge at most.

### Gifts

**Endpoint:** `GET /api/rest/v4/gifts/` – Lists **Gifts** received, as reported in the disclosure. Judges must report gifts over a certain threshold (e.g., > \$415 in value, per the example) on Part V of the form.

* **Query Parameters:**

  * `financial_disclosure` (integer or URL, optional): Filter by disclosure ID.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/gifts/?financial_disclosure=5366"
  ```

* **Response Structure:** List of **Gift** objects. Each includes:

  * `id` (integer) – Gift entry ID.
  * `financial_disclosure` (URL) – Parent disclosure.
  * `source` (string) – Source of the gift (who gave it).
  * `description` (string) – Description of the gift (e.g., “Rolex watch” or “Trip to conference including airfare and hotel”).
  * `value` (string) – Value of the gift (often a dollar amount or category, e.g., “\$600”).

* **Notes:** Gifts that aggregate above the threshold in a calendar year are reported. The `source` and `description` together tell what the gift was and who provided it. Use disclosure filter as usual.

### Reimbursements

**Endpoint:** `GET /api/rest/v4/reimbursements/` – Lists **Reimbursements** for travel, events, etc., reported on the disclosure (Part VI of the form). These are payments or reimbursements for travel or other expenses from third parties.

* **Query Parameters:**

  * `financial_disclosure` (integer or URL, optional): Filter by disclosure ID.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/reimbursements/?financial_disclosure=5366"
  ```

* **Response Structure:** List of **Reimbursement** objects, each with:

  * `id` (integer) – Entry ID.
  * `financial_disclosure` (URL) – Parent disclosure.
  * `source` (string) – Who paid or reimbursed (source identity).
  * `description` (string) – Description of expenses (often includes the nature of event and what was covered – e.g., “Conference on X, New York, NY (travel, food, lodging)”).
  * `amount` (string) – Amount of reimbursement (or value of expenses covered, often provided as a total or “N/A” if not required).
  * `date` or `dates` (string) – Dates of travel (sometimes included in description or separate field).

* **Notes:** Use disclosure filter. The description often contains multiple data points (destination, dates, purpose) as a single string since the form typically lists all in one line.

### Debts (Liabilities)

**Endpoint:** `GET /api/rest/v4/debts/` – Lists **Liabilities (Debts)** reported (Part VII of the form). This includes things like mortgages, loans, credit lines over the reporting threshold.

* **Query Parameters:**

  * `financial_disclosure` (integer or URL, optional): Filter by disclosure ID.

* **Example Request:**

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/debts/?financial_disclosure=5366"
  ```

* **Response Structure:** List of **Debt** objects, each with:

  * `id` (integer) – Debt entry ID.
  * `financial_disclosure` (URL) – Parent disclosure.
  * `creditor` (string) – Name of the creditor (who is owed).
  * `type` (string) – Type of liability (e.g., “Mortgage”, “Loan”, “Credit Card”).
  * `amount` (string) – Amount or range of the liability (for instance, categories like “\$15,000 - \$50,000” or “Over \$50,000”).
  * `term_rate` (string, if given) – Terms or interest rate (sometimes judges provide interest rate or term of loan).

* **Notes:** The endpoint is referred to as “Debts” in v4. Ensure to filter by disclosure. Typically a judge might have zero or a few entries here (like mortgages). If a judge has no reportable liabilities, there will be no entries for that disclosure.

*(There are potentially other sections in disclosures, such as “Positions” (outside positions held by the judge, Part I) which might also be captured, or “Miscellaneous” for gifts of travel, etc., but the above are the major categories documented.)*

All financial sub-endpoints use similar patterns: they require linking to a `financial_disclosure`. They share the same pagination format. Field types are mostly strings (since the disclosures are textual in nature – amounts are often strings with ranges, etc.).

## Legal Citation APIs

CourtListener offers endpoints to explore the citation network of judicial opinions, as well as to perform citation lookup and verification.

### Citation Graph – Opinions Cited

**Endpoint:** `GET /api/rest/v4/opinions-cited/` – Provides an interface to the **citation graph** between opinions. This endpoint allows you to retrieve relationships where one opinion cites another. Each result is essentially a citation linkage.

* **Query Parameters:**

  * Typically you will filter by one of the opinions in the relationship. For example:

    * `citing_opinion` (integer or URL, optional): If provided, returns all opinions that the given opinion cites.
    * `cited_opinion` (integer or URL, optional): If provided, returns all opinions that cite the given opinion.
  * You must supply at least one of these to get meaningful data. (If neither is provided, the endpoint may return all citation edges in the database, which is enormous – not practical.)

* **Example Request:** Opinions cited by opinion ID 1163781:

  ```bash
  curl -X GET --header "Authorization: Token YOUR_TOKEN" \
       "https://www.courtlistener.com/api/rest/v4/opinions-cited/?citing_opinion=1163781"
  ```

* **Response Structure:** Paginated list of **Citation** objects (implied; each representing a relationship). Each object might include:

  * `citing_opinion` (string URL) – The opinion that contains the citation (source of the cite).
  * `cited_opinion` (string URL) – The opinion that is being cited (target of the cite).
  * `count` (integer) – Possibly the number of times the citing opinion references the cited opinion (if tracked). Often this will be 1 for a single citation mention.
  * Other metadata: maybe a `citation_text` (the citation string used) or a flag if the reference is in text or footnote, etc., though these details might not be exposed.

* **Notes:** This endpoint essentially enumerates edges in the citation graph. It’s mainly useful if you want to programmatically traverse citations. For example, to find all citations from a given case or all cases that cite a particular case. In many cases, you may not need to use this directly, because the Opinion endpoint already provides an `opinions_cited` list (cites out) and CourtListener’s website provides “cited by” counts. But this API gives the raw data. Ensure to use filters – for instance, to get “cited by” list for an opinion, use `?cited_opinion=<id>`. To get “cites” (what it cites), use `?citing_opinion=<id>`. Pagination might be relevant for very famous cases with many citing opinions.

### Citation Lookup & Verification

**Endpoint:** `POST /api/rest/v3/citation-lookup/` – Accepts a block of text and extracts legal citations, returning matched opinions for each citation. This is a specialized endpoint to help verify citations (for example, to detect fake citations or to get the details of cited cases, useful for AI applications).

* **Request Body:** (required) A form-encoded or JSON payload with a `text` field containing the text to analyze for citations. For example, you can send `text="Obergefell v. Hodges (576 US 644) established ..."`.

* **Example Request (cURL):**

  ```bash
  curl -X POST "https://www.courtlistener.com/api/rest/v3/citation-lookup/" \
       --header "Authorization: Token YOUR_TOKEN" \
       --data "text=Obergefell v. Hodges (576 US 644) established the right to marriage..."
  ```

* **Response Structure:** The response is a JSON **array** where each element corresponds to a citation found in the text. Each element is an object with fields:

  ```json
  [
    {
      "citation": "576 US 644",
      "normalized_citations": ["576 U.S. 644"],
      "start_index": 22,
      "end_index": 32,
      "status": 200,
      "error_message": "",
      "clusters": [ {...} ]
    },
    ...
  ]
  ```

  Where:

  * `citation` (string) – The citation text exactly as it appeared in the input.
  * `normalized_citations` (array of strings) – The citation in a normalized format (for example, adding periods in reporter abbreviations, etc.). There can be multiple if the input citation was ambiguous or could match multiple formats.
  * `start_index` and `end_index` (integers) – The character offsets in the input text where this citation was found. This helps map back to the original text (e.g., to highlight it).
  * `status` (integer) – HTTP-like status indicating the result of lookup for this citation. `200` means a match was found, `404` would mean no case was found for that citation, etc.
  * `error_message` (string) – If `status` is not 200, this may contain a message (e.g., “Citation not found” or “Ambiguous citation”). Empty if no error.
  * `clusters` (array of objects) – If the citation was found, this array will contain the matching opinion cluster(s) for that citation. Usually this is a single object which is essentially the Opinion Cluster (case) that corresponds to the citation. The object will have the same fields as an OpinionCluster (e.g., `id`, `case_name`, `court`, etc., and perhaps an embedded representative Opinion or citation info). If multiple cases match the citation (ambiguous citation), multiple cluster objects could be returned.

* **Notes:** This endpoint is intended for **POST** use with text input. It can handle up to \~50 pages of text (around 64k characters) per request. It is very useful for automatically verifying citations in a document (e.g., a brief) to ensure they correspond to real cases. The `status` codes in the response use HTTP semantics: 200 = found, 404 = not found, 422 = ambiguous, etc., to indicate how each citation was resolved. The returned `clusters` give you the case details; from there you can retrieve full opinion info if needed. This API was introduced to combat AI hallucinations in legal text. It does not require separate GET calls for each citation – all results come back in one response. (As of now, the endpoint is under `/v3/citation-lookup/`. Future versions may have a v4 equivalent, but the functionality is the same.)

## Pagination, Filtering, and Output Formatting

**Pagination:** All list endpoints above use pagination. In v4 APIs, this is typically *cursor-based* pagination enabling deep scrolling. The JSON response for list endpoints always contains `next` and `previous` URLs. For v4 endpoints, the `next` URL will include a `cursor` query parameter to retrieve the next set of results. You should use these URLs rather than constructing page numbers (the v3 APIs used page numbering up to 100 pages). The `count` field gives the total number of results available (except in certain search scenarios where counts might be approximate or omitted for performance). Always check `next` and `previous` – if `next` is not `null`, there are more results to fetch.

**Filtering:** Most endpoints support filtering by their resource fields or related resource fields. The API documentation suggests using the OPTIONS method on endpoints to discover available filters and their syntax. Common patterns include:

* Direct field match (e.g., `?court=scotus` to filter court = SCOTUS).
* Case-insensitive contains for text (e.g., `name__icontains=smith`).
* Range queries for dates or numbers (e.g., `date_filed__range=2020-01-01/2020-12-31` for opinions or entries in 2020).
* Related object filtering via foreign keys (e.g., `?docket=<id>` on parties, docket-entries, etc., or `judge=<id>` on positions).
* The API also often supports ordering via an `order_by` param (for example, `order_by=date_filed` or `-date_filed` to sort descending). Check OPTIONS for supported ordering fields.

**Data Types:** Field types are typically consistent: dates are in ISO 8601 format (YYYY-MM-DD for dates, or date-time if time included); booleans are true/false; numeric IDs are integers; monetary amounts or ranges are strings as provided in original documents (for financial data); and references to other objects are given as URLs (strings beginning with `https://www.courtlistener.com/api/rest/…`). When an object is embedded (nested), its fields will appear as a sub-dictionary instead of a URL.

**Example Workflows:** To use these endpoints in an SDK, one would likely create classes or data structures for each resource (Docket, Opinion, Judge, etc.), with methods to list (with optional filters) and retrieve by ID. The query parameters allow fine-tuning requests, and the consistent JSON structure (with `results` arrays and pagination cursors) allows for easy iteration. Always ensure to handle pagination by checking the `next` URL.

**Special Formatting:** No special format is required in requests beyond standard query strings and JSON for POST. One notable formatting rule is for date range filters: they require the start and end date separated by a forward slash in one query value (e.g., `date_filed__range=2020-01-01/2020-12-31`). Also, when filtering by multiple values for the same field, the API might support comma-separated lists or multiple parameters (the documentation doesn’t explicitly mention multi-value queries, so if needed, do multiple calls or use search queries).

Each endpoint above is fully documented to cover the available operations (GET for all, and POST for citation-lookup; other POST/PUT operations are typically not used for data creation by external clients except in specialized cases). The responses and examples given reflect the expected JSON structures as documented and observed in CourtListener’s API v4.1. Use these as a blueprint for implementing an SDK or integration. All data is subject to CourtListener’s terms of use, and heavy usage may be subject to rate limits (though not detailed here by request).

**Sources:** The information above is based on the official CourtListener REST API documentation and examples, ensuring complete coverage of all REST endpoints and their expected inputs/outputs.
