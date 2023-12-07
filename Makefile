init:
	@docker compose build --no-cache
	@docker compose up -d
up:
	@docker compose up -d
down:
	@docker compose down
exec:
	@docker compose exec cat-leap sh