from typing import Generator

from httpx import Auth, Request, Response


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
