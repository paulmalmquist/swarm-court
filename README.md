# Swarm Court · Paul OS

A local-first, budget-gated agent control room for persistent coordination with intermittent Claude reasoning. It makes **ball in court** explicit: who owns the next action, why it is waiting, what evidence supports it, and which plan/code/feature is connected.

## Run it

Python 3.11+ is enough for the prototype. No Node build, cloud database, credentials, or model call is required.

```bash
git clone https://github.com/paulmalmquist/swarm-court.git
cd swarm-court
python -m src.server
```

Open **http://127.0.0.1:8765**.

State persists in `.runtime/court.sqlite3`. The service binds only to loopback.

## What is live

- Motion-enabled ownership topology with explicit current action owner
- Multiple concurrent “balls” through a persistent SQLite task ledger
- Queue filters for human, agent, and blocked work
- Clickable plan/code/feature links into real repository artifacts
- Local source viewer with SHA-256 provenance
- Local 384-dimensional hashed lexical-vector retrieval preview
- Optional local Qdrant + FastEmbed adapter for work-side validation
- Fail-closed Claude worker skeleton with one-slot concurrency and budget gates
- Synthetic handoff simulation with stale-version rejection and audit events
- Responsive dark-mode interface with reduced-motion support

## Validate

```bash
python -m unittest discover -s tests -v
python scripts/api_check.py
```

Current public build validation: **23 core tests + 12 local HTTP checks passed**, and `web/app.js` passes JavaScript syntax validation.

## Deliberately not connected

Claude execution defaults **OFF**. No Relativity/company systems, Jira, BigQuery, QMS, Confluence, credentials, production deployments, or proprietary data are present in this public repository.

The example tasks are synthetic. The dashboard does not pretend work is happening when idle.

## Memory model

Repository/source-system files remain authoritative for plans, code, definitions, and evidence. SQLite is authoritative for ownership, task state, handoffs, and approvals. The vector index is a **rebuildable retrieval aid**, never the ownership or authorization source of truth.

The default prototype retrieval is a local hashed lexical-vector implementation, not pretrained semantic embeddings. See [docs/VECTOR_MEMORY.md](docs/VECTOR_MEMORY.md) for the Qdrant/FastEmbed work-side path.

## Work transfer

Give [WORK_HANDOFF.md](WORK_HANDOFF.md) to your work Claude. It is designed to discover the real Paul OS directories, existing vector service, scheduler, governed sources, and permissions before replacing any synthetic connection.

## Budget stance

Always-on monitoring is not always-on inference. The proposed production shape uses deterministic observers, batching, one bounded Claude execution slot, compact retrieval packets, finite retries, and **no automatic paid/API fallback**.

Verify the actual work-seat billing mode and egress policy before enabling unattended model execution.
