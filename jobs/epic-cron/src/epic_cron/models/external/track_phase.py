"""Track Phase Model - Local copy for epic-cron."""

from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TrackPhase(Base):
    """Track Phase Model Class."""

    __tablename__ = "track_phases"

    id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(255), nullable=False)
    ea_act_id = Column(Integer, nullable=True)
    ea_act_name = Column(String(255), nullable=True)
    work_type_id = Column(Integer, nullable=False)
    work_type_name = Column(String(255), nullable=True)
    sort_order = Column(Integer, nullable=True)
    number_of_days = Column(Integer, nullable=True)
    display_name = Column(String(255), nullable=True)
    legislated = Column(Boolean, default=False, nullable=False)
    enable_submit = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False, nullable=False)
    created_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    updated_date = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc), nullable=True)
    created_by = Column(String(100), nullable=True)
    updated_by = Column(String(100), nullable=True)
