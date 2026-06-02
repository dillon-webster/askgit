# askgit

An AI-powered Git tutor in your terminal. Ask questions, get unstuck, and build a real
understanding of Git — all without leaving the command line.

Everything runs **locally inside a Docker container** — the AI model is baked right into
the image. No API keys, no accounts, no cloud. Nothing you type ever leaves your machine.

## Prerequisites

- [Docker](https://www.docker.com/products/docker-desktop/) installed and running.

That's it. You don't need Python, Ollama, or to download a model yourself — it's all in
the image.

## Quick start

Pick a folder you'll remember (your home directory is fine), then run one command:

```bash
cd ~
curl -s https://raw.githubusercontent.com/dillon-webster/askgit/main/chat.sh -o chat.sh && chmod +x chat.sh && ./chat.sh
```

This downloads a small helper script (`chat.sh`), which:

1. Pulls the `dillonwebster/askgit` image from Docker Hub (the **first run** downloads
   ~5GB — the runtime, server, and AI model bundled together; this only happens once).
2. Starts it as a container on port 8000.
3. Waits for the server, then drops you at a `You:` prompt.

Ask anything about Git, then press Enter. Press `Ctrl+C` to exit.

## Running it again

No re-downloading — the image is cached. Just go back to the same folder and run the
script again:

```bash
cd ~
./chat.sh
```

It reuses the running container, or restarts a stopped one in a second or two — you're
back at the `You:` prompt almost instantly.

## Linux note

On Linux you may hit `permission denied while trying to connect to the Docker daemon`.
Add your user to the `docker` group once:

```bash
sudo usermod -aG docker $USER
newgrp docker            # or log out and back in
```

Then re-run `./chat.sh`. (Mac/Windows Docker Desktop users don't need this.)

## Examples

```
You: How do I start a new repository?
You: How do I create a new feature branch?
You: What does git status show me?
You: I made changes on main, how do I move them to a new branch?
You: What's the difference between git add and git commit?
```

## How it works

- A **FastAPI** server (in `server/`) exposes a `/chat` endpoint.
- **Ollama** runs the `llama3.2:3b` model, baked into the image at build time.
- The `Dockerfile` bundles all of it into one image so it runs the same on any machine.
- `chat.sh` is just a convenience wrapper around `docker run` plus a simple chat loop.
