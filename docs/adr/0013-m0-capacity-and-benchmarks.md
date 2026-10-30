# ADR-0013: M0 capacity baseline and qualification benchmarks

Status: Proposed

## Context

[architecture.md, Capacity and service objectives — proposals, not promises](../architecture.md#capacity-and-service-objectives--proposals-not-promises) distinguishes workflow workload from earlier serverless estimates. [migration.md, Rollout](../migration.md#rollout) requires M0 inventory on current Temporal staging. FR-OBS-03, FR-OBS-05, FR-OBS-06 and FR-MIG-01 affect MIG-01 (#46), OBS-02 (#41), OBS-03 (#42) and OPS-03 (#45).

## Decision

Propose an M0 evidence package owned by SRE/platform team and Release/QA maintainers, with Falcone product owner agreement on the representative workload. Record actual deployed source/image versions separately from inspected source. Measure current Temporal staging read-only in `in-falcone-staging`: starts/s, committed transitions/run, waiting-run count and age, schedules and occurrence bursts, concurrent activities, signals, retries, payload/event sizes and retention. Do not treat WebSocket message rate or deployed function count as workflow throughput.

Build a model separating admission, transitions, timers, worker execution, outbox and storage. Account for idle multi-month waits, backlog recovery, skewed tenants, event bursts, long jobs and retained interpreter versions. Record sample window and variability, sanitized distributions and measurement limitations, without collecting credentials or unredacted tenant payloads.

Run subsequent native load/crash/soak benchmarks only in dedicated `fw-test-*` namespaces on the shared cluster under D7. Use bounded effect simulators and never double real effects. Explore the architecture's 10/100/1,000 starts/s tiers and 10–30 transitions/run as provisional test inputs, not supported capacity. Include fairness, expiry recovery, evaluator overload, DB failover, restored payloads and outbox catch-up; stop before harming shared product traffic.

Publish hardware, PostgreSQL/replication/storage configuration, engine/worker replica counts, connection and IO budgets, workload mix, offered and achieved rate, latency percentiles, error rate and saturation. Lease length, heartbeat/renewal intervals, scan batches, connection-budget and capacity numbers are provisional pending M0 measurement; tune them using measured tail latency and loss recovery. The architecture's availability, dispatch, timer and RPO/RTO figures remain provisional objectives pending workload agreement and actual HA/restore evidence.

Accept a supported envelope only when durable acknowledgements, fencing, fairness and recovery still hold at the agreed load. Product/SRE define availability exclusions and recovery/latency targets; no throughput result relaxes correctness. This documentation performs no cluster measurement or benchmark.

## Alternatives

- Reusing serverless message throughput gives no estimate for transactional workflow progression.
- Reporting peak starts/s alone hides waiting storage, history and recovery bottlenecks.
- Declaring targets contractual before measurement mistakes exploration for qualification.

## Consequences

M0 produces inputs for decomposition and sizing; production commitments remain gated on subsequent qualification. D2 stays TypeScript on Node.js, and the k3s stand-in does not certify an unknown corporate OpenShift deployment. Missing inventory or measurements are assigned evidence gaps, never fabricated values.
