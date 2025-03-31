#!/bin/bash
set -e
set -x  # Enable debug output

# Fetch the latest ChromeDriver version
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
echo "Installing ChromeDriver version: $CHROMEDRIVER_VERSION"

# Verify download URL
DOWNLOAD_URL="https://chromedriver.storage.googleapis.com/${CHROMEDRIVER_VERSION}/chromedriver_linux64.zip"
echo "Downloading from: $DOWNLOAD_URL"

# Download ChromeDriver
wget -v "$DOWNLOAD_URL" -O /tmp/chromedriver.zip || {
    echo "Failed to download ChromeDriver"
    exit 1
}

# Unzip and install
unzip -o /tmp/chromedriver.zip -d /usr/local/bin/ || {
    echo "Failed to unzip ChromeDriver"
    exit 1
}

# Make executable
chmod +x /usr/local/bin/chromedriver

# Clean up
rm /tmp/chromedriver.zip

# Verify installation
chromedriver --version || {
    echo "ChromeDriver installation failed"
    exit 1
}