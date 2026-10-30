# 2. Functional requirements

72 testable requirements for a custom Falcone service. Requirements added by the 30 October 2026 functional gap analysis continue each area's numbering. Inclusion is not proof of implementation.

## Falcone contracts and developer experience

- [ ] **FR-CON-01:** The system must preserve inventoried Falcone workflow API routes, response schemas, status codes and tenant-scoped identifiers through a compatibility facade.
- [ ] **FR-CON-02:** The project must publish a compatibility matrix marking each observed behavior as preserved, intentionally versioned, or a migration blocker.
- [ ] **FR-CON-03:** The system must expose authenticated start, get, list, cancel, retry and signal operations with tenant-scoped idempotency keys.
- [ ] **FR-CON-04:** The system must route every existing run to its recorded backend and return a retryable service-unavailable response when that backend is unavailable.
- [ ] **FR-CON-05:** The system must support CLI validate, publish, start, inspect, cancel and retry operations using Falcone authentication.
- [ ] **FR-CON-06:** The system must provide versioned task schemas and validation errors usable by Falcone's existing visual editor.

## DSL interpretation and versioning

- [ ] **FR-DSL-01:** The system must validate sequence, parallel, task, branch, wait, approval and sub-flow nodes using the inventoried Falcone DSL rules.
- [ ] **FR-DSL-02:** The system must reject invalid cycles, duplicate IDs, unknown tasks, dangling references and invalid cron/duration expressions before publishing.
- [ ] **FR-DSL-03:** The system must evaluate expressions with bounded input size, runtime and memory without network, filesystem or arbitrary-code access.
- [ ] **FR-DSL-04:** The system must persist branch decisions, parallel completion sets and deterministic output-merge behavior before advancing successors.
- [ ] **FR-DSL-05:** The system must pin each run to immutable definition and interpreter versions and each child to an authorized explicit definition version.
- [ ] **FR-DSL-06:** The system must reject unsupported historical versions and require an explicit audited migration plan before changing active-run semantics.

## Durable state and recovery

- [ ] **FR-DUR-01:** The system must acknowledge a start only after committing the run, pinned plan, first ready work, audit event and idempotency record.
- [ ] **FR-DUR-02:** The system must commit each state transition, ordered per-run event and generated work atomically under a checked revision.
- [ ] **FR-DUR-03:** The system must reject task completions and heartbeats with expired or superseded lease generations.
- [ ] **FR-DUR-04:** The system must recover abandoned tasks through durable scans even when all optional notifications are lost.
- [ ] **FR-DUR-05:** The system must bound event history and payload growth using configured limits and resumable continuation or archival policies.
- [ ] **FR-DUR-06:** The system must restore database and referenced object payloads to a consistent recovery point and reconcile external effects before resuming dispatch.

## Task execution and long-running work

- [ ] **FR-ACT-01:** The system must dispatch tasks through a versioned protocol carrying tenant, workspace, run, node occurrence, attempt, lease generation and pinned adapter version.
- [ ] **FR-ACT-02:** The system must execute side effects only in authorized workers and must reject unknown task types in production.
- [ ] **FR-ACT-03:** The system must apply configured maximum attempts, backoff, retryable error classes, start-to-close, schedule-to-close and heartbeat timeouts.
- [ ] **FR-ACT-04:** The system must classify connectors by idempotency support and surface ambiguous external outcomes instead of promising universal exactly-once effects.
- [ ] **FR-ACT-05:** The system must persist external job IDs and checkpoint references and resume observation after worker loss without blindly resubmitting the job.
- [ ] **FR-ACT-06:** The system must support configurable multi-day waits with bounded heartbeat, cancellation and credential-renewal policies.

## Timers and schedules

- [ ] **FR-TIM-01:** The system must persist wait and retry timers and fire each logical timer at most once into workflow state.
- [ ] **FR-TIM-02:** The system must resolve simultaneous signal, timeout and cancellation transitions with one documented transactional ordering rule.
- [ ] **FR-TIM-03:** The system must preserve Falcone schedule identities, published cron text, next-action times, recent actions and idempotent pause/resume behavior.
- [ ] **FR-TIM-04:** The system must implement explicit overlap, catch-up window, timezone and daylight-saving policies and atomically deduplicate each scheduled occurrence.
- [ ] **FR-TIM-05:** The system must fence schedule ownership during backend handover so only one engine may admit an occurrence.
- [ ] **FR-TIM-06:** The system must support audited bounded backfill with a preview of candidate occurrences and quota impact.

## Events and trigger delivery

- [ ] **FR-EVT-01:** The system must persist incoming trigger/event deduplication records and resulting workflow transitions before acknowledging delivery.
- [ ] **FR-EVT-02:** The system must publish committed outgoing events through a retryable transactional outbox with stable event IDs.
- [ ] **FR-EVT-03:** The system must authenticate webhook triggers with rotation-aware signatures, replay protection and size limits.
- [ ] **FR-EVT-04:** The system must derive tenant and workspace from verified trigger registration rather than caller-supplied payload fields.
- [ ] **FR-EVT-05:** The system must persist authorized signals using deduplication IDs and explicit run/node-occurrence correlation.
- [ ] **FR-EVT-06:** The system must define TTL, capacity and terminal-run behavior for unmatched or early-arriving signals.

## Human approvals and compensation

