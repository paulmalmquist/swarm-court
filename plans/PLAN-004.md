# PLAN-004 · Pipeline freshness investigation
Status: synthetic example / queued for the next reasoning slot
Action owner: Pipeline Sentinel
Accountable owner: Paul

## Signal
An approved deterministic freshness test found a stale synthetic data product. No real production data was queried.

## Procedure
Deduplicate by source/version/failure signature. Collect log excerpts and metadata once. Retrieve relevant runbooks and prior approved incident summaries. Classify root-cause hypotheses separately from observed evidence. Produce a bounded recommendation, not an unattended production repair.

## Completion
The proposed next action is explicit; all supporting evidence is linked; known coverage gaps remain visible; resolution is independently checked. If credentials are unavailable, assign a WAITING_PERMISSION action instead of retrying indefinitely.

## Links
Observer: src/observer.py
Worker: src/worker.py
Feature: /#/feature/pipeline-health
WORK-CONNECT: source health endpoint, read-only identity and freshness definitions.
