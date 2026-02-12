<?php

require_once __DIR__ . '/../vendor/autoload.php';

use CourtListener\AsyncCourtListenerClient;
use GuzzleHttp\Promise\Utils;

/**
 * Example: Async/Concurrent Usage with Promises
 * 
 * This example demonstrates how to use the AsyncCourtListenerClient
 * to make concurrent API requests using Guzzle promises.
 */

try {
    // Initialize the async client
    $client = new AsyncCourtListenerClient([
        'api_token' => getenv('COURTLISTENER_API_TOKEN') ?: 'your_token_here',
    ]);

    echo "=== Async CourtListener Client Examples ===\n\n";

    // Example 1: Single async request
    echo "1. Single Async Request:\n";
    $promise = $client->getAsync('courts/', ['page' => 1]);
    
    $promise->then(
        function ($result) {
            echo "   Success! Retrieved " . count($result['results'] ?? []) . " courts\n";
        },
        function ($error) {
            echo "   Error: " . $error->getMessage() . "\n";
        }
    );
    
    // Wait for the promise to resolve
    $promise->wait();
    echo "\n";

    // Example 2: Multiple concurrent requests
    echo "2. Multiple Concurrent Requests:\n";
    $promises = [
        'courts' => $client->getAsync('courts/', ['page' => 1]),
        'dockets' => $client->getAsync('dockets/', ['page' => 1]),
        'opinions' => $client->getAsync('opinions/', ['page' => 1]),
    ];
    
    // Wait for all promises to resolve
    $results = Utils::unwrap($promises);
    
    echo "   Courts: " . count($results['courts']['results'] ?? []) . " items\n";
    echo "   Dockets: " . count($results['dockets']['results'] ?? []) . " items\n";
    echo "   Opinions: " . count($results['opinions']['results'] ?? []) . " items\n";
    echo "\n";

    // Example 3: Batch requests with makeRequestsBatch
    echo "3. Batch Requests:\n";
    $batchRequests = [
        ['method' => 'GET', 'endpoint' => 'courts/', 'options' => ['query' => ['page' => 1]]],
        ['method' => 'GET', 'endpoint' => 'dockets/', 'options' => ['query' => ['page' => 1]]],
        ['method' => 'GET', 'endpoint' => 'opinions/', 'options' => ['query' => ['page' => 1]]],
    ];
    
    $batchPromise = $client->makeRequestsBatch($batchRequests);
    $batchResults = $batchPromise->wait();
    
    foreach ($batchResults as $key => $result) {
        if ($result['state'] === 'fulfilled') {
            $count = count($result['value']['results'] ?? []);
            echo "   Request $key: Success - $count items\n";
        } else {
            echo "   Request $key: Failed\n";
        }
    }
    echo "\n";

    // Example 4: Chaining promises
    echo "4. Promise Chaining:\n";
    $client->getAsync('courts/', ['page' => 1])
        ->then(function ($result) {
            echo "   First request completed\n";
            return $result['results'][0] ?? null;
        })
        ->then(function ($firstCourt) use ($client) {
            if ($firstCourt) {
                echo "   Processing first court: " . ($firstCourt['short_name'] ?? 'Unknown') . "\n";
            }
        })
        ->wait();
    echo "\n";

    // Example 5: Error handling with promises
    echo "5. Error Handling:\n";
    $client->getAsync('nonexistent-endpoint/')
        ->then(
            function ($result) {
                echo "   Success\n";
            },
            function ($error) {
                echo "   Caught error: " . $error->getMessage() . "\n";
            }
        )
        ->wait();

    echo "\n=== Examples Complete ===\n";

} catch (\Exception $e) {
    echo "Fatal error: " . $e->getMessage() . "\n";
    exit(1);
}
