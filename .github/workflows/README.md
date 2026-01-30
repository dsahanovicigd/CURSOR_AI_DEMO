# GitHub Actions Workflows

This directory contains GitHub Actions workflows for CI/CD automation.

## Workflows

### `ci-cd.yml` - Main CI/CD Pipeline

Comprehensive workflow for building, testing, and deploying the full-stack application.

#### Stages:

1. **Frontend Build & Test**
   - Installs Node.js dependencies
   - Runs linter
   - Builds React frontend
   - Runs Playwright tests
   - Uploads build artifacts

2. **Backend Build & Test**
   - Installs Python dependencies
   - Runs code linting (flake8, black)
   - Runs pytest with coverage
   - Runs comprehensive API tests
   - Uploads coverage reports

3. **Security Scan**
   - Runs Trivy vulnerability scanner
   - Uploads security findings to GitHub Security

4. **Deployment**
   - **Staging**: Deploys on `develop` branch
   - **Production**: Deploys on `main` branch (push events)

5. **Notifications**
   - Sends status notifications after workflow completion

## Setup

### Required GitHub Secrets

Add these secrets in your GitHub repository settings:

#### Staging Environment:
- `STAGING_HOST` - Staging server hostname/IP
- `STAGING_USER` - SSH username for staging
- `STAGING_SSH_KEY` - SSH private key for staging

#### Production Environment:
- `PRODUCTION_HOST` - Production server hostname/IP
- `PRODUCTION_USER` - SSH username for production
- `PRODUCTION_SSH_KEY` - SSH private key for production
- `AWS_ACCESS_KEY_ID` - AWS access key (if using AWS)
- `AWS_SECRET_ACCESS_KEY` - AWS secret key (if using AWS)

#### Application Secrets:
- `VITE_API_URL` - Frontend API URL (optional, defaults to localhost)
- `SECRET_KEY` - Flask secret key
- `JWT_SECRET_KEY` - JWT secret key
- `DATABASE_URL` - Database connection string

### Environment Variables

The workflow uses environment variables defined in the workflow file:
- `NODE_VERSION`: '20.x'
- `PYTHON_VERSION`: '3.11'
- `FLASK_APP`: 'app:create_app'

## Usage

### Automatic Triggers

- **Push to `main`**: Runs all tests and deploys to production
- **Push to `develop`**: Runs all tests and deploys to staging
- **Pull Request**: Runs tests only (no deployment)

### Manual Trigger

You can manually trigger the workflow:
1. Go to Actions tab in GitHub
2. Select "CI/CD Pipeline"
3. Click "Run workflow"
4. Choose environment (staging/production)
5. Click "Run workflow"

## Customization

### Deployment Methods

The workflow includes placeholder deployment steps. Customize based on your infrastructure:

#### Option 1: SSH Deployment
```yaml
- name: Deploy via SSH
  run: |
    ssh -i ${{ secrets.SSH_KEY }} user@host 'cd /app && git pull && ./deploy.sh'
```

#### Option 2: Docker Deployment
```yaml
- name: Build and push Docker images
  run: |
    docker build -t myapp:latest .
    docker push myapp:latest
```

#### Option 3: Cloud Platform Deployment
```yaml
# AWS Elastic Beanstalk
- name: Deploy to AWS EB
  run: |
    eb deploy production

# Google Cloud Run
- name: Deploy to Cloud Run
  run: |
    gcloud run deploy myapp --source .

# Azure App Service
- name: Deploy to Azure
  run: |
    az webapp up --name myapp --resource-group mygroup
```

#### Option 4: Kubernetes Deployment
```yaml
- name: Deploy to Kubernetes
  run: |
    kubectl apply -f k8s/
    kubectl rollout status deployment/myapp
```

### Notification Setup

Add notification steps in the `notify` job:

#### Slack Notification
```yaml
- name: Notify Slack
  uses: 8398a7/action-slack@v3
  with:
    status: ${{ job.status }}
    webhook_url: ${{ secrets.SLACK_WEBHOOK }}
```

#### Email Notification
```yaml
- name: Send Email
  uses: dawidd6/action-send-mail@v3
  with:
    server_address: smtp.gmail.com
    server_port: 465
    username: ${{ secrets.EMAIL_USERNAME }}
    password: ${{ secrets.EMAIL_PASSWORD }}
    subject: Deployment Status
    to: team@example.com
```

## Testing Locally

You can test workflow steps locally using [act](https://github.com/nektos/act):

```bash
# Install act
brew install act  # macOS
# or
curl https://raw.githubusercontent.com/nektos/act/master/install.sh | sudo bash

# Run workflow locally
act -j frontend-build
act -j backend-test
```

## Troubleshooting

### Common Issues

1. **Tests failing**: Check test logs in Actions tab
2. **Deployment failing**: Verify secrets are set correctly
3. **Build artifacts missing**: Ensure upload-artifact steps run before download
4. **Coverage reports not uploading**: Check Codecov token is set

### Debug Mode

Enable debug logging by adding:
```yaml
env:
  ACTIONS_STEP_DEBUG: true
  ACTIONS_RUNNER_DEBUG: true
```

## Best Practices

1. **Use matrix builds** for multiple Python/Node versions
2. **Cache dependencies** to speed up builds
3. **Run tests in parallel** when possible
4. **Use environment protection rules** for production
5. **Set up branch protection** for main branch
6. **Monitor workflow performance** and optimize slow steps
7. **Keep secrets secure** and rotate regularly
8. **Use deployment approvals** for production

## Additional Resources

- [GitHub Actions Documentation](https://docs.github.com/en/actions)
- [GitHub Actions Marketplace](https://github.com/marketplace?type=actions)
- [Workflow Syntax Reference](https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions)
