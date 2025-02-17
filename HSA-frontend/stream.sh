#!/bin/bash
# This is a file for streaming angular straight to django views + templates
# It's mostly supposed to be for docker environment.

if [ "$#" -lt 1 ]; then
  echo "Usage: $0 <development|staging|prod> "
  exit 1
fi

ENV="$1"

echo "Ensure this repository runs in the HSA-frontend folder"

ng build --c=$ENV

mv dist/hsa-frontend/browser/index.html ../HSA-backend/templates/index.html
mv dist/hsa-frontend/browser/* ../HSA-backend/static

echo "Files moved."