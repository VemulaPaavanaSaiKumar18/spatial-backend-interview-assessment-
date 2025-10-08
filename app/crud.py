from sqlalchemy.orm import Session
from shapely.geometry import shape
from . import models, schemas

# ---------- POINTS ----------
def create_point(db: Session, point: schemas.PointCreate):
    db_point = models.Point(name=point.name, geometry=point.geometry)
    db.add(db_point)
    db.commit()
    db.refresh(db_point)
    return db_point

def get_points(db: Session):
    return db.query(models.Point).all()

def update_point(db: Session, point_id: int, updated: schemas.PointCreate):
    db_point = db.query(models.Point).filter(models.Point.id == point_id).first()
    if db_point:
        db_point.name = updated.name
        db_point.geometry = updated.geometry
        db.commit()
        db.refresh(db_point)
    return db_point

# ---------- POLYGONS ----------
def create_polygon(db: Session, polygon: schemas.PolygonCreate):
    db_poly = models.Polygon(name=polygon.name, geometry=polygon.geometry)
    db.add(db_poly)
    db.commit()
    db.refresh(db_poly)
    return db_poly

def get_polygons(db: Session):
    return db.query(models.Polygon).all()

def update_polygon(db: Session, polygon_id: int, updated: schemas.PolygonCreate):
    db_poly = db.query(models.Polygon).filter(models.Polygon.id == polygon_id).first()
    if db_poly:
        db_poly.name = updated.name
        db_poly.geometry = updated.geometry
        db.commit()
        db.refresh(db_poly)
    return db_poly

# ---------- SPATIAL QUERY ----------
def get_points_in_polygon(db: Session, polygon_id: int):
    poly_record = db.query(models.Polygon).filter(models.Polygon.id == polygon_id).first()
    if not poly_record:
        return None

    polygon_shape = shape(poly_record.geometry)
    points = db.query(models.Point).all()

    inside_points = []
    for p in points:
        point_shape = shape(p.geometry)
        if polygon_shape.contains(point_shape):
            inside_points.append(p)

    return inside_points
