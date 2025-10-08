from pydantic import BaseModel
from pydantic import ConfigDict
from typing import Dict, Any

class PointBase(BaseModel):
    name: str
    geometry: Dict[str, Any]

class PointCreate(PointBase):
    pass

class PointResponse(PointBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class PolygonBase(BaseModel):
    name: str
    geometry: Dict[str, Any]

class PolygonCreate(PolygonBase):
    pass

class PolygonResponse(PolygonBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
