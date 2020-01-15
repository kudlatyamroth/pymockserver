from typing import List, Dict, Union

from pydantic import BaseModel, Field


QueryStrings = Dict[str, List[str]]


class HttpRequest(BaseModel):
    method: str = Field("GET", description="Http method", example="GET")
    path: str = Field(..., description="Url path", example="/users")
    query_string_parameters: QueryStrings = Field(
        None,
        title="queryStringParameters",
        alias="queryStringParameters",
        description="Query string parameters",
        example={"name": ["John"], "age": ["25", "30"],},
    )


class HttpResponse(BaseModel):
    status_code: int = Field(
        200,
        title="statusCode",
        alias="statusCode",
        description="Status code of mocked response",
        example=200,
        ge=100,
        le=599,
    )
    headers: Dict[str, str] = Field(
        None, description="Headers included in mock response", example={"x-user": "John Doe",},
    )
    body: Union[bool, str, int, Dict, List, None] = Field(
        "", description="Body that will be returned", example='{"users":["John","Dave"]}'
    )
    remaining_times: int = Field(
        -1,
        title="remainingTimes",
        alias="remainingTimes",
        description="Number of times this mock will be returned until deleted. -1 means unlimited",
        example="-1",
        ge=-1,
    )
    delay: int = Field(0, description="How much milliseconds wait until response", example="500", ge=0)


class CreatePayload(BaseModel):
    httpRequest: HttpRequest
    httpResponse: HttpResponse


MockList = List[HttpResponse]


class MockedData(BaseModel):
    httpRequest: HttpRequest
    httpResponse: MockList
