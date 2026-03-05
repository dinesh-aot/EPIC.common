"""Track Work Model - Local copy for epic-cron."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TrackWork(Base):
    """Track Work Model Class - Read-only table synchronized from EPIC.track."""

    __tablename__ = "track_works"

    id = Column(Integer, primary_key=True, autoincrement=False)
    project_id = Column(Integer, nullable=False)
    current_phase_id = Column(Integer, nullable=True)
    work_state = Column(String(50), nullable=True)
    title = Column(String(500), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
