# PLAN-001 · Governed metric certification
Status: synthetic example / awaiting Paul approval
Action owner: Paul
Accountable owner: Paul
Pending next owner: System features (synthetic route only)

## Decision required
Approve a read-only review of a proposed metric-definition change. Approval in the demo changes only its local task record. It never certifies a real metric or writes to BigQuery.

## Scope
Inspect the approved model definition, source lineage, acceptance tests and existing certification evidence. Identify whether a changed column alters the metric contract. Retrieve exact evidence with path, line range, file hash and version.

## Acceptance criteria
Every claim resolves to a live source artifact. The previous certification remains unchanged. The proposal includes a test plan, affected features and a rollback/rejection rationale. Domain-owner approval is mandatory for a real certification.

## Links
Implementation: src/ledger.py
Retrieval: src/retrieval.py
Feature: /#/feature/certification
Budget policy: config/runtime.json

## Work connection
WORK-CONNECT: discover the actual dbt model, governed view, evidence store, metric owner and feature route inside work Paul OS. Do not invent a BigQuery project or certificate ID.
