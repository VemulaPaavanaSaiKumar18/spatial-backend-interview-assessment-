from fastapi import FastAPI
from .database import Base, engine
from .routers import points, polygons

app = FastAPI(title="Spatial Data API", version="2.0")

Base.metadata.create_all(bind=engine)

app.include_router(points.router)
app.include_router(polygons.router)

# Health check route
@app.get("/health")
def health_check():
    return {"status": "ok"}
