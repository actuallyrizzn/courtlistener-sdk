<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Citations API endpoint
 */
class Citations extends BaseApi
{
    protected string $endpoint = 'citations/';

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
     * List citations with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listCitations(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific citations by ID
     *
     * @param int|string $id Citations ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getCitations(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search citations
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchCitations(array $params = []) {
        return $this->search($params);
    }
}
