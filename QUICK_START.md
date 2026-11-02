# Quick Start Guide - Abole Coffee Leaf Disease Detection

## 🚀 Single Localhost Setup

Access everything through **http://localhost:3000** (frontend automatically proxies API calls to backend)

## First Time Setup

### 1. Install Frontend Dependencies

Open a terminal in the `frontend` folder and run:

```bash
cd frontend
npm install
```

**Note:** If npm install hangs or fails:
- Try closing all terminal windows and run it again
- Or try: `npm install --legacy-peer-deps`
- Or use yarn: `yarn install`

### 2. Start Both Servers

#### Option A: Use the Startup Script (Windows)
Double-click `START_APP.bat` in the project root

#### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

## 🌐 Access the Application

Once both servers are running, open your browser to:

**http://localhost:3000**

The frontend (port 3000) automatically forwards API requests to the backend (port 8000).

## ✅ Verify Setup

1. **Backend:** http://localhost:8000/health should return `{"status":"ok"}`
2. **Frontend:** http://localhost:3000 should show the Abole web interface

## 📝 System Status

- **Demo Mode:** The system runs in demo mode (no ML model loaded)
- **Predictions:** Returns placeholder results until you train and add the ONNX model
- **Model Location:** Place your trained model at `backend/model/coffee_model.onnx`

## 🛠️ Troubleshooting

### npm install fails or hangs
- Delete `frontend/node_modules` folder if it exists
- Clear npm cache: `npm cache clean --force`
- Try: `npm install --legacy-peer-deps`

### Backend fails to start
- Check Python is installed: `python --version`
- Install dependencies: `cd backend && pip install -r requirements.txt`

### Port already in use
- Backend: Change port in `backend/app/config.py`
- Frontend: Change port in `frontend/vite.config.ts`

## 📦 Project Structure

```
abole/
├── backend/          # FastAPI backend (port 8000)
├── frontend/         # React + Vite frontend (port 3000)
├── model/           # ML model files (.onnx)
├── colab/           # Training notebook
└── START_APP.bat    # Quick start script
```

## 🔗 GitHub Repository

https://github.com/KalkidanAI/abole.git

## 📖 Full Documentation

See `README.md` for complete documentation, API details, and deployment instructions.
