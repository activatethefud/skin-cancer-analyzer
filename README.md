# Skin Cancer Analyzer

AI-powered skin lesion analysis using deep learning.

## Quick Start

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

### ML Training
```bash
cd ml
pip install -r requirements.txt
python prepare_dataset.py
python train.py
python export_model.py
```

## Docker

```bash
docker-compose up
```

## API Endpoints

- `POST /api/auth/register` - Create account
- `POST /api/auth/login` - Get JWT token
- `POST /api/analyze` - Upload image for analysis (auth required)
- `GET /api/analyze/history` - Get analysis history (auth required)

## Skin Lesion Classes

| Class | Description |
|-------|-------------|
| nv | Melanocytic nevi (benign) |
| mel | Melanoma (malignant) |
| bkl | Benign keratosis |
| vasc | Vascular lesions |
| bcc | Basal cell carcinoma |
| akiec | Actinic keratoses |
| df | Dermatofibroma |
