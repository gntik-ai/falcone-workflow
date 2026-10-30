# ADR-0005: Bounded task dispatch and ambiguous external outcomes

Status: Proposed

## Context

[architecture.md, Task and failure semantics](../architecture.md#task-and-failure-semantics) separates fenced state commits from at-least-once effects. FR-DUR-03, FR-DUR-04, FR-ACT-01, FR-ACT-03, FR-ACT-04 and FR-HUM-09 affect DUR-02 (#20), ACT-01 (#22), ACT-02 (#23) and HUM-03 (#33). The shared module dependency remains ADR-0004, under D4.

## Decision

Propose bounded claims using short database transactions and the shared lease/fencing module. Commit the new attempt and lease generation before external I/O. Keep the operation ID stable across retries; attempt IDs and fencing generations change. Tenant/workspace, run, node occurrence and pinned adapter version accompany each authorized dispatch. Scheduler fairness consumes Falcone quota policy and cannot create cross-tenant priority privileges.

Use database time for lease expiry. Heartbeats and completions must match the current generation, expected status and an unexpired lease; a rejected heartbeat cannot resurrect the attempt. Renewal stops after terminal state or loss of authorization. Durable expiry/recovery scans remain sufficient when notifications disappear. Do not dispatch new work while PostgreSQL is unavailable. Cancellation stops new normal work, with acknowledgement, remote cleanup and terminal outcome recorded separately.

Lease duration, heartbeat interval, renewal margin, claim batch size, scan interval, connection-budget and capacity numbers are provisional pending M0 measurement (ADR-0013). The architecture's example lease is not a default. Derive task-specific settings from measured latency and the pinned queue, attempt, heartbeat and total-operation timeout policies; preserve effective apiVersion v1.0 defaults.

Before dispatch, classify each connector as idempotent-by-key, reconcilable or non-idempotent. On unknown outcome, reuse the operation key where supported, reconcile provider state where possible, or open a typed ambiguous-outcome incident that stops that path. Never blindly retry an unknown non-idempotent effect, even when attempts remain. Fencing cannot undo a remote side effect. Repair requires authorization, reason and expected revision with a side-effect preview.

## Alternatives

- Holding database locks across HTTP calls consumes scarce connections and does not make remote effects transactional.
- Notification-only recovery strands work after message loss.
- Universal automatic retries or exactly-once promises conceal irreversible duplicates.

## Consequences

Worker loss may repeat external delivery, but stale attempts cannot commit progress. Connector classification and reconciliation are required acceptance evidence, alongside late heartbeat/completion, lost acknowledgement, cancellation and DB outage fixtures. Some incidents need human resolution rather than automatic completion; this is a deliberate correctness boundary.
