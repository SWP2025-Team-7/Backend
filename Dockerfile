FROM python:3.10-slim

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

WORKDIR /backend
COPY . /backend

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /backend
USER appuser

EXPOSE 8000

CMD ["uvicorn", "backend.backend_api:app", "--host", "0.0.0.0", "--port", "8000"]