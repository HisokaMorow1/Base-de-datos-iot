from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base  # Usa el Base de models.py

DATABASE_URL = "postgresql+psycopg2://iot_user:admin@localhost:5432/iot_db"

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)