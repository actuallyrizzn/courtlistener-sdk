<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Base API class providing common functionality for all API endpoints
 */
abstract class BaseApi
{
    protected CourtListenerClient $client;
    protected string $endpoint;

    /**
     * Constructor
     *
     * @param CourtListenerClient $client
     */
    public function __construct(CourtListenerClient $client)
    {
        $this->client = $client;
    }

    /**
     * Get all items with pagination
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function list(array $params = [])
    {
        return $this->client->makeRequest('GET', $this->endpoint, [
            'query' => $params
        ]);
    }

    /**
     * Get a specific item by ID
     *
     * @param int|string $id Item ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function get($id, array $params = [])
    {
        return $this->client->makeRequest('GET', $this->endpoint . $id . '/', [
            'query' => $params
        ]);
    }

    /**
     * Create a new item
     *
     * @param array $data Item data
     * @return array
     * @throws CourtListenerException
     */
    public function create(array $data)
    {
        return $this->client->makeRequest('POST', $this->endpoint, [
            'json' => $data
        ]);
    }

    /**
     * Update an existing item
     *
     * @param int|string $id Item ID
     * @param array $data Item data
     * @return array
     * @throws CourtListenerException
     */
    public function update($id, array $data)
    {
        return $this->client->makeRequest('PUT', $this->endpoint . $id . '/', [
            'json' => $data
        ]);
    }

    /**
     * Partially update an existing item
     *
     * @param int|string $id Item ID
     * @param array $data Item data
     * @return array
     * @throws CourtListenerException
     */
    public function patch($id, array $data)
    {
        return $this->client->makeRequest('PATCH', $this->endpoint . $id . '/', [
            'json' => $data
        ]);
    }

    /**
     * Delete an item
     *
     * @param int|string $id Item ID
     * @return array
     * @throws CourtListenerException
     */
    public function delete($id)
    {
        return $this->client->makeRequest('DELETE', $this->endpoint . $id . '/');
    }

    /**
     * Search items
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function search(array $params = [])
    {
        return $this->client->makeRequest('GET', $this->endpoint . 'search/', [
            'query' => $params
        ]);
    }

    /**
     * Get the endpoint path
     *
     * @return string
     */
    public function getEndpoint(): string
    {
        return $this->endpoint;
    }
}
