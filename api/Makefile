migrate-create:
	alembic revision --autogenerate -m ${MIGRATION}

migrate-apply:
	alembic upgrade head

run-local:
	poetry run uvicorn src.main:app --host localhost --port 8000 --reload --env-file .env.local