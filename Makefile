#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := `pwd`

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall


.PHONY: install-deps-with-dev
poetry-install-deps:
	poetry install --with dev


#* Linting
.PHONY: test
test:
	PYTHONPATH=$(PYTHONPATH) poetry run pytest -c pyproject.toml --cov-report=html --cov=src tests/

.PHONY: mypy
mypy:
	poetry run mypy --config-file pyproject.toml ./

.PHONY: black_check
black_check:
	poetry run black --diff --check .

.PHONY: pylint
pylint:
	poetry run pylint -j 4 src/

check-all: black_check pylint mypy test
