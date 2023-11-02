import json
from enum import Enum
from typing import Any, Optional, Union

from pydantic import BaseModel, Field

QueryStrings = dict[str, list[str]] | None
HeadersType = dict[str, str]
BodyType = Union[bool, str, int, dict[Any, Any], list[Any], None]


class MatchEnum(str, Enum):
    exact = "exact"
    partially = "partially"


class HttpRequest(BaseModel):
    method: str = Field("GET", description="Http method", json_schema_extra={"examples": ["GET"]})
    path: str = Field(..., description="Url path", json_schema_extra={"examples": ["/users"]})
    query_string_parameters: QueryStrings = Field(
        None,
        title="queryStringParameters",
        alias="queryStringParameters",
        description="Query string parameters",
        json_schema_extra={
            "examples": [
                {
                    "name": ["John"],
                    "age": ["25", "30"],
                }
            ]
        },
    )
    headers: dict[str, str] | None = Field(
        None,
        description="Headers that would match in request",
        json_schema_extra={
            "examples": [
                {
                    "x-user": "John Doe",
                }
            ]
        },
    )
    body: Union[bool, str, int, dict[Any, Any], list[Any], None] = Field(
        "",
        description="Body that will be matched against request",
        json_schema_extra={"examples": ['{"users":["John","Dave"]}']},
    )
    match_body_mode: Optional[MatchEnum] = Field(
        None,
        description="Specify mode with witch body will be matched in request",
        json_schema_extra={"examples": ["partially"]},
    )

    def print(self) -> str:
        return json.dumps(self.model_dump(), indent=2)


class HttpResponse(BaseModel):
    status_code: int = Field(
        200,
        title="statusCode",
        alias="statusCode",
        description="Status code of mocked response",
        ge=100,
        le=599,
        json_schema_extra={"examples": [200]},
    )
    headers: dict[str, str] | None = Field(
        None,
        description="Headers included in mock response",
        json_schema_extra={
            "examples": [
                {
                    "x-user": "John Doe",
                }
            ]
        },
    )
    body: Union[bool, str, int, dict[Any, Any], list[Any], None] = Field(
        None,
        description="Body that will be returned",
        json_schema_extra={"examples": ['{"users":["John","Dave"]}']},
    )
    remaining_times: int = Field(
        -1,
        title="remainingTimes",
        alias="remainingTimes",
        description="Number of times this mock will be returned until deleted. -1 means unlimited",
        ge=-1,
        json_schema_extra={"examples": ["-1"]},
    )
    delay: int = Field(
        0, description="How much milliseconds wait until response", ge=0, json_schema_extra={"examples": ["500"]}
    )

    def decrease_remaining_times(self) -> int:
        if self.remaining_times == -1:
            return self.remaining_times
        if self.remaining_times > 1:
            self.remaining_times -= 1
            return self.remaining_times
        if 0 <= self.remaining_times <= 1:
            return 0
        return self.remaining_times


class CreatePayload(BaseModel):
    httpRequest: HttpRequest
    httpResponse: HttpResponse


class MockData(BaseModel):
    request: HttpRequest
    response: HttpResponse


MockedData = list[MockData]
