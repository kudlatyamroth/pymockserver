from typing import cast

from pymockserver.adapters.shared_memory import db
from pymockserver.models.type import CreatePayload, MockData, MockedData
from pymockserver.tools.logger import logger

mocks: dict[str, MockedData] = {}


def get_mock(req_hash: str) -> MockedData | None:
    mock = db.get(req_hash)
    if mock is None:
        logger.info(f"Mock not found: {req_hash}")
        return mock
    logger.info(f"Found mock for hash: {req_hash}")
    return cast(MockedData, mock)


def set_mocks(req_hash: str, payload: MockedData) -> MockedData:
    db.set(req_hash, payload)
    logger.info(f"Set mocks for: {req_hash}")
    return payload


def add_mock(req_hash: str, payload: CreatePayload) -> MockedData:
    mock = db.get(req_hash)
    if mock:
        mock.append(MockData(request=payload.httpRequest, response=payload.httpResponse))
        logger.info(f"Append mock to hash: {req_hash} with request: {payload.httpRequest.print()}")
        db.set(req_hash, mock)
        return cast(MockedData, mock)
    mock = [MockData(request=payload.httpRequest, response=payload.httpResponse)]
    db.set(req_hash, mock)
    logger.info(f"Added new mock for: {req_hash} with request: {payload.httpRequest.print()}")
    return mock


def get_mocks() -> dict[str, MockedData]:
    return dict(db.all())


def delete_mock(req_hash: str) -> MockedData | None:
    logger.info(f"Deleting mocks for hash: {req_hash}")
    return db.delete(req_hash)


def purge_mocks() -> None:
    db.clear()
    logger.info("Clear all mocks")
