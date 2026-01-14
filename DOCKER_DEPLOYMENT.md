# Office Mate - Docker Deployment Guide

## 🐳 Docker Deployment Options

### Option 1: Local Development with Docker Compose

Run the entire stack (backend + frontend + database) locally:

```bash
# From the project root directory
docker-compose up --build
```

**Services will be available at:**

- Frontend: http://localhost:5173
- Backend API: http://localhost:5001
- PostgreSQL: localhost:5432

**Stop services:**

```bash
docker-compose down
```

**Stop and remove volumes (fresh start):**

```bash
docker-compose down -v
```

---

## Option 2: Deploy Backend to Render with Docker

Render supports Docker deployments, which ensures consistency between development and production.

### Step 1: Prepare Your Repository

Your repository now has:

- ✅ `office-mate-backend/Dockerfile`
- ✅ `office-mate-backend/.dockerignore`
- ✅ `docker-compose.yml` (for local dev)

### Step 2: Create Web Service on Render

1. **Go to Render Dashboard**

   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect Repository**

   - Select your `office-mate` repository
   - Click "Connect"

3. **Configure Service**

   **Basic Settings:**

   - **Name**: `office-mate-backend`
   - **Region**: Choose closest region
   - **Branch**: `main`
   - **Root Directory**: `office-mate-backend`
   - **Environment**: `Docker`

   **Docker Settings:**

   - Render auto-detects `Dockerfile`
   - **Dockerfile Path**: `Dockerfile` (default)

   **Instance Type:**

   - Free or Starter

### Step 3: Environment Variables

Add these in Render dashboard:

| Variable          | Value                         | Required                  |
| ----------------- | ----------------------------- | ------------------------- |
| `PORT`            | `10000`                       | ✅ (Render default)       |
| `DATABASE_URL`    | `postgresql://...`            | ✅ From Render PostgreSQL |
| `SECRET_KEY`      | `<random-64-char-hex>`        | ✅                        |
| `CORS_ORIGINS`    | `https://your-app.vercel.app` | ✅                        |
| `FLASK_ENV`       | `production`                  | ✅                        |
| `MAX_UPLOAD_SIZE` | `10485760`                    | Optional                  |

**Generate SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Add PostgreSQL Database

1. **Create Database:**

   - New + → PostgreSQL
   - Name: `office-mate-db`
   - Region: Same as web service
   - Plan: Free

2. **Connect to Web Service:**
   - Copy "Internal Database URL"
   - Add as `DATABASE_URL` environment variable in your web service

### Step 5: Deploy

Click "Create Web Service" - Render will:

1. Pull your repository
2. Build Docker image
3. Start container
4. Your API will be live at `https://office-mate-backend.onrender.com`

### Step 6: Verify

```bash
curl https://your-backend-url.onrender.com/
```

Expected:

```json
{ "status": "ok", "message": "Office Mate API is running" }
```

---

## Option 3: Deploy to Other Platforms

### Docker Hub + Any Cloud Platform

1. **Build and push to Docker Hub:**

```bash
cd office-mate-backend

# Build image
docker build -t yourusername/office-mate-backend:latest .

# Push to Docker Hub
docker push yourusername/office-mate-backend:latest
```

2. **Deploy to:**
   - **Railway**: Import from Docker Hub
   - **Fly.io**: `fly deploy` with Dockerfile
   - **DigitalOcean App Platform**: Connect repository
   - **AWS ECS/Fargate**: Use Docker image

---

## 🔧 Docker Commands Reference

### Backend Only

**Build:**

```bash
cd office-mate-backend
docker build -t office-mate-backend .
```

**Run:**

```bash
docker run -p 5001:10000 \
  -e DATABASE_URL=sqlite:///./data/office_mate.db \
  -e SECRET_KEY=your-secret-key \
  -e CORS_ORIGINS=http://localhost:5173 \
  office-mate-backend
```

**Run with environment file:**

```bash
docker run -p 5001:10000 --env-file .env office-mate-backend
```

### Frontend Only

**Build:**

```bash
cd office-mate
docker build -t office-mate-frontend .
```

**Run:**

```bash
docker run -p 5173:80 office-mate-frontend
```

---

## 🎯 Advantages of Docker Deployment

✅ **Consistency**: Same environment in dev, staging, and production
✅ **Isolation**: All dependencies bundled in the container
✅ **Portability**: Deploy anywhere that supports Docker
✅ **Scalability**: Easy to scale with container orchestration
✅ **Reproducibility**: Exact same build every time

---

## 🐛 Troubleshooting

### Build fails on Render

- Check Dockerfile syntax
- Ensure all dependencies in `flask_requirements.txt`
- View build logs in Render dashboard

### Container exits immediately

- Check logs: `docker logs <container-id>`
- Verify environment variables are set
- Ensure PORT is correct (10000 in Dockerfile)

### Database connection fails

- Verify `DATABASE_URL` format
- Check database is running
- Ensure database and backend are in same region (Render)

### CORS errors

- Update `CORS_ORIGINS` with exact frontend URL
- Include `https://` prefix
- Check for trailing slashes

---

## 📊 Resource Requirements

**Render Free Tier:**

- 512 MB RAM
- 0.1 CPU
- Shared infrastructure
- Spins down after 15 min inactivity

**Recommended for Production:**

- Starter: 512 MB RAM, $7/month
- Standard: 2 GB RAM, $25/month

---

## 🚀 Next Steps

1. Test locally with `docker-compose up`
2. Push code to GitHub
3. Deploy backend to Render (Docker)
4. Deploy frontend to Vercel
5. Update frontend `VITE_API_URL` to Render backend URL
6. Test full application

---

## 📝 Environment Files

**For local Docker development (.env):**

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/officemate
SECRET_KEY=local-dev-secret-key
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
FLASK_ENV=development
PORT=10000
```

**For production on Render:**
Set via Render Dashboard (not in .env file)
