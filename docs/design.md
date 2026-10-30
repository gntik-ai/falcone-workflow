# falcone-workflow design

Updated 30 October 2026. Source baseline inspected: Falcone commit `47674add95223e6ccd7f6f0dcd11106469a0a30e`. This is a repository snapshot, not a verified deployed version. **The operator accepted the architecture direction on 30 October 2026 ([ADR 0001](adr/0001-native-falcone-workflow.md)). No runtime is implemented, and corporate-cluster feasibility, capacity and security qualification remain unverified.**

## Purpose and scope

Build a first-party Falcone service that replaces the Temporal engine behind Falcone workflows while retaining Falcone's APIs, DSL, console, identity, tenancy and service integrations. This is not a proposal to install a different generic workflow platform.

Falcone's workflow API and DSL are the public contract. Raw Temporal SDK and server compatibility is out of scope. During migration both engines run behind the Falcone facade, and existing Temporal runs finish on Temporal. Existing code already establishes visual-DSL, external-call and human-approval requirements. Compensation and the flow-control, human-task and operator extensions from the functional gap analysis are opt-in and versioned; apiVersion v1.0 behavior is unchanged.

## Operator decisions (2026-10-30)

| # | Topic | Decision |
|---|---|---|
| D1 | Repository split | The engine, evaluator, scheduler/timer/lease services and trusted task workers live in `gntik-ai/falcone-workflow`. The workflow facade, backend routing, console, CLI, quotas, admission and service adapters live in `gntik-ai/falcone`. The Helm chart lives in `gntik-ai/falcone-charts`. A story that spans repositories is split into one issue per repository. Stories and epics are product-level and may span repositories; the backlog decomposition turns each story into technical issues, one per repository, each with a single owner and explicit cross-repository dependencies. |
| D2 | Engine language | TypeScript on Node.js. Go is no longer an M0 alternative. |
| D3 | Temporal compatibility | No raw Temporal SDK or server compatibility. Falcone's workflow API and DSL stay the public contract; both engines run behind the Falcone facade during migration; existing Temporal runs finish on Temporal. |
| D4 | Shared contracts with falcone-serverless | falcone-workflow consumes falcone-serverless's worker execution API (`ctr-worker-execution-api`) and job checkpoint contract (`ctr-job-checkpoint`), and the shared Falcone outbox/inbox and lease/fencing module that falcone-serverless story STO-03 builds in Falcone, instead of defining its own. INT-02 is rescoped to consuming those contracts. The serverless Temporal-activity tasks stay while Temporal serves existing runs. |
| D5 | Database | A separate database on the shared PostgreSQL cluster, not a schema in Falcone's database, with a connection budget. |
| D6 | License | MIT, the same as Falcone. |
| D7 | Cluster testing | Cluster tests run in dedicated `fw-test-*` namespaces and may read `in-falcone-staging`; `family-rentals-prod`, `musematic*` and `llmwiki*` are off limits. k3s with Pod Security "restricted" stands in for OpenShift. |
| D8 | Waits and compensation | Keep current waits and approvals, support multi-month waits, and make compensation opt-in and versioned. The maximum permitted wait W_max is 12 months (ADR-0009). |

The repository seed (license, contributor guide, CI and the TypeScript skeleton) already provides the CI bootstrap, so OPS-03 no longer blocks M0 for CI. Capacity must be measured on the current Temporal staging deployment during M0 (MIG-01).

## Repository ownership

| Repository | Owns |
|---|---|
| `gntik-ai/falcone-workflow` | Engine, bounded evaluator, scheduler, timer and lease services, trusted task workers |
| `gntik-ai/falcone` | Workflow facade and backend routing, console, CLI, quotas, admission and service adapters; the shared outbox/inbox and lease/fencing module |
| `gntik-ai/falcone-charts` | Helm chart deploying the engine and its workers |
| `gntik-ai/falcone-serverless` | Qualified untrusted computation and the worker execution and job checkpoint contracts |

## Recommended boundary

Retain the current Falcone DSL and develop an explicit durable state machine for its nodes. Run only trusted interpreter and connector code in engine processes. Tenant expressions receive strict limits; arbitrary tenant code belongs in qualified falcone-serverless execution profiles. Waiting workflows occupy persisted records, not dedicated pods or permanently blocked worker threads.

Use a dedicated database on the shared PostgreSQL cluster as the authoritative store, with its own roles and a connection budget. Use existing Kafka for event transport through the shared outbox/inbox module, not as a second authoritative workflow log. Large payloads remain behind Falcone's S3 abstraction. Keep identity through Keycloak/Falcone and credential references through the existing secret-management boundary.

## Evidence-driven scope

