from fastapi import APIRouter, Depends, HTTPException, Query, Response
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List, Optional
from app.database import get_db
import app.models as models
import app.schemas as schemas

router = APIRouter(prefix="/standards", tags=["Standards"])

@router.get("", response_model=List[schemas.StandardList])
def get_standards(
    response: Response,
    db: Session = Depends(get_db),
    sector_id: Optional[str] = None,
    category_id: Optional[str] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 200
):
    query = db.query(models.Standard).options(
        joinedload(models.Standard.sector),
        joinedload(models.Standard.category)
    )
    if sector_id:
        query = query.filter(models.Standard.sector_id == sector_id)
    if category_id:
        query = query.filter(models.Standard.category_id == category_id)
    if status:
        query = query.filter(models.Standard.status == status)
    
    total_count = query.count()
    response.headers["X-Total-Count"] = str(total_count)
    response.headers["Access-Control-Expose-Headers"] = "X-Total-Count"
    
    return query.offset(skip).limit(limit).all()

@router.get("/search", response_model=List[schemas.StandardList])
def search_standards(
    q: str = Query(..., min_length=1),
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100
):
    search_pattern = f"%{q}%"
    
    # Simple structured search matching standard number, title, short description
    query = db.query(models.Standard).options(
        joinedload(models.Standard.sector),
        joinedload(models.Standard.category)
    ).filter(
        or_(
            models.Standard.standard_number.ilike(search_pattern),
            models.Standard.title.ilike(search_pattern),
            models.Standard.short_description.ilike(search_pattern)
        )
    )
    return query.offset(skip).limit(limit).all()

@router.get("/sectors", response_model=List[schemas.SectorBase])
def get_sectors(db: Session = Depends(get_db)):
    return db.query(models.Sector).all()

@router.get("/categories", response_model=List[schemas.CategoryBase])
def get_categories(sector_id: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(models.Category)
    if sector_id:
        query = query.filter(models.Category.sector_id == sector_id)
    return query.all()

@router.get("/{standard_id}", response_model=schemas.StandardDetail)
def get_standard_by_id(standard_id: str, db: Session = Depends(get_db)):
    standard = db.query(models.Standard).filter(models.Standard.id == standard_id).first()
    if not standard:
        raise HTTPException(status_code=404, detail="Standard not found")
    return standard

@router.get("/{standard_id}/relationships", response_model=List[schemas.StandardRelationshipBase])
def get_standard_relationships(standard_id: str, db: Session = Depends(get_db)):
    return db.query(models.StandardRelationship).filter(
        or_(
            models.StandardRelationship.source_standard_id == standard_id,
            models.StandardRelationship.target_standard_id == standard_id
        )
    ).all()

@router.get("/{standard_id}/sources", response_model=List[schemas.StandardSourceBase])
def get_standard_sources(standard_id: str, db: Session = Depends(get_db)):
    return db.query(models.StandardSource).filter(models.StandardSource.standard_id == standard_id).all()
