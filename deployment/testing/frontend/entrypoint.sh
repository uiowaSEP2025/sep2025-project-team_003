#!/bin/bash
set -e
set -x

# Run tests in headless mode
ng test --watch=false --browsers=ChromeHeadless --code-coverage