<?php

require_once 'vendor/autoload.php';

use CourtListener\CourtListenerClient;

try {
    $client = new CourtListenerClient(['api_token' => 'test-token', 'verify_ssl' => false]);
    
    echo "Testing ABA Ratings endpoint...\n";
    $response = $client->abaRatings->list(['page' => 1, 'per_page' => 5]);
    
    echo "Response type: " . gettype($response) . "\n";
    echo "Response length: " . strlen($response) . "\n";
    echo "Response content: " . var_export($response, true) . "\n";
    
    if (is_string($response)) {
        echo "Response is string, trying to decode JSON...\n";
        $decoded = json_decode($response, true);
        if (json_last_error() === JSON_ERROR_NONE) {
            echo "JSON decode successful: " . var_export($decoded, true) . "\n";
        } else {
            echo "JSON decode failed: " . json_last_error_msg() . "\n";
        }
    }
    
} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}
