.PHONY: lint lint-fix test

lint:
	poetry run flake8
	poetry run isort --check-only pymockserver tests
	poetry run black --check pymockserver tests
	poetry run mypy

lint-fix:
	poetry run isort pymockserver tests
	poetry run black pymockserver tests
	poetry run flake8
	poetry run mypy

test:
	poetry run pytest -vv tests
