# Local vector memory

## Production choice
Reuse the existing local Paul OS vector service if present. Otherwise use one shared local Qdrant service and local CPU FastEmbed with an approved cached embedding model. No Supabase, hosted vector database, external embedding API or per-agent vector instance.

The proposed starting model is BAAI/bge-small-en-v1.5 (384 dimensions) for cheap text retrieval. Treat it as a baseline to evaluate, not evidence that it is ideal for your code or terminology. Preserve exact identifiers with SQLite FTS5. Consider a code-specific model only after measuring retrieval failures. Match the existing model/version/dimension if reusing an index.

## What to index
Approved skill Markdown, plans/decisions, concise successful run summaries, runbooks, schema/metric contracts, feature manifests and selectively approved code symbols. Not raw telemetry timeseries, complete QMS exports, secrets, credentials, binaries, virtual environments or every log line. Store pointers and summaries to governed systems instead of copying their entire contents.

## Metadata per chunk
Stable artifact ID; project ID; relative source path; Git commit/content hash; heading/symbol; line start/end; source system ID and version; lifecycle; approved scopes; classification; observation time; embedding model/revision. Revalidate source versions before using a citation. Approval/lifecycle and authorization are filters, not a learned score.

## Retrieval
Apply the authenticated principal's allowed source set. Retrieve semantic and FTS candidates. Fuse ranks, deduplicate, diversify across files, expand at most one hop of explicit evidence relationships, and re-read originals. Reject stale/revoked chunks. Send a bounded evidence packet to Claude only after egress approval. Never infer ownership, feature membership or authorization from vector proximity.

For single-user local use, the allowlisted registry is the boundary. A shared dashboard requires real authentication and source-ACL enforcement in both search and artifact reads. Do not assume that hiding cards in the UI enforces access.

## Reference memory sizing
100,000 x 384 x 4 bytes = 153,600,000 bytes (about 146.5 MiB) for float32 vectors alone, BEFORE graph index, text payloads, metadata and model/runtime overhead. Budget system RAM/disk from measurement, not this raw vector size. No GPU is required by this proposed CPU design.

## Included implementation
`src/retrieval.py` is a dependency-free, persistent **lexical-vector preview**: stable token hashing, cosine similarity and keyword rank fusion. It supports source-backed chunks and exact file hashes. Its UI labels are intentionally not semantic.
`src/qdrant_adapter.py` implements a local-only Qdrant/FastEmbed candidate adapter for work-side validation. Optional dependencies are in requirements-vector.txt. Pin tested versions and an approved model revision on the work machine before unattended use. A real semantic index was not run in this environment.

## Work-side activation
1. Inspect any existing registry/index before installing another service.
2. Acquire approved model weights through approved processes, cache them locally, record model revision/hash, and test with network access blocked. The first model acquisition may require a download; inference need not.
3. Run Qdrant on loopback only, with authentication and an approved image version/digest. Reuse the actual configured endpoint. Do not expose its default unauthenticated port to the network.
4. Install and pin the optional packages in an isolated environment. Keep the shipped lexical preview active until semantic integration passes.
5. Evaluate at least 20 known-answer queries: exact code symbol, plan paraphrase, obsolete decision, contradictory evidence, revoked file, duplicate chunks and missing source. Verify citations, ACLs, deletion, rebuild/restore and offline operation.
6. Replace retrieval via the adapter and accurately show backend, model, freshness, source counts and degraded status in the UI. Never silently switch to cloud embeddings.
