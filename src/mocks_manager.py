from typing import Dict, Optional

from logger import logger
from mock_types import MockedData, CreatePayload, MockList

mocks: Dict[str, MockedData] = {}


def get_mock(req_hash: str) -> Optional[MockedData]:
    mock = mocks.get(req_hash, None)
    if mock is None:
        logger.info(f"[MockServer] Mock not found: {req_hash}")
        return mock
    logger.info(f"[MockServer] Found mock for hash: {req_hash}")
    return mock


def decrease_remaining_times(mock_list: MockList, req_hash: str) -> None:
    mock = mock_list[0]
    if mock.remaining_times > 1:
        mock.remaining_times -= 1
        logger.info(f"[MockServer] Decreased remaining times in first mocked response for hash: {req_hash}")
        return
    if mock.remaining_times == -1:
        return
    if len(mock_list) > 1:
        del mock_list[0]
        logger.info(f"[MockServer] Deleted first mocked response for hash: {req_hash}")
        return
    delete_mock(req_hash)


def add_mock(req_hash: str, payload: CreatePayload) -> MockedData:
    mock = mocks.get(req_hash)
    if mock:
        mock.httpResponse.append(payload.httpResponse)
        logger.info(f"[MockServer] Append mock to hash: {req_hash}")
        return mock
    mocks[req_hash] = MockedData(httpRequest=payload.httpRequest, httpResponse=[payload.httpResponse])
    logger.info(f"[MockServer] Added new mock for: {req_hash}")
    return mocks[req_hash]


def get_mocks():
    return mocks


def delete_mock(req_hash: str) -> Optional[MockedData]:
    logger.info(f"[MockServer] Deleting mocks for hash: {req_hash}")
    return mocks.pop(req_hash, None)


def purge_mocks() -> None:
    mocks.clear()
    logger.info("[MockServer] Clear all mocks")
