#!/bin/bash

# Commit latest CI/CD pipeline fixes

echo "Staging workflow file..."
git add .github/workflows/ci-cd-unified.yml

echo ""
echo "Files staged. Review with: git diff --cached"
echo ""
echo "Committing with message..."
echo ""

git commit -m "fix: resolve GitHub Actions workflow validation errors

- Fix environment.url field to use static URLs instead of secrets expressions
- Update deployment steps to handle secrets with shell variable fallbacks
- Resolve 'Unrecognized named-value: secrets' errors in environment blocks
- Maintain secret usage in deployment steps where allowed

Fixes:
- Line 843: staging environment.url now uses static URL
- Line 922: production environment.url now uses static URL
- Deployment steps use secrets with proper fallback handling"

echo ""
echo "✅ Commit completed!"
echo ""
echo "To push: git push origin <branch-name>"
