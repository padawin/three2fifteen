# Three2Fifteen Application API service

## Requirements

Python 3.6

## Installation

	pip install -e .

## Setup

Copy config.template.cfg to config.cfg and update the content to fit your
environment.

Start then with:

	env THREE2FIFTEEN_API_SETTINGS=/path/to/config.cfg three2fifteen-api

## Database

A Postgres database is needed. For development purposes, docker can be used:

	$ docker run --name three2fifteen-postgres -e POSTGRES_PASSWORD=mysecretpassword -d postgres

## Tests

Install ``requirements_dev.txt``, then run:

    $ pytest
