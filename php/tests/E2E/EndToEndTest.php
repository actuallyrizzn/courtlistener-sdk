<?php

namespace CourtListener\Tests\E2E;

use CourtListener\CourtListenerClient;
use CourtListener\Utils\Pagination;
use CourtListener\Utils\Filters;
use PHPUnit\Framework\TestCase;

/**
 * End-to-end tests for complete user scenarios
 * 
 * @group e2e
 * @group slow
 */
class EndToEndTest extends TestCase
{
    private CourtListenerClient $client;

    protected function setUp(): void
    {
        $this->client = new CourtListenerClient(['api_token' => 'test-token']);
    }

    public function testCompleteResearchWorkflow()
    {
        // Simulate a complete legal research workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: Search for cases by topic
        $searchResults = $this->client->search->search([
            'q' => 'intellectual property',
            'type' => 'o',
            'order_by' => '-date_filed'
        ]);
        
        $this->assertIsArray($searchResults);
        $this->assertArrayHasKey('count', $searchResults);
        $this->assertArrayHasKey('results', $searchResults);
        
        // Step 2: Get detailed opinion information
        if (!empty($searchResults['results'])) {
            $opinionId = $searchResults['results'][0]['id'];
            $opinion = $this->client->opinions->getOpinion($opinionId);
            
            $this->assertIsArray($opinion);
            $this->assertArrayHasKey('id', $opinion);
            
            // Step 3: Get related citations
            $citations = $this->client->opinions->getOpinionsCited($opinionId);
            $this->assertIsArray($citations);
            
            $citing = $this->client->opinions->getOpinionsCiting($opinionId);
            $this->assertIsArray($citing);
            
            // Step 4: Get cluster information
            $clusters = $this->client->opinions->getClusters($opinionId);
            $this->assertIsArray($clusters);
        }
    }

    public function testDocketAnalysisWorkflow()
    {
        // Simulate a complete docket analysis workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: Search for dockets by case type
        $dockets = $this->client->dockets->getDocketsByCaseType('Civil', [
            'per_page' => 5,
            'order_by' => '-date_filed'
        ]);
        
        $this->assertIsArray($dockets);
        $this->assertArrayHasKey('count', $dockets);
        $this->assertArrayHasKey('results', $dockets);
        
        if (!empty($dockets['results'])) {
            $docketId = $dockets['results'][0]['id'];
            
            // Step 2: Get detailed docket information
            $docket = $this->client->dockets->getDocket($docketId);
            $this->assertIsArray($docket);
            $this->assertArrayHasKey('id', $docket);
            
            // Step 3: Get docket entries
            $entries = $this->client->dockets->getDocketEntries($docketId);
            $this->assertIsArray($entries);
            
            // Step 4: Get parties
            $parties = $this->client->dockets->getParties($docketId);
            $this->assertIsArray($parties);
            
            // Step 5: Get attorneys
            $attorneys = $this->client->dockets->getAttorneys($docketId);
            $this->assertIsArray($attorneys);
            
            // Step 6: Get RECAP documents
            $recapDocs = $this->client->dockets->getRecapDocuments($docketId);
            $this->assertIsArray($recapDocs);
        }
    }

    public function testCourtResearchWorkflow()
    {
        // Simulate a complete court research workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: Get court hierarchy
        $hierarchy = $this->client->courts->getHierarchy();
        $this->assertIsArray($hierarchy);
        
        // Step 2: Get court types
        $types = $this->client->courts->getTypes();
        $this->assertIsArray($types);
        
        // Step 3: Search for specific courts
        $courts = $this->client->courts->searchCourts([
            'q' => 'federal',
            'per_page' => 10
        ]);
        
        $this->assertIsArray($courts);
        $this->assertArrayHasKey('count', $courts);
        $this->assertArrayHasKey('results', $courts);
        
        if (!empty($courts['results'])) {
            $courtId = $courts['results'][0]['id'];
            
            // Step 4: Get detailed court information
            $court = $this->client->courts->getCourt($courtId);
            $this->assertIsArray($court);
            $this->assertArrayHasKey('id', $court);
            
            // Step 5: Get dockets for this court
            $courtDockets = $this->client->dockets->getDocketsByCourt($courtId, [
                'per_page' => 5
            ]);
            $this->assertIsArray($courtDockets);
        }
    }

