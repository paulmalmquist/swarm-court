# Budget · stop rather than silently spend

## Verify billing first
A work Claude seat can be Team, seat-based Enterprise or usage-based Enterprise. They are not economically equivalent. Anthropic's current documentation says consumption-based Enterprise use is billed at API rates. Do not infer a prepaid allowance from SSO, the phrase subscription, or a successful login.

The current Help Center update says Claude Agent SDK and claude -p continue drawing against plan usage limits while a previously announced separation is paused. This is not a perpetual price/terms guarantee. Recheck before deployment. Use the native work login; never extract or proxy account tokens or offer a shared inference gateway on one person's seat.

## Target economics (not a quote)
Existing approved host: target $0 incremental hosting/vendor subscription, excluding electricity, administration, storage, source API costs and any billed Claude consumption. Local vector storage and CPU embeddings add resource load, not external embedding API charges. Do not purchase hardware or cloud services for the pilot.

Start with 12 bounded dispatches/day, one concurrent process, 3 turns/dispatch, 180-second wall limit, 16,000 input characters, one retry, no subagents, 15-minute batching and no discretionary overnight inference. These are conservative operational defaults to measure, not a guarantee of fit in an allowance. The character limit is a byte/context proxy, not a token cap.

If included allowance is confirmed: preserve interactive capacity by count/time caps and require usage credits to be disabled or restricted by the admin. If consumption-billed: automation remains off until an explicit per-user/group provider spend control and approved budget are in place. A suggested pilot ceiling is $20/month only if the business approves it; it is a cap proposal, not a predicted bill. Provider caps can overshoot on a final request; retain headroom and bound single runs.

## Never fake the dashboard's cost meter
Display billing mode, verified-at time, local dispatch count, observed input/output usage when available, configured operating caps, pending budget-paused jobs, and freshness of provider data. Unknown remaining quota is UNKNOWN, not a fabricated percentage. A CLI/API-equivalent cost field is not necessarily incremental subscription spend. Show estimates separately from billed values.

No automatic switch to an API key, gateway, alternate account, model or paid credits when capacity is exhausted. No account rotation. Pause, preserve tasks, expose the next eligible time if known, and notify the owner once.

## Useful efficiency rules
Deduplicate incidents before retrieval. Re-embed only content-hash changes. Retrieve a handful of source chunks; read exact referenced code rather than whole repos. Use deterministic tests as critic for low-risk jobs. Invoke a second LLM reviewer only for ambiguity or consequential proposals; LLM agreement is not independent proof. No continuous inter-agent conversation. The UI and vector index do not need Claude running.
