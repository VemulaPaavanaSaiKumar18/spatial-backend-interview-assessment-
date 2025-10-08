from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./spatial.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
	"""Yield a SQLAlchemy Session and ensure it's closed after use.

	Use this in FastAPI dependencies as Depends(database.get_db) so FastAPI
	doesn't introspect the SessionLocal callable and expose internal
	parameters like `local_kw` as API query parameters.
	"""
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()
