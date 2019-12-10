import json
import time
from typing import Dict

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_404_NOT_FOUND

from logger import logger
from mock_types import CreatePayload, MockedData, HttpRequest
from utils import request_hash, query_params_to_http_qs


router = APIRouter()
mocks: Dict[str, MockedData] = {}


@router.post("/mockserver", status_code=HTTP_201_CREATED)
async def add_mock(body: CreatePayload):
    """
    Create route mock

    If route is already mocked it will add it to queue.
    """
    req_hash = request_hash(body.httpRequest)
    mock = mocks.get(req_hash)
    if mock:
        mock.httpResponse.append(body.httpResponse)
    else:
        mocks[req_hash] = MockedData(httpRequest=body.httpRequest, httpResponse=[body.httpResponse])
    logger.info(f"[MockServer] Added new mock for: {req_hash}")
    return {"status": "ok"}


@router.get("/mockserver", status_code=HTTP_200_OK)
async def get_all_mocks():
    """
    Get all mocked routes
    """
    return mocks


@router.delete("/mockserver", status_code=HTTP_200_OK)
async def delete_mock(http_request: HttpRequest):
    """
    Delete mock specified in request
    """
    req_hash = request_hash(http_request)
    logger.info(f"[MockServer] Deleted mock for: {req_hash}")
    return {"removed": mocks.pop(req_hash, None), "mocked": mocks}


@router.delete("/mockserver/reset", status_code=HTTP_200_OK)
async def clear_all_mocks():
    """
    Delete all mocked routes
    """
    mocks.clear()
    logger.info("[MockServer] Clear all mocks")
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
    mock_list = mocks.get(req_hash)
    if mock_list is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Not found")

    mock = mock_list.httpResponse[0]
    if 1 >= mock.remaining_times > -1:
        if len(mock_list.httpResponse) > 1:
            del mock_list.httpResponse[0]
        else:
            del mocks[req_hash]
    if mock.remaining_times > 1:
        mock.remaining_times -= 1

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


@router.get("/_meta/health", status_code=HTTP_200_OK, tags=["meta"])
async def health_check():
    """
    Status response for readiness and liveness probe
    """
    return {"status": "ok"}
