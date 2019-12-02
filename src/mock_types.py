from typing import List, Dict, Any

from pydantic import BaseModel, Schema


QueryStrings = Dict[str, List[str]]


class HttpRequest(BaseModel):
    method: str
    path: str
    query_string_parameters: QueryStrings = Schema(None, title='queryStringParameters', alias='queryStringParameters')


class HttpResponse(BaseModel):
    status_code: int = Schema(200, title='statusCode', alias='statusCode')
    headers: Dict[str, str] = None
    body: Any = Schema('', description='Body that will be returned')
    remaining_times: int = Schema(
        -1,
        title='remainingTimes',
        alias='remainingTimes',
        description='Number of times this mock will be returned until deleted. -1 means unlimited'
    )
    delay: int = Schema(0, description='How much milliseconds wait until response')


class CreateModel(BaseModel):
    httpRequest: HttpRequest
    httpResponse: HttpResponse


class MockedData(BaseModel):
    httpRequest: HttpRequest
    httpResponse: List[HttpResponse]
