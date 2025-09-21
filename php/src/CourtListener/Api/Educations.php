<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Educations API endpoint
 */
class Educations extends BaseApi
{
    protected string $endpoint = 'educations/';

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
     * List educations with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listEducations(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific educations by ID
     *
     * @param int|string $id Educations ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getEducations(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search educations
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchEducations(array $params = []) {
        return $this->search($params);
    }
}
