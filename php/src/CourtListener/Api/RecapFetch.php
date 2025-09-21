<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * RecapFetch API endpoint
 */
class RecapFetch extends BaseApi
{
    protected string $endpoint = 'recap-fetch/';

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
     * List recap fetch with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listRecapFetch(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific recap fetch by ID
     *
     * @param int|string $id RecapFetch ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getRecapFetch(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search recap fetch
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchRecapFetch(array $params = []) {
        return $this->search($params);
    }
}
