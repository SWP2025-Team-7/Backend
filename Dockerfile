FROM python:3.10-slim

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /backend
COPY . /backend

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /backend
USER appuser

EXPOSE 8000

ENTRYPOINT alembic upgrade head && uvicorn backend.backend_api:app --host 0.0.0.0 --port 8000  