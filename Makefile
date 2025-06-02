# Makefile for PDF Chatbot Project

.PHONY: all test-unit test-integration test-monitoring test lint format check k8s-validate

# Default target: run all checks
all: test lint

test-unit:
	@echo "Running unit tests with pytest..."
	python -m pytest tests/unit

test-integration:
	@echo "Running integration tests with pytest..."
	python -m pytest tests/integration

test-monitoring:
	@echo "Running monitoring tests with pytest..."
	python -m pytest tests/monitoring

# Run all tests with pytest
test:
	@echo "Running tests..."
	python -m pytest tests/

# Run ruff linting
lint:
	@echo "Running ruff lint check..."
	ruff check .
# Format code with black
format:
	@echo "Formatting code with black..."
	black app/main.py tests/

# Run lint check and format check together
check: lint format

k8s-validate:
	kubectl apply --dry-run=client -f k8s/