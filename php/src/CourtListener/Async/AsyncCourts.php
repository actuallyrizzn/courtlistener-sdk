<?php

namespace CourtListener\Async;

use CourtListener\Api\AsyncBaseApi;
use CourtListener\AsyncCourtListenerClient;

/**
 * Async Courts API
 */
class AsyncCourts extends AsyncBaseApi
{
    protected string $endpoint = 'courts/';

    public function __construct(AsyncCourtListenerClient $client)
    {
        parent::__construct($client);
    }
}
