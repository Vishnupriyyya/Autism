# Multi-stage Dockerfile for Django + Gunicorn on Cloud Run
# Python 3.12 slim for smaller image

FROM python:3.12-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --user -r requirements.txt

FROM python:3.12-slim

# Install gunicorn, etc. from builder
ENV PATH=/root/.local/bin:$PATH
COPY --from=builder /root/.local /root/.local

# Install system deps for Pillow/media
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy project
COPY . .

# Collect static files
RUN python manage.py collectstatic --noinput --settings=autism_platform.settings

# Run Gunicorn on port 8080 (Cloud Run default)
EXPOSE 8080

CMD gunicorn autism_platform.wsgi:application \
    --bind 0.0.0.0:8080 \
    --workers 2 \
    --threads 4 \
    --timeout 120 \
    --max-requests 1000 \
    --max-requests-jitter 100 \
    --preload
