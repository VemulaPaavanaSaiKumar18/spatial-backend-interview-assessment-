from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

from app import main, database
from app.database import Base


# Use an in-memory SQLite database for tests
SQLALCHEMY_TEST_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module", autouse=True)
def prepare_database():
    # Create tables
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def db_session():
    # Use a connection + transaction to isolate tests
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    try:
        yield session
    finally:
        session.close()
        transaction.rollback()
        connection.close()


@pytest.fixture()
def client(db_session):
    # Override the app dependency to use the test session
    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    main.app.dependency_overrides[database.get_db] = override_get_db
    client = TestClient(main.app)
    yield client
    main.app.dependency_overrides.clear()


def test_health_check(client):
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok"}


def test_create_and_get_point(client):
    payload = {
        "name": "Tower A",
        "geometry": {"type": "Point", "coordinates": [77.5946, 12.9716]}
    }
    r = client.post("/points/", json=payload)
    assert r.status_code == 200
    data = r.json()
    assert data["id"] == 1
    assert data["name"] == payload["name"]
    assert data["geometry"] == payload["geometry"]

    # list points
    r2 = client.get("/points/")
    assert r2.status_code == 200
    items = r2.json()
    assert isinstance(items, list)
    assert len(items) == 1


def test_update_point_not_found(client):
    payload = {"name": "Nope", "geometry": {"type": "Point", "coordinates": [0, 0]}}
    r = client.put("/points/999", json=payload)
    assert r.status_code == 404


def test_polygon_points_query(client):
    # create a polygon roughly surrounding the test point
    poly_payload = {
        "name": "Test Zone",
        "geometry": {
            "type": "Polygon",
            "coordinates": [[[77.5, 12.9], [77.7, 12.9], [77.7, 13.1], [77.5, 13.1], [77.5, 12.9]]]
        }
    }
    rpoly = client.post("/polygons/", json=poly_payload)
    assert rpoly.status_code == 200
    poly = rpoly.json()
    poly_id = poly["id"]

    # create an inside point
    inside = {"name": "Inside", "geometry": {"type": "Point", "coordinates": [77.6, 13.0]}}
    r1 = client.post("/points/", json=inside)
    assert r1.status_code == 200

    # create an outside point
    outside = {"name": "Outside", "geometry": {"type": "Point", "coordinates": [78.0, 14.0]}}
    r2 = client.post("/points/", json=outside)
    assert r2.status_code == 200

    # query points inside polygon
    rpts = client.get(f"/polygons/{poly_id}/points")
    assert rpts.status_code == 200
    pts = rpts.json()
    # should include the inside point but not the outside one
    names = {p["name"] for p in pts}
    assert "Inside" in names
    assert "Outside" not in names


def test_polygon_not_found(client):
    r = client.get("/polygons/9999/points")
    assert r.status_code == 404
