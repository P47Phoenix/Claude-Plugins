# API Documentation

## OpenAPI/Swagger Specification Conventions

### Structure

An OpenAPI specification defines the contract of an API. Key sections:

- **info** -- API title, version, description, contact, license
- **servers** -- Base URLs for each environment (production, staging, sandbox)
- **paths** -- Endpoint definitions with methods, parameters, request bodies, and responses
- **components/schemas** -- Reusable data models (request/response objects)
- **components/securitySchemes** -- Authentication methods
- **tags** -- Logical grouping of endpoints by resource or feature area

### Conventions

- Write descriptions in complete sentences with proper grammar
- Use consistent naming: camelCase for JSON fields, kebab-case for URL paths, UPPER_SNAKE_CASE for enum values
- Define all response codes for every endpoint -- do not rely on generic defaults
- Include `example` values for every schema property -- examples are the most-read part of API docs
- Use `$ref` to reference shared schemas -- do not duplicate schema definitions
- Keep the spec file in version control alongside the API code -- the spec is the source of truth

---

## Endpoint Documentation Pattern

### Standard Structure for Each Endpoint

```
## [METHOD] /path/to/resource

[One-sentence description of what this endpoint does]

### Parameters

| Name | In | Type | Required | Description |
|------|-----|------|----------|-------------|
| id | path | string (UUID) | Yes | Unique identifier of the resource |
| include | query | string | No | Comma-separated list of related resources to include |

### Request Body

[Description of the request body, when it should be sent]

```json
{
  "name": "Example Widget",
  "description": "A detailed description",
  "category": "electronics",
  "price": 29.99
}
```

### Response

**200 OK**

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "name": "Example Widget",
  "description": "A detailed description",
  "category": "electronics",
  "price": 29.99,
  "created_at": "2025-03-15T10:30:00Z"
}
```

### Error Responses

| Status | Code | Description |
|--------|------|-------------|
| 400 | INVALID_REQUEST | Request body failed validation |
| 401 | UNAUTHORIZED | Missing or invalid authentication |
| 404 | NOT_FOUND | Resource with the specified ID does not exist |
| 422 | VALIDATION_ERROR | Request is well-formed but contains semantic errors |
```

### Documentation Completeness Checklist

- [ ] HTTP method and path
- [ ] One-sentence description of purpose
- [ ] All path, query, and header parameters documented
- [ ] Request body with example
- [ ] Success response with example
- [ ] All error responses with codes and descriptions
- [ ] Authentication requirements stated
- [ ] Rate limiting information if applicable

---

## Request/Response Examples

### Realistic Data

- Use realistic, plausible data in examples -- not "string", "test", or "foo"
- Use consistent data across examples: if a user is created in one example, reference the same user in related examples
- Include all fields in examples, even optional ones, so readers know what is available
- Date/time values should be in ISO 8601 format with timezone

### Multiple Scenarios

Provide examples for common scenarios:

- **Minimal request** -- Only required fields, showing the simplest valid request
- **Full request** -- All fields including optional ones, showing the complete capability
- **Error scenario** -- A request that triggers a specific error, with the error response

### Error Case Examples

```
### Example: Validation Error

**Request:**
POST /api/v1/widgets
Content-Type: application/json

{
  "name": "",
  "price": -5.00
}

**Response: 422 Unprocessable Entity**

{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      {
        "field": "name",
        "message": "Name must not be empty"
      },
      {
        "field": "price",
        "message": "Price must be greater than 0"
      }
    ]
  }
}
```

---

## Error Catalog

### Standard Error Response Format

All error responses should follow a consistent structure:

```json
{
  "error": {
    "code": "MACHINE_READABLE_CODE",
    "message": "Human-readable description of the error",
    "details": [],
    "request_id": "req_abc123"
  }
}
```

### Common Error Codes

| HTTP Status | Error Code | When Used |
|-------------|-----------|-----------|
| 400 | BAD_REQUEST | Malformed request syntax (invalid JSON, missing Content-Type) |
| 401 | UNAUTHORIZED | Missing, invalid, or expired authentication credentials |
| 403 | FORBIDDEN | Valid credentials but insufficient permissions |
| 404 | NOT_FOUND | Resource does not exist at the specified path |
| 409 | CONFLICT | Request conflicts with current state (duplicate resource, version conflict) |
| 422 | VALIDATION_ERROR | Request is well-formed but fails business validation |
| 429 | RATE_LIMITED | Too many requests, retry after the specified delay |
| 500 | INTERNAL_ERROR | Unexpected server error (do not expose internal details) |
| 503 | SERVICE_UNAVAILABLE | Server is temporarily unable to handle the request |

### Troubleshooting Guidance

For each error code, provide:
- What the error means in plain language
- Common causes
- How to fix it
- Example of a corrected request

---

## Authentication Documentation

### API Keys

```
### Authentication

