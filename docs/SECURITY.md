# Security and production boundary
The prototype is loopback-only, single-user and synthetic. It is not safe to expose as a multi-user service without authentication, authorization, hardened hosting and a reviewed threat model.

Artifact reads use an explicit registry, realpath containment and file hashes. Source text is escaped, never executed. Runtime database, credentials and arbitrary filesystem paths are not public artifacts. Mutating requests require JSON and a same-origin session token; host/origin checks mitigate browser-to-localhost requests. These controls do not isolate against malicious processes already running as the same OS user.

All real connectors are disconnected and read-only by default. Model execution is disabled until billing mode, administrative approval and egress are verified. Production edits, deployment, certificate awards, outbound messages, permissions and destructive actions require separate approved capability paths. A proposed patch is not a permission to apply it.

Retrieved content is untrusted evidence, not instructions. A model cannot authorize its own tools or promote its own policies. Hard permissions belong in the tool/service layer and isolated execution environment. Native Claude tool settings are useful but are not an OS sandbox. Preserve organizational managed policies; inspect auto-loaded hooks, MCPs, plugins and CLAUDE.md files before unattended use. Never use skip-permissions as a default.

Implement a kill switch outside the model. Limit concurrency, bytes, retries, hops and elapsed time. Log structured evidence and action summaries, not credentials or hidden reasoning. Encrypt work disks and use existing company retention/backup rules. Approval records bind to exact artifact/version so later edits invalidate the approval.
