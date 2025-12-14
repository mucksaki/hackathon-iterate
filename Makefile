# Variables
PYTHON ?= python3
BACKEND_DIR := backend
VENV := .venv
VENV_PY := $(VENV)/bin/python

## COLORS (kept from your reference)
BLUE					=	\033[0;34m
LIGHT_BLUE		=	\033[1;34m
GREEN					=	\033[0;32m
YELLOW				=	\033[1;33m
RED						=	\033[0;31m
NC						=	\033[0m

.PHONY: all back-venv back-requirements back-test back-quality back-quality-fix clean front-test

# This creates a venv if it does not exist.
back-venv:
	@cd $(BACKEND_DIR) && \
	if [ ! -d "$(VENV)" ]; then \
		echo "$(LIGHT_BLUE)Creating virtual environment...$(NC)"; \
		$(PYTHON) -m venv $(VENV); \
	fi && \
	$(VENV_PY) -m pip install -U pip uv --quiet

# This install all the necessary requirements.
back-requirements: back-venv
	@echo "$(LIGHT_BLUE)Installing backend requirements...$(NC)"
	@cd $(BACKEND_DIR) && \
	$(VENV_PY) -m uv pip install -r requirements.txt --quiet

# This is to run the backend locally.
back-test: back-requirements
	@echo "$(GREEN)Starting backend (uvicorn)...$(NC)"
	@cd $(BACKEND_DIR) && \
	$(VENV_PY) -m uvicorn src.application:app --host 0.0.0.0 --port 8080 --reload

# This is to check if the backend is clean (does not modify code).
back-quality: back-requirements
	@echo "Running back quality (ruff + mypy)..."
	@cd $(BACKEND_DIR) && \
	$(VENV_PY) -m uv pip install ruff mypy --quiet && \
	echo "$(BLUE)Checking ruff lint...$(NC)" && $(VENV_PY) -m ruff check src && \
	echo "$(BLUE)Checking ruff format...$(NC)" && $(VENV_PY) -m ruff format --check src && \
	echo "$(BLUE)Running mypy...$(NC)" && $(VENV_PY) -m mypy src

# This cleans the backend code (modifies code).
back-quality-fix: back-requirements
	@echo "Running back quality fix (ruff)..."
	@cd $(BACKEND_DIR) && \
	$(VENV_PY) -m uv pip install ruff --quiet && \
	echo "$(BLUE)Running ruff autofix...$(NC)" && $(VENV_PY) -m ruff check --fix src && \
	echo "$(BLUE)Running ruff format...$(NC)" && $(VENV_PY) -m ruff format src

# This deletes the venv.
clean:
	@echo "$(YELLOW)Removing backend virtual environment...$(NC)"
	@rm -rf $(BACKEND_DIR)/$(VENV)

# This is to run the frontend locally.
front-test:
	@echo "Running front..."
	cd frontend && npm install && npm run dev