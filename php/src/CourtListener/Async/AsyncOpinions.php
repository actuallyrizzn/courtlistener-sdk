<?php

namespace CourtListener\Async;

use CourtListener\Api\AsyncBaseApi;
use CourtListener\AsyncCourtListenerClient;

/**
 * Async Opinions API
 */
class AsyncOpinions extends AsyncBaseApi
{
    protected string $endpoint = 'opinions/';

    public function __construct(AsyncCourtListenerClient $client)
    {
        parent::__construct($client);
    }
}
