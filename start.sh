#! /usr/bin/env sh
set -e

MODULE_NAME=${MODULE_NAME:-pymockserver.main}
VARIABLE_NAME=${VARIABLE_NAME:-app}
APP_MODULE=${APP_MODULE:-"$MODULE_NAME:$VARIABLE_NAME"}

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}
LOG_LEVEL=${LOG_LEVEL:-info}

# Single process, no workers: the mock store is a plain in-memory dict (see
# pymockserver/adapters/shared_memory.py), so it can't be shared across
# multiple processes. Scale out via Kubernetes replicas instead, not via
# uvicorn/gunicorn worker processes.
exec uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" --log-level "$LOG_LEVEL" --loop uvloop --http httptools
