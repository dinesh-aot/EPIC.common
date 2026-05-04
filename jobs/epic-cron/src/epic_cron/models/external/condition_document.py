"""Condition Document Model - Local copy for epic-cron."""

from datetime import datetime

from sqlalchemy import Boolean, Column, Date, DateTime, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import UniqueConstraint

Base = declarative_base()


class Document(Base):
    """Definition of the Condition Documents entity."""

    __tablename__ = 'documents'
    __table_args__ = (
        UniqueConstraint('document_id', name='uq_document'),
        {'schema': 'condition'},
    )

    id = Column(Integer, primary_key=True, autoincrement=True)
    document_id = Column(String(255), nullable=False, unique=True)
    document_type_id = Column(Integer, nullable=True)
    document_label = Column(Text)
    document_file_name = Column(Text)
    date_issued = Column(Date)
    act = Column(Integer)
    consultation_records_required = Column(Boolean)
    is_latest_amendment_added = Column(Boolean)
    is_active = Column(Boolean, default=False, nullable=False, server_default='false')
    project_id = Column(String(255), nullable=False)
    created_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_date = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)
    created_by = Column(String(50))
    updated_by = Column(String(50))
