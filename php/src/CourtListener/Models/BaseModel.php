<?php

namespace CourtListener\Models;

use ArrayAccess;
use JsonSerializable;

/**
 * Base model class providing common functionality for all data models
 */
class BaseModel implements ArrayAccess, JsonSerializable
{
    protected array $data = [];
    protected array $original = [];

    /**
     * Constructor
     *
     * @param array $data Model data
     */
    public function __construct(array $data = [])
    {
        $this->data = $data;
        $this->original = $data;
    }

    /**
     * Get a property value
     *
     * @param string $key Property key
     * @param mixed $default Default value
     * @return mixed
     */
    public function get(string $key, $default = null)
    {
        return $this->data[$key] ?? $default;
    }

    /**
     * Set a property value
     *
     * @param string $key Property key
     * @param mixed $value Property value
     * @return void
     */
    public function set(string $key, $value): void
    {
        $this->data[$key] = $value;
    }

    /**
     * Check if a property exists
     *
     * @param string $key Property key
     * @return bool
     */
    public function has(string $key): bool
    {
        return array_key_exists($key, $this->data);
    }

    /**
     * Get all data as array
     *
     * @return array
     */
    public function toArray(): array
    {
        return $this->data;
    }

    /**
     * Get all data as JSON
     *
     * @return string
     */
    public function toJson(): string
    {
        return json_encode($this->data, JSON_PRETTY_PRINT);
    }

    /**
     * Check if the model has been modified
     *
     * @return bool
     */
    public function isDirty(): bool
    {
        return $this->data !== $this->original;
    }

    /**
     * Get the original data
     *
     * @return array
     */
    public function getOriginal(): array
    {
        return $this->original;
    }

    /**
     * Reset the model to its original state
     *
     * @return void
     */
    public function reset(): void
    {
        $this->data = $this->original;
    }

    /**
     * ArrayAccess implementation
     */
    public function offsetExists($offset): bool
    {
        return $this->has($offset);
    }

    public function offsetGet($offset)
    {
        return $this->get($offset);
    }

    public function offsetSet($offset, $value): void
    {
        $this->set($offset, $value);
    }

    public function offsetUnset($offset): void
    {
        unset($this->data[$offset]);
    }

    /**
     * JsonSerializable implementation
     */
    public function jsonSerialize(): array
    {
        return $this->data;
    }

    /**
     * Magic method for getting properties
     */
    public function __get(string $key)
    {
        return $this->get($key);
    }

    /**
     * Magic method for setting properties
     */
    public function __set(string $key, $value): void
    {
        $this->set($key, $value);
    }

    /**
     * Magic method for checking property existence
     */
    public function __isset(string $key): bool
    {
        return $this->has($key);
    }

    /**
     * Magic method for unsetting properties
     */
    public function __unset(string $key): void
    {
        unset($this->data[$key]);
    }

    /**
     * String representation of the model
     */
    public function __toString(): string
    {
        return $this->toJson();
    }
}
