.PHONY: test

DEBIAN_VERSION				:= `cat ./configs/versions/debian-version`
PYTHON_VERSION				:= `cat ./configs/versions/python-version`
POETRY_VERSION				:= `cat ./configs/versions/poetry-version`

DOCKER_COMPOSE_FILE			:= ./configs/docker/docker-compose.yaml

IMAGE_NAME 					:= polygence-work
IMAGE_TAG					:= $(or ${IMAGE_TAG}, ${IMAGE_TAG}, latest)
CONTAINER_ID				:= $(or ${CONTAINER_ID}, ${CONTAINER_ID}, `date +%s`)
POSTGRES_USER				:= $(or ${POSTGRES_USER}, ${POSTGRES_USER}, admin)
POSTGRES_PASSWORD			:= $(or ${POSTGRES_PASSWORD}, ${POSTGRES_PASSWORD}, admin)
POSTGRES_DB					:= $(or ${POSTGRES_DB}, ${POSTGRES_DB}, database)

help:
	@fgrep -h "##" $(MAKEFILE_LIST) | fgrep -v fgrep | sed -e 's/\\$$//' | sed -e 's/\(.*\):.*##[ \t]*/    \1 ## /' | column -t -s '##'
	@echo


## Docker commands:

build: ## Build project image
	$(call docker_compose) build $(IMAGE_NAME)

destroy: ## Destroy project containers and image
	$(call docker_compose) down --rmi all --remove-orphans

images: ## List project images
	$(call docker_compose) images $(IMAGE_NAME)

containers: ## List project containers
	$(call docker_compose) ps --all

bash: ## Run bash shell
	$(call docker_compose_run) bash

database: ## Start database container
	$(call docker_compose) up --detach database

database-admin: ## Start database admin panel container
	$(call docker_compose) up --detach database-admin


## Check commands:

check-python: ## Check Python version
	$(eval CONTAINER_PYTHON_VERSION := $(call check_python))
	$(eval EXPECTED_PYTHON_VERSION := $(PYTHON_VERSION))
	@if [ "$(CONTAINER_PYTHON_VERSION)" == "$(EXPECTED_PYTHON_VERSION)" ]; then echo "Ok" && exit 0; else echo "Error" && exit 1; fi

check-poetry: ## Check Poetry version
	$(eval CONTAINER_POETRY_VERSION := $(call check_poetry))
	$(eval EXPECTED_POETRY_VERSION := $(POETRY_VERSION))
	@if [ "$(CONTAINER_POETRY_VERSION)" == "$(EXPECTED_POETRY_VERSION)" ]; then echo "Ok" && exit 0; else echo "Error" && exit 1; fi


## Poetry commands

install: ## Install project dependencies
	$(call docker_compose_run) bash -c "poetry env use /usr/local/bin/python && poetry install"

test: ## Run test cases
	$(call docker_compose_run) bash -c "poetry run python manage.py test"

pylint: ## Run pylint
	$(call docker_compose_run) bash -c "poetry run pylint src"

migrate: ## Run database migrations
	$(call docker_compose_run) bash -c "poetry run python manage.py migrate"

start: ## Start service
	$(call docker_compose_start) bash -c "poetry run python manage.py runserver 0.0.0.0:5000"


define docker_compose
	$(call docker_compose_file_variables) docker-compose --file $(DOCKER_COMPOSE_FILE) --project-name $(IMAGE_NAME)
endef

define docker_compose_run
	$(call docker_compose) run --name $(IMAGE_NAME)-$(CONTAINER_ID) --user=user --use-aliases --no-deps --rm $(IMAGE_NAME)
endef

define docker_compose_start
	$(call docker_compose) run --name $(IMAGE_NAME)-$(CONTAINER_ID) --user=user --use-aliases --service-ports --rm $(IMAGE_NAME)
endef

define docker_compose_file_variables
	IMAGE_NAME=$(IMAGE_NAME) \
	IMAGE_TAG=$(IMAGE_TAG) \
	CONTAINER_ID=$(CONTAINER_ID) \
	DEBIAN_VERSION=$(DEBIAN_VERSION) \
	PYTHON_VERSION=$(PYTHON_VERSION) \
	POETRY_VERSION=$(POETRY_VERSION) \
	POSTGRES_USER=$(POSTGRES_USER) \
	POSTGRES_PASSWORD=$(POSTGRES_PASSWORD) \
	POSTGRES_DB=$(POSTGRES_DB)
endef

define check_python
	$(shell sh -c "docker run --user user --rm --name $(IMAGE_NAME)$(CONTAINER_ID) $(IMAGE_NAME):$(IMAGE_TAG) python --version | cut -d' ' -f2")
endef

define check_poetry
	$(shell sh -c "docker run --user user --rm --name $(IMAGE_NAME)$(CONTAINER_ID) $(IMAGE_NAME):$(IMAGE_TAG) poetry --version | cut -d' ' -f3")
endef
