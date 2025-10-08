from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/points", tags=["Points"])

@router.post("/", response_model=schemas.PointResponse)
def create_point(point: schemas.PointCreate, db: Session = Depends(database.get_db)):
    return crud.create_point(db, point)

@router.get("/", response_model=list[schemas.PointResponse])
def get_points(db: Session = Depends(database.get_db)):
    return crud.get_points(db)

@router.put("/{point_id}", response_model=schemas.PointResponse)
def update_point(point_id: int, updated: schemas.PointCreate, db: Session = Depends(database.get_db)):
    point = crud.update_point(db, point_id, updated)
    if not point:
        raise HTTPException(status_code=404, detail="Point not found")
    return point
