.DEFAULT_GOAL := up

.PHONY: up down logs shell

up:
	docker compose up --build -d

down:
	docker compose down

logs:
	docker compose logs -f

shell:
	docker compose exec -it web python manage.py shell