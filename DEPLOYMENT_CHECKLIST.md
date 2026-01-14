# 🚀 Deployment Checklist - Office Mate

## Pre-Deployment ✅

### Backend

- ✅ Flask app created and configured
- ✅ Database models defined (User, Document, Task, Tag)
- ✅ All API endpoints implemented
- ✅ Authentication system working
- ✅ CORS configured
- ✅ Environment variables set
- ✅ Docker support added
- ✅ Gunicorn configured
- ✅ Requirements.txt updated
- ✅ .env file fixed
- ✅ Tests created and verified

### Frontend

- ✅ React + Vite setup
- ✅ Environment variable configured
- ✅ API integration ready
- ✅ Docker support added
- ✅ Nginx configuration created
- ✅ Production build configured

---

## Step 1: Deploy Backend to Render 🔴

### 1a. Prepare Repository

```bash
# Ensure all changes are committed
git add .
git commit -m "Backend ready for deployment"
git push origin main
```

**Files to ensure are committed:**

- ✅ office-mate-backend/Dockerfile
- ✅ office-mate-backend/gunicorn_config.py
- ✅ office-mate-backend/flask_requirements.txt (with all packages)
- ✅ office-mate-backend/.env (with correct config)
- ✅ office-mate-backend/flask_app.py (updated for production)
- ✅ RENDER_DEPLOYMENT.md
- ✅ DOCKER_DEPLOYMENT.md

### 1b. Create Render Web Service

1. Go to: https://dashboard.render.com
2. Click: **New +** → **Web Service**
3. Select: Your `office-mate` repository
4. Configure:
   - **Name:** `office-mate-backend`
   - **Region:** Choose closest to users
   - **Branch:** `main`
   - **Root Directory:** `office-mate-backend`
   - **Environment:** Select **Docker**
   - **Instance Type:** Free or Starter

### 1c. Set Environment Variables

In Render Dashboard, go to **Environment** and add:

```
DATABASE_URL = postgresql://user:password@hostname/dbname
SECRET_KEY = <GENERATE_RANDOM_32_HEX>
FLASK_ENV = production
CORS_ORIGINS = https://office-mate-frontend.vercel.app
MAX_UPLOAD_SIZE = 10485760
```

**To generate SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### 1d. Create PostgreSQL Database

1. In Render Dashboard: **New +** → **PostgreSQL**
2. Configure:
   - **Name:** `office-mate-db`
   - **Database:** `officemate`
   - **Region:** Same as web service
   - **Plan:** Free tier
3. Create and copy the **Internal Database URL**
4. Paste as `DATABASE_URL` in web service environment

### 1e. Deploy

1. Click: **Create Web Service**
2. Render will:
   - Clone repository
   - Build Docker image
   - Start container
   - Run health checks
3. Wait for deployment (2-5 minutes)
4. Get your backend URL: `https://office-mate-backend.onrender.com`

### 1f. Verify Backend

```bash
curl https://office-mate-backend.onrender.com/
# Should return: {"status": "ok", "message": "Office Mate API is running"}
```

---

## Step 2: Deploy Frontend to Vercel 🟦

### 2a. Build Frontend

```bash
cd office-mate
bun install
bun run build
# Creates: dist/ folder with optimized build
```

### 2b. Create Vercel Project

1. Go to: https://vercel.com/new
2. Import: Your `office-mate` repository
3. Configure:
   - **Project Name:** `office-mate-frontend` (or `office-mate`)
   - **Framework:** Vite
   - **Root Directory:** `office-mate`
   - **Build Command:** `bun run build`
   - **Output Directory:** `dist`

### 2c. Set Environment Variables

In Vercel, add **Environment Variables:**

```
VITE_API_URL = https://office-mate-backend.onrender.com
```

**Important:** Update the URL after backend is deployed!

### 2d. Deploy

1. Click: **Deploy**
2. Vercel will:
   - Build the React app
   - Deploy to CDN
   - Setup SSL certificate
3. Get your frontend URL: `https://office-mate.vercel.app`

### 2e. Verify Frontend

Visit: `https://office-mate.vercel.app`

- Should load without errors
- Check browser console for errors
- Try to login/register

---

## Step 3: Test Full Application 🧪

### Test Checklist

- [ ] Frontend loads at `https://office-mate.vercel.app`
- [ ] Backend health check: `https://office-mate-backend.onrender.com/`
- [ ] User Registration works
- [ ] User Login works
- [ ] Document upload functions
- [ ] Document search works
- [ ] Task creation works
- [ ] Task list displays
- [ ] No CORS errors in console
- [ ] No 404 API errors

### Test Account

```
Username: testuser
Email: test@example.com
Password: testpass123
```

---

## Step 4: Post-Deployment Monitoring 📊

