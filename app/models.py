from sqlalchemy import Column, Integer, String, JSON
from .database import Base

class Point(Base):
    __tablename__ = "points"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    geometry = Column(JSON, nullable=False)

class Polygon(Base):
    __tablename__ = "polygons"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    geometry = Column(JSON, nullable=False)
