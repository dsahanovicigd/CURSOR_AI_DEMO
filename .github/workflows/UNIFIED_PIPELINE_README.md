# Unified CI/CD Pipeline

## Overview

This is a unified, optimized CI/CD pipeline that combines the best features from three previous pipelines:
- `basic-ci-cd.yml` - Basic CI/CD with security scanning
- `ci-cd-optimized.yml` - Optimized pipeline with caching and blue-green deployment
- `ci-cd-ultra-optimized.yml` - Ultra-optimized with advanced caching and parallel execution

## Key Features

### 🚀 Performance Optimizations

1. **Advanced Caching**
   - Node.js dependencies (`node_modules`, npm cache)
   - Python dependencies (pip cache)
   - Vite build cache
   - Playwright browser cache
   - Docker layer caching

2. **Parallel Execution**
   - Frontend tests split into unit/integration/e2e
   - Backend tests split into unit/integration/api
   - Security scans run in parallel
   - Docker builds run in parallel

3. **Smart Dependency Management**
   - Conditional caching based on file existence
   - Cache hit detection to skip unnecessary installs
   - Optimized npm/pip install commands

### 🔒 Security

1. **Frontend Security**
   - npm audit
   - Snyk scanning
   - CodeQL analysis (JavaScript/TypeScript)

2. **Backend Security**
   - Safety (Python dependency vulnerabilities)
   - Bandit (Python SAST)
   - CodeQL analysis (Python)
   - Trivy container scanning

3. **Container Security**
   - Trivy vulnerability scanning
   - SARIF upload to GitHub Security

### 🧪 Testing Strategy

1. **Frontend Tests**
   - Unit tests (auth, navigation, registration)
   - Integration tests (product-search, task-management, accessibility)
   - E2E tests (error-handling, responsive)

2. **Backend Tests**
   - Unit tests with coverage
   - Integration tests with PostgreSQL
   - API comprehensive tests
   - Performance tests (Locust)

3. **Test Execution**
   - Parallel test execution (`pytest-xdist`)
   - Test result artifacts
   - Coverage reports (HTML, XML, JSON)

### 🐳 Docker

1. **Multi-stage Builds**
   - Frontend Docker image
   - Backend Docker image
   - Docker Buildx for advanced features

2. **Caching**
   - Registry-based cache
   - Layer caching
   - Build cache optimization

### 🚢 Deployment

1. **Blue-Green Deployment**
   - Zero-downtime deployments
   - Automatic environment detection
   - Traffic switching after smoke tests
   - Health monitoring
   - Automatic rollback on failure

2. **Environments**
   - Staging (develop branch)
   - Production (main branch)
   - Manual workflow dispatch support

3. **Deployment Safety**
   - Smoke tests before traffic switch
   - Health monitoring after deployment
   - Automatic rollback on failure
   - Deployment status tracking

### 📊 Monitoring & Notifications

1. **Slack Notifications**
   - Deployment success/failure
   - Workflow status
   - Commit and author information

2. **Artifacts**
   - Build artifacts (7-day retention)
   - Test reports
   - Coverage reports
   - Security reports

## Pipeline Structure

```
┌─────────────────┐
│  Frontend Build │
└────────┬────────┘
         │
    ┌────┴────┬──────────────┬──────────────┐
    │         │              │              │
┌───▼───┐ ┌──▼──────┐ ┌──────▼──────┐ ┌───▼──────┐
│ Unit  │ │Integrat│ │    E2E       │ │ Security │
│ Tests │ │ion Test│ │   Tests      │ │  Scan    │
└───┬───┘ └──┬──────┘ └──────┬──────┘ └───┬──────┘
    │        │              │              │
    └────────┴──────────────┴──────────────┘
                    │
            ┌───────▼────────┐
            │ Docker Build   │
            └───────┬────────┘
                    │
            ┌───────▼────────┐
            │   Deploy       │
            └───────┬────────┘
                    │
            ┌───────▼────────┐
            │  Notifications │
            └────────────────┘
```

## Job Dependencies

### Frontend Pipeline
- `frontend-build` → `frontend-test-unit`, `frontend-test-integration`, `frontend-test-e2e`
- All frontend tests → `docker-build-frontend`

### Backend Pipeline
- `backend-build` → `backend-test-unit`, `backend-test-integration`, `backend-test-api`
- `backend-build` → `backend-lint`
- All backend tests → `docker-build-backend`

