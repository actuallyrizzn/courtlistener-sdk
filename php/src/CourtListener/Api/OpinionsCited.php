<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * OpinionsCited API endpoint
 */
class OpinionsCited extends BaseApi
{
    protected string $endpoint = 'opinions-cited/';

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
     * List opinions cited with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listOpinionsCited(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific opinions cited by ID
     *
     * @param int|string $id OpinionsCited ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getOpinionsCited(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search opinions cited
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchOpinionsCited(array $params = []) {
        return $this->search($params);
    }
}
