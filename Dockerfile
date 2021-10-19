# syntax=docker/dockerfile:1

FROM python:3.9-slim-buster

WORKDIR /app

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --no-dev

COPY . .

CMD ["python3", "-m", "service", "run", "--host=0.0.0.0"]
