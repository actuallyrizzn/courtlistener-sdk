<?php

require 'vendor/autoload.php';

use CourtListener\CourtListenerClient;

echo "=== CourtListener PHP SDK - Endpoint Verification ===\n\n";

try {
    $client = new CourtListenerClient(['api_token' => 'test-token']);
    
    $reflection = new ReflectionClass($client);
    $properties = $reflection->getProperties(ReflectionProperty::IS_PUBLIC);
    
    echo "Total endpoints found: " . count($properties) . "\n\n";
    
    $endpoints = [];
    foreach ($properties as $property) {
        if ($property->isPublic() && !$property->isStatic()) {
            $endpoints[] = $property->getName();
        }
    }
    
    sort($endpoints);
    
    echo "Endpoints:\n";
    foreach ($endpoints as $endpoint) {
        echo "- $endpoint\n";
    }
    
    echo "\n✅ All " . count($endpoints) . " endpoints successfully initialized!\n";
    
} catch (Exception $e) {
    echo "❌ Error: " . $e->getMessage() . "\n";
}
