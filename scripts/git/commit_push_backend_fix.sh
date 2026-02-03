#!/bin/bash

# Commit and push backend build fix

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
git commit -m "fix: correct Flask app import path in backend build verification

- Simplify Python path handling in Flask app verification step
- Remove redundant PYTHONPATH export (already set in env)
- Use sys.path.insert with current directory directly
- Fix ModuleNotFoundError: No module named 'app' error

The working-directory is already set to ./flask_api, so we just need
to add '.' to sys.path to find the app module."

echo ""
echo "🚀 Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo ""
echo "✅ Successfully committed and pushed!"
