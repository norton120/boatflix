#!/bin/bash

# This script is used to initialize the host.
set -e

echo "Initializing host"
# Check if docker is installed
if ! command -v docker &> /dev/null; then
    echo "Docker not found, installing..."

    ## Update package list
    apt-get update -y

    echo "Adding Docker's official GPG key"
    curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --batch --yes --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
        "deb [arch=arm64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian \
        $(lsb_release -cs) stable" | \
        tee /etc/apt/sources.list.d/docker.list > /dev/null

    echo "Updating package list"
    apt-get update -y

    echo "Installing Docker Engine"
    apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

    echo "Starting and enabling Docker service"
    systemctl start docker
    systemctl enable docker

    echo "Adding current user to docker group"
    usermod -aG docker $USER

    echo "Docker installed successfully"
else
    echo "Docker is already installed"
fi
