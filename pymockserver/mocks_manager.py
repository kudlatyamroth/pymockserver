from typing import Dict, Optional

from database import db
from logger import logger
from mock_types import MockedData, CreatePayload, HttpResponse, HttpRequest
from utils import request_hash, dump_request

mocks: Dict[str, MockedData] = {}


def get_mock(http_request: HttpRequest) -> Optional[MockedData]:
    req_hash = request_hash(http_request)
    mock = db.get(req_hash)
    if mock is None:
        logger.info(f"Mock not found: {dump_request(http_request)}")
        return mock
    logger.info(f"Found mock for hash: {dump_request(http_request)}")
    return mock


def decrease_remaining_times(mock: MockedData, http_request: HttpRequest) -> HttpResponse:
    req_hash = request_hash(http_request)
    response = mock.httpResponse[0]
    if response.remaining_times == -1:
        return response
    if response.remaining_times > 1:
        mock.httpResponse[0].remaining_times -= 1
        db.set(req_hash, mock)
        logger.info(f"Decreased remaining times in first mocked response for hash: {dump_request(http_request)}")
        return response
    if len(mock.httpResponse) > 1:
        del mock.httpResponse[0]
        db.set(req_hash, mock)
        logger.info(f"Deleted first mocked response for hash: {dump_request(http_request)}")
        return response
    delete_mock(http_request)
    return response


def add_mock(payload: CreatePayload) -> MockedData:
    req_hash = request_hash(payload.httpRequest)
    mock = db.get(req_hash)
    if mock:
        mock.httpResponse.append(payload.httpResponse)
        logger.info(f"Append mock to hash: {dump_request(payload.httpRequest)}")
        db.set(req_hash, mock)
        return mock
    mock = MockedData(httpRequest=payload.httpRequest, httpResponse=[payload.httpResponse])
    db.set(req_hash, mock)
    logger.info(f"Added new mock for: {dump_request(payload.httpRequest)}")
    return mock


def get_mocks() -> Dict:
    return dict(db.all())


def delete_mock(http_request: HttpRequest) -> Optional[MockedData]:
    req_hash = request_hash(http_request)
    logger.info(f"Deleting mocks for hash: {dump_request(http_request)}")
    return db.delete(req_hash)


def purge_mocks() -> None:
    db.clear()
    logger.info("Clear all mocks")
