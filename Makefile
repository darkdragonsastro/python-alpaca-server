# Makefile for python-alpaca-server
#
# Python project using Poetry for dependency management

.PHONY: test lint typecheck build format install audit lock bump commit

# Run the full test suite
test:
	poetry run pytest

# Run linter (flake8)
lint:
	poetry run flake8 python_alpaca_server

# Run type checker (mypy)
typecheck:
	poetry run mypy python_alpaca_server

# Build the project
build:
	poetry build

# Format code (isort + black)
format:
	poetry run isort python_alpaca_server
	poetry run black python_alpaca_server

# Install dependencies
install:
	poetry install

# Security audit (not configured)
audit:
	@echo "INFO: No security audit configured (optional target)"

# Lock dependencies
lock:
	poetry lock

# Bump version using commitizen
bump:
	cz bump

# Create commit using commitizen
commit:
	cz commit
