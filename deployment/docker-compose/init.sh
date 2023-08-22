#!/usr/bin/env bash

# Prepare database directory
mkdir db

# Create configuration file
touch config.yaml

# Download docker-compose.yaml
curl -sL https://raw.githubusercontent.com/thevops/RSSAssistant/master/deployment/docker-compose/docker-compose.yaml -o docker-compose.yaml

# Pull Docker image
docker compose pull

# Information
echo "Please edit 'config.yaml' and run 'docker compose up -d' to start the application."
