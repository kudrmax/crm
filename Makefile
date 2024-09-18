DOCKER_COMPOSE_FILE = docker-compose.yaml
BACKEND_CMD = uvicorn main:app --host $(SERVER_HOST) --port $(SERVER_PORT) --reload
BOT_CMD = python3 bot.py
VENV_CMD = source .venv/bin/activate

include .env
#export $(shell sed 's/=.*//' .env)

db_up:
	docker compose -f $(DOCKER_COMPOSE_FILE) up -d

db_down:
	docker compose -f $(DOCKER_COMPOSE_FILE) down

backend_up:
	@echo "Starting FastAPI server..."
	@sh -c 'source .venv/bin/activate && $(BACKEND_CMD)'

bot_up:
	@echo "Starting Telegram bot..."
	@sh -c 'source .venv/bin/activate && $(BOT_CMD)'