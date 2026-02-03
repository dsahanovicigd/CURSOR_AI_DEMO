# GitHub Actions CI/CD Setup Guide

This guide explains how to set up and use the GitHub Actions workflows for this full-stack application.

## Overview

The repository includes comprehensive CI/CD workflows that automate:
- ✅ Building React frontend
- ✅ Testing frontend with Playwright
- ✅ Building Flask backend
- ✅ Testing backend with pytest
- ✅ Security scanning
- ✅ Deployment to staging and production

## Workflows

### 1. Main CI/CD Pipeline (`ci-cd.yml`)

**Triggers:**
- Push to `main` branch → Full test + Production deployment
- Push to `develop` branch → Full test + Staging deployment
- Pull requests → Tests only (no deployment)
- Manual workflow dispatch

**Jobs:**
1. **Frontend Build & Test** - Builds React app and runs Playwright tests
2. **Backend Lint** - Code quality checks
3. **Backend Test** - Runs pytest with coverage
4. **Backend Integration Test** - Runs comprehensive API tests
5. **Security Scan** - Vulnerability scanning with Trivy
6. **Deploy Staging** - Deploys to staging environment
7. **Deploy Production** - Deploys to production environment
8. **Notify** - Sends status notifications

### 2. Docker Build & Push (`docker-build.yml`)

**Triggers:**
- Push to `main` or `develop` branches
- Version tags (v*)
- Manual workflow dispatch

**Jobs:**
1. **Build Frontend Docker Image** - Builds and pushes frontend container
2. **Build Backend Docker Image** - Builds and pushes backend container

## Initial Setup

### Step 1: Enable GitHub Actions

1. Go to your repository on GitHub
2. Click **Settings** → **Actions** → **General**
3. Enable "Allow all actions and reusable workflows"
4. Save changes

### Step 2: Configure Secrets

Go to **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

#### Required Secrets:

**Staging Environment:**
```
STAGING_HOST=staging.example.com
STAGING_USER=deploy
STAGING_SSH_KEY=<your-ssh-private-key>
```

**Production Environment:**
```
PRODUCTION_HOST=example.com
PRODUCTION_USER=deploy
PRODUCTION_SSH_KEY=<your-ssh-private-key>
AWS_ACCESS_KEY_ID=<aws-key>  # If using AWS
AWS_SECRET_ACCESS_KEY=<aws-secret>  # If using AWS
```

**Application Secrets:**
```
VITE_API_URL=https://api.example.com  # Optional
SECRET_KEY=<flask-secret-key>
JWT_SECRET_KEY=<jwt-secret-key>
DATABASE_URL=postgresql://user:pass@host:5432/dbname
```

**Optional Notification Secrets:**
```
SLACK_WEBHOOK=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
EMAIL_USERNAME=your-email@gmail.com
EMAIL_PASSWORD=your-app-password
```

### Step 3: Configure Environments

1. Go to **Settings** → **Environments**
2. Create `staging` environment
3. Create `production` environment
4. Add environment-specific secrets
5. (Optional) Add protection rules:
   - Required reviewers for production
   - Deployment branches restriction

### Step 4: Set Up Branch Protection

1. Go to **Settings** → **Branches**
2. Add rule for `main` branch:
   - ✅ Require pull request reviews
   - ✅ Require status checks to pass
   - ✅ Require branches to be up to date
   - ✅ Select required checks:
     - Frontend Build & Test
     - Backend Tests
     - Security Scan

## Customization

### Deployment Methods

The workflow includes placeholder deployment steps. Choose and customize based on your infrastructure:

#### Option A: SSH Deployment

```yaml
- name: Deploy via SSH
  uses: appleboy/ssh-action@master
  with:
    host: ${{ secrets.STAGING_HOST }}
    username: ${{ secrets.STAGING_USER }}
    key: ${{ secrets.STAGING_SSH_KEY }}
    script: |
      cd /var/www/app
      git pull origin develop
      npm install
      npm run build
      sudo systemctl restart app
```

#### Option B: Docker Deployment

