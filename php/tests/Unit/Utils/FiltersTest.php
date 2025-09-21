<?php

namespace CourtListener\Tests\Unit\Utils;

use CourtListener\Utils\Filters;
use PHPUnit\Framework\TestCase;

class FiltersTest extends TestCase
{
    public function testDateRange()
    {
        $filters = Filters::dateRange('2023-01-01', '2023-12-31', 'date_filed');
        
        $this->assertEquals('2023-01-01', $filters['date_filed__gte']);
        $this->assertEquals('2023-12-31', $filters['date_filed__lte']);
    }

    public function testDateRangeWithStartDateOnly()
    {
        $filters = Filters::dateRange('2023-01-01', null, 'date_filed');
        
        $this->assertEquals('2023-01-01', $filters['date_filed__gte']);
        $this->assertArrayNotHasKey('date_filed__lte', $filters);
    }

    public function testDateRangeWithEndDateOnly()
    {
        $filters = Filters::dateRange(null, '2023-12-31', 'date_filed');
        
        $this->assertArrayNotHasKey('date_filed__gte', $filters);
        $this->assertEquals('2023-12-31', $filters['date_filed__lte']);
    }

    public function testTextSearch()
    {
        $filters = Filters::textSearch('copyright', 'q');
        
        $this->assertEquals('copyright', $filters['q']);
    }

    public function testTextSearchWithDefaultField()
    {
        $filters = Filters::textSearch('patent');
        
        $this->assertEquals('patent', $filters['q']);
    }

    public function testExact()
    {
        $filters = Filters::exact('federal', 'court_type');
        
        $this->assertEquals('federal', $filters['court_type']);
    }

    public function testContains()
    {
        $filters = Filters::contains('patent', 'case_name');
        
        $this->assertEquals('patent', $filters['case_name__icontains']);
    }

    public function testIn()
    {
        $filters = Filters::in(['1', '2', '3'], 'court');
        
        $this->assertEquals('1,2,3', $filters['court__in']);
    }

    public function testOrderBy()
    {
        $filters = Filters::orderBy('date_filed', 'asc');
        
        $this->assertEquals('date_filed', $filters['order_by']);
    }

    public function testOrderByDesc()
    {
        $filters = Filters::orderBy('date_filed', 'desc');
        
        $this->assertEquals('-date_filed', $filters['order_by']);
    }

    public function testOrderByMultiple()
    {
        $filters = Filters::orderByMultiple([
            'date_filed' => 'desc',
            'case_name' => 'asc'
        ]);
        
        $this->assertEquals('-date_filed,case_name', $filters['order_by']);
    }

    public function testBoolean()
    {
        $filters = Filters::boolean(true, 'has_audio');
        
        $this->assertEquals('true', $filters['has_audio']);
    }

    public function testBooleanFalse()
    {
        $filters = Filters::boolean(false, 'has_audio');
        
        $this->assertEquals('false', $filters['has_audio']);
    }

    public function testNull()
    {
        $filters = Filters::null('assigned_to', true);
        
        $this->assertEquals('true', $filters['assigned_to__isnull']);
    }

    public function testNullFalse()
    {
        $filters = Filters::null('assigned_to', false);
        
        $this->assertEquals('false', $filters['assigned_to__isnull']);
    }

    public function testRange()
    {
        $filters = Filters::range(100, 500, 'citation_count');
        
        $this->assertEquals(100, $filters['citation_count__gte']);
        $this->assertEquals(500, $filters['citation_count__lte']);
    }

    public function testRangeWithMinOnly()
    {
        $filters = Filters::range(100, null, 'citation_count');
        
        $this->assertEquals(100, $filters['citation_count__gte']);
        $this->assertArrayNotHasKey('citation_count__lte', $filters);
    }

    public function testRangeWithMaxOnly()
    {
        $filters = Filters::range(null, 500, 'citation_count');
        
        $this->assertArrayNotHasKey('citation_count__gte', $filters);
        $this->assertEquals(500, $filters['citation_count__lte']);
    }
}
