# 4. Implementation backlog

12 epics and 47 stories; effort S/M/L is relative, not a delivery estimate. M0 discovery; M1 durable core; M2 integration; M3 migration and qualification.

- **EP-CON — Falcone contracts and developer experience**

Preserve Falcone-facing behavior and establish the exact replacement boundary.

## CON-01 — Inventory and freeze the Falcone workflow contracts

<!-- falcone-workflow:CON-01 -->

## User story

As a Falcone maintainer, I want a versioned contract inventory so that replacement cannot silently change existing behavior.

## Description

Inventory routes, DSL, errors, roles, schedules, monitoring and task envelopes against pinned source and deployed fixtures.

## Acceptance criteria

- [ ] Capture fixtures for definition CRUD, publish, validate, executions, cancel, retry, signal, catalog and schedules.
- [ ] Include existing SSE node-status/log-line/stream-end frames and Last-Event-ID behavior.
- [ ] Record every direct Temporal SDK or API caller as a migration item; raw Temporal SDK and server compatibility is out of scope (ADR 0001).
- [ ] Fixture the legacy behaviors the native engine must reproduce: which triggers use start-or-signal and how their key is derived, what retry means, flow-input required/default enforcement, task-input reference rules, schedule overlap-alias normalisation and the effective retry and timeout defaults injected for absent policies.

## Planning

- Parent: EP-CON
- Phase: M0
- Effort: M
- Depends on: None

## Requirements

- **FR-CON-01:** The system must preserve inventoried Falcone workflow API routes, response schemas, status codes and tenant-scoped identifiers through a compatibility facade.
- **FR-CON-02:** The project must publish a compatibility matrix marking each observed behavior as preserved, intentionally versioned, or a migration blocker.


## CON-02 — Implement the Falcone facade and backend routing

<!-- falcone-workflow:CON-02 -->

## User story

As an application developer, I want stable Falcone APIs so that clients survive the engine migration.

## Description

Introduce a narrow WorkflowBackend interface inside Falcone; separate public compatibility from internal engine routes.

## Acceptance criteria

- [ ] Concurrent identical starts yield one run; reuse of the key with different input returns a conflict.
- [ ] Historic Temporal runs remain queryable and cancellable during mixed operation.
- [ ] Connection failure followed by recovery succeeds without process restart; legacy error mappings are fixture-tested.
- [ ] Business-ID conflict and reuse-after-close policies are fixture-tested, and a key reused after its retention window is documented.
- [ ] Cancel, terminate and retry are fixture-tested as distinct operations: terminate requires a reason and is audited, retry follows the inventoried legacy meaning, children follow FR-DSL-07, and each response reports acceptance separately from the terminal outcome.

## Planning

- Parent: EP-CON
- Phase: M1
- Effort: L
- Depends on: CON-01, DUR-01

## Requirements

