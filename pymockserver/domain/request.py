import json
from typing import Any, Optional

from starlette.requests import Request

from pymockserver.models.type import HttpRequest, QueryStrings


async def request_to_model(url_path: Optional[str], request: Request) -> HttpRequest:
    request_body = await decode_request(request)
    query_params = query_params_to_http_qs(request.query_params.multi_items())

    return HttpRequest(
        method=request.method,
        path=url_path,
        body=request_body,
        headers=request.headers,
        queryStringParameters=query_params,
    )


async def decode_request(request: Request) -> Any:
    try:
        return await request.json()
    except (json.JSONDecodeError, TypeError):
        return (await request.body()).decode("utf-8")


def query_params_to_http_qs(qs: list[tuple[str, str]]) -> QueryStrings:
    query_params: QueryStrings = {}
    for param in qs:
        if qp := query_params.get(param[0]):
            qp.append(param[1])
        else:
            query_params[param[0]] = [param[1]]
    return query_params


def serialize_query_string(qs: Optional[QueryStrings]) -> str:
    if qs is None:
        return ""
    sorted_dict = dict(sorted({key: ",".join(sorted(value)) for key, value in qs.items()}.items()))
    return "&".join([f"{key}={value}" for key, value in sorted_dict.items()])


def request_hash(request: HttpRequest) -> str:
    qs = serialize_query_string(request.query_string_parameters)
    return f"{request.method}:{request.path}?{qs}"