The inspected interpreter supports sequence, parallel, task, branch, wait, approval and sub-flow. It pins definitions and uses Temporal activities, timers, signals and child workflows. The facade owns definition versions, execution lifecycle and role checks. Flow cron scheduling is separate from Falcone's standalone scheduling-engine. Monitoring translates Temporal history to SSE.

The task catalog includes database, storage, functions, events, HTTP, email, LLM completion/batch and large-task execution. Those are replacement requirements, not greenfield feature suggestions. Source comments and historical READMEs sometimes describe early stubs; the implementation and contract fixtures must take precedence. In particular the dispatch catalog retains an echo fallback for harness/legacy paths; the new production worker must reject unknown task types.

## Functional gap analysis (2026-10-30)

A review against 16 workflow engines and specifications found the baseline strong on durability and weaker on flow-control primitives, run-level operator controls, admission control and visibility. Its findings are folded into this revision:

- **Must-have for migration or parity:** error-type taxonomy and `nonRetryableErrors` matching, trigger start-or-signal by business key, parallel failure and child propagation semantics, data-passing and flow-input rules, distinct cancel/terminate/retry operations, schedule policy fidelity, effective retry/timeout defaults and multi-month waits. These are requirements on existing stories.
- **Should-have:** error boundaries and finalizers (DSL-04), dynamic fan-out (DSL-05), in-flight version migration (DSL-06), callback-token and event-or-timeout waits (EVT-04), lifecycle events and trigger filters (EVT-05), flow concurrency, rate limits and priority (TEN-04), human-task forms, quorum and escalation (HUM-04), bulk operations (OPS-04), SLA alerts (OBS-04), run search (OBS-05), test mode (CON-04), and typed incidents, retention and erasure, output schemas and synchronous acknowledgements on existing stories.
- **Later** items are listed as optional enhancements after parity, and explicitly rejected patterns as rejected paths, in [trade-offs](tradeoffs.md).

Eighteen under-specified requirements were completed in place, including FR-ACT-06, which now requires multi-month waits and retention of interpreter and definition versions for at least the longest permitted wait. The operator later set that maximum wait, W_max, to 12 months (ADR-0009).

## Delivery gates

- **M0 — scope and feasibility:** inventory actual deployments and legacy semantics, preserve DSL fixtures, consume the falcone-serverless contracts, measure capacity on the current Temporal staging deployment and validate restricted deployment constraints on the k3s stand-in.
- **M1 — durable core:** transactional state, leases/fencing, timers, bounded evaluator, authentication and native worker context. Crash/concurrency tests are mandatory.
- **M2 — Falcone completeness:** port task catalog, triggers, schedules, approvals, quotas, SSE and optional compensation, plus the should-have flow-control, human-task and visibility features.
- **M3 — qualification and migration:** restore/load/soak tests, differential semantics, canary cohorts, schedule transfer, long-lived run drainage, operator bulk tooling, then retirement.

Do not remove Temporal merely because M1 demonstrations succeed. Some deployed workflows may remain on the old engine for their full lifetime.

## Accepted architecture decisions (ADRs 0002–0013)

The [architecture review](architecture-review.md) proposed ADRs 0002–0013 covering ownership, persistence, shared primitives, dispatch, serverless tasks, expressions, calendars, versions, migration, credentials, history and capacity. The operator accepted all twelve as written on 30 October 2026, including the explicit R3 approval for RLS (ADR-0003), expression isolation (ADR-0007), dual-engine and live-run migration (ADR-0010) and long-lived credentials (ADR-0011). D1–D8 remain authoritative.

The operator also resolved three review blockers: W_max is 12 months (F08, ADR-0009); the STO-03 shared module is falcone issues #1331, #1343, #1356, #1361 and #1381 (F03, ADR-0004); and `ctr-worker-execution-api` v1 is falcone-serverless #124 and #130, with `ctr-job-checkpoint` v1 planned as falcone-serverless task JOB-01.t1 (F05, ADR-0006). Exact contract paths and versions are confirmed from the delivered code as an integration gate. Per-repository technical issues come from the backlog decomposition (F01), and the M0 capacity baseline is a gate before numeric commitments (F12). The remaining findings stay open with their owner roles in the review.

## Document map

The combined design document, [falcone-workflow-design.md](falcone-workflow-design.md), is generated from these chapters and is what Hermes's backlog decomposition reads.

1. [Survey and comparative analysis](survey.md)
2. [Functional requirements](requirements.md)
3. [Baseline architecture](architecture.md)
4. [Detailed backlog](backlog.md) and [JSON import payloads](backlog.json)
5. [Open questions and ownership](open-questions.md)
6. [Trade-offs](tradeoffs.md) and [migration sequence](migration.md)
