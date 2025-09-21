<?php

namespace CourtListener\Tests\Unit;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\AuthenticationException;
use CourtListener\Exceptions\RateLimitException;
use CourtListener\Exceptions\NotFoundException;
use CourtListener\Exceptions\ServerException;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;
use GuzzleHttp\Client;
use GuzzleHttp\Psr7\Response;
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Exception\ConnectException;
use GuzzleHttp\Exception\ClientException;
use GuzzleHttp\Exception\ServerException as GuzzleServerException;

class CourtListenerClientComprehensiveTest extends TestCase
{
    private CourtListenerClient $client;
    private MockObject $mockHttpClient;

    protected function setUp(): void
    {
        $this->mockHttpClient = $this->createMock(Client::class);
        $this->client = new CourtListenerClient(['api_token' => 'test-token']);
        
        // Use reflection to inject the mock HTTP client
        $reflection = new \ReflectionClass($this->client);
        $clientProperty = $reflection->getProperty('httpClient');
        $clientProperty->setAccessible(true);
        $clientProperty->setValue($this->client, $this->mockHttpClient);
    }

    public function testClientInitializationWithAllParameters()
    {
        $config = [
            'api_token' => 'test-token',
            'base_url' => 'https://custom.example.com/api/',
            'timeout' => 60,
            'max_retries' => 5,
            'retry_delay' => 2.0
        ];

        $client = new CourtListenerClient($config);
        
        $this->assertEquals('test-token', $client->getApiToken());
        $this->assertEquals('https://custom.example.com/api/', $client->getBaseUrl());
    }

    public function testClientInitializationWithEnvironmentVariables()
    {
        // Temporarily set environment variables
        $originalToken = $_ENV['COURTLISTENER_API_TOKEN'] ?? null;
        $originalUrl = $_ENV['COURTLISTENER_BASE_URL'] ?? null;
        
        $_ENV['COURTLISTENER_API_TOKEN'] = 'env-token';
        $_ENV['COURTLISTENER_BASE_URL'] = 'https://env.example.com/api/';
        
        $client = new CourtListenerClient();
        
        $this->assertEquals('env-token', $client->getApiToken());
        $this->assertEquals('https://env.example.com/api/', $client->getBaseUrl());
        
        // Restore original values
        if ($originalToken !== null) {
            $_ENV['COURTLISTENER_API_TOKEN'] = $originalToken;
        } else {
            unset($_ENV['COURTLISTENER_API_TOKEN']);
        }
        
        if ($originalUrl !== null) {
            $_ENV['COURTLISTENER_BASE_URL'] = $originalUrl;
        } else {
            unset($_ENV['COURTLISTENER_BASE_URL']);
        }
    }