    public function testJudgeResearchWorkflow()
    {
        // Simulate a complete judge research workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: Search for judges
        $judges = $this->client->judges->searchJudges([
            'q' => 'Supreme Court',
            'per_page' => 10
        ]);
        
        $this->assertIsArray($judges);
        $this->assertArrayHasKey('count', $judges);
        $this->assertArrayHasKey('results', $judges);
        
        if (!empty($judges['results'])) {
            $judgeId = $judges['results'][0]['id'];
            
            // Step 2: Get detailed judge information
            $judge = $this->client->judges->getJudge($judgeId);
            $this->assertIsArray($judge);
            $this->assertArrayHasKey('id', $judge);
            
            // Step 3: Get opinions by this judge
            $opinions = $this->client->opinions->getOpinionsByJudge($judgeId, [
                'per_page' => 5
            ]);
            $this->assertIsArray($opinions);
            
            // Step 4: Get positions for this judge
            $positions = $this->client->positions->listPositions([
                'judge' => $judgeId,
                'per_page' => 5
            ]);
            $this->assertIsArray($positions);
        }
    }

    public function testFinancialDisclosureWorkflow()
    {
        // Simulate a complete financial disclosure research workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: Get financial disclosures
        $disclosures = $this->client->financialDisclosures->listFinancialDisclosures([
            'per_page' => 5
        ]);
        
        $this->assertIsArray($disclosures);
        $this->assertArrayHasKey('count', $disclosures);
        $this->assertArrayHasKey('results', $disclosures);
        
        if (!empty($disclosures['results'])) {
            $disclosureId = $disclosures['results'][0]['id'];
            
            // Step 2: Get detailed disclosure information
            $disclosure = $this->client->financialDisclosures->getFinancialDisclosure($disclosureId);
            $this->assertIsArray($disclosure);
            $this->assertArrayHasKey('id', $disclosure);
            
            // Step 3: Get related investments
            $investments = $this->client->investments->listInvestments([
                'financial_disclosure' => $disclosureId,
                'per_page' => 5
            ]);
            $this->assertIsArray($investments);
            
            // Step 4: Get related gifts
            $gifts = $this->client->gifts->listGifts([
                'financial_disclosure' => $disclosureId,
                'per_page' => 5
            ]);
            $this->assertIsArray($gifts);
            
            // Step 5: Get related debts
            $debts = $this->client->debts->listDebts([
                'financial_disclosure' => $disclosureId,
                'per_page' => 5
            ]);
            $this->assertIsArray($debts);
        }
    }

    public function testAlertManagementWorkflow()
    {
        // Simulate a complete alert management workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: List existing alerts
        $alerts = $this->client->alerts->listAlerts([
            'per_page' => 5
        ]);
        
        $this->assertIsArray($alerts);
        $this->assertArrayHasKey('count', $alerts);
        $this->assertArrayHasKey('results', $alerts);
        
        // Step 2: List docket alerts
        $docketAlerts = $this->client->docketAlerts->listDocketAlerts([
            'per_page' => 5
        ]);
        
        $this->assertIsArray($docketAlerts);
        $this->assertArrayHasKey('count', $docketAlerts);
        $this->assertArrayHasKey('results', $docketAlerts);
        
        // Note: Creating/updating/deleting alerts would require valid API token
        // and would be tested in live tests
    }

