import json
import time
from typing import Any, Optional, Union

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from pymockserver import managers
from pymockserver.models.type import CreatePayload, HttpRequest, MockedData
from pymockserver.utils import query_params_to_http_qs, request_hash

router = APIRouter(tags=["MockServer"])


@router.post("/mockserver", status_code=HTTP_201_CREATED)
async def add_mock(body: CreatePayload) -> dict[str, str]:
    """
    Create route mock

    If route is already mocked it will add it to queue.
    """
    req_hash = request_hash(body.httpRequest)
    managers.add_mock(req_hash, body)
    return {"status": "ok"}


@router.get("/mockserver", status_code=HTTP_200_OK)
async def get_all_mocks() -> dict[str, MockedData]:
    """
    Get all mocked routes
    """
    return managers.get_mocks()


@router.delete("/mockserver", status_code=HTTP_200_OK)
async def delete_mock(http_request: HttpRequest) -> dict[str, Union[Optional[MockedData], dict[str, MockedData]]]:
    """
    Delete mock specified in request
    """
    req_hash = request_hash(http_request)
    return {"removed": managers.delete_mock(req_hash), "mocked": managers.get_mocks()}


@router.delete("/mockserver/reset", status_code=HTTP_200_OK)
async def clear_all_mocks() -> dict[str, str]:
    """
    Delete all mocked routes
    """
    managers.purge_mocks()
    return {"status": "ok"}


@router.post("{url_path:path}", include_in_schema=False)
@router.patch("{url_path:path}", include_in_schema=False)
@router.get("{url_path:path}", include_in_schema=False)
@router.put("{url_path:path}", include_in_schema=False)
@router.delete("{url_path:path}", include_in_schema=False)
async def mock_response(*, url_path: Optional[str] = None, request: Request, response: Response) -> Any:
    http_request = HttpRequest(
        method=request.method,
        path=url_path,
        queryStringParameters=query_params_to_http_qs(request.query_params.multi_items()),
    )

    req_hash = request_hash(http_request)
    mock = managers.get_mock(req_hash)
    if mock is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Not found")

    mocked_response = managers.decrease_remaining_times(mock, req_hash)
    if mocked_response.headers:
        for header, value in mocked_response.headers.items():
            response.headers[header] = value

    if mocked_response.delay:
        time.sleep(mocked_response.delay / 1000)

    response.status_code = mocked_response.status_code
    try:
        if not isinstance(mocked_response.body, (str, bytes, bytearray)):
            raise TypeError("Body is not json string")
        return json.loads(mocked_response.body)
    except (json.JSONDecodeError, TypeError):
        return mocked_response.body
