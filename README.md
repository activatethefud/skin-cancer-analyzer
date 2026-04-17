# Skin Cancer Analyzer

AI-powered skin lesion analysis using deep learning (MobileNetV3-Small).

## Quick Start (Without Docker)

### 1. Install dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend  
cd ../frontend
npm install
```

### 2. Start services
```bash
# Option 1: Use the start script (starts both backend & frontend)
./start.sh

# Option 2: Manual start
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
```

### 3. Open browser
- Frontend: http://localhost:3000
- API Docs: http://localhost:8000/docs

## Docker

```bash
docker-compose up
```

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/register` | POST | Create account |
| `/api/auth/login` | POST | Get JWT token |
| `/api/analyze` | POST | Upload image for analysis (auth required) |
| `/api/analyze/history` | GET | Get analysis history (auth required) |
| `/api/analyze/model-status` | GET | Check if model is loaded |

## Skin Lesion Classes (Binary)

| Class | Description |
|-------|-------------|
| benign | Benign lesion |
| malignant | Malignant lesion (melanoma, etc.) |

## Tech Stack

- **Frontend**: Next.js 14, TypeScript, Tailwind CSS
- **Backend**: FastAPI, SQLAlchemy, JWT auth
- **ML**: PyTorch + torchvision, MobileNetV3-Small

## Model Training

```bash
cd ml
pip install -r requirements.txt

# Download dataset from HuggingFace
python -c "from datasets import load_dataset; load_dataset('preetsojitra/binary-2K-samples-skin-lesion-HM10000')"

# Train
python src/train.py

# Export to backend
python src/export_model.py
```