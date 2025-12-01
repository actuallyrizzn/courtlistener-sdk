<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * DocketAlerts API endpoint
 */
class DocketAlerts extends BaseApi
{
    protected string $endpoint = 'docket-alerts/';

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
     * List docket alerts with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listDocketAlerts(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific docket alerts by ID
     *
     * @param int|string $id DocketAlerts ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketAlerts($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search docket alerts
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchDocketAlerts(array $params = []) {
        return $this->search($params);
    }
}
