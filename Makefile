.PHONY: install test lint run build clean

install:
	pip install -r requirements-dev.txt

lint:
	ruff check app tests

test:
	pytest --cov=app --cov-report=term-missing --cov-report=xml

run:
	uvicorn app.main:app --reload

build: lint test
	@echo "Build local exitosa"

clean:
	rmdir /s /q .pytest_cache __pycache__ htmlcov 2>nul || exit 0