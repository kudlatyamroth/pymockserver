# PyMockserver

[![Release](https://github.com/kudlatyamroth/pymockserver/actions/workflows/release.yml/badge.svg)](https://github.com/kudlatyamroth/pymockserver/actions/workflows/release.yml)
[![Unittests](https://github.com/kudlatyamroth/pymockserver/actions/workflows/test.yaml/badge.svg)](https://github.com/kudlatyamroth/pymockserver/actions/workflows/test.yaml)

# Introduction

One more implementation of MockServer, but for simple tasks.
It aims to be simple and fast.

Main differences to other solutions like `https://www.mock-server.com/`:
- easier to create mock
- easier to delete mock
- faster create and get mock for request

# Usage

### Create mock

To create mock, just send post request to PyMockserver:

```shell
curl --request POST "http://pymockserver/mockserver" --data '{
        "httpRequest": {
            "method": "GET",
            "path": "/test"
        },
        "httpResponse": {
            "body": {
                "status": "ok"
            },
            "statusCode": 200,
            "remainingTimes": -1,
            "delay": 0
        }
    }'
```

And now to request for this mock like that:
```shell
curl --request GET "http://pymockserver/test"
```
and this will return status code 200 and body:
```json
{
    "status": "ok"
}
```

### Delete mock

Same as create mock, but request method DELETE. So to delete previous mock send request:
```shell
curl --request DELETE "http://pymockserver/mockserver" --data '{
        "method": "GET",
        "path": "/test"
    }'
```

### Delete all mock

To delete all mocks, just send delete request to `/mockserver/reset`:
```shell
curl --request DELETE "http://pymockserver/mockserver/reset"
```


### Get all mock

To get all mocks, just send get request to `/mockserver`:
```shell
curl --request GET "http://pymockserver/mockserver"
```

### Fixtures

PyMockserver has ability to load fixtures.
To provide fixtures for PyMockserver, just set fixtureFiles in helm values file, ex:
```yaml
fixtureFiles:
  fixtures.yaml: |
    - httpRequest:
        method: GET
        path: /test
        queryStringParameters:
      httpResponse:
        statusCode: 200
        body:
          status: "ok"
```

## Request options

httpRequest:

| key    | example value | default | required | description                                                          |
|--------|---------------|---------|----------|----------------------------------------------------------------------|
| method | `"POST"`        | GET | - | Specify valid http request method, with which mock will be returned |
| path   | `"/test"`       | - | yes | Path at which mock can be requested |
| queryStringParameters | `{ "age": [20] }` | - | - | Parameters that needs to be provided in request to get this mock |
| headers | `{"x-user": "John"}` | - | - | Headers that needs to be provided in request to get this mock |
| body | `{"status": "ok"}` | - | - | Whole body or part of the body that needs to match to get this mock |
| match_body_mode | `"exact"` | - | - | Specify how to match body. `exact` - will need perfect match, `partially` - needs only part of body to match |


httpResponse:

| key        | example value | default | required | description                                                          |
|------------|---------------|---------|----------|----------------------------------------------------------------------|
| statusCode | `400` | `200` | - | Http status code that response will return |
| headers    | `{"x-user": "John"}` | - | - | Headers that response will have |
| body | `{"status": "ok"}` | - | - | Body that response will have |
| remainingTimes | `5` | `-1` | - | Defines how many times this mock can be matched and returned before auto delete mock. If `-1` it means that this mock can be matched and returned infinite times, and only way to get rid of this mock is to manually delete it or clear all mocks |
| delay | `10` | `0` | - | If greater then 0, it will delay response for that time. Value is expressed in milliseconds |
