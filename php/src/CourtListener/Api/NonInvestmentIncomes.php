<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * NonInvestmentIncomes API endpoint
 */
class NonInvestmentIncomes extends BaseApi
{
    protected string $endpoint = 'non-investment-incomes/';

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
     * List non investment incomes with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listNonInvestmentIncomes(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific non investment incomes by ID
     *
     * @param int|string $id NonInvestmentIncomes ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getNonInvestmentIncomes($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search non investment incomes
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchNonInvestmentIncomes(array $params = []): array
    {
        return $this->search($params);
    }
}
