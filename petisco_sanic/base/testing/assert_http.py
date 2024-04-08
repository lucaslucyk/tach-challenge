# from sanic.response import HTTPResponse
from sanic_testing.testing import TestingResponse


def decode_body(response: TestingResponse) -> str:
    return (
        response.body
        if isinstance(response.body, bytes)
        else response.body.decode()
    )


def assert_http(response: TestingResponse, expected_status_code: int) -> None:

    response_detail = (
        response.json
        if isinstance(response.json, dict)
        else decode_body(response)
    )
    assert (
        response.status == expected_status_code
    ), f"{response.status} - {response_detail}"
