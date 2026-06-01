FROM ollama/ollama
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY server/requirements.txt .
RUN pip3 install --break-system-packages -r requirements.txt

COPY server/ ./server/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

RUN ollama serve & sleep 5 && ollama pull llama3.2:3b

EXPOSE 8000

ENTRYPOINT ["./entrypoint.sh"]
