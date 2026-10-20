# CRON Jobs

## SYNC_REPORT

Triggers the report-obligation package sync in Submit for every onboarded project.

The reconcile logic (fetching approved reports from the Condition repository,
inserting obligations, and creating/removing their submission packages) lives in
**submit-api**. This cron job only selects the onboarded projects and calls the
submit-api endpoint per project, so the business rules are not duplicated.

- Run: `python3 invoke_jobs.py SYNC_REPORT` (or `./run_sync_report.sh`). Scheduled
  daily at midnight.
- Scope: projects that have an `account_projects` entry in Submit.
- Call: `POST {SUBMIT_API_BASE_URL}/api/projects/{project_id}/report-packages/sync`,
  authorized with the Keycloak service account (`SERVICE_ACCOUNT_ID` /
  `SERVICE_ACCOUNT_SECRET`). The service account must carry the `eao_create`
  (or `full_access`) realm role.
- Error handling: a project whose endpoint call fails is logged and skipped; the run
  continues and logs an aggregated summary
  (`projects`, `added`, `created_packages`, `removed`, `kept`, `skipped`).

### What submit-api does per project

- Fetches `GET {CONDITION_API_BASE_URL}/api/reports/project/{epic_guid}` (approved
  reports only).
- Inserts any obligation returned for the first time into `project_reports` and
  creates one empty `Report` submission package linked via `packages.project_report_id`.
- Leaves existing obligations and their packages unchanged (no update churn).
- For an obligation no longer returned: deletes the obligation and its package **only
  if the package has no uploaded documents**; a package with documents is kept.
- A Condition API failure leaves all previously stored obligations unchanged.

### Dependency note

Each obligation is keyed on the source report id (field `id` in the Condition API
response). Until the Condition repository emits that id on the project reports
endpoint, rows without an id are skipped and logged. The Condition repository is also
responsible for returning only the currently enforceable version of each condition
(superseded conditions excluded).
