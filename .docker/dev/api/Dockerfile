FROM tiangolo/uvicorn-gunicorn-fastapi:python3.11

RUN pip install poetry

ENV POETRY_VIRTUALENVS_CREATE=false

COPY ../api/pyproject.toml /app/pyproject.toml
COPY ../api/poetry.lock /app/poetry.lock
COPY ../api /app

WORKDIR /app/src

RUN poetry install --no-root

EXPOSE 8080

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080", "--workers", "3"]