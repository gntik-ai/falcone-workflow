# 4. Implementation backlog

12 epics and 36 stories; effort S/M/L is relative, not a delivery estimate. M0 discovery; M1 durable core; M2 integration; M3 migration and qualification.

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
- [ ] Record whether arbitrary Temporal SDK workflows exist; do not claim raw SDK compatibility without evidence.

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

## Planning

- Parent: EP-CON
- Phase: M1
- Effort: L
- Depends on: CON-01, DUR-01

## Requirements

- **FR-CON-03:** The system must expose authenticated start, get, list, cancel, retry and signal operations with tenant-scoped idempotency keys.
- **FR-CON-04:** The system must route every existing run to its recorded backend and return a retryable service-unavailable response when that backend is unavailable.


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

## Planning

- Parent: EP-CON
- Phase: M2
- Effort: M
- Depends on: CON-02, DSL-01, OBS-01

## Requirements

- **FR-CON-05:** The system must support CLI validate, publish, start, inspect, cancel and retry operations using Falcone authentication.
- **FR-CON-06:** The system must provide versioned task schemas and validation errors usable by Falcone's existing visual editor.


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

## Planning

- Parent: EP-DSL
- Phase: M0
- Effort: L
- Depends on: CON-01

## Requirements

- **FR-DSL-01:** The system must validate sequence, parallel, task, branch, wait, approval and sub-flow nodes using the inventoried Falcone DSL rules.
- **FR-DSL-02:** The system must reject invalid cycles, duplicate IDs, unknown tasks, dangling references and invalid cron/duration expressions before publishing.


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

## Planning

- Parent: EP-DSL
- Phase: M1
- Effort: L
- Depends on: DSL-01, DUR-01

## Requirements

- **FR-DSL-03:** The system must evaluate expressions with bounded input size, runtime and memory without network, filesystem or arbitrary-code access.
- **FR-DSL-04:** The system must persist branch decisions, parallel completion sets and deterministic output-merge behavior before advancing successors.


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

## Planning

- Parent: EP-DSL
- Phase: M1
- Effort: L
- Depends on: DSL-02

## Requirements

- **FR-DSL-05:** The system must pin each run to immutable definition and interpreter versions and each child to an authorized explicit definition version.
- **FR-DSL-06:** The system must reject unsupported historical versions and require an explicit audited migration plan before changing active-run semantics.


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

Claim ready tasks with bounded leases, database time, monotonic attempt fencing and periodic reconciliation.

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

## Planning

- Parent: EP-DUR
- Phase: M3
- Effort: L
- Depends on: DUR-02, OPS-02

## Requirements

- **FR-DUR-05:** The system must bound event history and payload growth using configured limits and resumable continuation or archival policies.
- **FR-DUR-06:** The system must restore database and referenced object payloads to a consistent recovery point and reconcile external effects before resuming dispatch.


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

## Planning

- Parent: EP-ACT
- Phase: M1
- Effort: L
- Depends on: ACT-01, TIM-01

## Requirements

- **FR-ACT-03:** The system must apply configured maximum attempts, backoff, retryable error classes, start-to-close, schedule-to-close and heartbeat timeouts.
- **FR-ACT-04:** The system must classify connectors by idempotency support and surface ambiguous external outcomes instead of promising universal exactly-once effects.


## ACT-03 — Support asynchronous jobs and checkpoints

<!-- falcone-workflow:ACT-03 -->

## User story

As a data analyst, I want long-running tasks to survive worker restarts so that analysis is resumable.

## Description

Separate job submission, observation, checkpoint and result retrieval; avoid holding orchestration processes during waits.

## Acceptance criteria

- [ ] A worker dies after job submission; reconciliation finds the same external job.
- [ ] A cancelled job cannot report the workflow completed; delayed cleanup is visible and retried under policy.
- [ ] A capability-qualified checkpoint resumes correctly; unsupported native workloads remain migration blockers.

## Planning

- Parent: EP-ACT
- Phase: M2
- Effort: L
- Depends on: ACT-02, INT-02

