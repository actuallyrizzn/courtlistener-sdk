# CourtListener Python SDK — Troubleshooting (Unofficial)

This guide covers common issues, error messages, and debugging tips for the **unofficial** CourtListener Python SDK.

**⚠️ Important Notice**: This is an unofficial SDK developed by the community and is not affiliated with, endorsed by, or officially supported by CourtListener or Free Law Project.

## Table of Contents
- [Common Errors](#common-errors)
- [HTTP 202 Responses](#http-202-responses)
- [Attribute Errors](#attribute-errors)
- [Debugging Tools](#debugging-tools)
- [Getting Help](#getting-help)

---

## Common Errors

- `AuthenticationError`: Check your API token in `.env` or passed to the client
- `NotFoundError`: The resource does not exist or is restricted
- `RateLimitError`: Too many requests; wait and retry
- `APIError`: Other API errors; check the message for details

## HTTP 202 Responses

If you see HTTP 202 (Accepted), the API is rate limiting or processing your request asynchronously. Best practices:
- Wait and retry after a delay
- Use exponential backoff for repeated requests
- See [Advanced Usage](./advanced_usage.md#handling-rate-limits)

## Attribute Errors

If you see errors like `'Docket' object has no attribute 'case_name'`:
- Ensure you are using the correct data model (not a raw dict)
- Clean up `.pyc` files if you recently changed class definitions
- See `tests/manual_debug/` for debug scripts

## Debugging Tools

- Use scripts in `tests/manual_debug/` to debug endpoints, models, and API responses
- Check the [User Guide](./user_guide.md) for usage patterns

## Getting Help

- Review the [User Guide](./user_guide.md) and [API Reference](./api_reference.md)
- Open an issue or discussion on the project repository 