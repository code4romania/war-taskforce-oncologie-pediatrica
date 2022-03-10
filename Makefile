help:                             ## Display a help message detailing commands and their purpose
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""

build:                            ## builds the container
	docker-compose build --pull

build-dev:                        ## builds the container with the development flag
	docker-compose build --build-arg ENVIRONMENT=development --pull

run:
	docker-compose up

run-d:
	docker-compose up -d

seed_superuser:                   ## creates a superuser for the APP based on the data in the .env file
	docker-compose exec oncoped ./manage.py seed_superuser

seed_groups:                   ## creates a groups for the APP based on the data in the .env file
	docker-compose exec oncoped ./manage.py seed_groups

seed: seed_superuser seed_groups

drop-db:                          ## drops the database
	docker-compose down -t 60
	docker volume rm oncoped-pgdata

## [UTILS]
requirements-build:               ## run pip compile and add requirements from the *.in files
	docker-compose run --rm --no-deps --entrypoint "bash -c" oncoped "cd /code && pip-compile -o requirements.txt requirements.in && pip-compile -o requirements-dev.txt requirements-dev.in"

requirements-update:              ## run pip compile and rebuild the requirements files
	docker-compose run --rm --no-deps --entrypoint "bash -c" oncoped "cd /code && pip-compile -r -U -o requirements.txt requirements.in && pip-compile -r -U -o requirements-dev.txt requirements-dev.in && chmod a+r requirements.txt && chmod a+r requirements-dev.txt"

migrations:                       ## generate migrations in a clean container
	docker-compose exec oncoped ./manage.py makemigrations

migrate:                          ## apply migrations in a clean container
	docker-compose exec oncoped ./manage.py migrate

makemessages:                     ## generate the strings marked for translation
	docker-compose exec oncoped ./manage.py makemessages -a

compilemessages:                  ## compile the translations
	docker-compose exec oncoped ./manage.py compilemessages

collectstatic:
	docker-compose exec oncoped ./manage.py collectstatic --no-input

format:
	docker-compose run --rm --no-deps --entrypoint "bash -c" oncoped "isort --skip migrations . && black --target-version=py39 --exclude migrations ."

format-check:
	docker-compose run --rm --no-deps --entrypoint "bash -c" oncoped "isort --skip migrations --check . && black --target-version=py39 --check --diff --exclude migrations ."
