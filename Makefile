#!make

help:
	@echo "available actions:"
	@echo "    build"
	@echo "        Build container image"
	@echo "    install"
	@echo "        Build, configure and install application"
	@echo "    uninstall"
	@echo "        Uninstall all containers and remove volumes and network ** Highly destructable **"
	@echo '    init_db'
	@echo '        Initiliaze dependencies (Database, etc)'
	@echo '    load_db'
	@echo '        Load/reload data person/company data from the resources folder the database'
	@echo '        Attention: If the database is already populated, this command will delete and recreate everything'
	@echo '    migration'
	@echo '        Run migrations'
	@echo '    start'
	@echo '        Start application (It does not install the application, just start containers)'
	@echo '    stop'
	@echo '        Stop application (It does not uninstall the application, just stop containers)'
	@echo '    status'
	@echo '        Check containers status (same as docker ps)'

.PHONY: help

build:
	DOCKER_BUILDKIT=1 BUILDKIT_PROGRESS=plain docker build -t"pandora-api:local" .

install: |build init_db load_db start

uninstall: |stop
	docker-compose down --remove-orphans -v

init_db:
	docker-compose run init-db

load_db:
	docker-compose run load-db-data

start:
	docker-compose up -d api

stop:
	docker-compose stop

status:
	docker ps | grep pandora