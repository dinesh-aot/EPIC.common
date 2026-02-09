"""Condition Project Model - Local copy for epic-cron."""

from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()


class Project(Base):
    """Definition of the Condition Projects entity."""

    __tablename__ = 'projects'
    __table_args__ = (
        UniqueConstraint('project_id', name='uq_project'),
        {'schema': 'condition'},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    project_id = Column(String(255), nullable=False, unique=True)
    project_name = Column(Text)
    project_type = Column(Text)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    created_by = Column(String(50))
    updated_by = Column(String(50))