- [ ] **FR-HUM-01:** The system must derive approval actor identity from verified authentication and enforce configured reviewer permissions.
- [ ] **FR-HUM-02:** The system must preserve approval outcome fields and distinguish rejection, timeout and cancellation.
- [ ] **FR-HUM-03:** The system must record completed compensatable operations and schedule configured compensations in dependency-safe reverse order.
- [ ] **FR-HUM-04:** The system must track compensation retries, failures and manual intervention separately from the original task outcome.
- [ ] **FR-HUM-05:** The system must require authorization, reason and expected run revision for manual repair or retry actions.
- [ ] **FR-HUM-06:** The system must preserve original history and create explicit linked attempts or continuation records for repair.

## Security, tenancy and Falcone quotas

- [ ] **FR-TEN-01:** The system must enforce tenant/workspace ownership for definitions, runs, events, schedules, payloads and monitoring streams using verified identity.
- [ ] **FR-TEN-02:** The system must preserve Falcone definition-write role restrictions and test authorization on every execution lifecycle operation.
- [ ] **FR-TEN-03:** The system must bind execution credential references to authoritative tenant, workspace, root run and allowed child lineage before connector use.
- [ ] **FR-TEN-04:** The system must renew or reauthorize long-lived runs under Falcone policy without storing bearer tokens or secret values in history.
- [ ] **FR-TEN-05:** The system must consume versioned Falcone quota policy for starts, active tasks, waiting runs, retries, fan-out, payload bytes and retention.
- [ ] **FR-TEN-06:** The system must enforce fair tenant/workspace admission with idempotent reservations, releases and usage events across crashes.

## Falcone services and serverless integration

- [ ] **FR-INT-01:** The system must preserve qualified contracts for db.query, storage.get/put, functions.invoke, events.publish, http.request, email.send, llm.complete, llm.batch and largeTask.run.
- [ ] **FR-INT-02:** The system must enforce per-connector timeout, payload, credential, egress and workspace policies before performing external calls.
- [ ] **FR-INT-03:** The system must define versioned start/status/cancel/result callbacks with stable operation keys, authenticated correlation and explicit cancellation outcomes.
- [ ] **FR-INT-04:** The system must avoid a runtime dependency cycle: falcone-serverless execution primitives must run without calling Temporal or requiring falcone-workflow to execute themselves.
- [ ] **FR-INT-05:** The system must store large payloads through tenant-scoped Falcone object references with content hashes, retention metadata and authorization checks.
- [ ] **FR-INT-06:** The system must persist provider job IDs and bounded poll schedules for batch tasks, including cancellation cleanup and credential expiry.

## Monitoring, audit and performance

- [ ] **FR-OBS-01:** The system must expose ordered tenant-scoped history and compatible SSE frames with stable resumable event cursors.
- [ ] **FR-OBS-02:** The system must emit audit events for lifecycle, authorization-sensitive changes, approvals, repair and backend handover.
- [ ] **FR-OBS-03:** The system must measure admission latency, transition throughput, queue age, timer lag, lease expiry, retry rate, outbox lag and database contention.
- [ ] **FR-OBS-04:** The system must propagate trace correlation across Falcone services while redacting secrets and controlling metric cardinality.
- [ ] **FR-OBS-05:** The project must benchmark workflow starts, step transitions, durable waits and activity concurrency independently from Falcone's WebSocket message rate.
- [ ] **FR-OBS-06:** The project must publish achieved availability, latency and recovery results against an agreed workload and resource budget before production cutover.

## Deployment, CI/CD and operations

- [ ] **FR-OPS-01:** The system must deploy using existing PostgreSQL and standard namespaced resources without mandatory CRDs, operators, cluster roles or privileged containers.
- [ ] **FR-OPS-02:** The system must run as non-root with arbitrary allowed UID, read-only root filesystem, dropped capabilities and no host access.
- [ ] **FR-OPS-03:** The system must support rolling compatible upgrades, bounded graceful drain and documented rollback limits for schema and interpreter changes.
- [ ] **FR-OPS-04:** The project must provide tested runbooks for database failover, backup restore, stuck runs, queue overload and key rotation.
- [ ] **FR-OPS-05:** The project must gate releases on contract, isolation, state-machine fault, schema-migration and dependency-security checks.
- [ ] **FR-OPS-06:** The project must assign accountable runtime maintenance, SRE on-call, security review and Falcone product ownership before production release.

## Temporal migration and retirement

- [ ] **FR-MIG-01:** The project must inventory Temporal-dependent code, active workflow versions, open executions, schedule ownership and task adapters before selecting migration cohorts.
- [ ] **FR-MIG-02:** The project must compare native and Temporal outcomes using deterministic fixtures or isolated effect simulators without doubling production effects.
- [ ] **FR-MIG-03:** The system must route new starts by approved cohort and persist backend ownership for all later run operations.
- [ ] **FR-MIG-04:** The system must keep in-flight Temporal runs on Temporal unless an explicit application-level checkpoint transfer is validated.
- [ ] **FR-MIG-05:** The project must verify no remaining required Temporal runs, schedules, credentials or callers before removing the Temporal deployment and SDK dependencies.
- [ ] **FR-MIG-06:** The project must update Falcone integration documentation and falcone-serverless workflow references to the native contract with a rollback and retention plan.