```yaml
- name: Deploy Docker containers
  run: |
    docker-compose -f docker-compose.prod.yml pull
    docker-compose -f docker-compose.prod.yml up -d
```

#### Option C: Cloud Platform Deployment

**AWS Elastic Beanstalk:**
```yaml
- name: Deploy to AWS EB
  run: |
    pip install awsebcli
    eb init -p python-3.11 myapp --region us-east-1
    eb deploy production
```

**Google Cloud Run:**
```yaml
- name: Deploy to Cloud Run
  uses: google-github-actions/deploy-cloudrun@v1
  with:
    service: myapp
    image: gcr.io/${{ secrets.GCP_PROJECT }}/myapp:${{ github.sha }}
```

**Azure App Service:**
```yaml
- name: Deploy to Azure
  uses: azure/webapps-deploy@v2
  with:
    app-name: myapp
    publish-profile: ${{ secrets.AZURE_PUBLISH_PROFILE }}
```

#### Option D: Kubernetes Deployment

```yaml
- name: Deploy to Kubernetes
  uses: azure/k8s-deploy@v4
  with:
    manifests: |
      k8s/deployment.yaml
      k8s/service.yaml
    images: |
      myapp:${{ github.sha }}
```

### Notification Setup

#### Slack Notification

Add to `notify` job:
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    text: |
      Workflow: ${{ github.workflow }}
      Status: ${{ job.status }}
      Commit: ${{ github.sha }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

#### Email Notification

Add to `notify` job:
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: "Deployment Status: ${{ job.status }}"
    to: team@example.com
    body: |
      Workflow: ${{ github.workflow }}
      Status: ${{ job.status }}
      Commit: ${{ github.sha }}
```

## Testing Workflows Locally

### Using Act (GitHub Actions Local Runner)

```bash
# Install act
brew install act  # macOS
# or download from https://github.com/nektos/act/releases

# List workflows
act -l

# Run specific job
act -j frontend-build

# Run with secrets
act -j backend-test --secret-file .secrets

# Run specific workflow
act -W .github/workflows/ci-cd.yml
```

### Using Docker Compose

Test deployment locally:
```bash
docker-compose -f docker-compose.test.yml up --build
```

## Monitoring

### View Workflow Runs

1. Go to **Actions** tab in GitHub
2. Click on a workflow run
3. View logs for each job
4. Download artifacts (builds, reports, etc.)

### Workflow Status Badge

Add to README.md:
```markdown
![CI/CD](https://github.com/username/repo/workflows/CI/CD%20Pipeline/badge.svg)
```

## Troubleshooting

### Common Issues

**1. Tests failing**
- Check test logs in Actions tab
- Run tests locally to reproduce
- Check environment variables

**2. Deployment failing**
- Verify secrets are set correctly
- Check SSH keys have correct permissions
- Verify server access

**3. Build artifacts missing**
- Ensure upload-artifact runs before download
- Check artifact retention settings

**4. Coverage not uploading**
- Verify Codecov token is set
- Check coverage.xml file exists

**5. Docker build failing**
- Check Dockerfile syntax
- Verify build context paths
- Check registry permissions

### Debug Mode

Enable debug logging:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

Or add to workflow:
```yaml
- name: Debug
  run: |
    echo "::debug::GitHub Event: ${{ toJson(github.event) }}"
    echo "::debug::Secrets: ${{ toJson(secrets) }}"
```

## Best Practices

1. ✅ **Use matrix builds** for multiple versions
2. ✅ **Cache dependencies** to speed up builds
3. ✅ **Run tests in parallel** when possible
4. ✅ **Use environment protection** for production
5. ✅ **Set up branch protection** for main branch
6. ✅ **Monitor workflow performance** and optimize
7. ✅ **Keep secrets secure** and rotate regularly
8. ✅ **Use deployment approvals** for production
9. ✅ **Add status badges** to README
10. ✅ **Document deployment process**

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
- [GitHub Actions Best Practices](https://docs.github.com/en/actions/learn-github-actions/best-practices)

## Support

For issues or questions:
1. Check workflow logs in Actions tab
2. Review this documentation
3. Check GitHub Actions documentation
4. Open an issue in the repository
