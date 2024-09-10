# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Generate account statements.

This module will create statement records for each account.
"""
import os
import sys

from flask import Flask
from utils.logger import setup_logging
import config

setup_logging(os.path.join(os.path.abspath(os.path.dirname(__file__)), 'logging.conf'))  # important to do this first


def create_app(run_mode=os.getenv('FLASK_ENV', 'production')):
    """Return a configured Flask App using the Factory method."""
    from epic_cron.models.db import init_db  # Import the correct methods

    app = Flask(__name__)
    print(f'>>>>> Creating app in run_mode: {run_mode}')

    # Load configuration based on the run mode
    app.config.from_object(config.CONFIGURATION.get(run_mode, 'production'))

    # Initialize the Epic Track and Compliance DB engines using init_db
    track_session, compliance_session = init_db(app)

    # Configure other components (e.g., Sentry, logging, etc.)
    # ...

    register_shellcontext(app)

    # Return the app along with the database sessions
    return app, track_session, compliance_session


def register_shellcontext(app):
    """Register shell context objects."""
    def shell_context():
        """Shell context objects."""
        return {
            'app': app
        }

    app.shell_context_processor(shell_context)


def run(job_name):
    """Main function to run the job."""
    from tasks.project_extractor import ProjectExtractor

    # Create the Flask app and initialize database sessions
    application, track_session, compliance_session = create_app()

    # Push the app context to ensure the Flask app is available during task execution
    with application.app_context():
        if job_name == 'EXTRACT_PROJECT':
            ProjectExtractor.do_sync()  # Pass sessions
            application.logger.info(f'<<<< Completed Project Sync >>>>')
        else:
            application.logger.debug('No valid job_name passed. Exiting without running any tasks.')

    return


if __name__ == "__main__":
    run('EXTRACT_PROJECT')
