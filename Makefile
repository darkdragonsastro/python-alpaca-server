.PHONY: lint lock install bump commit

lint:
	poetry run isort python_alpaca_server
	poetry run black python_alpaca_server
	poetry run flake8 python_alpaca_server
	poetry run mypy python_alpaca_server

lock:
	poetry lock

install:
	poetry install

bump:
	cz bump

commit:
	cz commit
