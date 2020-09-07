#!make

build:
	DOCKER_BUILDKIT=1 BUILDKIT_PROGRESS=plain docker build -t"pandora-api:local" .

uninstall:
	docker-compose stop
	docker-compose down -v --remove-orphans

init:
	docker-compose run pandora-init

install: |build init start

start:
	docker-compose up -d api

stop:
	docker-compose stop