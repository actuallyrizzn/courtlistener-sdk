<?php

namespace CourtListener\Tests\Unit;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\AuthenticationException;
use PHPUnit\Framework\TestCase;

class CourtListenerClientTest extends TestCase
{
    public function testClientInitializationWithToken()
    {
        $client = new CourtListenerClient(['api_token' => 'test-token']);
        
        $this->assertInstanceOf(CourtListenerClient::class, $client);
        $this->assertEquals('test-token', $client->getApiToken());
    }

    public function testClientInitializationWithoutToken()
    {
        $this->expectException(AuthenticationException::class);
        $this->expectExceptionMessage('API token is required');
        
        new CourtListenerClient();
    }

    public function testClientInitializationWithEmptyToken()
    {
        $this->expectException(AuthenticationException::class);
        $this->expectExceptionMessage('API token is required');
        
        new CourtListenerClient(['api_token' => '']);
    }

    public function testClientGetters()
    {
        $client = new CourtListenerClient([
            'api_token' => 'test-token',
            'base_url' => 'https://test.example.com/api/'
        ]);
        
        $this->assertEquals('test-token', $client->getApiToken());
        $this->assertEquals('https://test.example.com/api/', $client->getBaseUrl());
    }

    public function testClientHasHttpClient()
    {
        $client = new CourtListenerClient(['api_token' => 'test-token']);
        
        $this->assertInstanceOf(\GuzzleHttp\Client::class, $client->getHttpClient());
    }

    public function testClientInitializesEndpoints()
    {
        $client = new CourtListenerClient(['api_token' => 'test-token']);
        
        // Test that all major endpoints are initialized
        $this->assertInstanceOf(\CourtListener\Api\Dockets::class, $client->dockets);
        $this->assertInstanceOf(\CourtListener\Api\Opinions::class, $client->opinions);
        $this->assertInstanceOf(\CourtListener\Api\Courts::class, $client->courts);
        $this->assertInstanceOf(\CourtListener\Api\Judges::class, $client->judges);
        $this->assertInstanceOf(\CourtListener\Api\Alerts::class, $client->alerts);
    }
}
