# PLAN-002 · Incremental knowledge refresh
Status: synthetic example / librarian working
Action owner: Knowledge Librarian
Accountable owner: Paul

## Goal
Index changed approved Markdown and code without re-embedding the full corpus. Keep source files authoritative. Keep embeddings, index and logs local.

## Method
Manifest approved roots. Reject secrets and generated/vendor directories. Resolve real paths to prevent symlink escape. Chunk Markdown by heading and code by symbol where possible. Store file SHA-256, Git commit, heading/symbol, line start/end, lifecycle and access scope.
Use local embeddings and one shared Qdrant service. Blend vector candidates with SQLite FTS5 exact matches. Expand only explicitly registered relationships. Re-read candidate sources and compare hashes before model use.

## Completion
Changed chunks indexed; deleted/revoked chunks removed; citations valid; recall regression tests pass; corpus and embedding versions recorded. A semantic match is a lead, not proof.

## Links
Implementation: src/retrieval.py
Production adapter: src/qdrant_adapter.py
Feature: /#/feature/memory
WORK-CONNECT: reuse the existing context registry/index if present; do not index arbitrary folders.
