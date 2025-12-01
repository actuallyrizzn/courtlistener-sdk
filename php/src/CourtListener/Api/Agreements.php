<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Agreements API endpoint
 */
class Agreements extends BaseApi
{
    protected string $endpoint = 'agreements/';

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
     * List agreements with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listAgreements(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific agreements by ID
     *
     * @param int|string $id Agreements ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getAgreements($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search agreements
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchAgreements(array $params = []) {
        return $this->search($params);
    }
}
