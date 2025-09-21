<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * AbaRatings API endpoint
 */
class AbaRatings extends BaseApi
{
    protected string $endpoint = 'aba-ratings/';

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
     * List aba ratings with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listAbaRatings(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific aba ratings by ID
     *
     * @param int|string $id AbaRatings ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getAbaRatings($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search aba ratings
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchAbaRatings(array $params = []): array
    {
        return $this->search($params);
    }
}
