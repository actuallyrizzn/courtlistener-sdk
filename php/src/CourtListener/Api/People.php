<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * People API endpoint
 */
class People extends BaseApi
{
    protected string $endpoint = 'people/';

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
     * List people with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listPeople(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific people by ID
     *
     * @param int|string $id People ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getPeople($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search people
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchPeople(array $params = []) {
        return $this->search($params);
    }
}
