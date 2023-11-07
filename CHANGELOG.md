





## 2.1.0 (2023-11-07)

### Feat

- better readme
- add ruff dependency
- remove useless now gitpython and invoke
- remove useless scripts
- remove pre-commit dependency
- update dependencies and docker image

### Fix

- remove typescript client from version bump

## 2.0.2 (2021-08-05)

### Fix

- preload application in docker

## 2.0.1 (2021-08-05)

### Fix

- change deprecated use of logger warn method to warning

## 2.0.0 (2021-08-05)

### Feat

- handle partially match on headers
- handle exact and partially match on body
- add headers and body to HttpRequest type

### BREAKING CHANGE

- changing structure of fixtures and change in way it matches requests

## 1.9.0 (2021-07-27)

### Feat

- do not include version in helm package in release
- do not create volume storage for diskcache
- remove diskcache from dependency and remove its adapter
- add shared memory adapter and switch to it
- move logger, fixture and utils to tool module
- move manager to models module
- rename database to diskcache as it truly is and move it to adapters module
- move model types to models package

## 1.8.3 (2021-07-26)

### Fix

- creating dist dir during release build

## 1.8.2 (2021-07-26)

### Fix

- get rid of error with fetching tags

## 1.8.1 (2021-07-26)

### Fix

- run invoke by poetry for releasing openapi

## 1.8.0 (2021-07-26)

### Feat

- do not try to bump version of removed helm v2 files

## 1.7.1 (2021-01-21)

### Fix

- **helm**: remove typo in helm3

## 1.7.0 (2020-11-06)

### Feat

- load fixtures on start
- **helm**: add possibility to add fixture files loaded on start

## 1.6.5 (2020-05-13)

### Fix

- **logger**: remove duplicated app name in logs

### Refactor

- add missing types and better file names

## 1.6.4 (2020-05-13)

### Fix

- **docker**: change app dir and module name

## 1.6.3 (2020-05-09)

### Refactor

- add little change to use some features from py3.8

## 1.6.2 (2020-05-08)

### Refactor

- **imports**: change local imports to have prefix with pymockserver

## 1.6.1 (2020-05-06)

### Fix

- **typescript-client**: update packages to fix security warning

## 1.6.0 

### Feat

- **git**: remove bump2version as commitizen fill that gap
- **git**: add commitizen to dev dependencies and configure bump version with it

### Fix

- **typo**: rename settings dict in database model

### Refactor

- **helm**: fix typo in helm deployment

## 1.5.5 

### Refactor

- **diskcache**: fix typo when no specify database directory

### Perf

- **cache**: defaults to not limit memory media volume

## 1.5.4 

### Perf

- **gunicorn**: increase max_requests and jitter for workers
- **cache**: use memory storage for sqlite file, if it not exist use tmp dir
- **gunicorn**: limit workers to 4
- **cache**: mount memory storage for use with diskcache

## 1.5.3 

### Feat

- **logger**: setup logger

### Fix

- **pickle**: lock pickle_protocol on version 4

### Perf

- **cache**: disable cull and evict on diskcache

## 1.5.1 

### Perf

- **gunicorn**: limit max_requests and increase keepalive

## 1.4.0 

### Feat

- **cache**: add database layer, started and closed with fastapi

### Refactor

- **tests**: use diskcache in tests

### Perf

- **gunicorn**: remove concurrency limits

## 0.7.0 (2019-12-09)

## 0.6.0 (2019-12-03)

## 0.5.2 (2019-12-03)

## 0.5.1 (2019-12-03)

## 0.5.0 (2019-12-03)

## 0.4.0 (2019-12-02)

## 0.3.0 (2019-12-02)

## 0.2.0 (2019-12-02)
