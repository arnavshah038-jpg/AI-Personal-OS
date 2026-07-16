from app.database.db import engine
from app.database.base import Base

# Import all models
import app.database.models

print("Creating tables...")

Base.metadata.create_all(bind=engine)

print("✅ Tables created successfully!")