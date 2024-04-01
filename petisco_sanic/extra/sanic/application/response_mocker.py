from typing import Any, Dict, Union
from sanic.exceptions import HTTPException
from sanic.request import Request


class ResponseMocker:
    """
    This class mocks the router response if the client sends a valid response value through request headers
    """

    def __init__(
        self,
        header_key: str = "X-Status-Code-Mock-Response",
        responses: Union[Dict[Union[int, str], Dict[str, Any]], None] = None,
    ) -> None:
        """
        header_key: by default "X-Status-Code-Mock-Response", but you can modify with this parameter.
        responses: This will be added automatically by the FastapiApplication if you define responses to router.
        """
        self.header_key = header_key
        self.responses = responses

    def __call__(self, request: Request) -> None:
        status_code = request.headers.get(self.header_key)
        if status_code:
            status_code = int(status_code)
            message = (
                self.responses.get(status_code, {}) if self.responses else {}
            )
            message["is_mocked"] = True
            raise HTTPException(message=message, status_code=status_code)
