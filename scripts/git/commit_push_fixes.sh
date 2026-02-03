#!/bin/bash

# Commit and push fixes for backend build and Docker tags

set -e

BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
echo ""

echo "📝 Staging workflow file..."
git add .github/workflows/ci-cd-unified.yml

echo ""
echo "📋 Changes:"
git diff --cached --stat

echo ""
echo "💾 Committing..."
git commit -m "fix: resolve backend build and Docker tag errors

Backend Build Fix:
- Use os.getcwd() instead of '.' for more reliable path resolution
- Ensure PYTHONPATH is correctly set to flask_api directory
- Fix ModuleNotFoundError: No module named 'app' error

Docker Tag Fix:
- Add step to conditionally set Docker tags based on DOCKER_USERNAME secret
- Use shell script to build tags dynamically
- Provide fallback 'local' tags when secret is not available
- Fix 'invalid reference format' error when DOCKER_USERNAME is empty
- Make cache-from and cache-to conditional as well
- Only push images when DOCKER_USERNAME is set and not a PR

Changes:
- Backend: Use os.getcwd() for absolute path resolution
- Frontend Docker: Conditional tags with format() function
- Backend Docker: Conditional tags with format() function"

echo ""
echo "🚀 Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo ""
echo "✅ Successfully committed and pushed!"
