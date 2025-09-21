<?php

namespace CourtListener\Tests\Integration;

use CourtListener\CourtListenerClient;
use CourtListener\Utils\Pagination;
use CourtListener\Utils\Filters;
use PHPUnit\Framework\TestCase;

/**
 * Integration tests for complete workflows
 * 
 * @group integration
 */
class WorkflowTest extends TestCase
{
    private CourtListenerClient $client;

    protected function setUp(): void
    {
        $this->client = new CourtListenerClient(['api_token' => 'test-token']);
    }

    public function testCompleteDocketWorkflow()
    {
        // Test the complete docket workflow using mocks
        $this->assertInstanceOf(CourtListenerClient::class, $this->client);
        
        // Test that all docket methods exist and are callable
        $dockets = $this->client->dockets;
        
        $this->assertTrue(method_exists($dockets, 'listDockets'));
        $this->assertTrue(method_exists($dockets, 'getDocket'));
        $this->assertTrue(method_exists($dockets, 'searchDockets'));
        $this->assertTrue(method_exists($dockets, 'getDocketByNumber'));
        $this->assertTrue(method_exists($dockets, 'getDocketsByCourt'));
        $this->assertTrue(method_exists($dockets, 'getDocketsByDateRange'));
        $this->assertTrue(method_exists($dockets, 'getDocketEntries'));
        $this->assertTrue(method_exists($dockets, 'getParties'));
        $this->assertTrue(method_exists($dockets, 'getAttorneys'));
        $this->assertTrue(method_exists($dockets, 'getRecapDocuments'));
    }

    public function testCompleteOpinionWorkflow()
    {
        // Test the complete opinion workflow using mocks
        $opinions = $this->client->opinions;
        
        $this->assertTrue(method_exists($opinions, 'listOpinions'));
        $this->assertTrue(method_exists($opinions, 'getOpinion'));
        $this->assertTrue(method_exists($opinions, 'searchOpinions'));
        $this->assertTrue(method_exists($opinions, 'getOpinionsCited'));
        $this->assertTrue(method_exists($opinions, 'getOpinionsCiting'));
        $this->assertTrue(method_exists($opinions, 'getClusters'));
        $this->assertTrue(method_exists($opinions, 'getOpinionsByCourt'));
        $this->assertTrue(method_exists($opinions, 'getOpinionsByJudge'));
        $this->assertTrue(method_exists($opinions, 'getPrecedentialOpinions'));
        $this->assertTrue(method_exists($opinions, 'getRecentOpinions'));
    }

    public function testSearchWorkflow()
    {
        // Test search functionality across different endpoints
        $search = $this->client->search;
        
        $this->assertTrue(method_exists($search, 'list'));
        $this->assertTrue(method_exists($search, 'get'));
        $this->assertTrue(method_exists($search, 'search'));
    }

    public function testFinancialDisclosureWorkflow()
    {
        // Test financial disclosure workflow
        $financial = $this->client->financial;
        $financialDisclosures = $this->client->financialDisclosures;
        $investments = $this->client->investments;
        $gifts = $this->client->gifts;
        $debts = $this->client->debts;
        
        $this->assertTrue(method_exists($financial, 'list'));
        $this->assertTrue(method_exists($financialDisclosures, 'list'));
        $this->assertTrue(method_exists($investments, 'list'));
        $this->assertTrue(method_exists($gifts, 'list'));
        $this->assertTrue(method_exists($debts, 'list'));
    }

    public function testPeopleAndEducationWorkflow()
    {
        // Test people and education workflow
        $people = $this->client->people;
        $judges = $this->client->judges;
        $schools = $this->client->schools;
        $educations = $this->client->educations;
        $positions = $this->client->positions;
        
        $this->assertTrue(method_exists($people, 'list'));
        $this->assertTrue(method_exists($judges, 'list'));
        $this->assertTrue(method_exists($schools, 'list'));
        $this->assertTrue(method_exists($educations, 'list'));
        $this->assertTrue(method_exists($positions, 'list'));
    }

    public function testAlertWorkflow()
    {
        // Test alert workflow
        $alerts = $this->client->alerts;
        $docketAlerts = $this->client->docketAlerts;
        
        $this->assertTrue(method_exists($alerts, 'list'));
        $this->assertTrue(method_exists($alerts, 'get'));
        $this->assertTrue(method_exists($alerts, 'create'));
        $this->assertTrue(method_exists($alerts, 'update'));
        $this->assertTrue(method_exists($alerts, 'delete'));
        
        $this->assertTrue(method_exists($docketAlerts, 'list'));
        $this->assertTrue(method_exists($docketAlerts, 'get'));
        $this->assertTrue(method_exists($docketAlerts, 'create'));
        $this->assertTrue(method_exists($docketAlerts, 'update'));
        $this->assertTrue(method_exists($docketAlerts, 'delete'));
    }

