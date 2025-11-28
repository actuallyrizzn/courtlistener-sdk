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
    public function listDockets(array $params = []) {
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
    public function getDocket($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search dockets
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchDockets(array $params = []) {
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
    public function getDocketEntries($docketId, array $params = []) {
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
    public function getParties($docketId, array $params = []) {
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
    public function getAttorneys($docketId, array $params = []) {
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
    public function getRecapDocuments($docketId, array $params = []) {
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
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByCourt($courtId, array $params = []) {
        $courtFilters = array_merge(['court' => $courtId], $params);
        return $this->listDockets($courtFilters);
    }

    /**
     * Get dockets within a date range
     *
     * @param string|null $startDate Start date (Y-m-d format)
     * @param string|null $endDate End date (Y-m-d format)
     * @param string|null $courtId Court ID to filter by
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByDateRange($startDate = null, $endDate = null, $courtId = null, array $params = []) {
        $filters = $params;
        
        if ($startDate) {
            $filters['date_filed__gte'] = $startDate;
        }
        
        if ($endDate) {
            $filters['date_filed__lte'] = $endDate;
        }
        
        if ($courtId) {
            $filters['court'] = $courtId;
        }
        
        return $this->listDockets($filters);
    }

    /**
     * Get dockets by case type
     *
     * @param string $caseType Case type
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByCaseType($caseType, array $params = []) {
        $typeFilters = array_merge(['case_type' => $caseType], $params);
        return $this->listDockets($typeFilters);
    }

    /**
     * Get dockets by nature of suit
     *
     * @param string $natureOfSuit Nature of suit
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByNatureOfSuit($natureOfSuit, array $params = []) {
        $suitFilters = array_merge(['nature_of_suit' => $natureOfSuit], $params);
        return $this->listDockets($suitFilters);
    }

    /**
     * Get dockets by assigned judge
     *
     * @param string $judgeId Judge ID
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByJudge($judgeId, array $params = []) {
        $judgeFilters = array_merge(['assigned_to' => $judgeId], $params);
        return $this->listDockets($judgeFilters);
    }

    /**
     * Get dockets with specific status
     *
     * @param string $status Docket status
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByStatus($status, array $params = []) {
        $statusFilters = array_merge(['status' => $status], $params);
        return $this->listDockets($statusFilters);
    }

    /**
     * Get dockets with financial disclosures
     *
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsWithFinancialDisclosures(array $params = []) {
        $financialFilters = array_merge(['has_financial_disclosures' => 'true'], $params);
        return $this->listDockets($financialFilters);
    }

    /**
     * Get dockets with audio recordings
     *
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsWithAudio(array $params = []) {
        $audioFilters = array_merge(['has_audio' => 'true'], $params);
        return $this->listDockets($audioFilters);
    }

    /**
     * Get dockets with RECAP documents
     *
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsWithRecapDocuments(array $params = []) {
        $recapFilters = array_merge(['has_recap_documents' => 'true'], $params);
        return $this->listDockets($recapFilters);
    }

    /**
     * Get dockets by jurisdiction type
     *
     * @param string $jurisdictionType Jurisdiction type
     * @param array $params Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketsByJurisdictionType($jurisdictionType, array $params = []) {
        $jurisdictionFilters = array_merge(['jurisdiction_type' => $jurisdictionType], $params);
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
    public function getDocketsByJuryDemand($juryDemand, array $params = []) {
        $juryFilters = array_merge(['jury_demand' => $juryDemand], $params);
        return $this->listDockets($juryFilters);
    }
}
