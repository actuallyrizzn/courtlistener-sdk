<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Sources API endpoint
 */
class Sources extends BaseApi
{
    protected string $endpoint = 'sources/';

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
     * List sources with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listSources(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific sources by ID
     *
     * @param int|string $id Sources ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getSources($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search sources
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchSources(array $params = []) {
        return $this->search($params);
    }
}
