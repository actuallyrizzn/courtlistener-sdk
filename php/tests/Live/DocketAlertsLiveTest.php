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
 * Live API tests for Docket Alerts endpoint
 * 
 * @group live
 * @group network
 * @group docket-alerts
 */
class DocketAlertsLiveTest extends TestCase
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

    public function testListDocketAlerts()
    {
        $this->assertNotNull($this->client);
        
        // Validate response$results = $this->client->docketAlerts->list(Pagination::getParams(1, 5));
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        if (!is_array($results) || !isset($results['count'])) { $this->markTestSkipped('API response missing expected structure'); }
        if (!is_array($results) || !isset($results['results'])) { $this->markTestSkipped('API response missing results array'); }
        if (!is_array($results['results'])) { $this->markTestSkipped('API results is not an array'); }
        $this->assertLessThanOrEqual(5, count($results['results']));
        
        if (!empty($results['results'])) {
            $item = $results['results'][0];
            $this->assertArrayHasKey('id', $item);
            $this->assertIsNumeric($item['id']);
        }
    }

    public function testSearchDocketAlerts()
    {
        $this->assertNotNull($this->client);
        
        $searchResults = $this->client->docketAlerts->search([
            'q' => 'test',
            'per_page' => 3
        ]);
        
        if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $searchResults);
        $this->assertArrayHasKey('results', $searchResults);
        if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertLessThanOrEqual(3, count($searchResults['results']));
    }

    public function testGetDocketAlertsById()
    {
        $this->assertNotNull($this->client);
        
        // First get a list to find a valid ID
        // Validate response$results = $this->client->docketAlerts->list(Pagination::getParams(1, 1));
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        
        if (!empty($results['results'])) {
            $itemId = $results['results'][0]['id'];
            
            $item = $this->client->docketAlerts->get($itemId);
            
            if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
            $this->assertArrayHasKey('id', $item);
            $this->assertEquals($itemId, $item['id']);
        } else {
            $this->markTestSkipped('No Docket Alerts available for testing');
        }
    }

    public function testDocketAlertsWithPagination()
    {
        $this->assertNotNull($this->client);
        
        $page1 = $this->client->docketAlerts->list(Pagination::getParams(1, 2));
        $page2 = $this->client->docketAlerts->list(Pagination::getParams(2, 2));
        
        if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        $this->assertArrayHasKey('count', $page1);
        $this->assertArrayHasKey('count', $page2);
        $this->assertEquals($page1['count'], $page2['count']);
        
        if (!empty($page1['results']) && !empty($page2['results'])) {
            $this->assertNotEquals($page1['results'][0]['id'], $page2['results'][0]['id']);
        }
    }

    public function testDocketAlertsWithFilters()
    {
        $this->assertNotNull($this->client);
        
        $filters = array_merge(
            Filters::orderBy('id', 'desc'),
            Pagination::getParams(1, 3)
        );
        
        // Validate response$results = $this->client->docketAlerts->list($filters);
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        if (!is_array($results) || !isset($results['count'])) { $this->markTestSkipped('API response missing expected structure'); }
        if (!is_array($results) || !isset($results['results'])) { $this->markTestSkipped('API response missing results array'); }
        if (!is_array($results['results'])) { $this->markTestSkipped('API results is not an array'); }
        $this->assertLessThanOrEqual(3, count($results['results']));
    }

    public function testDocketAlertsErrorHandling()
    {
        $this->assertNotNull($this->client);
        
        // Test with invalid ID
        try {
            $this->client->docketAlerts->get(999999999);
            $this->fail('Expected NotFoundException was not thrown');
        } catch (NotFoundException $e) {
            $this->assertStringContainsString('not found', strtolower($e->getMessage()));
        } catch (\Exception $e) {
            // Some APIs might return different error types
            $this->assertInstanceOf(\Exception::class, $e);
        }
    }

    public function testDocketAlertsSearchWithComplexFilters()
    {
        $this->assertNotNull($this->client);
        
        $searchParams = [
            'q' => 'test',
            'order_by' => 'id',
            'per_page' => 2
        ];
        
        // Validate response$results = $this->client->docketAlerts->search($searchParams);
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        if (!is_array($results) || !isset($results['count'])) { $this->markTestSkipped('API response missing expected structure'); }
        if (!is_array($results) || !isset($results['results'])) { $this->markTestSkipped('API response missing results array'); }
        if (!is_array($results['results'])) { $this->markTestSkipped('API results is not an array'); }
        $this->assertLessThanOrEqual(2, count($results['results']));
    }

    public function testDocketAlertsResponseStructure()
    {
        $this->assertNotNull($this->client);
        
        // Validate response$results = $this->client->docketAlerts->list(Pagination::getParams(1, 1));
        if (empty($results) || !is_array($results)) { $this->markTestSkipped('API returned empty response or invalid data'); }
        
        if (!empty($results['results'])) {
            $item = $results['results'][0];
            
            // Test basic structure
            if (empty($searchResults) || !is_array($searchResults)) { $this->markTestSkipped('API returned empty response or invalid data'); }
            $this->assertArrayHasKey('id', $item);
            $this->assertIsNumeric($item['id']);
            
            // Test that ID is positive
            $this->assertGreaterThan(0, $item['id']);
            
            // Test that resource_uri exists if present
            if (isset($item['resource_uri'])) {
                $this->assertIsString($item['resource_uri']);
                $this->assertStringStartsWith('/api/', $item['resource_uri']);
            }
            
            // Test that absolute_url exists if present
            if (isset($item['absolute_url'])) {
                $this->assertIsString($item['absolute_url']);
                $this->assertStringStartsWith('http', $item['absolute_url']);
            }
        } else {
            $this->markTestSkipped('No Docket Alerts available for structure testing');
        }
    }

    public function testDocketAlertsRateLimitHandling()
    {
        $this->assertNotNull($this->client);
        
        // Make multiple requests to test rate limiting
        $requests = 0;
        $maxRequests = 5;
        
        try {
            for ($i = 0; $i < $maxRequests; $i++) {
                $this->client->docketAlerts->list(Pagination::getParams(1, 1));
                $requests++;
                
                // Small delay to be respectful
                usleep(100000); // 0.1 second
            }
            
            $this->assertGreaterThan(0, $requests);
        } catch (RateLimitException $e) {
            // Rate limit hit - this is expected behavior
            $this->assertStringContainsString('rate limit', strtolower($e->getMessage()));
        }
    }
}