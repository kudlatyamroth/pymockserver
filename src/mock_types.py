from typing import List, Dict, Any

from pydantic import BaseModel, Schema


QueryStrings = Dict[str, List[str]]


class HttpRequest(BaseModel):
    method: str = Schema("GET", description="Http method", example="GET")  # type: ignore
    path: str = Schema(..., description="Url path", example="/users")  # type: ignore
    query_string_parameters: QueryStrings = Schema(  # type: ignore
        None,
        title="queryStringParameters",
        alias="queryStringParameters",
        description="Query string parameters",
        example={"name": ["John"], "age": ["25", "30"],},
    )


class HttpResponse(BaseModel):
    status_code: int = Schema(  # type: ignore
        200, title="statusCode", alias="statusCode", description="Status code of mocked response", example=200,
    )
    headers: Dict[str, str] = Schema(  # type: ignore
        None, description="Headers included in mock response", example={"x-user": "John Doe",},
    )
    body: Any = Schema("", description="Body that will be returned", example='"{"users":["John","Dave"]}"')  # type: ignore
    remaining_times: int = Schema(  # type: ignore
        -1,
        title="remainingTimes",
        alias="remainingTimes",
        description="Number of times this mock will be returned until deleted. -1 means unlimited",
        example="-1",
    )
    delay: int = Schema(0, description="How much milliseconds wait until response", example="500")  # type: ignore


class CreatePayload(BaseModel):
    httpRequest: HttpRequest
    httpResponse: HttpResponse


class MockedData(BaseModel):
    httpRequest: HttpRequest
    httpResponse: List[HttpResponse]
