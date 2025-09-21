<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Clusters API endpoint
 */
class Clusters extends BaseApi
{
    protected string $endpoint = 'clusters/';

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
     * List clusters with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listClusters(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific clusters by ID
     *
     * @param int|string $id Clusters ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getClusters(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search clusters
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchClusters(array $params = []) {
        return $this->search($params);
    }
}
