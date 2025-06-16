FROM python:3.10-slim

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /bot_backend
COPY . /bot_backend

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /bot_backend
USER appuser

EXPOSE 8000

CMD ["uvicorn", "bot_backend.backend_api:app", "--host", "0.0.0.0", "--port", "8000"]