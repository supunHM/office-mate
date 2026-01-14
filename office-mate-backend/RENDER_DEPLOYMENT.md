# Office Mate Backend - Render Deployment Guide

## 🚀 Deploy to Render

Follow these steps to deploy the Office Mate backend to Render.

### Prerequisites

- GitHub account with the office-mate repository
- Render account (free tier available at https://render.com)

### Step 1: Prepare Your Repository

Your repository already has:

- ✅ `flask_requirements.txt` - Python dependencies
- ✅ `gunicorn_config.py` - Production server configuration
- ✅ `flask_app.py` - Main application (updated for production)
- ✅ `.env.example` - Environment variable template

### Step 2: Create a New Web Service on Render

1. **Go to Render Dashboard**

   - Visit https://dashboard.render.com
   - Click "New +" → "Web Service"

2. **Connect Your Repository**

   - Select "Connect a repository"
   - Choose your GitHub account
   - Select the `office-mate` repository
   - Click "Connect"

3. **Configure the Web Service**

   **Basic Settings:**

   - **Name**: `office-mate-backend` (or your preferred name)
   - **Region**: Choose closest to your users
   - **Branch**: `main`
   - **Root Directory**: `office-mate-backend`
   - **Runtime**: `Python 3`

   **Build & Deploy:**

   - **Build Command**:

     ```bash
     pip install -r flask_requirements.txt
     ```

   - **Start Command**:
     ```bash
     gunicorn -c gunicorn_config.py flask_app:app
     ```

   **Instance Type:**

   - Select **Free** (or paid plan if needed)

### Step 3: Set Environment Variables

Click "Advanced" → "Add Environment Variable" and add:

| Key               | Value                                | Notes                                  |
| ----------------- | ------------------------------------ | -------------------------------------- |
| `DATABASE_URL`    | (Use Render PostgreSQL - see Step 4) | Database connection string             |
| `SECRET_KEY`      | `<generate-random-32-char-string>`   | **IMPORTANT**: Use a strong random key |
| `CORS_ORIGINS`    | `https://your-frontend.vercel.app`   | Update with your Vercel URL            |
| `MAX_UPLOAD_SIZE` | `10485760`                           | 10MB in bytes                          |
| `FLASK_ENV`       | `production`                         | Disables debug mode                    |
| `PYTHON_VERSION`  | `3.11.0`                             | Optional: specify Python version       |

**Generate a secure SECRET_KEY:**

```bash
python -c "import secrets; print(secrets.token_hex(32))"
```

### Step 4: Add PostgreSQL Database (Recommended for Production)

1. In Render Dashboard, click "New +" → "PostgreSQL"
2. **Name**: `office-mate-db`
3. **Database**: `officemate`
4. **User**: (auto-generated)
5. **Region**: Same as your web service
6. **Plan**: Free
7. Click "Create Database"

8. **Connect to Web Service:**
   - Go back to your web service
   - In Environment Variables, update `DATABASE_URL`:
   - Copy the "Internal Database URL" from your PostgreSQL dashboard
   - Paste it as the value for `DATABASE_URL`

### Step 5: Deploy

1. Click "Create Web Service"
2. Render will:
   - Clone your repository
   - Install dependencies
   - Start the server
3. Wait for deployment (usually 2-5 minutes)
4. Your backend will be live at: `https://office-mate-backend.onrender.com`

### Step 6: Verify Deployment

Test your API:

```bash
curl https://your-backend-url.onrender.com/
```

Expected response:

```json
{
  "status": "ok",
  "message": "Office Mate API is running"
}
```

### Step 7: Update Frontend

Update your Vercel frontend environment variable:

- Variable: `VITE_API_URL`
- Value: `https://your-backend-url.onrender.com`

---

## 📝 Important Notes

### Free Tier Limitations

- Your service will spin down after 15 minutes of inactivity
- First request after spin-down may take 30-60 seconds (cold start)
- 750 hours/month of free runtime

### Database Migrations

If you update your database models:

```bash
# SSH into Render or use Render Shell
python init_db.py
```

### Logs

- View logs in Render Dashboard → Your Service → Logs
- Real-time log streaming available

### Custom Domain

- Go to Settings → Custom Domain
- Add your domain (e.g., `api.yourdomain.com`)
- Update DNS records as shown

---

## 🔧 Troubleshooting

### Build Fails

- Check `flask_requirements.txt` syntax
- Ensure all dependencies are compatible
- View build logs in Render dashboard

### Service Won't Start

- Check environment variables are set correctly
- Review start command: `gunicorn -c gunicorn_config.py flask_app:app`
- Check logs for Python errors

### Database Connection Issues

- Verify `DATABASE_URL` is correct
- Check database is in the same region
- Ensure PostgreSQL database is running

### CORS Errors

- Update `CORS_ORIGINS` with your actual frontend URL
- Include `https://` in the URL
- Multiple origins: comma-separated

---

## 🎯 Next Steps

1. ✅ Deploy backend to Render
2. ✅ Test API endpoints
3. ✅ Deploy frontend to Vercel (separate guide)
4. ✅ Update frontend to use Render backend URL
5. ✅ Test full application flow

---

## 📞 Support

If you encounter issues:

- Check Render documentation: https://render.com/docs
- Review logs in Render dashboard
- Ensure all environment variables are set correctly
