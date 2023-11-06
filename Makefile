.PHONY: lint lint-fix test

lint:
	poetry run ruff check .
	poetry run ruff format --check .
	poetry run mypy

lint-fix:
	poetry run ruff check --fix --exit-zero .
	poetry run ruff format .
	poetry run mypy

lint-unsafe-fix:
	poetry run ruff check --fix --unsafe-fixes --exit-zero .
	poetry run ruff format .
	poetry run mypy

test:
	poetry run pytest -vv tests
