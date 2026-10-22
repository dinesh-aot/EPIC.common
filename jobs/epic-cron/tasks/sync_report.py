# Copyright © 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the 'License');
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an 'AS IS' BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Sync approved report obligations from the condition repository into Submit."""
from datetime import datetime

from flask import current_app

from epic_cron.models.db import init_submit_db, init_submit_session, ma
from epic_cron.services.report_sync_service import ReportSyncService


class SyncReport:  # pylint:disable=too-few-public-methods
    """Task to sync approved reports for onboarded projects."""

    @classmethod
    def sync_report(cls):
        """Sync approved reports from the condition repository into Submit."""
        init_submit_db(current_app)
        submit_session = init_submit_session(current_app)
        ma.init_app(current_app)
        current_app.logger.info('Starting Report Sync---{}'.format(datetime.now()))
        ReportSyncService.sync_project_reports(submit_session)
