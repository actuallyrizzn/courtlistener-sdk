<?php

namespace CourtListener\Tests\Unit;

use CourtListener\AsyncCourtListenerClient;
use CourtListener\Exceptions\AuthenticationException;
use PHPUnit\Framework\TestCase;
use GuzzleHttp\Promise\PromiseInterface;

/**
 * Tests for AsyncCourtListenerClient
 */
class AsyncCourtListenerClientTest extends TestCase
{
    private array $validConfig;

    protected function setUp(): void
    {
        parent::setUp();
        
        // Set up valid configuration
        $this->validConfig = [
            'api_token' => 'test_token_12345',
            'base_url' => 'https://www.courtlistener.com/api/rest/v4/',
            'timeout' => 30,
            'max_retries' => 3,
            'retry_delay' => 1.0,
        ];
    }

    public function testConstructorWithValidConfig(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $this->assertInstanceOf(AsyncCourtListenerClient::class, $client);
        $this->assertEquals($this->validConfig['base_url'], $client->getBaseUrl());
        $this->assertEquals($this->validConfig['api_token'], $client->getApiToken());
    }

    public function testConstructorWithoutApiTokenThrowsException(): void
    {
        $this->expectException(AuthenticationException::class);
        $this->expectExceptionMessage('API token is required');
        
        new AsyncCourtListenerClient(['api_token' => '']);
    }

    public function testGetAsyncReturnsPromise(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $promise = $client->getAsync('courts/', ['page' => 1]);
        
        $this->assertInstanceOf(PromiseInterface::class, $promise);
    }

    public function testPostAsyncReturnsPromise(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $promise = $client->postAsync('alerts/', ['name' => 'Test Alert']);
        
        $this->assertInstanceOf(PromiseInterface::class, $promise);
    }

    public function testPutAsyncReturnsPromise(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $promise = $client->putAsync('alerts/123/', ['name' => 'Updated Alert']);
        
        $this->assertInstanceOf(PromiseInterface::class, $promise);
    }

    public function testPatchAsyncReturnsPromise(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $promise = $client->patchAsync('alerts/123/', ['name' => 'Patched Alert']);
        
        $this->assertInstanceOf(PromiseInterface::class, $promise);
    }

    public function testDeleteAsyncReturnsPromise(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $promise = $client->deleteAsync('alerts/123/');
        
        $this->assertInstanceOf(PromiseInterface::class, $promise);
    }

    public function testMakeRequestsBatch(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $requests = [
            ['method' => 'GET', 'endpoint' => 'courts/', 'options' => []],
            ['method' => 'GET', 'endpoint' => 'dockets/', 'options' => []],
        ];
        
        $promise = $client->makeRequestsBatch($requests);
        
        $this->assertInstanceOf(PromiseInterface::class, $promise);
    }

    public function testGetHttpClient(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $httpClient = $client->getHttpClient();
        
        $this->assertInstanceOf(\GuzzleHttp\Client::class, $httpClient);
    }

    public function testToString(): void
    {
        $client = new AsyncCourtListenerClient($this->validConfig);
        
        $string = (string) $client;
        
        $this->assertStringContainsString('AsyncCourtListenerClient', $string);
        $this->assertStringContainsString('api_token=', $string);
        $this->assertStringContainsString('base_url=', $string);
    }

    public function testConfigurationDefaults(): void
    {
        $client = new AsyncCourtListenerClient(['api_token' => 'test_token']);
        
        $this->assertEquals('https://www.courtlistener.com/api/rest/v4/', $client->getBaseUrl());
    }
}
