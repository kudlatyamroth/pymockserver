FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7

COPY main.py mock_types.py utils.py /app/

RUN pip install email-validator==1.0.5

EXPOSE 80

ENV WORKERS_PER_CORE 1
ENV WEB_CONCURRENCY 1
