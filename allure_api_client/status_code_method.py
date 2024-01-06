import allure


def check_status_code(response, status_code: int) -> None:
    with allure.step('Checking the status of the request code'):
        assert response.status_code == status_code, \
            f"""Wrong status code, expected: {status_code}, received: {response.status_code}
                message: {response.text}"""
