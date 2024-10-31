#!/bin/bash

# URL to check
URL="http://localhost"

# Check the HTTP status code
STATUS=$(curl -o /dev/null -s -w "%{http_code}" $URL)

# If the status is not 200, restart Docker Compose services
if [ "$STATUS" -ne 200 ]; then
  echo "Service not responding with 200. Restarting Docker Compose services..."
  docker compose down
  docker compose up -d
else
  echo "Service is up with status 200."
fi
