#!/bin/bash
set -e

# Fetch the latest ChromeDriver version
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"

# Download ChromeDriver
wget -q "https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip" -O /tmp/chromedriver.zip

# Unzip and install
unzip /tmp/chromedriver.zip -d /usr/local/bin/
chmod +x /usr/local/bin/chromedriver

# Clean up
rm /tmp/chromedriver.zip

# Verify installation
chromedriver --version