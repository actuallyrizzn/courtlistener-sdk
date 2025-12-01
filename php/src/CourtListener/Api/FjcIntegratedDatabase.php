<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * FjcIntegratedDatabase API endpoint
 */
class FjcIntegratedDatabase extends BaseApi
{
    protected string $endpoint = 'fjc-integrated-database/';

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
     * List fjc integrated database with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listFjcIntegratedDatabase(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific fjc integrated database by ID
     *
     * @param int|string $id FjcIntegratedDatabase ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getFjcIntegratedDatabase($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search fjc integrated database
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchFjcIntegratedDatabase(array $params = []) {
        return $this->search($params);
    }
}
