<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * DisclosurePositions API endpoint
 */
class DisclosurePositions extends BaseApi
{
    protected string $endpoint = 'disclosure-positions/';

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
     * List disclosure positions with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listDisclosurePositions(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific disclosure positions by ID
     *
     * @param int|string $id DisclosurePositions ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getDisclosurePositions($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search disclosure positions
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchDisclosurePositions(array $params = []): array
    {
        return $this->search($params);
    }
}
