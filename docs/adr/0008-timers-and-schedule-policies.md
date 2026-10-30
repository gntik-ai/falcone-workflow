# ADR-0008: Durable timers and explicit schedule calendar policies

Status: Accepted (2026-10-30)

Accepted by the operator on 30 October 2026 as written.

## Context

[architecture.md, Data model and invariants](../architecture.md#data-model-and-invariants) stores timers and schedule occurrences durably. [migration.md, Rollout](../migration.md#rollout) requires ownership epochs and bounded catch-up during cutover. FR-TIM-01, FR-TIM-02, FR-TIM-04, FR-TIM-05, FR-TIM-06, FR-TIM-07 and FR-TIM-08 affect TIM-01 (#25), TIM-02 (#26) and TIM-03 (#27).

## Decision

Propose persisting each timer's due UTC instant before arming it. Absolute or CEL-computed waits with an explicit IANA time zone are evaluated once, under the pinned interpreter, then stored; restarts do not recompute their due time. Resolve signal, timeout and cancellation by the first eligible transaction to commit under the expected run revision; retries observe the recorded winner. Fire each logical timer into workflow state at most once.

Preserve apiVersion v1.0 cron evaluation in UTC, original cron text, schedule identities and inventoried effective catch-up defaults. Preserve the eight overlap names `skip`, `allow`, `allow_all`, `buffer`, `buffer_one`, `buffer_all`, `cancel_other` and `terminate_other`, normalizing aliases only as proven by CON-01 fixtures; default remains `skip`. Do not infer alias equivalence from spelling.

For the additive time-zone-aware field, store the IANA zone and calendar-rule version: a nonexistent local time runs once at the next valid instant; an ambiguous local time runs once at its first occurrence. Derive nominal UTC instants deterministically and deduplicate by tenant/workspace, schedule ID and nominal UTC instant. Pin the calendar/time-zone data needed to reproduce occurrence calculation; changes require an explicit versioned policy.

Persist start/end bounds, bounded jitter, maximum action count and pause-on-failure policy. Audited pause/resume notes and trigger-now follow FR-TIM-08; pausing leaves admitted runs alone, and trigger-now bypasses catch-up but applies overlap unless explicitly overridden. Backfill is distinct from catch-up: dry-run [start, end), reprocess mode, bounded occurrences, one active backfill per schedule, separate concurrency cap, pause/cancel and audit. Ownership epoch checks fence all admission paths during backend handover.

## Alternatives

- Process-local timers lose waiting work on restart.
- Host-local time or implicit DST defaults change outcomes across deployments.
- Unbounded catch-up or backfill can flood admission and duplicate effects.

## Consequences

Release/QA maintainers must fixture DST gaps/folds, cron aliases, pause, overlap, manual triggers and ownership races. Policy bounds and timer scan/capacity numbers are provisional pending M0 measurement; catch-up defaults come from deployed legacy inventory, not invented values. Current waits and approvals remain supported under D8.
