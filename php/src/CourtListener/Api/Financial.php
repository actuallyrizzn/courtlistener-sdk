<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Financial API endpoint
 */
class Financial extends BaseApi
{
    protected string $endpoint = 'financial/';

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
     * List financial with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listFinancial(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific financial by ID
     *
     * @param int|string $id Financial ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getFinancial($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search financial
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchFinancial(array $params = []) {
        return $this->search($params);
    }
}
