from typing import Dict, Optional

from database import db
from logger import logger
from mock_types import MockedData, CreatePayload, HttpResponse

mocks: Dict[str, MockedData] = {}


def get_mock(req_hash: str) -> Optional[MockedData]:
    mock = db.get(req_hash)
    if mock is None:
        logger.info(f"[MockServer] Mock not found: {req_hash}")
        return mock
    logger.info(f"[MockServer] Found mock for hash: {req_hash}")
    return mock


def decrease_remaining_times(mock: MockedData, req_hash: str) -> HttpResponse:
    response = mock.httpResponse[0]
    if response.remaining_times == -1:
        return response
    if response.remaining_times > 1:
        mock.httpResponse[0].remaining_times -= 1
        db.set(req_hash, mock)
        logger.info(f"[MockServer] Decreased remaining times in first mocked response for hash: {req_hash}")
        return response
    if len(mock.httpResponse) > 1:
        del mock.httpResponse[0]
        db.set(req_hash, mock)
        logger.info(f"[MockServer] Deleted first mocked response for hash: {req_hash}")
        return response
    delete_mock(req_hash)
    return response


def add_mock(req_hash: str, payload: CreatePayload) -> MockedData:
    mock = db.get(req_hash)
    if mock:
        mock.httpResponse.append(payload.httpResponse)
        logger.info(f"[MockServer] Append mock to hash: {req_hash}")
        db.set(req_hash, mock)
        return mock
    mock = MockedData(httpRequest=payload.httpRequest, httpResponse=[payload.httpResponse])
    db.set(req_hash, mock)
    logger.info(f"[MockServer] Added new mock for: {req_hash}")
    return mock


def get_mocks():
    return dict(db.all())


def delete_mock(req_hash: str) -> Optional[MockedData]:
    logger.info(f"[MockServer] Deleting mocks for hash: {req_hash}")
    return db.delete(req_hash)


def purge_mocks() -> None:
    db.clear()
    logger.info("[MockServer] Clear all mocks")
