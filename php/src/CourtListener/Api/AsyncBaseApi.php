<?php

namespace CourtListener\Api;

use CourtListener\AsyncCourtListenerClient;
use GuzzleHttp\Promise\PromiseInterface;

/**
 * Base API class providing async functionality for all API endpoints
 * 
 * All methods return Promises that can be awaited or chained.
 */
abstract class AsyncBaseApi
{
    protected AsyncCourtListenerClient $client;
    protected string $endpoint;

    /**
     * Constructor
     *
     * @param AsyncCourtListenerClient $client
     */
    public function __construct(AsyncCourtListenerClient $client)
    {
        $this->client = $client;
    }

    /**
     * Get all items with pagination (async)
     *
     * @param array $params Query parameters
     * @return PromiseInterface
     */
    public function listAsync(array $params = []): PromiseInterface
    {
        return $this->client->getAsync($this->endpoint, $params);
    }

    /**
     * Get a specific item by ID (async)
     *
     * @param int|string $id Item ID
     * @param array $params Query parameters
     * @return PromiseInterface
     */
    public function getAsync($id, array $params = []): PromiseInterface
    {
        return $this->client->getAsync($this->endpoint . $id . '/', $params);
    }

    /**
     * Create a new item (async)
     *
     * @param array $data Item data
     * @return PromiseInterface
     */
    public function createAsync(array $data): PromiseInterface
    {
        return $this->client->postAsync($this->endpoint, $data);
    }

    /**
     * Update an existing item (async)
     *
     * @param int|string $id Item ID
     * @param array $data Item data
     * @return PromiseInterface
     */
    public function updateAsync($id, array $data): PromiseInterface
    {
        return $this->client->putAsync($this->endpoint . $id . '/', $data);
    }

    /**
     * Partially update an existing item (async)
     *
     * @param int|string $id Item ID
     * @param array $data Item data
     * @return PromiseInterface
     */
    public function patchAsync($id, array $data): PromiseInterface
    {
        return $this->client->patchAsync($this->endpoint . $id . '/', $data);
    }

    /**
     * Delete an item (async)
     *
     * @param int|string $id Item ID
     * @return PromiseInterface
     */
    public function deleteAsync($id): PromiseInterface
    {
        return $this->client->deleteAsync($this->endpoint . $id . '/');
    }

    /**
     * Search items (async)
     *
     * @param array $params Search parameters
     * @return PromiseInterface
     */
    public function searchAsync(array $params = []): PromiseInterface
    {
        return $this->client->getAsync($this->endpoint . 'search/', $params);
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
