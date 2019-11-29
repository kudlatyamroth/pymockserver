from typing import List, Dict, Any

from pydantic import BaseModel, Schema


class QueryString(BaseModel):
    name: str
    values: List[str]


class HttpRequest(BaseModel):
    method: str
    path: str
    query_string_parameters: List[QueryString] = Schema(None, alias='queryStringParameters')


class HttpResponse(BaseModel):
    status_code: int = Schema(200, alias='status-code')
    headers: List[Dict[str, str]] = None
    body: Any


class Times(BaseModel):
    remaining_times: int = Schema(None, alias='remainingTimes')
    unlimited: bool = True


class CreateModel(BaseModel):
    httpRequest: HttpRequest
    httpResponse: HttpResponse
    times: Times
