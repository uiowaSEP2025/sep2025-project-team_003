FROM node:22-alpine AS frontend
# Copy the rest of the application
COPY . .

# Set working directory
WORKDIR /HSA-frontend

# Copy package files first for better caching
COPY package*.json ./
RUN npm install -g @angular/cli
RUN npm install

RUN ng build


FROM python:3.13-alpine3.21 AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies including PostgreSQL, build tools, and utilities for installing Chrome
RUN apk add --no-cache \
    --upgrade bash \
    chromium \
    chromium-chromedriver \
    su-exec \
    build-base \
    postgresql17 \
    postgresql17-contrib \
    postgresql17-dev \
    build-base \
    libpq-dev \
    python3-dev \
    gcc \
    xvfb

# Copy from frontend stage with specific paths
COPY --from=frontend /HSA-frontend /app/HSA-frontend
COPY --from=frontend /build_django_index.py /app/
COPY --from=frontend /HSA-backend /app/HSA-backend
COPY --from=frontend /deployment/testing/integration/entrypoint.sh /app/HSA-backend/entrypoint.sh
# Run the build script
WORKDIR /app
RUN python3 build_django_index.py

WORKDIR /app/HSA-backend

# Environment variables for Django database configuration
ENV CHROME_BIN=/usr/bin/google-chrome
ENV DISPLAY=:99
ENV DATABASE_NAME=django_db
ENV DATABASE_USERNAME=django_user
ENV DATABASE_PASSWORD=123abc!
ENV DATABASE_IP=localhost
ENV INTEGRATION_FLAG=1
# Install Python dependencies
RUN pip3 install --no-cache-dir -r requirements.txt

RUN chmod +x entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/app/HSA-backend/entrypoint.sh"]