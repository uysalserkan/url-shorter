# Default Makefile
PYTHON = python3
APP_SCRIPT = app.py

all: run

run:
	uvicorn app:app --reload --port 25200

lint:
	pylint $(APP_SCRIPT)
