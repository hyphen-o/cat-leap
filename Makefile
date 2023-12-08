init:
	@docker compose build --no-cache
	@docker compose up -d
up:
	@docker compose up -d
down:
	@docker compose down
exec:
	@docker compose exec cat-leap bash
build:
	@docker compose exec cat-leap poetry build
install:
	@docker compose exec cat-leap poetry install
	@docker compose exec cat-leap poetry update
lint:
	@docker compose exec cat-leap poetry run pylint .
format:
	@docker compose exec cat-leap poetry run black .