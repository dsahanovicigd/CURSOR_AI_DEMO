# Render.com Deployment Guide

This guide will help you deploy both the Flask API backend and React frontend to Render.com.

## Prerequisites

1. A [Render.com account](https://render.com) (free tier available)
2. Your code pushed to a Git repository (GitHub, GitLab, or Bitbucket)
3. Basic understanding of environment variables

## Architecture Overview

The deployment consists of 4 services:
1. **Flask API** - Python web service (backend)
2. **React Frontend** - Static site (frontend)
3. **PostgreSQL** - Database
4. **Redis** - Cache and Celery broker

## Quick Start (Using render.yaml)

### Step 1: Push to Git Repository

```bash
git add render.yaml
git commit -m "Add Render.com configuration"
git push origin main
```

### Step 2: Create Blueprint on Render

1. Go to [Render Dashboard](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your Git repository
4. Select the repository containing `render.yaml`
5. Click **"Apply"**

Render will automatically create all services defined in `render.yaml`.

### Step 3: Configure Environment Variables

After services are created, you need to set some environment variables:

#### For Flask API Service:

1. Go to your **flask-api** service
2. Navigate to **Environment** tab
3. Set `CORS_ORIGINS`:
   ```
   https://react-frontend.onrender.com,https://your-custom-domain.com
   ```
   (Replace with your actual frontend URL)

#### For React Frontend Service:

1. Go to your **react-frontend** service
2. Navigate to **Environment** tab
3. Set `VITE_API_URL`:
   ```
   https://flask-api.onrender.com/api
   ```
   (Replace with your actual backend URL)

### Step 4: Run Database Migrations

After the Flask API service is deployed:

1. Go to your **flask-api** service
2. Click **"Shell"** tab
3. Run:
   ```bash
   cd flask_api
   python -m flask db upgrade
   ```

### Step 5: Create Admin User (Optional)

In the Shell tab:
```bash
cd flask_api
python create_admin_user.py
```

## Manual Setup (Without Blueprint)

If you prefer to set up services manually:

### 1. Create PostgreSQL Database

1. Go to **Dashboard** → **New +** → **PostgreSQL**
2. Name: `postgres-db`
3. Plan: **Starter** (free tier)
4. Region: Choose closest to your users
5. Click **Create Database**
6. **Save the connection string** - you'll need it later

### 2. Create Redis Instance

1. Go to **Dashboard** → **New +** → **Redis**
2. Name: `redis-cache`
3. Plan: **Starter** (free tier)
4. Region: Same as database
5. Click **Create Redis**
6. **Save the connection string**

### 3. Create Flask API Web Service

1. Go to **Dashboard** → **New +** → **Web Service**
2. Connect your Git repository
3. Configure:
   - **Name:** `flask-api`
   - **Environment:** `Python 3`
   - **Region:** Same as database
   - **Branch:** `main` (or your default branch)
   - **Root Directory:** `flask_api`
   - **Build Command:**
     ```bash
     pip install --upgrade pip && pip install -r requirements.txt && python -m flask db upgrade || true
     ```
   - **Start Command:**
     ```bash
     gunicorn --bind 0.0.0.0:$PORT --workers 4 --threads 2 --timeout 120 --access-logfile - --error-logfile - run:app
     ```
4. Add Environment Variables:
   - `FLASK_ENV` = `production`
   - `FLASK_APP` = `app:create_app`
   - `PYTHON_VERSION` = `3.11.0`
   - `DATABASE_URL` = (from PostgreSQL service)
   - `REDIS_URL` = (from Redis service)
   - `CELERY_BROKER_URL` = (from Redis service)
   - `CELERY_RESULT_BACKEND` = (from Redis service)
   - `SECRET_KEY` = (generate a random string)
   - `JWT_SECRET_KEY` = (generate a random string)
   - `CORS_ORIGINS` = `https://react-frontend.onrender.com` (update after frontend deploy)
5. Click **Create Web Service**

### 4. Create React Frontend Static Site

1. Go to **Dashboard** → **New +** → **Static Site**
2. Connect your Git repository
3. Configure:
   - **Name:** `react-frontend`
   - **Branch:** `main`
   - **Root Directory:** `.` (root)
   - **Build Command:** `npm install && npm run build`
   - **Publish Directory:** `dist`
4. Add Environment Variable:
   - `VITE_API_URL` = `https://flask-api.onrender.com/api` (update with your backend URL)
5. Click **Create Static Site**

## Environment Variables Reference

### Flask API Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `FLASK_ENV` | Flask environment | `production` |
| `FLASK_APP` | Flask app entry point | `app:create_app` |
| `DATABASE_URL` | PostgreSQL connection string | Auto-set from database service |
| `REDIS_URL` | Redis connection string | Auto-set from Redis service |
| `SECRET_KEY` | Flask secret key | Generate random string |
| `JWT_SECRET_KEY` | JWT signing key | Generate random string |
| `CORS_ORIGINS` | Allowed CORS origins | `https://react-frontend.onrender.com` |

### Flask API Optional Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `CELERY_BROKER_URL` | Celery broker URL | Uses `REDIS_URL` |
| `CELERY_RESULT_BACKEND` | Celery result backend | Uses `REDIS_URL` |
| `LIMITER_STORAGE_URI` | Rate limiter storage | `memory://` |

### React Frontend Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://flask-api.onrender.com/api` |

## Generating Secret Keys

You can generate secure random keys using:

```bash
# Python
python -c "import secrets; print(secrets.token_urlsafe(32))"

# OpenSSL
openssl rand -hex 32

# Node.js
node -e "console.log(require('crypto').randomBytes(32).toString('hex'))"
```

## Database Migrations

After first deployment, run migrations:

1. Go to **flask-api** service → **Shell** tab
2. Run:
   ```bash
   cd flask_api
   python -m flask db upgrade
   ```

## Custom Domains

### For Flask API:

1. Go to **flask-api** service → **Settings** → **Custom Domains**
2. Add your domain (e.g., `api.yourdomain.com`)
3. Follow DNS configuration instructions
4. Update `CORS_ORIGINS` to include your custom domain

### For React Frontend:

1. Go to **react-frontend** service → **Settings** → **Custom Domains**
2. Add your domain (e.g., `yourdomain.com`)
3. Follow DNS configuration instructions
4. Update `VITE_API_URL` if using custom backend domain

## Monitoring & Logs

- **Logs:** Available in each service's **Logs** tab
- **Metrics:** View in service dashboard (CPU, Memory, Requests)
- **Alerts:** Configure in **Settings** → **Alerts**

## Troubleshooting

### Flask API Won't Start

1. Check **Logs** tab for errors
2. Verify all environment variables are set
3. Ensure database is accessible
4. Check `DATABASE_URL` format is correct

### Database Connection Errors

1. Verify `DATABASE_URL` is set correctly
2. Check database service is running
3. Ensure database name/user match
4. Check firewall/network settings

### CORS Errors

1. Verify `CORS_ORIGINS` includes your frontend URL
2. Check for trailing slashes
3. Ensure URLs match exactly (including `https://`)

### Frontend Can't Connect to API

1. Verify `VITE_API_URL` is set correctly
2. Ensure backend service is running
3. Check CORS settings on backend
4. Verify API endpoints are accessible

### Build Failures

1. Check **Logs** for specific error messages
2. Verify all dependencies are in `requirements.txt` (backend) or `package.json` (frontend)
3. Check Python/Node version compatibility
4. Review build command syntax

## Scaling

### Free Tier Limitations

- **Web Services:** Sleep after 15 minutes of inactivity
- **PostgreSQL:** 90MB storage limit
- **Redis:** 25MB memory limit

### Upgrading Plans

1. Go to service → **Settings** → **Plan**
2. Select higher tier (Starter, Standard, Pro)
3. Services restart automatically

### Horizontal Scaling

For production, consider:
- Using **Standard** or **Pro** plans
- Enabling **Auto-scaling** in service settings
- Using **Load Balancer** for multiple instances

## Cost Estimation

### Free Tier (Development)
- Web Service: Free (with limitations)
- PostgreSQL: Free (90MB)
- Redis: Free (25MB)
- Static Site: Free
- **Total: $0/month**

### Starter Plan (Small Production)
- Web Service: $7/month
- PostgreSQL: $7/month
- Redis: $7/month
- Static Site: Free
- **Total: ~$21/month**

### Standard Plan (Medium Production)
- Web Service: $25/month
- PostgreSQL: $20/month
- Redis: $15/month
- Static Site: Free
- **Total: ~$60/month**

## Security Best Practices

1. **Never commit secrets** - Use environment variables
2. **Use HTTPS** - Render provides SSL certificates automatically
3. **Rotate keys regularly** - Update `SECRET_KEY` and `JWT_SECRET_KEY` periodically
4. **Enable rate limiting** - Already configured in Flask app
5. **Monitor logs** - Check for suspicious activity
6. **Keep dependencies updated** - Regularly update `requirements.txt` and `package.json`

## CI/CD Integration

Render automatically deploys on:
- Push to main branch
- Manual deploy trigger
- Scheduled deploys (Pro plan)

You can also integrate with GitHub Actions for additional CI/CD workflows.

## Support

- **Render Docs:** https://render.com/docs
- **Render Community:** https://community.render.com
- **Support:** support@render.com

## Next Steps

1. ✅ Deploy services using `render.yaml`
2. ✅ Configure environment variables
3. ✅ Run database migrations
4. ✅ Test API endpoints
5. ✅ Verify frontend connects to backend
6. ✅ Set up custom domains (optional)
7. ✅ Configure monitoring and alerts
8. ✅ Set up backups for database
