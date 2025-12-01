<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Tag API endpoint
 */
class Tag extends BaseApi
{
    protected string $endpoint = 'tag/';

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
     * List tag with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listTag(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific tag by ID
     *
     * @param int|string $id Tag ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getTag($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search tag
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchTag(array $params = []) {
        return $this->search($params);
    }
}