## Requirements

- **FR-ACT-05:** The system must persist external job IDs and checkpoint references and resume observation after worker loss without blindly resubmitting the job.
- **FR-ACT-06:** The system must support configurable multi-day waits with bounded heartbeat, cancellation and credential-renewal policies.


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

## Planning

- Parent: EP-TIM
- Phase: M1
- Effort: M
- Depends on: DUR-01

## Requirements

- **FR-TIM-01:** The system must persist wait and retry timers and fire each logical timer at most once into workflow state.
- **FR-TIM-02:** The system must resolve simultaneous signal, timeout and cancellation transitions with one documented transactional ordering rule.


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

## Planning

- Parent: EP-TIM
- Phase: M2
- Effort: L
- Depends on: TIM-01, CON-02

## Requirements

- **FR-TIM-03:** The system must preserve Falcone schedule identities, published cron text, next-action times, recent actions and idempotent pause/resume behavior.
- **FR-TIM-04:** The system must implement explicit overlap, catch-up window, timezone and daylight-saving policies and atomically deduplicate each scheduled occurrence.


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

## Planning

- Parent: EP-TIM
- Phase: M3
- Effort: L
- Depends on: TIM-02, MIG-02

## Requirements

- **FR-TIM-05:** The system must fence schedule ownership during backend handover so only one engine may admit an occurrence.
- **FR-TIM-06:** The system must support audited bounded backfill with a preview of candidate occurrences and quota impact.


- **EP-EVT — Events and trigger delivery**

Use Falcone's existing event infrastructure with durable inbox/outbox semantics.

## EVT-01 — Add inbox and outbox integration

<!-- falcone-workflow:EVT-01 -->

## User story

As a platform engineer, I want durable event delivery so that broker outages cannot lose workflow transitions.

## Description

Use Kafka as transport, PostgreSQL as state authority; enforce tenant-bound event identities.

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
- **FR-EVT-02:** The system must publish committed outgoing events through a retryable transactional outbox with stable event IDs.


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

## Planning

- Parent: EP-EVT
- Phase: M2
- Effort: L
- Depends on: EVT-01, TEN-01

## Requirements

- **FR-EVT-03:** The system must authenticate webhook triggers with rotation-aware signatures, replay protection and size limits.
- **FR-EVT-04:** The system must derive tenant and workspace from verified trigger registration rather than caller-supplied payload fields.


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

## Planning

- Parent: EP-EVT
- Phase: M2
- Effort: L
- Depends on: EVT-01, TIM-01

## Requirements

- **FR-EVT-05:** The system must persist authorized signals using deduplication IDs and explicit run/node-occurrence correlation.
- **FR-EVT-06:** The system must define TTL, capacity and terminal-run behavior for unmatched or early-arriving signals.


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

## Planning

- Parent: EP-HUM
- Phase: M2
- Effort: M
- Depends on: EVT-03, TEN-01

## Requirements

- **FR-HUM-01:** The system must derive approval actor identity from verified authentication and enforce configured reviewer permissions.
- **FR-HUM-02:** The system must preserve approval outcome fields and distinguish rejection, timeout and cancellation.


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

Support retry-from-known-boundary and reconciliation acknowledgements; disallow arbitrary history edits.

## Acceptance criteria

- [ ] Stale revision or cross-tenant repair requests fail before mutation.
- [ ] Preview identifies side effects that may repeat and requires a documented resolution for ambiguous tasks.
- [ ] Every accepted repair records actor, reason, prior revision and resulting attempt lineage.

## Planning

- Parent: EP-HUM
- Phase: M3
- Effort: L
- Depends on: HUM-02, OBS-01

## Requirements

- **FR-HUM-05:** The system must require authorization, reason and expected run revision for manual repair or retry actions.
- **FR-HUM-06:** The system must preserve original history and create explicit linked attempts or continuation records for repair.


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
- [ ] A saturated tenant does not starve eligible work from other tenants in the benchmark.
- [ ] Billing fixtures classify retries, failures, waits and cancellations explicitly; workflow does not invent independent tariff rules.

