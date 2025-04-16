FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y unzip libaio1 curl && rm -rf /var/lib/apt/lists/*

# Copy backend code
COPY backend/ .

# Oracle client + wallet
COPY backend/oracle_client/instantclient_23_7 ./oracle_client/instantclient_23_7
COPY backend/wallet/Wallet_userdetails ./oracle_client/instantclient_23_7/network/admin
COPY backend/wallet/Wallet_userdetails ./wallet

# Copy env
COPY .env .env

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

ENV LD_LIBRARY_PATH=/app/oracle_client/instantclient_23_7

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
