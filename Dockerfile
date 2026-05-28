FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 10000

# 🔥 FIX: hardcode port (Render-safe)
CMD ["uvicorn", "src.crypto.api.app:app", "--host", "0.0.0.0", "--port", "10000"]