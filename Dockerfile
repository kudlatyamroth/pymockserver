FROM tiangolo/uvicorn-gunicorn:python3.8-alpine3.10

RUN apk add --no-cache --virtual .build-deps gcc libc-dev make \
    && apk add curl \
    && apk del .build-deps gcc libc-dev make

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY pymockserver /app

EXPOSE 80

ENV WORKERS_PER_CORE 1
ENV WEB_CONCURRENCY 4
ENV KEEP_ALIVE 300
ENV TIMEOUT 300
ENV ACCESS_LOG ''
ENV GUNICORN_CMD_ARGS '--max-requests=300 --max-requests-jitter=300'
