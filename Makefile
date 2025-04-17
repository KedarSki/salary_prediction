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

#* Airflow (local standalone)
.PHONY: airflow-init
airflow-init:
	poetry run airflow db init
	poetry run airflow users create \
		--username admin \
		--firstname Admin \
		--lastname User \
		--role Admin \
		--email admin@example.com \
		--password admin

.PHONY: airflow-start
airflow-start:
	poetry run airflow webserver -p 8080 & \
	poetry run airflow scheduler

.PHONY: airflow-stop
airflow-stop:
	@pkill -f "airflow webserver" || true
	@pkill -f "airflow scheduler" || true

#* DAG test (manual)
.PHONY: dag-test
dag-test:
	poetry run python airflow/dags/salary_pipeline.dag.py

#* Docker Oracle (future use)
.PHONY: run-oracle-docker
run-oracle-docker:
	docker compose -f docker-compose.oracle.yml up -d

.PHONY: stop-oracle-docker
stop-oracle-docker:
	docker compose -f docker-compose.oracle.yml down

#* Docker Airflow (future use)
.PHONY: run-airflow-docker
run-airflow-docker:
	docker compose -f docker-compose.airflow.yml up -d

.PHONY: stop-airflow-docker
stop-airflow-docker:
	docker compose -f docker-compose.airflow.yml down

#* Helpers
.PHONY: wsl-path
wsl-path:
	@echo "Current WSL path: $(shell pwd)"
