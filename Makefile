.PHONY: test-db test test-down

test-db:
	docker compose --profile test up -d --wait db_test

test: test-db
	env -u POSTGRES_DB -u POSTGRES_HOST -u POSTGRES_PORT -u POSTGRES_USER -u POSTGRES_PASSWORD poetry run pytest -s --setup-show

test-down:
	docker compose --profile test rm -s -f db_test