This API uses API keys for authentication. Include your API key in the
`Authorization` header of every request:

    Authorization: Bearer YOUR_API_KEY

**Obtaining an API key:**
1. Log in to the developer portal at [URL]
2. Navigate to Settings > API Keys
3. Click "Create new key" and provide a description
4. Copy the key immediately -- it will not be shown again

**Key security:**
- Never expose API keys in client-side code or public repositories
- Rotate keys immediately if compromised
- Use separate keys for development and production
```

### OAuth 2.0 Flows

Document each supported flow:

- **Authorization Code** -- For server-side applications. Include the full redirect flow with code examples.
- **Client Credentials** -- For machine-to-machine communication. Include a token request example.
- **PKCE** -- For mobile and single-page applications. Include code verifier/challenge generation.

For each flow, provide:
- Step-by-step flow description
- Required parameters at each step
- Example requests and responses
- Token refresh procedure
- Error handling for expired/revoked tokens

### Bearer Tokens

```
### Using Bearer Tokens

After obtaining a token, include it in the Authorization header:

    Authorization: Bearer eyJhbGciOiJSUzI1NiIs...

**Token lifetime:** Access tokens expire after 1 hour.

**Refreshing tokens:**

POST /oauth/token
Content-Type: application/x-www-form-urlencoded

grant_type=refresh_token&refresh_token=YOUR_REFRESH_TOKEN&client_id=YOUR_CLIENT_ID
```

---

## Rate Limiting Documentation

### Documenting Limits

```
### Rate Limits

| Tier | Requests per minute | Requests per day |
|------|---------------------|------------------|
| Free | 60 | 1,000 |
| Pro | 600 | 50,000 |
| Enterprise | 6,000 | Unlimited |

Rate limits are applied per API key. Limits reset at the start of each window.
```

### Response Headers

```
### Rate Limit Headers

Every API response includes rate limit information:

| Header | Description |
|--------|-------------|
| X-RateLimit-Limit | Maximum requests allowed in the current window |
| X-RateLimit-Remaining | Requests remaining in the current window |
| X-RateLimit-Reset | UTC timestamp when the window resets |
| Retry-After | Seconds to wait before retrying (only on 429 responses) |
```

### Retry Guidance

```
### Handling Rate Limits

When you receive a 429 response:

1. Read the `Retry-After` header to determine wait time
2. Wait for the specified duration
3. Retry the request

**Best practices:**
- Implement exponential backoff for retries
- Cache responses to reduce request volume
- Batch requests where the API supports it
- Monitor your usage via the rate limit headers
```

---

## API Versioning Documentation

### Specifying the Version

```
### API Versioning

This API uses URL path versioning. The current version is v2.

    https://api.example.com/v2/widgets

### Available Versions

| Version | Status | End of Life |
|---------|--------|-------------|
| v2 | Current | -- |
| v1 | Deprecated | 2025-12-31 |
```

### Migration Guides Between Versions

For each version transition, provide:

- Summary of breaking changes
- Field-by-field mapping from old to new
- Code examples showing before (old version) and after (new version)
- Timeline: deprecation date, end-of-life date, shutdown date

---

## SDK and Client Library Documentation

### Patterns

- Provide quick-start examples for each supported language
- Show installation instructions (package manager command)
- Include initialization with authentication
- Show the most common operations (CRUD for the primary resource)
- Document error handling patterns specific to the SDK

### Example Structure

```
### Python SDK

**Installation:**
    pip install example-api-client

**Quick Start:**

    from example_api import Client

    client = Client(api_key="YOUR_API_KEY")

    # Create a widget
    widget = client.widgets.create(
        name="My Widget",
        category="electronics",
        price=29.99
    )

    # List widgets
    widgets = client.widgets.list(limit=10)

    # Handle errors
    try:
        widget = client.widgets.get("nonexistent-id")
    except client.NotFoundError:
        print("Widget not found")
```

### Consistency Across Languages

- Use the same example data across all language examples
- Document the same operations in the same order
- Include error handling in every language example
- Note language-specific conventions (naming, async patterns)
