<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Debts API endpoint
 */
class Debts extends BaseApi
{
    protected string $endpoint = 'debts/';

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
     * List debts with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listDebts(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific debts by ID
     *
     * @param int|string $id Debts ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getDebts(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search debts
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchDebts(array $params = []) {
        return $this->search($params);
    }
}
