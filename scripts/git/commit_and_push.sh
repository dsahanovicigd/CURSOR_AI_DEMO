#!/bin/bash

# Commit and push latest CI/CD pipeline fixes

set -e  # Exit on error

echo "=========================================="
echo "Committing and Pushing Latest Changes"
echo "=========================================="
echo ""

# Get current branch name
BRANCH=$(git branch --show-current)
echo "Current branch: $BRANCH"
echo ""

# Stage the workflow file
echo "📝 Staging workflow file..."
git add .github/workflows/ci-cd-unified.yml

# Show what will be committed
echo ""
echo "📋 Changes to be committed:"
git diff --cached --stat
echo ""

# Ask for confirmation
read -p "Do you want to commit these changes? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "❌ Commit cancelled."
    exit 1
fi

# Commit with message
echo ""
echo "💾 Committing changes..."
git commit -m "fix: resolve CI/CD pipeline errors

- Fix Flask app import error by adding explicit PYTHONPATH export
- Make Docker login conditional to avoid errors when secrets are missing
- Add permissions and conditional upload for Trivy security scan
- Fix security-events permission for SARIF uploads
- Handle fork PRs gracefully for security uploads

Fixes:
- Backend build: ModuleNotFoundError for 'app' module
- Docker build: Username and password required error
- Security scan: Resource not accessible by integration error"

echo ""
echo "✅ Commit successful!"
echo ""

# Ask if user wants to push
read -p "Do you want to push to origin/$BRANCH? (y/n) " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "⏸️  Push cancelled. You can push later with:"
    echo "   git push origin $BRANCH"
    exit 0
fi

# Push to remote
echo ""
echo "🚀 Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo ""
echo "✅ Successfully pushed to origin/$BRANCH!"
echo ""
echo "View your changes at:"
echo "https://github.com/$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/')/actions"
