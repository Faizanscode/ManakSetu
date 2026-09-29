from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
import uuid

from app.database import get_db
from app import models, schemas

router = APIRouter(
    prefix="/history",
    tags=["History"],
    responses={404: {"description": "Not found"}},
)

@router.post("/", response_model=schemas.AnalysisHistoryResponse, status_code=status.HTTP_201_CREATED)
def create_history(history: schemas.AnalysisHistoryCreate, db: Session = Depends(get_db)):
    db_history = models.AnalysisHistory(
        id=str(uuid.uuid4()),
        title=history.title,
        procurement_requirement=history.procurement_requirement,
        category=history.category,
        priority=history.priority,
        extracted_requirement=history.extracted_requirement,
        recommendations=history.recommendations,
        gaps=history.gaps,
        specification=history.specification,
        status=history.status
    )
    db.add(db_history)
    db.commit()
    db.refresh(db_history)
    return db_history

@router.get("/", response_model=List[schemas.AnalysisHistoryList])
def list_history(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    histories = db.query(models.AnalysisHistory).order_by(models.AnalysisHistory.created_at.desc()).offset(skip).limit(limit).all()
    return histories

@router.get("/{history_id}", response_model=schemas.AnalysisHistoryResponse)
def get_history(history_id: str, db: Session = Depends(get_db)):
    db_history = db.query(models.AnalysisHistory).filter(models.AnalysisHistory.id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="Analysis history not found")
    return db_history

@router.put("/{history_id}", response_model=schemas.AnalysisHistoryResponse)
def update_history(history_id: str, history_update: schemas.AnalysisHistoryUpdate, db: Session = Depends(get_db)):
    db_history = db.query(models.AnalysisHistory).filter(models.AnalysisHistory.id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="Analysis history not found")
    
    update_data = history_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_history, key, value)
        
    db.commit()
    db.refresh(db_history)
    return db_history

@router.delete("/{history_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_history(history_id: str, db: Session = Depends(get_db)):
    db_history = db.query(models.AnalysisHistory).filter(models.AnalysisHistory.id == history_id).first()
    if db_history is None:
        raise HTTPException(status_code=404, detail="Analysis history not found")
    db.delete(db_history)
    db.commit()
    return None
