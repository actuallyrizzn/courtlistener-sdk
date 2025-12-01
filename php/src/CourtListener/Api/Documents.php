<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Documents API endpoint
 */
class Documents extends BaseApi
{
    protected string $endpoint = 'documents/';

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
     * List documents with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listDocuments(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific documents by ID
     *
     * @param int|string $id Documents ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getDocuments($id, array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search documents
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchDocuments(array $params = []) {
        return $this->search($params);
    }
}
