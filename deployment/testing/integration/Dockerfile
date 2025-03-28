FROM node:22-alpine AS frontend
# Copy the rest of the application
COPY . .
# Install Chrome and dependencies
RUN apk add --no-cache \
    chromium \
    chromium-chromedriver \
    harfbuzz \
    nss \
    freetype \
    ttf-freefont

# Set Chrome environment variables
ENV CHROME_BIN=/usr/bin/chromium-browser
ENV CHROME_PATH=/usr/lib/chromium/

# Set working directory
WORKDIR /HSA-frontend

# Copy package files first for better caching
COPY package*.json ./
RUN npm install -g @angular/cli
RUN npm install

RUN ng build


FROM python:3.13 AS backend

WORKDIR /app
# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
# Install postgresql client
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy from frontend stage with specific paths
COPY --from=frontend /HSA-frontend /app/HSA-frontend
COPY --from=frontend /build_django_index.py /app/
COPY --from=frontend /HSA-backend /app/HSA-backend

WORKDIR /app
RUN python3 build_django_index.py
WORKDIR /app/HSA-backend
ENV DATABASE_NAME=django_db
ENV DATABASE_USERNAME=django_user
ENV DATABASE_PASSWORD=123abc!
ENV DATABASE_IP=localhost


# Setup backend
RUN pip3 install --no-cache-dir -r requirements.txt
# Set up entrypoint script
# Set up entrypoint script
RUN chmod +x ../deployment/testing/integration/entrypoint.sh
RUN ../deployment/testing/integration/entrypoint.sh

