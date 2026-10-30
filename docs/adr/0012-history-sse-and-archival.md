# ADR-0012: Durable history, resumable SSE and bounded archival

Status: Accepted (2026-10-30)

Accepted by the operator on 30 October 2026 as written.

## Context

[architecture.md, Data model and invariants](../architecture.md#data-model-and-invariants) defines ordered per-run events and reference payloads. [architecture.md, Typical invocation](../architecture.md#typical-invocation) projects history to the existing SSE facade. FR-DUR-05, FR-DUR-06, FR-DUR-07, FR-OBS-01, FR-OBS-02 and FR-INT-05 affect DUR-03 (#21), OBS-01 (#40), INT-03 (#39) and OPS-02 (#44).

## Decision

Propose append-only, tenant/workspace-scoped structural history committed in the same transaction as run progress. Project the inventoried node-status, log-line and stream-end frames through Falcone; persist stable per-run sequence cursors and resume from Last-Event-ID. A projection crash may replay delivery but cannot invent transitions. Stream authorization applies on retrieval and reconnection; public opaque IDs are not authority.

Bound each history segment by configured event count and byte size. Continuations keep the public run ID, link segments and preserve monotonic SSE cursor order. Separate projection lag from engine progress. Cursor expiry or missing archived data must produce an explicit compatible response established by CON-01 fixtures, never silently skip events. Closed-run retention and cursor availability must be documented together before acceptance of the retrieval contract.

Large payloads use immutable tenant-scoped object references with content hashes, quota limits and retention metadata. Verify upload before committing a reference; sweep orphan uploads after a safe grace period. Retain all objects needed by live runs, approvals, checkpoints and compensations. Missing or hash-mismatched payloads open incidents instead of returning fabricated values.

Closed runs follow per-workspace retention policy and legal holds. Authorized deletion of a closed run and its objects is audited; data-subject erasure removes payload objects while retaining redacted structural history. Keep secrets and unredacted payloads out of history, SSE and lifecycle events. Confirm provider behavior through the configured Falcone S3 adapter, not a provider-specific engine API.

Coordinate database PITR with object versions and credential recovery dependencies; reconcile external effects before resuming restored dispatch. Retention thresholds, inline limits, archival batches and connection/capacity budgets are provisional pending M0 measurement and policy approval, with no deletion of live dependencies to meet a storage target.

## Alternatives

- In-memory SSE cursors cannot survive restart or reliably represent committed history.
- One unbounded history document makes long waits and high-transition runs operationally unsafe.
- Archiving without reference/restore coordination can preserve events while losing their required inputs.

## Consequences

Workflow/runtime maintainers own event ordering and segment reconstruction; Falcone integration team owns compatible SSE presentation; SRE/platform team owns archival and restore evidence. Product retention/erasure policy and the actual object provider remain owner gates, not decisions inferred from this proposal.
