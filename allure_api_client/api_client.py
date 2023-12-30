from __future__ import annotations

import json
from http import HTTPStatus
from typing import Any
from typing import Callable
from typing import Generator

import allure
from httpx import Auth
from httpx import Client
from httpx import Cookies
from httpx import Request
from httpx import Response
from pydantic import HttpUrl


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


class BearerToken(Auth):
    def __init__(self, token: str) -> None:
        self.token = token
        if not self.token:
            raise Exception("The token is mandatory")

    def auth_flow(
            self, request: Request
    ) -> Generator[Request, Response, None]:
        request.headers['Authorization'] = f'Bearer {self.token}'
        yield request


class APIClient(Client):

    def __init__(
            self,
            base_url: HttpUrl,
            cookies: Cookies | None = None,
            auth: Callable[..., Any] | object | None = None,
            verify: bool = False,
    ) -> None:
        """
            Args:
                base_url (HttpUrl): The base URL to be used for requests.
                auth (Callable[..., Any] | object, optional): An authentication object or callable authentication object
                    that will be used for request authorization. If not provided, no authentication
                    will be used. Defaults to None.
                verify (bool, optional): Determines whether to verify SSL certificates for HTTPS
                    requests. Defaults to False.
        """
        super().__init__(auth=None, verify=verify, event_hooks={'request': [request_hook], 'response': [response_hook]})
        self.auth = auth
        self.cookies = cookies
        self.base_url = base_url

    def send_request(
            self,
            method: str,
            path: str,
            headers: dict | None = None,
            params: dict | None = None,
            data: dict | None = None,
            json: dict | None = None,
            files: dict | list | None = None,
            follow_redirects: bool = True,
            timeout=300,
            status_code: int = HTTPStatus.OK,
    ):
        """ Send HTTP-request """
        response = self.request(
            method=method,
            url=f'{self.base_url}{path}',
            headers=headers, params=params,
            data=data, json=json,
            files=files, auth=self.auth, cookies=self.cookies,
            follow_redirects=follow_redirects,
            timeout=timeout,
        )
        self.check_status_code(response=response, status_code=status_code)
        return response

    @staticmethod
    def check_status_code(response, status_code: int) -> None:
        with allure.step('Checking the status of the request code'):
            assert response.status_code == status_code, \
                f"""Wrong status code, expected: {status_code}, received: {response.status_code}
                    message: {response.text}"""
