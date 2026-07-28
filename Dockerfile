FROM ghcr.io/astral-sh/uv:0.11.25 AS uv

FROM python:3.12-alpine

LABEL maintainer="Karol Fuksiewicz <kfuks2@gmail.com>"

COPY --from=uv /uv /usr/local/bin/uv

# dependencies
# Copy using uv.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./uv.lock* /app/

ENV UV_NO_CACHE=1
ENV UV_PYTHON_DOWNLOADS=never
ENV UV_PROJECT_ENVIRONMENT=/usr/local

RUN apk add --no-cache --virtual .build-deps gcc libc-dev libffi-dev make \
    && cd /app/ \
    && uv sync --locked --no-dev \
    && apk del .build-deps gcc libc-dev libffi-dev make

# run setup
COPY ./start.sh /start.sh
RUN chmod +x /start.sh

COPY ./gunicorn_conf.py /gunicorn_conf.py

WORKDIR /app/

COPY pymockserver /app/pymockserver

ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 80

ENV WORKERS_PER_CORE 1
ENV WEB_CONCURRENCY 4
ENV KEEP_ALIVE 300
ENV TIMEOUT 300
ENV ACCESS_LOG ''
# `--preload` is required: it makes gunicorn import the app (and create the
# multiprocessing.Manager backing the in-memory mock store, see
# pymockserver/adapters/shared_memory.py) once in the master process *before*
# forking workers, so every worker shares the very same mock storage. Without
# it each worker would get its own, independent store.
ENV GUNICORN_CMD_ARGS '--preload --max-requests=300 --max-requests-jitter=300'
ENV MODULE_NAME 'pymockserver.main'
ENV PRELOAD 1

CMD ["/start.sh"]
