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
"""Synchronize staff work roles from EPIC.track to EPIC.submit."""
from datetime import datetime

from flask import current_app

from epic_cron.models.db import init_submit_db, ma
from epic_cron.services.staff_work_role_sync_service import StaffWorkRoleSyncService


class SyncStaffWorkRole:  # pylint:disable=too-few-public-methods
    """Task to synchronize staff work roles from track to submit."""

    @classmethod
    def sync_staff_work_roles(cls):
        """Synchronize staff work roles from track to submit."""
        init_submit_db(current_app)
        ma.init_app(current_app)
        current_app.logger.info('Starting Staff Work Role Sync---{}'.format(datetime.now()))
        StaffWorkRoleSyncService.sync_staff_work_roles_to_submit()
