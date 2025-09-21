<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Dockets API endpoint
 */
class Dockets extends BaseApi
{
    protected string $endpoint = 'dockets/';

    /**
     * Constructor
     *
     * @param CourtListenerClient $client
     */
    public function __construct(CourtListenerClient $client)
    {
        parent::__construct($client);
    }

    /**
     * List dockets with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listDockets(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific docket by ID
     *
     * @param int|string $id Docket ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocket($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search dockets
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchDockets(array $params = []): array
    {
        return $this->search($params);
    }

    /**
     * Get docket entries for a specific docket
     *
     * @param int|string $docketId Docket ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketEntries($docketId, array $params = []): array
    {
        return $this->client->makeRequest('GET', "dockets/{$docketId}/docket-entries/", [
            'query' => $params
        ]);
    }

    /**
     * Get parties for a specific docket
     *
     * @param int|string $docketId Docket ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getParties($docketId, array $params = []): array
    {
        return $this->client->makeRequest('GET', "dockets/{$docketId}/parties/", [
            'query' => $params
        ]);
    }

    /**
     * Get attorneys for a specific docket
     *
     * @param int|string $docketId Docket ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getAttorneys($docketId, array $params = []): array
    {
        return $this->client->makeRequest('GET', "dockets/{$docketId}/attorneys/", [
            'query' => $params
        ]);
    }

    /**
     * Get RECAP documents for a specific docket
     *
     * @param int|string $docketId Docket ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getRecapDocuments($docketId, array $params = []): array
    {
        return $this->client->makeRequest('GET', "dockets/{$docketId}/recap/", [
            'query' => $params
        ]);
    }

    /**
     * Get docket by docket number
     *
     * @param string $docketNumber Docket number
     * @param string|null $court Court ID to filter by
     * @return array|null
     * @throws CourtListenerException
     */
    public function getDocketByNumber(string $docketNumber, ?string $court = null): ?array
    {
        $filters = ['docket_number' => $docketNumber];
        if ($court) {
            $filters['court'] = $court;
        }
        
        $response = $this->listDockets($filters);
        
        if (!empty($response['results'])) {
            return $response['results'][0];
        }
        
        return null;
    }

    /**
     * Get dockets for a specific court
     *
     * @param string $courtId Court ID
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByCourt(string $courtId, array $filters = []): array
    {
        $courtFilters = array_merge(['court' => $courtId], $filters);
        return $this->listDockets($courtFilters);
    }

    /**
     * Get dockets within a date range
     *
     * @param string|null $startDate Start date (Y-m-d format)
     * @param string|null $endDate End date (Y-m-d format)
     * @param string|null $court Court ID to filter by
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByDateRange(
        ?string $startDate = null,
        ?string $endDate = null,
        ?string $court = null,
        array $filters = []
    ): array {
        $dateFilters = [];
        
        if ($startDate) {
            $dateFilters['date_filed__gte'] = $startDate;
        }
        
        if ($endDate) {
            $dateFilters['date_filed__lte'] = $endDate;
        }
        
        if ($court) {
            $dateFilters['court'] = $court;
        }
        
        $allFilters = array_merge($dateFilters, $filters);
        return $this->listDockets($allFilters);
    }

    /**
     * Get dockets by case type
     *
     * @param string $caseType Case type
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByCaseType(string $caseType, array $filters = []): array
    {
        $typeFilters = array_merge(['case_type' => $caseType], $filters);
        return $this->listDockets($typeFilters);
    }

    /**
     * Get dockets by nature of suit
     *
     * @param string $natureOfSuit Nature of suit
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByNatureOfSuit(string $natureOfSuit, array $filters = []): array
    {
        $suitFilters = array_merge(['nature_of_suit' => $natureOfSuit], $filters);
        return $this->listDockets($suitFilters);
    }

    /**
     * Get dockets by assigned judge
     *
     * @param string $judgeId Judge ID
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByJudge(string $judgeId, array $filters = []): array
    {
        $judgeFilters = array_merge(['assigned_to' => $judgeId], $filters);
        return $this->listDockets($judgeFilters);
    }

    /**
     * Get dockets with specific status
     *
     * @param string $status Docket status
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByStatus(string $status, array $filters = []): array
    {
        $statusFilters = array_merge(['status' => $status], $filters);
        return $this->listDockets($statusFilters);
    }

    /**
     * Get dockets with financial disclosures
     *
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsWithFinancialDisclosures(array $filters = []): array
    {
        $financialFilters = array_merge(['has_financial_disclosures' => 'true'], $filters);
        return $this->listDockets($financialFilters);
    }

    /**
     * Get dockets with audio recordings
     *
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsWithAudio(array $filters = []): array
    {
        $audioFilters = array_merge(['has_audio' => 'true'], $filters);
        return $this->listDockets($audioFilters);
    }

    /**
     * Get dockets with RECAP documents
     *
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsWithRecapDocuments(array $filters = []): array
    {
        $recapFilters = array_merge(['has_recap_documents' => 'true'], $filters);
        return $this->listDockets($recapFilters);
    }

    /**
     * Get dockets by jurisdiction type
     *
     * @param string $jurisdictionType Jurisdiction type
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByJurisdictionType(string $jurisdictionType, array $filters = []): array
    {
        $jurisdictionFilters = array_merge(['jurisdiction_type' => $jurisdictionType], $filters);
        return $this->listDockets($jurisdictionFilters);
    }

    /**
     * Get dockets by jury demand
     *
     * @param string $juryDemand Jury demand status
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByJuryDemand(string $juryDemand, array $filters = []): array
    {
        $juryFilters = array_merge(['jury_demand' => $juryDemand], $filters);
        return $this->listDockets($juryFilters);
    }
}
