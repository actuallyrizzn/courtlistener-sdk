<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * DocketEntries API endpoint
 */
class DocketEntries extends BaseApi
{
    protected string $endpoint = 'docket-entries/';

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
     * List docket entries with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listDocketEntries(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific docket entries by ID
     *
     * @param int|string $id DocketEntries ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocketEntries($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search docket entries
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchDocketEntries(array $params = []) {
        return $this->search($params);
    }
}
