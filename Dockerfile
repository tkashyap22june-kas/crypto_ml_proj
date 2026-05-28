FROM python:3.10-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# IMPORTANT: set src as python root
ENV PYTHONPATH=/app/src

EXPOSE 10000

CMD ["uvicorn", "crypto.api.app:app", "--host", "0.0.0.0", "--port", "10000"]