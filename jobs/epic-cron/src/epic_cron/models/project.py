from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Create a base class using SQLAlchemy's declarative_base
Base = declarative_base()

class Project(Base):
    """Project Model Class for Cron Job."""

    __tablename__ = "projects"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=True)
