# Makefile for PDF Chatbot Project

.PHONY: all test lint format check k8s-validate

# Default target: run all checks
all: test lint

# Run all tests with pytest
test:
	@echo "Running tests..."
	pytest tests/

# Run flake8 linting
lint:
	@echo "Running flake8 lint check..."
	flake8 app/main.py tests/ --max-line-length=88 --exclude=.venv

# Format code with black
format:
	@echo "Formatting code with black..."
	black app/main.py tests/

# Run lint check and format check together
check: lint format

k8s-validate:
	kubectl apply --dry-run=client -f k8s/