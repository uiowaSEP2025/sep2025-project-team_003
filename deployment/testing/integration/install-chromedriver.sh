#!/bin/bash
set -e

# Get Chrome version
CHROME_VERSION=$(google-chrome --version | cut -d ' ' -f 3 | cut -d '.' -f 1)
echo "Detected Chrome version: $CHROME_VERSION"

# Function to get the latest compatible ChromeDriver
get_chromedriver_version() {
    local major_version=$1

    # Try descending versions until we find a compatible ChromeDriver
    while [ $major_version -gt 0 ]; do
        echo "Trying to find ChromeDriver for version $major_version" >&2

        # Attempt to get the latest release for this version
        DRIVER_VERSION=$(curl -sS "https://chromedriver.storage.googleapis.com/LATEST_RELEASE_${major_version}" 2>/dev/null)

        # Check if we got a valid version
        if [[ "$DRIVER_VERSION" =~ ^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$ ]]; then
            echo "$DRIVER_VERSION"
            return 0
        fi

        # Decrement version and try again
        major_version=$((major_version - 1))
    done

    # If all else fails, get the latest overall version
    curl -sS https://chromedriver.storage.googleapis.com/LATEST_RELEASE
}

# Get the appropriate ChromeDriver version
CHROME_DRIVER_VERSION=$(get_chromedriver_version $CHROME_VERSION)
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