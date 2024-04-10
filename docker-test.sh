#!/bin/bash

clear

# Define the name for your Docker container
CONTAINER_NAME="updawg-test"

# Check if a container with the specified name is running
if docker ps -a --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}\$"; then
    echo "Stopping and removing existing container: ${CONTAINER_NAME}"
    docker stop ${CONTAINER_NAME} >/dev/null
    docker rm ${CONTAINER_NAME} >/dev/null
fi

# Build the Docker image using the Dockerfile in the current directory
echo "Building Docker image..."
docker build -t my-ubuntu-image .

# Run a new container from the built image
echo "Starting new container: ${CONTAINER_NAME}"
docker run -it --name ${CONTAINER_NAME} my-ubuntu-image
