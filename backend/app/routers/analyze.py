from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import os
import uuid
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.core.config import settings
from app.models.user import User
from app.schemas.analysis import AnalysisResponse, AnalysisHistory, PredictionResult

router = APIRouter(prefix="/analyze", tags=["analysis"])


MOCK_PREDICTIONS = [
    {"class_name": "nv", "confidence": 0.72},
    {"class_name": "mel", "confidence": 0.15},
    {"class_name": "bkl", "confidence": 0.05},
    {"class_name": "bcc", "confidence": 0.04},
    {"class_name": "akiec", "confidence": 0.02},
    {"class_name": "vasc", "confidence": 0.01},
    {"class_name": "df", "confidence": 0.01},
]


async def save_upload(file: UploadFile) -> str:
    file_ext = file.filename.split(".")[-1].lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )
    
    unique_filename = f"{uuid.uuid4()}.{file_ext}"
    file_path = os.path.join(settings.UPLOAD_DIR, unique_filename)
    
    os.makedirs(settings.UPLOAD_DIR, exist_ok=True)
    
    with open(file_path, "wb") as f:
        content = await file.read()
        if len(content) > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE // (1024*1024)}MB"
            )
        f.write(content)
    
    return unique_filename


async def get_predictions(image_path: str) -> List[PredictionResult]:
    return [PredictionResult(**pred) for pred in MOCK_PREDICTIONS]


@router.post("", response_model=AnalysisResponse)
async def analyze_image(
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    filename = await save_upload(file)
    predictions = await get_predictions(filename)
    
    top_prediction = predictions[0]
    
    analysis = {
        "id": hash(filename) % 100000,
        "filename": filename,
        "top_prediction": top_prediction.class_name,
        "confidence": top_prediction.confidence,
        "all_predictions": predictions,
        "created_at": datetime.utcnow()
    }
    
    return analysis


@router.get("/history", response_model=AnalysisHistory)
def get_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    return {"analyses": []}
