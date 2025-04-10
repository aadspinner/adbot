FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for Oracle Instant Client
RUN apt-get update && apt-get install -y libaio1 unzip curl && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY . .

# Set up Oracle Instant Client
RUN mkdir -p /opt/oracle && \
    curl -L -o wallet.zip https://path-to-your-wallet.zip && \
    unzip wallet.zip -d /opt/oracle/wallet && \
    rm wallet.zip

# Environment setup
ENV TNS_ADMIN=/opt/oracle/wallet
ENV LD_LIBRARY_PATH=/opt/oracle/instantclient:$LD_LIBRARY_PATH

# Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
