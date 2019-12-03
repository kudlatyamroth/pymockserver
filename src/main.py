import json
import logging
import time
from typing import Dict

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK

from mock_types import HttpRequest, CreatePayload, MockedData
from utils import request_hash, query_params_to_http_qs

app = FastAPI()
logger = logging.getLogger("fastapi")

mocks: Dict[str, MockedData] = {}


@app.post('/mockserver', status_code=HTTP_201_CREATED)
async def add_mock(body: CreatePayload):
    req_hash = request_hash(body.httpRequest)
    mock = mocks.get(req_hash)
    if mock:
        mock.httpResponse.append(body.httpResponse)
    else:
        mocks[req_hash] = MockedData(httpRequest=body.httpRequest, httpResponse=[body.httpResponse])
    logger.info(f'[MockServer] Added new mock for: {req_hash}')
    return {'status': 'ok'}


@app.get('/mockserver', status_code=HTTP_200_OK)
async def get_mocks():
    return mocks


@app.delete('/mockserver', status_code=HTTP_200_OK)
async def delete_routes(http_request: HttpRequest):
    req_hash = request_hash(http_request)
    logger.info(f'[MockServer] Deleted mock for: {req_hash}')
    return {'removed': mocks.pop(req_hash, None), 'mocked': mocks}


@app.delete('/mockserver/reset', status_code=HTTP_200_OK)
async def clear_mocks():
    mocks.clear()
    logger.info('[MockServer] Clear all mocks')
    return {'status': 'ok'}


@app.post('{url_path:path}', include_in_schema=False)
@app.patch('{url_path:path}', include_in_schema=False)
@app.get('{url_path:path}', include_in_schema=False)
@app.put('{url_path:path}', include_in_schema=False)
@app.delete('{url_path:path}', include_in_schema=False)
async def get_mocks(*, url_path: str = None, request: Request, response: Response):
    http_request = HttpRequest(
        method=request.method,
        path=url_path,
        queryStringParameters=query_params_to_http_qs(request.query_params.multi_items()),
    )

    req_hash = request_hash(http_request)
    mock_list = mocks.get(req_hash)
    if mock_list is None:
        response.status_code = HTTP_404_NOT_FOUND
        return {'code': HTTP_404_NOT_FOUND, 'status': 'Not found'}

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
        time.sleep(mock.delay/1000)

    response.status_code = mock.status_code
    try:
        return json.loads(mock.body)
    except (json.JSONDecodeError, TypeError):
        return mock.body


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, debug=True)
