FROM node:22-alpine AS frontend
# Copy the rest of the application
COPY . .

# Set working directory
WORKDIR /HSA-frontend

# Copy package files first for better caching
COPY package*.json ./
RUN npm install -g @angular/cli
RUN npm install

# Run staging commands
RUN ng build --configuration=staging


FROM python:3.13 AS backend
# Create necessary directories first
WORKDIR /app

ARG DATABASE_IP
ARG DATABASE_USERNAME
ARG DATABASE_PASSWORD
ARG DATABASE_NAME
ARG EMAIL_HOST
ARG EMAIL_HOST_USER
ARG EMAIL_HOST_PASSWORD
ENV DATABASE_IP=$DATABASE_IP
ENV DATABASE_USERNAME=$DATABASE_USERNAME
ENV DATABASE_PASSWORD=$DATABASE_PASSWORD
ENV DATABASE_NAME=$DATABASE_NAME
ENV EMAIL_HOST = $EMAIL_HOST
ENV EMAIL_HOST_USER = $EMAIL_HOST_USER
ENV EMAIL_HOST_PASSWORD = $EMAIL_HOST_PASSWORD

# Copy from frontend stage with specific paths
COPY --from=frontend /HSA-frontend /app/HSA-frontend
COPY --from=frontend /build_django_index.py /app/
COPY --from=frontend /HSA-backend /app/HSA-backend

# Run the build script
WORKDIR /app
RUN python3 build_django_index.py

# Setup backend
WORKDIR /app/HSA-backend
RUN pip3 install -r requirements.txt

# Final server command
STOPSIGNAL SIGINT
CMD python3 manage.py runserver 0.0.0.0:8000
