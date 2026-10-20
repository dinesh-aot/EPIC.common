"""Tests for the report-package sync cron trigger (SYNC_REPORT)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

import requests
from flask import Flask

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
for _path in (PROJECT_ROOT, SRC_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from epic_cron.services.report_sync_service import ReportSyncService  # noqa: E402


def _app():
    """Return a Flask app configured with a Submit API base URL."""
    app = Flask(__name__)
    app.config["SUBMIT_API_BASE_URL"] = "http://submit"
    return app


def _response(payload):
    """Return a mock requests response yielding the given JSON payload."""
    resp = MagicMock()
    resp.json.return_value = payload
    resp.raise_for_status.return_value = None
    return resp


def test_skips_when_submit_api_not_configured():
    """Without SUBMIT_API_BASE_URL the job is a no-op."""
    app = Flask(__name__)
    with app.app_context():
        summary = ReportSyncService.sync_project_reports(session_factory=object())
    assert summary["projects"] == 0


def test_calls_endpoint_per_project_and_aggregates_counts():
    """Each onboarded project is synced and its counts are aggregated."""
    app = _app()
    with app.app_context(), \
            patch.object(ReportSyncService, "_get_admin_token", return_value="tok"), \
            patch.object(ReportSyncService, "_get_onboarded_project_ids", return_value=[1, 2]), \
            patch("epic_cron.services.report_sync_service.session_scope"), \
            patch("epic_cron.services.report_sync_service.requests.post") as post:
        post.side_effect = [
            _response({"added": 2, "created_packages": 2, "removed": 0, "kept": 1}),
            _response({"added": 1, "created_packages": 1, "removed": 1, "kept": 0}),
        ]
        summary = ReportSyncService.sync_project_reports(session_factory=object())

    assert post.call_count == 2
    assert summary["projects"] == 2
    assert summary["added"] == 3
    assert summary["created_packages"] == 3
    assert summary["removed"] == 1
    assert summary["kept"] == 1
    assert summary["skipped"] == 0


def test_isolates_failing_project_and_continues():
    """A project whose endpoint call fails is skipped; others still process."""
    app = _app()
    with app.app_context(), \
            patch.object(ReportSyncService, "_get_admin_token", return_value="tok"), \
            patch.object(ReportSyncService, "_get_onboarded_project_ids", return_value=[1, 2]), \
            patch("epic_cron.services.report_sync_service.session_scope"), \
            patch("epic_cron.services.report_sync_service.requests.post") as post:
        post.side_effect = [
            requests.RequestException("boom"),
            _response({"added": 1, "created_packages": 1, "removed": 0, "kept": 0}),
        ]
        summary = ReportSyncService.sync_project_reports(session_factory=object())

    assert summary["skipped"] == 1
    assert summary["projects"] == 1
    assert summary["added"] == 1


def test_endpoint_url_uses_project_id():
    """The per-project call targets the report-packages sync endpoint."""
    app = _app()
    with app.app_context(), \
            patch("epic_cron.services.report_sync_service.requests.post") as post:
        post.return_value = _response({"added": 0, "created_packages": 0, "removed": 0, "kept": 0})
        ReportSyncService._sync_single_project("http://submit", {}, 42)

    called_url = post.call_args[0][0]
    assert called_url == "http://submit/api/projects/42/report-packages/sync"
