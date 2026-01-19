FROM python:3.9-slim

# System Deps
RUN apt-get update && apt-get install -y \
    build-essential git libsndfile1 curl ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python Deps
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download Dictionary (Prevent Runtime Error)
RUN python3 -m unidic_lite.download

COPY main.py .

CMD ["python", "main.py"]