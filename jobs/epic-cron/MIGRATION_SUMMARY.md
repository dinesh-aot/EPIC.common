# Submit-Cron to Epic-Cron Migration Summary

**Migration Date:** February 6, 2026  
**Status:** ✅ COMPLETED

## Overview

Successfully migrated all submit-cron functionality from `submit-v2/submit-cron` to `common/jobs/epic-cron`. The epic-cron service now consolidates all EPIC system cron jobs in one location as part of the Epic.Common repository.

## What Was Migrated

### Source Code
- ✅ All submit_cron Python modules → `epic_cron/submit/`
  - 9 services (mail, CHES, invitation, package submission, etc.)
  - Models for Submit and Centre databases
  - 5 processors for centre email handling
  - Repositories and utilities
- ✅ 3 task files (submit_mail, centre_mail, sync_approved_condition)
- ✅ 9 HTML email templates → `templates/submit/`
- ✅ 3 shell scripts (run_emailer.sh, run_centre_emailer.sh, run_approved_condition.sh)

### Configuration
- ✅ CHES email service configuration
- ✅ JWT/OIDC and Keycloak settings
- ✅ Submit web URL and sender email configuration
- ✅ Centre database configuration
- ✅ Condition API configuration

### Cron Jobs
Now running 5 cron jobs total:
1. **Project Extractor (Submit)** - Daily at 1am
2. **Project Extractor (Compliance)** - Daily at 3am
3. **Submit Emailer** - Every 5 minutes
4. **Centre Emailer** - Every 5 minutes
5. **Approved Condition Sync** - Weekdays at 5pm

### Helm Chart
- ✅ Updated deployment.yaml with CHES, Centre DB, and Keycloak environment variables
- ✅ Added secrets for CHES and Keycloak credentials
- ✅ Updated values.yaml, values.prod.yaml, and values.test.yaml
- ✅ Configured crontab with all 5 jobs

### Dependencies
- ✅ Added marshmallow==3.21.3
- ✅ Added marshmallow-enum==1.5.1
- ✅ Added pytz
- ✅ Updated flask-jwt-oidc

### Tests & Migrations
- ✅ Copied to `tests/submit/`
- ✅ Copied to `migrations/submit/`

## Key Changes Made

### Import Path Updates
All imports changed from:
```python
from submit_cron.services.mail_service import EmailService
```
To:
```python
from epic_cron.submit.services.mail_service import EmailService
```

### Configuration Updates
**File:** `config.py`
- Added CHES configuration (token endpoint, client ID/secret, base URL)
- Added JWT/OIDC settings
- Added Centre database URI
- Added submit web configuration (WEB_URL, SENDER_EMAIL, STAFF_SUPPORT_MAIL_ID)
- Added SQLALCHEMY_DATABASE_URI alias for backward compatibility

### Job Handler Updates
**File:** `invoke_jobs.py`
- Added EMAIL job handler (supports both SUBMIT and CENTRE targets)
- Added SYNC_CONDITION job handler
- Imported SubmitMailer, CentreMailer, and SyncApprovedCondition classes

### Crontab Updates
**File:** `cron/crontab`
```
# PROJECT EXTRACTORS
0 1 * * * default cd /epic-cron && ./run_project_cron_submit.sh
0 3 * * * default cd /epic-cron && ./run_project_cron_compliance.sh
# SUBMIT EMAILER - Runs every 5 minutes
*/5 * * * * default cd /epic-cron && ./run_emailer.sh
# CENTRE EMAILER - Runs every 5 minutes
*/5 * * * * default cd /epic-cron && ./run_centre_emailer.sh
# SYNC APPROVED CONDITION - Runs at 5pm on weekdays
0 17 * * 1-5 default cd /epic-cron && ./run_approved_condition.sh
```

## Directory Structure

