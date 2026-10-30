# ADR-0004: Shared outbox, inbox and lease fencing consumption

Status: Proposed

## Context

[architecture.md, Repository placement and shared contracts](../architecture.md#repository-placement-and-shared-contracts) assigns shared primitives to the Falcone module built by falcone-serverless story STO-03 (D4). [architecture.md, Data model and invariants](../architecture.md#data-model-and-invariants) requires atomic workflow progress. FR-EVT-01, FR-EVT-02, FR-DUR-02, FR-DUR-03 and FR-DUR-04 affect EVT-01 (#28), DUR-01 (#19) and DUR-02 (#20).

## Decision

Consume the shared module rather than create an engine-specific implementation. **Interface assumption to confirm with the owners:** the authoritative repository/path, exported API, version and migration ownership for STO-03 are absent from this snapshot. The following are required capabilities to validate, not factual signatures or a new contract:

- Participate in the caller's PostgreSQL transaction in the engine's separate database so state and outbox, or inbox deduplication and transition, share a commit boundary.
- Preserve tenant/workspace scope, stable event/deduplication identity and bounded relay claims; expose retryable publication and retention sufficient for redelivery.
- Claim, renew and complete work with database time, expiring leases and monotonic fencing generations; reject expired or superseded generations atomically with progress.
- Permit durable scans after lost notifications, and expose migration/version compatibility for multiple engine replicas.

The Falcone integration team coordinates confirmation with the STO-03 owners in Falcone/falcone-serverless; Workflow/runtime maintainers record the pinned source and contract tests before integration. `ctr-worker-execution-api` and `ctr-job-checkpoint` are also interface assumptions to confirm with their owners, covered by ADR-0006; they do not prove the shared module's transaction compatibility.

If delivery is late or transaction participation is incompatible, keep dependent production work gated. A boundary simulator may exercise development fixtures but must be marked non-production and cannot establish durability. Escalate the gap to the owning repository; do not ship a parallel module or replace atomic writes with remote calls. Changing D4 requires a separate operator decision.

## Alternatives

- Independently implementing the primitives here conflicts with D4.
- A remote outbox write after committing workflow state loses the authoritative transaction boundary.
- Treating Kafka acknowledgement as workflow commit fails the required durable-state invariant.

## Consequences

Upstream contract delivery blocks production integration. Acceptance evidence must include commit-before-publish crashes, duplicate delivery, late completion, expired heartbeat and notification loss using the consumed module. Lease, heartbeat, connection-budget and capacity numbers remain provisional pending M0 measurement; this ADR fixes no signature or numeric default.
