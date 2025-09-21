<?php

namespace CourtListener\Utils;

/**
 * Validation utilities for the CourtListener SDK
 * 
 * @package CourtListener\Utils
 */
class Validators
{
    /**
     * Validate a date string
     *
     * @param string|null $date Date string to validate
     * @param string $format Expected date format
     * @return bool
     */
    public static function validateDate(?string $date, string $format = 'Y-m-d'): bool
    {
        if ($date === null || $date === '') {
            return false;
        }

        $d = \DateTime::createFromFormat($format, $date);
        return $d && $d->format($format) === $date;
    }

    /**
     * Validate a citation string
     *
     * @param string|null $citation Citation to validate
     * @return bool
     */
    public static function validateCitation(?string $citation): bool
    {
        if ($citation === null || $citation === '') {
            return false;
        }

        // Basic citation validation patterns
        $patterns = [
            '/^\d+\s+U\.S\.\s+\d+$/',  // SCOTUS: "123 U.S. 456"
            '/^\d+\s+F\.\s*\d+$/',     // Federal Reporter: "123 F. 456"
            '/^\d+\s+F\.\s*Supp\.\s*\d+$/', // Federal Supplement: "123 F. Supp. 456"
            '/^\d+\s+[A-Za-z]+\.?\s*[A-Za-z]*\.?\s*\d+$/',   // State citations: "123 Cal. 456" or "123 N.Y. 456"
        ];

        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $citation)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Validate a docket number
     *
     * @param string|null $docketNumber Docket number to validate
     * @return bool
     */
    public static function validateDocketNumber(?string $docketNumber): bool
    {
        if ($docketNumber === null || $docketNumber === '') {
            return false;
        }

        // Common docket number patterns
        $patterns = [
            '/^\d+-\d+-\w+-\d+$/',       // 1-23-cv-456
            '/^\d+:\d+-\w+-\d+$/',       // 1:23-cv-456
            '/^\d+-\w+-\d+$/',           // 1-cv-456
            '/^\d+$/',                   // Simple number
            '/^\d+-\d+$/',               // 1-23
        ];

        foreach ($patterns as $pattern) {
            if (preg_match($pattern, $docketNumber)) {
                return true;
            }
        }

        return false;
    }

    /**
     * Validate a court ID
     *
     * @param string|null $courtId Court ID to validate
     * @return bool
     */
    public static function validateCourtId(?string $courtId): bool
    {
        if ($courtId === null || $courtId === '') {
            return false;
        }

        // Court ID patterns (alphanumeric with hyphens)
        return preg_match('/^[a-zA-Z0-9\-_]+$/', $courtId) === 1;
    }

    /**
     * Validate an API token
     *
     * @param string|null $token API token to validate
     * @return bool
     */
    public static function validateApiToken(?string $token): bool
    {
        if ($token === null || $token === '') {
            return false;
        }

        // API token should be at least 20 characters
        return strlen($token) >= 20;
    }

    /**
     * Validate an ID (positive integer)
     *
     * @param mixed $id ID to validate
     * @return bool
     */
    public static function validateId($id): bool
    {
        if (is_int($id)) {
            return $id > 0;
        }

        if (is_string($id)) {
            return ctype_digit($id) && (int)$id > 0;
        }

        return false;
    }

    /**
     * Validate a URL
     *
     * @param string|null $url URL to validate
     * @return bool
     */
    public static function validateUrl(?string $url): bool
    {
        if ($url === null || $url === '') {
            return false;
        }

        // Only allow HTTP and HTTPS URLs
        if (!filter_var($url, FILTER_VALIDATE_URL)) {
            return false;
        }

        $parsed = parse_url($url);
        return isset($parsed['scheme']) && in_array($parsed['scheme'], ['http', 'https']);
    }

