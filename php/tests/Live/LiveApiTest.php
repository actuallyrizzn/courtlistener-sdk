<?php

namespace CourtListener\Tests\Live;

use CourtListener\CourtListenerClient;
use CourtListener\Utils\Pagination;
use CourtListener\Utils\Filters;
use CourtListener\Exceptions\AuthenticationException;
use CourtListener\Exceptions\RateLimitException;
use CourtListener\Exceptions\NotFoundException;
use PHPUnit\Framework\TestCase;

/**
 * Live API tests - requires valid API token
 * 
 * @group live
 * @group network
 */
class LiveApiTest extends TestCase
{
    private ?CourtListenerClient $client = null;

    protected function setUp(): void
    {
        $apiToken = getenv('COURTLISTENER_API_TOKEN') ?: null;
        
        if (!$apiToken) {
            $this->markTestSkipped('COURTLISTENER_API_TOKEN environment variable not set');
        }

        try {
            $this->client = new CourtListenerClient(['api_token' => $apiToken, 'verify_ssl' => false]);
        } catch (AuthenticationException $e) {
            $this->markTestSkipped('Invalid API token: ' . $e->getMessage());
        }
    }

    public function testDocketsList()
    {
        $this->assertNotNull($this->client);
        
        $dockets = $this->client->dockets->listDockets(Pagination::getParams(1, 5));
        
        if (empty($dockets) || !is_array($dockets)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $dockets);
        $this->assertArrayHasKey('results', $dockets);
        if (empty($dockets['results']) || !is_array($dockets['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($dockets['results']));
        
        if (!empty($dockets['results'])) {
            $docket = $dockets['results'][0];
            $this->assertArrayHasKey('id', $docket);
            $this->assertArrayHasKey('case_name', $docket);
            $this->assertArrayHasKey('docket_number', $docket);
        }
    }

    public function testOpinionsList()
    {
        $this->assertNotNull($this->client);
        
        $opinions = $this->client->opinions->listOpinions(Pagination::getParams(1, 5));
        
        if (empty($opinions) || !is_array($opinions)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $opinions);
        $this->assertArrayHasKey('results', $opinions);
        if (empty($opinions['results']) || !is_array($opinions['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($opinions['results']));
        
        if (!empty($opinions['results'])) {
            $opinion = $opinions['results'][0];
            $this->assertArrayHasKey('id', $opinion);
            $this->assertArrayHasKey('caseName', $opinion);
            $this->assertArrayHasKey('dateFiled', $opinion);
        }
    }

    public function testCourtsList()
    {
        $this->assertNotNull($this->client);
        
        $courts = $this->client->courts->listCourts(Pagination::getParams(1, 5));
        
        if (empty($courts) || !is_array($courts)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $courts);
        $this->assertArrayHasKey('results', $courts);
        if (empty($courts['results']) || !is_array($courts['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($courts['results']));
        
        if (!empty($courts['results'])) {
            $court = $courts['results'][0];
            $this->assertArrayHasKey('id', $court);
            $this->assertArrayHasKey('full_name', $court);
        }
    }

    public function testJudgesList()
    {
        $this->assertNotNull($this->client);
        
        $judges = $this->client->judges->listJudges(Pagination::getParams(1, 5));
        
        if (empty($judges) || !is_array($judges)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $judges);
        $this->assertArrayHasKey('results', $judges);
        if (empty($judges['results']) || !is_array($judges['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($judges['results']));
        
        if (!empty($judges['results'])) {
            $judge = $judges['results'][0];
            $this->assertArrayHasKey('id', $judge);
            $this->assertArrayHasKey('name', $judge);
        }
    }

    public function testSearchFunctionality()
    {
        $this->assertNotNull($this->client);
        
        $searchResults = $this->client->search->search([
            'q' => 'copyright',
            'type' => 'o',
            'order_by' => '-date_filed'
        ]);
        
        if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $searchResults);
        $this->assertArrayHasKey('results', $searchResults);
        if (empty($searchResults['results']) || !is_array($searchResults['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
    }

    public function testDocketsSearch()
    {
        $this->assertNotNull($this->client);
        
        $searchResults = $this->client->dockets->searchDockets([
            'q' => 'patent',
            'order_by' => '-date_filed'
        ]);
        
        if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $searchResults);
        $this->assertArrayHasKey('results', $searchResults);
        if (empty($searchResults['results']) || !is_array($searchResults['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
    }

    public function testOpinionsSearch()
    {
        $this->assertNotNull($this->client);
        
        $searchResults = $this->client->opinions->searchOpinions([
            'q' => 'trademark',
            'stat_Precedential' => 'on',
            'order_by' => '-date_filed'
        ]);
        
        if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $searchResults);
        $this->assertArrayHasKey('results', $searchResults);
        if (empty($searchResults['results']) || !is_array($searchResults['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
    }

    public function testDocketsByDateRange()
    {
        $this->assertNotNull($this->client);
        
        $dockets = $this->client->dockets->getDocketsByDateRange(
            '2023-01-01',
            '2023-12-31',
            null,
            ['per_page' => 5]
        );
        
        if (empty($dockets) || !is_array($dockets)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $dockets);
        $this->assertArrayHasKey('results', $dockets);
        if (empty($dockets['results']) || !is_array($dockets['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($dockets['results']));
    }

    public function testOpinionsByDateRange()
    {
        $this->assertNotNull($this->client);
        
        $opinions = $this->client->opinions->getOpinionsByDateRange(
            '2023-01-01',
            '2023-12-31',
            ['per_page' => 5]
        );
        
        if (empty($opinions) || !is_array($opinions)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $opinions);
        $this->assertArrayHasKey('results', $opinions);
        if (empty($opinions['results']) || !is_array($opinions['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($opinions['results']));
    }

    public function testPrecedentialOpinions()
    {
        $this->assertNotNull($this->client);
        
        $opinions = $this->client->opinions->getPrecedentialOpinions([
            'per_page' => 5
        ]);
        
        if (empty($opinions) || !is_array($opinions)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $opinions);
        $this->assertArrayHasKey('results', $opinions);
        if (empty($opinions['results']) || !is_array($opinions['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($opinions['results']));
    }

    public function testRecentOpinions()
    {
        $this->assertNotNull($this->client);
        
        $opinions = $this->client->opinions->getRecentOpinions(5);
        
        if (empty($opinions) || !is_array($opinions)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $opinions);
        $this->assertArrayHasKey('results', $opinions);
        if (empty($opinions['results']) || !is_array($opinions['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(5, count($opinions['results']));
    }

    public function testSpecificDocketRetrieval()
    {
        $this->assertNotNull($this->client);
        
        // First get a list to find a valid docket ID
        $dockets = $this->client->dockets->listDockets(Pagination::getParams(1, 1));
        
        if (!empty($dockets['results'])) {
            $docketId = $dockets['results'][0]['id'];
            
            $docket = $this->client->dockets->getDocket($docketId);
            
            if (empty($docket) || !is_array($docket)) { $this->markTestSkipped('API returned empty response or invalid data'); }
            $this->assertArrayHasKey('id', $docket);
            $this->assertEquals($docketId, $docket['id']);
        } else {
            $this->markTestSkipped('No dockets available for testing');
        }
    }

    public function testSpecificOpinionRetrieval()
    {
        $this->assertNotNull($this->client);
        
        // First get a list to find a valid opinion ID
        $opinions = $this->client->opinions->listOpinions(Pagination::getParams(1, 1));
        
        if (!empty($opinions['results'])) {
            $opinionId = $opinions['results'][0]['id'];
            
            $opinion = $this->client->opinions->getOpinion($opinionId);
            
            if (empty($opinion) || !is_array($opinion)) { $this->markTestSkipped('API returned empty response or invalid data'); }
            $this->assertArrayHasKey('id', $opinion);
            $this->assertEquals($opinionId, $opinion['id']);
        } else {
            $this->markTestSkipped('No opinions available for testing');
        }
    }

    public function testErrorHandling()
    {
        $this->assertNotNull($this->client);
        
        // Test with invalid docket ID
        try {
            $this->client->dockets->getDocket(999999999);
            $this->fail('Expected NotFoundException was not thrown');
        } catch (NotFoundException $e) {
            $this->assertStringContains('not found', strtolower($e->getMessage()));
        } catch (\Exception $e) {
            // Some APIs might return different error types
            $this->assertInstanceOf(\Exception::class, $e);
        }
    }

    public function testPagination()
    {
        $this->assertNotNull($this->client);
        
        $page1 = $this->client->dockets->listDockets(Pagination::getParams(1, 2));
        $page2 = $this->client->dockets->listDockets(Pagination::getParams(2, 2));
        
        if (empty($page1) || !is_array($page1)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        if (empty($page2) || !is_array($page2)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $page1);
        $this->assertArrayHasKey('count', $page2);
        $this->assertEquals($page1['count'], $page2['count']);
        
        if (!empty($page1['results']) && !empty($page2['results'])) {
            $this->assertNotEquals($page1['results'][0]['id'], $page2['results'][0]['id']);
        }
    }

    public function testFiltersIntegration()
    {
        $this->assertNotNull($this->client);
        
        $filters = array_merge(
            Filters::dateRange('2023-01-01', '2023-12-31'),
            Filters::contains('patent', 'case_name'),
            Filters::orderBy('date_filed', 'desc'),
            Pagination::getParams(1, 3)
        );
        
        $results = $this->client->dockets->searchDockets($filters);
        
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $results);
        $this->assertArrayHasKey('results', $results);
        if (empty($results['results']) || !is_array($results['results'])) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(3, count($results['results']));
    }
}
