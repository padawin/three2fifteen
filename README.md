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

## Tests

Install ``requirements_dev.txt``, then run:

    $ PYTHONPATH=. pytest

## Database

	docker pull mysql/mysql-server:latest
	docker run  --name=mysql1 -p 3306:3306 -e MYSQL_ROOT_PASSWORD=123456  mysql/mysql-server:latest
	docker exec -it mysql1 mysql -uroot -p

	> create database three2Fifteen
	> use three2Fifteen
