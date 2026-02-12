<?php

namespace CourtListener;

use CourtListener\Api\AbaRatings;
use CourtListener\Api\Agreements;
use CourtListener\Api\Alerts;
use CourtListener\Api\Attorneys;
use CourtListener\Api\Audio;
use CourtListener\Api\Citations;
use CourtListener\Api\Clusters;
use CourtListener\Api\Courts;
use CourtListener\Api\Debts;
use CourtListener\Api\DisclosurePositions;
use CourtListener\Api\DocketAlerts;
use CourtListener\Api\DocketEntries;
use CourtListener\Api\Dockets;
use CourtListener\Api\Documents;
use CourtListener\Api\Educations;
use CourtListener\Api\Financial;
use CourtListener\Api\FinancialDisclosures;
use CourtListener\Api\FjcIntegratedDatabase;
use CourtListener\Api\Gifts;
use CourtListener\Api\Investments;
use CourtListener\Api\Judges;
use CourtListener\Api\NonInvestmentIncomes;
use CourtListener\Api\Opinions;
use CourtListener\Api\OpinionsCited;
use CourtListener\Api\OriginatingCourtInformation;
use CourtListener\Api\Parties;
use CourtListener\Api\People;
use CourtListener\Api\PoliticalAffiliations;
use CourtListener\Api\Positions;
use CourtListener\Api\RecapDocuments;
use CourtListener\Api\RecapFetch;
use CourtListener\Api\RecapQuery;
use CourtListener\Api\Reimbursements;
use CourtListener\Api\RetentionEvents;
use CourtListener\Api\Schools;
use CourtListener\Api\Search;
use CourtListener\Api\Sources;
use CourtListener\Api\SpouseIncomes;
use CourtListener\Api\Tag;
use CourtListener\Exceptions\CourtListenerException;
use CourtListener\Exceptions\AuthenticationException;
use GuzzleHttp\Client;
use GuzzleHttp\Promise\PromiseInterface;
use GuzzleHttp\Promise\Utils;
use Dotenv\Dotenv;

/**
 * Async CourtListener PHP SDK Client
 * 
 * Provides promise-based async methods using Guzzle's async interface.
 * This allows for concurrent requests and non-blocking I/O.
 * 
 * @package CourtListener
 * @version 0.1.0
 */
class AsyncCourtListenerClient
{
    private Client $httpClient;
    private string $baseUrl;
    private string $apiToken;
    private array $defaultHeaders;
    private int $timeout;
    private int $maxRetries;
    private float $retryDelay;

    /**
     * Constructor
     *
     * @param array $config Configuration options
     * @throws CourtListenerException
     */
    public function __construct(array $config = [])
    {
        // Load environment variables
        $this->loadEnvironmentVariables();

        // Set configuration
        $this->baseUrl = $config['base_url'] ?? $_ENV['COURTLISTENER_BASE_URL'] ?? 'https://www.courtlistener.com/api/rest/v4/';
        $this->apiToken = $config['api_token'] ?? $_ENV['COURTLISTENER_API_TOKEN'] ?? '';
        $this->timeout = $config['timeout'] ?? 30;
        $this->maxRetries = $config['max_retries'] ?? 3;
        $this->retryDelay = $config['retry_delay'] ?? 1.0;

        // Validate API token
        if (empty($this->apiToken)) {
            throw new AuthenticationException('API token is required. Set COURTLISTENER_API_TOKEN environment variable or pass api_token in config.');
        }

        // Set default headers
        $this->defaultHeaders = [
            'Authorization' => 'Token ' . $this->apiToken,
            'Content-Type' => 'application/json',
            'User-Agent' => 'CourtListener-PHP-SDK-Async/0.1.0',
            'Accept' => 'application/json',
        ];

        // Initialize HTTP client
        $this->httpClient = new Client([
            'base_uri' => $this->baseUrl,
            'timeout' => $this->timeout,
            'headers' => $this->defaultHeaders,
            'verify' => $config['verify_ssl'] ?? true,
        ]);
    }

    /**
     * Load environment variables from .env file
     */
    private function loadEnvironmentVariables(): void
    {
        $envFile = dirname(__DIR__, 3) . '/.env';
        if (file_exists($envFile)) {
            $dotenv = Dotenv::createImmutable(dirname($envFile));
            $dotenv->load();
        }
    }

    /**
     * Make an async HTTP request that returns a promise
     *
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array $options Request options
     * @return PromiseInterface
     */
    public function makeRequestAsync(string $method, string $endpoint, array $options = []): PromiseInterface
    {
        return $this->httpClient->requestAsync($method, $endpoint, $options)
            ->then(
                function ($response) {
                    return $this->handleResponse($response);
                },
                function ($exception) {
                    return $this->handleException($exception);
                }
            );
    }

