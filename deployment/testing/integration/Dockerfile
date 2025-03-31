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


FROM python:3.13 AS backend

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install system dependencies including PostgreSQL, build tools, and utilities for installing Chrome
RUN apt-get update && apt-get install -y \
wget \
gnupg2 \
postgresql \
postgresql-contrib \
libpq-dev \
python3-dev \
gcc \
xvfb

# Add the Google Chrome signing key and repository, then install Google Chrome Stable
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - && \
echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" \
> /etc/apt/sources.list.d/google-chrome.list && \
apt-get update && \
apt-get install -y google-chrome-stable

# (Optional) Cleanup APT caches to reduce image size
RUN rm -rf /var/lib/apt/lists/*

# Copy the application code and set working directory
COPY . /app
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

# Set up entrypoint script for testing
RUN chmod +x ../deployment/testing/integration/entrypoint.sh
RUN ../deployment/testing/integration/entrypoint.sh