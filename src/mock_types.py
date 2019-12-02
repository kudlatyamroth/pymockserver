from typing import List, Dict, Any

from pydantic import BaseModel, Schema


QueryStrings = Dict[str, List[str]]


class HttpRequest(BaseModel):
    method: str
    path: str
    query_string_parameters: QueryStrings = Schema(None, alias='queryStringParameters')


class HttpResponse(BaseModel):
    status_code: int = Schema(200, alias='statusCode')
    headers: List[Dict[str, str]] = None
    body: Any = Schema('', description='Body that will be returned')


class Times(BaseModel):
    remaining_times: int = Schema(None, alias='remainingTimes')
    unlimited: bool = True


class CreateModel(BaseModel):
    httpRequest: HttpRequest
    httpResponse: HttpResponse
    times: Times
