<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Schools API endpoint
 */
class Schools extends BaseApi
{
    protected string $endpoint = 'schools/';

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
     * List schools with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listSchools(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific schools by ID
     *
     * @param int|string $id Schools ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getSchools(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search schools
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchSchools(array $params = []) {
        return $this->search($params);
    }
}
