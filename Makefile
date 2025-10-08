# Makefile for managing the project

.PHONY: setup server clean test

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

# Run test suite inside the project's virtualenv (creates venv if missing)
test:
	@if [ ! -d ".venv" ]; then \
		echo "Creating virtualenv..."; \
		python3 -m venv .venv; \
	fi
	# Install dependencies into the virtualenv only once (use marker file)
	@if [ ! -f .venv/.installed ]; then \
		echo "Installing dependencies into virtualenv..."; \
		. .venv/bin/activate && python -m pip install -r requirements.txt; \
		touch .venv/.installed; \
	else \
		echo "Dependencies already installed, skipping."; \
	fi
	# Use the venv Python to run pytest (avoids using system pytest)
	.venv/bin/python -m pytest -q
