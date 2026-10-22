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
"""Trigger report-obligation package sync in Submit for every onboarded project.

The reconcile logic (fetching approved reports from the Condition repository,
creating/removing report packages) lives in submit-api. This cron job only
selects the onboarded projects and calls the submit-api endpoint per project,
so the business rules are not duplicated.
"""
import requests
from flask import current_app

from epic_cron.models.db import session_scope
from epic_cron.models.external.submit import SubmitAccountProject

_REQUEST_TIMEOUT = 60


class ReportSyncService:
    """Service to trigger report-package sync in Submit per onboarded project."""

    @staticmethod
    def sync_project_reports(session_factory):
        """Call the Submit report-package sync endpoint for each onboarded project.

        A project is "onboarded" when it has an account_projects entry. Each
        project's failure is isolated so the rest still run. Returns a run
        summary aggregating the per-project counts returned by Submit.
        """
        submit_api_base_url = current_app.config.get("SUBMIT_API_BASE_URL")
        if not submit_api_base_url:
            current_app.logger.warning(
                "SUBMIT_API_BASE_URL not configured. Skipping report sync."
            )
            return {"projects": 0, "added": 0, "created_packages": 0,
                    "removed": 0, "kept": 0, "skipped": 0}

        token = ReportSyncService._get_admin_token()
        if not token:
            raise RuntimeError("Failed to fetch authorization token.")

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json",
        }

        summary = {"projects": 0, "added": 0, "created_packages": 0,
                   "removed": 0, "kept": 0, "skipped": 0}

        with session_scope(session_factory) as session:
            project_ids = ReportSyncService._get_onboarded_project_ids(session)
        current_app.logger.info("Found %d onboarded projects to sync.", len(project_ids))

        for project_id in project_ids:
            try:
                counts = ReportSyncService._sync_single_project(
                    submit_api_base_url, headers, project_id
                )
                summary["projects"] += 1
                for key in ("added", "created_packages", "removed", "kept"):
                    summary[key] += counts.get(key, 0)
            except requests.RequestException as err:
                summary["skipped"] += 1
                current_app.logger.error(
                    "Skipping project %s: %s", project_id, err
                )

        current_app.logger.info(
            "Report sync complete. projects=%d added=%d created_packages=%d "
            "removed=%d kept=%d skipped=%d",
            summary["projects"], summary["added"], summary["created_packages"],
            summary["removed"], summary["kept"], summary["skipped"],
        )
        return summary

    @staticmethod
    def _get_onboarded_project_ids(session):
        """Return distinct project ids that have an account project."""
        return [
            row[0]
            for row in session.query(SubmitAccountProject.project_id).distinct().all()
        ]

    @staticmethod
    def _sync_single_project(base_url, headers, project_id):
        """Call the Submit report-package sync endpoint for one project."""
        endpoint = f"{base_url}/api/projects/{project_id}/report-packages/sync"
        current_app.logger.info("Syncing report packages for project %s: %s", project_id, endpoint)

        response = requests.post(endpoint, headers=headers, timeout=_REQUEST_TIMEOUT)
        response.raise_for_status()
        return response.json() or {}

    @staticmethod
    def _get_admin_token():
        """Fetch an admin token using client credentials from Keycloak."""
        config = current_app.config
        base_url = config.get("KEYCLOAK_BASE_URL")
        realm = config.get("KEYCLOAK_REALM_NAME")
        admin_client_id = config.get("SERVICE_ACCOUNT_ID")
        admin_secret = config.get("SERVICE_ACCOUNT_SECRET")
        timeout = config.get("CONNECT_TIMEOUT", 60)

        token_url = f"{base_url}/auth/realms/{realm}/protocol/openid-connect/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = (
            f"client_id={admin_client_id}"
            f"&grant_type=client_credentials"
            f"&client_secret={admin_secret}"
        )

        try:
            current_app.logger.info("Fetching Keycloak token from: %s", token_url)
            response = requests.post(token_url, data=data, headers=headers, timeout=timeout)
            response.raise_for_status()
            access_token = response.json().get("access_token")
            if not access_token:
                raise RuntimeError("Keycloak response did not include an access token.")
            return access_token
        except requests.RequestException as err:
            current_app.logger.error("Error while fetching Keycloak token: %s", err)
            raise
