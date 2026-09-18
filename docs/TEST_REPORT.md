# Validation report

Validated September 17, 2026 (local user date).

## Passed
- 23 core unit tests: persistence, accepted handoff audit, stale-version rejection, pause, single slot, daily dispatch cap, artifact allowlisting, symlink escape rejection, source hashes, lexical-vector retrieval, source deletion/update, observer deduplication and fail-closed billing policy.
- 12 local HTTP checks, including every one of the 23 registered source artifacts resolving with matching hashes, local hybrid retrieval, token/origin enforcement, accepted ownership handoff, version conflicts and persistence across a fresh ledger instance.
- 18 standalone UI behavior checks in Chromium: node interactions, plan/code viewing, feature route, source-line citations, search, filters, pause, handoff, audit event, motion toggle, explicit unknown billing and mobile overflow check.
- No JavaScript runtime errors in the tested UI paths.
- No Claude/model calls, company-system calls or paid service purchases.

## Important coverage limits
The browser environment blocked direct navigation to localhost. UI tests therefore rendered the standalone HTML in memory; the real server/API was tested separately over local HTTP with Python. This is not a claim of a fully integrated browser-to-server end-to-end test.

The Qdrant/FastEmbed adapter could not be integration-tested because optional dependencies and model weights were unavailable in this environment. The working default is explicitly labeled lexical-vector preview, not pretrained semantic retrieval. The standalone HTML uses a simpler local keyword preview. Neither is a substitute for work-side semantic relevance/ACL tests.

The Claude CLI skeleton was not executed against a work seat. Organization billing, installed CLI flags, managed settings, egress, authentication, genuine quota visibility, real connectors and unattended production scheduling remain work-side gates. No task updates or artifacts were sent to a work system.

## Reproduce
```bash
python -m unittest discover -s tests -v
python scripts/api_check.py
```
UI checks additionally require an approved Playwright installation and Chromium; adapt the executable path in scripts/browser_check.py. The application itself has no third-party Python or JavaScript dependencies. Optional semantic dependencies are separate.

See test-results/unit-report.txt, api-report.json and browser-report.json for detailed results. Screenshots are in test-results/.
