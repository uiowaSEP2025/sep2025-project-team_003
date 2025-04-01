FROM python:3.13-alpine3.21 AS backend
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install postgresql client
RUN apk add --no-cache \
    --upgrade bash \
    su-exec \
    build-base \
    postgresql17 \
    postgresql17-contrib \
    postgresql17-dev \
    build-base \
    libpq-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY . /app/

WORKDIR /app/HSA-backend
ENV DATABASE_NAME=django_db
ENV DATABASE_USERNAME=django_user
ENV DATABASE_PASSWORD=123abc!
ENV DATABASE_IP=localhost

COPY ./deployment/testing/backend/entrypoint.sh /app/HSA-backend/entrypoint.sh
# Setup backend
RUN pip3 install --no-cache-dir -r requirements.txt

# Set up entrypoint script
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/HSA-backend/entrypoint.sh"]

