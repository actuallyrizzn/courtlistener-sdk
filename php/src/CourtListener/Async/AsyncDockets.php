<?php

namespace CourtListener\Async;

use CourtListener\Api\AsyncBaseApi;
use CourtListener\AsyncCourtListenerClient;

/**
 * Async Dockets API
 */
class AsyncDockets extends AsyncBaseApi
{
    protected string $endpoint = 'dockets/';

    public function __construct(AsyncCourtListenerClient $client)
    {
        parent::__construct($client);
    }
}
