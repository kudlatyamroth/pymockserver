.PHONY: lint lint-fix test

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run mypy

lint-fix:
	uv run ruff check --fix --exit-zero .
	uv run ruff format .
	uv run mypy

lint-unsafe-fix:
	uv run ruff check --fix --unsafe-fixes --exit-zero .
	uv run ruff format .
	uv run mypy

test:
	uv run pytest -vv tests
