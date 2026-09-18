# Visual specification · useful motion, not a screensaver

## Reading order
At a glance: Who needs to act? Why? What exact action? What can I open to verify it? Is the system actually connected and current?
The primary surface is a stable topology with a clearly outlined action-owning node. A selected task shows its route and owner detail. A side panel shows the current ball, accountable person, time in state, next action and evidence links.

## Views
Court: stable nodes, task route, accepted handoff animation.
Queue: all actionable leaf tasks, explicit reasons, filters for Mine/Agents/Blocked.
Memory: local search, source excerpts, file hashes, backend identity and provenance.
Features: feature -> implementing code -> plan -> acceptance criteria -> owning task.
Budget: counts, configured caps, real billing mode or UNKNOWN, reason dispatch is disabled.

## Motion vocabulary
A packet traverses an edge once when an accepted handoff is recorded. A subtle pulse means an active task state, not throughput. Amber halo means a human decision. Red boundary means blocked. Gray dashed edges are inactive or awaiting permission. Completed handoffs fade to a thin evidence trail.
No permanently racing particles implying work when idle. No background polling of Claude just to animate. Use UI events/heartbeats to distinguish live, disconnected, replay and synthetic modes. Show last data timestamp and missed-heartbeat age. Stop motion when tab is hidden. Respect prefers-reduced-motion and offer a persistent manual switch. Preserve keyboard navigation and a non-graph table view.

The included prototype has a labeled synthetic handoff demo, selected-owner halos, pause/motion controls and real artifact viewing. It uses lightweight SVG/CSS rather than a 3-D engine. Work production can retain this rendering or migrate to React Flow when graph manipulation actually requires it.

## Link contract
Every link originates in a verified artifact/feature registry: stable artifact ID, kind, repo-relative path, source hash, optional commit, line range, and optional approved system URL. The local viewer resolves allowlisted IDs; never accept arbitrary paths or URL schemes. External Git links should use immutable commits where available. VS Code links require the real discovered path and an explicit user click. Missing/unverified targets display NOT CONNECTED, never fabricated URLs. Recheck ACLs server-side on every open.
