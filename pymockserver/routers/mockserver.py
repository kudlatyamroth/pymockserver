import json
import time

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

import mocks_manager
from mock_types import CreatePayload, HttpRequest
from utils import request_hash, query_params_to_http_qs


router = APIRouter()


@router.post("/mockserver", status_code=HTTP_201_CREATED)
async def add_mock(body: CreatePayload):
    """
    Create route mock

    If route is already mocked it will add it to queue.
    """
    req_hash = request_hash(body.httpRequest)
    mocks_manager.add_mock(req_hash, body)
    return {"status": "ok"}


@router.get("/mockserver", status_code=HTTP_200_OK)
async def get_all_mocks():
    """
    Get all mocked routes
    """
    return mocks_manager.get_mocks()


@router.delete("/mockserver", status_code=HTTP_200_OK)
async def delete_mock(http_request: HttpRequest):
    """
    Delete mock specified in request
    """
    req_hash = request_hash(http_request)
    return {"removed": mocks_manager.delete_mock(req_hash), "mocked": mocks_manager.get_mocks()}


@router.delete("/mockserver/reset", status_code=HTTP_200_OK)
async def clear_all_mocks():
    """
    Delete all mocked routes
    """
    mocks_manager.purge_mocks()
    return {"status": "ok"}


@router.post("{url_path:path}", include_in_schema=False)
@router.patch("{url_path:path}", include_in_schema=False)
@router.get("{url_path:path}", include_in_schema=False)
@router.put("{url_path:path}", include_in_schema=False)
@router.delete("{url_path:path}", include_in_schema=False)
async def mock_response(*, url_path: str = None, request: Request, response: Response):
    http_request = HttpRequest(
        method=request.method,
        path=url_path,
        queryStringParameters=query_params_to_http_qs(request.query_params.multi_items()),
    )

    req_hash = request_hash(http_request)
    mock_list = mocks_manager.get_mock(req_hash)
    if mock_list is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Not found")

    mock = mock_list.httpResponse[0]
    mocks_manager.decrease_remaining_times(mock_list.httpResponse, req_hash)

    if mock.headers:
        for header, value in mock.headers.items():
            response.headers[header] = value

    if mock.delay:
        time.sleep(mock.delay / 1000)

    response.status_code = mock.status_code
    try:
        return json.loads(mock.body)
    except (json.JSONDecodeError, TypeError):
        return mock.body
