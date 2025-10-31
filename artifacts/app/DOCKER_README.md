# Docker Quick Start

## Build the Image
From the `artifacts/app` directory:

```pwsh
# Pick an image name (change if you like)
# cd to artifacts/app
$IMAGE_NAME="my-app"

# Build
docker build -t $IMAGE_NAME .
```

## Run the Container
Map host port 3001 to container port 3001:

```pwsh
docker run --name ${IMAGE_NAME}-ctr -p 3001:3001 $IMAGE_NAME
```

Then open: http://localhost:3001

## Detached Mode
```pwsh
docker run -d --name ${IMAGE_NAME}-ctr -p 3001:3001 $IMAGE_NAME
```
List containers:
```pwsh
docker ps
```

## Stop / Remove All Existing Docker Containers (Recursive)
```pwsh
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
```

## Logs
```pwsh
docker logs -f ${IMAGE_NAME}-ctr
```

## Troubleshooting
- "Site can’t be reached" → Ensure you used `-p 3001:3001` and browse `http://localhost:3001` (not `0.0.0.0`).
- Port already in use → Pick another host port: `docker run -p 8080:3001 $IMAGE_NAME` then browse http://localhost:8080.
- Container exits immediately → Check logs: `docker logs ${IMAGE_NAME}-ctr`.
- Code changes not showing → Rebuild the image.

`EXPOSE 3001` documents the container port; it does not publish it—`-p` does.

## Compose (Optional)
```yaml
services:
  app:
    build: .
    ports:
      - "3001:3001"
```

## FastAPI App Reference
The command in the Dockerfile runs:
```
uvicorn main:app --host 0.0.0.0 --port 3001
```
Ensure `main.py` defines `app = FastAPI()`.

---
Minimal, portable, and ready to copy-paste.