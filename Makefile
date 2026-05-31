

.PHONY: start_api
start_api:
	./api/postgres.sh
	sleep 2
	cd api;poetry run alembic upgrade head
	cd api;poetry run python3 -m src.main

.PHONY: start_web
start_web:
	cd web; npm run dev

