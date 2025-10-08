from pydantic import BaseModel
from typing import Dict, Any

class PointBase(BaseModel):
    name: str
    geometry: Dict[str, Any]

class PointCreate(PointBase):
    pass

class PointResponse(PointBase):
    id: int
    class Config:
        orm_mode = True

class PolygonBase(BaseModel):
    name: str
    geometry: Dict[str, Any]

class PolygonCreate(PolygonBase):
    pass

class PolygonResponse(PolygonBase):
    id: int
    class Config:
        orm_mode = True
