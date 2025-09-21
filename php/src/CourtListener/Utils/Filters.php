<?php

namespace CourtListener\Utils;

/**
 * Filter utility class for building API query parameters
 */
class Filters
{
    /**
     * Build date range filter
     *
     * @param string|null $startDate Start date (Y-m-d format)
     * @param string|null $endDate End date (Y-m-d format)
     * @param string $field Field name
     * @return array
     */
    public static function dateRange(?string $startDate = null, ?string $endDate = null, string $field = 'date_filed'): array
    {
        $filters = [];
        
        if ($startDate) {
            $filters["{$field}__gte"] = $startDate;
        }
        
        if ($endDate) {
            $filters["{$field}__lte"] = $endDate;
        }
        
        return $filters;
    }

    /**
     * Build text search filter
     *
     * @param string $query Search query
     * @param string $field Field name
     * @return array
     */
    public static function textSearch(string $query, string $field = 'q'): array
    {
        return [$field => $query];
    }

    /**
     * Build exact match filter
     *
     * @param mixed $value Value to match
     * @param string $field Field name
     * @return array
     */
    public static function exact($value, string $field): array
    {
        return [$field => $value];
    }

    /**
     * Build contains filter
     *
     * @param string $value Value to contain
     * @param string $field Field name
     * @return array
     */
    public static function contains(string $value, string $field): array
    {
        return ["{$field}__icontains" => $value];
    }

    /**
     * Build in filter
     *
     * @param array $values Values to match
     * @param string $field Field name
     * @return array
     */
    public static function in(array $values, string $field): array
    {
        return ["{$field}__in" => implode(',', $values)];
    }

    /**
     * Build ordering filter
     *
     * @param string $field Field to order by
     * @param string $direction Order direction (asc/desc)
     * @return array
     */
    public static function orderBy(string $field, string $direction = 'asc'): array
    {
        $prefix = $direction === 'desc' ? '-' : '';
        return ['order_by' => $prefix . $field];
    }

    /**
     * Build multiple ordering filter
     *
     * @param array $fields Array of field => direction pairs
     * @return array
     */
    public static function orderByMultiple(array $fields): array
    {
        $orderBy = [];
        
        foreach ($fields as $field => $direction) {
            $prefix = $direction === 'desc' ? '-' : '';
            $orderBy[] = $prefix . $field;
        }
        
        return ['order_by' => implode(',', $orderBy)];
    }

    /**
     * Build boolean filter
     *
     * @param bool $value Boolean value
     * @param string $field Field name
     * @return array
     */
    public static function boolean(bool $value, string $field): array
    {
        return [$field => $value ? 'true' : 'false'];
    }

    /**
     * Build null filter
     *
     * @param string $field Field name
     * @param bool $isNull Whether field should be null
     * @return array
     */
    public static function null(string $field, bool $isNull = true): array
    {
        $suffix = $isNull ? '__isnull' : '__isnull';
        return ["{$field}{$suffix}" => $isNull ? 'true' : 'false'];
    }

    /**
     * Build range filter
     *
     * @param mixed $min Minimum value
     * @param mixed $max Maximum value
     * @param string $field Field name
     * @return array
     */
    public static function range($min, $max, string $field): array
    {
        $filters = [];
        
        if ($min !== null) {
            $filters["{$field}__gte"] = $min;
        }
        
        if ($max !== null) {
            $filters["{$field}__lte"] = $max;
        }
        
        return $filters;
    }
}
