# Scripts Directory

This directory contains all executable scripts organized by purpose for easy navigation.

## 📁 Directory Structure

```
scripts/
├── README.md                    # This file
├── development/                 # Development and service management
├── testing/                     # Testing scripts
├── git/                         # Git and version control scripts
├── ci-cd/                       # CI/CD related scripts
├── qa/                          # QA automation scripts (links)
└── backend/                     # Backend-specific scripts
```

## 🚀 Quick Start

### Development Scripts
- `development/start-all-services.sh` - Start all services (frontend, backend, Redis)
- `development/stop-all-services.sh` - Stop all services
- `development/investigate_redis.sh` - Investigate Redis activity

### Backend Scripts
- `backend/start.sh` - Start Flask API server
- `backend/stop.sh` - Stop Flask API server
- `backend/setup.sh` - Setup Flask API environment

### Testing Scripts
- `testing/run_tests.sh` - Run Flask API tests
- `testing/run_unittest.sh` - Run Flask API unit tests

### Git Scripts
- `git/COMMIT_COMMAND.sh` - Standard commit command
- `git/commit_and_push.sh` - Commit and push changes
- `git/commit_latest.sh` - Commit latest changes
- `git/commit_push_*.sh` - Various commit and push scripts

### CI/CD Scripts
- `ci-cd/check-workflows.sh` - Check GitHub Actions workflows

### QA Scripts
QA automation scripts are located in `qa-automation/scripts/`:
- `qa-automation/scripts/master-qa-runner.sh` - Master QA runner
- `qa-automation/scripts/run-all-qa.sh` - Run all QA tests
- `qa-automation/scripts/run-performance-tests.sh` - Performance tests
- `qa-automation/scripts/run-security-scan.sh` - Security scans

---

## 📋 Script Categories

### 🔧 Development Scripts
Scripts for managing development environment and services.

| Script | Description |
|--------|-------------|
| `start-all-services.sh` | Start all application services |
| `stop-all-services.sh` | Stop all application services |
| `investigate_redis.sh` | Investigate Redis connection and activity |

### 🔙 Backend Scripts
Flask API specific scripts.

| Script | Description |
|--------|-------------|
| `start.sh` | Start Flask API server |
| `stop.sh` | Stop Flask API server |
| `setup.sh` | Setup Flask API development environment |

### 🧪 Testing Scripts
Scripts for running tests.

| Script | Description |
|--------|-------------|
| `run_tests.sh` | Run Flask API test suite |
| `run_unittest.sh` | Run Flask API unit tests |

### 📦 Git Scripts
Scripts for Git operations and version control.

| Script | Description |
|--------|-------------|
| `COMMIT_COMMAND.sh` | Standard commit command template |
| `commit_and_push.sh` | Commit changes and push to remote |
| `commit_latest.sh` | Commit latest changes |
| `commit_push_backend_fix.sh` | Commit and push backend fixes |
| `commit_push_final_fixes.sh` | Commit and push final fixes |
| `commit_push_fixes.sh` | Commit and push general fixes |
| `commit_push_latest.sh` | Commit and push latest changes |
| `commit_push_zap_fix.sh` | Commit and push ZAP scan fixes |

### 🔄 CI/CD Scripts
Scripts for Continuous Integration/Continuous Deployment.

| Script | Description |
|--------|-------------|
| `check-workflows.sh` | Check GitHub Actions workflow status |

### ✅ QA Scripts
Quality Assurance automation scripts (located in `qa-automation/scripts/`).

| Script | Location | Description |
|--------|----------|-------------|
| `master-qa-runner.sh` | `qa-automation/scripts/` | Master QA test runner |
| `run-all-qa.sh` | `qa-automation/scripts/` | Run all QA tests |
| `run-performance-tests.sh` | `qa-automation/scripts/` | Run performance tests |
| `run-security-scan.sh` | `qa-automation/scripts/` | Run security scans |
| `security-scan.sh` | `qa-automation/security/` | Security scanning script |
| `setup-python-deps.sh` | `qa/` | Setup Python dependencies for QA |

---

## 🎯 Usage Examples

### Start Development Environment
```bash
./scripts/development/start-all-services.sh
```

### Run Tests
```bash
./scripts/testing/run_tests.sh
```

### Commit Changes
```bash
./scripts/git/commit_and_push.sh "Your commit message"
```

### Check CI/CD Status
```bash
./scripts/ci-cd/check-workflows.sh
```

### Run QA Tests
```bash
./qa-automation/scripts/run-all-qa.sh
```

---

## 📝 Adding New Scripts

When adding new scripts:

1. **Choose the right category**:
   - Development/service management → `development/`
   - Testing → `testing/`
   - Git operations → `git/`
   - CI/CD → `ci-cd/`
   - Backend-specific → `backend/`
   - QA → `qa-automation/scripts/`

2. **Follow naming conventions**:
   - Use lowercase with hyphens: `script-name.sh`
   - Make scripts executable: `chmod +x script-name.sh`
   - Add shebang: `#!/bin/bash`

3. **Update this README** with the new script

---

## 🔍 Finding Scripts

- **By purpose**: Check the category directories
- **By name**: Use `find scripts -name "*keyword*"`
- **By location**: Original locations preserved in comments

---

*Last Updated: January 2026*
