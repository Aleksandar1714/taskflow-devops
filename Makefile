APP_NAME=taskflow
IMAGE ?= $(DOCKERHUB_USERNAME)/taskflow
TAG ?= latest

install:
	python -m venv .venv && . .venv/bin/activate && pip install -r requirements-dev.txt && pre-commit install

test:
	pytest -q

lint:
	ruff check .
	black --check .
	bandit -r app

run:
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-build:
	docker build -t $(IMAGE):$(TAG) .

docker-run:
	docker run -p 8000:8000 $(IMAGE):$(TAG)
