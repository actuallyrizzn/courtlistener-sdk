<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Reimbursements API endpoint
 */
class Reimbursements extends BaseApi
{
    protected string $endpoint = 'reimbursements/';

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
     * List reimbursements with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listReimbursements(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific reimbursements by ID
     *
     * @param int|string $id Reimbursements ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getReimbursements($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search reimbursements
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchReimbursements(array $params = []): array
    {
        return $this->search($params);
    }
}
