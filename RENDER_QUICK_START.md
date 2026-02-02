# Render.com Quick Start Guide

## 🚀 Deploy in 5 Minutes

### Step 1: Prepare Your Repository

```bash
# Add Render configuration
git add render.yaml
git commit -m "Add Render.com deployment configuration"
git push origin main
```

### Step 2: Create Blueprint on Render

1. Visit [dashboard.render.com](https://dashboard.render.com)
2. Click **"New +"** → **"Blueprint"**
3. Connect your Git repository
4. Select repository → Click **"Apply"**

Render will automatically:
- ✅ Create Flask API service
- ✅ Create React frontend static site
- ✅ Create PostgreSQL database
- ✅ Create Redis cache
- ✅ Link all services together

### Step 3: Configure Environment Variables

#### Backend (flask-api service):
1. Go to **flask-api** → **Environment**
2. Set `CORS_ORIGINS`:
   ```
   https://react-frontend.onrender.com
   ```

#### Frontend (react-frontend service):
1. Go to **react-frontend** → **Environment**
2. Set `VITE_API_URL`:
   ```
   https://flask-api.onrender.com/api
   ```
   (Use the actual URL from your flask-api service)

### Step 4: Run Database Migrations

1. Go to **flask-api** → **Shell**
2. Run:
   ```bash
   cd flask_api
   python -m flask db upgrade
   ```

### Step 5: Test Your Deployment

- **Backend API:** `https://flask-api.onrender.com/api`
- **Frontend:** `https://react-frontend.onrender.com`

## 📋 Checklist

- [ ] Code pushed to Git repository
- [ ] Blueprint created on Render
- [ ] All services deployed successfully
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] API endpoints tested
- [ ] Frontend connects to backend
- [ ] CORS configured correctly

## 🔧 Troubleshooting

**Services won't start?**
- Check **Logs** tab for errors
- Verify environment variables are set
- Ensure database is running

**Database connection errors?**
- Verify `DATABASE_URL` is set
- Check database service status
- Run migrations in Shell

**CORS errors?**
- Update `CORS_ORIGINS` with exact frontend URL
- Include `https://` prefix
- No trailing slashes

## 📚 Full Documentation

See [RENDER_DEPLOYMENT_GUIDE.md](./RENDER_DEPLOYMENT_GUIDE.md) for detailed instructions.

## 💰 Cost

**Free Tier:**
- Perfect for development/testing
- Services sleep after 15 min inactivity
- 90MB PostgreSQL, 25MB Redis

**Starter Plan (~$21/month):**
- Always-on services
- Better for small production apps

## 🆘 Need Help?

- [Render Docs](https://render.com/docs)
- [Render Community](https://community.render.com)
- Check service **Logs** for error messages
