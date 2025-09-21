<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * RetentionEvents API endpoint
 */
class RetentionEvents extends BaseApi
{
    protected string $endpoint = 'retention-events/';

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
     * List retention events with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listRetentionEvents(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific retention events by ID
     *
     * @param int|string $id RetentionEvents ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getRetentionEvents(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search retention events
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchRetentionEvents(array $params = []) {
        return $this->search($params);
    }
}
