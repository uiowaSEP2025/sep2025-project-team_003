#!/bin/bash
set -e
set -x

# Run tests in headless mode
RUN ng test --watch=false --browsers=ChromeHeadless