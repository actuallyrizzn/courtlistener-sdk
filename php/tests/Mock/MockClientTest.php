<?php

namespace CourtListener\Tests\Mock;

use CourtListener\CourtListenerClient;
use CourtListener\Exceptions\AuthenticationException;
use CourtListener\Exceptions\RateLimitException;
use CourtListener\Exceptions\NotFoundException;
use CourtListener\Exceptions\ServerException;
use PHPUnit\Framework\TestCase;

class MockClientTest extends TestCase
{
    private CourtListenerClient $client;

    protected function setUp(): void
    {
        $this->client = new CourtListenerClient(['api_token' => 'mock-token']);
    }

    public function testClientInitialization()
    {
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        $this->assertEquals('mock-token', $this->client->getApiToken());
    }

    public function testAllEndpointsAvailable()
    {
        $expectedEndpoints = [
            'dockets', 'opinions', 'courts', 'judges', 'alerts', 'audio',
            'clusters', 'positions', 'financial', 'docketEntries', 'attorneys',
            'parties', 'documents', 'citations', 'recapDocuments', 'financialDisclosures',
            'investments', 'nonInvestmentIncomes', 'agreements', 'gifts', 'reimbursements',
            'debts', 'disclosurePositions', 'spouseIncomes', 'opinionsCited', 'docketAlerts',
            'people', 'schools', 'educations', 'sources', 'retentionEvents', 'abaRatings',
            'politicalAffiliations', 'tag', 'recapFetch', 'recapQuery', 'originatingCourtInformation',
            'fjcIntegratedDatabase', 'search'
        ];

        foreach ($expectedEndpoints as $endpoint) {
            $this->assertTrue(property_exists($this->client, $endpoint), "Endpoint $endpoint not found");
            $this->assertIsObject($this->client->$endpoint, "Endpoint $endpoint is not an object");
        }
    }

    public function testDocketsEndpointMethods()
    {
        $dockets = $this->client->dockets;
        $expectedMethods = [
            'listDockets', 'getDocket', 'searchDockets', 'getDocketEntries',
            'getParties', 'getAttorneys', 'getRecapDocuments', 'getDocketByNumber',
            'getDocketsByCourt', 'getDocketsByDateRange', 'getDocketsByCaseType',
            'getDocketsByNatureOfSuit', 'getDocketsByJudge', 'getDocketsByStatus',
            'getDocketsWithFinancialDisclosures', 'getDocketsWithAudio',
            'getDocketsWithRecapDocuments', 'getDocketsByJurisdictionType',
            'getDocketsByJuryDemand'
        ];

        foreach ($expectedMethods as $method) {
            $this->assertTrue(method_exists($dockets, $method), "Method $method not found on Dockets endpoint");
        }
    }

    public function testOpinionsEndpointMethods()
    {
        $opinions = $this->client->opinions;
        $expectedMethods = [
            'listOpinions', 'getOpinion', 'searchOpinions', 'getOpinionsCited',
            'getOpinionsCiting', 'getClusters', 'getOpinionsByCourt', 'getOpinionsByJudge',
            'getOpinionsByDateRange', 'getPrecedentialOpinions', 'getNonPrecedentialOpinions',
            'getOpinionsByType', 'getOpinionsWithAudio', 'getOpinionsByJurisdiction',
            'getOpinionsByResourceType', 'getRecentOpinions', 'getOpinionsByCluster',
            'getOpinionsByCitationCount'
        ];

        foreach ($expectedMethods as $method) {
            $this->assertTrue(method_exists($opinions, $method), "Method $method not found on Opinions endpoint");
        }
    }

    public function testUtilityClasses()
    {
        $this->assertTrue(class_exists('CourtListener\Utils\Pagination'));
        $this->assertTrue(class_exists('CourtListener\Utils\Filters'));
        $this->assertTrue(class_exists('CourtListener\Models\BaseModel'));
    }

    public function testExceptionClasses()
    {
        $this->assertTrue(class_exists('CourtListener\Exceptions\CourtListenerException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\AuthenticationException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\RateLimitException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\NotFoundException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\ServerException'));
    }

    public function testExceptionHierarchy()
    {
        $this->assertInstanceOf(\Exception::class, new AuthenticationException());
        $this->assertInstanceOf(\Exception::class, new RateLimitException());
        $this->assertInstanceOf(\Exception::class, new NotFoundException());
        $this->assertInstanceOf(\Exception::class, new ServerException());
    }

    public function testClientConfiguration()
    {
        $this->assertStringStartsWith('https://', $this->client->getBaseUrl());
        $this->assertInstanceOf(\GuzzleHttp\Client::class, $this->client->getHttpClient());
    }

    public function testEndpointInstantiation()
    {
        // Test that all endpoints can be instantiated without errors
        $endpoints = [
            'dockets', 'opinions', 'courts', 'judges', 'alerts', 'audio',
            'clusters', 'positions', 'financial', 'docketEntries', 'attorneys',
            'parties', 'documents', 'citations', 'recapDocuments', 'financialDisclosures',
            'investments', 'nonInvestmentIncomes', 'agreements', 'gifts', 'reimbursements',
            'debts', 'disclosurePositions', 'spouseIncomes', 'opinionsCited', 'docketAlerts',
            'people', 'schools', 'educations', 'sources', 'retentionEvents', 'abaRatings',
            'politicalAffiliations', 'tag', 'recapFetch', 'recapQuery', 'originatingCourtInformation',
            'fjcIntegratedDatabase', 'search'
        ];

        foreach ($endpoints as $endpoint) {
            $instance = $this->client->$endpoint;
            $this->assertIsObject($instance, "Failed to instantiate $endpoint");
            $this->assertTrue(method_exists($instance, 'list'), "$endpoint missing list method");
            $this->assertTrue(method_exists($instance, 'get'), "$endpoint missing get method");
            $this->assertTrue(method_exists($instance, 'search'), "$endpoint missing search method");
        }
    }

    public function testBaseApiMethods()
    {
        // Test that all endpoints inherit from BaseApi and have standard methods
        $endpoints = ['dockets', 'opinions', 'courts', 'judges'];
        
        foreach ($endpoints as $endpoint) {
            $instance = $this->client->$endpoint;
            $this->assertTrue(method_exists($instance, 'list'));
            $this->assertTrue(method_exists($instance, 'get'));
            $this->assertTrue(method_exists($instance, 'create'));
            $this->assertTrue(method_exists($instance, 'update'));
            $this->assertTrue(method_exists($instance, 'patch'));
            $this->assertTrue(method_exists($instance, 'delete'));
            $this->assertTrue(method_exists($instance, 'search'));
        }
    }
}
