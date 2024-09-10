from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask import current_app

# DB initialize
db = SQLAlchemy()  # This is the generic model structure


def init_db(app):
    """Initialize the database engines using the URLs from the app config."""
    # Source Database engine
    epic_track_engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
    track_session = sessionmaker(bind=epic_track_engine)

    # Target Database engine
    compliance_engine = create_engine(app.config['COMPLIANCE_DATABASE_URI'])
    compliance_session = sessionmaker(bind=compliance_engine)

    return track_session, compliance_session

