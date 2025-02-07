#!/bin/bash
# This is a script to automate Docker commands as a nice abstraction.
# Usage: ./script.sh <ignored> <build|run|secrets> [env_file_for_secrets]

# Ensure at least two arguments are provided.
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <build|run|secrets> [env_file_for_secrets]"
  exit 1
fi

COMMAND="$1"

if [ "$COMMAND" == "build" ]; then
  # Build the Docker image with the tag "hsa-app"
  docker build . -t "hsa-app"

elif [ "$COMMAND" == "clean" ]; then
    docker kill hsa-app
    docker rm hsa-app

elif [ "$COMMAND" == "run" ]; then
  # Check that all required environment variables are set
  if [ -z "$DATABASE_NAME" ] || [ -z "$DATABASE_IP" ] || [ -z "$DATABASE_USERNAME" ] || [ -z "$DATABASE_PASSWORD" ]; then
    echo "Please set DATABASE_NAME, DATABASE_IP, DATABASE_USERNAME, and DATABASE_PASSWORD."
    exit 1
  fi

  # Run the Docker container, passing the environment variables
  docker run --init --name "hsa-app" -p 8000:8000 \
    --env DATABASE_NAME="$DATABASE_NAME" \
    --env DATABASE_USERNAME="$DATABASE_USERNAME" \
    --env DATABASE_IP="$DATABASE_IP" \
    --env DATABASE_PASSWORD="$DATABASE_PASSWORD" \
    "hsa-app"

else
  echo "Invalid command: $COMMAND. Please use 'build', 'run', or 'secrets'."
  exit 1
fi
