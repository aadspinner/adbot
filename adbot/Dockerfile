FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y unzip libaio1 curl && rm -rf /var/lib/apt/lists/*

# Copy backend code and Oracle client
COPY backend /app
COPY backend/oracle_client/instantclient_23_7 /app/oracle_client/instantclient_23_7

# Copy .env file
COPY .env /app/.env
COPY backend/wallet/Wallet_userdetails /app/oracle_client/instantclient_23_7/network/admin

COPY backend/wallet/Wallet_userdetails /app/wallet
COPY backend/oracle_client/instantclient_23_7 /app/oracle_client/instantclient_23_7


# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Set Oracle client library path
ENV LD_LIBRARY_PATH=/app/oracle_client/instantclient_23_7

# Expose the port for FastAPI
EXPOSE 8000

# Run app with Uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
