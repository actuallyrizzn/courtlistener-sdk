<?php

namespace CourtListener\Tests\Unit\Models;

use CourtListener\Models\RecapFetch;
use PHPUnit\Framework\TestCase;

class RecapFetchTest extends TestCase
{
    private RecapFetch $model;

    protected function setUp(): void
    {
        $this->model = new RecapFetch();
    }

    public function testConstructor()
    {
        $this->assertInstanceOf(RecapFetch::class, $this->model);
    }

    public function testConstructorWithData()
    {
        $data = [
            'id' => 123,
            'name' => 'Test RECAP Fetch',
            'date_created' => '2023-01-01T00:00:00Z',
            'date_modified' => '2023-01-02T00:00:00Z'
        ];
        
        $model = new RecapFetch($data);
        $this->assertEquals(123, $model->getId());
        $this->assertEquals('Test RECAP Fetch', $model->getName());
    }

    public function testGetId()
    {
        $this->model->set('id', 456);
        $this->assertEquals(456, $this->model->getId());
    }

    public function testGetIdWithNull()
    {
        $this->assertNull($this->model->getId());
    }

    public function testGetName()
    {
        $this->model->set('name', 'Test Name');
        $this->assertEquals('Test Name', $this->model->getName());
    }

    public function testGetNameWithTitle()
    {
        $this->model->set('title', 'Test Title');
        $this->assertEquals('Test Title', $this->model->getName());
    }

    public function testGetNameWithCaseName()
    {
        $this->model->set('case_name', 'Test Case');
        $this->assertEquals('Test Case', $this->model->getName());
    }

    public function testGetNameWithNull()
    {
        $this->assertNull($this->model->getName());
    }

    public function testGetResourceUri()
    {
        $this->model->set('resource_uri', '/api/test/123/');
        $this->assertEquals('/api/test/123/', $this->model->getResourceUri());
    }

    public function testGetResourceUriWithNull()
    {
        $this->assertNull($this->model->getResourceUri());
    }

    public function testGetAbsoluteUrl()
    {
        $this->model->set('absolute_url', 'https://example.com/test/123/');
        $this->assertEquals('https://example.com/test/123/', $this->model->getAbsoluteUrl());
    }

    public function testGetAbsoluteUrlWithNull()
    {
        $this->assertNull($this->model->getAbsoluteUrl());
    }

    public function testGetDateCreated()
    {
        $this->model->set('date_created', '2023-01-01T00:00:00Z');
        $this->assertEquals('2023-01-01T00:00:00Z', $this->model->getDateCreated());
    }

    public function testGetDateCreatedWithNull()
    {
        $this->assertNull($this->model->getDateCreated());
    }

    public function testGetDateModified()
    {
        $this->model->set('date_modified', '2023-01-02T00:00:00Z');
        $this->assertEquals('2023-01-02T00:00:00Z', $this->model->getDateModified());
    }

    public function testGetDateModifiedWithNull()
    {
        $this->assertNull($this->model->getDateModified());
    }

    public function testIsModified()
    {
        $this->assertFalse($this->model->isModified());
        
        $this->model->set('name', 'Modified Name');
        $this->assertTrue($this->model->isModified());
    }

    public function testToStringWithIdAndName()
    {
        $this->model->set('id', 789);
        $this->model->set('name', 'Test Name');
        
        $expected = 'RecapFetch #789: Test Name';
        $this->assertEquals($expected, (string) $this->model);
    }

    public function testToStringWithIdOnly()
    {
        $this->model->set('id', 789);
        
        $expected = 'RecapFetch #789';
        $this->assertEquals($expected, (string) $this->model);
    }

    public function testToStringWithNameOnly()
    {
        $this->model->set('name', 'Test Name');
        
        $expected = 'RecapFetch';
        $this->assertEquals($expected, (string) $this->model);
    }

    public function testToStringEmpty()
    {
        $expected = 'RecapFetch';
        $this->assertEquals($expected, (string) $this->model);
    }

    public function testInheritsFromBaseModel()
    {
        $this->assertInstanceOf(\CourtListener\Models\BaseModel::class, $this->model);
    }

    public function testBasicModelFunctionality()
    {
        // Test basic BaseModel functionality
        $this->model->set('test_field', 'test_value');
        $this->assertEquals('test_value', $this->model->get('test_field'));
        $this->assertTrue($this->model->has('test_field'));
        $this->assertFalse($this->model->has('nonexistent_field'));
        
        // Test array access
        $this->model['array_field'] = 'array_value';
        $this->assertEquals('array_value', $this->model['array_field']);
        $this->assertTrue(isset($this->model['array_field']));
        
        // Test JSON serialization
        $json = json_encode($this->model);
        $this->assertIsString($json);
        
        // Test toArray
        $array = $this->model->toArray();
        $this->assertIsArray($array);
    }

    public function testModelWithComprehensiveData()
    {
        $comprehensiveData = [
            'id' => 999,
            'name' => 'Comprehensive Test RECAP Fetch',
            'title' => 'Test Title',
            'case_name' => 'Test Case Name',
            'resource_uri' => '/api/comprehensive/999/',
            'absolute_url' => 'https://example.com/comprehensive/999/',
            'date_created' => '2023-01-01T00:00:00Z',
            'date_modified' => '2023-01-02T00:00:00Z',
            'description' => 'Test description',
            'status' => 'active',
            'metadata' => ['key' => 'value']
        ];
        
        $model = new RecapFetch($comprehensiveData);
        
        $this->assertEquals(999, $model->getId());
        $this->assertEquals('Comprehensive Test RECAP Fetch', $model->getName());
        $this->assertEquals('/api/comprehensive/999/', $model->getResourceUri());
        $this->assertEquals('https://example.com/comprehensive/999/', $model->getAbsoluteUrl());
        $this->assertEquals('2023-01-01T00:00:00Z', $model->getDateCreated());
        $this->assertEquals('2023-01-02T00:00:00Z', $model->getDateModified());
        
        // Test additional fields
        $this->assertEquals('Test description', $model->get('description'));
        $this->assertEquals('active', $model->get('status'));
        $this->assertEquals(['key' => 'value'], $model->get('metadata'));
    }

    public function testModelWithEmptyData()
    {
        $model = new RecapFetch([]);
        
        $this->assertNull($model->getId());
        $this->assertNull($model->getName());
        $this->assertNull($model->getResourceUri());
        $this->assertNull($model->getAbsoluteUrl());
        $this->assertNull($model->getDateCreated());
        $this->assertNull($model->getDateModified());
        $this->assertFalse($model->isModified());
    }

    public function testModelWithPartialData()
    {
        $partialData = [
            'id' => 555,
            'name' => 'Partial Test'
        ];
        
        $model = new RecapFetch($partialData);
        
        $this->assertEquals(555, $model->getId());
        $this->assertEquals('Partial Test', $model->getName());
        $this->assertNull($model->getResourceUri());
        $this->assertNull($model->getAbsoluteUrl());
        $this->assertNull($model->getDateCreated());
        $this->assertNull($model->getDateModified());
    }
}