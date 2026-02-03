# Complete Vercel Deployment Guide

This guide provides step-by-step instructions for deploying your React + Vite frontend to Vercel.

## 📋 Prerequisites

- GitHub account
- Vercel account (free tier available)
- Backend API deployed (Railway, Render, or other platform)
- Node.js 20.x installed locally (for testing)

## 🚀 Step-by-Step Deployment

### Step 1: Prepare Your Repository

Your repository is already configured with:
- ✅ `vercel.json` - Vercel configuration file
- ✅ `vite.config.ts` - Updated to support environment variables
- ✅ `src/services/api.ts` - Updated to use `VITE_API_URL` environment variable
- ✅ Build scripts in `package.json`

### Step 2: Sign Up for Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click **"Sign Up"**
3. Choose **"Continue with GitHub"**
4. Authorize Vercel to access your GitHub account

### Step 3: Import Your Project

1. In Vercel dashboard, click **"Add New Project"**
2. Find your repository in the list (or search for it)
3. Click **"Import"** next to your repository

### Step 4: Configure Project Settings

Vercel will auto-detect your Vite project. Verify these settings:

**Framework Preset:** `Vite` (auto-detected)

**Root Directory:** `./` (leave as default)

**Build and Output Settings:**
- **Build Command:** `npm run build` (auto-detected)
- **Output Directory:** `dist` (auto-detected)
- **Install Command:** `npm install` (auto-detected)

**Environment Variables:**
Click **"Environment Variables"** and add:

```
VITE_API_URL=https://your-backend-url.com/api
```

**Important:** Replace `your-backend-url.com` with your actual backend URL:
- If using Railway: `https://your-app-name.railway.app/api`
- If using Render: `https://your-app-name.onrender.com/api`
- If using other platform: `https://your-backend-domain.com/api`

### Step 5: Deploy

1. Click **"Deploy"** button
2. Wait for the build to complete (usually 1-3 minutes)
3. Once deployed, you'll get a URL like: `https://your-project-name.vercel.app`

### Step 6: Configure Backend CORS

Your Flask backend needs to allow requests from your Vercel domain.

#### Option A: Update Environment Variables (Recommended)

In your backend deployment (Railway/Render/etc.), add environment variable:

```
CORS_ORIGINS=https://your-project-name.vercel.app,https://your-project-name.vercel.app/*
```

Or for multiple environments:
```
CORS_ORIGINS=https://your-project-name.vercel.app,https://your-project-name-git-main.vercel.app,http://localhost:5173
```

#### Option B: Update Flask Config Directly

If you need to update the Flask config file directly, edit `flask_api/config.py`:

```python
# In ProductionConfig class
CORS_ORIGINS = [
    'https://your-project-name.vercel.app',
    'https://your-project-name-git-main.vercel.app',  # Preview deployments
    'http://localhost:5173'  # Local development
]
```

### Step 7: Test Your Deployment

1. Visit your Vercel URL: `https://your-project-name.vercel.app`
2. Test the following:
   - ✅ Page loads correctly
   - ✅ API calls work (check browser console)
   - ✅ Authentication works (login/register)
   - ✅ No CORS errors in console
   - ✅ All routes work (SPA routing)

## 🔄 Automatic Deployments

Vercel automatically deploys:

- **Production:** Every push to `main` branch
- **Preview:** Every push to other branches
- **Preview:** Every pull request

### Branch Deployments

- **Main branch** → Production deployment (`your-project.vercel.app`)
- **Other branches** → Preview deployments (`your-project-git-branch-name.vercel.app`)

## 🔧 Environment Variables

### Required Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `VITE_API_URL` | Backend API URL | `https://api.example.com/api` |

### Setting Environment Variables

1. Go to **Project Settings** → **Environment Variables**
2. Add variables for:
   - **Production** (main branch)
   - **Preview** (all other branches)
   - **Development** (local development)

### Environment Variable Format

For Vite, environment variables must start with `VITE_`:
- ✅ `VITE_API_URL` - Works
- ❌ `API_URL` - Won't work (not exposed to client)

## 📁 Project Structure

Your project structure is optimized for Vercel:

```
your-project/
├── vercel.json          # Vercel configuration
├── vite.config.ts       # Vite configuration
├── package.json         # Build scripts
├── index.html          # Entry HTML
├── src/
│   ├── services/
│   │   └── api.ts      # API service (uses VITE_API_URL)
│   └── ...
└── dist/               # Build output (generated)
```

## 🐛 Troubleshooting

### Build Fails

**Error:** `Build failed`

