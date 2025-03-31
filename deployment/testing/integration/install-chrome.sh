#!/bin/bash
set -e

# Fetch the latest ChromeDriver version
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
echo "Latest ChromeDriver version: $CHROMEDRIVER_VERSION"

# Extract Chrome major version from ChromeDriver version
CHROME_MAJOR_VERSION=$(echo $CHROMEDRIVER_VERSION | cut -d. -f1)

# Download specific Chrome version
wget -q https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_MAJOR_VERSION}-1_amd64.deb -O /tmp/chrome.deb

# Remove existing Chrome
apt-get remove -y google-chrome-stable

# Install the specific Chrome version
dpkg -i /tmp/chrome.deb || apt-get install -y -f

# Clean up
rm /tmp/chrome.deb

# Verify installation
google-chrome --version