<?php

require_once __DIR__ . '/../vendor/autoload.php';

use CourtListener\CourtListenerClient;
use CourtListener\Utils\Pagination;
use CourtListener\Utils\Filters;

// Initialize the client
$client = new CourtListenerClient();

echo "=== CourtListener PHP SDK - Advanced Usage Examples ===\n\n";

try {
    // Example 1: Pagination handling
    echo "1. Pagination example:\n";
    $page = 1;
    $allDockets = [];
    
    do {
        $dockets = $client->dockets->listDockets(Pagination::getParams($page, 10));
        $allDockets = array_merge($allDockets, $dockets['results']);
        
        echo "Page {$page}: " . count($dockets['results']) . " dockets\n";
        $page++;
        
        // Limit to first 3 pages for demo
    } while ($dockets['next'] && $page <= 3);
    
    echo "Total collected: " . count($allDockets) . " dockets\n\n";

    // Example 2: Complex search with multiple filters
    echo "2. Complex search:\n";
    $searchParams = array_merge(
        Filters::dateRange('2023-01-01', '2023-12-31'),
        Filters::contains('trademark', 'case_name'),
        Filters::exact('federal', 'court_type'),
        Filters::orderBy('date_filed', 'desc'),
        Pagination::getParams(1, 5)
    );
    
    $results = $client->dockets->searchDockets($searchParams);
    echo "Complex search found {$results['count']} results\n";
    foreach ($results['results'] as $docket) {
        echo "- {$docket['case_name']} ({$docket['court_name']})\n";
    }
    echo "\n";

    // Example 3: Working with specific docket details
    echo "3. Docket details:\n";
    if (!empty($results['results'])) {
        $docketId = $results['results'][0]['id'];
        $docket = $client->dockets->getDocket($docketId);
        
        echo "Docket ID: {$docket['id']}\n";
        echo "Case Name: {$docket['case_name']}\n";
        echo "Court: {$docket['court_name']}\n";
        echo "Date Filed: {$docket['date_filed']}\n";
        echo "Case Type: {$docket['case_type_name']}\n";
        
        // Get docket entries
        $entries = $client->dockets->getDocketEntries($docketId, ['per_page' => 3]);
        echo "Docket Entries: {$entries['count']} total\n";
        foreach ($entries['results'] as $entry) {
            echo "  - {$entry['entry_number']}: {$entry['description']}\n";
        }
    }
    echo "\n";

    // Example 4: Opinion analysis
    echo "4. Opinion analysis:\n";
    $opinions = $client->opinions->searchOpinions([
        'q' => 'artificial intelligence',
        'stat_Precedential' => 'on',
        'order_by' => '-date_filed'
    ]);
    
    echo "Found {$opinions['count']} AI-related precedential opinions\n";
    foreach (array_slice($opinions['results'], 0, 2) as $opinion) {
        echo "- {$opinion['caseName']}\n";
        echo "  Court: {$opinion['court']}\n";
        echo "  Date: {$opinion['dateFiled']}\n";
        echo "  Type: {$opinion['type']}\n";
        
        // Get citations
        $citations = $client->opinions->getOpinionsCited($opinion['id']);
        echo "  Citations: {$citations['count']} opinions cited\n";
    }
    echo "\n";

    // Example 5: Error handling
    echo "5. Error handling example:\n";
    try {
        $client->dockets->getDocket(999999999); // Non-existent ID
    } catch (Exception $e) {
        echo "Caught expected error: " . $e->getMessage() . "\n";
    }

} catch (Exception $e) {
    echo "Unexpected error: " . $e->getMessage() . "\n";
}

echo "\n=== Advanced Examples Complete ===\n";
