<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Gifts API endpoint
 */
class Gifts extends BaseApi
{
    protected string $endpoint = 'gifts/';

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
     * List gifts with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listGifts(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific gifts by ID
     *
     * @param int|string $id Gifts ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getGifts($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search gifts
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchGifts(array $params = []) {
        return $this->search($params);
    }
}
