# PLAN-003 · Application query audit
Status: synthetic example / waiting for permission
Action owner: Access approver (unassigned in demo)
Accountable owner: Paul

## Blocker
The permitted registry does not yet contain an approved read-only BigQuery metadata adapter. Do not guess the approver, bypass permissions, or inspect business rows.

## Scope
Compare an application's declared governed sources with its query templates, contracts and source inventory. SQL analysis alone is not proof of runtime row-level security. Validate actual execution identity, authorized views, dataset permissions and query job evidence through approved adapters.

## Acceptance criteria
A finding connects the app feature to exact SQL/code, declared contract, lineage and permission evidence. Unavailable checks are visibly unknown, not green. Production writes and certification awards remain human-gated.

## Links
Budget/permissions: config/runtime.json
Feature: /#/feature/query-audit
WORK-CONNECT: actual application route, source repo commit, BigQuery identity and system owner must be discovered at work.
