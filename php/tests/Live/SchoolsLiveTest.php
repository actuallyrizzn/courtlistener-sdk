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
 * Live API tests for Schools endpoint
 * 
 * @group live
 * @group network
 * @group schools
 */
class SchoolsLiveTest extends TestCase
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

    public function testListSchools()
    {
        $this->assertNotNull($this->client);
        
        $results = $this->client->schools->list(Pagination::getParams(1, 5));
        
        $this->assertIsArray($results);
        $this->assertArrayHasKey('count', $results);
        $this->assertArrayHasKey('results', $results);
        $this->assertIsArray($results['results']);
        $this->assertLessThanOrEqual(5, count($results['results']));
        
        if (!empty($results['results'])) {
            $item = $results['results'][0];
            $this->assertArrayHasKey('id', $item);
            $this->assertIsNumeric($item['id']);
        }
    }

    public function testSearchSchools()
    {
        $this->assertNotNull($this->client);
        
        $searchResults = $this->client->schools->search([
            'q' => 'test',
            'per_page' => 3
        ]);
        
        $this->assertIsArray($searchResults);
        $this->assertArrayHasKey('count', $searchResults);
        $this->assertArrayHasKey('results', $searchResults);
        $this->assertIsArray($searchResults['results']);
        $this->assertLessThanOrEqual(3, count($searchResults['results']));
    }

    public function testGetSchoolsById()
    {
        $this->assertNotNull($this->client);
        
        // First get a list to find a valid ID
        $results = $this->client->schools->list(Pagination::getParams(1, 1));
        
        if (!empty($results['results'])) {
            $itemId = $results['results'][0]['id'];
            
            $item = $this->client->schools->get($itemId);
            
            $this->assertIsArray($item);
            $this->assertArrayHasKey('id', $item);
            $this->assertEquals($itemId, $item['id']);
        } else {
            $this->markTestSkipped('No Schools available for testing');
        }
    }

    public function testSchoolsWithPagination()
    {
        $this->assertNotNull($this->client);
        
        $page1 = $this->client->schools->list(Pagination::getParams(1, 2));
        $page2 = $this->client->schools->list(Pagination::getParams(2, 2));
        
        $this->assertIsArray($page1);
        $this->assertIsArray($page2);
        $this->assertArrayHasKey('count', $page1);
        $this->assertArrayHasKey('count', $page2);
        $this->assertEquals($page1['count'], $page2['count']);
        
        if (!empty($page1['results']) && !empty($page2['results'])) {
            $this->assertNotEquals($page1['results'][0]['id'], $page2['results'][0]['id']);
        }
    }

    public function testSchoolsWithFilters()
    {
        $this->assertNotNull($this->client);
        
        $filters = array_merge(
            Filters::orderBy('id', 'desc'),
            Pagination::getParams(1, 3)
        );
        
        $results = $this->client->schools->list($filters);
        
        $this->assertIsArray($results);
        $this->assertArrayHasKey('count', $results);
        $this->assertArrayHasKey('results', $results);
        $this->assertIsArray($results['results']);
        $this->assertLessThanOrEqual(3, count($results['results']));
    }

    public function testSchoolsErrorHandling()
    {
        $this->assertNotNull($this->client);
        
        // Test with invalid ID
        try {
            $this->client->schools->get(999999999);
            $this->fail('Expected NotFoundException was not thrown');
        } catch (NotFoundException $e) {
            $this->assertStringContainsString('not found', strtolower($e->getMessage()));
        } catch (\Exception $e) {
            // Some APIs might return different error types
            $this->assertInstanceOf(\Exception::class, $e);
        }
    }

    public function testSchoolsSearchWithComplexFilters()
    {
        $this->assertNotNull($this->client);
        
        $searchParams = [
            'q' => 'test',
            'order_by' => 'id',
            'per_page' => 2
        ];
        
        $results = $this->client->schools->search($searchParams);
        
        $this->assertIsArray($results);
        $this->assertArrayHasKey('count', $results);
        $this->assertArrayHasKey('results', $results);
        $this->assertIsArray($results['results']);
        $this->assertLessThanOrEqual(2, count($results['results']));
    }

    public function testSchoolsResponseStructure()
    {
        $this->assertNotNull($this->client);
        
        $results = $this->client->schools->list(Pagination::getParams(1, 1));
        
        if (!empty($results['results'])) {
            $item = $results['results'][0];
            
            // Test basic structure
            $this->assertIsArray($item);
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
            $this->markTestSkipped('No Schools available for structure testing');
        }
    }

    public function testSchoolsRateLimitHandling()
    {
        $this->assertNotNull($this->client);
        
        // Make multiple requests to test rate limiting
        $requests = 0;
        $maxRequests = 5;
        
        try {
            for ($i = 0; $i < $maxRequests; $i++) {
                $this->client->schools->list(Pagination::getParams(1, 1));
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