    public function testMakeRequestGetSuccess()
    {
        $expectedResponse = ['id' => 123, 'name' => 'Test'];
        $mockResponse = new Response(200, [], json_encode($expectedResponse));

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->with('GET', 'test/', ['query' => ['page' => 1]])
            ->willReturn($mockResponse);

        $result = $this->client->makeRequest('GET', 'test/', ['query' => ['page' => 1]]);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testMakeRequestPostSuccess()
    {
        $data = ['name' => 'New Item'];
        $expectedResponse = ['id' => 456, 'name' => 'New Item'];
        $mockResponse = new Response(201, [], json_encode($expectedResponse));

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->with('POST', 'test/', ['json' => $data])
            ->willReturn($mockResponse);

        $result = $this->client->makeRequest('POST', 'test/', ['json' => $data]);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testMakeRequestWithCustomHeaders()
    {
        $expectedResponse = ['id' => 789];
        $mockResponse = new Response(200, [], json_encode($expectedResponse));

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->with('GET', 'test/', [
                'headers' => ['Custom-Header' => 'custom-value']
            ])
            ->willReturn($mockResponse);

        $result = $this->client->makeRequest('GET', 'test/', [
            'headers' => ['Custom-Header' => 'custom-value']
        ]);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testMakeRequestWithRetryOnConnectionError()
    {
        $expectedResponse = ['id' => 999];
        $mockResponse = new Response(200, [], json_encode($expectedResponse));

        $this->mockHttpClient->expects($this->exactly(3))
            ->method('request')
            ->willReturnCallback(function () use ($mockResponse) {
                static $callCount = 0;
                $callCount++;
                
                if ($callCount < 3) {
                    throw new ConnectException('Connection failed', $this->createMock(\Psr\Http\Message\RequestInterface::class));
                }
                
                return $mockResponse;
            });

        $result = $this->client->makeRequest('GET', 'test/');
        $this->assertEquals($expectedResponse, $result);
    }

    public function testMakeRequestWithRetryOnServerError()
    {
        $expectedResponse = ['id' => 888];
        $mockResponse = new Response(200, [], json_encode($expectedResponse));

        $this->mockHttpClient->expects($this->exactly(3))
            ->method('request')
            ->willReturnCallback(function () use ($mockResponse) {
                static $callCount = 0;
                $callCount++;
                
                if ($callCount < 3) {
                    throw new GuzzleServerException('Server error', $this->createMock(\Psr\Http\Message\RequestInterface::class), $mockResponse);
                }
                
                return $mockResponse;
            });

        $result = $this->client->makeRequest('GET', 'test/');
        $this->assertEquals($expectedResponse, $result);
    }

    public function testMakeRequestMaxRetriesExceeded()
    {
        $this->mockHttpClient->expects($this->exactly(3))
            ->method('request')
            ->willThrowException(new ConnectException('Connection failed', $this->createMock(\Psr\Http\Message\RequestInterface::class)));

        $this->expectException(\CourtListener\Exceptions\CourtListenerException::class);
        $this->client->makeRequest('GET', 'test/');
    }

    public function testMakeRequestRateLimitError()
    {
        $mockResponse = new Response(429, [], json_encode(['detail' => 'Rate limit exceeded']));

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->willThrowException(new ClientException('Rate limit', $this->createMock(\Psr\Http\Message\RequestInterface::class), $mockResponse));

        $this->expectException(RateLimitException::class);
        $this->client->makeRequest('GET', 'test/');
    }

    public function testMakeRequestNotFoundError()
    {
        $mockResponse = new Response(404, [], json_encode(['detail' => 'Not found']));

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->willThrowException(new ClientException('Not found', $this->createMock(\Psr\Http\Message\RequestInterface::class), $mockResponse));

        $this->expectException(NotFoundException::class);
        $this->client->makeRequest('GET', 'test/');
    }

    public function testMakeRequestServerError()
    {
        $mockResponse = new Response(500, [], json_encode(['detail' => 'Internal server error']));

        $this->mockHttpClient->expects($this->exactly(3))
            ->method('request')
            ->willThrowException(new GuzzleServerException('Server error', $this->createMock(\Psr\Http\Message\RequestInterface::class), $mockResponse));

        $this->expectException(ServerException::class);
        $this->client->makeRequest('GET', 'test/');
    }

    public function testMakeRequestAuthenticationError()
    {
        $mockResponse = new Response(401, [], json_encode(['detail' => 'Authentication failed']));

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->willThrowException(new ClientException('Unauthorized', $this->createMock(\Psr\Http\Message\RequestInterface::class), $mockResponse));

        $this->expectException(AuthenticationException::class);
        $this->client->makeRequest('GET', 'test/');
    }

    public function testMakeRequestWithInvalidJsonResponse()
    {
        $mockResponse = new Response(200, [], 'invalid json');

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->willReturn($mockResponse);

        $result = $this->client->makeRequest('GET', 'test/');
        $this->assertEquals('invalid json', $result);
    }

    public function testMakeRequestWithEmptyResponse()
    {
        $mockResponse = new Response(204, [], '');

        $this->mockHttpClient->expects($this->once())
            ->method('request')
            ->willReturn($mockResponse);

        $result = $this->client->makeRequest('DELETE', 'test/');
        $this->assertEquals('', $result);
    }

    public function testAllEndpointsAreInitialized()
    {
        $expectedEndpoints = [
            'abaRatings', 'agreements', 'alerts', 'attorneys', 'audio',
            'citations', 'clusters', 'courts', 'debts', 'disclosurePositions',
            'docketAlerts', 'docketEntries', 'dockets', 'documents', 'educations',
            'financial', 'financialDisclosures', 'fjcIntegratedDatabase', 'gifts',
            'investments', 'judges', 'nonInvestmentIncomes', 'opinions', 'opinionsCited',
            'originatingCourtInformation', 'parties', 'people', 'politicalAffiliations',
            'positions', 'recapDocuments', 'recapFetch', 'recapQuery', 'reimbursements',
            'retentionEvents', 'schools', 'search', 'sources', 'spouseIncomes', 'tag'
        ];

        foreach ($expectedEndpoints as $endpoint) {
            $this->assertTrue(property_exists($this->client, $endpoint), "Endpoint $endpoint not found");
            $this->assertIsObject($this->client->$endpoint, "Endpoint $endpoint is not an object");
        }
    }

    public function testEndpointMethodsAreCallable()
    {
        $endpoints = ['dockets', 'opinions', 'courts', 'judges', 'alerts'];
        
        foreach ($endpoints as $endpoint) {
            $instance = $this->client->$endpoint;
            
            $this->assertTrue(method_exists($instance, 'list'), "$endpoint missing list method");
            $this->assertTrue(method_exists($instance, 'get'), "$endpoint missing get method");
            $this->assertTrue(method_exists($instance, 'create'), "$endpoint missing create method");
            $this->assertTrue(method_exists($instance, 'update'), "$endpoint missing update method");
            $this->assertTrue(method_exists($instance, 'patch'), "$endpoint missing patch method");
            $this->assertTrue(method_exists($instance, 'delete'), "$endpoint missing delete method");
            $this->assertTrue(method_exists($instance, 'search'), "$endpoint missing search method");
        }
    }

    public function testClientConfiguration()
    {
        $this->assertStringStartsWith('https://', $this->client->getBaseUrl());
        $this->assertInstanceOf(Client::class, $this->client->getHttpClient());
        $this->assertEquals('test-token', $this->client->getApiToken());
    }

    public function testClientWithCustomConfiguration()
    {
        $config = [
            'api_token' => 'custom-token',
            'base_url' => 'https://custom.example.com/api/',
            'timeout' => 60,
            'max_retries' => 5,
            'retry_delay' => 2.0
        ];

        $client = new CourtListenerClient($config);
        
        $this->assertEquals('custom-token', $client->getApiToken());
        $this->assertEquals('https://custom.example.com/api/', $client->getBaseUrl());
    }

    public function testClientRepr()
    {
        $repr = (string) $this->client;
        $this->assertStringContainsString('CourtListenerClient', $repr);
        $this->assertStringContainsString('test-tok', $repr);
    }

    public function testClientWithEmptyConfiguration()
    {
        $client = new CourtListenerClient([]);
        
        // Should use default values
        $this->assertStringStartsWith('https://', $client->getBaseUrl());
        $this->assertInstanceOf(Client::class, $client->getHttpClient());
    }

    public function testClientWithPartialConfiguration()
    {
        $config = ['api_token' => 'partial-token'];
        $client = new CourtListenerClient($config);
        
        $this->assertEquals('partial-token', $client->getApiToken());
        $this->assertStringStartsWith('https://', $client->getBaseUrl());
    }
}