- **FR-CON-03:** The system must expose authenticated start, get, list, cancel, retry and signal operations with idempotency keys scoped to (tenant, workspace, flow): the same key with the same input returns the same run for at least max(24 h, the run's retention) and a different input returns a conflict; an optional business ID has a conflict policy (fail or use-existing; terminate-existing is administrator-only) and a reuse-after-close policy (allow, allow-if-failed or reject).
- **FR-CON-04:** The system must route every existing run to its recorded backend and return a retryable service-unavailable response when that backend is unavailable.
- **FR-CON-07:** The system must provide cancel (cooperative: stops new normal work, runs configured cleanup or compensation), terminate (administrative: no further workflow logic, reason required, audited) and retry (the inventoried legacy meaning, recorded either as a linked new run or as a new attempt lineage of the failed node occurrence) as distinct operations with explicit parent/child propagation, each reporting request acceptance separately from the eventual terminal outcome.


## CON-03 — Provide CLI and console integration contracts

<!-- falcone-workflow:CON-03 -->

## User story

As a Falcone user, I want familiar authoring and monitoring tools so that I do not need another workflow portal.

## Description

Use the current console DSL and task catalog; add CLI operations through the same facade.

## Acceptance criteria

- [ ] CLI and console send equivalent requests and display stable error codes.
- [ ] A round-trip through the editor preserves all supported DSL fields.
- [ ] Read-only users can inspect authorized flows but cannot publish definitions.
- [ ] A connector output that violates its pinned output schema fails the node with a typed non-retryable error and no completion is committed.

## Planning

- Parent: EP-CON
- Phase: M2
- Effort: M
- Depends on: CON-02, DSL-01, OBS-01

## Requirements

- **FR-CON-05:** The system must support CLI validate, publish, start, inspect, cancel and retry operations using Falcone authentication.
- **FR-CON-06:** The system must provide versioned task schemas and validation errors usable by Falcone's existing visual editor, preserving the FLW-E001 to FLW-E009 codes, rules and kinds verbatim; new validation rules receive new codes and never reuse existing ones.
- **FR-CON-09:** The system must validate connector outputs against the pinned task output schema before committing a completion, treating a violation as a typed non-retryable error, and must expose input and output schemas to the visual editor for reference completion.


## CON-04 — Add test mode with mocked outputs and simulated time

<!-- falcone-workflow:CON-04 -->

## User story

As a flow author, I want to test branches, timeouts and approvals without live connectors so that I can verify a flow before publishing it.

## Description

Run a flow version against a separate test dispatcher that returns mocked task outputs or errors, advances simulated time and injects signals, events and approval decisions. Share the effect simulator with the MIG-01 differential harness. Expose test mode through the facade API and the CLI.

## Acceptance criteria

- [ ] A test run with mocked outputs produces the same history, error codes and SSE frames as the equivalent live fixture run.
- [ ] Test mode resolves no credentials and its dispatcher has no route to any connector; an attempt to reach one fails the test run.
- [ ] Simulated time fires timers, approval timeouts and schedule occurrences deterministically without wall-clock waiting.
- [ ] Test runs are marked as test runs, emit no production usage events, and their quota treatment is documented.

## Planning

- Parent: EP-CON
- Phase: M2
- Effort: M
- Depends on: CON-03, MIG-01

## Requirements

- **FR-CON-08:** The system must run a flow version in test mode with mocked task outputs or errors, simulated time and injected signals, events and approval decisions, producing the same history, error codes and SSE frames as live execution without resolving credentials or dispatching to any connector, through both the API and the CLI.


- **EP-DSL — DSL interpretation and versioning**

Build a native interpreter for Falcone definitions without executing arbitrary tenant orchestration code.

## DSL-01 — Qualify and compile the existing Falcone DSL

<!-- falcone-workflow:DSL-01 -->

## User story

As a flow author, I want my current definitions to work so that migration does not require rewriting every flow.

## Description

Compile v1.0 graph structure to an immutable execution plan; preserve schema and validator diagnostics.

## Acceptance criteria

- [ ] All existing valid and invalid DSL fixtures produce equivalent results or documented blockers.
- [ ] Compilation stores schema version, plan hash and interpreter version.
- [ ] Repeated node references receive unique execution occurrence IDs while retaining canvas node IDs.
- [ ] Fixtures cover task-input references to flow inputs, run variables and prior node outputs, including missing, null and type-coercion cases; a start that violates a declared flow-input type, required or default rule is rejected with a stable error code and creates no run.

## Planning

- Parent: EP-DSL
- Phase: M0
- Effort: L
- Depends on: CON-01

## Requirements

- **FR-DSL-01:** The system must validate sequence, parallel, task, branch, wait, approval and sub-flow nodes using the inventoried Falcone DSL rules.
- **FR-DSL-02:** The system must reject invalid cycles, duplicate IDs, unknown tasks, dangling references and invalid cron/duration expressions before publishing, reporting the inventoried FLW-E001 to FLW-E009 codes, rules and kinds verbatim.
- **FR-DSL-08:** The system must preserve the inventoried rules by which task and sub-flow inputs reference flow inputs, run variables and prior node-occurrence outputs (reference syntax, evaluation time, missing-reference, null and type-coercion behaviour), and must apply declared flow-input type, required and default rules at admission, rejecting violations with stable error codes before a run is created.


## DSL-02 — Implement bounded expressions and graph semantics

<!-- falcone-workflow:DSL-02 -->

## User story

As a flow author, I want predictable branches and parallel joins so that failures do not change business outcomes.

## Description

Keep CEL semantics compatible with existing fixtures; isolate evaluation and persist selected branches and outputs.

## Acceptance criteria

- [ ] CEL compatibility fixtures cover nulls, numbers, errors and time-sensitive inputs; incompatible expressions block migration.
- [ ] Crash/restart at a branch or join neither duplicates successors nor loses completed branches.
- [ ] Conflicting parallel writes are rejected or resolved by a versioned documented rule; elapsed time is not an implicit merge order.
- [ ] Expressions exceeding a configured length, cost, result-size or input limit fail with a stable error code, and re-evaluating a persisted expression after restart uses the persisted evaluation time.
- [ ] apiVersion v1.0 fixtures reproduce the Temporal outcome when one parallel branch fails while siblings run: fail-fast or wait-all, whether in-flight siblings are cancelled, left running or abandoned, and which sibling results are retained.

## Planning

- Parent: EP-DSL
- Phase: M1
- Effort: L
- Depends on: DSL-01, DUR-01

## Requirements

- **FR-DSL-03:** The system must evaluate expressions with bounded input size, runtime and memory without network, filesystem or arbitrary-code access; maximum expression length, evaluation cost and steps, result size and input bytes are configured per interpreter version, the CEL library version is pinned per interpreter version, and clock functions use the persisted evaluation time, never the wall clock at replay.
- **FR-DSL-04:** The system must persist branch decisions, parallel completion sets and deterministic output-merge behavior before advancing successors; parallel failure and cancellation semantics follow FR-DSL-07.
- **FR-DSL-07:** The system must define per interpreter version, and preserve for apiVersion v1.0, (a) parallel-node failure semantics: fail-fast or wait-all, whether in-flight sibling tasks are cancelled, left running or abandoned, and which sibling results are retained; and (b) child-run behaviour when the parent is cancelled, terminated, fails or times out: terminate, request-cancel or abandon. Both must be fixture-tested against Temporal outcomes.


## DSL-03 — Pin definitions, children and interpreter semantics

<!-- falcone-workflow:DSL-03 -->

## User story

As an operator, I want safe upgrades so that long-running flows retain their intended behavior.

## Description

Version definitions, connector contracts and interpreter semantics independently; retain old interpreters while runs drain.

## Acceptance criteria

- [ ] Publishing a new definition leaves active parent and child runs unchanged.
- [ ] A rolling upgrade with old/new evaluators completes compatible runs and leaves unsupported runs safely parked.
- [ ] Bounded sub-flow depth and expanded graph size prevent recursive resource exhaustion.
- [ ] Cancelling, terminating, failing or timing out a parent applies the inventoried legacy child policy (Temporal's default is terminate) in fixtures; an abandoned child still counts against its tenant's quota.
- [ ] An upgrade cannot remove an interpreter or definition version while an open run references it.

## Planning

- Parent: EP-DSL
- Phase: M1
- Effort: L
- Depends on: DSL-02

## Requirements

- **FR-DSL-05:** The system must pin each run to immutable definition and interpreter versions and each child to an authorized explicit definition version; child behavior on parent cancellation, termination, failure or timeout follows FR-DSL-07.
- **FR-DSL-06:** The system must reject unsupported historical versions, require an explicit audited migration plan before changing active-run semantics, and retain every interpreter and definition version referenced by an open run for at least the longest permitted remaining wait, or migrate the run through FR-DSL-11.


## DSL-04 — Add error boundaries and failure handlers

<!-- falcone-workflow:DSL-04 -->

## User story

As a flow author, I want to catch specific errors, always run cleanup and handle flow failure so that business flows can end gracefully instead of only retrying or failing.

## Description

In an additive DSL version, add error boundaries on task, sub-flow, sequence and parallel nodes that route matching FR-ACT-07 error types to a handler node after retries are exhausted, finalizer nodes for a scope and a flow-level on-failure handler. A boundary handler runs before compensation; compensation runs only when the error escapes the scope. Extend validation so scoped handler edges keep the graph acyclic. apiVersion v1.0 behavior is unchanged.

## Acceptance criteria

- [ ] An error matching a boundary's declared type runs its handler after retries are exhausted and is recorded in history; a non-matching error fails the run exactly as in apiVersion v1.0.
- [ ] Finalizers run once on success, failure and cancellation of their scope, each with its own timeout so cancellation stays bounded; a crash during a finalizer resumes without running it twice.
- [ ] With compensation (HUM-02) enabled, the boundary handler runs first and compensation runs only when the error escapes the scope.
- [ ] Validation rejects handler edges that form a cycle with a new FLW error code; apiVersion v1.0 validation fixtures are unchanged.

## Planning

- Parent: EP-DSL
- Phase: M2
- Effort: L
- Depends on: DSL-03, ACT-02, HUM-02

## Requirements

- **FR-DSL-09:** In an additive DSL version, the system must support error boundaries on task, sub-flow, sequence and parallel nodes that route errors matching declared error types (after retries are exhausted) to a declared handler node, optional finalizer nodes that run on success, failure or cancellation of their scope, and a flow-level on-failure handler; caught errors must be recorded in history, and uncaught errors must fail the run exactly as in v1.0.


## DSL-05 — Add dynamic fan-out over runtime collections

<!-- falcone-workflow:DSL-05 -->

## User story

As a flow author, I want to run a task or sub-flow for each item of a runtime list so that per-file, per-record and per-prompt processing needs no fixed number of branches.

## Description

Add a map node in an additive DSL version with a declared maximum item count, maximum concurrency, failure policy and index-ordered output. Reserve fan-out quota at expansion time, persist per-item occurrence state, store item results as object references and chunk large collections into child runs.

## Acceptance criteria

- [ ] A collection over the declared maximum item count is rejected before expansion is committed; expansion reserves fan-out quota (FR-TEN-05) and fails explicitly when the quota is exceeded.
- [ ] A crash during expansion or item execution neither duplicates nor drops items; per-item occurrence IDs are stable across recovery.
- [ ] Fail-fast, continue and minimum success count or ratio policies produce the documented run outcome, and the output collection is ordered by item index regardless of completion order.
- [ ] Running items never exceed the declared concurrency, and one tenant's large map does not starve other tenants in the TEN-03 fairness benchmark.

## Planning

- Parent: EP-DSL
- Phase: M2
- Effort: L
- Depends on: DSL-03, TEN-03

## Requirements

- **FR-DSL-10:** The system must support a map node that runs a task or sub-flow for each element of a runtime collection with a declared maximum item count, maximum concurrency, failure policy (fail-fast, continue, or minimum success count or ratio) and index-ordered output collection, reserving fan-out quota at expansion time and persisting per-item occurrence state so that a crash neither duplicates nor drops items.


## DSL-06 — Migrate in-flight runs between flow versions

<!-- falcone-workflow:DSL-06 -->

## User story

As a workspace operator, I want to move waiting runs to a corrected version of the same flow so that a definition fix can reach runs that wait for months.

## Description

Native-to-native only: migrate selected waiting or running native runs to another published version of the same flow using an explicit node-occurrence mapping, validated in a dry run and applied atomically per run. This is not a Temporal-history converter (FR-MIG-04). Credential lineage, quota reservations and absolute timer due times carry over unchanged.

## Acceptance criteria

- [ ] A dry run lists, per selected run, the mapped node occurrences and every reason a run cannot be migrated, without changing any run.
- [ ] Migration is rejected when an active task, timer or approval lacks a mapping or a mapping changes node type or scope.
- [ ] An applied migration commits atomically per run under the expected revision, keeps absolute timer due times, credential lineage and quota reservations, and records actor, reason and both versions in audit.
- [ ] A stale run revision fails that run's migration without partial changes.

## Planning

- Parent: EP-DSL
- Phase: M3
- Effort: L
- Depends on: DSL-03, OBS-01

## Requirements

- **FR-DSL-11:** The system must migrate selected waiting or running native runs to another published version of the same flow using an explicit node-occurrence mapping that is validated in a dry run, applied atomically per run under the expected revision and recorded in audit, and must reject migration when an active task, timer or approval lacks a mapping or the mapping changes node type or scope.


- **EP-DUR — Durable state and recovery**

Make PostgreSQL transactions the authoritative boundary for workflow progress.

## DUR-01 — Implement the transactional run state machine

<!-- falcone-workflow:DUR-01 -->

## User story

As a platform engineer, I want atomic state transitions so that crashes cannot lose accepted work.

## Description

Persist run state, history, ready work and outbox records in one transaction with optimistic revisions.

## Acceptance criteria

- [ ] Fault injection before/after commit proves that acknowledged starts remain discoverable.
- [ ] Two evaluators racing one revision produce exactly one committed transition.
- [ ] No production in-memory fallback exists when PostgreSQL is unavailable.

## Planning

- Parent: EP-DUR
- Phase: M1
- Effort: L
- Depends on: DSL-01

## Requirements

- **FR-DUR-01:** The system must acknowledge a start only after committing the run, pinned plan, first ready work, audit event and idempotency record.
- **FR-DUR-02:** The system must commit each state transition, ordered per-run event and generated work atomically under a checked revision.


## DUR-02 — Add task leases, fencing and recovery scans

<!-- falcone-workflow:DUR-02 -->

## User story

As an SRE, I want workers to recover abandoned tasks so that node failure does not strand runs.

## Description

Claim ready tasks with bounded leases, database time, monotonic attempt fencing and periodic reconciliation, using the shared Falcone lease/fencing module that falcone-serverless story STO-03 builds in Falcone instead of an engine-specific implementation.

## Acceptance criteria

- [ ] Kill a worker after claim and verify another claims after expiry.
- [ ] An old worker completion cannot change a newer attempt or terminal run.
- [ ] DB disconnection stops new dispatch; bounded reconnection resumes scanning without manual repair.

## Planning

- Parent: EP-DUR
- Phase: M1
- Effort: L
- Depends on: DUR-01

## Requirements

- **FR-DUR-03:** The system must reject task completions and heartbeats with expired or superseded lease generations.
- **FR-DUR-04:** The system must recover abandoned tasks through durable scans even when all optional notifications are lost.


## DUR-03 — Bound history and verify disaster recovery

<!-- falcone-workflow:DUR-03 -->

## User story

As an operator, I want recoverable compact state so that months-long runs do not create unbounded replay costs.

## Description

Use explicit continuations and snapshots; preserve audit order and payload references through archival.

## Acceptance criteria

- [ ] Restore an encrypted backup into an isolated environment and complete waiting and running fixtures.
- [ ] Compacted runs retain a contiguous inspectable event lineage or an explicit archive cursor.
- [ ] Recovery reports possible post-backup external effects and prevents automatic duplicate dispatch until reconciled.
- [ ] A run that exceeds a segment limit continues under the same public run ID, and an SSE client resumes across the segment boundary without gaps.
- [ ] Closed runs past the workspace retention period are deleted with their payload objects unless a legal hold applies; erasure for a data subject removes linked payload objects while keeping redacted structural history; every deletion is audited.

## Planning

- Parent: EP-DUR
- Phase: M3
- Effort: L
- Depends on: DUR-02, OPS-02

## Requirements

- **FR-DUR-05:** The system must bound event history and payload growth using configured limits and resumable continuation or archival policies: a run segment has a configured maximum event count and byte size, and continuation keeps the public run ID, links segments and keeps SSE cursors (FR-OBS-01) monotonic across segments.
- **FR-DUR-06:** The system must restore database and referenced object payloads to a consistent recovery point and reconcile external effects before resuming dispatch.
- **FR-DUR-07:** The system must apply a per-workspace retention period to closed runs within quota limits, support authorized deletion of individual closed runs and their payload objects with audit, and support erasure of payload objects linked to a data subject while preserving redacted structural history, honoring legal-hold flags that suspend deletion.


- **EP-ACT — Task execution and long-running work**

Separate orchestration from side effects and enforce honest delivery semantics.

## ACT-01 — Define the native activity worker protocol

<!-- falcone-workflow:ACT-01 -->

## User story

As a connector maintainer, I want an engine-neutral task context so that Falcone adapters no longer import Temporal.

## Description

Specify claim, heartbeat, complete and fail messages with run/occurrence/attempt identity and credentials.

## Acceptance criteria

- [ ] A native worker executes a test connector without any Temporal SDK import.
- [ ] Invalid tenant, adapter version or lease metadata is rejected before connector I/O.
- [ ] Production dispatch cannot reach the legacy echo/mock fallback.

## Planning

- Parent: EP-ACT
- Phase: M1
- Effort: L
- Depends on: DUR-02

## Requirements

- **FR-ACT-01:** The system must dispatch tasks through a versioned protocol carrying tenant, workspace, run, node occurrence, attempt, lease generation and pinned adapter version.
- **FR-ACT-02:** The system must execute side effects only in authorized workers and must reject unknown task types in production.


## ACT-02 — Implement retries, deadlines and side-effect safety

<!-- falcone-workflow:ACT-02 -->

## User story

As a workflow author, I want controlled retries so that transient failures recover without uncontrolled duplicate effects.

## Description

Use stable business-operation idempotency keys across attempts, typed errors and durable retry timers.

## Acceptance criteria

- [ ] Inject a crash after external success but before completion commit; idempotent connector deduplicates the retry.
- [ ] Non-idempotent connector enters reconciliation-required when success is ambiguous.
- [ ] Run cancellation and retry budgets terminate new attempts without erasing prior outcomes.
- [ ] A v1.0 task without a retry policy compiles to a plan recording the effective legacy defaults (Temporal: unlimited attempts, 1 s initial interval, coefficient 2.0, maximum 100 × initial); fixtures verify the backoff formula and each timeout kind.
- [ ] An error whose type is listed in nonRetryableErrors fails without retry; an unknown legacy error-type name in a definition is reported as a migration blocker, not ignored.

## Planning

- Parent: EP-ACT
- Phase: M1
- Effort: L
- Depends on: ACT-01, TIM-01

## Requirements

- **FR-ACT-03:** The system must apply the retry fields maxAttempts (at least 1), initialInterval, backoffCoefficient (at least 1), maximumInterval and nonRetryableErrors (FR-ACT-07 types) with delay(n) = min(initialInterval × backoffCoefficient^(n−1), maximumInterval), and the timeouts scheduleToStart (queue wait), startToClose (per attempt), scheduleToClose (all attempts), heartbeat (at most startToClose) and a run-level executionTimeout (none for apiVersion v1.0); the compiled plan of a v1.0 definition must store the effective legacy defaults explicitly, including those injected for absent policies or timeouts; optional jitter and a connector-supplied next-delay override belong to a new apiVersion and never extend maxAttempts or scheduleToClose.
- **FR-ACT-04:** The system must classify each catalog connector as idempotent-by-key, reconcilable (read-after-timeout) or non-idempotent, use that class for retry eligibility, the repair preview (FR-HUM-08) and ambiguous-outcome incidents (FR-HUM-09), block blind retries of non-idempotent connectors regardless of maxAttempts, and surface ambiguous external outcomes instead of promising universal exactly-once effects.
- **FR-ACT-07:** The system must classify every task, expression and connector failure with a stable error type from a versioned taxonomy (at least validation, authorization, timeout, communication, rate-limited, ambiguous-outcome, cancelled and connector-specific types), and must evaluate nonRetryableErrors for apiVersion v1.0 definitions against the inventoried legacy Temporal error-type names emitted by each catalog task.


## ACT-03 — Support asynchronous jobs and checkpoints

<!-- falcone-workflow:ACT-03 -->

## User story

As a data analyst, I want long-running tasks to survive worker restarts so that analysis is resumable.

## Description

Separate job submission, observation, checkpoint and result retrieval; avoid holding orchestration processes during waits. Checkpoints use the falcone-serverless job checkpoint contract (ctr-job-checkpoint).

## Acceptance criteria

- [ ] A worker dies after job submission; reconciliation finds the same external job.
- [ ] A cancelled job cannot report the workflow completed; delayed cleanup is visible and retried under policy.
- [ ] A capability-qualified checkpoint resumes correctly; unsupported native workloads remain migration blockers.
- [ ] A run waiting for the configured multi-month maximum in a simulated-time test resumes with renewed credentials after a Keycloak session or offline-token expiry, on its pinned interpreter version.

## Planning

- Parent: EP-ACT
- Phase: M2
- Effort: L
- Depends on: ACT-02, INT-02

## Requirements

- **FR-ACT-05:** The system must persist external job IDs and checkpoint references and resume observation after worker loss without blindly resubmitting the job.
- **FR-ACT-06:** The system must support waits, approvals and timers lasting months, up to a policy maximum set by the product owner, with bounded heartbeat, cancellation and credential-renewal policies, and must exercise credential renewal (FR-TEN-04) in a test that crosses a Keycloak session or offline-token expiry.


- **EP-TIM — Timers and schedules**

Replace Temporal timers and schedules with durable Falcone-owned scheduling.

## TIM-01 — Implement durable timers and race resolution

<!-- falcone-workflow:TIM-01 -->

## User story

As a workflow author, I want durable delays so that waits survive outages.

## Description

Store due timestamps in PostgreSQL, use database time and serialize timer firing with signals/cancellation.

## Acceptance criteria

- [ ] Restart all engine pods while a timer is pending; it fires after recovery.
- [ ] Race an approval, timeout and cancellation and verify one accepted outcome and audited losers.
- [ ] Clock skew between workers does not move a database-timed deadline earlier.
- [ ] A computed wait-until instant is persisted when the timer is armed and is not re-evaluated after restart or upgrade; an instant given in a named time zone fires at the correct UTC instant across a DST change.

## Planning

- Parent: EP-TIM
- Phase: M1
- Effort: M
- Depends on: DUR-01

## Requirements

- **FR-TIM-01:** The system must persist wait and retry timers and fire each logical timer at most once into workflow state.
- **FR-TIM-02:** The system must resolve simultaneous signal, timeout and cancellation transitions with one documented transactional ordering rule.
- **FR-TIM-07:** The system must support waiting until an absolute instant or a CEL-computed instant with an explicit IANA time zone, evaluated once and persisted before the timer is armed.


## TIM-02 — Replace flow schedules with compatible controls

<!-- falcone-workflow:TIM-02 -->

## User story

As a workspace owner, I want existing cron controls so that scheduled automation remains operable.

## Description

Preserve one schedule per flow and public list/get/pause/resume/trigger responses; persist occurrence identity.

## Acceptance criteria

- [ ] Fixtures match the current schedule API, including absent and foreign schedules.
- [ ] Concurrent schedulers create one run per occurrence and enforce overlap policy.
- [ ] DST transitions and outage catch-up produce documented bounded outcomes.
- [ ] Each of the eight overlap names and an absent catchupWindow have fixtures matching the inventoried legacy outcome.
- [ ] Trigger-now is audited and applies the overlap policy unless overridden; a schedule past its end bound or maximum action count, or paused on failure, admits no further occurrences.

## Planning

- Parent: EP-TIM
- Phase: M2
- Effort: L
- Depends on: TIM-01, CON-02

## Requirements

- **FR-TIM-03:** The system must preserve Falcone schedule identities, published cron text, next-action times, the inventoried number of retained recent actions and idempotent pause/resume behavior; trigger-now and pause/resume notes follow FR-TIM-08.
- **FR-TIM-04:** The system must preserve the eight DSL overlap names (skip, allow, allow_all, buffer, buffer_one, buffer_all, cancel_other, terminate_other) with their inventoried normalisation and skip as the default, use the inventoried effective catch-up window when catchupWindow is absent, evaluate apiVersion v1.0 schedules in UTC, run a nonexistent local time once at the next valid instant and an ambiguous local time once at its first occurrence for time-zone-aware schedules (a new field), and atomically deduplicate each occurrence by (schedule ID, nominal UTC instant); pausing does not affect admitted runs and manual triggers are not bound by the catch-up window.
- **FR-TIM-08:** The system must support optional schedule start and end bounds, bounded jitter, a maximum action count, pause-on-failure, an operator note on pause and resume, and an audited trigger-now action that applies the schedule's overlap policy unless overridden.


## TIM-03 — Coordinate schedule cutover and backfill

<!-- falcone-workflow:TIM-03 -->

## User story

As an operator, I want one active schedule owner so that migration cannot double-fire workflows.

## Description

Add backend ownership epochs, bounded backfill and reconciliation against legacy schedule state.

## Acceptance criteria

- [ ] Pause legacy admission, reconcile accepted occurrences, transfer the ownership epoch and resume the new scheduler.
- [ ] A stale schedule owner cannot admit runs after handover.
- [ ] Backfill cancellation stops future admissions without deleting already accepted runs.
- [ ] A second backfill on a schedule with an active backfill is rejected, and each reprocess mode selects the documented occurrences in fixtures.

## Planning

- Parent: EP-TIM
- Phase: M3
- Effort: L
- Depends on: TIM-02, MIG-02

## Requirements

- **FR-TIM-05:** The system must fence schedule ownership during backend handover so only one engine may admit an occurrence.
- **FR-TIM-06:** The system must support audited bounded backfill over [start, end) with a reprocess mode (missing only, missing and failed, or all), an order (oldest first by default, newest first optional), a concurrency cap independent of live scheduling and the schedule's overlap policy; backfill is exempt from the catch-up window, limited to one active backfill per schedule with a maximum occurrence count, can be paused and cancelled, and offers a dry run listing candidate occurrences and quota impact.


- **EP-EVT — Events and trigger delivery**

Use Falcone's existing event infrastructure with durable inbox/outbox semantics.

## EVT-01 — Add inbox and outbox integration

<!-- falcone-workflow:EVT-01 -->

## User story

As a platform engineer, I want durable event delivery so that broker outages cannot lose workflow transitions.

## Description

Use Kafka as transport and PostgreSQL as state authority; enforce tenant-bound event identities. Use the shared Falcone outbox/inbox module that falcone-serverless story STO-03 builds in Falcone instead of an engine-specific implementation.

## Acceptance criteria

- [ ] Crash between DB commit and broker acknowledgement; redelivery causes no second logical admission.
- [ ] Crash after publish but before outbox acknowledgement; consumer deduplication handles repeat delivery.
- [ ] Broker unavailability accumulates bounded backlog and exposes age/size metrics.

## Planning

- Parent: EP-EVT
- Phase: M1
- Effort: L
- Depends on: DUR-01

## Requirements

- **FR-EVT-01:** The system must persist incoming trigger/event deduplication records and resulting workflow transitions before acknowledging delivery.
- **FR-EVT-02:** The system must publish committed outgoing events, including the FR-EVT-09 lifecycle event catalogue, through a retryable transactional outbox with stable event IDs.


## EVT-02 — Preserve webhook and platform-event triggers

<!-- falcone-workflow:EVT-02 -->

## User story

As a Falcone user, I want existing event triggers so that my automations continue to start securely.

## Description

Reuse Falcone HMAC webhook validation and structural tenant/workspace event routing.

## Acceptance criteria

- [ ] Invalid signature, expired replay window and oversized request are rejected before admission.
- [ ] Foreign workspace identifiers cannot reroute an event.
- [ ] Publish/update/delete registration reconciliation has no unbounded stale listeners.
- [ ] Concurrent deliveries for one business key yield at most one open run and every signal is delivered; a caller-supplied tenant or workspace field cannot change the derived key.

## Planning

- Parent: EP-EVT
- Phase: M2
- Effort: L
- Depends on: EVT-01, TEN-01

## Requirements

- **FR-EVT-03:** The system must authenticate webhook triggers with rotation-aware signatures, replay protection and size limits.
- **FR-EVT-04:** The system must derive tenant and workspace from verified trigger registration rather than caller-supplied payload fields.
- **FR-EVT-07:** For each inventoried trigger that uses start-or-signal semantics, the system must derive a tenant- and workspace-scoped business key from the verified trigger registration and event, and in one transaction either deliver the signal to the open run holding that key or start a new run and deliver the signal to it, so that concurrent deliveries for one key yield at most one open run and no lost signal.


## EVT-03 — Implement correlated signals and event waits

<!-- falcone-workflow:EVT-03 -->

## User story

As a workflow author, I want durable external signals so that workflows can wait without active threads.

## Description

Persist ordered signal inboxes, bounded early-arrival buffers and explicit correlation policies.

## Acceptance criteria

- [ ] Signal-before-wait survives restart and is consumed by its intended occurrence.
- [ ] Duplicate and unauthorized signals do not unblock additional nodes.
- [ ] Overflow and stale signals produce documented errors/dead-letter records without tenant data leakage.
- [ ] Signal and approval-decision requests return accepted, rejected by validation, target not waiting, duplicate or run terminal after commit, and an invalid payload is never persisted.

## Planning

- Parent: EP-EVT
- Phase: M2
- Effort: L
- Depends on: EVT-01, TIM-01

## Requirements

- **FR-EVT-05:** The system must persist authorized signals using deduplication IDs and explicit run/node-occurrence correlation.
- **FR-EVT-06:** The system must take the TTL and per-run capacity for unmatched or early-arriving signals from quota policy, consume buffered signals FIFO per signal name, deduplicate them by signal ID while buffered and for the run's retention after consumption, reject a signal to a terminal run with an explicit error code and record it, and deliver a signal matching several waits to the earliest-armed node occurrence.
- **FR-EVT-11:** The system must return, after commit, a synchronous result for signals and approval decisions (accepted, rejected by validation, target not waiting, duplicate, or run terminal), validating the payload before it is persisted.


## EVT-04 — Add callback-token and event-or-timeout waits

<!-- falcone-workflow:EVT-04 -->

## User story

As a flow author, I want to wait for an external callback or a correlated event with a timeout so that flows can integrate with e-signature, payment and partner systems that answer later.

## Description

In an additive DSL version, add a callback wait node that issues a single-use signed completion token or URL bound to tenant and node occurrence, and an event-wait node that races a correlated platform event or signal against a timeout. Tokens are bearer capabilities: keep them short-lived, never log them, revoke them on cancellation, keep tenant identifiers out of the URL path and rate-limit the endpoint per tenant.

## Acceptance criteria

- [ ] A callback token accepts exactly one authenticated completion; a second use, an expired or revoked token, a token for another tenant or node occurrence and an oversized or schema-invalid payload are rejected and recorded.
- [ ] Completion, timeout and cancellation races resolve by the FR-TIM-02 ordering rule with one recorded winner.
- [ ] Tokens never appear in logs, history or metrics, and cancelling the run revokes its outstanding tokens.
- [ ] An event wait records whether the event or the timeout won, with the event reference; an early matching event is governed by FR-EVT-06, and matching uses the correlation-key index, never a payload scan.

## Planning

- Parent: EP-EVT
- Phase: M2
- Effort: L
- Depends on: EVT-03, TIM-01, TEN-01

## Requirements

- **FR-EVT-08:** The system must provide a callback wait node that issues a single-use, signed, tenant- and node-occurrence-bound completion token or URL with an expiry, accepts exactly one authenticated completion (success, failure, or progress heartbeat) validated against a declared payload schema and size limit, and resolves completion, timeout and cancellation races with the FR-TIM-02 ordering rule.
- **FR-EVT-12:** The system must support an event-wait node that waits for a correlated platform event or signal matching a declared filter, with a timeout, and records which condition won together with the event reference.


## EVT-05 — Publish lifecycle events and add trigger filters

<!-- falcone-workflow:EVT-05 -->

## User story

As a workspace administrator, I want lifecycle events and filtered triggers so that I can notify on failure, chain flows and start runs only for relevant events.

## Description

Define a versioned CloudEvents lifecycle catalogue for run and node-occurrence transitions, published through the outbox; node-level events are opt-in per flow. Add a CEL filter and an input mapping to platform-event and webhook triggers. Bound flow-to-flow chains with a causation ID.

## Acceptance criteria

- [ ] Each catalogued transition emits one CloudEvent with a stable ID through the outbox; events carry identifiers, versions and object references, and scans find no secrets or unredacted payload values.
- [ ] Node-level lifecycle events are emitted only for flows that opt in.
- [ ] A run started by another flow's lifecycle event carries a causation ID, and a chain that exceeds the configured depth is rejected and recorded.
- [ ] A trigger whose filter rejects an event admits no run and records the decision in the delivery record; filter and mapping errors produce stable error codes.

## Planning

- Parent: EP-EVT
- Phase: M2
- Effort: M
- Depends on: EVT-01, EVT-02

## Requirements

- **FR-EVT-09:** The system must publish versioned CloudEvents-formatted lifecycle events for run and node-occurrence transitions (started, completed, failed, cancelled, terminated, waiting for approval or callback, incident opened and resolved, SLA breached) through the outbox, carrying identifiers, versions and object references but no secrets or unredacted payload values.
- **FR-EVT-10:** The system must support a CEL filter over the verified event and an input mapping for each platform-event and webhook trigger, evaluated before admission and recorded in the trigger's delivery record.


- **EP-HUM — Human approvals and compensation**

Extend Falcone business workflows with auditable decisions and recoverable cleanup.

## HUM-01 — Preserve human approval behavior

<!-- falcone-workflow:HUM-01 -->

## User story

As a reviewer, I want authorized approval decisions so that sensitive steps need accountable consent.

## Description

Preserve existing flowApproval/human-approval semantics at the facade while binding decisions to authenticated actors.

## Acceptance criteria

- [ ] Forged actor fields are ignored or rejected; an unauthorized reviewer cannot decide.
- [ ] Concurrent approval submissions produce one accepted decision and auditable conflicts.
- [ ] Legacy untargeted approval behavior is explicitly fixture-tested; stricter occurrence targeting uses a versioned change.
- [ ] Outcome fixtures contain every outcome field; rejection and timeout produce the approval.rejected and approval.timeout error types while apiVersion v1.0 run outcomes match the legacy fixtures.

## Planning

- Parent: EP-HUM
- Phase: M2
- Effort: M
- Depends on: EVT-03, TEN-01

## Requirements

- **FR-HUM-01:** The system must derive approval actor identity from verified authentication and enforce configured reviewer permissions.
- **FR-HUM-02:** The system must preserve approval outcome fields as {decision, actor subject, actor display name, decided-at, comment, decision revision, source (UI or API)}, distinguish rejection, timeout and cancellation, produce the declared default outcome or the approval.timeout error type on timeout, and raise the approval.rejected error type on rejection so that error boundaries (FR-DSL-09) can route it in a new DSL version.


## HUM-02 — Add versioned saga compensation

<!-- falcone-workflow:HUM-02 -->

## User story

As a business process owner, I want compensating actions so that partial success can be repaired.

## Description

Add an opt-in DSL extension for compensation, leaving v1.0 behavior intact.

## Acceptance criteria

- [ ] A failed later task compensates only committed successful predecessors.
- [ ] A crash during compensation resumes without skipping or blindly duplicating completed cleanup.
- [ ] UI/API distinguish failed, compensating, compensated and compensation-failed without rewriting history.

## Planning

- Parent: EP-HUM
- Phase: M2
- Effort: L
- Depends on: ACT-02, DSL-03

## Requirements

- **FR-HUM-03:** The system must record completed compensatable operations and schedule configured compensations in dependency-safe reverse order.
- **FR-HUM-04:** The system must track compensation retries, failures and manual intervention separately from the original task outcome.


## HUM-03 — Provide audited operator repair actions

<!-- falcone-workflow:HUM-03 -->

## User story

As an authorized operator, I want controlled repair tools so that ambiguous outcomes can be resolved safely.

## Description

Support retry-from-known-boundary, run-level repair operations and reconciliation acknowledgements; disallow arbitrary history edits. Represent every condition that needs human resolution as a typed incident.

## Acceptance criteria

- [ ] Stale revision or cross-tenant repair requests fail before mutation.
- [ ] Preview identifies side effects that may repeat and requires a documented resolution for ambiguous tasks.
- [ ] Every accepted repair records actor, reason, prior revision and resulting attempt lineage.
- [ ] Pause stops new dispatch for the run and resume restarts it; retry in place, skip with a schema-valid output, set variables and rerun from a node are each fixture-tested, and an output or variable that fails its schema is rejected.
- [ ] Each listed incident condition opens a typed incident that stops dispatch on that path and emits a lifecycle event; the incident closes only through an audited resolution action.

## Planning

- Parent: EP-HUM
- Phase: M3
- Effort: L
- Depends on: HUM-02, OBS-01, EVT-05

## Requirements

- **FR-HUM-05:** The system must require authorization, reason and expected run revision for manual repair or retry actions, including the FR-HUM-08 run operations.
- **FR-HUM-06:** The system must preserve original history and create explicit linked attempts or continuation records for repair.
- **FR-HUM-08:** The system must provide authorized, audited run operations (pause and resume dispatch; retry a failed node occurrence in place; skip a node with an operator-supplied, schema-valid output; set run variables; and rerun from a selected node as a new linked run pinned to the original or an explicitly selected compatible version), each requiring the expected run revision and showing a preview of side effects that may repeat according to connector idempotency class.
- **FR-HUM-09:** The system must represent each condition that requires human resolution (retries exhausted under an alert-only timeout policy, ambiguous external outcome, expression evaluation error, missing or hash-mismatched payload, expired or revoked credential, policy-blocked effect, undeliverable signal) as a typed incident on the affected node occurrence that stops dispatch on that path, emits a lifecycle event, and closes only through an audited resolution action.


## HUM-04 — Add human-task forms, quorum and escalation

<!-- falcone-workflow:HUM-04 -->

## User story

As a business process owner, I want approvals with typed forms, quorum, separation of duties and escalation so that approval steps match our review policies.

## Description

Extend approval nodes in an additive DSL version with a versioned response schema, assignment by user, Keycloak group or role expression, quorum rules, optional prohibition of approval by the run initiator, non-interrupting reminder and escalation timers and a declared default outcome on timeout. Resolve group membership at decision time and persist a snapshot. Notifications use lifecycle events. apiVersion v1.0 approvals are unchanged.

## Acceptance criteria

- [ ] A response that does not match the versioned response schema is rejected before it is persisted.
- [ ] Any, all and N-of-M quorum rules complete only when satisfied, using HUM-01's single-winner transaction under concurrent responses; the run initiator cannot approve when that prohibition is configured.
- [ ] Reminder and escalation timers fire without interrupting the approval, and a timeout applies the declared default outcome.
- [ ] Every response, reassignment and escalation is audited with the group-membership snapshot used for the decision; apiVersion v1.0 approval fixtures are unchanged.

## Planning

- Parent: EP-HUM
- Phase: M2
- Effort: L
- Depends on: HUM-01, TIM-01, EVT-05

## Requirements

- **FR-HUM-07:** The system must support approval nodes with a versioned response schema (choices and typed fields), assignment by user, Keycloak group or role expression, quorum rules (any, all, or N of M), optional prohibition of approval by the run initiator, reminder and escalation timers that do not interrupt the approval, and a declared default outcome on timeout. Every response, reassignment and escalation must be recorded in audit history.


- **EP-TEN — Security, tenancy and Falcone quotas**

Keep identity, policy and resource accounting under Falcone ownership.

## TEN-01 — Preserve tenant and workspace authorization

<!-- falcone-workflow:TEN-01 -->

## User story

As a tenant administrator, I want strict isolation so that no other tenant can observe or operate my workflows.

## Description

Use verified Keycloak/Falcone identity, deny-by-default engine authorization, PostgreSQL RLS and explicit workspace binding.

## Acceptance criteria

- [ ] Cross-tenant and cross-workspace negative tests cover API, worker completion, SSE and object references.
- [ ] RLS is enforced for application-role queries and pooled connections cannot retain prior tenant context.
- [ ] Production trusts only authenticated gateway/service identities; injected headers or body tenant IDs cannot elevate access.

## Planning

- Parent: EP-TEN
- Phase: M1
- Effort: L
- Depends on: CON-01, DUR-01

## Requirements

- **FR-TEN-01:** The system must enforce tenant/workspace ownership for definitions, runs, events, schedules, payloads and monitoring streams using verified identity.
- **FR-TEN-02:** The system must preserve Falcone definition-write role restrictions and test authorization on every execution lifecycle operation.


## TEN-02 — Replace Temporal-bound credentials safely

<!-- falcone-workflow:TEN-02 -->

## User story

As a security engineer, I want native execution credentials so that activities retain least privilege after migration.

## Description

Replace Temporal ancestry lookup with authoritative native run lineage; use short-lived capabilities and secret references.

## Acceptance criteria

- [ ] Foreign, expired, revoked and sibling-run references fail closed.
- [ ] Children and retries inherit only declared scope using recorded lineage, never caller-provided ancestry.
- [ ] History/log scans contain no raw execution tokens; credential-store outage produces a bounded retryable failure.

## Planning

- Parent: EP-TEN
- Phase: M1
- Effort: L
- Depends on: TEN-01, ACT-01

## Requirements

- **FR-TEN-03:** The system must bind execution credential references to authoritative tenant, workspace, root run and allowed child lineage before connector use.
- **FR-TEN-04:** The system must renew or reauthorize long-lived runs under Falcone policy without storing bearer tokens or secret values in history.


## TEN-03 — Implement fair admission and quota accounting

<!-- falcone-workflow:TEN-03 -->

## User story

As a Falcone operator, I want centrally managed limits so that retries and noisy tenants cannot exhaust capacity.

## Description

Separate stored definitions, waiting runs, runnable steps, external activities and message rate; integrate Falcone policy and billing ledgers.

## Acceptance criteria

- [ ] Concurrent admissions cannot exceed a configured hard limit; expired reservations are reconciled.
- [ ] With one tenant saturating its share, other tenants' p95 ready-task dispatch latency stays within the agreed factor of their unloaded baseline in the OBS-03 benchmark.
- [ ] Billing fixtures classify retries, failures, waits and cancellations explicitly; workflow does not invent independent tariff rules.

## Planning

- Parent: EP-TEN
- Phase: M2
- Effort: L
- Depends on: DUR-02, TEN-02

## Requirements

- **FR-TEN-05:** The system must consume versioned Falcone quota policy for starts, active tasks, waiting runs, retries, fan-out, payload bytes and retention.
- **FR-TEN-06:** The system must enforce fair tenant/workspace admission with idempotent reservations, releases and usage events across crashes, using weighted round-robin across tenants and then across workspaces within a tenant, with weights from quota policy.


## TEN-04 — Add flow concurrency, rate limits and priority

<!-- falcone-workflow:TEN-04 -->

## User story

As a workspace administrator, I want per-flow and per-key concurrency limits, rate limits and priorities so that flows respect partner limits and urgent work runs first without hurting other tenants.

## Description

Add optional concurrency limits per flow and per key (a bounded CEL expression over verified run input) with an overflow strategy, per-workspace named rate limits referenced by task nodes, bounded priority tiers and weighted fairness keys. Priority never overrides tenant fairness; distinct keys per workspace are capped; queued runs count as waiting runs for quota.

## Acceptance criteria

- [ ] A per-key limit of one admits one open run per key; queue with maximum wait, reject, cancel-newest and cancel-oldest overflow strategies produce the documented outcomes.
- [ ] A key expression cannot reach another tenant's or workspace's scope, and the per-workspace distinct-key cap is enforced.
- [ ] Task nodes that reference a named rate limit never exceed its units per window.
- [ ] Higher-priority work is dispatched first only within the tenant's fair share; under contention no workspace exceeds its configured share in the benchmark.

## Planning

- Parent: EP-TEN
- Phase: M2
- Effort: L
- Depends on: TEN-03, DSL-02

## Requirements

- **FR-TEN-07:** The system must enforce optional per-flow and per-key concurrency limits, where the key is a bounded CEL expression over verified run input, with a declared overflow strategy (queue with maximum wait, reject, cancel newest, or cancel oldest running), and per-workspace named rate limits (units per window) that task nodes reference, without letting any tenant-defined key cross tenant or workspace scope.
- **FR-TEN-08:** The system must support bounded run priority tiers inherited by tasks and children, and weighted fairness keys, such that priority orders work only within a tenant's fair share and no workspace exceeds its configured share under contention.


- **EP-INT — Falcone services and serverless integration**

Port first-party adapters and define the boundary with falcone-serverless.

## INT-01 — Port the existing first-party task catalog

<!-- falcone-workflow:INT-01 -->

## User story

As a Falcone developer, I want current task types to work so that workflows remain useful on day one.

## Description

Extract engine-neutral activity context for DB, storage, functions, events, HTTP, email and LLM tasks.

## Acceptance criteria

- [ ] Each task type has success/error/cancellation/duplicate-attempt fixtures, a mapping from every legacy Temporal error type it emits to its FR-ACT-07 type, and an explicit migration status.
- [ ] HTTP SSRF tests cover redirects, DNS resolution, private/metadata targets and credential forwarding.
- [ ] External effects run against controlled test services; existing mocks are never reported as live qualification.

## Planning

- Parent: EP-INT
- Phase: M2
- Effort: L
- Depends on: ACT-02, TEN-02

## Requirements

- **FR-INT-01:** The system must preserve qualified contracts for db.query, storage.get/put, functions.invoke, events.publish, http.request, email.send, llm.complete, llm.batch and largeTask.run.
- **FR-INT-02:** The system must enforce per-connector timeout, payload, credential, egress and workspace policies before performing external calls.


## INT-02 — Consume the falcone-serverless execution and checkpoint contracts

<!-- falcone-workflow:INT-02 -->

## User story

As a platform developer, I want one shared invocation contract so that workflow and serverless can evolve independently.

## Description

Consume falcone-serverless's worker execution API (ctr-worker-execution-api) and job checkpoint contract (ctr-job-checkpoint) instead of defining a workflow-specific protocol. Keep workflow state in falcone-workflow and untrusted computation in falcone-serverless; the serverless Temporal-activity tasks stay while Temporal serves existing runs. Separate legacy largeTask support.

## Acceptance criteria

- [ ] A contract simulator built from the pinned serverless contract versions tests submit acknowledgement loss, duplicate completion, stale cancellation and checkpoint references.
- [ ] An ADR records the consumed contract versions and the ownership of execution leases, logical retries, metering and checkpoint retention.
- [ ] Legacy largeTask profiles incompatible with restricted Wasm execution are flagged; no silent native-container fallback is permitted.
- [ ] A gap found in a serverless contract becomes a falcone-serverless issue; no local workaround protocol is added.

## Planning

- Parent: EP-INT
- Phase: M0
- Effort: L
- Depends on: CON-01

## Requirements

- **FR-INT-03:** The system must invoke falcone-serverless through pinned versions of ctr-worker-execution-api and ctr-job-checkpoint with stable operation keys, authenticated correlation and explicit cancellation outcomes, and must not define a parallel workflow-specific execution or checkpoint protocol.
- **FR-INT-04:** The system must avoid a runtime dependency cycle: falcone-serverless execution primitives must run without calling Temporal or requiring falcone-workflow to execute themselves.


## INT-03 — Preserve asynchronous batch and object-storage behavior

<!-- falcone-workflow:INT-03 -->

## User story

As a workflow user, I want large inputs and provider jobs to remain durable so that orchestration is not tied to one process.

## Description

Use a provider-neutral Falcone S3 interface and submit/status/collect/cancel phases for asynchronous integrations.

## Acceptance criteria

- [ ] An interrupted LLM batch resumes polling the same provider job; ambiguous submit is reconciled.
- [ ] Missing or hash-mismatched objects fail explicitly; no cross-tenant object can be dereferenced.
- [ ] SeaweedFS or another configured S3 provider passes the adapter contract before deployment; backend identity is recorded.
- [ ] A payload over the inline threshold is stored by reference, and exceeding the per-run or per-node maximum fails with an explicit error.

## Planning

- Parent: EP-INT
- Phase: M2
- Effort: L
- Depends on: INT-01, INT-02, EVT-03

## Requirements

- **FR-INT-05:** The system must store large payloads through tenant-scoped Falcone object references with content hashes, retention metadata and authorization checks, using a configured inline threshold and per-run and per-node maximum referenced bytes that are part of quota policy and recorded in the policy snapshot, and failing explicitly when a limit is exceeded.
- **FR-INT-06:** The system must persist provider job IDs and bounded poll schedules for batch tasks, including cancellation cleanup and credential expiry.


- **EP-OBS — Monitoring, audit and performance**

Preserve the Falcone run view and make recovery measurable.

## OBS-01 — Implement run history and resumable SSE

<!-- falcone-workflow:OBS-01 -->

## User story

As a Falcone user, I want the existing run timeline so that I can inspect progress after migration.

## Description

Project durable native events to existing node-status/log-line/stream-end frames; retain run/node mapping.

## Acceptance criteria

- [ ] Disconnect/reconnect with Last-Event-ID produces no missing persisted events within retention.
- [ ] Terminal streams replay retained history and end; expired cursors receive an explicit resynchronization response.
- [ ] Slow consumers are bounded and cannot block workflow commits or leak foreign run data.

## Planning

- Parent: EP-OBS
- Phase: M2
- Effort: L
- Depends on: DUR-01, CON-01

## Requirements

- **FR-OBS-01:** The system must expose ordered tenant-scoped history and compatible SSE frames with stable resumable event cursors.
- **FR-OBS-02:** The system must emit audit events for lifecycle, authorization-sensitive changes, approvals, repair and backend handover.


## OBS-02 — Add operational metrics and tracing

<!-- falcone-workflow:OBS-02 -->

## User story

As an SRE, I want queue and recovery visibility so that failures are detected before workflows stall.

## Description

Instrument engine transactions, timers, outbox, adapters and leases with OpenTelemetry and Prometheus-compatible metrics.

## Acceptance criteria

- [ ] Dashboards separate starts, transitions, messages, running activities and waiting runs.
- [ ] An injected database outage, broker outage and stalled adapter trigger distinct actionable alerts.
- [ ] Per-run IDs appear in traces/logs rather than unbounded metric labels; payload logging is redacted.

## Planning

- Parent: EP-OBS
- Phase: M2
- Effort: M
- Depends on: OBS-01, DUR-02

## Requirements

- **FR-OBS-03:** The system must measure admission latency, transition throughput, queue age, timer lag, lease expiry, retry rate, outbox lag and database contention.
- **FR-OBS-04:** The system must propagate trace correlation across Falcone services while redacting secrets and controlling metric cardinality.


## OBS-03 — Qualify performance and reliability targets

<!-- falcone-workflow:OBS-03 -->

## User story

As a product owner, I want measured capacity so that commitments match infrastructure.

## Description

Publish reproducible load, soak and fault-injection profiles; treat numerical targets as provisional until tested.

## Acceptance criteria

- [ ] Run small/medium/load profiles with 20 tenants, mixed waits and fan-out; publish hardware, DB configuration and percentiles.
- [ ] Measure p95 start acknowledgement, ready-task dispatch and due-timer lag under load and failure recovery.
- [ ] Document saturation, fairness and storage growth; do not interpret 100k messages/s as 100k workflow starts/s.

## Planning

- Parent: EP-OBS
- Phase: M3
- Effort: L
- Depends on: OBS-02, TEN-03, OPS-02

## Requirements

- **FR-OBS-05:** The project must benchmark workflow starts, step transitions, durable waits and activity concurrency independently from Falcone's WebSocket message rate.
- **FR-OBS-06:** The project must publish achieved availability, latency and recovery results against an agreed workload and resource budget before production cutover.


## OBS-04 — Add SLA and deadline alerts

<!-- falcone-workflow:OBS-04 -->

## User story

As a workspace administrator, I want deadlines on flows and nodes so that I am alerted, or the run is failed or cancelled, when work is late.

## Description

Evaluate declared per-flow and per-node deadlines, measured from run start, a schedule's nominal time or approval assignment, with durable timers; record SLA events and apply the configured action.

## Acceptance criteria

- [ ] A breached deadline records one SLA event and emits the SLA-breached lifecycle event, including after an engine restart.
- [ ] Notify-only leaves the run running; fail and cancel apply the FR-CON-07 semantics.
- [ ] Deadlines measured from run start, schedule nominal time and approval assignment have fixtures, including a run that completes in time and raises no event.

## Planning

- Parent: EP-OBS
- Phase: M2
- Effort: M
- Depends on: OBS-02, EVT-05, TIM-01, CON-02

## Requirements

- **FR-OBS-07:** The system must evaluate declared per-flow and per-node deadlines (maximum duration from run start, from a schedule's nominal time, or from approval assignment) and on breach must record an SLA event and apply the configured action: notify only, fail, or cancel.


## OBS-05 — Add run search, labels and search attributes

<!-- falcone-workflow:OBS-05 -->

## User story

As an operator or tenant user, I want to search and count runs by status, flow and business attributes so that I can find, for example, all failed runs for one customer this week.

## Description

Index run status, flow, version, time range, trigger, initiator and bounded user-defined labels or typed search attributes in PostgreSQL with per-workspace limits; no separate visibility store.

## Acceptance criteria

- [ ] Filtered list and count queries return only runs of the caller's workspace, with stable pagination under concurrent inserts.
- [ ] Attribute count, key length and value size limits are enforced at start and when a node sets an attribute.
- [ ] Supported filters use indexes at the OBS-03 benchmark data volume.
- [ ] Labels and attributes follow payload retention and redaction rules.

## Planning

- Parent: EP-OBS
- Phase: M2
- Effort: M
- Depends on: OBS-01, TEN-01

## Requirements

- **FR-OBS-08:** The system must let authorized users list and count runs within a workspace by status, flow, version, time range, trigger, initiator, and bounded user-defined labels or typed search attributes set at start or by nodes, with indexed filters, stable pagination and per-workspace limits on attribute count, key length and value size.


- **EP-OPS — Deployment, CI/CD and operations**

Operate as a restricted Falcone service without administrator-installed runtimes.

## OPS-01 — Package restricted Kubernetes and OpenShift deployment

<!-- falcone-workflow:OPS-01 -->

## User story

As a platform operator, I want ordinary namespaced deployment so that restricted clusters can host the engine.

## Description

Provide containers, migrations, health probes and documented external service requirements; the Helm chart lives in gntik-ai/falcone-charts.

## Acceptance criteria

- [ ] Install in a restricted namespace with no permission to create cluster-scoped resources.
- [ ] Document pre-provisioned namespace, RBAC, DB, gateway and network prerequisites and pass readiness checks.
- [ ] Cluster tests run in dedicated fw-test-* namespaces on the shared k3s cluster with Pod Security restricted standing in for OpenShift restricted-v2, may read in-falcone-staging and touch no other namespace; the actual corporate OpenShift version is qualified before production rather than assumed.
- [ ] The engine never exceeds its database connection budget under load, and exhausting the budget does not affect Falcone's own database.

## Planning

- Parent: EP-OPS
- Phase: M1
- Effort: L
- Depends on: DUR-01

## Requirements

- **FR-OPS-01:** The system must deploy using its own database on the shared PostgreSQL cluster within a declared connection budget, and standard namespaced resources without mandatory CRDs, operators, cluster roles or privileged containers.
- **FR-OPS-02:** The system must run as non-root with arbitrary allowed UID, read-only root filesystem, dropped capabilities and no host access.


## OPS-02 — Implement upgrade, backup and recovery runbooks

<!-- falcone-workflow:OPS-02 -->

## User story

As an on-call engineer, I want tested operating procedures so that releases and incidents are recoverable.

## Description

Use expand/contract schema migrations, drain behavior, PostgreSQL HA and coordinated payload backup policies.

## Acceptance criteria

- [ ] Old/new binaries coexist through a schema expansion and drain test.
- [ ] A DB failover test fences old owners before new dispatch resumes.
- [ ] A restore rehearsal reports measured RPO/RTO, required object versions and credential recovery dependencies.

## Planning

- Parent: EP-OPS
- Phase: M3
- Effort: L
- Depends on: OPS-01, DSL-03

## Requirements

- **FR-OPS-03:** The system must support rolling compatible upgrades, bounded graceful drain and documented rollback limits for schema and interpreter changes, retaining every interpreter version referenced by an open run for at least the longest permitted remaining wait.
- **FR-OPS-04:** The project must provide tested runbooks for database failover, backup restore, stuck runs, queue overload and key rotation.


## OPS-03 — Establish CI, security qualification and ownership

<!-- falcone-workflow:OPS-03 -->

## User story

As a maintainer, I want enforceable release gates so that durability regressions cannot ship unnoticed.

## Description

The repository seed already provides the CI bootstrap (typecheck, unit tests and the generated-documentation check). Add contract suites, concurrency/fault tests, supply-chain checks and named ownership responsibilities.

## Acceptance criteria

- [ ] CI keeps checking generated backlog integrity and runs a real PostgreSQL integration suite in fw-test-* namespaces once implementation exists.
- [ ] Images have pinned dependencies, SBOMs and signed release artifacts; copied upstream code has documented provenance.
- [ ] An ownership/runbook review names escalation and patch responsibilities; documentation alone cannot mark runtime qualified.

## Planning

- Parent: EP-OPS
- Phase: M1
- Effort: L
- Depends on: CON-01, OPS-01

## Requirements

- **FR-OPS-05:** The project must gate releases on contract, isolation, state-machine fault, schema-migration and dependency-security checks.
- **FR-OPS-06:** The project must assign accountable runtime maintenance, SRE on-call, security review and Falcone product ownership before production release.


## OPS-04 — Provide bulk run operations and operator tooling

<!-- falcone-workflow:OPS-04 -->

## User story

As an operator, I want to act on many runs at once with the same safeguards as single-run repair so that incidents affecting many runs can be resolved quickly and safely.

## Description

Apply cancel, terminate, pause, resume and retry to a filtered set of runs in one workspace as a resumable, rate-limited batch with a dry-run count, and expose the HUM-03 run-level repair operations and bulk operations through the operator API and CLI with the same authorization and audit.

## Acceptance criteria

- [ ] A dry run returns the number of matching runs without changing any run.
- [ ] A batch respects its rate limit, resumes after an engine restart without applying an operation twice to one run, and reports a per-run outcome.
- [ ] A filter cannot match runs outside the caller's workspace.
- [ ] One audit record references all affected runs, and each run's history records the operation.

## Planning

- Parent: EP-OPS
- Phase: M3
- Effort: M
- Depends on: HUM-03, CON-02, OBS-05

## Requirements

- **FR-OPS-07:** The system must apply cancel, terminate, pause, resume and retry to a filtered set of runs within one workspace as a resumable, rate-limited batch with a dry-run count, per-run outcome and a single audit record referencing all affected runs.


- **EP-MIG — Temporal migration and retirement**

Retire Temporal only when Falcone contract and recovery evidence support it.

## MIG-01 — Build a migration inventory and differential harness

<!-- falcone-workflow:MIG-01 -->

## User story

As a release engineer, I want evidence of semantic parity so that unsupported flows are not cut over.

## Description

Inventory deployed DSLs, open runs, schedules, Temporal patches and SDK usage; use isolated effects for comparisons.

## Acceptance criteria

- [ ] Cover sequence, parallel, branches, approval/cancel races, children, batch polling, retries and schedule errors.
- [ ] Track each incompatible semantic with owner and resolution; do not copy Temporal history into native tables.
- [ ] Record the actual deployed image/source baseline separately from repository inspection.
- [ ] Measure starts per second, committed transitions per run, open waits, schedule count and retention on the current Temporal staging deployment (read-only in in-falcone-staging) and publish them as the capacity baseline.

## Planning

- Parent: EP-MIG
- Phase: M0
- Effort: L
- Depends on: CON-01

## Requirements

- **FR-MIG-01:** The project must inventory Temporal-dependent code, active workflow versions, open executions, schedule ownership and task adapters before selecting migration cohorts.
- **FR-MIG-02:** The project must compare native and Temporal outcomes using deterministic fixtures or isolated effect simulators without doubling production effects.


## MIG-02 — Implement staged routing and in-flight drainage

<!-- falcone-workflow:MIG-02 -->

## User story

As an operator, I want controlled rollout so that existing workflows finish safely.

## Description

Route new runs by cohort; keep a durable backend locator; drain old runs and retain old worker versions.

## Acceptance criteria

- [ ] Rollback routes future starts back while native runs retain native ownership.
- [ ] Schedule/webhook/event ownership is coordinated to avoid duplicate admission during rollout.
- [ ] A long-lived Temporal run remains operable until completion or an approved explicit intervention; no automatic restart repeats effects.

## Planning

- Parent: EP-MIG
- Phase: M3
- Effort: L
- Depends on: MIG-01, CON-02, INT-01, HUM-01

## Requirements

- **FR-MIG-03:** The system must route new starts by approved cohort and persist backend ownership for all later run operations.
- **FR-MIG-04:** The system must keep in-flight Temporal runs on Temporal unless an explicit application-level checkpoint transfer is validated.


## MIG-03 — Qualify retirement and synchronize Falcone documentation

<!-- falcone-workflow:MIG-03 -->

## User story

As the Falcone owner, I want a verifiable retirement gate so that Temporal can be removed safely.

## Description

Update Falcone code/charts and the serverless design only after contract readiness; preserve audit/retention obligations.

## Acceptance criteria

- [ ] Scan code, manifests and runtime telemetry for remaining callers and record authorized exceptions.
- [ ] Complete a no-Temporal end-to-end workflow run covering function invocation, storage, approval and recovery.
- [ ] Retain required old histories and recovery material, then remove resources only through a separately authorized rollout.

## Planning

- Parent: EP-MIG
- Phase: M3
- Effort: L
- Depends on: MIG-02, TIM-03, OBS-03, DUR-03

## Requirements

- **FR-MIG-05:** The project must verify no remaining required Temporal runs, schedules, credentials or callers before removing the Temporal deployment and SDK dependencies.
- **FR-MIG-06:** The project must update Falcone integration documentation and falcone-serverless workflow references to the native contract with a rollback and retention plan.


