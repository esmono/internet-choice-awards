FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -qq --no-install-recommends make postgresql-client xmlsec1 curl

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PIPENV_VENV_IN_PROJECT 1

RUN pip install --upgrade pip
RUN pip install pipenv

COPY . /usr/src/app
RUN make install
