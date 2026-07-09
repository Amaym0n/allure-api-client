from httpx import Request

from api_client.hooks import build_curl


def test_build_curl_get_without_body_or_custom_headers():
    curl = build_curl(Request('GET', 'https://example.com/users'))

    assert curl == 'curl --insecure --location --request GET https://example.com/users --header \'host: example.com\''


def test_build_curl_get_with_query_params():
    curl = build_curl(
        Request(
            'GET',
            'https://example.com/users',
            params={'page': '1', 'q': 'hello world'},
        )
    )

    assert "--request GET 'https://example.com/users?page=1&q=hello+world'" in curl


def test_build_curl_post_with_headers_and_json_body():
    curl = build_curl(
        Request(
            'POST',
            'https://example.com/users',
            headers={'Authorization': 'Bearer token'},
            json={'name': "O'Reilly"},
        )
    )

    assert '--request POST https://example.com/users' in curl
    assert "--header 'authorization: Bearer token'" in curl
    assert '--data-raw \'{"name":"O\'"\'"\'Reilly"}\'' in curl


def test_build_curl_patch_with_raw_body():
    curl = build_curl(Request('PATCH', 'https://example.com/users/1', content='raw body'))

    assert '--request PATCH https://example.com/users/1' in curl
    assert "--data-raw 'raw body'" in curl


def test_build_curl_delete_without_body():
    curl = build_curl(Request('DELETE', 'https://example.com/users/1'))

    assert curl == 'curl --insecure --location --request DELETE https://example.com/users/1 --header \'host: example.com\''
