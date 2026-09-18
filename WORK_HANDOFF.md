# Work Claude handoff · Swarm Court

You are integrating a local, budget-friendly agent coordination layer into Paul's real Paul OS. Preserve existing working systems. This package contains a tested local UI/ledger/retrieval prototype, not a connected production swarm.

## Non-negotiable constraints
Use the approved WORK Claude account. No personal subscription, no account-token extraction, no shared-seat model gateway, no automatic API fallback. Spend is not assumed to be free. No Supabase. Keep the vector index and embeddings local. Preserve existing Markdown/skill directories as authoritative. A local index does not make Claude inference local: enforce approved egress before sending excerpts. Do not send prohibited company data.

Deliver a polished, responsive, motion-enabled node readout of ball in court, with real plan/code/feature/evidence links. Ownership must come from explicit task records and accepted handoffs, not model inference or vector similarity. Unknown and disconnected must stay visible. No pretend metrics, fake live activity or fabricated links.

## First: discovery without mutation
Read existing CLAUDE.md instructions. Inspect only explicitly authorized Paul OS/project roots. Inventory the existing scheduler, vector DB, Context Registry, agents/skills, promotion/evaluation rules, app registry, local embedding model and dashboard. Do not assume this project's relative paths are actual work paths. Write `WORK_DISCOVERY.md` with verified locations, versions, permission boundaries, reuse decisions and unresolved items. Use WORK-CONNECT markers to identify substitutions.

Verify whether the work seat is Team, seat-based Enterprise or consumption-billed Enterprise; confirm Claude Code entitlement, admin policy for unattended use, model availability, usage-credit settings and available provider spend controls. Authentication alone does not verify billing. Keep execution_enabled=false until all gates pass. Never change organization billing settings yourself.

## Build order

### Gate A · observable without inference
Integrate an artifact/feature registry using actual paths and URLs. Reuse SQLite state or existing equivalent; keep artifact content in files. Map this UI into the existing dashboard or run it locally. Replace synthetic examples only with explicitly sourced records. Add node -> task -> owner -> next action -> plan -> code -> feature -> evidence links. Preserve versioned citations. Ensure keyboard and reduced-motion operation.
Acceptance: every source link resolves or is marked missing, startup makes zero Claude calls, page motion does not invent work, and full task state survives restart.

### Gate B · local semantic memory
Reuse the local Qdrant/registry if available. Replace the lexical preview with tested Qdrant + cached approved local embeddings. Start with allowed Markdown/skills/plans and selected code symbols. Enforce source ACL/classification/lifecycle, hash-based incremental updates, deletion/revocation, exact-ID/FTS retrieval, semantic retrieval and source revalidation. Never put task ownership in the vector DB.
Acceptance: pass known-answer/paraphrase/symbol/revoked/stale/missing-source retrieval tests; model inference and indexing function with outbound network blocked; provenance opens the correct source lines/version. Report backend degradation truthfully.

### Gate C · deterministic observation and reliable dispatch
Start with only Pipeline Sentinel, Governance Agent and Knowledge Librarian. Observe approved metadata/local changes; do not poll Claude. Add coalescing, idempotency, atomic leases, heartbeats, a transactional event outbox, bounded backoff, retry/hop caps, dead letters and crash recovery. No self-reenqueuing loop without new evidence. Pending handoff keeps the original owner until acceptance. Preserve an accountable human for each task.
Acceptance: duplicate signals cause one logical incident; crash/restart never loses a task or double-applies a side effect; permission and capacity failures do not spin; idle means zero inference.

### Gate D · bounded work Claude
Use native approved Claude Code invocation; do not proxy tokens. Verify installed flags and managed settings. Start with one worker, 12 dispatches/day, 3 turns, 180 seconds and small context packets. Use deterministic tests as the default critic. Validate structured outputs and exact evidence references. Keep proposals read-only. No production commits/PR publication/deployment/certification or external messages without explicit authorization.
For allowance-based seats, confirm paid extra usage cannot silently activate. For consumption-based seats, require approved provider-side spend control and a conservative single-run ceiling before enabling. Fail closed on unknown billing, auth failures, exhausted capacity or loss of usage visibility where needed. Counts are not dollar limits. No automatic fallback.
Acceptance: simulated limit/timeout/auth/invalid-output tests stop dispatch; normal interactive use keeps usable capacity; cost readout separates estimates, observed usage and billed amounts.

### Gate E · work pilot and promotion
Run in shadow/read-only mode. Measure useful findings, false positives, source accuracy, stale citations, owner correctness, blocker age, execution time, input size and marginal cost. Calibrate dispatch caps using measured work, not invented token equivalents. Self-improvement proposes versioned candidates and evaluations; human promotion remains required. Add Jira/Application Auditor/RDF-Telemetry roles only after the first three are useful and approved.

## UI acceptance
The primary question is WHO HAS THE NEXT ACTION, not how many colorful agents exist. Stable layout; accepted-handoff packet animation; active-worker pulse; human decision halo; permission/capacity/stalled states; no idle animation presented as work. Click a node to open its current task, plan, code, evidence and feature. The summary supports multiple balls for concurrent leaf tasks. An unassigned approver stays visibly unassigned.

## Required final work-side deliverables
Verified discovery manifest; reuse/integration diff; tested source registry; local retrieval index and evaluation report; supervised worker with budget gates; persistent ownership ledger and audit trail; live dashboard with truthful timestamps; operational runbook; backup/restore and kill-switch test; explicit remaining coverage gaps. Do not claim company integration or operational autonomy until tested against the actual approved environment.
