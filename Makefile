init:
	@docker compose build --no-cache
	@docker compose up -d

up:
	@docker compose up -d
	
down:
	@docker compose down

exec:
ifeq ($(args),)
	@docker compose exec cat-leap bash
else
	@docker compose exec cat-leap $(args)
endif

build:
	@docker compose exec cat-leap poetry build

install:
	@docker compose exec cat-leap poetry install
	@docker compose exec cat-leap poetry update

lint:
	@docker compose exec cat-leap poetry run pylint catleap

type-check:
	@docker compose exec cat-leap poetry run mypy .

format:
	@docker compose exec cat-leap poetry run black .