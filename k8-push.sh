#!/bin/bash
# This script:
# 1. Builds the Docker image
# 2. Transfers it to dockerhub
# 3. Runs the terraform to update k8s
# Build Docker image

docker build -t mzeng1417/hsa-image-store:latest .

# Transfer Docker image to remote host
docker push mzeng1417/hsa-image-store:latest

kubectl delete service hsa-app-service
kubectl delete pods hsa-app

# adjust the YAML
sed -e "s|\${DATABASE_NAME}|${DATABASE_NAME}|g" \
    -e "s|\${DATABASE_USERNAME}|${DATABASE_USERNAME}|g" \
    -e "s|\${DATABASE_IP}|${DATABASE_IP}|g" \
    -e "s|\${DATABASE_PASSWORD}|${DATABASE_PASSWORD}|g" \
    kubernates/hsa-app-template.yaml > terraform.tf.yaml

#kubectl apply -f terraform.tf.yaml
kubectl apply -f kubernates/hsa-app-service.yaml