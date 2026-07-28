.PHONY: lint lint-fix test

lint:
	uv run ruff check .
	uv run ruff format --check .
	uv run ty check

lint-fix:
	uv run ruff check --fix --exit-zero .
	uv run ruff format .
	uv run ty check

lint-unsafe-fix:
	uv run ruff check --fix --unsafe-fixes --exit-zero .
	uv run ruff format .
	uv run ty check

test:
	uv run pytest -vv tests
