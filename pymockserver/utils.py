from typing import List, Optional, Tuple

from fastapi import FastAPI
from fastapi.routing import APIRoute

from pymockserver.mock_types import HttpRequest, QueryStrings


def join_query_string(qs: Optional[QueryStrings]):
    if qs is None:
        return ""
    sorted_dict = dict(sorted({key: ",".join(sorted(value)) for key, value in qs.items()}.items()))
    return "&".join([f"{key}={value}" for key, value in sorted_dict.items()])


def request_hash(request: HttpRequest):
    qs = join_query_string(request.query_string_parameters)
    return f"{request.method}:{request.path}?{qs}"


def query_params_to_http_qs(qs: List[Tuple[str, str]]):
    query_params: QueryStrings = {}
    for param in qs:
        qp = query_params.get(param[0])
        if qp:
            qp.append(param[1])
        else:
            query_params[param[0]] = [param[1]]
    return query_params


def use_route_names_as_operation_ids(app: FastAPI) -> None:
    """
    Simplify operation IDs so that generated API clients have simpler function
    names.
    """
    for route in app.routes:
        if isinstance(route, APIRoute):
            route.operation_id = route.name
