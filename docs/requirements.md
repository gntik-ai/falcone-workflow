# 2. Functional requirements

98 testable requirements for a custom Falcone service. Requirements added by the 30 October 2026 functional gap analysis continue each area's numbering. Inclusion is not proof of implementation.

## Falcone contracts and developer experience

- [ ] **FR-CON-01:** The system must preserve inventoried Falcone workflow API routes, response schemas, status codes and tenant-scoped identifiers through a compatibility facade.
- [ ] **FR-CON-02:** The project must publish a compatibility matrix marking each observed behavior as preserved, intentionally versioned, or a migration blocker.
- [ ] **FR-CON-03:** The system must expose authenticated start, get, list, cancel, retry and signal operations with idempotency keys scoped to (tenant, workspace, flow): the same key with the same input returns the same run for at least max(24 h, the run's retention) and a different input returns a conflict; an optional business ID has a conflict policy (fail or use-existing; terminate-existing is administrator-only) and a reuse-after-close policy (allow, allow-if-failed or reject).
- [ ] **FR-CON-04:** The system must route every existing run to its recorded backend and return a retryable service-unavailable response when that backend is unavailable.
- [ ] **FR-CON-05:** The system must support CLI validate, publish, start, inspect, cancel and retry operations using Falcone authentication.
- [ ] **FR-CON-06:** The system must provide versioned task schemas and validation errors usable by Falcone's existing visual editor, preserving the FLW-E001 to FLW-E009 codes, rules and kinds verbatim; new validation rules receive new codes and never reuse existing ones.
- [ ] **FR-CON-07:** The system must provide cancel (cooperative: stops new normal work, runs configured cleanup or compensation), terminate (administrative: no further workflow logic, reason required, audited) and retry (the inventoried legacy meaning, recorded either as a linked new run or as a new attempt lineage of the failed node occurrence) as distinct operations with explicit parent/child propagation, each reporting request acceptance separately from the eventual terminal outcome.
- [ ] **FR-CON-08:** The system must run a flow version in test mode with mocked task outputs or errors, simulated time and injected signals, events and approval decisions, producing the same history, error codes and SSE frames as live execution without resolving credentials or dispatching to any connector, through both the API and the CLI.
- [ ] **FR-CON-09:** The system must validate connector outputs against the pinned task output schema before committing a completion, treating a violation as a typed non-retryable error, and must expose input and output schemas to the visual editor for reference completion.

## DSL interpretation and versioning

- [ ] **FR-DSL-01:** The system must validate sequence, parallel, task, branch, wait, approval and sub-flow nodes using the inventoried Falcone DSL rules.
- [ ] **FR-DSL-02:** The system must reject invalid cycles, duplicate IDs, unknown tasks, dangling references and invalid cron/duration expressions before publishing, reporting the inventoried FLW-E001 to FLW-E009 codes, rules and kinds verbatim.
- [ ] **FR-DSL-03:** The system must evaluate expressions with bounded input size, runtime and memory without network, filesystem or arbitrary-code access; maximum expression length, evaluation cost and steps, result size and input bytes are configured per interpreter version, the CEL library version is pinned per interpreter version, and clock functions use the persisted evaluation time, never the wall clock at replay.
- [ ] **FR-DSL-04:** The system must persist branch decisions, parallel completion sets and deterministic output-merge behavior before advancing successors; parallel failure and cancellation semantics follow FR-DSL-07.
- [ ] **FR-DSL-05:** The system must pin each run to immutable definition and interpreter versions and each child to an authorized explicit definition version; child behavior on parent cancellation, termination, failure or timeout follows FR-DSL-07.
- [ ] **FR-DSL-06:** The system must reject unsupported historical versions, require an explicit audited migration plan before changing active-run semantics, and retain every interpreter and definition version referenced by an open run for at least the longest permitted remaining wait, or migrate the run through FR-DSL-11.
- [ ] **FR-DSL-07:** The system must define per interpreter version, and preserve for apiVersion v1.0, (a) parallel-node failure semantics: fail-fast or wait-all, whether in-flight sibling tasks are cancelled, left running or abandoned, and which sibling results are retained; and (b) child-run behaviour when the parent is cancelled, terminated, fails or times out: terminate, request-cancel or abandon. Both must be fixture-tested against Temporal outcomes.
- [ ] **FR-DSL-08:** The system must preserve the inventoried rules by which task and sub-flow inputs reference flow inputs, run variables and prior node-occurrence outputs (reference syntax, evaluation time, missing-reference, null and type-coercion behaviour), and must apply declared flow-input type, required and default rules at admission, rejecting violations with stable error codes before a run is created.
- [ ] **FR-DSL-09:** In an additive DSL version, the system must support error boundaries on task, sub-flow, sequence and parallel nodes that route errors matching declared error types (after retries are exhausted) to a declared handler node, optional finalizer nodes that run on success, failure or cancellation of their scope, and a flow-level on-failure handler; caught errors must be recorded in history, and uncaught errors must fail the run exactly as in v1.0.
- [ ] **FR-DSL-10:** The system must support a map node that runs a task or sub-flow for each element of a runtime collection with a declared maximum item count, maximum concurrency, failure policy (fail-fast, continue, or minimum success count or ratio) and index-ordered output collection, reserving fan-out quota at expansion time and persisting per-item occurrence state so that a crash neither duplicates nor drops items.
- [ ] **FR-DSL-11:** The system must migrate selected waiting or running native runs to another published version of the same flow using an explicit node-occurrence mapping that is validated in a dry run, applied atomically per run under the expected revision and recorded in audit, and must reject migration when an active task, timer or approval lacks a mapping or the mapping changes node type or scope.

## Durable state and recovery

- [ ] **FR-DUR-01:** The system must acknowledge a start only after committing the run, pinned plan, first ready work, audit event and idempotency record.
- [ ] **FR-DUR-02:** The system must commit each state transition, ordered per-run event and generated work atomically under a checked revision.
- [ ] **FR-DUR-03:** The system must reject task completions and heartbeats with expired or superseded lease generations.
- [ ] **FR-DUR-04:** The system must recover abandoned tasks through durable scans even when all optional notifications are lost.
- [ ] **FR-DUR-05:** The system must bound event history and payload growth using configured limits and resumable continuation or archival policies: a run segment has a configured maximum event count and byte size, and continuation keeps the public run ID, links segments and keeps SSE cursors (FR-OBS-01) monotonic across segments.
- [ ] **FR-DUR-06:** The system must restore database and referenced object payloads to a consistent recovery point and reconcile external effects before resuming dispatch.
- [ ] **FR-DUR-07:** The system must apply a per-workspace retention period to closed runs within quota limits, support authorized deletion of individual closed runs and their payload objects with audit, and support erasure of payload objects linked to a data subject while preserving redacted structural history, honoring legal-hold flags that suspend deletion.

## Task execution and long-running work

- [ ] **FR-ACT-01:** The system must dispatch tasks through a versioned protocol carrying tenant, workspace, run, node occurrence, attempt, lease generation and pinned adapter version.
- [ ] **FR-ACT-02:** The system must execute side effects only in authorized workers and must reject unknown task types in production.
- [ ] **FR-ACT-03:** The system must apply the retry fields maxAttempts (at least 1), initialInterval, backoffCoefficient (at least 1), maximumInterval and nonRetryableErrors (FR-ACT-07 types) with delay(n) = min(initialInterval × backoffCoefficient^(n−1), maximumInterval), and the timeouts scheduleToStart (queue wait), startToClose (per attempt), scheduleToClose (all attempts), heartbeat (at most startToClose) and a run-level executionTimeout (none for apiVersion v1.0); the compiled plan of a v1.0 definition must store the effective legacy defaults explicitly, including those injected for absent policies or timeouts; optional jitter and a connector-supplied next-delay override belong to a new apiVersion and never extend maxAttempts or scheduleToClose.
- [ ] **FR-ACT-04:** The system must classify each catalog connector as idempotent-by-key, reconcilable (read-after-timeout) or non-idempotent, use that class for retry eligibility, the repair preview (FR-HUM-08) and ambiguous-outcome incidents (FR-HUM-09), block blind retries of non-idempotent connectors regardless of maxAttempts, and surface ambiguous external outcomes instead of promising universal exactly-once effects.
- [ ] **FR-ACT-05:** The system must persist external job IDs and checkpoint references and resume observation after worker loss without blindly resubmitting the job.
- [ ] **FR-ACT-06:** The system must support waits, approvals and timers lasting months, up to a policy maximum set by the product owner, with bounded heartbeat, cancellation and credential-renewal policies, and must exercise credential renewal (FR-TEN-04) in a test that crosses a Keycloak session or offline-token expiry.
- [ ] **FR-ACT-07:** The system must classify every task, expression and connector failure with a stable error type from a versioned taxonomy (at least validation, authorization, timeout, communication, rate-limited, ambiguous-outcome, cancelled and connector-specific types), and must evaluate nonRetryableErrors for apiVersion v1.0 definitions against the inventoried legacy Temporal error-type names emitted by each catalog task.

## Timers and schedules

- [ ] **FR-TIM-01:** The system must persist wait and retry timers and fire each logical timer at most once into workflow state.
- [ ] **FR-TIM-02:** The system must resolve simultaneous signal, timeout and cancellation transitions with one documented transactional ordering rule.
- [ ] **FR-TIM-03:** The system must preserve Falcone schedule identities, published cron text, next-action times, the inventoried number of retained recent actions and idempotent pause/resume behavior; trigger-now and pause/resume notes follow FR-TIM-08.
- [ ] **FR-TIM-04:** The system must preserve the eight DSL overlap names (skip, allow, allow_all, buffer, buffer_one, buffer_all, cancel_other, terminate_other) with their inventoried normalisation and skip as the default, use the inventoried effective catch-up window when catchupWindow is absent, evaluate apiVersion v1.0 schedules in UTC, run a nonexistent local time once at the next valid instant and an ambiguous local time once at its first occurrence for time-zone-aware schedules (a new field), and atomically deduplicate each occurrence by (schedule ID, nominal UTC instant); pausing does not affect admitted runs and manual triggers are not bound by the catch-up window.
- [ ] **FR-TIM-05:** The system must fence schedule ownership during backend handover so only one engine may admit an occurrence.
- [ ] **FR-TIM-06:** The system must support audited bounded backfill over [start, end) with a reprocess mode (missing only, missing and failed, or all), an order (oldest first by default, newest first optional), a concurrency cap independent of live scheduling and the schedule's overlap policy; backfill is exempt from the catch-up window, limited to one active backfill per schedule with a maximum occurrence count, can be paused and cancelled, and offers a dry run listing candidate occurrences and quota impact.
- [ ] **FR-TIM-07:** The system must support waiting until an absolute instant or a CEL-computed instant with an explicit IANA time zone, evaluated once and persisted before the timer is armed.
- [ ] **FR-TIM-08:** The system must support optional schedule start and end bounds, bounded jitter, a maximum action count, pause-on-failure, an operator note on pause and resume, and an audited trigger-now action that applies the schedule's overlap policy unless overridden.

## Events and trigger delivery

- [ ] **FR-EVT-01:** The system must persist incoming trigger/event deduplication records and resulting workflow transitions before acknowledging delivery.
- [ ] **FR-EVT-02:** The system must publish committed outgoing events, including the FR-EVT-09 lifecycle event catalogue, through a retryable transactional outbox with stable event IDs.
- [ ] **FR-EVT-03:** The system must authenticate webhook triggers with rotation-aware signatures, replay protection and size limits.
- [ ] **FR-EVT-04:** The system must derive tenant and workspace from verified trigger registration rather than caller-supplied payload fields.
- [ ] **FR-EVT-05:** The system must persist authorized signals using deduplication IDs and explicit run/node-occurrence correlation.
- [ ] **FR-EVT-06:** The system must take the TTL and per-run capacity for unmatched or early-arriving signals from quota policy, consume buffered signals FIFO per signal name, deduplicate them by signal ID while buffered and for the run's retention after consumption, reject a signal to a terminal run with an explicit error code and record it, and deliver a signal matching several waits to the earliest-armed node occurrence.
- [ ] **FR-EVT-07:** For each inventoried trigger that uses start-or-signal semantics, the system must derive a tenant- and workspace-scoped business key from the verified trigger registration and event, and in one transaction either deliver the signal to the open run holding that key or start a new run and deliver the signal to it, so that concurrent deliveries for one key yield at most one open run and no lost signal.
- [ ] **FR-EVT-08:** The system must provide a callback wait node that issues a single-use, signed, tenant- and node-occurrence-bound completion token or URL with an expiry, accepts exactly one authenticated completion (success, failure, or progress heartbeat) validated against a declared payload schema and size limit, and resolves completion, timeout and cancellation races with the FR-TIM-02 ordering rule.
- [ ] **FR-EVT-09:** The system must publish versioned CloudEvents-formatted lifecycle events for run and node-occurrence transitions (started, completed, failed, cancelled, terminated, waiting for approval or callback, incident opened and resolved, SLA breached) through the outbox, carrying identifiers, versions and object references but no secrets or unredacted payload values.
- [ ] **FR-EVT-10:** The system must support a CEL filter over the verified event and an input mapping for each platform-event and webhook trigger, evaluated before admission and recorded in the trigger's delivery record.
- [ ] **FR-EVT-11:** The system must return, after commit, a synchronous result for signals and approval decisions (accepted, rejected by validation, target not waiting, duplicate, or run terminal), validating the payload before it is persisted.
- [ ] **FR-EVT-12:** The system must support an event-wait node that waits for a correlated platform event or signal matching a declared filter, with a timeout, and records which condition won together with the event reference.

## Human approvals and compensation

- [ ] **FR-HUM-01:** The system must derive approval actor identity from verified authentication and enforce configured reviewer permissions.
- [ ] **FR-HUM-02:** The system must preserve approval outcome fields as {decision, actor subject, actor display name, decided-at, comment, decision revision, source (UI or API)}, distinguish rejection, timeout and cancellation, produce the declared default outcome or the approval.timeout error type on timeout, and raise the approval.rejected error type on rejection so that error boundaries (FR-DSL-09) can route it in a new DSL version.
- [ ] **FR-HUM-03:** The system must record completed compensatable operations and schedule configured compensations in dependency-safe reverse order.
- [ ] **FR-HUM-04:** The system must track compensation retries, failures and manual intervention separately from the original task outcome.
- [ ] **FR-HUM-05:** The system must require authorization, reason and expected run revision for manual repair or retry actions, including the FR-HUM-08 run operations.
- [ ] **FR-HUM-06:** The system must preserve original history and create explicit linked attempts or continuation records for repair.
- [ ] **FR-HUM-07:** The system must support approval nodes with a versioned response schema (choices and typed fields), assignment by user, Keycloak group or role expression, quorum rules (any, all, or N of M), optional prohibition of approval by the run initiator, reminder and escalation timers that do not interrupt the approval, and a declared default outcome on timeout. Every response, reassignment and escalation must be recorded in audit history.
- [ ] **FR-HUM-08:** The system must provide authorized, audited run operations (pause and resume dispatch; retry a failed node occurrence in place; skip a node with an operator-supplied, schema-valid output; set run variables; and rerun from a selected node as a new linked run pinned to the original or an explicitly selected compatible version), each requiring the expected run revision and showing a preview of side effects that may repeat according to connector idempotency class.
- [ ] **FR-HUM-09:** The system must represent each condition that requires human resolution (retries exhausted under an alert-only timeout policy, ambiguous external outcome, expression evaluation error, missing or hash-mismatched payload, expired or revoked credential, policy-blocked effect, undeliverable signal) as a typed incident on the affected node occurrence that stops dispatch on that path, emits a lifecycle event, and closes only through an audited resolution action.

## Security, tenancy and Falcone quotas

- [ ] **FR-TEN-01:** The system must enforce tenant/workspace ownership for definitions, runs, events, schedules, payloads and monitoring streams using verified identity.
- [ ] **FR-TEN-02:** The system must preserve Falcone definition-write role restrictions and test authorization on every execution lifecycle operation.
- [ ] **FR-TEN-03:** The system must bind execution credential references to authoritative tenant, workspace, root run and allowed child lineage before connector use.
- [ ] **FR-TEN-04:** The system must renew or reauthorize long-lived runs under Falcone policy without storing bearer tokens or secret values in history.
- [ ] **FR-TEN-05:** The system must consume versioned Falcone quota policy for starts, active tasks, waiting runs, retries, fan-out, payload bytes and retention.
- [ ] **FR-TEN-06:** The system must enforce fair tenant/workspace admission with idempotent reservations, releases and usage events across crashes, using weighted round-robin across tenants and then across workspaces within a tenant, with weights from quota policy.
- [ ] **FR-TEN-07:** The system must enforce optional per-flow and per-key concurrency limits, where the key is a bounded CEL expression over verified run input, with a declared overflow strategy (queue with maximum wait, reject, cancel newest, or cancel oldest running), and per-workspace named rate limits (units per window) that task nodes reference, without letting any tenant-defined key cross tenant or workspace scope.
- [ ] **FR-TEN-08:** The system must support bounded run priority tiers inherited by tasks and children, and weighted fairness keys, such that priority orders work only within a tenant's fair share and no workspace exceeds its configured share under contention.

## Falcone services and serverless integration

- [ ] **FR-INT-01:** The system must preserve qualified contracts for db.query, storage.get/put, functions.invoke, events.publish, http.request, email.send, llm.complete, llm.batch and largeTask.run.
- [ ] **FR-INT-02:** The system must enforce per-connector timeout, payload, credential, egress and workspace policies before performing external calls.
- [ ] **FR-INT-03:** The system must invoke falcone-serverless through pinned versions of ctr-worker-execution-api and ctr-job-checkpoint with stable operation keys, authenticated correlation and explicit cancellation outcomes, and must not define a parallel workflow-specific execution or checkpoint protocol.
- [ ] **FR-INT-04:** The system must avoid a runtime dependency cycle: falcone-serverless execution primitives must run without calling Temporal or requiring falcone-workflow to execute themselves.
- [ ] **FR-INT-05:** The system must store large payloads through tenant-scoped Falcone object references with content hashes, retention metadata and authorization checks, using a configured inline threshold and per-run and per-node maximum referenced bytes that are part of quota policy and recorded in the policy snapshot, and failing explicitly when a limit is exceeded.
- [ ] **FR-INT-06:** The system must persist provider job IDs and bounded poll schedules for batch tasks, including cancellation cleanup and credential expiry.

## Monitoring, audit and performance

- [ ] **FR-OBS-01:** The system must expose ordered tenant-scoped history and compatible SSE frames with stable resumable event cursors.
- [ ] **FR-OBS-02:** The system must emit audit events for lifecycle, authorization-sensitive changes, approvals, repair and backend handover.
- [ ] **FR-OBS-03:** The system must measure admission latency, transition throughput, queue age, timer lag, lease expiry, retry rate, outbox lag and database contention.
- [ ] **FR-OBS-04:** The system must propagate trace correlation across Falcone services while redacting secrets and controlling metric cardinality.
- [ ] **FR-OBS-05:** The project must benchmark workflow starts, step transitions, durable waits and activity concurrency independently from Falcone's WebSocket message rate.
- [ ] **FR-OBS-06:** The project must publish achieved availability, latency and recovery results against an agreed workload and resource budget before production cutover.
- [ ] **FR-OBS-07:** The system must evaluate declared per-flow and per-node deadlines (maximum duration from run start, from a schedule's nominal time, or from approval assignment) and on breach must record an SLA event and apply the configured action: notify only, fail, or cancel.
- [ ] **FR-OBS-08:** The system must let authorized users list and count runs within a workspace by status, flow, version, time range, trigger, initiator, and bounded user-defined labels or typed search attributes set at start or by nodes, with indexed filters, stable pagination and per-workspace limits on attribute count, key length and value size.

## Deployment, CI/CD and operations

- [ ] **FR-OPS-01:** The system must deploy using its own database on the shared PostgreSQL cluster within a declared connection budget, and standard namespaced resources without mandatory CRDs, operators, cluster roles or privileged containers.
- [ ] **FR-OPS-02:** The system must run as non-root with arbitrary allowed UID, read-only root filesystem, dropped capabilities and no host access.
- [ ] **FR-OPS-03:** The system must support rolling compatible upgrades, bounded graceful drain and documented rollback limits for schema and interpreter changes, retaining every interpreter version referenced by an open run for at least the longest permitted remaining wait.
- [ ] **FR-OPS-04:** The project must provide tested runbooks for database failover, backup restore, stuck runs, queue overload and key rotation.
- [ ] **FR-OPS-05:** The project must gate releases on contract, isolation, state-machine fault, schema-migration and dependency-security checks.
- [ ] **FR-OPS-06:** The project must assign accountable runtime maintenance, SRE on-call, security review and Falcone product ownership before production release.
- [ ] **FR-OPS-07:** The system must apply cancel, terminate, pause, resume and retry to a filtered set of runs within one workspace as a resumable, rate-limited batch with a dry-run count, per-run outcome and a single audit record referencing all affected runs.

## Temporal migration and retirement

- [ ] **FR-MIG-01:** The project must inventory Temporal-dependent code, active workflow versions, open executions, schedule ownership and task adapters before selecting migration cohorts.
- [ ] **FR-MIG-02:** The project must compare native and Temporal outcomes using deterministic fixtures or isolated effect simulators without doubling production effects.
- [ ] **FR-MIG-03:** The system must route new starts by approved cohort and persist backend ownership for all later run operations.
- [ ] **FR-MIG-04:** The system must keep in-flight Temporal runs on Temporal unless an explicit application-level checkpoint transfer is validated.
- [ ] **FR-MIG-05:** The project must verify no remaining required Temporal runs, schedules, credentials or callers before removing the Temporal deployment and SDK dependencies.
- [ ] **FR-MIG-06:** The project must update Falcone integration documentation and falcone-serverless workflow references to the native contract with a rollback and retention plan.
