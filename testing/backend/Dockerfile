FROM python:3.13 AS backend
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

COPY . /app
WORKDIR /app/HSA-backend
ENV DATABASE_NAME=django_db
ENV DATABASE_USERNAME=django_user
ENV DATABASE_PASSWORD=123abc!
ENV DATABASE_IP=localhost


# Setup backend
RUN pip3 install --no-cache-dir -r requirements.txt
# Set up entrypoint script
# Set up entrypoint script
RUN chmod +x ../testing/backend/entrypoint.sh
RUN ../testing/backend/entrypoint.sh

