from sanic.response import HTTPResponse


def assert_http(response: HTTPResponse, expected_status_code: int) -> None:

    response_detail = (
        response.body
        if isinstance(response.body, bytes)
        else response.body.decode()
    )
    assert (
        response.status == expected_status_code
    ), f"{response.status} - {response_detail}"
