#!/bin/bash
# This is a file for streaming angular straight to django views + templates
# It's mostly supposed to be for docker environment.

echo "Ensure this repository runs in the HSA-frontend folder"

ng build

mv dist/hsa-frontend/browser/index.html ../HSA-backend/templates/index.html
mv dist/hsa-frontend/browser/* ../HSA-backend/static

echo "Files moved."