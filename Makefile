ifeq ($(OS),Windows_NT)
	DETECTED_OS := Windwos
else
	DETECTED_OS := $(shell uname)
endif

ifeq (${WORKON_HOME},)
	ENV := $(CURDIR)/.venv
else
	ENV := ${WORKON_HOME}
endif

ifeq ($(DETECTED_OS),Windows)
	BIN := $(ENV)/Scripts
else
	BIN := $(ENV)/bin
endif

PYTHON := $(BIN)/python
PIPENV_RUN := pipenv run
FLAKE8 := $(BIN)/flake8
COVERAGE := $(BIN)/coverage
BLACK := $(BIN)/black
MANAGE := $(PIPENV_RUN) $(PYTHON) manage.py

## Code formatter for python https://black.readthedocs.io/
black:
	$(BLACK) awards

## Drops the current database, creates it, and migrates.
create-db:
	createdb awards
	$(MANAGE) migrate

## Create a superuser
create-superuser:
	$(MANAGE) createsuperuser

## Plain dumpdata command to: dump.json
dumpdata:
	$(MANAGE) dumpdata --indent 4 > example.json

## Start the gunicorn server on a unix socket
gunicorn:
	$(PIPENV_RUN) gunicorn --workers=2 -b 0.0.0.0:8000 awards.wsgi

## Display this help secion
help:
	@awk '/^#/{c=substr($$0,3);next}c&&/^[[:alpha:]][[:alnum:]_-]+:/{print substr($$1,1,index($$1,":")),c}1{c=0}' $(MAKEFILE_LIST) | column -s: -t

## Install dependencies per Pipfile
install:
	pipenv install

## Install dev dependencies per Pipfile
install-dev:
	pipenv install --dev

## Run linting for Python
lint: lint-python

## Run the flake8 linter
lint-python:
	$(FLAKE8)

## Load data from: dump.json
loaddata:
	$(MANAGE) loaddata example.json

## Make migration files
make-migrations:
	$(MANAGE) makemigrations
	$(MAKE) black

## Run unapplied migrations
migrate:
	$(MANAGE) migrate

## Drop into the django python shell
shell:
	$(MANAGE) shell

## Start the dev server on 0.0.0.0:8080
start:
	$(MANAGE) runserver 0.0.0.0:8080

## Collect static files for deployment, no input required
static:
	$(MANAGE) collectstatic --noinput --clear

## Run coverage
test:
	$(COVERAGE) erase
	pipenv run $(COVERAGE) run manage.py test
	$(COVERAGE) report -m

.PHONY: black create-db create-superuser dumpdata gunicorn help install install-dev lint lint-python loaddata make-migrations migrate shell start static test
