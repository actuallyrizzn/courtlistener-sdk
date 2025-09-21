<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Attorneys API endpoint
 */
class Attorneys extends BaseApi
{
    protected string $endpoint = 'attorneys/';

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
     * List attorneys with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listAttorneys(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific attorneys by ID
     *
     * @param int|string $id Attorneys ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getAttorneys($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search attorneys
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchAttorneys(array $params = []): array
    {
        return $this->search($params);
    }
}
