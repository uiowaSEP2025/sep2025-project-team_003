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

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql \
    postgresql-contrib \
    libpq-dev \
    python3-dev \
    gcc \
    wget \
    unzip \
    curl \
    gnupg \
    xvfb \
    && wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable
# Set environment variables
ENV CHROME_BIN=/usr/bin/google-chrome
ENV DISPLAY=:99

# Copy from frontend stage with specific paths
COPY --from=frontend /HSA-frontend /app/HSA-frontend
COPY --from=frontend /build_django_index.py /app/
COPY --from=frontend /HSA-backend /app/HSA-backend
COPY --from=frontend /deployment /app/deployment


WORKDIR /app
RUN python3 build_django_index.py
WORKDIR /app/HSA-backend
ENV DATABASE_NAME=django_db
ENV DATABASE_USERNAME=django_user
ENV DATABASE_PASSWORD=123abc!
ENV DATABASE_IP=localhost
ENV INTEGRATION_FLAG=1
# In the Dockerfile
RUN chmod +x ../deployment/testing/integration/install-chromedriver.sh \
    && chmod +x ../deployment/testing/integration/install-chrome.sh

RUN ../deployment/testing/integration/install-chromedriver.sh
RUN ../deployment/testing/integration/install-chrome.sh

# Setup backend
RUN pip3 install --no-cache-dir -r requirements.txt

# Set up entrypoint script
RUN chmod +x ../deployment/testing/integration/entrypoint.sh
RUN ../deployment/testing/integration/entrypoint.sh