**Solutions:**
1. Check build logs in Vercel dashboard
2. Ensure all dependencies are in `package.json`
3. Verify Node.js version (should be 20.x)
4. Check for TypeScript errors: `npm run build` locally

### API Calls Fail

**Error:** `Failed to fetch` or CORS errors

**Solutions:**
1. Verify `VITE_API_URL` is set correctly in Vercel
2. Check backend CORS configuration includes your Vercel domain
3. Ensure backend is running and accessible
4. Check browser console for specific error messages

### 404 Errors on Routes

**Error:** Page shows 404 when navigating

**Solutions:**
1. Verify `vercel.json` has rewrites configured (already done)
2. Ensure all routes use React Router correctly
3. Check that `index.html` is in the root of `dist/`

### Environment Variables Not Working

**Error:** `VITE_API_URL` is undefined

**Solutions:**
1. Ensure variable name starts with `VITE_`
2. Rebuild after adding environment variables
3. Check variable is set for correct environment (Production/Preview)
4. Restart deployment after adding variables

### Build Takes Too Long

**Solutions:**
1. Check `package.json` for unnecessary dependencies
2. Use Vercel's build cache (automatic)
3. Optimize build process if needed
4. Check for large files in repository

## 🔐 Security Best Practices

### Environment Variables

- ✅ Never commit `.env` files to Git
- ✅ Use Vercel's environment variables for secrets
- ✅ Use different API URLs for production/preview

### CORS Configuration

- ✅ Only allow specific domains (not `*`)
- ✅ Include preview deployment URLs
- ✅ Test CORS in production environment

### Headers

Your `vercel.json` includes security headers:
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: SAMEORIGIN`
- `X-XSS-Protection: 1; mode=block`
- `Referrer-Policy: strict-origin-when-cross-origin`

## 📊 Monitoring & Analytics

### Vercel Analytics (Optional)

1. Go to **Project Settings** → **Analytics**
2. Enable **Web Analytics** (free tier available)
3. View traffic, performance metrics, and user behavior

### Performance Monitoring

Vercel automatically provides:
- Build logs
- Function logs
- Performance metrics
- Error tracking

## 🔄 Updating Your Deployment

### Automatic Updates

- Push to `main` → Auto-deploys to production
- Push to other branch → Creates preview deployment
- Create PR → Creates preview deployment

### Manual Deployment

1. Go to **Deployments** tab
2. Click **"Redeploy"** on any deployment
3. Or trigger via GitHub push

### Rollback

1. Go to **Deployments** tab
2. Find previous successful deployment
3. Click **"..."** → **"Promote to Production"**

## 📝 Custom Domain (Optional)

### Adding Custom Domain

1. Go to **Project Settings** → **Domains**
2. Add your domain: `app.yourdomain.com`
3. Follow DNS configuration instructions
4. Vercel automatically provisions SSL certificate

### DNS Configuration

Add CNAME record:
```
Type: CNAME
Name: app (or @ for root domain)
Value: cname.vercel-dns.com
```

## 🎯 Next Steps

After successful deployment:

1. ✅ Test all features in production
2. ✅ Set up monitoring/analytics
3. ✅ Configure custom domain (optional)
4. ✅ Set up CI/CD for backend (if not done)
5. ✅ Document API endpoints for team
6. ✅ Set up error tracking (Sentry, etc.)

## 📚 Additional Resources

- [Vercel Documentation](https://vercel.com/docs)
- [Vite Deployment Guide](https://vitejs.dev/guide/static-deploy.html#vercel)
- [React Router Deployment](https://reactrouter.com/en/main/start/overview#deployment)
- [Environment Variables Guide](https://vercel.com/docs/concepts/projects/environment-variables)

## 🆘 Getting Help

If you encounter issues:

1. Check Vercel build logs
2. Check browser console for errors
3. Verify backend is running and accessible
4. Test API endpoints directly (Postman/curl)
5. Check Vercel status page: status.vercel.com
6. Review Vercel documentation
7. Check GitHub Issues for similar problems

## ✅ Deployment Checklist

Before deploying, ensure:

- [ ] Code is pushed to GitHub
- [ ] `vercel.json` is in repository root
- [ ] `VITE_API_URL` environment variable is set
- [ ] Backend is deployed and accessible
- [ ] Backend CORS allows Vercel domain
- [ ] Build works locally: `npm run build`
- [ ] All tests pass: `npm run test`
- [ ] No console errors in development

## 🎉 Success!

Once deployed, you'll have:
- ✅ Production URL: `https://your-project.vercel.app`
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ Automatic deployments
- ✅ Preview deployments for PRs
- ✅ Build logs and analytics

Your application is now live! 🚀
