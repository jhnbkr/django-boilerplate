SHELL := /bin/bash -e

.PHONY: help \
        serve \
        start-services \
        stop-services \
        clean-services \
        setup-python-env \
        clean-python-caches \
        clean-pytest-caches \
        clean-python-env \
        clean-python \
        clean \
        clean-full \
        setup \
        reset

# Configuration
SERVICE_NAME := harvester-service
DEVELOP_PATH := $(PWD)/develop
DOCKER_COMPOSE_FILE := $(DEVELOP_PATH)/docker-compose.yml
DOCKER_DATA_PATH := $(DEVELOP_PATH)/data
SERVER_PORT := 8282
REQUIREMENTS_FILE := $(PWD)/requirements.txt
VENV_PATH := $(PWD)/venv

# Colors
RED := \033[1;31m
GREEN := \033[1;32m
YELLOW := \033[1;33m
CYAN := \033[1;36m
RESET := \033[0m

# Utilities
ACTIVATE_VENV := source $(VENV_PATH)/bin/activate
CHECK_DOCKER_COMPOSE := @command -v docker-compose >/dev/null 2>&1 || { echo >&2 "${RED}docker-compose is required but it's not installed. Aborting.${RESET}"; exit 1; }

# Documentation
help: ## Display available commands
	@awk 'BEGIN {FS = ":.*?## "}; \
        /^[$$()%0-9a-zA-Z_-]+:.*?## / { \
            printf "${CYAN}  %-30s${RESET} %s\n", $$1, $$2 \
        }' $(MAKEFILE_LIST) | sort

# Server
serve: ## Start the server
	@echo -e "${GREEN}> Starting server on port $(SERVER_PORT)...${RESET}"
	$(ACTIVATE_VENV) && uvicorn project.asgi:application --host 0.0.0.0 --port $(SERVER_PORT) --reload

# Services
start-services: ## Start all services
	@echo -e "${GREEN}> Starting services...${RESET}"
	$(CHECK_DOCKER_COMPOSE)
	docker-compose -p $(SERVICE_NAME) -f $(DOCKER_COMPOSE_FILE) up --detach

stop-services: ## Stop all services
	@echo -e "${RED}> Stopping services...${RESET}"
	$(CHECK_DOCKER_COMPOSE)
	docker-compose -p $(SERVICE_NAME) -f $(DOCKER_COMPOSE_FILE) down

clean-services: ## Clean all services and volumes
	@echo -e "${RED}> Cleaning services and volumes...${RESET}"
	$(CHECK_DOCKER_COMPOSE)
	docker-compose -p $(SERVICE_NAME) -f $(DOCKER_COMPOSE_FILE) down --remove-orphans --volumes
	rm -rf $(DOCKER_DATA_PATH)

# Python
setup-python-env: ## Set up the Python environment and install dependencies
	@echo -e "${YELLOW}> Setting up Python environment...${RESET}"
	test -d $(VENV_PATH) || python -m venv $(VENV_PATH)
	$(ACTIVATE_VENV) && pip install -r $(REQUIREMENTS_FILE)

clean-python-caches: ## Remove Python cache files
	@echo -e "${RED}> Cleaning Python cache files...${RESET}"
	find . -type f -name '*.py[co]' -delete -o -type d -name __pycache__ -delete

clean-pytest-caches: ## Clear pytest cache
	@echo -e "${RED}> Cleaning pytest cache...${RESET}"
	rm -rf .pytest_cache

clean-python-env: ## Remove the Python environment
	@echo -e "${RED}> Removing Python environment...${RESET}"
	rm -rf $(VENV_PATH)

clean-python: clean-python-caches clean-pytest-caches clean-python-env ## Clean up all Python-related caches and environment

# Project
clean: clean-python stop-services ## Clean the Python environment and stop all services
clean-full: clean clean-services ## Perform a full clean of the project
setup: setup-python-env start-services ## Set up the environment and start services
reset: clean setup ## Reset the environment by cleaning and then setting up
