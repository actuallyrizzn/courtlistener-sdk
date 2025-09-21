<?php

namespace CourtListener\Api;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\CourtListenerException;

/**
 * Audio API endpoint
 */
class Audio extends BaseApi
{
    protected string $endpoint = 'audio/';

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
     * List audio with advanced filtering
     *
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function listAudio(array $params = []) {
        return $this->list($params);
    }

    /**
     * Get a specific audio by ID
     *
     * @param int|string $id Audio ID
     * @param array $params Query parameters
     * @return array
     * @throws CourtListenerException
     */
    public function getAudio(array $params = []) {
        return $this->get($id, $params);
    }

    /**
     * Search audio
     *
     * @param array $params Search parameters
     * @return array
     * @throws CourtListenerException
     */
    public function searchAudio(array $params = []) {
        return $this->search($params);
    }
}
