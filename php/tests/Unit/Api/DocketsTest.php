<?php

namespace CourtListener\Tests\Unit\Api;

use CourtListener\Api\Dockets;
use CourtListener\CourtListenerClient;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;

class DocketsTest extends TestCase
{
    private Dockets $endpoint;
    private MockObject $client;

    protected function setUp(): void
    {
        $this->client = $this->createMock(CourtListenerClient::class);
        $this->endpoint = new Dockets($this->client);
    }

    public function testList()
    {
        $expectedResponse = [
            'count' => 100,
            'next' => 'http://api.example.com/dockets/?page=2',
            'previous' => null,
            'results' => [
                ['id' => 1, 'name' => 'Test Item 1'],
                ['id' => 2, 'name' => 'Test Item 2']
            ]
        ];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['page' => 1]])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->list(['page' => 1]);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGet()
    {
        $expectedResponse = ['id' => 123, 'name' => 'Test Item'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/123/', ['query' => []])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->get(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testSearch()
    {
        $expectedResponse = ['count' => 5, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/search/', ['query' => ['q' => 'test']])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->search(['q' => 'test']);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testCreate()
    {
        $data = ['name' => 'New Item', 'description' => 'Test Description'];
        $expectedResponse = ['id' => 456, 'name' => 'New Item', 'description' => 'Test Description'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('POST', 'dockets/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->create($data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testUpdate()
    {
        $data = ['name' => 'Updated Item'];
        $expectedResponse = ['id' => 123, 'name' => 'Updated Item'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('PUT', 'dockets/123/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->update(123, $data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testPatch()
    {
        $data = ['name' => 'Patched Item'];
        $expectedResponse = ['id' => 123, 'name' => 'Patched Item'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('PATCH', 'dockets/123/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->patch(123, $data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testDelete()
    {
        $expectedResponse = ['success' => true];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('DELETE', 'dockets/123/')
            ->willReturn($expectedResponse);

        $result = $this->endpoint->delete(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testListWithPagination()
    {
        $expectedResponse = [
            'count' => 200,
            'next' => 'http://api.example.com/dockets/?page=3',
            'previous' => 'http://api.example.com/dockets/?page=1',
            'results' => []
        ];

        $params = ['page' => 2, 'per_page' => 50];
        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => $params])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->list($params);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testListWithFilters()
    {
        $expectedResponse = ['count' => 10, 'results' => []];

        $filters = [
            'q' => 'search term',
            'date_created__gte' => '2023-01-01',
            'date_created__lte' => '2023-12-31',
            'ordering' => '-date_created'
        ];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => $filters])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->list($filters);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testSearchWithComplexFilters()
    {
        $expectedResponse = ['count' => 3, 'results' => []];

        $searchParams = [
            'q' => 'complex search',
            'type' => 'specific',
            'status' => 'active',
            'ordering' => 'name'
        ];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/search/', ['query' => $searchParams])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->search($searchParams);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetWithParams()
    {
        $expectedResponse = ['id' => 789, 'name' => 'Test Item'];

        $params = ['include' => 'related_data', 'format' => 'detailed'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/789/', ['query' => $params])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->get(789, $params);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testCreateWithValidation()
    {
        $data = ['name' => 'Valid Item'];
        $expectedResponse = ['id' => 999, 'name' => 'Valid Item'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('POST', 'dockets/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->create($data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testUpdateWithPartialData()
    {
        $data = ['description' => 'Updated description only'];
        $expectedResponse = ['id' => 123, 'name' => 'Original Name', 'description' => 'Updated description only'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('PUT', 'dockets/123/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->update(123, $data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testPatchWithMinimalData()
    {
        $data = ['status' => 'inactive'];
        $expectedResponse = ['id' => 123, 'status' => 'inactive'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('PATCH', 'dockets/123/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->patch(123, $data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testDeleteWithConfirmation()
    {
        $expectedResponse = ['success' => true, 'message' => 'Item deleted successfully'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('DELETE', 'dockets/123/')
            ->willReturn($expectedResponse);

        $result = $this->endpoint->delete(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testInheritsFromBaseApi()
    {
        $this->assertInstanceOf(\CourtListener\Api\BaseApi::class, $this->endpoint);
    }

    public function testHasRequiredMethods()
    {
        $this->assertTrue(method_exists($this->endpoint, 'list'));
        $this->assertTrue(method_exists($this->endpoint, 'get'));
        $this->assertTrue(method_exists($this->endpoint, 'create'));
        $this->assertTrue(method_exists($this->endpoint, 'update'));
        $this->assertTrue(method_exists($this->endpoint, 'patch'));
        $this->assertTrue(method_exists($this->endpoint, 'delete'));
        $this->assertTrue(method_exists($this->endpoint, 'search'));
    }

    public function testEndpointName()
    {
        $reflection = new \ReflectionClass($this->endpoint);
        $this->assertEquals('Dockets', $reflection->getShortName());
    }

    public function testClientInjection()
    {
        $reflection = new \ReflectionClass($this->endpoint);
        $clientProperty = $reflection->getProperty('client');
        $clientProperty->setAccessible(true);
        
        $injectedClient = $clientProperty->getValue($this->endpoint);
        $this->assertSame($this->client, $injectedClient);
    }

    /**
     * @dataProvider docketSubresourceProvider
     */
    public function testDocketSubresourceRequests(string $method, string $pathSegment)
    {
        $docketId = 555;
        $params = ['per_page' => 5];
        $expectedResponse = ['results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', "dockets/{$docketId}/{$pathSegment}/", ['query' => $params])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->{$method}($docketId, $params);
        $this->assertEquals($expectedResponse, $result);
    }

    /**
     * @dataProvider docketFilterProvider
     */
    public function testFilterHelpersMergeParameters(string $method, string $filterKey, string $filterValue)
    {
        $params = ['per_page' => 10];
        $expectedFilters = array_merge($params, [$filterKey => $filterValue]);
        $expectedResponse = ['count' => 0, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => $expectedFilters])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->{$method}($filterValue, $params);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsByDateRangeBuildsFilters()
    {
        $params = ['per_page' => 25];
        $expectedFilters = [
            'per_page' => 25,
            'date_filed__gte' => '2024-01-01',
            'date_filed__lte' => '2024-06-30',
            'court' => 'test-court'
        ];
        $expectedResponse = ['results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => $expectedFilters])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->getDocketsByDateRange('2024-01-01', '2024-06-30', 'test-court', $params);
        $this->assertEquals($expectedResponse, $result);
    }

    /**
     * @dataProvider docketToggleProvider
     */
    public function testToggleHelpersSetFlags(string $method, string $flagKey)
    {
        $params = ['per_page' => 5];
        $expectedFilters = array_merge($params, [$flagKey => 'true']);
        $expectedResponse = ['results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => $expectedFilters])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->{$method}($params);
        $this->assertEquals($expectedResponse, $result);
    }

    public function docketSubresourceProvider(): array
    {
        return [
            ['getDocketEntries', 'docket-entries'],
            ['getParties', 'parties'],
            ['getAttorneys', 'attorneys'],
            ['getRecapDocuments', 'recap'],
        ];
    }

    public function docketFilterProvider(): array
    {
        return [
            ['getDocketsByCourt', 'court', 'court-123'],
            ['getDocketsByCaseType', 'case_type', 'Civil'],
            ['getDocketsByNatureOfSuit', 'nature_of_suit', '890'],
            ['getDocketsByJudge', 'assigned_to', 'judge-99'],
            ['getDocketsByStatus', 'status', 'open'],
            ['getDocketsByJurisdictionType', 'jurisdiction_type', 'federal'],
            ['getDocketsByJuryDemand', 'jury_demand', 'jury'],
        ];
    }

    public function docketToggleProvider(): array
    {
        return [
            ['getDocketsWithFinancialDisclosures', 'has_financial_disclosures'],
            ['getDocketsWithAudio', 'has_audio'],
            ['getDocketsWithRecapDocuments', 'has_recap_documents'],
        ];
    }
}