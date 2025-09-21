<?php

namespace CourtListener\Tests\Unit\Models;

use CourtListener\Models\BaseModel;
use PHPUnit\Framework\TestCase;

class BaseModelTest extends TestCase
{
    private BaseModel $model;

    protected function setUp(): void
    {
        $this->model = new BaseModel([
            'id' => 123,
            'name' => 'Test Model',
            'active' => true,
            'metadata' => ['key' => 'value']
        ]);
    }

    public function testConstructor()
    {
        $this->assertInstanceOf(BaseModel::class, $this->model);
        $this->assertEquals(123, $this->model->get('id'));
        $this->assertEquals('Test Model', $this->model->get('name'));
    }

    public function testGet()
    {
        $this->assertEquals(123, $this->model->get('id'));
        $this->assertEquals('Test Model', $this->model->get('name'));
        $this->assertTrue($this->model->get('active'));
        $this->assertNull($this->model->get('nonexistent'));
        $this->assertEquals('default', $this->model->get('nonexistent', 'default'));
    }

    public function testSet()
    {
        $this->model->set('new_field', 'new_value');
        $this->assertEquals('new_value', $this->model->get('new_field'));
    }

    public function testHas()
    {
        $this->assertTrue($this->model->has('id'));
        $this->assertTrue($this->model->has('name'));
        $this->assertFalse($this->model->has('nonexistent'));
    }

    public function testToArray()
    {
        $array = $this->model->toArray();
        $this->assertIsArray($array);
        $this->assertEquals(123, $array['id']);
        $this->assertEquals('Test Model', $array['name']);
    }

    public function testToJson()
    {
        $json = $this->model->toJson();
        $this->assertIsString($json);
        
        $decoded = json_decode($json, true);
        $this->assertEquals(123, $decoded['id']);
        $this->assertEquals('Test Model', $decoded['name']);
    }

    public function testIsDirty()
    {
        $this->assertFalse($this->model->isDirty());
        
        $this->model->set('name', 'Modified Name');
        $this->assertTrue($this->model->isDirty());
    }

    public function testGetOriginal()
    {
        $original = $this->model->getOriginal();
        $this->assertEquals('Test Model', $original['name']);
        
        $this->model->set('name', 'Modified Name');
        $this->assertEquals('Modified Name', $this->model->get('name'));
        $this->assertEquals('Test Model', $this->model->getOriginal()['name']);
    }

    public function testReset()
    {
        $this->model->set('name', 'Modified Name');
        $this->assertTrue($this->model->isDirty());
        
        $this->model->reset();
        $this->assertFalse($this->model->isDirty());
        $this->assertEquals('Test Model', $this->model->get('name'));
    }

    public function testArrayAccess()
    {
        // Test offsetExists
        $this->assertTrue(isset($this->model['id']));
        $this->assertFalse(isset($this->model['nonexistent']));
        
        // Test offsetGet
        $this->assertEquals(123, $this->model['id']);
        
        // Test offsetSet
        $this->model['new_field'] = 'new_value';
        $this->assertEquals('new_value', $this->model['new_field']);
        
        // Test offsetUnset
        unset($this->model['name']);
        $this->assertFalse(isset($this->model['name']));
    }

    public function testMagicMethods()
    {
        // Test __get
        $this->assertEquals(123, $this->model->id);
        $this->assertEquals('Test Model', $this->model->name);
        
        // Test __set
        $this->model->magic_field = 'magic_value';
        $this->assertEquals('magic_value', $this->model->magic_field);
        
        // Test __isset
        $this->assertTrue(isset($this->model->id));
        $this->assertFalse(isset($this->model->nonexistent));
        
        // Test __unset
        unset($this->model->name);
        $this->assertFalse(isset($this->model->name));
    }

    public function testJsonSerializable()
    {
        $jsonData = json_encode($this->model);
        $this->assertIsString($jsonData);
        
        $decoded = json_decode($jsonData, true);
        $this->assertEquals(123, $decoded['id']);
        $this->assertEquals('Test Model', $decoded['name']);
    }

    public function testToString()
    {
        $string = (string) $this->model;
        $this->assertIsString($string);
        
        $decoded = json_decode($string, true);
        $this->assertEquals(123, $decoded['id']);
    }
}
