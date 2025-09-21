<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Investments API endpoint
 */
class Investments extends BaseApi
{
    protected string $endpoint = 'investments/';

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
     * List investments with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listInvestments(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific investments by ID
     *
     * @param int|string $id Investments ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getInvestments(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search investments
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchInvestments(array $params = []) {
        return $this->search($params);
    }
}
