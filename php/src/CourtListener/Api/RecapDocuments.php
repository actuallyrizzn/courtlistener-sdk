<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * RecapDocuments API endpoint
 */
class RecapDocuments extends BaseApi
{
    protected string $endpoint = 'recap-documents/';

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
     * List recap documents with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listRecapDocuments(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific recap documents by ID
     *
     * @param int|string $id RecapDocuments ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getRecapDocuments($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search recap documents
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchRecapDocuments(array $params = []): array
    {
        return $this->search($params);
    }
}
