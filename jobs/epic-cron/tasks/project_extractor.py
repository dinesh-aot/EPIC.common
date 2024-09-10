from datetime import datetime
from epic_cron.models.db import init_db  # Function that initializes DB engines
from epic_cron.models.project import Project  # Import the independent Project model
from flask import current_app

class ProjectExtractor:
    """Task to run EpicTrack Project Extraction."""

    @classmethod
    def do_sync(cls):
        """Perform the ETL."""
        print('Starting Project Extractor at------------------------', datetime.now())

        # Initialize sessions for both source (Epic Track) and target (Compliance) databases
        track_session, compliance_session = init_db(current_app)

        # Step 1: Clear the Compliance DB (Target DB) of existing Project records
        compliance_sess = compliance_session()  # Manually create a session for target DB
        try:
            print("Deleting all records from Compliance DB (Target)")
            compliance_sess.query(Project).delete()
            compliance_sess.commit()
            print("Deleted all existing Project records from Compliance DB")

        except Exception as e:
            print(f"Error occurred while clearing Compliance DB: {e}")
            compliance_sess.rollback()
        finally:
            compliance_sess.close()  # Ensure session is closed after deletion

        # Step 2: Query projects from Epic Track (Source DB) and insert into Compliance DB
        session = track_session()  # Manually create a session for source DB
        try:
            projects = session.query(Project).all()
            print('------------ Retrieved projects from Epic Track')

            # Insert new records into the Compliance DB
            for project in projects:
                print(f"Processing project: {project.name}")

                compliance_sess = compliance_session()  # Manually create a session for target DB
                try:
                    # Insert new record into Compliance DB
                    new_compliance_project = Project(
                        id=project.id,
                        name=project.name,
                        description=project.description
                    )
                    compliance_sess.add(new_compliance_project)
                    print(f"Inserted new target project: {new_compliance_project.name}")

                    # Step 3: Commit changes to the Compliance DB
                    compliance_sess.commit()

                except Exception as e:
                    print(f"Error occurred while writing to Compliance DB: {e}")
                    compliance_sess.rollback()
                finally:
                    compliance_sess.close()  # Ensure session is closed after each iteration

        except Exception as e:
            print(f"Error occurred during ETL: {e}")
            session.rollback()

        finally:
            session.close()  # Ensure the session is closed at the end