    public function testAdvancedSearchWorkflow()
    {
        // Simulate an advanced search workflow using filters
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: Build complex search filters
        $filters = array_merge(
            Filters::dateRange('2023-01-01', '2023-12-31'),
            Filters::contains('patent', 'case_name'),
            Filters::exact('federal', 'court_type'),
            Filters::orderBy('date_filed', 'desc'),
            Pagination::getParams(1, 10)
        );
        
        // Step 2: Search dockets with complex filters
        $dockets = $this->client->dockets->searchDockets($filters);
        $this->assertIsArray($dockets);
        $this->assertArrayHasKey('count', $dockets);
        $this->assertArrayHasKey('results', $dockets);
        
        // Step 3: Search opinions with complex filters
        $opinionFilters = array_merge(
            Filters::dateRange('2023-01-01', '2023-12-31'),
            Filters::textSearch('trademark'),
            Filters::exact('on', 'stat_Precedential'),
            Filters::orderBy('date_filed', 'desc'),
            Pagination::getParams(1, 10)
        );
        
        $opinions = $this->client->opinions->searchOpinions($opinionFilters);
        $this->assertIsArray($opinions);
        $this->assertArrayHasKey('count', $opinions);
        $this->assertArrayHasKey('results', $opinions);
    }

    public function testPaginationWorkflow()
    {
        // Simulate a pagination workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Step 1: Get first page
        $page1 = $this->client->dockets->listDockets(Pagination::getParams(1, 5));
        $this->assertIsArray($page1);
        $this->assertArrayHasKey('count', $page1);
        $this->assertArrayHasKey('results', $page1);
        $this->assertLessThanOrEqual(5, count($page1['results']));
        
        // Step 2: Get second page if available
        if (isset($page1['next']) && $page1['next']) {
            $page2 = $this->client->dockets->listDockets(Pagination::getParams(2, 5));
            $this->assertIsArray($page2);
            $this->assertArrayHasKey('count', $page2);
            $this->assertArrayHasKey('results', $page2);
            $this->assertEquals($page1['count'], $page2['count']);
        }
    }

    public function testErrorHandlingWorkflow()
    {
        // Simulate error handling scenarios
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Test that all exception classes are available
        $this->assertTrue(class_exists('CourtListener\Exceptions\CourtListenerException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\AuthenticationException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\RateLimitException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\NotFoundException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\ServerException'));
        
        // Test exception instantiation
        $exceptions = [
            new \CourtListener\Exceptions\CourtListenerException('Test'),
            new \CourtListener\Exceptions\AuthenticationException('Test'),
            new \CourtListener\Exceptions\RateLimitException('Test'),
            new \CourtListener\Exceptions\NotFoundException('Test'),
            new \CourtListener\Exceptions\ServerException('Test')
        ];
        
        foreach ($exceptions as $exception) {
            $this->assertInstanceOf(\Exception::class, $exception);
            $this->assertEquals('Test', $exception->getMessage());
        }
    }

    public function testModelWorkflow()
    {
        // Simulate model usage workflow
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Test BaseModel functionality
        $model = new \CourtListener\Models\BaseModel([
            'id' => 1,
            'name' => 'Test Case',
            'date_filed' => '2023-01-01',
            'active' => true
        ]);
        
        $this->assertEquals(1, $model->get('id'));
        $this->assertEquals('Test Case', $model->get('name'));
        $this->assertTrue($model->has('id'));
        $this->assertFalse($model->has('nonexistent'));
        
        // Test model modification
        $model->set('name', 'Modified Case');
        $this->assertEquals('Modified Case', $model->get('name'));
        $this->assertTrue($model->isDirty());
        
        // Test model reset
        $model->reset();
        $this->assertFalse($model->isDirty());
        $this->assertEquals('Test Case', $model->get('name'));
        
        // Test array access
        $this->assertEquals(1, $model['id']);
        $model['new_field'] = 'new_value';
        $this->assertEquals('new_value', $model['new_field']);
        
        // Test JSON serialization
        $json = json_encode($model);
        $this->assertIsString($json);
        $decoded = json_decode($json, true);
        $this->assertEquals(1, $decoded['id']);
    }
}
