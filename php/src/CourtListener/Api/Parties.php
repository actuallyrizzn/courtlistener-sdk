<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Parties API endpoint
 */
class Parties extends BaseApi
{
    protected string $endpoint = 'parties/';

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
     * List parties with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listParties(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific parties by ID
     *
     * @param int|string $id Parties ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getParties($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search parties
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchParties(array $params = []): array
    {
        return $this->search($params);
    }
}
