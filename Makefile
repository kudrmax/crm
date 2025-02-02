include .env
export $(shell sed 's/=.*//' .env)

DUMP_FILE ?= ./db_backup.sql

dump:
	pg_dump -U $(POSTGRES_USER) -h localhost -p $(POSTGRES_PORT) -d $(POSTGRES_DATABASE) > $(DUMP_FILE)

load_dumped:
	psql -U $(POSTGRES_USER) -h localhost -p $(POSTGRES_PORT) -d $(POSTGRES_DATABASE) -f $(DUMP_FILE)

db:
	docker compose up -d db

bot:
	docker compose up -d bot --build