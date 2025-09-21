<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * OriginatingCourtInformation API endpoint
 */
class OriginatingCourtInformation extends BaseApi
{
    protected string $endpoint = 'originating-court-information/';

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
     * List originating court information with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listOriginatingCourtInformation(array $params = []): array
    {
        return $this->list($params);
    }

    /**
     * Get a specific originating court information by ID
     *
     * @param int|string $id OriginatingCourtInformation ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getOriginatingCourtInformation($id, array $params = []): array
    {
        return $this->get($id, $params);
    }

    /**
     * Search originating court information
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchOriginatingCourtInformation(array $params = []): array
    {
        return $this->search($params);
    }
}
