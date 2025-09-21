<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * FinancialDisclosures API endpoint
 */
class FinancialDisclosures extends BaseApi
{
    protected string $endpoint = 'financial-disclosures/';

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
     * List financial disclosures with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listFinancialDisclosures(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific financial disclosures by ID
     *
     * @param int|string $id FinancialDisclosures ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getFinancialDisclosures(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search financial disclosures
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchFinancialDisclosures(array $params = []) {
        return $this->search($params);
    }
}
