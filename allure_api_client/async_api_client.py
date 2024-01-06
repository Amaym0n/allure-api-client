from __future__ import annotations

from http import HTTPStatus
from typing import Any
from typing import Callable

from httpx import AsyncClient, Response
from httpx import Cookies
from pydantic import HttpUrl

from allure_api_client.hooks import request_hook, response_hook
from allure_api_client.status_code_method import check_status_code


class AsyncAPIClient(AsyncClient):

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

    async def send_request(
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
    ) -> Response:
        """ Send HTTP-request """
        response = await self.request(
            method=method,
            url=f'{self.base_url}{path}',
            headers=headers, params=params,
            data=data, json=json,
            files=files, auth=self.auth, cookies=self.cookies,
            follow_redirects=follow_redirects,
            timeout=timeout,
        )
        check_status_code(response=response, status_code=status_code)
        return response
