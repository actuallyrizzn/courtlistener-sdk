<?php

/**
 * Script to verify 100% API endpoint coverage
 */

require_once __DIR__ . '/vendor/autoload.php';

use CourtListener\CourtListenerClient;

echo "=== CourtListener PHP SDK - Endpoint Coverage Verification ===\n\n";

// Expected endpoints from Python SDK
$expectedEndpoints = [
    'search',
    'dockets', 
    'opinions',
    'judges',
    'courts',
    'audio',
    'clusters',
    'positions',
    'financial',
    'docket_entries',
    'attorneys',
    'parties',
    'documents',
    'citations',
    'recap_documents',
    'financial_disclosures',
    'investments',
    'non_investment_incomes',
    'agreements',
    'gifts',
    'reimbursements',
    'debts',
    'disclosure_positions',
    'spouse_incomes',
    'opinions_cited',
    'alerts',
    'docket_alerts',
    'people',
    'schools',
    'educations',
    'sources',
    'retention_events',
    'aba_ratings',
    'political_affiliations',
    'tag',
    'recap_fetch',
    'recap_query',
    'originating_court_information',
    'fjc_integrated_database'
];

echo "Expected endpoints: " . count($expectedEndpoints) . "\n\n";

try {
    // Initialize client (this will test all endpoint initialization)
    $client = new CourtListenerClient(['api_token' => 'test-token']);
    
    // Get all public properties (endpoints)
    $reflection = new ReflectionClass($client);
    $properties = $reflection->getProperties(ReflectionProperty::IS_PUBLIC);
    
    $actualEndpoints = [];
    foreach ($properties as $property) {
        if ($property->isPublic() && !$property->isStatic()) {
            $actualEndpoints[] = $property->getName();
        }
    }
    
    echo "Actual endpoints found: " . count($actualEndpoints) . "\n\n";
    
    // Check coverage
    $missing = array_diff($expectedEndpoints, $actualEndpoints);
    $extra = array_diff($actualEndpoints, $expectedEndpoints);
    
    if (empty($missing) && empty($extra)) {
        echo "✅ 100% COVERAGE ACHIEVED!\n";
        echo "All " . count($expectedEndpoints) . " expected endpoints are present.\n\n";
    } else {
        if (!empty($missing)) {
            echo "❌ Missing endpoints (" . count($missing) . "):\n";
            foreach ($missing as $endpoint) {
                echo "  - $endpoint\n";
            }
            echo "\n";
        }
        
        if (!empty($extra)) {
            echo "⚠️  Extra endpoints (" . count($extra) . "):\n";
            foreach ($extra as $endpoint) {
                echo "  - $endpoint\n";
            }
            echo "\n";
        }
    }
    
    // Test endpoint instantiation
    echo "Testing endpoint instantiation...\n";
    $workingEndpoints = 0;
    $failedEndpoints = [];
    
    foreach ($actualEndpoints as $endpoint) {
        try {
            $endpointInstance = $client->$endpoint;
            if (is_object($endpointInstance)) {
                $workingEndpoints++;
                echo "  ✅ $endpoint\n";
            } else {
                $failedEndpoints[] = $endpoint;
                echo "  ❌ $endpoint (not an object)\n";
            }
        } catch (Exception $e) {
            $failedEndpoints[] = $endpoint;
            echo "  ❌ $endpoint (error: " . $e->getMessage() . ")\n";
        }
    }
    
    echo "\nWorking endpoints: $workingEndpoints/" . count($actualEndpoints) . "\n";
    
    if (!empty($failedEndpoints)) {
        echo "Failed endpoints: " . implode(', ', $failedEndpoints) . "\n";
    }
    
    // Test basic functionality
    echo "\nTesting basic functionality...\n";
    try {
        // Test that endpoints have expected methods
        $testEndpoints = ['dockets', 'opinions', 'courts', 'judges'];
        foreach ($testEndpoints as $endpoint) {
            $instance = $client->$endpoint;
            $methods = get_class_methods($instance);
            $expectedMethods = ['list', 'get', 'search'];
            
            $hasExpectedMethods = true;
            foreach ($expectedMethods as $method) {
                if (!in_array($method . ucfirst($endpoint), $methods)) {
                    $hasExpectedMethods = false;
                    break;
                }
            }
            
            if ($hasExpectedMethods) {
                echo "  ✅ $endpoint has expected methods\n";
            } else {
                echo "  ❌ $endpoint missing expected methods\n";
            }
        }
    } catch (Exception $e) {
        echo "  ❌ Error testing functionality: " . $e->getMessage() . "\n";
    }
    
} catch (Exception $e) {
    echo "❌ Error initializing client: " . $e->getMessage() . "\n";
}

echo "\n=== Verification Complete ===\n";
