#!/bin/bash
# This script:
# 1. Builds the Docker image
# 2. Transfers it to a remote host via SCP
# 3. Ensures the remote container uses the new image tagged as latest

# WARNING: Using an image hub (e.g., Docker Hub) is strongly recommended.

# Required environment variables:
# - SSHURL: SSH target in user@host format
# - SSHPASS (optional): If using a password (not recommended)
# - Ensure SSH key authentication is set up for best security.

if [ -z "$SSHURL" ]; then
  echo "Error: SSHURL is not set."
  exit 1
fi

# Build Docker image
docker build -t hsa-app .

# Transfer Docker image to remote host
if [ "$1" == "pass" ]; then
  if [ -z "$SSHPASS" ]; then
    echo "Error: SSHPASS is not set."
    exit 1
  fi
  # clean on host
  sshpass -p "$SSHPASS" ssh -o StrictHostKeyChecking=no "$SSHURL" 'ctr images rm hsa-app:latest'
  docker save hsa-app | sshpass -p "$SSHPASS" ssh -o "StrictHostKeyChecking no" -C "$SSHURL" "ctr image import -"
else
  echo "Non-auto is not supported. Please run this with "pass" and set SSHPASS"
fi