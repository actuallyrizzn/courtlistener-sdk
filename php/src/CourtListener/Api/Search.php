<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Search API endpoint
 */
class Search extends BaseApi
{
    protected string $endpoint = 'search/';

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
     * List search with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listSearch(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific search by ID
     *
     * @param int|string $id Search ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getSearch($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search search
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchSearch(array $params = []): array
    {
        return $this->search($params);
    }
}
