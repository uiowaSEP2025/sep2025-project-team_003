#!/bin/bash
set -e

# Get Chrome version
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1)
echo "Detected Chrome version: $CHROME_VERSION"

# Try to get ChromeDriver version for specific Chrome version
CHROME_DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${CHROME_VERSION}" || echo "")

# If specific version fails, use latest
if [ -z "$CHROME_DRIVER_VERSION" ]; then
    CHROME_DRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
fi

echo "Using ChromeDriver version: $CHROME_DRIVER_VERSION"

# Download ChromeDriver
wget -q "https://chromedriver.storage.googleapis.com/${CHROME_DRIVER_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip

# Unzip and install
unzip /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Clean up
rm /tmp/chromedriver.zip

# Verify installation
chromedriver --version