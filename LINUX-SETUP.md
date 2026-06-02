# askgit on Linux — quick setup & troubleshooting

## Run it (same command the class uses)
```
cd ~
curl -s https://raw.githubusercontent.com/dillon-webster/askgit/main/chat.sh -o chat.sh && chmod +x chat.sh && ./chat.sh
```
- First run pulls ~5GB from Docker Hub (once). After that it's instant.
- `Ctrl+C` exits the chat; the container keeps running in the background.
- Re-open later: `cd ~` then `./chat.sh` (no re-download).
- No `docker login` needed — the image is public.

## "permission denied while trying to connect to the Docker API"
Your user isn't in the `docker` group. Fix it once:
```
sudo usermod -aG docker $USER   # add yourself to the docker group
newgrp docker                   # apply it in this shell (or log out/in)
docker ps                       # should now work with NO permission error
./chat.sh                       # re-run
```
Quick alternative (not the clean fix): `sudo ./chat.sh`

## Other gotchas
- **Daemon not running:** `sudo systemctl start docker`
- **curl missing:** `sudo apt install curl`
- **Port 8000 in use:** something else is on :8000 — stop it, or you'll get a bind error.
- **`pull access denied` / requires login:** the image is private — make
  `dillonwebster/askgit` public at hub.docker.com → repo → Settings.

## Useful checks
```
docker ps              # running containers
docker ps -a           # all containers (incl. stopped 'askgit')
docker logs askgit     # see the server's output if something's wrong
docker stop askgit     # stop it
docker rm askgit       # delete the container (image stays cached)
```