## Planning

- Parent: EP-TEN
- Phase: M2
- Effort: L
- Depends on: DUR-02, TEN-02

## Requirements

- **FR-TEN-05:** The system must consume versioned Falcone quota policy for starts, active tasks, waiting runs, retries, fan-out, payload bytes and retention.
- **FR-TEN-06:** The system must enforce fair tenant/workspace admission with idempotent reservations, releases and usage events across crashes.


- **EP-INT — Falcone services and serverless integration**

Port first-party adapters and define the boundary with falcone-serverless.

## INT-01 — Port the existing first-party task catalog

<!-- falcone-workflow:INT-01 -->

## User story

As a Falcone developer, I want current task types to work so that workflows remain useful on day one.

## Description

Extract engine-neutral activity context for DB, storage, functions, events, HTTP, email and LLM tasks.

## Acceptance criteria

- [ ] Each task type has success/error/cancellation/duplicate-attempt fixtures and an explicit migration status.
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


## INT-02 — Define the serverless invocation and checkpoint contract

<!-- falcone-workflow:INT-02 -->

## User story

As a platform developer, I want one shared invocation contract so that workflow and serverless can evolve independently.

## Description

Keep workflow state in falcone-workflow and untrusted computation in falcone-serverless; separate legacy largeTask support.

## Acceptance criteria

- [ ] A contract simulator tests submit acknowledgement loss, duplicate completion, stale cancellation and checkpoint references.
- [ ] An ADR records ownership of execution leases, logical retries, metering and checkpoint retention.
- [ ] Legacy largeTask profiles incompatible with restricted Wasm execution are flagged; no silent native-container fallback is permitted.

## Planning

- Parent: EP-INT
- Phase: M0
- Effort: L
- Depends on: CON-01

## Requirements

- **FR-INT-03:** The system must define versioned start/status/cancel/result callbacks with stable operation keys, authenticated correlation and explicit cancellation outcomes.
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

## Planning

- Parent: EP-INT
- Phase: M2
- Effort: L
- Depends on: INT-01, INT-02, EVT-03

## Requirements

- **FR-INT-05:** The system must store large payloads through tenant-scoped Falcone object references with content hashes, retention metadata and authorization checks.
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


- **EP-OPS — Deployment, CI/CD and operations**

Operate as a restricted Falcone service without administrator-installed runtimes.

## OPS-01 — Package restricted Kubernetes and OpenShift deployment

<!-- falcone-workflow:OPS-01 -->

## User story

As a platform operator, I want ordinary namespaced deployment so that restricted clusters can host the engine.

## Description

Provide containers, Helm manifests, migrations, health probes and documented external service requirements.

## Acceptance criteria

- [ ] Install in a restricted namespace with no permission to create cluster-scoped resources.
- [ ] Document pre-provisioned namespace, RBAC, DB, gateway and network prerequisites and pass readiness checks.
- [ ] Test the agreed Kubernetes minors and actual corporate OpenShift version; unsupported versions fail qualification rather than being assumed.

## Planning

- Parent: EP-OPS
- Phase: M1
- Effort: L
- Depends on: DUR-01

## Requirements

- **FR-OPS-01:** The system must deploy using existing PostgreSQL and standard namespaced resources without mandatory CRDs, operators, cluster roles or privileged containers.
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

- **FR-OPS-03:** The system must support rolling compatible upgrades, bounded graceful drain and documented rollback limits for schema and interpreter changes.
- **FR-OPS-04:** The project must provide tested runbooks for database failover, backup restore, stuck runs, queue overload and key rotation.


## OPS-03 — Establish CI, security qualification and ownership

<!-- falcone-workflow:OPS-03 -->

## User story

As a maintainer, I want enforceable release gates so that durability regressions cannot ship unnoticed.

## Description

Add contract suites, concurrency/fault tests, supply-chain checks and named ownership responsibilities.

## Acceptance criteria

- [ ] CI checks generated backlog integrity and runs a real PostgreSQL integration suite once implementation exists.
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


