.PHONY: install up down

install:
	./scripts/install-all.sh

up:
	docker compose up -d postgres redis

down:
	docker compose down
