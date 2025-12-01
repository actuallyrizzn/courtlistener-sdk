# Error Handling Standards

This document defines the standard error handling patterns for the CourtListener SDK.

## Exception Types

### Python
- `CourtListenerError` - Base exception for all SDK errors
- `AuthenticationError` - Invalid or missing API token (401, 403)
- `NotFoundError` - Resource not found (404)
- `RateLimitError` - Rate limit exceeded (429)
- `ValidationError` - Input validation failed (400)
- `APIError` - General API errors (4xx, 5xx)
- `ConnectionError` - Network connection failures
- `TimeoutError` - Request timeout

### PHP
- `CourtListenerException` - Base exception for all SDK errors
- `AuthenticationException` - Invalid or missing API token (401, 403)
- `NotFoundException` - Resource not found (404)
- `RateLimitException` - Rate limit exceeded (429)
- `ServerException` - Server errors (5xx)

## Error Handling Patterns

### Python
1. **API Modules**: Should use `self.client.get()`, `self.client.post()`, etc.
2. **Client**: Handles all HTTP errors via `_handle_response()`
3. **Error Messages**: Should be user-friendly and include context when possible

### PHP
1. **API Modules**: Should use `$this->list()`, `$this->get()`, `$this->search()` from BaseApi
2. **BaseApi**: Routes to client's `makeRequest()` which handles errors
3. **Error Messages**: Should be user-friendly and consistent

## Status Code Mapping

- **200-299**: Success - return data
- **401**: AuthenticationError / AuthenticationException
- **403**: AuthenticationError / AuthenticationException
- **404**: NotFoundError / NotFoundException
- **429**: RateLimitError / RateLimitException (with retry logic)
- **500+**: APIError / ServerException
- **Other 4xx**: APIError / CourtListenerException

## Retry Logic

- **Network errors** (ConnectionError, TimeoutError): Retry with exponential backoff
- **429 Rate Limit**: Retry after delay (respect Retry-After header if present)
- **4xx Client errors**: Do not retry
- **5xx Server errors**: Retry with exponential backoff

## Best Practices

1. Always use client/base methods for requests (don't bypass error handling)
2. Preserve original exception context when re-raising
3. Include helpful error messages with context
4. Document exceptions in method docstrings/PHPDoc

