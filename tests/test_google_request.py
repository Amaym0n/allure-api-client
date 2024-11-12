from http import HTTPStatus

from api_client import APIClient


def test_google_request():
    APIClient(base_url='https://www.google.com', with_allure=False).send_request(method='GET', path='/',
                                                                                 status_code=HTTPStatus.OK)
