# Start from Ollama's official image — it already has the Ollama
# AI model runtime installed and ready to go.
FROM ollama/ollama

# Install Python and pip (the base image doesn't include them), then
# clean up the apt cache afterward to keep the image smaller.
RUN apt-get update && apt-get install -y python3 python3-pip && rm -rf /var/lib/apt/lists/*

# Set the working directory inside the container. Everything after this
# runs from /app, and COPY destinations are relative to it.
WORKDIR /app

# Copy only the requirements file first. Docker caches each layer, so as
# long as requirements.txt doesn't change, the pip install below is reused
# from cache instead of re-running on every build.
COPY server/requirements.txt .

# Install the Python dependencies. --break-system-packages allows pip to
# install into the system Python (needed on newer Debian-based images).
RUN pip3 install --break-system-packages -r requirements.txt

# Now copy the rest of the app code in (done after pip install so code
# changes don't bust the dependency cache layer above).
COPY server/ ./server/

# Copy the startup script and make it executable.
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

# Store models at /models instead of Ollama's default /root/.ollama. The
# base image declares /root/.ollama as a VOLUME, and Docker discards
# anything written to a VOLUME path during build — so a model pulled there
# never ends up in the final image. /models is a normal path that persists.
# This ENV applies at build AND runtime, so the server reads the same place.
ENV OLLAMA_MODELS=/models

# Bake the AI model into the image: start the Ollama server in the
# background, wait for it to come up, then pull llama3.2:3b. This means the
# ~2GB model ships inside the image — no download needed at runtime.
RUN ollama serve & sleep 5 && ollama pull llama3.2:3b

# Document that the container listens on port 8000 (the FastAPI server).
EXPOSE 8000

# The command that runs when the container starts. entrypoint.sh launches
# Ollama and then the FastAPI app.
ENTRYPOINT ["./entrypoint.sh"]
