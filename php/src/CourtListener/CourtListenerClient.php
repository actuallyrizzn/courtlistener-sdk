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
use CourtListener\Exceptions\RateLimitException;
use CourtListener\Exceptions\NotFoundException;
use CourtListener\Exceptions\ServerException;
use GuzzleHttp\Client;
use GuzzleHttp\Exception\GuzzleException;
use GuzzleHttp\Exception\RequestException;
use GuzzleHttp\Exception\ConnectException;
use GuzzleHttp\Exception\TooManyRedirectsException;
use GuzzleHttp\Exception\ClientException;
use GuzzleHttp\Exception\ServerException as GuzzleServerException;
use Dotenv\Dotenv;

/**
 * CourtListener PHP SDK Client
 * 
 * An unofficial PHP SDK for the CourtListener REST API.
 * 
 * @package CourtListener
 * @version 0.1.0
 * @author CourtListener SDK Community
 * @license AGPL-3.0-or-later
 */
class CourtListenerClient
{
    private Client $httpClient;
    private string $baseUrl;
    private string $apiToken;
    private array $defaultHeaders;
    private int $timeout;
    private int $maxRetries;
    private float $retryDelay;

    // API Endpoint Instances
    public AbaRatings $abaRatings;
    public Agreements $agreements;
    public Alerts $alerts;
    public Attorneys $attorneys;
    public Audio $audio;
    public Citations $citations;
    public Clusters $clusters;
    public Courts $courts;
    public Debts $debts;
    public DisclosurePositions $disclosurePositions;
    public DocketAlerts $docketAlerts;
    public DocketEntries $docketEntries;
    public Dockets $dockets;
    public Documents $documents;
    public Educations $educations;
    public Financial $financial;
    public FinancialDisclosures $financialDisclosures;
    public FjcIntegratedDatabase $fjcIntegratedDatabase;
    public Gifts $gifts;
    public Investments $investments;
    public Judges $judges;
    public NonInvestmentIncomes $nonInvestmentIncomes;
    public Opinions $opinions;
    public OpinionsCited $opinionsCited;
    public OriginatingCourtInformation $originatingCourtInformation;
    public Parties $parties;
    public People $people;
    public PoliticalAffiliations $politicalAffiliations;
    public Positions $positions;
    public RecapDocuments $recapDocuments;
    public RecapFetch $recapFetch;
    public RecapQuery $recapQuery;
    public Reimbursements $reimbursements;
    public RetentionEvents $retentionEvents;
    public Schools $schools;
    public Search $search;
    public Sources $sources;
    public SpouseIncomes $spouseIncomes;
    public Tag $tag;

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
            'User-Agent' => 'CourtListener-PHP-SDK/0.1.0',
            'Accept' => 'application/json',
        ];

        // Initialize HTTP client
        $this->httpClient = new Client([
            'base_uri' => $this->baseUrl,
            'timeout' => $this->timeout,
            'headers' => $this->defaultHeaders,
            'verify' => $config['verify_ssl'] ?? true, // Allow SSL verification to be disabled for testing
        ]);

        // Initialize API endpoints
        $this->initializeEndpoints();
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
     * Initialize all API endpoint instances
     */
    private function initializeEndpoints(): void
    {
        $this->abaRatings = new AbaRatings($this);
        $this->agreements = new Agreements($this);
        $this->alerts = new Alerts($this);
        $this->attorneys = new Attorneys($this);
        $this->audio = new Audio($this);
        $this->citations = new Citations($this);
        $this->clusters = new Clusters($this);
        $this->courts = new Courts($this);
        $this->debts = new Debts($this);
        $this->disclosurePositions = new DisclosurePositions($this);
        $this->docketAlerts = new DocketAlerts($this);
        $this->docketEntries = new DocketEntries($this);
        $this->dockets = new Dockets($this);
        $this->documents = new Documents($this);
        $this->educations = new Educations($this);
        $this->financial = new Financial($this);
        $this->financialDisclosures = new FinancialDisclosures($this);
        $this->fjcIntegratedDatabase = new FjcIntegratedDatabase($this);
        $this->gifts = new Gifts($this);
        $this->investments = new Investments($this);
        $this->judges = new Judges($this);
        $this->nonInvestmentIncomes = new NonInvestmentIncomes($this);
        $this->opinions = new Opinions($this);
        $this->opinionsCited = new OpinionsCited($this);
        $this->originatingCourtInformation = new OriginatingCourtInformation($this);
        $this->parties = new Parties($this);
        $this->people = new People($this);
        $this->politicalAffiliations = new PoliticalAffiliations($this);
        $this->positions = new Positions($this);
        $this->recapDocuments = new RecapDocuments($this);
        $this->recapFetch = new RecapFetch($this);
        $this->recapQuery = new RecapQuery($this);
        $this->reimbursements = new Reimbursements($this);
        $this->retentionEvents = new RetentionEvents($this);
        $this->schools = new Schools($this);
        $this->search = new Search($this);
        $this->sources = new Sources($this);
        $this->spouseIncomes = new SpouseIncomes($this);
        $this->tag = new Tag($this);
    }

    /**
     * Make an HTTP request to the CourtListener API
     *
     * @param string $method HTTP method
     * @param string $endpoint API endpoint
     * @param array $options Request options
     * @return array Response data
     * @throws CourtListenerException
     */
    public function makeRequest(string $method, string $endpoint, array $options = [])
    {
        $attempt = 0;
        $lastException = null;

        while ($attempt < $this->maxRetries) {
            try {
                $response = $this->httpClient->request($method, $endpoint, $options);
                return $this->handleResponse($response);
            } catch (ClientException $e) {
                $lastException = $e;
                $statusCode = $e->getResponse()->getStatusCode();
                
                // Don't retry on client errors (4xx)
                if ($statusCode >= 400 && $statusCode < 500) {
                    throw $this->handleClientException($e);
                }
                
                // Retry on 429 (rate limit)
                if ($statusCode === 429) {
                    $attempt++;
                    if ($attempt < $this->maxRetries) {
                        sleep($this->retryDelay * $attempt);
                        continue;
                    }
                    throw new RateLimitException('Rate limit exceeded. Please try again later.');
                }
                
                throw $this->handleClientException($e);
            } catch (GuzzleServerException $e) {
                $lastException = $e;
                $attempt++;
                if ($attempt < $this->maxRetries) {
                    sleep($this->retryDelay * $attempt);
                    continue;
                }
                throw new ServerException('Server error occurred. Please try again later.');
            } catch (ConnectException $e) {
                $lastException = $e;
                $attempt++;
                if ($attempt < $this->maxRetries) {
                    sleep($this->retryDelay * $attempt);
                    continue;
                }
                throw new CourtListenerException('Connection error: ' . $e->getMessage());
            } catch (GuzzleException $e) {
                throw new CourtListenerException('Request failed: ' . $e->getMessage());
            }
        }

        throw $lastException ?: new CourtListenerException('Request failed after maximum retries.');
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
     * Handle client exceptions
     *
     * @param ClientException $e
     * @return CourtListenerException
     */
    private function handleClientException(ClientException $e): CourtListenerException
    {
        $statusCode = $e->getResponse()->getStatusCode();
        $body = $e->getResponse()->getBody()->getContents();

        switch ($statusCode) {
            case 401:
                return new AuthenticationException('Authentication failed. Please check your API token.');
            case 403:
                return new AuthenticationException('Access forbidden. Please check your API token permissions.');
            case 404:
                return new NotFoundException('Resource not found.');
            case 429:
                return new RateLimitException('Rate limit exceeded. Please try again later.');
            default:
                return new CourtListenerException("Client error {$statusCode}: {$body}");
        }
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
        return sprintf('CourtListenerClient(api_token=%s, base_url=%s)', 
            substr($this->apiToken, 0, 8) . '...', 
            $this->baseUrl
        );
    }
}
