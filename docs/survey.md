# 1. Survey and comparative analysis

Reviewed 22 October 2026. Platform behavior is grounded in [primary sources](sources.md); suitability ratings are architectural judgments for Falcone. No benchmark below claims measured superiority.

## Temporal baseline

Temporal separates Frontend RPC admission, History state/timers, Matching task queues and an internal Worker service. Application workers run workflow and activity code outside the server. Durable history supports replay; activities provide side effects, retries and heartbeats; timers, signals, child workflows and schedules support extended business processes. Persistent storage is required; visibility and operational tooling add deployment concerns. [T1–T3]

Its strongest reference for Falcone is explicit failure semantics. The replacement must preserve accepted work, cancellation behavior, version pinning and recovery, not merely a graph traversal API.

### Observed Falcone coupling and pain points

- Workflow orchestration imports Temporal SDK primitives throughout the DSL interpreter; task adapters rely on Activity Context and Temporal error classes.
- Credential reference resolution queries Temporal run ancestry. Removing the SDK without replacing this authorization proof would break isolation.
- Schedule management and triggers use a Temporal client; an existing reconnect fix documents how a rejected connection promise could poison later requests.
- Monitoring maps Temporal event types and activity IDs into Falcone SSE frames.
- The worker package documents a TypeScript/CommonJS bundling deviation from sibling ESM services. This is a repository-specific integration constraint, not a claim that all Temporal installations require Falcone's exact build layout.
- Falcone supplies business schemas, catalog, identity and quotas around the engine. A custom engine can integrate these directly, but Falcone then owns distributed-system correctness and on-call operations.

Temporal does not intrinsically require privileged tenant pods or an operator. Restricted OpenShift deployment alone does not prove replacement is necessary; first-party control and a smaller Falcone-specific scope are the additional rationale.

## Comparison

| Reference | Functional model | Scale model and extensibility | Strength versus Temporal for this design | Weakness / Falcone mapping |
|---|---|---|---|---|
| **Temporal** | Durable code workflows, activity retries, signals, timers, children and schedules | Independently scaled server services and application workers; SDKs and activities | Existing implementation and strong recovery semantics | Multiple operational components; SDK/replay and history coupling; Falcone IAM/S3/task policy still supplied by adapters |
| **Cadence** | Durable code workflows, activities, signals and long-lived state | Distributed service with partitioned history and worker task lists; SDK activity implementations | Valuable independent reference for timeout and task lifecycle contracts | Similar distributed-service and replay burden; not a simplification by itself; domain isolation does not replace Falcone workspace authorization [C1–C2] |
| **Conductor OSS** | Declarative workflows and task workers across languages | Scale servers and poll-based workers; task domains, custom workers and persistence/queue integrations | Closest conceptual reference to Falcone's existing DSL and task catalog | Adoption would still require DSL/contract translation and policy adapters; persistence/queue combinations add operations choices [N1] |
| **Apache Airflow** | Scheduled DAG/task execution, dependencies and operational run management | Scheduler/executor/worker architecture; pluggable executors and providers | Strong reference for schedules, backfills, task history and operational UX | Primarily batch/data orchestration; a less natural base for Falcone's interactive signal/approval flows; DAG Python is trusted code, not tenant sandboxing [A1–A2] |
| **Dapr Workflow** | Code-defined durable workflows integrated with invocation, pub/sub and state | Durable Task engine and distributed runtime; SDK activities and Dapr components | Useful activity/lifecycle abstraction and failure-recovery patterns | Full Dapr adoption adds another runtime and configuration surface; Kubernetes installation details require qualification under corporate restrictions [D1–D2] |
| **DBOS TypeScript** | Application-embedded durable steps/workflows backed by PostgreSQL | Application workers and database coordination; library calls and queues | Closest lower-operations alternative and reference for leveraging Falcone PostgreSQL | Still a library dependency and programming-model migration; tenant isolation, DSL execution and API compatibility remain Falcone work [B1–B2] |
| **Restate — source-available reference** | Journaled durable services, workflow primitives and keyed state | Partitioned runtime with external SDK service endpoints | Useful design reference for durable calls, operation identity and suspension | Current server license is BSL 1.1, explicitly not open source; do not count it among OSS alternatives or copy server code into Falcone without a separately approved licensing path [R1–R2] |

Cadence, Conductor, Airflow, Dapr and DBOS provide five open-source references beyond Temporal. Maturity is not identical: Temporal/Cadence and Airflow have longer operating histories; evaluate DBOS and individual Dapr workflow SDKs against the actual Falcone workload rather than assuming feature parity.

