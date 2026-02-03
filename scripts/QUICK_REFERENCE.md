# Scripts Quick Reference

Quick reference guide for commonly used scripts.

## 🚀 Most Used Scripts

### Start Development
```bash
./scripts/development/start-all-services.sh
```

### Stop Development
```bash
./scripts/development/stop-all-services.sh
```

### Run Tests
```bash
./scripts/testing/run_tests.sh
```

### Commit Changes
```bash
./scripts/git/commit_and_push.sh "Your commit message"
```

### Check CI/CD
```bash
./scripts/ci-cd/check-workflows.sh
```

## 📍 Script Locations

| Purpose | Location |
|---------|----------|
| Development | `scripts/development/` |
| Backend | `scripts/backend/` |
| Testing | `scripts/testing/` |
| Git | `scripts/git/` |
| CI/CD | `scripts/ci-cd/` |
| QA | `qa-automation/scripts/` |

## 🔍 Find a Script

```bash
# Find by name
find scripts -name "*keyword*"

# List all scripts
find scripts -type f -name "*.sh"
```
