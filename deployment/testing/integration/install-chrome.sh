#!/bin/bash
set -e
set -x  # Enable debug output

# Update package lists
apt-get update

# Fetch the latest ChromeDriver version
CHROMEDRIVER_VERSION=$(curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE)
echo "Latest ChromeDriver version: $CHROMEDRIVER_VERSION"

# Extract Chrome major version from ChromeDriver version
CHROME_MAJOR_VERSION=$(echo $CHROMEDRIVER_VERSION | cut -d. -f1)
CHROME_FULL_VERSION="${CHROME_MAJOR_VERSION}.0.6998.0"

echo "Attempting to download Chrome version: $CHROME_FULL_VERSION"

# Construct download URL
CHROME_URL="https://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_${CHROME_FULL_VERSION}-1_amd64.deb"

# Download Chrome
wget -v "$CHROME_URL" -O /tmp/chrome.deb || {
    echo "Failed to download Chrome from $CHROME_URL"
    # Print out available versions
    echo "Checking available versions:"
    curl -s https://dl.google.com/linux/chrome/deb/dists/stable/main/binary-amd64/Packages | grep "google-chrome-stable" | grep "Version"
    exit 1
}

# Remove existing Chrome
apt-get remove -y google-chrome-stable || true

# Install dependencies
apt-get install -y \
    wget \
    gnupg \
    libgconf-2-4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libxss1 \
    libxshmfence-dev \
    libgbm1

# Install the specific Chrome version
dpkg -i /tmp/chrome.deb || {
    # If dpkg fails, try to fix dependencies
    apt-get install -y -f
    dpkg -i /tmp/chrome.deb
}

# Clean up
rm /tmp/chrome.deb

# Verify installation
google-chrome --version || {
    echo "Chrome installation failed"
    exit 1
}