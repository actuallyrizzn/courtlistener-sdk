<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Positions API endpoint
 */
class Positions extends BaseApi
{
    protected string $endpoint = 'positions/';

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
     * List positions with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listPositions(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific positions by ID
     *
     * @param int|string $id Positions ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getPositions(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search positions
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchPositions(array $params = []) {
        return $this->search($params);
    }
}
