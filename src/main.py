import json
import logging
from typing import Dict

import uvicorn
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from starlette.status import HTTP_404_NOT_FOUND, HTTP_201_CREATED, HTTP_200_OK

from mock_types import HttpRequest, CreateModel
from utils import request_hash, query_params_to_http_qs

app = FastAPI()
logger = logging.getLogger("fastapi")

mocks: Dict[str, CreateModel] = {}


@app.post('/mockserver', status_code=HTTP_201_CREATED)
async def add_mock(body: CreateModel):
    req_hash = request_hash(body.httpRequest)
    mocks[req_hash] = body
    logger.warning(f'[MockServer] Added new mock for: {req_hash}')
    return {'status': 'ok'}


@app.get('/mockserver', status_code=HTTP_200_OK)
async def get_mocks():
    return mocks


@app.delete('/mockserver', status_code=HTTP_200_OK)
async def delete_routes(http_request: HttpRequest):
    req_hash = request_hash(http_request)
    logger.warning(f'[MockServer] Deleted mock for: {req_hash}')
    return {'removed': mocks.pop(req_hash), 'mocked': mocks}


@app.delete('/mockserver/reset', status_code=HTTP_200_OK)
async def clear_mocks():
    mocks.clear()
    logger.warning('[MockServer] Clear all mocks')
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

    mock = mocks.get(request_hash(http_request))
    if mock is None:
        response.status_code = HTTP_404_NOT_FOUND
        return {'code': HTTP_404_NOT_FOUND, 'status': 'Not found'}

    response.status_code = mock.httpResponse.status_code
    try:
        return json.loads(mock.httpResponse.body)
    except (json.JSONDecodeError, TypeError):
        return mock.httpResponse.body


if __name__ == '__main__':
    uvicorn.run('main:app', host='0.0.0.0', port=8000, reload=True, debug=True)
