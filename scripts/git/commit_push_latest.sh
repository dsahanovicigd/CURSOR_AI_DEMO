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

# Commit with message
echo "💾 Committing changes..."
git commit -m "fix: remove invalid secret checks from GitHub Actions conditions

- Remove secret checks from Docker login if conditions (secrets cannot be checked in if statements)
- Add continue-on-error to Docker login to handle missing secrets gracefully
- Simplify Docker push conditions to only check event type
- Fix 'Unrecognized named-value: secrets' errors in workflow validation

Fixes:
- Line 768: Frontend Docker login condition
- Line 812: Backend Docker login condition
- Lines 787, 825: Docker push conditions"

echo ""
echo "✅ Commit successful!"
echo ""

# Push to remote
echo "🚀 Pushing to origin/$BRANCH..."
git push origin "$BRANCH"

echo ""
echo "✅ Successfully pushed to origin/$BRANCH!"
echo ""
echo "View your changes at:"
REPO_URL=$(git config --get remote.origin.url | sed 's/.*github.com[:/]\(.*\)\.git/\1/' | sed 's/^git@github.com://')
if [ ! -z "$REPO_URL" ]; then
    echo "https://github.com/$REPO_URL/actions"
fi
