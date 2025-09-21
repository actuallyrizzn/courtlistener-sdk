<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * SpouseIncomes API endpoint
 */
class SpouseIncomes extends BaseApi
{
    protected string $endpoint = 'spouse-incomes/';

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
     * List spouse incomes with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listSpouseIncomes(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific spouse incomes by ID
     *
     * @param int|string $id SpouseIncomes ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getSpouseIncomes($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search spouse incomes
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchSpouseIncomes(array $params = []): array
    {
        return $this->search($params);
    }
}
