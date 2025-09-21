# CourtListener SDK — Troubleshooting (Unofficial)

This guide covers common issues, error messages, and debugging tips for the **unofficial** CourtListener SDK for both Python and PHP.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Table of Contents
- [Common Errors](#common-errors)
- [HTTP 202 Responses](#http-202-responses)
- [Language-Specific Issues](#language-specific-issues)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

---

## Common Errors

**Python:**
- `AuthenticationError`: Check your API token in `.env` or passed to the client
- `NotFoundError`: The resource does not exist or is restricted
- `RateLimitError`: Too many requests; wait and retry
- `APIError`: Other API errors; check the message for details

**PHP:**
- `AuthenticationException`: Check your API token in `.env` or passed to the client
- `NotFoundException`: The resource does not exist or is restricted
- `RateLimitException`: Too many requests; wait and retry
- `ServerException`: Other API errors; check the message for details

## HTTP 202 Responses

If you see HTTP 202 (Accepted), the API is rate limiting or processing your request asynchronously. Best practices:
- Wait and retry after a delay
- Use exponential backoff for repeated requests
- See [Advanced Usage](./advanced_usage.md#handling-rate-limits)

## Language-Specific Issues

### Python Issues

**Attribute Errors:**
If you see errors like `'Docket' object has no attribute 'case_name'`:
- Ensure you are using the correct data model (not a raw dict)
- Clean up `.pyc` files if you recently changed class definitions
- See `python/tests/manual_debug/` for debug scripts

**Import Errors:**
- Ensure you're in the correct directory when running scripts
- Check that all dependencies are installed: `pip install -r requirements.txt`

### PHP Issues

**Class Not Found Errors:**
- Ensure Composer autoloading is working: `composer dump-autoload`
- Check that you're using the correct namespace: `use CourtListener\CourtListenerClient;`

**Method Not Found Errors:**
- Verify you're using the correct method names (camelCase for properties)
- Check the API reference for correct method signatures

**SSL Certificate Errors:**
- For testing, you can disable SSL verification: `['verify_ssl' => false]`
- For production, ensure proper SSL certificates are installed

**Memory Issues:**
- Increase PHP memory limit: `php -d memory_limit=512M your_script.php`
- Use pagination for large datasets

## Debugging Tools

**Python:**
- Use scripts in `python/tests/manual_debug/` to debug endpoints, models, and API responses
- Run tests: `python -m pytest`
- Check the [User Guide](./user_guide.md) for usage patterns

**PHP:**
- Run comprehensive test suite: `composer test`
- Use specific test categories: `composer test-unit`, `composer test-live`
- Check code quality: `composer stan`
- Debug with verbose output: `vendor/bin/phpunit --verbose`

## Getting Help

- Review the [User Guide](./user_guide.md) and [API Reference](./api_reference.md)
- Check language-specific documentation:
  - [Python README](../python/README.md)
  - [PHP README](../php/README.md)
- Open an issue or discussion on the project repository 