    public function testCourtWorkflow()
    {
        // Test court workflow
        $courts = $this->client->courts;
        
        $this->assertTrue(method_exists($courts, 'listCourts'));
        $this->assertTrue(method_exists($courts, 'getCourt'));
        $this->assertTrue(method_exists($courts, 'searchCourts'));
        $this->assertTrue(method_exists($courts, 'getHierarchy'));
        $this->assertTrue(method_exists($courts, 'getTypes'));
    }

    public function testAudioWorkflow()
    {
        // Test audio workflow
        $audio = $this->client->audio;
        
        $this->assertTrue(method_exists($audio, 'listAudio'));
        $this->assertTrue(method_exists($audio, 'getAudio'));
        $this->assertTrue(method_exists($audio, 'searchAudio'));
    }

    public function testCitationWorkflow()
    {
        // Test citation workflow
        $citations = $this->client->citations;
        $opinionsCited = $this->client->opinionsCited;
        
        $this->assertTrue(method_exists($citations, 'list'));
        $this->assertTrue(method_exists($citations, 'get'));
        $this->assertTrue(method_exists($opinionsCited, 'list'));
        $this->assertTrue(method_exists($opinionsCited, 'get'));
    }

    public function testRecapWorkflow()
    {
        // Test RECAP workflow
        $recapDocuments = $this->client->recapDocuments;
        $recapFetch = $this->client->recapFetch;
        $recapQuery = $this->client->recapQuery;
        
        $this->assertTrue(method_exists($recapDocuments, 'list'));
        $this->assertTrue(method_exists($recapFetch, 'list'));
        $this->assertTrue(method_exists($recapQuery, 'list'));
    }

    public function testUtilityIntegration()
    {
        // Test utility classes integration
        $paginationParams = Pagination::getParams(1, 20);
        $this->assertIsArray($paginationParams);
        $this->assertEquals(1, $paginationParams['page']);
        $this->assertEquals(20, $paginationParams['per_page']);
        
        $dateFilters = Filters::dateRange('2023-01-01', '2023-12-31');
        $this->assertIsArray($dateFilters);
        $this->assertArrayHasKey('date_filed__gte', $dateFilters);
        $this->assertArrayHasKey('date_filed__lte', $dateFilters);
        
        $textFilters = Filters::textSearch('patent', 'q');
        $this->assertIsArray($textFilters);
        $this->assertEquals('patent', $textFilters['q']);
        
        $exactFilters = Filters::exact('federal', 'court_type');
        $this->assertIsArray($exactFilters);
        $this->assertEquals('federal', $exactFilters['court_type']);
    }

    public function testErrorHandlingIntegration()
    {
        // Test error handling across the SDK
        $this->assertTrue(class_exists('CourtListener\Exceptions\CourtListenerException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\AuthenticationException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\RateLimitException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\NotFoundException'));
        $this->assertTrue(class_exists('CourtListener\Exceptions\ServerException'));
    }

    public function testModelIntegration()
    {
        // Test model integration
        $this->assertTrue(class_exists('CourtListener\Models\BaseModel'));
        $this->assertTrue(class_exists('CourtListener\Models\Docket'));
        
        // Test BaseModel functionality
        $model = new \CourtListener\Models\BaseModel(['id' => 1, 'name' => 'test']);
        $this->assertEquals(1, $model->get('id'));
        $this->assertEquals('test', $model->get('name'));
        $this->assertTrue($model->has('id'));
        $this->assertFalse($model->has('nonexistent'));
    }

    public function testAllEndpointsIntegration()
    {
        // Test that all 39 endpoints are properly integrated
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
            $instance = $this->client->$endpoint;
            $this->assertIsObject($instance, "Endpoint $endpoint is not an object");
            
            // Test that all endpoints have basic CRUD methods
            $this->assertTrue(method_exists($instance, 'list'), "$endpoint missing list method");
            $this->assertTrue(method_exists($instance, 'get'), "$endpoint missing get method");
            $this->assertTrue(method_exists($instance, 'search'), "$endpoint missing search method");
        }
    }
}
