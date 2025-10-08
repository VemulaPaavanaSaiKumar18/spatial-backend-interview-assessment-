# Spatial Data API (FastAPI + SQLite)

Now includes a **spatial query endpoint** to find points inside polygons! 🗺️

## 🚀 Setup Instructions

1. **Setup the project**
   ```bash
   make setup
   ```

2. **Run the server**
   ```bash
   make server
   ```

3. **Access API Docs**
   Visit: http://127.0.0.1:8000/docs

---

### Example Requests

#### POST /points
```json
{
  "name": "Tower A",
  "geometry": {
    "type": "Point",
    "coordinates": [77.5946, 12.9716]
  }
}
```

#### POST /polygons
```json
{
  "name": "Test Zone",
  "geometry": {
    "type": "Polygon",
    "coordinates": [[[77.5, 12.9], [77.6, 12.9], [77.6, 13.0], [77.5, 13.0], [77.5, 12.9]]]
  }
}
```

#### GET /polygons/{polygon_id}/points
Finds all points located **inside** the given polygon.
