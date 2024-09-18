.PHONY: lint

lint:
	poetry run isort python_alpaca_server
	poetry run black python_alpaca_server
	poetry run flake8 python_alpaca_server
	poetry run mypy python_alpaca_server
