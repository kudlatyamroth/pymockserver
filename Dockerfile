FROM tiangolo/uvicorn-gunicorn-fastapi:python3.7-alpine3.8

COPY pymockserver /app

RUN pip install email-validator==1.0.5

EXPOSE 80

ENV WORKERS_PER_CORE 1
ENV WEB_CONCURRENCY 1

CMD /usr/local/bin/uvicorn --host 0.0.0.0 --port 80 main:app
