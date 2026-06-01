#!/bin/bash

if ! docker ps -a --format '{{.Names}}' | grep -q '^askgit$'; then
  docker run -d -p 8000:8000 --name askgit dillonwebster/askgit
elif ! docker ps --format '{{.Names}}' | grep -q '^askgit$'; then
  docker start askgit
fi

echo "Waiting for server to start..."
until curl -s http://localhost:8000/health > /dev/null 2>&1; do
  sleep 1
done

while true; do
  read -p "You: " msg
  echo -n "Bot: "
  curl -s -X POST http://localhost:8000/chat \
    -H "Content-Type: application/json" \
    -d "{\"messages\": [{\"role\": \"user\", \"content\": \"$msg\"}]}"
  echo
done
