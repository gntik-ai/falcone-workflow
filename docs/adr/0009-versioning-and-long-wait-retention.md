# ADR-0009: Pinned versions, long-wait retention and native run migration

Status: Accepted (2026-10-30)

Accepted by the operator on 30 October 2026 as written. The explicit R3 approval recorded that day names ADR-0003, ADR-0007, ADR-0010 and ADR-0011; whether it also covers this ADR's native live-run migration (DSL-06) awaits operator confirmation.

## Context

[design.md, Operator decisions (2026-10-30)](../design.md#operator-decisions-2026-10-30) establishes multi-month waits and opt-in, versioned compensation (D8). [architecture.md, Data model and invariants](../architecture.md#data-model-and-invariants) pins plans and interpreter metadata. FR-DSL-05, FR-DSL-06, FR-DSL-11, FR-ACT-06 and FR-OPS-03 affect DSL-03 (#18), DSL-06 (#54) and OPS-02 (#44).

## Decision

Propose pinning each run to immutable definition, compiled-plan hash, interpreter, CEL library/limits, adapter contracts and policy versions. Children use authorized explicit definition versions. Publishing a new definition or deploying a new interpreter does not alter open runs. Unsupported historical versions remain safely parked with an incident; upgrades must not remove the versions needed to execute them.

Let `W_max` be the maximum permitted wait, set by the Falcone product owner. This ADR fixes no value: it must support multi-month waits and current approvals under D8. Retain interpreter artifacts and definitions for at least the longest permitted remaining wait and for as long as any open run still references them; expiry of a nominal retention window never authorizes deletion of a live dependency. Include paused runs, children, approvals and compensation versions in reference checks. Closed-run history and erasure follow ADR-0012 independently.

Use expand/contract schema upgrades that support retained interpreters and bounded drain. Publish an artifact/reference inventory and rollback limits before deployment. When artifact retention cannot be met, park affected work or obtain an explicit migration plan; do not substitute current semantics.

DSL-06 (#54) is native-to-native only. Propose a dry-run-validated node-occurrence mapping to another published version of the same flow, rejecting missing mappings for active tasks, timers or approvals and changes to node type or scope. Apply atomically per run under the expected revision with actor, reason and old/new versions in audit. Preserve absolute timer due times, credential lineage and quota reservations. Quiesce dispatch and account for outstanding leased work so old attempts cannot commit against migrated state. This does not convert Temporal histories or authorize live transfer across engines.

Acceptance requires R3 review with a second reviewer (Security engineers) and explicit operator approval for live-run migration. Product approval of `W_max` and operational retention capacity remain separate gates.

## Alternatives

- Always using the latest interpreter changes open-run semantics.
- A fixed short retention window violates D8 and may strand months-long waits.
- Generic Temporal history conversion contradicts the D3 migration boundary.

## Consequences

Long waits create multi-version operational obligations. Workflow/runtime maintainers own version compatibility; SRE/platform team budgets retained artifacts and rollback support. Acceptance evidence must cover rolling versions, suspended runs, a stale migration revision and unmapped active work without waiting months in wall time.

## Operator resolution (2026-10-30)

`W_max` is 12 months (finding F08): the maximum permitted wait for waits, approvals and timers. Interpreter and definition versions, and anything else a live run pins, are retained for at least 12 months after the last run that pins them closes, and never while an open run still references them. FR-ACT-06, FR-DSL-06 and FR-OPS-03 carry the value.