### Render Dashboard

- Monitor backend logs
- Check error rates
- Watch resource usage
- Monitor database connection

### Vercel Dashboard

- Monitor frontend build status
- Check deployment logs
- Monitor performance metrics
- Check error tracking

### Manual Checks

- Test API endpoints regularly
- Check document uploads work
- Verify search functionality
- Test task management
- Monitor database size

---

## Troubleshooting Guide 🔧

### Backend Won't Start

**Error:** `ModuleNotFoundError`

- **Solution:** Check `flask_requirements.txt` is correct
- **Solution:** Ensure all packages installed

**Error:** `Database connection failed`

- **Solution:** Verify `DATABASE_URL` is correct
- **Solution:** Check PostgreSQL is running
- **Solution:** Verify database exists

**Error:** `CORS error in frontend`

- **Solution:** Update `CORS_ORIGINS` in environment
- **Solution:** Include full URL with `https://`

### Frontend Won't Load

**Error:** `API not responding`

- **Solution:** Check backend is deployed
- **Solution:** Verify `VITE_API_URL` is correct
- **Solution:** Check CORS headers in response

**Error:** `Build failing`

- **Solution:** Check `package.json` scripts
- **Solution:** Verify all dependencies installed
- **Solution:** Check Vite config

### Database Issues

**Error:** `relation "users" does not exist`

- **Solution:** Run migrations
- **Solution:** Manually create tables via Flask shell

**Error:** `Connection pooling error`

- **Solution:** Increase max connections
- **Solution:** Monitor and optimize queries

---

## Rollback Procedure 🔄

If something goes wrong:

### Render Backend

1. Go to your service on Render
2. Click: **Logs**
3. Review error messages
4. Click: **Manual Deploy** to redeploy
5. Or rollback to previous commit

### Vercel Frontend

1. Go to **Deployments**
2. Find the last working version
3. Click: **Redeploy**
4. Or: Push new commit to redeploy

### Database

- PostgreSQL backups available in Render
- Download and restore if needed

---

## Maintenance Tasks 🛠️

### Weekly

- [ ] Check error logs
- [ ] Monitor database size
- [ ] Test core functionality
- [ ] Review resource usage

### Monthly

- [ ] Analyze performance metrics
- [ ] Update dependencies
- [ ] Security audit
- [ ] Database optimization

### As Needed

- [ ] Add new features
- [ ] Fix bugs
- [ ] Optimize slow queries
- [ ] Scale resources

---

## Success Criteria ✅

### Backend

- ✅ Deploys without errors
- ✅ Health check returns 200
- ✅ Database connected
- ✅ API endpoints responding
- ✅ Authentication working

### Frontend

- ✅ Builds without errors
- ✅ Loads in browser
- ✅ No console errors
- ✅ API integration working
- ✅ Forms submitting

### Integration

- ✅ Frontend → Backend communication
- ✅ User registration working
- ✅ Document uploads functional
- ✅ Search results returning
- ✅ Task management operational

---

## Deployment Summary

| Component | URL                                        | Status    |
| --------- | ------------------------------------------ | --------- |
| Backend   | `https://office-mate-backend.onrender.com` | To Deploy |
| Frontend  | `https://office-mate.vercel.app`           | To Deploy |
| Database  | Render PostgreSQL                          | To Create |
| Auth      | JWT-based                                  | Ready     |

---

## Quick Reference

### Backend Render URL

```
https://office-mate-backend.onrender.com/
```

### Frontend Vercel URL

```
https://office-mate.vercel.app
```

### API Documentation

- File: `API_ROUTES.md`
- Location: `office-mate-backend/API_ROUTES.md`

### Deployment Guides

- Docker: `DOCKER_DEPLOYMENT.md`
- Render (Traditional): `RENDER_DEPLOYMENT.md`
- This Checklist: `DEPLOYMENT_CHECKLIST.md`

---

## Important Notes

1. **Save SECRET_KEY somewhere safe** - You won't be able to see it again
2. **Database URL should use Internal URL** for Render-to-Render communication
3. **Frontend CORS_ORIGINS must match** the actual Vercel URL
4. **Free tier spins down** after 15 minutes of inactivity
5. **First request after spin-down** may take 30-60 seconds

---

**Ready to deploy? Let's go! 🚀**

Follow the steps above in order for successful deployment.

For questions, refer to:

- `RENDER_DEPLOYMENT.md` - Detailed Render instructions
- `DOCKER_DEPLOYMENT.md` - Docker deployment options
- `TEST_REPORT.md` - Test results and verification

---

**Estimated Deployment Time:** 15-30 minutes
**Difficulty Level:** Intermediate
**Support:** Check logs in Render/Vercel dashboards
