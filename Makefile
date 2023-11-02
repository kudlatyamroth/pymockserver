.PHONY: lint lint-fix test

lint:
	poetry run flake8
	poetry run isort --check-only pymockserver deploy tests
	poetry run black --check pymockserver deploy tests
	poetry run mypy

lint-fix:
	poetry run isort pymockserver tests
	poetry run black pymockserver deploy tests
	poetry run flake8
	poetry run mypy

test:
	poetry run pytest -vv tests
