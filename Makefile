.PHONY: run
run: uvicorn app.main:app --reload --workers 1 --host 0.0.0.0 --port 8000

.PHONY: migration-head
migration-head: alembic upgrade head

.PHONY: migration-base
migration-base: alembic downgrade base

.PHONY: migration-up
migration-up: alembic upgrade +1

.PHONY: migration-down
migration-down: alembic downgrade -1

.PHONY: install
install:  ## Install dependencies
	pip install -r requirements.txt

.PHONY: swagger
swagger:  ## Install dependencies
	run
	python -m webbrowser "http://localhost:8000/docs"

.PHONY: lint
lint: # Lint code
	flake8 --exclude .\migrations
	mypy .
	black --line-length 79 --skip-string-normalization --check .

.PHONY: check
check: lint test
