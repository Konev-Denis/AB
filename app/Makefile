.PHONY: run
run: uvicorn main:app --reload

.PHONY: install
install:  ## Install dependencies
	pip install -r requirements.txt

.PHONY: swagger
swagger:  ## Install dependencies
	run
	python -m webbrowser "http://localhost:8000/docs"

.PHONY: lint
lint: # Lint code
	flake8 --exclude test_main.py .
	mypy .
	black --line-length 79 --skip-string-normalization --check .

.PHONY: check
check: lint test
