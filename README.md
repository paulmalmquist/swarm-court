# Swarm Court · Paul OS
A local-first, budget-gated agent control room. Synthetic examples, real links to the included plans and source, explicit ownership, motion-driven handoffs, persistent task ledger, and local retrieval.

## Start the prototype
Python 3.11+; no pip install, Node build, cloud hosting, or credentials required.

```bash
python -m src.server
```
Open http://127.0.0.1:8765. State persists in `.runtime/court.sqlite3`. The server binds only to loopback. Run `python -m unittest discover -s tests -v` to test. A standalone preview is in `Swarm-Court-Preview.html`; open it in a desktop browser for the interactive preview. Its state is browser-memory-only, unlike the server.

## What works
Animated node topology; clickable tasks and nodes; current and accountable ownership; queue, memory, feature, and budget views; source/plan viewer with line numbers and source hashes; local hybrid retrieval; auditable simulated handoffs; pause/resume; state persisted across server restarts; optimistic version checks; an allowlisted artifact registry.

## What is deliberately not connected
Claude execution defaults OFF. No company systems, repositories, credentials, Jira, BigQuery, QMS, or production deployments are connected. The example tasks and owner durations are synthetic, not observations of your work. The source links open actual files in this package; no company links are invented.

Default retrieval is a **384-dimensional hashed lexical-vector preview**, stored locally in SQLite and combined with keyword scores. It is not a pretrained semantic model and must not be represented as Qdrant or semantic quality. The optional production adapter uses local Qdrant + FastEmbed; see `docs/VECTOR_MEMORY.md`. That adapter is included but not integration-tested here, because its dependencies/model were unavailable in this environment.

## Work transfer
Read `WORK_HANDOFF.md` in your work Claude. Inspect your actual Paul OS paths before integrating. Reuse an existing approved local context registry/vector service. Do not create a competing source of truth. All work-specific substitutions are marked `WORK-CONNECT:`. The application does not publish work-system changes or deploy a hosted service.

## Budget stance
Always-on monitoring is not always-on inference. One Claude slot, deterministic event filtering, batch dispatch, compact retrieval packets, finite retries, and stop-on-limit. A work subscription does NOT necessarily imply prepaid inference: usage-based Enterprise plans bill consumption. Verify the actual organization billing mode before enabling any model calls.

## Public GitHub publication
See [PUBLISH_GITHUB.md](PUBLISH_GITHUB.md). The prepared release includes a hash-verified publishing helper for `paulmalmquist/swarm-court`. From a fresh extraction, run `python scripts/publish_github.py`; Git and GitHub CLI are required. Repository creation and push occur only when you run that command successfully.
