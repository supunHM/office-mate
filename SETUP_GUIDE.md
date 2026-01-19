# Office Mate - Complete Setup Guide

## 📋 Table of Contents
1. [Prerequisites](#prerequisites)
2. [Initial Setup](#initial-setup)
3. [Backend Setup (Flask)](#backend-setup-flask)
4. [Frontend Setup (React)](#frontend-setup-react)
5. [Running the Application](#running-the-application)
6. [Testing the Application](#testing-the-application)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

Before starting, ensure you have the following installed on your machine:

### Required Software

1. **Python 3.8 or higher**
   ```bash
   # Check Python version
   python3 --version
   # Should show: Python 3.8.x or higher
   ```

2. **Node.js 16 or higher** (includes npm)
   ```bash
   # Check Node.js version
   node --version
   # Should show: v16.x.x or higher
   
   # Check npm version
   npm --version
   # Should show: 8.x.x or higher
   ```

3. **Git** (for cloning the repository)
   ```bash
   # Check Git version
   git --version
   # Should show: git version 2.x.x
   ```

4. **Package Manager**
   
   **macOS - Homebrew** (for Tesseract OCR)
   ```bash
   # Check if Homebrew is installed
   brew --version
   # If not installed, visit: https://brew.sh
   ```
   
   **Windows - Chocolatey** (optional, for easier software installation)
   ```powershell
   # Check if Chocolatey is installed
   choco --version
   # If not installed, visit: https://chocolatey.org/install
   # Or install manually from official websites
   ```

---

## Initial Setup

### Step 1: Clone the Repository (if not already done)

```bash
# Navigate to your projects directory
cd ~/Documents

# Clone the repository (if applicable)
# git clone <repository-url>
# cd office-mate

# Or navigate to existing project
cd Dev-Pro
```

### Step 2: Project Structure

Your project should have this structure:
```
Dev-Pro/
├── office-mate/                # Frontend (React + TypeScript)
├── office-mate-backend/        # Backend (Flask + Python)
└── .venv/                      # Python virtual environment (will be created)
```

**Note for Windows users:** Use backslashes in paths when needed:
- Example: `C:\Users\YourName\Documents\Dev-Pro`

---

## Backend Setup (Flask)

### Step 1: Create Python Virtual Environment

```bash
# Navigate to project root
cd /Users/supunherath/Documents/Dev-Pro

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
# macOS/Linux:
source .venv/bin/activate

# Windows (Command Prompt):
# .venv\Scripts\activate.bat

# Windows (PowerShell):
# .venv\Scripts\Activate.ps1
# Note: You may need to enable script execution first:
# Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Your terminal prompt should now show (.venv)
```

### Step 2: Install Backend Dependencies

```bash
# Navigate to backend directory
cd office-mate-backend

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# If requirements.txt doesn't exist, install manually:
pip install flask flask-cors flask-sqlalchemy flask-jwt-extended bcrypt
pip install pytesseract python-docx pypdf2 pillow
pip install scikit-learn spacy joblib
pip install python-dateutil

# Install spaCy English model (required for NLP)
python -m spacy download en_core_web_sm
```

### Step 3: Install Tesseract OCR

#### macOS
```bash
brew install tesseract

# Verify installation
tesseract --version
# Should show: tesseract 5.x.x
```

#### Linux (Ubuntu/Debian)
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr

# Verify installation
tesseract --version
```

#### Windows

**Option 1: Using Chocolatey (Recommended)**
```powershell
# Install with Chocolatey
choco install tesseract

# Verify installation
tesseract --version
```

**Option 2: Manual Installation**
1. Download the installer from: https://github.com/UB-Mannheim/tesseract/wiki
2. Download the latest version (e.g., `tesseract-ocr-w64-setup-5.3.x.exe`)
3. Run the installer and follow the wizard
4. **Important:** Note the installation path (typically `C:\Program Files\Tesseract-OCR`)
5. Add Tesseract to your PATH:
   - Open "Environment Variables" from System Properties
   - Under "System variables", find and edit "Path"
   - Add: `C:\Program Files\Tesseract-OCR`
   - Click OK to save
6. **Restart your terminal** for PATH changes to take effect

**Verify Installation:**
```powershell
# Should work after adding to PATH
tesseract --version

# If not found, you may need to set TESSDATA_PREFIX environment variable:
# setx TESSDATA_PREFIX "C:\Program Files\Tesseract-OCR\tessdata"
```

### Step 4: Initialize Database

```bash
# Still in office-mate-backend directory
# The database will be created automatically when you first run the app

# (Optional) Create initial admin user
python -c "
from flask import Flask
from flask_models import db, User
import bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///office_mate.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

with app.app_context():
    db.create_all()
    
    # Create admin user if not exists
    if not User.query.filter_by(username='admin').first():
        hashed = bcrypt.hashpw('admin123'.encode('utf-8'), bcrypt.gensalt())
        admin = User(
            username='admin',
            email='admin@gmail.com',
            password_hash=hashed.decode('utf-8'),
            full_name='Admin User'
        )
        db.session.add(admin)
        db.session.commit()
        print('Admin user created!')
    else:
        print('Admin user already exists')
"
```

### Step 5: Train ML Classifier (First Time Only)

```bash
# Still in office-mate-backend directory
python train_flask_classifier.py

# Expected output:
# Training classifier...
# Classifier saved to models_store/classifier.joblib
# Classifier accuracy: 0.95 (or similar)
```

### Step 6: Verify Backend Setup

```bash
# Check if all required files exist
ls flask_app.py
ls flask_auth.py
ls flask_documents_api.py
ls flask_tasks_api.py
ls flask_models.py

# Check if database exists
ls office_mate.db

# Check if ML model exists
ls models_store/classifier.joblib
```

---

## Frontend Setup (React)

### Step 1: Install Node Modules

```bash
# Navigate to frontend directory
cd /Users/supunherath/Documents/Dev-Pro/office-mate

# Install all npm dependencies
npm install

# This will install:
# - React, React Router, React Query
# - TypeScript and Vite
# - Tailwind CSS
# - Shadcn UI components
# - Axios for API calls
# - date-fns for date handling
# - And all other dependencies from package.json
```

**Expected output:**
```
added 500+ packages in 30s
```

### Step 2: Create Environment File (Optional)

```bash
# Still in office-mate directory
# Create .env file for environment variables

cat > .env << 'EOF'
# API Configuration
VITE_API_URL=http://localhost:5001

# App Configuration
VITE_APP_NAME=Office Mate
EOF
```

### Step 3: Verify Frontend Setup

```bash
# Check if node_modules folder exists
ls node_modules

# Check if key configuration files exist
ls package.json
ls vite.config.ts
ls tailwind.config.ts
ls tsconfig.json
```

---

## Running the Application

### Method 1: Run Both Servers Separately (Recommended)

#### Terminal 1: Start Backend Server

```bash
# Open first terminal
cd /Users/supunherath/Documents/Dev-Pro

# Activate virtual environment
source .venv/bin/activate

# Navigate to backend
cd office-mate-backend

# Start Flask server
python flask_app.py
```

**Expected output:**
```
 * Serving Flask app 'flask_app'
 * Debug mode: on
 * Running on http://127.0.0.1:5001
 * Running on http://192.168.x.x:5001
Press CTRL+C to quit
```

#### Terminal 2: Start Frontend Server

```bash
# Open second terminal
cd /Users/supunherath/Documents/Dev-Pro/office-mate

# Start React development server
npm run dev
```

**Expected output:**
```
VITE v5.4.19  ready in 500 ms

➜  Local:   http://localhost:8081/
➜  Network: http://192.168.x.x:8081/
```

### Method 2: Use Background Process (Alternative)

#### Start Backend in Background

```bash
cd /Users/supunherath/Documents/Dev-Pro
source .venv/bin/activate
cd office-mate-backend

# Start in background
nohup python flask_app.py > flask.log 2>&1 &

# Save the process ID
echo $! > flask.pid

# View logs
tail -f flask.log
```

#### Start Frontend in Background

```bash
cd /Users/supunherath/Documents/Dev-Pro/office-mate

# Start in background
nohup npm run dev > vite.log 2>&1 &

# Save the process ID
echo $! > vite.pid

# View logs
tail -f vite.log
```

#### Stop Background Processes

```bash
# Stop Flask
kill $(cat office-mate-backend/flask.pid)

# Stop Vite
kill $(cat office-mate/vite.pid)

# Or kill by port
lsof -ti:5001 | xargs kill -9  # Flask
lsof -ti:8081 | xargs kill -9  # Vite
```

---

## Testing the Application

### Step 1: Access the Application

1. **Open your browser**
2. **Navigate to:** http://localhost:8081
3. **You should see the Office Mate login page**

### Step 2: Login

Use the default admin credentials:
- **Email/Username:** `admin@gmail.com`
- **Password:** `admin123`

### Step 3: Test Document Upload

1. Click on **"Documents"** in the navigation
2. Click **"Upload Document"** button
3. Select a file (PDF, DOCX, or Image)
4. Wait for processing
5. Verify:
   - Document appears in the list
   - Category is automatically assigned
   - Tags are extracted
   - Text extraction details are shown

### Step 4: Test Task Management

1. Click on **"Tasks"** in the navigation
2. Click **"Add Task"** button
3. Fill in:
   - **Title:** "Test Task"
   - **Description:** "This is a test"
   - **Priority:** Select one
   - **Due Date:** Select a date
   - **Linked Document:** Select a document (optional)
4. Click **"Save"**
5. Verify task appears in the appropriate section

### Step 5: Test Dashboard

1. Click on **"Dashboard"** in the navigation
2. Verify you see:
   - Total documents count
   - Open tasks count
   - Upcoming deadlines
   - Document categories breakdown
   - Recent documents
   - High priority tasks

### Step 6: Run Backend Tests (Optional)

```bash
# Terminal 1: Make sure Flask server is running
cd /Users/supunherath/Documents/Dev-Pro/office-mate-backend
source ../.venv/bin/activate
python flask_app.py

# Terminal 2: Run tests
cd /Users/supunherath/Documents/Dev-Pro/office-mate-backend
source ../.venv/bin/activate
python test_task_api_complete.py
```

**Expected output:**
```
ℹ Logging in...
✓ Login successful
ℹ Testing Task Creation
✓ Task created successfully!
ℹ Testing Get All Tasks
✓ Retrieved X tasks
...
✓ All Tests Completed!
```

### Step 7: API Health Check

```bash
# Test Flask API
curl http://localhost:5001/
# Expected: {"status": "ok", "message": "Office Mate API is running"}

# Test authentication
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin@gmail.com","password":"admin123"}'
# Expected: {"access_token": "...", "user": {...}}
```

---

## Troubleshooting

### Backend Issues

#### Issue: `ModuleNotFoundError: No module named 'flask'`

**Solution:**
```bash
# Make sure virtual environment is activated
source .venv/bin/activate

# Reinstall dependencies
pip install -r office-mate-backend/requirements.txt
```

#### Issue: `OSError: [E050] Can't find model 'en_core_web_sm'`

**Solution:**
```bash
# Download spaCy model
python -m spacy download en_core_web_sm

# Verify installation
python -c "import spacy; nlp = spacy.load('en_core_web_sm'); print('Model loaded successfully!')"
```

#### Issue: `FileNotFoundError: [Errno 2] No such file or directory: 'tesseract'`

**Solution:**
```bash
# macOS
brew install tesseract

# Linux
sudo apt-get install tesseract-ocr

# Verify installation
which tesseract
tesseract --version
```

#### Issue: Port 5001 already in use

**Solution:**
```bash
# Find process using port 5001
lsof -ti:5001

# Kill the process
lsof -ti:5001 | xargs kill -9

# Or change port in flask_app.py
# Change: app.run(debug=True, host='0.0.0.0', port=5001)
# To:     app.run(debug=True, host='0.0.0.0', port=5002)
```

#### Issue: Database errors

**Solution:**
```bash
# Delete and recreate database
cd office-mate-backend
rm office_mate.db

# Restart Flask (will auto-create database)
python flask_app.py
```

### Frontend Issues

#### Issue: `Cannot find module` or `Module not found`

**Solution:**
```bash
# Delete node_modules and reinstall
cd office-mate
rm -rf node_modules package-lock.json
npm install
```

#### Issue: Port 8081 already in use

**Solution:**
```bash
# Find and kill process using port 8081
lsof -ti:8081 | xargs kill -9

# Or use different port
# Edit vite.config.ts:
# server: { port: 8082 }
```

#### Issue: Vite cache issues

**Solution:**
```bash
# Clear Vite cache
cd office-mate
rm -rf node_modules/.vite
npm run dev
```

#### Issue: `CORS` errors in browser console

**Solution:**
```bash
# Verify Flask CORS configuration in flask_app.py includes:
# CORS(app, origins=['http://localhost:8081'], supports_credentials=True)

# Restart Flask server after changes
```

### General Issues

#### Issue: `EACCES: permission denied` (macOS/Linux)

**Solution:**
```bash
# Fix npm permissions
sudo chown -R $USER:$(id -gn $USER) ~/.npm
sudo chown -R $USER:$(id -gn $USER) office-mate/node_modules

# Or use sudo (not recommended)
sudo npm install
```

#### Issue: Python virtual environment not activating

**Solution (macOS/Linux):**
```bash
# Recreate virtual environment
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate

# Reinstall dependencies
pip install -r office-mate-backend/requirements.txt
```

**Solution (Windows PowerShell):**
```powershell
# Recreate virtual environment
Remove-Item -Recurse -Force .venv
python -m venv .venv
.venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.venv\Scripts\Activate.ps1

# Reinstall dependencies
pip install -r office-mate-backend\requirements.txt
```

### Windows-Specific Issues

#### Issue: PowerShell script execution disabled

**Solution:**
```powershell
# Allow running scripts for current user
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating virtual environment again
.venv\Scripts\Activate.ps1
```

#### Issue: `python3` or `pip3` not recognized on Windows

**Solution:**
```powershell
# Use 'python' and 'pip' instead of 'python3' and 'pip3'
python --version
pip --version

# Create virtual environment
python -m venv .venv
```

#### Issue: Long path issues on Windows

**Solution:**
```powershell
# Enable long paths in Windows 10/11
# Run PowerShell as Administrator:
New-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Control\FileSystem" -Name "LongPathsEnabled" -Value 1 -PropertyType DWORD -Force

# Or manually enable via Group Policy:
# 1. Press Win+R, type 'gpedit.msc'
# 2. Navigate to: Local Computer Policy > Computer Configuration > Administrative Templates > System > Filesystem
# 3. Enable "Enable Win32 long paths"
```

#### Issue: Tesseract not found after installation

**Solution:**
```powershell
# Add Tesseract to PATH manually
# 1. Open System Properties > Environment Variables
# 2. Edit PATH, add: C:\Program Files\Tesseract-OCR
# 3. Restart terminal

# Or set for current session:
$env:Path += ";C:\Program Files\Tesseract-OCR"

# Verify:
tesseract --version
```

---

## Quick Reference Commands

### Start Development

**macOS/Linux:**
```bash
# Terminal 1 - Backend
cd /Users/supunherath/Documents/Dev-Pro
source .venv/bin/activate
cd office-mate-backend
python flask_app.py

# Terminal 2 - Frontend
cd /Users/supunherath/Documents/Dev-Pro/office-mate
npm run dev
```

**Windows (PowerShell):**
```powershell
# Terminal 1 - Backend
cd C:\Users\YourName\Documents\Dev-Pro
.venv\Scripts\Activate.ps1
cd office-mate-backend
python flask_app.py

# Terminal 2 - Frontend
cd C:\Users\YourName\Documents\Dev-Pro\office-mate
npm run dev
```

**Windows (Command Prompt):**
```cmd
REM Terminal 1 - Backend
cd C:\Users\YourName\Documents\Dev-Pro
.venv\Scripts\activate.bat
cd office-mate-backend
python flask_app.py

REM Terminal 2 - Frontend
cd C:\Users\YourName\Documents\Dev-Pro\office-mate
npm run dev
```

### Stop Development

```bash
# Press CTRL+C in both terminals
```

**Kill processes by port if needed:**

**macOS/Linux:**
```bash
lsof -ti:5001 | xargs kill -9  # Backend
lsof -ti:8081 | xargs kill -9  # Frontend
```

**Windows (PowerShell):**
```powershell
# Find and kill process on port 5001 (Backend)
Get-NetTCPConnection -LocalPort 5001 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }

# Find and kill process on port 8081 (Frontend)
Get-NetTCPConnection -LocalPort 8081 | Select-Object -ExpandProperty OwningProcess | ForEach-Object { Stop-Process -Id $_ -Force }
```

**Windows (Command Prompt):**
```cmd
REM Find process using port 5001
netstat -ano | findstr :5001
REM Kill process (replace PID with actual process ID from above)
taskkill /PID <PID> /F

REM Find process using port 8081
netstat -ano | findstr :8081
REM Kill process
taskkill /PID <PID> /F
```

### Reinstall Everything

**macOS/Linux:**
```bash
# Backend
cd /Users/supunherath/Documents/Dev-Pro
rm -rf .venv
python3 -m venv .venv
source .venv/bin/activate
pip install -r office-mate-backend/requirements.txt
python -m spacy download en_core_web_sm

# Frontend
cd office-mate
rm -rf node_modules package-lock.json
npm install
```

**Windows (PowerShell):**
```powershell
# Backend
cd C:\Users\YourName\Documents\Dev-Pro
Remove-Item -Recurse -Force .venv
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r office-mate-backend\requirements.txt
python -m spacy download en_core_web_sm

# Frontend
cd office-mate
Remove-Item -Recurse -Force node_modules, package-lock.json
npm install
```

### Reset Database

```bash
cd /Users/supunherath/Documents/Dev-Pro/office-mate-backend
rm office_mate.db
python flask_app.py  # Will auto-create
```

### Check Running Processes

```bash
# Check if backend is running
curl http://localhost:5001/

# Check if frontend is running
curl http://localhost:8081/

# List all processes on ports
lsof -i :5001
lsof -i :8081
```

---

## Production Deployment

### Environment Variables

Create `.env` file in backend:
```bash
cd office-mate-backend
cat > .env << 'EOF'
SECRET_KEY=your-production-secret-key-change-this
DATABASE_URI=postgresql://user:pass@host:5432/office_mate
FLASK_ENV=production
PORT=5001
EOF
```

### Build Frontend for Production

```bash
cd office-mate
npm run build

# Output will be in dist/ folder
# Serve with nginx or any static file server
```

### Run Backend in Production

```bash
# Use gunicorn (install first)
pip install gunicorn

# Run with gunicorn
gunicorn -w 4 -b 0.0.0.0:5001 flask_app:app
```

---

## Additional Resources

- **Task Section Documentation:** [TASK_SECTION_FIX_SUMMARY.md](./TASK_SECTION_FIX_SUMMARY.md)
- **Quick Start Guide:** [TASK_QUICK_START.md](./TASK_QUICK_START.md)
- **Backend README:** [office-mate-backend/BACKEND_README.md](./office-mate-backend/BACKEND_README.md)
- **Flask Integration:** [office-mate-backend/FLASK_INTEGRATION.md](./office-mate-backend/FLASK_INTEGRATION.md)

---

## Support

If you encounter issues not covered in this guide:

1. Check the terminal output for error messages
2. Review the troubleshooting section above
3. Check browser console for frontend errors
4. Verify all dependencies are installed
5. Ensure both servers are running on correct ports

---

## Summary Checklist

- [ ] Python 3.8+ installed
- [ ] Node.js 16+ installed
- [ ] Virtual environment created and activated
- [ ] Backend dependencies installed
- [ ] spaCy model downloaded
- [ ] Tesseract OCR installed
- [ ] ML classifier trained
- [ ] Frontend dependencies installed (npm install)
- [ ] Database initialized
- [ ] Backend server running on port 5001
- [ ] Frontend server running on port 8081
- [ ] Can login with admin credentials
- [ ] Can upload documents
- [ ] Can create tasks
- [ ] Dashboard displays data

**Congratulations! Your Office Mate application is now running! 🎉**