### Security Pipeline
- All security scans run in parallel (no dependencies)

### Deployment Pipeline
- Staging: Requires frontend/backend builds, tests, and Docker builds
- Production: Requires all tests, security scans, performance tests, and Docker builds

## Usage

### Automatic Triggers

- **Push to `main`**: Full pipeline → Production deployment
- **Push to `develop`**: Full pipeline → Staging deployment
- **Pull Request**: Tests and security scans only (no deployment)

### Manual Trigger

```yaml
workflow_dispatch:
  inputs:
    environment: staging | production
    skip_tests: true | false
```

### Skip Tests (Use with Caution)

```bash
# Via GitHub UI: Set skip_tests to true
# Or via GitHub CLI:
gh workflow run ci-cd-unified.yml -f skip_tests=true -f environment=staging
```

## Required Secrets

### Docker
- `DOCKER_USERNAME` - Docker Hub username
- `DOCKER_PASSWORD` - Docker Hub password or token

### Deployment - Staging
- `STAGING_HOST` - Staging server hostname/IP
- `STAGING_USER` - SSH username
- `STAGING_SSH_KEY` - SSH private key
- `STAGING_URL` - Staging URL (optional)

### Deployment - Production
- `PRODUCTION_HOST` - Production server hostname/IP
- `PRODUCTION_USER` - SSH username
- `PRODUCTION_SSH_KEY` - SSH private key
- `PRODUCTION_URL` - Production URL (optional)

### Security
- `SNYK_TOKEN` - Snyk API token (optional)
- `SLACK_WEBHOOK_URL` - Slack webhook URL (optional)

### Application
- `VITE_API_URL` - Frontend API URL (optional, defaults to localhost:5001)

## Performance Metrics

### Expected Execution Times

- **Frontend Build**: ~5-8 minutes (with cache), ~10 minutes (without cache)
- **Frontend Tests**: ~10-15 minutes (parallel execution)
- **Backend Build**: ~3-5 minutes (with cache), ~8 minutes (without cache)
- **Backend Tests**: ~15-20 minutes (parallel execution)
- **Security Scans**: ~10-15 minutes (parallel execution)
- **Docker Builds**: ~5-8 minutes (with cache), ~12 minutes (without cache)
- **Deployment**: ~5-10 minutes

### Total Pipeline Time

- **Full Pipeline (with cache)**: ~25-35 minutes
- **Full Pipeline (without cache)**: ~45-60 minutes
- **PR Pipeline (tests only)**: ~20-25 minutes

## Optimization Tips

1. **Enable Caching**: Ensure cache keys are stable and don't change unnecessarily
2. **Parallel Execution**: Tests run in parallel to reduce total time
3. **Conditional Execution**: Use `if` conditions to skip unnecessary jobs
4. **Artifact Retention**: Adjust retention days based on storage needs
5. **Timeout Settings**: Adjust timeouts based on actual execution times

## Troubleshooting

### Cache Issues
- Clear caches if builds are failing unexpectedly
- Check cache key stability
- Verify cache paths are correct

### Test Failures
- Check test artifacts for detailed error messages
- Review coverage reports for test gaps
- Verify test dependencies are installed

### Deployment Failures
- Check deployment logs
- Verify secrets are set correctly
- Review smoke test results
- Check health monitoring logs

### Security Scan Failures
- Review security reports in artifacts
- Check for false positives
- Update dependencies if vulnerabilities found

## Migration from Old Pipelines

The old pipelines have been archived in `.github/workflows/archived/`:
- `basic-ci-cd.yml` → Archived
- `ci-cd-optimized.yml` → `archived/ci-cd-optimized.yml.backup`
- `ci-cd-ultra-optimized.yml` → `archived/ci-cd-ultra-optimized.yml.backup`

To restore an old pipeline, copy it back to `.github/workflows/` and rename it.

## Best Practices

1. **Always test locally** before pushing
2. **Review security reports** regularly
3. **Monitor deployment health** after each deployment
4. **Keep dependencies updated** to avoid security vulnerabilities
5. **Use feature flags** for gradual rollouts
6. **Monitor pipeline performance** and optimize slow jobs
7. **Keep secrets secure** and rotate them regularly

## Support

For issues or questions:
1. Check workflow logs in GitHub Actions
2. Review artifact reports
3. Check security scan results
4. Review deployment logs
