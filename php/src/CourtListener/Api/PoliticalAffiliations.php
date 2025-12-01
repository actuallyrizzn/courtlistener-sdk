<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * PoliticalAffiliations API endpoint
 */
class PoliticalAffiliations extends BaseApi
{
    protected string $endpoint = 'political-affiliations/';

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
     * List political affiliations with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listPoliticalAffiliations(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific political affiliations by ID
     *
     * @param int|string $id PoliticalAffiliations ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getPoliticalAffiliations($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search political affiliations
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchPoliticalAffiliations(array $params = []) {
        return $this->search($params);
    }
}
