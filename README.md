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

# Table of contents

- [How it works](#how-it-works)
- [API reference](#api-reference)
  - [`GET /_meta/health`](#get-_metahealth)
  - [`POST /mockserver`](#post-mockserver)
  - [`GET /mockserver`](#get-mockserver)
  - [`DELETE /mockserver`](#delete-mockserver)
  - [`DELETE /mockserver/reset`](#delete-mockserverreset)
  - [Any other path (mocked route)](#any-other-path-mocked-route)
- [Request/response matching rules](#requestresponse-matching-rules)
- [Request options](#request-options)
- [Response options](#response-options)
- [Fixtures](#fixtures)
- [Architecture](#architecture)
- [Configuration (environment variables)](#configuration-environment-variables)
- [Running locally](#running-locally)
- [Development](#development)
- [Docker & Helm](#docker--helm)

# How it works

PyMockserver exposes a control API (`/mockserver`) that you use to register fake
("mocked") responses for arbitrary HTTP requests. Every other path/method that is
not one of the control endpoints is treated as a candidate for mock matching: the
server looks up a mock registered for that exact `method + path + queryStringParameters`
combination and, if found, additionally checks `headers`/`body` matching rules before
returning the configured response.

Registered mocks are kept in memory only (a plain dict, see
[Architecture](#architecture)) - restarting the process clears everything, unless
[fixtures](#fixtures) are used to preload them again on startup.

# API reference

The interactive OpenAPI/Swagger documentation is always available on a running
instance at `/docs` (and the raw schema at `/openapi.json`, also committed in this
repo as [`openapi.json`](./openapi.json)).

## `GET /_meta/health`

Health check endpoint, meant to be used as a readiness/liveness probe (see
`helm_v3/pymockserver/values.yaml`).

```shell
curl --request GET "http://pymockserver/_meta/health"
```

Response `200 OK`:
```json
{ "status": "ok" }
```

## `POST /mockserver`

Registers a new mock. Body has to match the `CreatePayload` schema: `httpRequest` +
`httpResponse` (see [Request options](#request-options) / [Response options](#response-options)).

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

And now request this mock like that:
```shell
curl --request GET "http://pymockserver/test"
```
which returns status code 200 and body:
```json
{
    "status": "ok"
}
```

If a mock with the exact same `method + path + queryStringParameters` already exists,
the new one is **appended to a FIFO queue** instead of replacing it - see
[Request/response matching rules](#requestresponse-matching-rules).

Response `201 Created`:
```json
{ "status": "ok" }
```

## `GET /mockserver`

Returns every currently registered mock, grouped by their internal hash key
(`method:path?queryString`).

```shell
curl --request GET "http://pymockserver/mockserver"
```

Response `200 OK`, e.g.:
```json
{
    "GET:/test?": [
        {
            "request": { "method": "GET", "path": "/test", "...": "..." },
            "response": { "status_code": 200, "...": "..." }
        }
    ]
}
```

## `DELETE /mockserver`

Deletes **all** mocks registered for a given `httpRequest` (method + path +
queryStringParameters). It removes the whole queue for that request signature at once,
not a single queued response.

```shell
curl --request DELETE "http://pymockserver/mockserver" --data '{
        "method": "GET",
        "path": "/test"
    }'
```

Response `200 OK`:
```json
{ "removed": [ /* the deleted mocks, or null if nothing matched */ ], "mocked": { /* remaining mocks, same shape as GET /mockserver */ } }
```

## `DELETE /mockserver/reset`

Deletes every registered mock at once.

```shell
curl --request DELETE "http://pymockserver/mockserver/reset"
```

Response `200 OK`:
```json
{ "status": "ok" }
```

## Any other path (mocked route)

Every request that doesn't hit one of the endpoints above (any method, any path) is
matched against the registered mocks and, if a match is found, the configured mocked
response is returned. If nothing matches, the server responds with `404 Not Found`
and `{"detail": "Not found matching response"}`.

# Request/response matching rules

1. **Lookup key**: incoming requests are looked up by an exact-match key built from
   `method`, `path` and `queryStringParameters` (see `request_hash` in
   `pymockserver/domain/request.py`). Query string values are compared as sets, order
   of values/keys doesn't matter, but every key/value pair has to be present.
2. **Queue of candidates**: several mocks can be registered for the very same
   `method + path + queryStringParameters`. They are checked **in the order they were
   created** and the first one whose `body`/`headers` match wins.
3. **Body matching** (`match_body_mode` on `httpRequest`):
   - not set (`None`, default) → body is ignored, any request body matches.
   - `exact` → the request body must be equal to the mocked `body`.
   - `partially` → the mocked `body` only needs to be a subset of the request body
     (recursively, for dicts/lists/scalars).
4. **Headers matching**: if `headers` is set on the mock, the request headers must
   contain those headers (partial/subset match, same algorithm as `partially` body
   matching). If not set (or empty), headers are ignored.
5. **`remainingTimes` bookkeeping**: every time a mock is matched, its
   `remainingTimes` counter is decreased (unless it's `-1`, meaning unlimited).
   When it reaches `0`:
   - if it was the only mock registered for that request signature, the whole entry
     is deleted;
   - if there are other queued mocks for the same signature, only the exhausted one
     is removed and the rest remain (and will be tried in order on the next request).
6. **`delay`**: if greater than `0`, the response is delayed by that many
   milliseconds (`asyncio.sleep`) before being returned.

# Request options

`httpRequest`:

| key    | example value | default | required | description                                                          |
|--------|---------------|---------|----------|----------------------------------------------------------------------|
| method | `"POST"`        | GET | - | Specify valid http request method, with which mock will be returned |
| path   | `"/test"`       | - | yes | Path at which mock can be requested |
| queryStringParameters | `{ "age": ["20"] }` | - | - | Parameters (map of string to list of strings) that need to be provided in the request to get this mock |
| headers | `{"x-user": "John"}` | - | - | Headers that needs to be provided in request to get this mock |
| body | `{"status": "ok"}` | - | - | Whole body or part of the body that needs to match to get this mock |
| match_body_mode | `"exact"` | `null` | - | Specify how to match body. `exact` - needs a perfect match, `partially` - needs only part of body to match, unset - body is ignored |

# Response options

`httpResponse`:

| key        | example value | default | required | description                                                          |
|------------|---------------|---------|----------|----------------------------------------------------------------------|
| statusCode | `400` | `200` | - | Http status code that response will return (`100`-`599`) |
| headers    | `{"x-user": "John"}` | - | - | Headers that response will have |
| body | `{"status": "ok"}` | `null` | - | Body that response will have |
| remainingTimes | `5` | `-1` | - | Defines how many times this mock can be matched and returned before it's automatically deleted. `-1` means this mock can be matched infinite times, and the only way to get rid of it is to manually delete it or clear all mocks |
| delay | `10` | `0` | - | If greater than 0, delays the response by that many milliseconds |

# Fixtures

PyMockserver can preload mocks on startup from files placed in `/etc/fixtures`
inside the container (see `FIXTURES_DIR` in `pymockserver/domain/fixture.py`). Both
`.yaml` and `.json` files are supported (any other extension is ignored), each file
containing a list of `httpRequest`/`httpResponse` objects (same schema as
`POST /mockserver`).

When deploying with the provided Helm chart, fixture files can be supplied through
the `fixtureFiles` value, which are mounted as files under `/etc/fixtures`, e.g.:
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

# Architecture

The project is a small [FastAPI](https://fastapi.tiangolo.com/) application, structured
in a light "hexagonal-ish" layout:

```
pymockserver/
├── main.py                # FastAPI app, lifespan (connects db + loads fixtures)
├── routers/
│   ├── meta.py             # /_meta/health
│   └── mockserver.py       # /mockserver CRUD + catch-all mock responder
├── domain/
│   ├── request.py          # incoming request -> HttpRequest model, hashing/serialization of the lookup key
│   ├── response.py         # matching logic (body/headers) + remainingTimes bookkeeping
│   └── fixture.py          # loading fixtures from /etc/fixtures on startup
├── models/
│   ├── type.py             # pydantic models: HttpRequest, HttpResponse, CreatePayload, MockData...
│   └── manager.py          # CRUD operations on top of the storage adapter
├── adapters/
│   └── shared_memory.py    # storage backend: a plain in-memory dict, single-process only (see below)
└── tools/
    ├── logger.py           # app logger configuration
    └── utils.py            # misc FastAPI helpers (operation IDs)
```

Key design point: the app runs as a **single uvicorn process** (no gunicorn, no
`--workers`), so mocks can simply be stored in a plain `dict` (see
`pymockserver/adapters/shared_memory.py`) - there is only ever one process, so
there's nothing to keep in sync across workers.

> [!IMPORTANT]
> The plain dict is safe without any locking *only* because of this
> single-process, single-event-loop design: every route handler that touches the
> store is `async def` (never a plain `def`, which Starlette would run in a
> thread pool), and asyncio is cooperative on a single thread - a coroutine only
> yields control at an `await`. The hot path that reads/matches/decrements/deletes
> mocks (`pymockserver/domain/response.py::retrieve_matching_response`) contains
> no `await` points, so it always runs atomically with respect to every other
> in-flight request, no matter how many requests are concurrent from the client's
> point of view.
>
> If a plain `def` handler that touches the store were ever added, or the app
> were changed to run real OS threads or multiple worker processes, this
> guarantee would break and explicit locking (or a shared/external store) would
> be needed again. Horizontal scaling is handled via Kubernetes `replicaCount`
> (see `helm_v3/pymockserver/values.yaml`) instead of multiple processes/threads
> within one container - mocks are not shared across pods, only within one.

# Configuration (environment variables)

These are consumed by `start.sh` (used when running via the Docker image), which
starts a single `uvicorn` process directly:

| variable | default | description |
|----------|---------|--------------|
| `MODULE_NAME` | `pymockserver.main` | Python module containing the FastAPI `app` |
| `VARIABLE_NAME` | `app` | Name of the FastAPI app object |
| `HOST` | `0.0.0.0` | Bind host |
| `PORT` | `80` | Bind port |
| `LOG_LEVEL` | `info` | Uvicorn log level |

Fixtures are read from a fixed path, `/etc/fixtures` (not configurable via
environment variable).

# Running locally

Requirements: Python `>=3.14` and [uv](https://docs.astral.sh/uv/).

```shell
uv sync
uv run uvicorn pymockserver.main:app --reload --port 8000
```

The app will be available on `http://localhost:8000`, with interactive docs on
`http://localhost:8000/docs`.

# Development

This project uses `ruff` for linting/formatting, [`ty`](https://docs.astral.sh/ty/)
for type checking, and `pytest` for tests. Common tasks are wired up in the `Makefile`:

```shell
make lint         # ruff check + ruff format --check + ty check
make lint-fix      # ruff check --fix + ruff format + ty check
make test          # pytest -vv tests
```

Commit messages follow [Conventional Commits](https://www.conventionalcommits.org/)
and versioning/changelog is managed by [Commitizen](https://commitizen-tools.github.io/commitizen/).

# Docker & Helm

A production-ready Docker image (Python 3.14 alpine, single uvicorn process) is
provided via the `Dockerfile`. A Helm v3 chart is available under `helm_v3/pymockserver`,
including readiness/liveness probes pointed at `/_meta/health` and support for mounting
[fixture files](#fixtures) via the `fixtureFiles` value.
