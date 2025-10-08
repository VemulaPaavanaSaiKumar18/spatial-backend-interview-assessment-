# Makefile for managing the project

.PHONY: setup server clean

# Setup the project (create venv and install dependencies)
setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

# Run the server
server:
	. .venv/bin/activate && uvicorn app.main:app --reload

# Clean up the virtual environment
clean:
	rm -rf .venv
