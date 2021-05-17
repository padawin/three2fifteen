# Three2Fifteen Application

## Requirements

Python 3.6

## Installation

	pip install -e .

## Setup

Copy config.py.example to config.py and update the content to fit your
environment.

Start then with:

	python app.py

To use the app in development mode, use:

	DEV=1 python app.py

Then, the game is accessible at:

	http://localhost:5000

## Tests

Install ``requirements_dev.txt``, then run:

    $ PYTHONPATH=. pytest

## Database

	docker-compose up
	docker exec -it db-three2fifteen mysql -u user -p

	> create database three2Fifteen;
	> use three2Fifteen;
