<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * RecapQuery API endpoint
 */
class RecapQuery extends BaseApi
{
    protected string $endpoint = 'recap-query/';

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
     * List recap query with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listRecapQuery(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific recap query by ID
     *
     * @param int|string $id RecapQuery ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getRecapQuery(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search recap query
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchRecapQuery(array $params = []) {
        return $this->search($params);
    }
}
