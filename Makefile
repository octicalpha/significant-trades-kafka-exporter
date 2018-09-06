.EXPORT_ALL_VARIABLES:
APP_VERSION			= $(shell git describe --abbrev=0 --tags)
APP_NAME				= stke
DOCKER_ID_USER	= dmi7ry
ENV_DIR					= ./docker-compose

all: build

build:
	docker-compose build

release:
	export APP_VERSION=latest ;\
	docker-compose build

run: build
	docker-compose up $(APP_NAME)
run-prod: build
	docker-compose -f $(ENV_DIR)/docker-compose-prod.yml -f docker-compose.yml up $(APP_NAME)
run-dev: build
	docker-compose -f $(ENV_DIR)/docker-compose-dev.yml -f docker-compose.yml up $(APP_NAME)

up: build
	docker-compose up -d $(APP_NAME)
up-prod: build
	docker-compose -f $(ENV_DIR)/docker-compose-prod.yml -f docker-compose.yml up -d $(APP_NAME)
up-dev: build
	docker-compose -f $(ENV_DIR)/docker-compose-dev.yml -f docker-compose.yml up -d $(APP_NAME)

stop:
	docker-compose stop $(APP_NAME)

shell:
	docker exec -it $(APP_NAME) bash

push-latest:
	export APP_VERSION=latest ;\
	docker-compose push

push:
	docker-compose push

publish: build push release push-latest
