from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(prefix="/polygons", tags=["Polygons"])

@router.post("/", response_model=schemas.PolygonResponse)
def create_polygon(polygon: schemas.PolygonCreate, db: Session = Depends(database.get_db)):
    return crud.create_polygon(db, polygon)

@router.get("/", response_model=list[schemas.PolygonResponse])
def get_polygons(db: Session = Depends(database.get_db)):
    return crud.get_polygons(db)

@router.put("/{polygon_id}", response_model=schemas.PolygonResponse)
def update_polygon(polygon_id: int, updated: schemas.PolygonCreate, db: Session = Depends(database.get_db)):
    poly = crud.update_polygon(db, polygon_id, updated)
    if not poly:
        raise HTTPException(status_code=404, detail="Polygon not found")
    return poly

@router.get("/{polygon_id}/points", response_model=list[schemas.PointResponse])
def get_points_inside_polygon(polygon_id: int, db: Session = Depends(database.get_db)):
    points = crud.get_points_in_polygon(db, polygon_id)
    if points is None:
        raise HTTPException(status_code=404, detail="Polygon not found")
    return points
