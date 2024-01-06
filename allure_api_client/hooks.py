import json

import allure
from httpx import Response, Request


def request_hook(request: Request) -> None:
    """  """
    with allure.step(title=f'Request: [{request.method}] --> {request.url}'):
        headers = request.headers
        body = '' if request.content == b'' \
            else f" --data '{request.content if isinstance(request.content, str) else request.content.decode()}'"
        curl = f"curl --location '{request.url}' --header '{json.dumps(dict(headers))}'{body}"
        print(curl)
        allure.attach(curl, 'request', allure.attachment_type.TEXT)
    return


def response_hook(response: Response) -> None:
    """  """
    with allure.step(title=f'Response: [{response.request.method}] --> {response.request.url}'):
        response.read()
        resp_message = f'status_code: {response.status_code} \n  Content: \n {response.text}'
        print(resp_message)
        allure.attach(resp_message, 'response', allure.attachment_type.TEXT)
    return
