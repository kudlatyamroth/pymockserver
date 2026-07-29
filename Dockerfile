FROM ghcr.io/astral-sh/uv:0.11.25 AS uv

FROM python:3.14-alpine

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

WORKDIR /app/

COPY pymockserver /app/pymockserver

ENV PYTHONPATH=/app:$PYTHONPATH

EXPOSE 80

ENV MODULE_NAME 'pymockserver.main'

CMD ["/start.sh"]
