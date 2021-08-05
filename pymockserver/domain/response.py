from typing import Any, Optional, cast

from pymockserver.domain.request import request_hash
from pymockserver.models import manager
from pymockserver.models.type import HttpRequest, HttpResponse, MatchEnum, MockData, MockedData
from pymockserver.tools.logger import logger


def is_partially_match_dict(body: Any, mock: dict[str, Any]) -> bool:
    for key, value in mock.items():
        if key not in body:
            return False
        if not is_partially_match(body.get(key), value):
            return False
    return True


def is_partially_match_list(body: Any, mock: list[Any]) -> bool:
    for value in mock:
        if not isinstance(mock, (str, int, float, bool, bytes)) and not any(
            [is_partially_match(x, value) for x in cast(list[Any], body)]
        ):
            return False
        if value not in body:
            return False
    return True


def is_partially_match(body: Any, mock: Any) -> bool:
    if type(mock) is not type(body):
        return False
    if mock is None and body is not None:
        return False
    if isinstance(mock, dict):
        if not is_partially_match_dict(body, mock):
            return False
    if isinstance(mock, list):
        if not is_partially_match_list(body, mock):
            return False
    if isinstance(mock, (str, int, float, bool, bytes)) and mock != body:
        return False
    return True


def is_body_match(request: Any, mock: MockData) -> bool:
    if mock.request.match_body_mode is None:
        return True
    if mock.request.match_body_mode == MatchEnum.exact:
        if request == mock.request.body:
            return True
    if mock.request.match_body_mode == MatchEnum.partially:
        if is_partially_match(request, mock.request.body):
            return True
    return False


def is_headers_match(request: Any, mock: MockData) -> bool:
    if mock.request.headers is None:
        return True
    if len(mock.request.headers) == 0:
        return True
    return is_partially_match(request, mock.request.headers)


def find_matching_response(request: HttpRequest, mocks: MockedData) -> tuple[Optional[int], Optional[HttpResponse]]:
    for resp_id, mock in enumerate(mocks):
        logger.info(f"Try to match\n{request.print()}\nagainst:\n{mock.request.print()}")
        if not is_body_match(request.body, mock):
            continue
        if not is_headers_match(request.headers, mock):
            continue
        return resp_id, mock.response
    return None, None


def retrieve_matching_response(mocks: MockedData, request: HttpRequest, req_hash: str) -> Optional[HttpResponse]:
    resp_id, response = find_matching_response(request, mocks)
    if resp_id is None or response is None:
        return None

    logger.info("mock matched")
    remaining_times = response.decrease_remaining_times()
    mocks[resp_id].response = response

    if remaining_times == 0 and len(mocks) <= 1:
        manager.delete_mock(req_hash)

    if remaining_times == 0 and len(mocks) > 1:
        del mocks[resp_id]
        manager.set_mocks(req_hash, mocks)
        logger.info(f"Deleted first mocked response for hash: {req_hash}")

    logger.info(f"Decreased remaining times in first mocked response for hash: {req_hash}")
    return response


async def get_mocked_response(http_request: HttpRequest) -> Optional[HttpResponse]:
    req_hash = request_hash(http_request)
    if (mock := manager.get_mock(req_hash)) is None:
        return None

    return retrieve_matching_response(mock, http_request, req_hash)
