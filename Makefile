# @todo разобраться что делает каждая буква в этих командах

up:
	docker compose -f docker-compose.yaml up -d

down:
	docker compose -f docker-compose.yaml down && docker network prune --force