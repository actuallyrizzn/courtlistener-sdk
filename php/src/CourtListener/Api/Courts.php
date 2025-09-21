<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Courts API endpoint
 */
class Courts extends BaseApi
{
    protected string $endpoint = 'courts/';

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
     * List courts with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listCourts(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific court by ID
     *
     * @param int|string $id Court ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getCourt($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search courts
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchCourts(array $params = []): array
    {
        return $this->search($params);
    }

    /**
     * Get court hierarchy
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getHierarchy(array $params = []): array
    {
        return $this->client->makeRequest('GET', 'courts/hierarchy/', [
            'query' => $params
        ]);
    }

    /**
     * Get court types
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getTypes(array $params = []): array
    {
        return $this->client->makeRequest('GET', 'courts/types/', [
            'query' => $params
        ]);
    }
}
