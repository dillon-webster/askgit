#!/bin/sh
ollama serve &
until ollama list > /dev/null 2>&1; do 
  sleep 1
done
exec uvicorn server.main:app --host 0.0.0.0 --port 8000
