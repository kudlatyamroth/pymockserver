import hashlib
import json
from typing import List, Tuple

from fastapi import FastAPI
from fastapi.routing import APIRoute

from mock_types import QueryStrings, HttpRequest


def dump_request(request: HttpRequest) -> str:
    return json.dumps(request.dict(), indent=2)


def request_hash(request: HttpRequest) -> str:
    request.body = request.body or ""
    return hashlib.md5(json.dumps(request.dict(), sort_keys=True).encode("utf-8")).hexdigest()


def query_params_to_http_qs(qs: List[Tuple[str, str]]) -> QueryStrings:
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
