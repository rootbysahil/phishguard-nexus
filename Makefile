.PHONY: all setup data features train evaluate fresh-eval test lint run dev clean

# Python environment settings
PYTHON ?= python
PIP ?= pip

all: data features train evaluate test

setup:
	$(PIP) install -r backend/requirements.txt

data:
	$(PYTHON) backend/data/scripts/download_data.py

features:
	$(PYTHON) backend/data/scripts/build_features.py

train:
	$(PYTHON) backend/data/scripts/train_model.py

evaluate:
	$(PYTHON) backend/data/scripts/evaluate_model.py

fresh-eval:
	$(PYTHON) backend/data/scripts/evaluate_fresh.py

test:
	pytest backend/tests/ -v

lint:
	ruff check backend/
	black --check backend/

dev-backend:
	uvicorn backend.app.main:app --host 0.0.0.0 --port 8000 --reload

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache .ruff_cache
