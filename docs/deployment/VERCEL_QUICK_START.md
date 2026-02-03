# Vercel Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Step 1: Push to GitHub
```bash
git add .
git commit -m "Add Vercel configuration"
git push origin main
```

### Step 2: Deploy to Vercel

1. Go to [vercel.com](https://vercel.com) and sign in with GitHub
2. Click **"Add New Project"**
3. Import your repository
4. Add environment variable:
   ```
   VITE_API_URL=https://your-backend-url.com/api
   ```
5. Click **"Deploy"**

### Step 3: Update Backend CORS

In your backend deployment (Railway/Render), add:
```
CORS_ORIGINS=https://your-project-name.vercel.app
```

### Step 4: Test

Visit your Vercel URL and test the application!

## 📝 Files Created

- ✅ `vercel.json` - Vercel configuration
- ✅ `VERCEL_DEPLOYMENT_GUIDE.md` - Complete guide
- ✅ `.env.example` - Environment variable template

## 🔗 Next Steps

See `VERCEL_DEPLOYMENT_GUIDE.md` for detailed instructions.