    /**
     * Make multiple async requests concurrently
     *
     * @param array $requests Array of request configurations [['method' => 'GET', 'endpoint' => 'courts/', 'options' => []], ...]
     * @return PromiseInterface Promise that resolves to array of responses
     */
    public function makeRequestsBatch(array $requests): PromiseInterface
    {
        $promises = [];
        
        foreach ($requests as $key => $request) {
            $method = $request['method'] ?? 'GET';
            $endpoint = $request['endpoint'] ?? '';
            $options = $request['options'] ?? [];
            
            $promises[$key] = $this->makeRequestAsync($method, $endpoint, $options);
        }
        
        return Utils::settle($promises);
    }

    /**
     * Wait for all promises to resolve
     *
     * @param array $promises Array of PromiseInterface objects
     * @return array Array of resolved values
     */
    public function awaitAll(array $promises): array
    {
        return Utils::unwrap($promises);
    }

    /**
     * GET request that returns a promise
     *
     * @param string $endpoint API endpoint
     * @param array $params Query parameters
     * @return PromiseInterface
     */
    public function getAsync(string $endpoint, array $params = []): PromiseInterface
    {
        $options = [];
        if (!empty($params)) {
            $options['query'] = $params;
        }
        
        return $this->makeRequestAsync('GET', $endpoint, $options);
    }

    /**
     * POST request that returns a promise
     *
     * @param string $endpoint API endpoint
     * @param array $data Request body data
     * @return PromiseInterface
     */
    public function postAsync(string $endpoint, array $data = []): PromiseInterface
    {
        $options = [];
        if (!empty($data)) {
            $options['json'] = $data;
        }
        
        return $this->makeRequestAsync('POST', $endpoint, $options);
    }

    /**
     * PUT request that returns a promise
     *
     * @param string $endpoint API endpoint
     * @param array $data Request body data
     * @return PromiseInterface
     */
    public function putAsync(string $endpoint, array $data = []): PromiseInterface
    {
        $options = [];
        if (!empty($data)) {
            $options['json'] = $data;
        }
        
        return $this->makeRequestAsync('PUT', $endpoint, $options);
    }

    /**
     * PATCH request that returns a promise
     *
     * @param string $endpoint API endpoint
     * @param array $data Request body data
     * @return PromiseInterface
     */
    public function patchAsync(string $endpoint, array $data = []): PromiseInterface
    {
        $options = [];
        if (!empty($data)) {
            $options['json'] = $data;
        }
        
        return $this->makeRequestAsync('PATCH', $endpoint, $options);
    }

    /**
     * DELETE request that returns a promise
     *
     * @param string $endpoint API endpoint
     * @return PromiseInterface
     */
    public function deleteAsync(string $endpoint): PromiseInterface
    {
        return $this->makeRequestAsync('DELETE', $endpoint);
    }

    /**
     * Handle HTTP response
     *
     * @param \Psr\Http\Message\ResponseInterface $response
     * @return array
     * @throws CourtListenerException
     */
    private function handleResponse($response)
    {
        $statusCode = $response->getStatusCode();
        $body = $response->getBody()->getContents();

        if ($statusCode >= 200 && $statusCode < 300) {
            // Return raw content for empty responses
            if (empty($body)) {
                return $body;
            }
            
            $data = json_decode($body, true);
            if (json_last_error() !== JSON_ERROR_NONE) {
                // Return raw content for invalid JSON
                return $body;
            }
            return $data;
        }

        throw new CourtListenerException("HTTP error {$statusCode}: {$body}");
    }

    /**
     * Handle exceptions from async requests
     *
     * @param \Throwable $exception
     * @throws CourtListenerException
     */
    private function handleException(\Throwable $exception)
    {
        throw new CourtListenerException('Async request failed: ' . $exception->getMessage(), $exception->getCode(), $exception);
    }

    /**
     * Get the HTTP client instance
     *
     * @return Client
     */
    public function getHttpClient(): Client
    {
        return $this->httpClient;
    }

    /**
     * Get the base URL
     *
     * @return string
     */
    public function getBaseUrl(): string
    {
        return $this->baseUrl;
    }

    /**
     * Get the API token
     *
     * @return string
     */
    public function getApiToken(): string
    {
        return $this->apiToken;
    }

    /**
     * String representation of the client
     *
     * @return string
     */
    public function __toString(): string
    {
        return sprintf('AsyncCourtListenerClient(api_token=%s, base_url=%s)', 
            substr($this->apiToken, 0, 8) . '...', 
            $this->baseUrl
        );
    }
}
