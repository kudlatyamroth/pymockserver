FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

COPY pymockserver /app

RUN pip install --no-cache-dir email-validator==1.0.5

EXPOSE 80
