# allure-api-client

A lightweight API client built on top of httpx that adds convenient defaults for testing, plus optional Allure-friendly request/response logging. It ships with:
- Synchronous and asynchronous clients
- Optional Allure hooks to log cURL, request, and response details
- Simple Bearer token authentication helper
- Built-in status code verification in a single send_request call

## Requirements
- Python 3.11+

## Installation

```bash
pip install allure-api-client
```

If you want Allure reporting, also install Allure and its pytest plugin and generate a report when you run tests:
- Python dependency (already declared by this package): allure-pytest
- CLI: https://docs.qameta.io/allure/

Example test run with Allure report generation:
```bash
pytest --alluredir=./allure-results
allure serve ./allure-results
```

## Quick start (synchronous)

```python
from api_client import APIClient, BearerToken

client = APIClient(
    base_url="https://api.example.com",
    auth=BearerToken("YOUR_ACCESS_TOKEN"),  # optional
    verify=False,                            # optional, default False
    with_allure=True                         # optional, default True: enable Allure hooks
)

response = client.send_request(
    method="GET",
    path="/users",
    params={"page": 1},
    # By default, the client expects HTTP 200 (HTTPStatus.OK)
    # You can override the expectation per request:
    # status_code=201,
)
print(response.status_code)
print(response.json())
```

## Quick start (asynchronous)

```python
import asyncio
from api_client import AsyncAPIClient, BearerToken

async def main() -> None:
    async with AsyncAPIClient(
        base_url="https://api.example.com",
        auth=BearerToken("YOUR_ACCESS_TOKEN"),  # optional
        verify=False,                            # optional
        with_allure=True                         # optional
    ) as client:
        response = await client.send_request(
            method="GET",
            path="/users",
        )
        print(response.status_code)
        print(response.json())

asyncio.run(main())
```

## Authentication

Use a Bearer token if your API requires it:
```python
from api_client import BearerToken

auth = BearerToken("YOUR_ACCESS_TOKEN")
# pass it to APIClient/AsyncAPIClient via the auth parameter
```

## Allure integration
- By default, the clients are created with with_allure=True. The library will attach helpful request/response data to Allure, including a cURL snippet for easy reproduction.
- If you do not use Allure, set with_allure=False to use minimal internal hooks instead.

## Status code handling
- send_request verifies the response status code for you using the status_code parameter (default: 200 OK).
- If the actual status code does not match the expected value, an assertion-like error is raised coming from the underlying check.

Example expecting 201 Created:
```python
from api_client import APIClient

client = APIClient(base_url="https://api.example.com")
response = client.send_request(
    method="POST",
    path="/users",
    json={"name": "Alice"},
    status_code=201,
)
```

## Configuration reference
Common parameters on client initialization:
- base_url: Base URL string for your API (e.g., https://api.example.com)
- auth: Any httpx-compatible auth object; BearerToken helper is provided
- cookies: Optional httpx.Cookies to send on each request
- verify: Whether to verify TLS certificates (default False)
- with_allure: Enable/disable Allure hooks (default True)

Common parameters on send_request:
- method: HTTP method (e.g., "GET", "POST", ...)
- path: Path appended to base_url
- headers, params, data, json, files
- follow_redirects (default True)
- timeout (seconds, default 300)
- status_code: expected response status (default 200)

## Contributing
Contributions are welcome! Please open an issue or a pull request.

## License
Released under the MIT License. See [LICENSE](LICENSE).
