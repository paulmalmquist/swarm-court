# Validation report

Validated September 18, 2026.

## Current public build

- **23 core unit tests passed**: persistence, accepted handoff audit, stale-version rejection, pause, single reasoning slot, daily dispatch cap, artifact allowlisting, symlink escape rejection, source hashes, lexical-vector retrieval, source deletion/update, observer deduplication, and fail-closed billing policy.
- **12 local HTTP checks passed**: all 23 allowlisted source artifacts resolve, local retrieval returns evidence, arbitrary paths are rejected, token/origin checks work, accepted ownership handoffs persist, stale writes conflict, pause blocks mutation, and the run makes zero model calls.
- `web/app.js` passes JavaScript syntax validation.
- No Claude/model calls, company-system calls, hosted vector services, or paid service purchases were used by these checks.

## Reproduce

```bash
python -m unittest discover -s tests -v
python scripts/api_check.py
```

## Coverage limits

The public repository is a synthetic local prototype. Qdrant/FastEmbed has not been integration-tested against the user's work environment, and the Claude worker skeleton has not been executed against the work seat. Organization billing, egress approval, actual connectors, unattended scheduling, and production permissions remain work-side gates.
