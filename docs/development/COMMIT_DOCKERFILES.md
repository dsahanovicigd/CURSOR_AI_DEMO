# Commit Dockerfiles to Git

## Issue
Dockerfiles exist locally but are **not tracked in git**, causing CI builds to skip.

## Files to Commit

1. `Dockerfile.frontend` - Frontend Docker image
2. `flask_api/Dockerfile` - Backend Docker image

## Commands

```bash
# Add Dockerfiles to git
git add Dockerfile.frontend flask_api/Dockerfile

# Commit
git commit -m "Add Dockerfiles for frontend and backend builds"

# Push
git push origin main
```

## After Committing

Once committed, the Docker build jobs will:
- ✅ Find the Dockerfiles in CI
- ✅ Build Docker images successfully
- ✅ Push images to container registry

## Current Behavior (Before Commit)

- ⚠️ Docker builds are skipped gracefully (no errors)
- ⚠️ Workflows continue without Docker builds
- ⚠️ No Docker images are created

## Verification

After committing, verify:
1. Docker build jobs complete successfully
2. Images are pushed to registry (if configured)
3. No "Dockerfile not found" warnings
