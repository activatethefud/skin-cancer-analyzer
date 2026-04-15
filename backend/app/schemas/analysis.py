from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class PredictionResult(BaseModel):
    class_name: str
    confidence: float


class AnalysisResponse(BaseModel):
    id: int
    filename: str
    top_prediction: str
    confidence: float
    all_predictions: List[PredictionResult]
    created_at: datetime


class AnalysisHistory(BaseModel):
    analyses: List[AnalysisResponse]
