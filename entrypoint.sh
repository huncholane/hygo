#!/bin/bash
if [ -f .env ]; then
    docker compose down
    docker compose up -d --build --remove-orphans
else
    echo "No .env file found. Please create one and try again."
fi