<?php

namespace CourtListener\Utils;

/**
 * Pagination utility class
 */
class Pagination
{
    /**
     * Get pagination parameters for API requests
     *
     * @param int $page Page number
     * @param int $perPage Items per page
     * @return array
     */
    public static function getParams(int $page = 1, int $perPage = 20): array
    {
        return [
            'page' => $page,
            'per_page' => $perPage,
        ];
    }

    /**
     * Get cursor-based pagination parameters
     *
     * @param string|null $cursor Cursor for pagination
     * @param int $perPage Items per page
     * @return array
     */
    public static function getCursorParams(?string $cursor = null, int $perPage = 20): array
    {
        $params = ['per_page' => $perPage];
        
        if ($cursor) {
            $params['cursor'] = $cursor;
        }
        
        return $params;
    }

    /**
     * Extract pagination info from API response
     *
     * @param array $response API response
     * @return array
     */
    public static function extractInfo(array $response): array
    {
        return [
            'count' => $response['count'] ?? 0,
            'next' => $response['next'] ?? null,
            'previous' => $response['previous'] ?? null,
            'current_page' => self::getCurrentPage($response),
            'total_pages' => self::getTotalPages($response),
            'per_page' => self::getPerPage($response),
        ];
    }

    /**
     * Get current page from response
     *
     * @param array $response API response
     * @return int
     */
    private static function getCurrentPage(array $response): int
    {
        if (isset($response['next'])) {
            $url = parse_url($response['next']);
            parse_str($url['query'] ?? '', $query);
            return max(1, ($query['page'] ?? 2) - 1);
        }
        
        return 1;
    }

    /**
     * Get total pages from response
     *
     * @param array $response API response
     * @return int
     */
    private static function getTotalPages(array $response): int
    {
        $count = $response['count'] ?? 0;
        $perPage = self::getPerPage($response);
        
        return $perPage > 0 ? ceil($count / $perPage) : 1;
    }

    /**
     * Get items per page from response
     *
     * @param array $response API response
     * @return int
     */
    private static function getPerPage(array $response): int
    {
        if (isset($response['next'])) {
            $url = parse_url($response['next']);
            parse_str($url['query'] ?? '', $query);
            return (int) ($query['per_page'] ?? 20);
        }
        
        return 20;
    }
}
