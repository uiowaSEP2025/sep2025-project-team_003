# This version of the dockerfile would combine all 3 tests and run them under one build. Unfortunately this is not available in the Azure Free version.
# Saving it for future use.
FROM python:3.13-alpine3.21

# Copy the rest of the application
COPY . /app/

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies including PostgreSQL, build tools, and utilities for installing Chrome
RUN apk add --no-cache \
    --upgrade bash \
    nodejs \
    npm \
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
    harfbuzz \
    nss \
    freetype \
    ttf-freefont \
    xvfb

# Set working directory
WORKDIR /app/HSA-frontend

# Copy package files first for better caching
COPY package*.json ./
RUN npm install -g @angular/cli
RUN npm install

RUN ng build

# Run the build script
WORKDIR /app
RUN python3 build_django_index.py

# Environment variables for Django database configuration
# Set Chrome environment variables
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/

ENV DISPLAY=:99
ENV DATABASE_NAME=django_db
ENV DATABASE_USERNAME=django_user
ENV DATABASE_PASSWORD=123abc!
ENV DATABASE_IP=localhost
ENV INTEGRATION_FLAG=1
# Install Python dependencies
WORKDIR /app/HSA-backend

RUN pip3 install --no-cache-dir -r requirements.txt
COPY ./deployment/testing/build-database.sh /app/HSA-backend/build-database.sh
RUN chmod +x build-database.sh
RUN ./build-database.sh

WORKDIR /app/
COPY ./deployment/testing/entrypoint.sh /app/entrypoint.sh
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["frontend"]