    /**
     * Validate a required field
     *
     * @param mixed $value Value to validate
     * @param string $fieldName Field name for error messages
     * @return bool
     */
    public static function validateRequired($value, string $fieldName = 'field'): bool
    {
        if ($value === null) {
            return false;
        }

        if (is_string($value)) {
            return trim($value) !== '';
        }

        if (is_array($value)) {
            return !empty($value);
        }

        return true;
    }

    /**
     * Validate email address
     *
     * @param string|null $email Email to validate
     * @return bool
     */
    public static function validateEmail(?string $email): bool
    {
        if ($email === null || $email === '') {
            return false;
        }

        return filter_var($email, FILTER_VALIDATE_EMAIL) !== false;
    }

    /**
     * Validate phone number
     *
     * @param string|null $phone Phone to validate
     * @return bool
     */
    public static function validatePhone(?string $phone): bool
    {
        if ($phone === null || $phone === '') {
            return false;
        }

        // Remove common phone number formatting
        $cleaned = preg_replace('/[^\d]/', '', $phone);
        
        // US phone numbers should be 10 or 11 digits
        return strlen($cleaned) >= 10 && strlen($cleaned) <= 11;
    }

    /**
     * Validate a case name
     *
     * @param string|null $caseName Case name to validate
     * @return bool
     */
    public static function validateCaseName(?string $caseName): bool
    {
        if ($caseName === null || $caseName === '') {
            return false;
        }

        // Case name should be at least 3 characters and contain letters
        return strlen(trim($caseName)) >= 3 && preg_match('/[a-zA-Z]/', $caseName);
    }

    /**
     * Validate a judge name
     *
     * @param string|null $judgeName Judge name to validate
     * @return bool
     */
    public static function validateJudgeName(?string $judgeName): bool
    {
        if ($judgeName === null || $judgeName === '') {
            return false;
        }

        // Judge name should be at least 5 characters and contain letters
        return strlen(trim($judgeName)) >= 5 && preg_match('/[a-zA-Z]/', $judgeName);
    }

    /**
     * Validate a search query
     *
     * @param string|null $query Search query to validate
     * @return bool
     */
    public static function validateSearchQuery(?string $query): bool
    {
        if ($query === null || $query === '') {
            return false;
        }

        // Search query should be at least 2 characters
        return strlen(trim($query)) >= 2;
    }

    /**
     * Validate pagination parameters
     *
     * @param array $params Pagination parameters
     * @return bool
     */
    public static function validatePaginationParams(array $params): bool
    {
        if (isset($params['page']) && (!is_int($params['page']) || $params['page'] < 1)) {
            return false;
        }

        if (isset($params['per_page']) && (!is_int($params['per_page']) || $params['per_page'] < 1 || $params['per_page'] > 100)) {
            return false;
        }

        return true;
    }

    /**
     * Validate date range parameters
     *
     * @param array $params Date range parameters
     * @return bool
     */
    public static function validateDateRangeParams(array $params): bool
    {
        $startDate = $params['date_created__gte'] ?? $params['date_filed__gte'] ?? null;
        $endDate = $params['date_created__lte'] ?? $params['date_filed__lte'] ?? null;

        if ($startDate && !self::validateDate($startDate)) {
            return false;
        }

        if ($endDate && !self::validateDate($endDate)) {
            return false;
        }

        if ($startDate && $endDate) {
            $start = \DateTime::createFromFormat('Y-m-d', $startDate);
            $end = \DateTime::createFromFormat('Y-m-d', $endDate);
            
            if ($start && $end && $start > $end) {
                return false;
            }
        }

        return true;
    }

    /**
     * Validate filter parameters
     *
     * @param array $filters Filter parameters
     * @return bool
     */
    public static function validateFilters(array $filters): bool
    {
        // Validate pagination
        if (!self::validatePaginationParams($filters)) {
            return false;
        }

        // Validate date range
        if (!self::validateDateRangeParams($filters)) {
            return false;
        }

        // Validate search query if present
        if (isset($filters['q']) && !self::validateSearchQuery($filters['q'])) {
            return false;
        }

        return true;
    }
}