```
common/jobs/epic-cron/
├── src/
│   └── epic_cron/
│       ├── submit/              # NEW: All submit-cron code
│       │   ├── models/
│       │   ├── services/
│       │   ├── processors/
│       │   ├── repositories/
│       │   └── utils/
│       ├── models/
│       ├── services/
│       └── utils/
├── tasks/
│   ├── project_extractor.py
│   ├── virus_scanner.py
│   ├── submit_mail.py           # NEW
│   ├── centre_mail.py           # NEW
│   └── sync_approved_condition.py # NEW
├── templates/
│   └── submit/                  # NEW: 9 HTML email templates
├── migrations/
│   └── submit/                  # NEW: Submit-specific migrations
├── tests/
│   └── submit/                  # NEW: Submit-specific tests
├── cron/
│   └── crontab                  # UPDATED: 5 jobs
├── config.py                    # UPDATED: Added CHES, JWT, Centre DB
├── invoke_jobs.py               # UPDATED: Added EMAIL, SYNC_CONDITION
├── requirements/
│   └── prod.txt                 # UPDATED: Added dependencies
├── run_emailer.sh               # NEW
├── run_centre_emailer.sh        # NEW
└── run_approved_condition.sh    # NEW
```

## Helm Chart Environment Variables Added

### CHES Configuration
- `CHES_TOKEN_ENDPOINT`
- `CHES_BASE_URL`
- `CHES_CLIENT_ID` (secret)
- `CHES_CLIENT_SECRET` (secret)

### Centre Database
- `CENTRE_DATABASE_USERNAME`
- `CENTRE_DATABASE_PASSWORD`
- `CENTRE_DATABASE_NAME`
- `CENTRE_DATABASE_HOST`
- `CENTRE_DATABASE_PORT`

### Submit Web Configuration
- `WEB_URL`
- `SENDER_EMAIL`
- `STAFF_SUPPORT_MAIL_ID`

### Keycloak
- `KEYCLOAK_BASE_URL`
- `KEYCLOAK_REALM_NAME`
- `KEYCLOAK_SERVICE_ACCOUNT_ID` (secret)
- `KEYCLOAK_SERVICE_ACCOUNT_SECRET` (secret)

### Condition API
- `CONDITION_API_BASE_URL`

## Next Steps

### 1. Testing
- [ ] Test all 5 cron jobs in development environment
- [ ] Verify database connections (Submit, Centre, Track, Compliance, Condition)
- [ ] Test CHES email sending functionality
- [ ] Test Keycloak authentication
- [ ] Run unit tests from `tests/submit/`

### 2. Deployment
- [ ] Build Docker image with merged code
- [ ] Update CI/CD pipeline to build epic-cron with submit functionality
- [ ] Deploy to test environment
- [ ] Monitor cron job execution logs
- [ ] Validate email delivery

### 3. Configuration
- [ ] Set CHES credentials in secrets
- [ ] Set Keycloak service account credentials
- [ ] Configure environment-specific URLs and email addresses
- [ ] Update CONDITION_API_BASE_URL for each environment

### 4. Documentation
- [ ] Update team documentation about consolidated cron location
- [ ] Document new environment variables
- [ ] Update deployment procedures

### 5. Deprecation
- [ ] Plan deprecation timeline for submit-v2/submit-cron deployment
- [ ] Notify teams about migration
- [ ] Schedule removal of old submit-cron deployment

## Important Notes

### Backward Compatibility
- `SQLALCHEMY_DATABASE_URI` is aliased to `SUBMIT_DATABASE_URI` for compatibility
- All original submit-cron functionality is preserved
- No changes were made to submit-v2/submit-cron (as requested)

### Database Connections
Epic-cron now connects to 5 databases:
1. **Track DB** - Project tracking data
2. **Submit DB** - Submit application data
3. **Compliance DB** - Compliance data
4. **Centre DB** - Centre-specific data (uses submit-patroni)
5. **Condition DB** - Condition API (via REST API)

### Python Version
- Epic-cron uses Python 3.10
- Submit-cron used Python 3.12
- Consider upgrading to 3.12 in future for consistency

### Dependency Considerations
- Marshmallow version pinned to 3.21.3 for compatibility
- Flask-jwt-oidc version updated (removed specific version pin)
- All submit-cron dependencies are now included

## Verification Checklist

Before deploying to production:
- [ ] All imports updated correctly
- [ ] All environment variables configured
- [ ] Secrets properly set in Helm values
- [ ] Crontab schedules verified
- [ ] Database connections tested
- [ ] CHES email service tested
- [ ] All 5 cron jobs execute successfully
- [ ] Logs show no errors
- [ ] Email delivery confirmed
- [ ] Approved condition sync working

## Contact

For questions or issues related to this migration, contact the EPIC development team.

---

**Migration completed successfully on February 6, 2026**
