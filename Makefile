# Font Analyzer - Development Makefile (UV)

.PHONY: help install install-dev test lint format type-check clean build run-example docker-build docker-run

help:  ## Show this help message
	@echo "Font Analyzer - Development Commands (UV)"
	@echo "============================================="
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	uv sync --no-dev

install-dev:  ## Install development dependencies
	uv sync
	uv run pre-commit install

test:  ## Run tests
	uv run python -m unittest tests.test_font_analyzer -v

test-cov:  ## Run tests with coverage
	uv run pytest tests/ -v --cov=src --cov-report=html --cov-report=term

lint:  ## Run linting (flake8)
	uv run flake8 src tests --max-line-length=88 --extend-ignore=E203,W503

format:  ## Format code with black
	uv run black src tests

format-check:  ## Check code formatting
	uv run black --check src tests

type-check:  ## Run type checking with mypy
	uv run mypy src

quality:  ## Run all quality checks
	make format-check
	make lint
	make type-check

quality-fix:  ## Fix code quality issues
	make format
	make lint

clean:  ## Clean up build artifacts and cache
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	rm -rf build/
	rm -rf dist/
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/

build:  ## Build package
	python -m build

run-example-url:  ## Run example with URL
	python main.py --url "https://fonts.google.com"

run-example-file:  ## Run example with local font file
	python main.py --font_path "fonts/Lato-Regular.ttf"

docker-build:  ## Build Docker image
	docker build -t font-detector .

docker-run:  ## Run with Docker
	docker run -v $$(pwd)/fonts:/app/fonts font-detector --font_path fonts/Lato-Regular.ttf

docker-compose:  ## Run with docker-compose
	docker-compose up

setup-dev:  ## Set up development environment
	python -m venv .venv
	@echo "Virtual environment created. Activate with:"
	@echo "  source .venv/bin/activate  (Linux/Mac)"
	@echo "  .venv\\Scripts\\activate     (Windows)"
	@echo "Then run: make install-dev"

check-security:  ## Check for security vulnerabilities
	pip install safety bandit
	safety check
	bandit -r src/

pre-commit:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

bump-version:  ## Bump version (requires bump2version)
	bump2version patch

release:  ## Prepare release (build, test, etc.)
	make clean
	make quality
	make test
	make build
	@echo "Release ready! Don't forget to:"
	@echo "1. Update CHANGELOG.md"
	@echo "2. Create a git tag"
	@echo "3. Push to repository"

# Development workflow commands
dev-setup: setup-dev install-dev  ## Complete development setup

dev-check: quality test  ## Run all development checks

dev-reset: clean install-dev  ## Reset development environment
