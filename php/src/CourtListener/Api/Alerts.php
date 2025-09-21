<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Alerts API endpoint
 */
class Alerts extends BaseApi
{
    protected string $endpoint = 'alerts/';

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
     * List alerts with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listAlerts(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific alert by ID
     *
     * @param int|string $id Alert ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getAlert(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Create a new alert
     *
     * @param array $data Alert data
     * @return array
     * @throws CourtListenerException
     */
    public function createAlert(array $params = []) {
        return $this->create($data);
    }

    /**
     * Update an existing alert
     *
     * @param int|string $id Alert ID
     * @param array $data Alert data
     * @return array
     * @throws CourtListenerException
     */
    public function updateAlert(array $params = []) {
        return $this->update($id, $data);
    }

    /**
     * Delete an alert
     *
     * @param int|string $id Alert ID
     * @return array
     * @throws CourtListenerException
     */
    public function deleteAlert(array $params = []) {
        return $this->delete($id);
    }

    /**
     * Search alerts
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchAlerts(array $params = []) {
        return $this->search($params);
    }
}
