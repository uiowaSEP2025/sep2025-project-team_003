#!/bin/bash
set -e
set -x


function init_pg {
  # Start PostgreSQL
  su-exec postgres pg_ctl -D /var/lib/postgresql/data start

  # Wait for PostgreSQL to be ready
  until pg_isready; do
      echo "Waiting for PostgreSQL to start..."
      sleep 2
  done
}

TESTING_ENV=${1:-frontend}

function run_test {
  case "$TESTING_ENV" in
  frontend)
    echo "Running Frontend Tests"
    export CHROME_BIN="/usr/bin/google-chrome"
    cd /app/HSA-frontend/
    ng test --watch=false --browsers=ChromeHeadless
    ;;
  backend)
    echo "Running Backend Tests"
    init_pg
    cd /app/HSA-backend/
    python manage.py test -v 2
    ;;
  integration)
    echo "Running Integration Tests"
    # Start Xvfb
    Xvfb :99 -ac &
    export DISPLAY=:99
    init_pg
    cd /app/HSA-backend/
    python manage.py behave
    # Cleanup
    pkill Xvfb
    ;;
  *)
    echo "Unknown test mode: $TESTING_ENV"
    echo "Available modes: frontend, backend, integration"
    exit 1
    ;;
  esac
}

# Run the test
run_test