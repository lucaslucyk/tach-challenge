from typing import Iterable
from sanic.request import Request
from sanic.response import HTTPResponse

# def _add_cors_headers(response: HTTPResponse, methods: Iterable[str]) -> None:
#     allow_methods = list(set(methods))
#     if "OPTIONS" not in allow_methods:
#         allow_methods.append("OPTIONS")
#     headers = {
#         "Access-Control-Allow-Methods": ",".join(allow_methods),
#         "Access-Control-Allow-Origin": "tach.la",
#         "Access-Control-Allow-Credentials": "true",
#         "Access-Control-Allow-Headers": (
#             "origin, content-type, accept, "
#             "authorization, x-xsrf-token, x-request-id"
#         ),
#     }
#     response.headers.extend(headers)

# def add_cors_headers(request: Request, response: HTTPResponse):
#     methods = [method for method in request.route.methods]
#     _add_cors_headers(response, methods)


# Middleware para manejar CORS
async def add_cors_headers(request: Request, response: HTTPResponse):
    # Permitir solicitudes desde cualquier origen
    response.headers['Access-Control-Allow-Origin'] = '*'
    # Permitir los métodos HTTP especificados
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS, PUT, DELETE'
    # Permitir los encabezados especificados
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response