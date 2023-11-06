import asyncio
import json
from typing import Any

from fastapi import APIRouter, HTTPException
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_200_OK, HTTP_201_CREATED, HTTP_404_NOT_FOUND

from pymockserver.domain.request import request_hash, request_to_model
from pymockserver.domain.response import get_mocked_response
from pymockserver.models import manager
from pymockserver.models.type import CreatePayload, HttpRequest, MockedData

router = APIRouter(tags=["MockServer"])


@router.post("/mockserver", status_code=HTTP_201_CREATED)
async def add_mock(body: CreatePayload) -> dict[str, str]:
    """
    Create route mock

    If route is already mocked it will add it to queue.
    """
    req_hash = request_hash(body.httpRequest)
    manager.add_mock(req_hash, body)
    return {"status": "ok"}


@router.get("/mockserver", status_code=HTTP_200_OK)
async def get_all_mocks() -> dict[str, MockedData]:
    """
    Get all mocked routes
    """
    return manager.get_mocks()


@router.delete("/mockserver", status_code=HTTP_200_OK)
async def delete_mock(http_request: HttpRequest) -> dict[str, dict[str, MockedData] | MockedData | None]:
    """
    Delete mock specified in request
    """
    req_hash = request_hash(http_request)
    return {"removed": manager.delete_mock(req_hash), "mocked": manager.get_mocks()}


@router.delete("/mockserver/reset", status_code=HTTP_200_OK)
async def clear_all_mocks() -> dict[str, str]:
    """
    Delete all mocked routes
    """
    manager.purge_mocks()
    return {"status": "ok"}


@router.post("{url_path:path}", include_in_schema=False)
@router.patch("{url_path:path}", include_in_schema=False)
@router.get("{url_path:path}", include_in_schema=False)
@router.put("{url_path:path}", include_in_schema=False)
@router.delete("{url_path:path}", include_in_schema=False)
async def mock_response(*, url_path: str | None = None, request: Request, response: Response) -> Any:
    http_request = await request_to_model(url_path, request)
    mocked_response = await get_mocked_response(http_request)

    if mocked_response is None:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="Not found matching response")

    if mocked_response.headers:
        for header, value in mocked_response.headers.items():
            response.headers[header] = value

    if mocked_response.delay:
        await asyncio.sleep(mocked_response.delay / 1000)

    response.status_code = mocked_response.status_code
    try:
        if not isinstance(mocked_response.body, str | bytes | bytearray):
            raise TypeError("Body is not json string")
        return json.loads(mocked_response.body)
    except (json.JSONDecodeError, TypeError):
        return mocked_response.body
