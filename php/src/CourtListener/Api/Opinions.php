<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Opinions API endpoint
 */
class Opinions extends BaseApi
{
    protected string $endpoint = 'opinions/';

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
     * List opinions with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listOpinions(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific opinion by ID
     *
     * @param int|string $id Opinion ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinion(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search opinions
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchOpinions(array $params = []) {
        return $this->search($params);
    }

    /**
     * Get opinions cited by a specific opinion
     *
     * @param int|string $opinionId Opinion ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsCited(array $params = []) {
        return $this->client->makeRequest('GET', "opinions/{$opinionId}/cited/", [
            'query' => $params
        ]);
    }

    /**
     * Get opinions that cite a specific opinion
     *
     * @param int|string $opinionId Opinion ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsCiting(array $params = []) {
        return $this->client->makeRequest('GET', "opinions/{$opinionId}/citing/", [
            'query' => $params
        ]);
    }

    /**
     * Get clusters for a specific opinion
     *
     * @param int|string $opinionId Opinion ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getClusters(array $params = []) {
        return $this->client->makeRequest('GET', "opinions/{$opinionId}/clusters/", [
            'query' => $params
        ]);
    }

    /**
     * Get opinions by court
     *
     * @param string $courtId Court ID
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByCourt(array $params = []) {
        $courtFilters = array_merge(['court' => $courtId], $filters);
        return $this->listOpinions($courtFilters);
    }

    /**
     * Get opinions by judge
     *
     * @param string $judgeId Judge ID
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByJudge(array $params = []) {
        $judgeFilters = array_merge(['author' => $judgeId], $filters);
        return $this->listOpinions($judgeFilters);
    }

    /**
     * Get opinions by date range
     *
     * @param string|null $startDate Start date (Y-m-d format)
     * @param string|null $endDate End date (Y-m-d format)
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByDateRange($startDate, $endDate, array $filters = []) {
        $dateFilters = [];
        
        if ($startDate) {
            $dateFilters['date_filed__gte'] = $startDate;
        }
        
        if ($endDate) {
            $dateFilters['date_filed__lte'] = $endDate;
        }
        
        $allFilters = array_merge($dateFilters, $filters);
        return $this->listOpinions($allFilters);
    }

    /**
     * Get precedential opinions
     *
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getPrecedentialOpinions(array $filters = []) {
        $precedentialFilters = array_merge(['stat_Precedential' => 'on'], $filters);
        return $this->listOpinions($precedentialFilters);
    }

    /**
     * Get non-precedential opinions
     *
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getNonPrecedentialOpinions(array $params = []) {
        $nonPrecedentialFilters = array_merge(['stat_Non-Precedential' => 'on'], $filters);
        return $this->listOpinions($nonPrecedentialFilters);
    }

    /**
     * Get opinions by type
     *
     * @param string $type Opinion type
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByType(array $params = []) {
        $typeFilters = array_merge(['type' => $type], $filters);
        return $this->listOpinions($typeFilters);
    }

    /**
     * Get opinions with audio
     *
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsWithAudio(array $params = []) {
        $audioFilters = array_merge(['has_audio' => 'true'], $filters);
        return $this->listOpinions($audioFilters);
    }

    /**
     * Get opinions by jurisdiction
     *
     * @param string $jurisdiction Jurisdiction
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByJurisdiction(array $params = []) {
        $jurisdictionFilters = array_merge(['jurisdiction' => $jurisdiction], $filters);
        return $this->listOpinions($jurisdictionFilters);
    }

    /**
     * Get opinions by resource type
     *
     * @param string $resourceType Resource type
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByResourceType(array $params = []) {
        $resourceFilters = array_merge(['resource_type' => $resourceType], $filters);
        return $this->listOpinions($resourceFilters);
    }

    /**
     * Get recent opinions
     *
     * @param int $limit Number of recent opinions to retrieve
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getRecentOpinions($limit = 20, array $filters = []) {
        $recentFilters = array_merge([
            'order_by' => '-date_filed',
            'per_page' => $limit
        ], $filters);
        return $this->listOpinions($recentFilters);
    }

    /**
     * Get opinions by cluster
     *
     * @param string $clusterId Cluster ID
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByCluster(array $params = []) {
        $clusterFilters = array_merge(['cluster' => $clusterId], $filters);
        return $this->listOpinions($clusterFilters);
    }

    /**
     * Get opinions with specific citation count
     *
     * @param int $minCitations Minimum citation count
     * @param int|null $maxCitations Maximum citation count
     * @param array $filters Additional filters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsByCitationCount(array $params = []) {
        $citationFilters = ['citation_count__gte' => $minCitations];
        
        if ($maxCitations !== null) {
            $citationFilters['citation_count__lte'] = $maxCitations;
        }
        
        $allFilters = array_merge($citationFilters, $filters);
        return $this->listOpinions($allFilters);
    }
}
