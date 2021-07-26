from typing import Optional, cast

from pymockserver.database import db
from pymockserver.logger import logger
from pymockserver.models.type import CreatePayload, HttpResponse, MockedData

mocks: dict[str, MockedData] = {}


def get_mock(req_hash: str) -> Optional[MockedData]:
    mock = db.get(req_hash)
    if mock is None:
        logger.info(f"Mock not found: {req_hash}")
        return mock
    logger.info(f"Found mock for hash: {req_hash}")
    return cast(MockedData, mock)


def decrease_remaining_times(mock: MockedData, req_hash: str) -> HttpResponse:
    response = mock.httpResponse[0]
    if response.remaining_times == -1:
        return response
    if response.remaining_times > 1:
        mock.httpResponse[0].remaining_times -= 1
        db.set(req_hash, mock)
        logger.info(f"Decreased remaining times in first mocked response for hash: {req_hash}")
        return response
    if len(mock.httpResponse) > 1:
        del mock.httpResponse[0]
        db.set(req_hash, mock)
        logger.info(f"Deleted first mocked response for hash: {req_hash}")
        return response
    delete_mock(req_hash)
    return response


def set_mocks(req_hash: str, payload: MockedData) -> MockedData:
    db.set(req_hash, payload)
    logger.info(f"Set mocks for: {req_hash}")
    return payload


def add_mock(req_hash: str, payload: CreatePayload) -> MockedData:
    mock = db.get(req_hash)
    if mock:
        mock.httpResponse.append(payload.httpResponse)
        logger.info(f"Append mock to hash: {req_hash}")
        db.set(req_hash, mock)
        return cast(MockedData, mock)
    mock = MockedData(httpRequest=payload.httpRequest, httpResponse=[payload.httpResponse])
    db.set(req_hash, mock)
    logger.info(f"Added new mock for: {req_hash}")
    return mock


def get_mocks() -> dict[str, MockedData]:
    return dict(db.all())


def delete_mock(req_hash: str) -> Optional[MockedData]:
    logger.info(f"Deleting mocks for hash: {req_hash}")
    return db.delete(req_hash)


def purge_mocks() -> None:
    db.clear()
    logger.info("Clear all mocks")
