<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Judges API endpoint
 */
class Judges extends BaseApi
{
    protected string $endpoint = 'judges/';

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
     * List judges with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listJudges(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific judges by ID
     *
     * @param int|string $id Judges ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getJudges($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search judges
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchJudges(array $params = []): array
    {
        return $this->search($params);
    }
}
