<?php

require_once __DIR__ . '/../vendor/autoload.php';

use CourtListener\CourtListenerClient;
use CourtListener\Utils\Pagination;
use CourtListener\Utils\Filters;

// Initialize the client
$client = new CourtListenerClient();

echo "=== CourtListener PHP SDK - Basic Usage Examples ===\n\n";

try {
    // Example 1: List dockets
    echo "1. Listing recent dockets:\n";
    $dockets = $client->dockets->listDockets(Pagination::getParams(1, 5));
    
    echo "Found {$dockets['count']} total dockets\n";
    foreach ($dockets['results'] as $docket) {
        echo "- {$docket['case_name']} ({$docket['docket_number']})\n";
    }
    echo "\n";

    // Example 2: Search opinions
    echo "2. Searching opinions:\n";
    $opinions = $client->opinions->searchOpinions([
        'q' => 'copyright',
        'order_by' => '-date_filed',
        'stat_Precedential' => 'on'
    ]);
    
    echo "Found {$opinions['count']} opinions matching 'copyright'\n";
    foreach (array_slice($opinions['results'], 0, 3) as $opinion) {
        echo "- {$opinion['caseName']} ({$opinion['dateFiled']})\n";
    }
    echo "\n";

    // Example 3: Get specific court
    echo "3. Getting court information:\n";
    $courts = $client->courts->listCourts(['per_page' => 1]);
    if (!empty($courts['results'])) {
        $court = $courts['results'][0];
        echo "Court: {$court['full_name']} ({$court['id']})\n";
        echo "Jurisdiction: {$court['jurisdiction']}\n";
    }
    echo "\n";

    // Example 4: List judges
    echo "4. Listing judges:\n";
    $judges = $client->judges->listJudges(Pagination::getParams(1, 3));
    
    echo "Found {$judges['count']} judges\n";
    foreach ($judges['results'] as $judge) {
        echo "- {$judge['name']} ({$judge['id']})\n";
    }
    echo "\n";

    // Example 5: Search with filters
    echo "5. Advanced search with filters:\n";
    $filters = array_merge(
        Filters::dateRange('2023-01-01', '2023-12-31', 'date_filed'),
        Filters::contains('patent', 'case_name'),
        Filters::orderBy('date_filed', 'desc')
    );
    
    $filteredDockets = $client->dockets->searchDockets($filters);
    echo "Found {$filteredDockets['count']} dockets with 'patent' in case name from 2023\n";
    foreach (array_slice($filteredDockets['results'], 0, 2) as $docket) {
        echo "- {$docket['case_name']} ({$docket['date_filed']})\n";
    }

} catch (Exception $e) {
    echo "Error: " . $e->getMessage() . "\n";
}

echo "\n=== Examples Complete ===\n";
