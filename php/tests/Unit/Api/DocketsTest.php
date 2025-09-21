<?php

namespace CourtListener\Tests\Unit\Api;

use CourtListener\Api\Dockets;
use CourtListener\CourtListenerClient;
use PHPUnit\Framework\TestCase;
use PHPUnit\Framework\MockObject\MockObject;

class DocketsTest extends TestCase
{
    private Dockets $dockets;
    private MockObject $client;

    protected function setUp(): void
    {
        $this->client = $this->createMock(CourtListenerClient::class);
        $this->dockets = new Dockets($this->client);
    }

    public function testListDockets()
    {
        $expectedResponse = [
            'count' => 100,
            'next' => 'http://api.example.com/dockets/?page=2',
            'previous' => null,
            'results' => [
                ['id' => 1, 'case_name' => 'Test Case 1'],
                ['id' => 2, 'case_name' => 'Test Case 2']
            ]
        ];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['page' => 1]])
            ->willReturn($expectedResponse);

        $result = $this->dockets->listDockets(['page' => 1]);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocket()
    {
        $expectedResponse = ['id' => 123, 'case_name' => 'Test Case'];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/123/', ['query' => []])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocket(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testSearchDockets()
    {
        $expectedResponse = ['count' => 5, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/search/', ['query' => ['q' => 'patent']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->searchDockets(['q' => 'patent']);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketEntries()
    {
        $expectedResponse = ['count' => 10, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/123/docket-entries/', ['query' => []])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketEntries(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetParties()
    {
        $expectedResponse = ['count' => 3, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/123/parties/', ['query' => []])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getParties(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetAttorneys()
    {
        $expectedResponse = ['count' => 2, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/123/attorneys/', ['query' => []])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getAttorneys(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetRecapDocuments()
    {
        $expectedResponse = ['count' => 5, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/123/recap/', ['query' => []])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getRecapDocuments(123);
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketByNumber()
    {
        $expectedResponse = [
            'count' => 1,
            'results' => [['id' => 123, 'docket_number' => '1:23-cv-456']]
        ];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['docket_number' => '1:23-cv-456']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketByNumber('1:23-cv-456');
        $this->assertEquals($expectedResponse['results'][0], $result);
    }

    public function testGetDocketByNumberNotFound()
    {
        $expectedResponse = ['count' => 0, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['docket_number' => 'nonexistent']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketByNumber('nonexistent');
        $this->assertNull($result);
    }

    public function testGetDocketsByCourt()
    {
        $expectedResponse = ['count' => 50, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['court' => 'ca1']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsByCourt('ca1');
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsByDateRange()
    {
        $expectedResponse = ['count' => 25, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => [
                'date_filed__gte' => '2023-01-01',
                'date_filed__lte' => '2023-12-31'
            ]])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsByDateRange('2023-01-01', '2023-12-31');
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsByCaseType()
    {
        $expectedResponse = ['count' => 10, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['case_type' => 'Civil']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsByCaseType('Civil');
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsByJudge()
    {
        $expectedResponse = ['count' => 15, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['assigned_to' => 'judge123']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsByJudge('judge123');
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsWithFinancialDisclosures()
    {
        $expectedResponse = ['count' => 8, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['has_financial_disclosures' => 'true']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsWithFinancialDisclosures();
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsWithAudio()
    {
        $expectedResponse = ['count' => 12, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['has_audio' => 'true']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsWithAudio();
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsWithRecapDocuments()
    {
        $expectedResponse = ['count' => 20, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['has_recap_documents' => 'true']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsWithRecapDocuments();
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsByJurisdictionType()
    {
        $expectedResponse = ['count' => 30, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['jurisdiction_type' => 'Federal']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsByJurisdictionType('Federal');
        $this->assertEquals($expectedResponse, $result);
    }

    public function testGetDocketsByJuryDemand()
    {
        $expectedResponse = ['count' => 5, 'results' => []];

        $this->client->expects($this->once())
            ->method('makeRequest')
            ->with('GET', 'dockets/', ['query' => ['jury_demand' => 'Jury']])
            ->willReturn($expectedResponse);

        $result = $this->dockets->getDocketsByJuryDemand('Jury');
        $this->assertEquals($expectedResponse, $result);
    }
}
