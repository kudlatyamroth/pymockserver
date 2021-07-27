from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field

QueryStrings = dict[str, list[str]]
HeadersType = dict[str, str]
BodyType = Union[bool, str, int, dict[Any, Any], list[Any], None]


class MatchEnum(str, Enum):
    exact = "exact"
    partially = "partially"


class HttpRequest(BaseModel):
    method: str = Field("GET", description="Http method", example="GET")
    path: str = Field(..., description="Url path", example="/users")
    query_string_parameters: QueryStrings = Field(
        None,
        title="queryStringParameters",
        alias="queryStringParameters",
        description="Query string parameters",
        example={
            "name": ["John"],
            "age": ["25", "30"],
        },
    )
    headers: dict[str, str] = Field(
        None,
        description="Headers that would match in request",
        example={
            "x-user": "John Doe",
        },
    )
    body: Union[bool, str, int, dict[Any, Any], list[Any], None] = Field(
        "",
        description="Body that will be matched against request",
        example='{"users":["John","Dave"]}',
    )
    match_body_mode: Optional[MatchEnum] = Field(
        None,
        description="Specify mode with witch body will be matched in request",
        example="partially",
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
    headers: dict[str, str] = Field(
        None,
        description="Headers included in mock response",
        example={
            "x-user": "John Doe",
        },
    )
    body: Union[bool, str, int, dict[Any, Any], list[Any], None] = Field(
        None, description="Body that will be returned", example='{"users":["John","Dave"]}'
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


MockedData = list[list[HttpRequest, HttpResponse]]