## Functional references from the gap analysis (30 October 2026)

A functional gap analysis compared capabilities across 16 products. It added the 11 below and re-checked Temporal, Conductor OSS, Airflow 3.x, Restate and DBOS for capabilities this survey had not compared: Temporal updates, priority/fairness, the schedule policy set, reset/batch operations and parent-close policy; Conductor timeout policies, rate limits, rerun/skip and its test API; Airflow 3 human-in-the-loop operators, deadline alerts and backfill reprocess modes; DBOS queue flow control (the closest PostgreSQL-native reference for TEN-03 and TEN-04); Restate awakeables. Products are pattern references; none is adopted. Source-available products are **design references only**: no code is copied from them.

| Product | License class | What Falcone borrows |
|---|---|---|
| Argo Workflows | Apache-2.0 | Retry strategy with expressions; mutex/semaphore synchronization; cron concurrency policy, time zone and documented DST behavior; parameter fan-out; archive TTL |
| Camunda 8 / Zeebe | Camunda License 1.0, source-available; production licence required for self-managed since 8.6. **Design reference only** | Typed incidents; instance migration with mapping instructions; instance modification; multi-instance with completion condition; message correlation with TTL buffering; error boundary events; user-task assignment, due dates and escalation |
| Kestra | Apache-2.0; enterprise features proprietary | Concurrency overflow (queue, cancel, fail); missed-schedule recovery and pausable backfill; SLA actions; replay from a task; error branches, allow-failure and after-execution handlers |
| Prefect 3 | Apache-2.0 | Concurrency slots with leases and rate limits; typed wait-for-input; automations including absence-of-event triggers |
| n8n | Sustainable Use License (fair-code, not OSI open source). **Design reference only** | Error workflows; Wait node resumed by an authenticated URL or form with a wait limit |
| Windmill | Apache-2.0 / AGPLv3 plus a proprietary enterprise edition. **Design reference only** | Approval count, self-approval prohibition, group restriction, form schema and continue-on-timeout; concurrency limits with custom keys |
| Hatchet | MIT | CEL concurrency keys with round-robin and cancel strategies; static and dynamic rate limits; priority tiers; durable sleep/event or-groups |
| Inngest | SSPL-1.0 with a future Apache-2.0 licence. **Design reference only** | Flow control (concurrency, throttling, debounce, priority, batching); cancel-on-event; wait-for-event with match and timeout; idempotency window |
| Serverless Workflow / Open Workflow DSL | CNCF specification; license not reviewed | Task vocabulary (try/catch/raise, competing fork, listen-until, for); retry when/except-when/jitter; RFC 7807 error types; workflow and task lifecycle CloudEvents |
| Dagster | Apache-2.0 | Sensor `run_key` deduplication as a precedent for start-or-signal; partitions and backfills |
| Flyte | Apache-2.0 | Typed task interfaces; map tasks with partial-failure tolerance; gate nodes |

Restate (BSL 1.1, above) is also a design reference only. The patterns adopted from these products are the gap-analysis requirements in section 2 and stories CON-04, DSL-04 to DSL-06, EVT-04, EVT-05, HUM-04, TEN-04, OBS-04, OBS-05 and OPS-04; deferred and rejected patterns are in section 6. Sources are listed under "Functional gap analysis references".

## Falcone integration implications

For every alternative, Keycloak authentication, Falcone workspace roles and quota policy need an application-specific authorization layer. S3 is suitable for large payload references, not an automatic replacement for the engine's transactional state. A function invocation adapter is required for falcone-serverless. Multi-tenancy must cover database predicates, events, histories, callbacks and credentials; an engine namespace or task queue alone is not an untrusted-code isolation boundary.

Adopt patterns rather than cloning engines: durable transitions from Temporal/Cadence; explicit task graphs from Conductor; schedule operations from Airflow; narrow activity protocols from Dapr; transactional persistence from DBOS. Restate is an additional conceptual reference only.

## Licensing and reuse

Inspected repository pages identify Cadence and Conductor as Apache-2.0 and DBOS TypeScript as MIT. Pin exact upstream revisions and inspect component licenses before reusing code. Current Restate license specifies BSL 1.1 and a future change license; “public repository” must not be equated with open-source reuse permission. Camunda 8, Inngest, n8n, Windmill and Restate are source-available or not OSI open source and are design references only. Falcone itself, and this service, are MIT-licensed (D6). No upstream code is included in this proposal. [C1, N1, B2, R2]

