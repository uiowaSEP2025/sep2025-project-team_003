#!/bin/bash
set -e
set -x

# Run tests in headless mode
ng test --watch=false --browsers=ChromeHeadless --code-coverage

# Optionally, create a summary of the coverage for easier parsing
npx istanbul report text-summary