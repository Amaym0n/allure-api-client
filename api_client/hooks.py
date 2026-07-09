import logging
from shlex import quote

from httpx import Request
from httpx import Response

logger = logging.getLogger()


def build_curl(request: Request) -> str:
    parts = [
        'curl',
        '--insecure',
        '--location',
        '--request',
        request.method,
        quote(str(request.url)),
    ]

    for header, value in request.headers.multi_items():
        parts.extend(['--header', quote(f'{header}: {value}')])

    content = request.read()
    if content != b'':
        body = content if isinstance(content, str) else content.decode(errors='replace')
        parts.extend(['--data-raw', quote(body)])

    return ' '.join(parts)


def build_response_message(response: Response) -> str:
    response.read()
    return f'status_code: {response.status_code} \n  Content: \n {response.text}'


def print_request_hook(request: Request) -> None:
    print(build_curl(request=request))


def print_response_hook(response: Response) -> None:
    print(build_response_message(response=response))


def logger_request_hook(request: Request) -> None:
    logger.info(build_curl(request=request))


def logger_response_hook(response: Response) -> None:
    logger.info(build_response_message(response=response))


def allure_request_hook(request: Request) -> None:
    """
    This hook function is designed to be used with the httpx.Client event hooks for requests.
    It captures and logs the outgoing request details, including the method, URL, headers, and body.
    The request is formatted as a cURL command and attached to the Allure test report for easier debugging and reproduction.

    Args:
        request (Request): The httpx.Request object representing the outgoing HTTP request.

    Example:
        # To use this hook, attach it to a httpx.Client instance's event_hooks for requests
        client = httpx.Client(event_hooks={'request': [request_hook]})
    """
    import allure
    with allure.step(title=f'Request: [{request.method}] --> {request.url}'):
        curl = build_curl(request=request)
        allure.attach(curl, 'curl', allure.attachment_type.TEXT)


def allure_response_hook(response: Response) -> None:
    """
    This hook function is designed to be used with the httpx.Client event hooks for responses.
    It captures and logs the details of the incoming response, including the request method, request URL, status code,
    and response content. The response details are attached to the Allure test report for documentation and analysis.

    Args:
        response (Response): The httpx.Response object representing the incoming HTTP response.

    Example:
        # To use this hook, attach it to a httpx.Client instance's event_hooks for responses
        client = httpx.Client(event_hooks={'response': [response_hook]})
    """
    import allure
    with allure.step(title=f'Response: [{response.request.method}] --> {response.request.url}'):
        resp_message = build_response_message(response=response)
        allure.attach(resp_message, 'response', allure.attachment_type.TEXT)


def request_hook(
        request: Request,
        *,
        with_print: bool = True,
        with_allure: bool = True,
        with_logger: bool = True,
) -> None:
    if with_print:
        print_request_hook(request=request)
    if with_logger:
        logger_request_hook(request=request)
    if with_allure:
        allure_request_hook(request=request)


def response_hook(
        response: Response,
        *,
        with_print: bool = True,
        with_allure: bool = True,
        with_logger: bool = True,
) -> None:
    if with_print:
        print_response_hook(response=response)
    if with_logger:
        logger_response_hook(response=response)
    if with_allure:
        allure_response_hook(response=response)


async def async_request_hook(
        request: Request,
        *,
        with_print: bool = True,
        with_allure: bool = True,
        with_logger: bool = True,
) -> None:
    request_hook(
        request=request,
        with_print=with_print,
        with_allure=with_allure,
        with_logger=with_logger,
    )


async def async_response_hook(
        response: Response,
        *,
        with_print: bool = True,
        with_allure: bool = True,
        with_logger: bool = True,
) -> None:
    response_hook(
        response=response,
        with_print=with_print,
        with_allure=with_allure,
        with_logger=with_logger,
    )
