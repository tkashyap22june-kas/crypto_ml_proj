FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 🔥 CRITICAL FIX (must be /app, NOT /app/src)
ENV PYTHONPATH=/app

EXPOSE 10000

CMD ["sh", "-c", "uvicorn src.crypto.api.app:app --host 0.0.0.0 --port $PORT"]