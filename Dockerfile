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


# Run tests in headless mode
RUN ng test --watch=false --browsers=ChromeHeadless

# Run staging commands
RUN ng build


FROM python:3.13 AS backend
# Create necessary directories first
WORKDIR /app

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