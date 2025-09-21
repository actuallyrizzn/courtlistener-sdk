<?php

namespace CourtListener\Models;

/**
 * Alert model
 * 
 * @package CourtListener\Models
 */
class Alert extends BaseModel
{
    /**
     * Constructor
     *
     * @param array $data Model data
     */
    public function __construct(array $data = [])
    {
        parent::__construct($data);
    }

    /**
     * Get the model's primary identifier
     *
     * @return mixed
     */
    public function getId()
    {
        return $this->get('id');
    }

    /**
     * Get the model's name or title
     *
     * @return string|null
     */
    public function getName()
    {
        return $this->get('name') ?? $this->get('title') ?? $this->get('case_name');
    }

    /**
     * Get the model's resource URI
     *
     * @return string|null
     */
    public function getResourceUri()
    {
        return $this->get('resource_uri');
    }

    /**
     * Get the model's absolute URL
     *
     * @return string|null
     */
    public function getAbsoluteUrl()
    {
        return $this->get('absolute_url');
    }

    /**
     * Get the model's date created
     *
     * @return string|null
     */
    public function getDateCreated()
    {
        return $this->get('date_created');
    }

    /**
     * Get the model's date modified
     *
     * @return string|null
     */
    public function getDateModified()
    {
        return $this->get('date_modified');
    }

    /**
     * Check if the model has been modified
     *
     * @return bool
     */
    public function isModified()
    {
        return $this->isDirty();
    }

    /**
     * Get a string representation of the model
     *
     * @return string
     */
    public function __toString()
    {
        $name = $this->getName();
        $id = $this->getId();
        
        if ($name && $id) {
            return "Alert #{$id}: {$name}";
        } elseif ($id) {
            return "Alert #{$id}";
        } else {
            return "Alert";
        }
    }
}