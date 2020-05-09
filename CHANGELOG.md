



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
