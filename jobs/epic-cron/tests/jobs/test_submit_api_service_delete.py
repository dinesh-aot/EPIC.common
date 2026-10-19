"""Tests for SubmitApiService de-provisioning (work_id + email)."""

import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from flask import Flask

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SRC_DIR = PROJECT_ROOT / "src"
for _path in (PROJECT_ROOT, SRC_DIR):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

from epic_cron.services.submit_api_service import SubmitApiService  # noqa: E402

MODULE_PATH = "epic_cron.services.submit_api_service"


def _app():
    """Build a Flask app configured with the Submit API base URL."""
    app = Flask(__name__)
    app.config["SUBMIT_API_BASE_URL"] = "http://submit-api"
    app.config["CONNECT_TIMEOUT"] = 60
    return app


def test_delete_staff_user_work_sends_email_as_query_param():
    """The delete call targets the work endpoint and passes email as a param."""
    app = _app()
    with app.app_context(), \
            patch.object(SubmitApiService, "_get_headers", return_value={}), \
            patch(f"{MODULE_PATH}.requests") as mock_requests:
        response = MagicMock()
        response.json.return_value = {"message": "removed"}
        mock_requests.delete.return_value = response

        result = SubmitApiService.delete_staff_user_work(
            work_id=42, email="a@b.ca"
        )

        assert result == {"message": "removed"}
        mock_requests.delete.assert_called_once()
        _args, kwargs = mock_requests.delete.call_args
        called_url = _args[0] if _args else kwargs.get("url")
        assert called_url == "http://submit-api/api/staff-user-works/work/42"
        assert kwargs["params"] == {"email": "a@b.ca"}


def test_delete_staff_user_work_raises_on_http_error():
    """A failed HTTP call propagates the exception to the caller."""
    app = _app()
    with app.app_context(), \
            patch.object(SubmitApiService, "_get_headers", return_value={}), \
            patch(f"{MODULE_PATH}.requests") as mock_requests:
        response = MagicMock()
        response.raise_for_status.side_effect = Exception("boom")
        mock_requests.delete.return_value = response

        try:
            SubmitApiService.delete_staff_user_work(work_id=1, email="a@b.ca")
            assert False, "expected exception"
        except Exception as ex:  # noqa: B902
            assert "boom" in str(ex)
