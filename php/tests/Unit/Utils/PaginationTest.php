<?php

namespace CourtListener\Tests\Unit\Utils;

use CourtListener\Utils\Pagination;
use PHPUnit\Framework\TestCase;

class PaginationTest extends TestCase
{
    public function testGetParams()
    {
        $params = Pagination::getParams(2, 50);
        
        $this->assertEquals(2, $params['page']);
        $this->assertEquals(50, $params['per_page']);
    }

    public function testGetParamsWithDefaults()
    {
        $params = Pagination::getParams();
        
        $this->assertEquals(1, $params['page']);
        $this->assertEquals(20, $params['per_page']);
    }

    public function testGetCursorParams()
    {
        $params = Pagination::getCursorParams('abc123', 25);
        
        $this->assertEquals('abc123', $params['cursor']);
        $this->assertEquals(25, $params['per_page']);
    }

    public function testGetCursorParamsWithoutCursor()
    {
        $params = Pagination::getCursorParams(null, 30);
        
        $this->assertArrayNotHasKey('cursor', $params);
        $this->assertEquals(30, $params['per_page']);
    }

    public function testExtractInfo()
    {
        $response = [
            'count' => 100,
            'next' => 'https://api.example.com/endpoint/?page=2&per_page=20',
            'previous' => null,
            'results' => []
        ];
        
        $info = Pagination::extractInfo($response);
        
        $this->assertEquals(100, $info['count']);
        $this->assertStringContainsString('page=2', $info['next']);
        $this->assertNull($info['previous']);
        $this->assertEquals(1, $info['current_page']);
        $this->assertEquals(5, $info['total_pages']);
        $this->assertEquals(20, $info['per_page']);
    }

    public function testExtractInfoWithNoNext()
    {
        $response = [
            'count' => 15,
            'next' => null,
            'previous' => 'https://api.example.com/endpoint/?page=1&per_page=20',
            'results' => []
        ];
        
        $info = Pagination::extractInfo($response);
        
        $this->assertEquals(15, $info['count']);
        $this->assertNull($info['next']);
        $this->assertStringContainsString('page=1', $info['previous']);
        $this->assertEquals(1, $info['current_page']);
        $this->assertEquals(1, $info['total_pages']);
        $this->assertEquals(20, $info['per_page']);
    }
}
