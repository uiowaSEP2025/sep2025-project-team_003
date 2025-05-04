FROM node:22-alpine AS frontend
# Copy the rest of the application
COPY . /app/
# Install Chrome and dependencies
RUN apk add --no-cache \
    --upgrade bash \
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
WORKDIR /app/HSA-frontend

# Copy package files first for better caching
COPY package*.json ./
RUN npm install -g @angular/cli
RUN npm install

COPY ./deployment/testing/frontend/entrypoint.sh /app/HSA-frontend/entrypoint.sh

# Set up entrypoint script
RUN chmod +x entrypoint.sh
ENTRYPOINT ["/app/HSA-frontend/entrypoint.sh"]

