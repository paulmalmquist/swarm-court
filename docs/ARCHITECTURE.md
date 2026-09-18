# Architecture · persistent coordination, intermittent reasoning

## Three kinds of truth
1. Files and approved source systems are authoritative for plans, code, definitions and evidence.
2. SQLite is authoritative for tasks, ownership, handoffs, leases, approvals and audit events.
3. Qdrant is a rebuildable semantic search index, not a workflow engine and not an authorization system.

The UI graph is derived from the ledger and explicit typed relationships. Do not draw an embedding-neighbor graph and call it workflow ownership.

## Minimal production deployment
One approved workstation or existing always-on internal host. One Python service. SQLite WAL. Existing local Qdrant or a loopback-bound Qdrant container. CPU embeddings. Local browser UI. One Claude Code execution slot. No Kubernetes, Redis, hosted vector service, GPU or extra agent seats for the pilot.

## Event flow
Approved local observer -> dedupe and coalescing -> durable task -> local retrieval -> context packet -> budget and egress gates -> bounded Claude Code process -> schema and deterministic evidence checks -> proposed result -> human approval where required -> accepted handoff -> UI event.

Empty queue produces zero model calls. System and ownership state remains available without Claude. Chat histories do not become authoritative memory. Save compact outcomes and indexed source artifacts instead.

## Ownership contract
Task: task_id, project_id, status, action_owner_id, accountable_owner_id, pending_owner_id, waiting_on_type, reason, next_action, entered_at, lease_expires_at, heartbeat_at, version, priority, artifact_ids, evidence_ids, feature_ids, source_version, budget_class, correlation_id.

One actionable leaf task has one current action owner. A project may have several parallel leaf tasks and therefore several balls. The accountable human remains stable unless explicitly reassigned.

Handoff proposed is not handoff accepted. Keep the original owner until the recipient accepts or an authorized deterministic routing rule commits the transfer. Store both records with a monotonic event ID. Commit task state and outbox event atomically. Use compare-and-swap task versions. A worker lease expiring marks an uncertain/stalled run; it does not silently prove failure or success.

## States
QUEUED, RUNNING, WAITING_HUMAN, WAITING_PERMISSION, WAITING_CAPACITY, BLOCKED, STALLED, COMPLETED, CANCELLED, DEAD_LETTER. Show next_action and waiting reason, not only colors.

## Reliability work before real unattended operation
OS supervisor (systemd / launchd / Windows Task Scheduler as appropriate); single-instance guard; atomic claims; bounded leases and heartbeats; idempotency keys; exponential backoff with jitter; finite retry/hop counts; dead-letter queue; crash recovery; transactional outbox; circuit breaker; backups and restore tests; daily human exception digest.

The included prototype persists simulated handoffs and rejects stale versions. It is NOT a completed unattended production scheduler. The worker is an opt-in, budget-gated CLI skeleton, not a validated work integration.

## Existing Paul OS
WORK-CONNECT: inspect the actual numbered skill/agent directories, existing scheduler, registries and UI before choosing locations. Respect existing CLAUDE.md files. This portable project does not assume it knows your work filesystem.

## Data boundary
Embedding and search run locally. Approved excerpts sent to work Claude still leave the machine for model inference. Work-seat authorization is not permission to transmit every repository or aerospace data class. Enforce the organization's approved classification/egress controls; prohibited sources stay local and unavailable to the cloud worker.
