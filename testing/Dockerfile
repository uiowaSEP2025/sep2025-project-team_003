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