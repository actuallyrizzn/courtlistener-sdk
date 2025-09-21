<?php

namespace CourtListener\Tests\Unit\Api;

use CourtListener\Api\Sources;
use CourtListener\CourtListenerClient;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;

class SourcesTest extends TestCase
{
    private Sources $endpoint;
    private MockObject $client;

    protected function setUp(): void
    {
        $this->client = $this->createMock(CourtListenerClient::class);
        $this->endpoint = new Sources($this->client);
    }

    public function testList()
    {
        $expectedResponse = [
            'count' => 100,
            'next' => 'http://api.example.com/sources/?page=2',
            'previous' => null,
            'results' => [
                ['id' => 1, 'name' => 'Test Item 1'],
                ['id' => 2, 'name' => 'Test Item 2']
            ]
        ];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'sources/', ['query' => ['page' => 1]])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->list(['page' => 1]);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGet()
    {
        $expectedResponse = ['id' => 123, 'name' => 'Test Item'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'sources/123/', ['query' => []])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->get(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testSearch()
    {
        $expectedResponse = ['count' => 5, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'sources/search/', ['query' => ['q' => 'test']])
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
            ->with('POST', 'sources/', ['json' => $data])
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
            ->with('PUT', 'sources/123/', ['json' => $data])
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
            ->with('PATCH', 'sources/123/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->patch(123, $data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testDelete()
    {
        $expectedResponse = ['success' => true];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('DELETE', 'sources/123/')
            ->willReturn($expectedResponse);

        $result = $this->endpoint->delete(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testListWithPagination()
    {
        $expectedResponse = [
            'count' => 200,
            'next' => 'http://api.example.com/sources/?page=3',
            'previous' => 'http://api.example.com/sources/?page=1',
            'results' => []
        ];

        $params = ['page' => 2, 'per_page' => 50];
        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'sources/', ['query' => $params])
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
            ->with('GET', 'sources/', ['query' => $filters])
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
            ->with('GET', 'sources/search/', ['query' => $searchParams])
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
            ->with('GET', 'sources/789/', ['query' => $params])
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
            ->with('POST', 'sources/', ['json' => $data])
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
            ->with('PUT', 'sources/123/', ['json' => $data])
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
            ->with('PATCH', 'sources/123/', ['json' => $data])
            ->willReturn($expectedResponse);

        $result = $this->endpoint->patch(123, $data);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testDeleteWithConfirmation()
    {
        $expectedResponse = ['success' => true, 'message' => 'Item deleted successfully'];

        $params = ['confirm' => 'true'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('DELETE', 'sources/123/')
            ->willReturn($expectedResponse);

        $result = $this->endpoint->delete(123, $params);
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
        $this->assertEquals('Sources', $reflection->getShortName());
    }

    public function testClientInjection()
    {
        $reflection = new \ReflectionClass($this->endpoint);
        $clientProperty = $reflection->getProperty('client');
        $clientProperty->setAccessible(true);
        
        $injectedClient = $clientProperty->getValue($this->endpoint);
        $this->assertSame($this->client, $injectedClient);
    }
}