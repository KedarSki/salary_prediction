#* Variables
SHELL := /usr/bin/env bash
PYTHON := python
PYTHONPATH := $(shell pwd)

#* Poetry
.PHONY: poetry-download
poetry-download:
	curl -sSL https://install.python-poetry.org | $(PYTHON) -

.PHONY: poetry-remove
poetry-remove:
	curl -sSL https://install.python-poetry.org | $(PYTHON) - --uninstall

.PHONY: poetry-install-deps
poetry-install-deps:
	poetry install --with dev

#* Dev environment
.PHONY: activate
activate:
	poetry shell

#* Linting & Testing
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

.PHONY: check-all
check-all: black_check pylint mypy test

#* Airflow
.PHONY: run-airflow
run-airflow:
	cd airflow_local && docker compose up

.PHONY: stop-airflow
stop-airflow:
	cd airflow_local && docker compose down

#* CSV helper
.PHONY: copy-csv
copy-csv:
	mkdir -p airflow_local/dags/files
	cp data/salary.csv airflow_local/dags/files/salary.csv

#* PostgreSQL
.PHONY: psql-connect
psql-connect:
	psql -h localhost -p 5433 -U airflow -d salary_db

#* DAG local test (optional python testing hook, not Airflow scheduler)
.PHONY: etl-dag-test
etl-dag-test:
	poetry run python etl/helpers/transform.py