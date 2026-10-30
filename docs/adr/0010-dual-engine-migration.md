# ADR-0010: Dual-engine routing, drainage and schedule cutover

Status: Proposed

## Context

[migration.md, Rollout](../migration.md#rollout) and [design.md, Purpose and scope](../design.md#purpose-and-scope) preserve Falcone's facade while existing Temporal runs finish on Temporal (D3). FR-CON-04, FR-MIG-01, FR-MIG-02, FR-MIG-03, FR-MIG-04, FR-MIG-05 and FR-TIM-05 affect CON-02 (#14), MIG-01 (#46), MIG-02 (#47), MIG-03 (#48) and TIM-03 (#27).

## Decision

Propose durable, tenant-scoped backend locators owned by the Falcone facade. Select a backend for new starts by an approved cohort and persist that choice with start idempotency before acknowledging admission. Route every later operation to the recorded backend, including retries after a lost response; backend outage yields a retryable unavailable response, never fallback execution on another engine. Never infer ownership from caller-supplied ID syntax.

Inventory actual deployed versions, callers, open runs, pinned workers, schedules and credentials before selecting a cohort. Use isolated differential fixtures; never shadow live effects. Keep existing Temporal runs, workers and required contracts on Temporal until drained. No generic history converter or automatic transfer is proposed. Any exceptional application-level checkpoint transfer requires a separate validated plan, deduplicated effects and a recorded cutover boundary.

Transfer schedules and trigger admission using a durable ownership epoch: pause old admission, fence stale owners, reconcile already admitted occurrences/events, then enable the new owner. Check the epoch on every admission path, including manual triggers and backfill. Use explicit bounded catch-up for the gap under ADR-0008; do not run both owners optimistically.

Rollback changes future admission cohorts and requires the same fenced schedule handover protocol; it does not move existing native runs to Temporal or replay their effects. Retain native routing and workers for those runs. Retirement requires an empty required caller/run/schedule/credential inventory, or explicit approved retention exceptions with maintained access. This ADR does not authorize deletion of any deployment.

Acceptance requires R3 review with a second reviewer (Security engineers) and explicit operator approval for live-run migration and lineage/routing boundaries. Falcone integration team owns facade changes; Workflow/runtime maintainers supply native contracts; Release/QA maintainers provide cutover/rollback evidence.

## Alternatives

- Immediate migration of all live runs violates D3 without an accepted application-specific plan.
- Routing by ID heuristics or fallback on outage can create duplicate runs and tenant-boundary mistakes.
- Reverting all routing after a canary strands native runs already admitted.

## Consequences

Both engines may operate for months and require parallel maintenance. API compatibility remains bounded by inventoried Falcone semantics, not raw Temporal SDK compatibility. Unqualified native profiles or contract gaps block the relevant cohort rather than changing accepted decisions.
