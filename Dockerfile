FROM python:3.11-alpine

LABEL maintainer="Karol Fuksiewicz <kfuks2@gmail.com>"

# dependencies
# Copy using poetry.lock* in case it doesn't exist yet
COPY ./pyproject.toml ./poetry.lock* /app/

ENV PIP_NO_CACHE_DIR=off
ENV PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apk add --no-cache --virtual .build-deps gcc libc-dev libffi-dev make \
    && apk add curl \
    && curl -sSL https://install.python-poetry.org | POETRY_HOME=/opt/poetry python \
        && cd /usr/local/bin \
        && ln -s /opt/poetry/bin/poetry \
        && poetry config virtualenvs.create false \
    && cd /app/ \
    && poetry install --no-root --no-dev \
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
ENV GUNICORN_CMD_ARGS '--preload --max-requests=300 --max-requests-jitter=300'
ENV MODULE_NAME 'pymockserver.main'
ENV PRELOAD 1

CMD ["/start.sh"]
