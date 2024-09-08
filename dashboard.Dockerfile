# Start with the official Python image from the Docker Hub
FROM python:3.12-slim-bookworm

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev --no-interaction --no-ansi

COPY . .

CMD ["python", "-m", "calmmage_services_registry.dashboard"]
