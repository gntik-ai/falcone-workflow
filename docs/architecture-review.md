# Architecture review before backlog decomposition

Review baseline: source commit `4113bea8cb3ef7bfaf3fd88c2329b66c0b3c132d`, dated 30 October 2026. The inspected Falcone source baseline in [design.md](design.md) is not a deployed inventory. The review covers the design, architecture, migration plan, 98 requirements and 47 published stories; it provides no runtime qualification evidence.

ADR 0001 remains Accepted and byte-identical. D1–D8 remain authoritative. All 12 ADRs below have **Status: Proposed**: a proposed resolution does not close an open question or authorize implementation, migration or rollout. The operator reviews each ADR individually before backlog decomposition. The original design, planning source, open questions and generated documents remain unchanged; the proposed diffs below are unapplied follow-up material.

Acceptance of ADR-0003 (tenant RLS), ADR-0007 (expression isolation), ADR-0009 (native live-run migration), ADR-0010 (cross-engine migration boundaries) and ADR-0011 (credentials) requires **R3 review with a second reviewer and explicit operator approval**. The proposed second reviewer role is **Security engineers**, from [open-questions.md, Ownership](open-questions.md#ownership); the operator must name the accountable reviewer at acceptance. This R1 documentation ChangeSet does not satisfy those R3 gates.

## ADR index

Numbers follow the requested topic order. Each row maps to exactly one new file; no topic is split or merged.

| ADR | Title | Topic |
|---|---|---|
| [ADR-0002](adr/0002-repository-ownership.md) | Repository ownership and per-repository story split | 1: D1 ownership and technical issue boundaries |
| [ADR-0003](adr/0003-persistence-and-platform-boundary.md) | Persistence roles, tenant RLS and platform budgets | 2: D5 database and platform assumptions |
| [ADR-0004](adr/0004-shared-outbox-inbox-and-fencing.md) | Shared outbox, inbox and lease fencing consumption | 3: D4 / STO-03 consumer requirements and late delivery |
| [ADR-0005](adr/0005-task-dispatch-and-ambiguous-outcomes.md) | Bounded task dispatch and ambiguous external outcomes | 4: claims, heartbeat, fencing and at-least-once effects |
| [ADR-0006](adr/0006-serverless-tasks-and-worker-envelope.md) | Serverless function and job tasks and the ACT-01 envelope | 5: invocation/checkpoints and envelope reuse |
| [ADR-0007](adr/0007-bounded-expression-isolation.md) | Bounded expression evaluation outside engine processes | 6: evaluator isolation and cost limits |
| [ADR-0008](adr/0008-timers-and-schedule-policies.md) | Durable timers and explicit schedule calendar policies | 7: time zones, overlap, catch-up and DST |
| [ADR-0009](adr/0009-versioning-and-long-wait-retention.md) | Pinned versions, long-wait retention and native run migration | 8: D8 retention and DSL-06 |
| [ADR-0010](adr/0010-dual-engine-migration.md) | Dual-engine routing, drainage and schedule cutover | 9: D3 migration, rollback and Temporal drainage |
| [ADR-0011](adr/0011-long-lived-run-credentials.md) | Long-lived run authority, renewal and revocation | 10: credential lineage and current authorization |
| [ADR-0012](adr/0012-history-sse-and-archival.md) | Durable history, resumable SSE and bounded archival | 11: history projection, retention and restore |
| [ADR-0013](adr/0013-m0-capacity-and-benchmarks.md) | M0 capacity baseline and qualification benchmarks | 12: Temporal staging baseline and native measurement plan |

## Severity scale

- **blocker:** blocks backlog decomposition of the affected work until an operator reviews the proposal and the specified owner supplies the missing decision or contract evidence. It does not mean that this Markdown change is a runtime blocker.
- **high:** must be resolved before implementation of the affected correctness or security boundary; technical work can be outlined with an explicit gate.
- **medium:** must be resolved before integration, sizing or production qualification; decomposition may carry an owner-bound dependency.
- **low:** documentation or project administration follow-up; does not block decomposition.

No target or assumption becomes a commitment merely by being listed here. Lease, heartbeat, connection-budget and capacity numbers are provisional pending M0 measurement, consistent with [architecture.md, Capacity and service objectives — proposals, not promises](architecture.md#capacity-and-service-objectives--proposals-not-promises).

## Findings

FR IDs below refer to [requirements.md](requirements.md); story numbers refer to [github-issues.md](github-issues.md). A resolving ADR identifies a proposed resolution; acceptance and evidence are still required. Owner-only rows remain open decisions. Repeated design sections reflect separate gaps, not additional ADR topics.

| Finding | Severity | Design section | Proposed change / evidence needed | Affected FR IDs | Stories | Resolving ADR or owner role |
|---|---|---|---|---|---|---|
| F01 | blocker | design.md — Repository ownership; architecture.md — Repository placement and shared contracts | Product stories lack per-repository technical ownership. Require one owner and explicit contract dependencies for each repository's issue; create no issues in this change. | FR-CON-01, FR-INT-03, FR-OPS-01 | CON-02 #14, INT-02 #38, OPS-01 #43 | ADR-0002; Workflow/runtime maintainers with Falcone integration team |
| F02 | high | architecture.md — Recommended stack and rationale; Data model and invariants | Separate DB placement alone does not establish isolation/recovery. Specify non-bypass runtime RLS, separate migration access, transaction-local scope, measured connection/IO budgets and platform HA/PITR terms. | FR-TEN-01, FR-DUR-02, FR-DUR-06, FR-OPS-01 | TEN-01 #34, DUR-01 #19, OPS-01 #43, OPS-02 #44 | ADR-0003; SRE/platform team; R3 acceptance |
| F03 | blocker | architecture.md — Repository placement and shared contracts | STO-03 API/path/version and transaction participation are unverified. Confirm consumer capabilities with owners; gate production integration if late, without shipping a parallel implementation. | FR-EVT-01, FR-EVT-02, FR-DUR-03 | EVT-01 #28, DUR-02 #20 | ADR-0004; Falcone integration team coordinates upstream owners |
| F04 | high | architecture.md — Task and failure semantics | Lease example could become an unsupported default. Specify provisional bounded claims/renewal, stale heartbeat rejection, connector classes and ambiguous-outcome incidents without promising exactly-once effects. | FR-DUR-03, FR-DUR-04, FR-ACT-03, FR-ACT-04, FR-HUM-09 | DUR-02 #20, ACT-02 #23, HUM-03 #33 | ADR-0005; Workflow/runtime maintainers |
| F05 | blocker | architecture.md — Repository placement and shared contracts; migration.md — Cross-repository work | Serverless contract definitions and ACT-01 envelope compatibility are absent. Obtain authoritative fixtures and ownership of retries, leases, metering and checkpoints; qualify native profiles before choosing envelope reuse. | FR-INT-03, FR-INT-04, FR-ACT-01, FR-ACT-05 | INT-02 #38, ACT-01 #22, ACT-03 #24 | ADR-0006; Falcone integration team coordinates contract owners |
| F06 | high | architecture.md — Recommended stack and rationale; design.md — Recommended boundary | Process isolation and hard CEL limits need a qualification plan. Pin semantics/limits, evaluate outside transactions against persisted time and commit outcomes by revision. | FR-DSL-03, FR-DSL-04, FR-DSL-08 | DSL-02 #17, DSL-01 #16 | ADR-0007; Security engineers; R3 acceptance |
| F07 | high | migration.md — Boundary mapping; Rollout; architecture.md — Data model and invariants | Calendar fidelity and handover need explicit policies. Preserve legacy aliases/defaults; specify additive time zones/DST, bounded backfill, timer races and epoch-fenced admission. | FR-TIM-02, FR-TIM-04, FR-TIM-05, FR-TIM-06, FR-TIM-07, FR-TIM-08 | TIM-01 #25, TIM-02 #26, TIM-03 #27 | ADR-0008; Workflow/runtime maintainers |
| F08 | blocker | design.md — Operator decisions (2026-10-30); architecture.md — Data model and invariants | Maximum wait is unset. Parameterize retention with product-owned W_max, preserve every live version reference and distinguish native DSL-06 migration from Temporal drainage. | FR-DSL-05, FR-DSL-06, FR-DSL-11, FR-ACT-06, FR-OPS-03 | DSL-03 #18, DSL-06 #54, OPS-02 #44 | ADR-0009; Falcone product owner; R3 acceptance for live migration |
| F09 | high | migration.md — Rollout; Required failure matrix | Rollback must not strand native runs. Persist backend ownership, fence schedule/trigger handover, drain Temporal and limit rollback to future admissions. | FR-CON-04, FR-MIG-03, FR-MIG-04, FR-MIG-05, FR-TIM-05 | CON-02 #14, MIG-02 #47, MIG-03 #48, TIM-03 #27 | ADR-0010; Falcone integration team; R3 acceptance |
| F10 | high | architecture.md — Long-lived credentials and payloads; Typical invocation | Revocation and expiry need owner-confirmed policy. Resolve task credentials from authoritative lineage; fail closed for unauthorized effects and require audited controlled reauthorization. | FR-TEN-03, FR-TEN-04, FR-ACT-06, FR-HUM-09 | TEN-02 #35, ACT-03 #24, HUM-03 #33 | ADR-0011; Security engineers with Falcone integration team; R3 acceptance |
| F11 | high | architecture.md — Data model and invariants; Long-lived credentials and payloads; Typical invocation | History limits must preserve live payloads and resumable cursors. Define linked segments, closed-run retention/erasure/legal holds and coordinated object/DB restore. | FR-DUR-05, FR-DUR-06, FR-DUR-07, FR-OBS-01, FR-INT-05 | DUR-03 #21, OBS-01 #40, INT-03 #39 | ADR-0012; Workflow/runtime maintainers with SRE/platform team |
| F12 | blocker | architecture.md — Capacity and service objectives — proposals, not promises; design.md — Delivery gates | No measured workflow baseline supports numeric commitments. Capture Temporal staging workload in M0 and publish independent native load/recovery evidence with resource budgets. | FR-OBS-03, FR-OBS-05, FR-OBS-06, FR-MIG-01 | MIG-01 #46, OBS-02 #41, OBS-03 #42 | ADR-0013; SRE/platform team with Release/QA maintainers |
| F13 | medium | design.md — Evidence-driven scope; migration.md — Rollout | Inspected source is not authoritative deployed inventory. Record actual source/image and contract versions before choosing migration cohorts. | FR-CON-02, FR-MIG-01 | CON-01 #13, MIG-01 #46 | Falcone integration team with Release/QA maintainers |
| F14 | medium | architecture.md — Recommended stack and rationale; Long-lived credentials and payloads | S3 provider is unknown. Confirm provider, object-version/retention support and scoped adapter behavior; keep engine provider-neutral. | FR-INT-05, FR-DUR-06 | INT-03 #39, OPS-02 #44 | Falcone integration team with SRE/platform team |
| F15 | medium | design.md — Delivery gates; architecture.md — Recommended stack and rationale | Corporate OpenShift release and PostgreSQL service terms are unverified. Record restricted-resource compatibility, actual HA/backup and budget terms; k3s alone is insufficient qualification. | FR-OPS-01, FR-OPS-02, FR-OPS-04 | OPS-01 #43, OPS-02 #44 | SRE/platform team |
| F16 | medium | design.md — Functional gap analysis (2026-10-30); Evidence-driven scope | Approval policy remains product-owned. Confirm actors, segregation of duty, quorum and deadlines without altering current verified-identity behavior. | FR-HUM-01, FR-HUM-02, FR-HUM-07 | HUM-01 #31, HUM-04 #57 | Falcone product owner with Falcone integration team |
| F17 | medium | design.md — Repository ownership; architecture.md — Typical invocation | Billing of retries, waits, failed starts, queued work and idle/history storage is unset. Falcone defines policy; engine consumes limits and emits idempotent usage facts. | FR-TEN-05, FR-TEN-06 | TEN-03 #36 | Falcone product owner with Falcone integration team |
| F18 | medium | design.md — Delivery gates; architecture.md — Dependencies retained and replaced | Operational roles are not named people or a rota. Assign on-call, recovery, security qualification and runtime upgrade accountability before production. | FR-OPS-04, FR-OPS-05, FR-OPS-06 | OPS-02 #44, OPS-03 #45 | SRE/platform team, Workflow/runtime maintainers, Security engineers and Falcone product owner |
| F19 | low | design.md — Document map; Repository ownership | Native GitHub Project/sub-issue setup is not established. Confirm whether Markdown issue hierarchy suffices; no issue mutation is part of this review. | FR-OPS-06 | OPS-03 #45 | Falcone integration team |
| F20 | medium | architecture.md — Recommended stack and rationale | If measurement shows shared-cluster isolation cannot meet the agreed budget, a dedicated-instance exception would change D5: **requires operator decision**. Retain D5 until a separately accepted decision; no ADR here selects that exception. | FR-OPS-01, FR-OBS-06 | OPS-01 #43, OBS-03 #42 | SRE/platform team escalates to Falcone product owner and operator |

## Open-question map

All 13 rows of [open-questions.md, Open](open-questions.md#open) appear below in source order. Roles are drawn from its Ownership section. “ADR” means a proposed route to resolution, not an accepted answer. A named role must obtain any external owner evidence; this review invents no missing contract definitions or deployed facts.

| Question | Proposed resolution or remaining action | Accountable owner role | Existing gate |
|---|---|---|---|
| What is the maximum permitted wait? | ADR-0009 parameterizes W_max; product must set a multi-month-compatible value before retention commitments. | Falcone product owner | M0 product review |
| Which deployed Falcone version and contracts are authoritative? | Record deployed image/source/contract inventory (F13); ADR-0004 and ADR-0006 require authoritative upstream repo/path/version confirmation. | Falcone integration team | M0 / MIG-01 |
| What are starts/s, transitions/run, waiting-run count, schedule count and retention? | ADR-0013 requires Temporal staging measurement; no serverless-throughput substitution. | SRE/platform team with Release/QA maintainers | M0 / capacity gate |
| Is S3 currently SeaweedFS, RustFS or another deployment? | Confirm provider and adapter guarantees (F14); ADR-0012 keeps object references provider-neutral. | Falcone integration team | INT-03 |
| What corporate OpenShift release and PostgreSQL HA service are available? | Record actual platform versions, restricted-resource compatibility, HA, backup/PITR and connection-budget terms (F15, ADR-0003); D7 k3s stand-in is not qualification. | SRE/platform team | OPS-01 |
| Which largeTask.run profiles and native Python/data libraries must survive? | Inventory required profiles with product, qualify only serverless-supported paths via ADR-0006 or block their migration. | Falcone integration team with Falcone product owner | INT-02 |
| Should the trusted-worker protocol (ACT-01) reuse the `ctr-worker-execution-api` envelope? | ADR-0006 proposes separate internal trusted context unless owners confirm envelope compatibility; no parallel serverless protocol. | Workflow/runtime maintainers with Falcone integration team | M1 / ACT-01 |
| How does user/role revocation affect long-lived runs? | ADR-0011 proposes blocking newly unauthorized effects, typed incidents and controlled reauthorization; service owners confirm revocation behavior. | Security engineers with Falcone integration team | TEN-02 |
| Which approval actors, segregation-of-duty rules and deadlines apply? | Product defines policies (F16); preserve existing identity and make HUM-04 extensions opt-in. | Falcone product owner | HUM-01 / HUM-04 |
| How are retries, failed starts, waits, queued runs, idle capacity and history billed? | Product/integration define Falcone policy (F17); engine implements supplied limits and idempotent facts. | Falcone product owner with Falcone integration team | TEN-03 |
| What are accepted availability, recovery and latency targets? | ADR-0013 supplies measurement/qualification plan; product and SRE agree workload, exclusions and targets before any contractual commitment. | Falcone product owner with SRE/platform team | OBS-03 |
| Who owns on-call, database recovery, security qualification and runtime upgrades? | Name accountable people and escalation rota for each responsibility (F18); this review only proposes role-level routing. | SRE/platform team with Workflow/runtime maintainers, Security engineers and Falcone product owner | OPS-03 |
| Is native GitHub Project/sub-issue setup required? | Confirm administration preference (F19); current labels/Markdown hierarchy remain, without connector mutations. | Falcone integration team | Project administration |

## Operator decisions and follow-up boundaries

D1 ownership, D2 TypeScript, D3 facade/drainage, D4 contract reuse, D5 separate shared-cluster database, D6 MIT, D7 test boundaries and D8 waits/compensation remain intact. F20 is a conditional exception for operator consideration only, marked **requires operator decision**; it is not decided by an ADR. No proposal here changes any D-decision.

Before decomposing work affected by a blocker, the operator reviews the relevant ADR and the owner records the missing product choice, contract inventory or measurement dependency. Other findings retain their implementation/integration/production gates. R3-sensitive ADRs require the separate review and approval stated above. Named reviewer identity, STO-03 and serverless contract paths/versions, W_max, profile requirements and platform service terms remain open until their owners supply them.

The generated design read by decomposition does not embed these new files. An operator-reviewed follow-up must apply appropriate source edits, update open-question dispositions only when actually resolved and regenerate documents. The diffs below are proposals for that follow-up, not acceptance of any ADR. This review does not create or modify issues in any repository, qualify infrastructure, or run cluster workloads.

## Proposed source diffs — unapplied

These patches use current source context and preserve D1–D8. They expose proposal/evidence gates in the source consumed by the generator; they do not mark the ADRs Accepted. The planning-source patch clarifies existing story descriptions without adding requirements, stories or dependencies. Additional per-repository technical issues remain operator-owned follow-up work. No source file shown below is modified by this ChangeSet.

Proposed `design.md` patch:

```diff
--- a/docs/design.md
+++ b/docs/design.md
@@ -63,6 +63,12 @@

 Do not remove Temporal merely because M1 demonstrations succeed. Some deployed workflows may remain on the old engine for their full lifetime.

+## Proposed architecture decisions before decomposition
+
+The [architecture review](architecture-review.md) indexes Proposed ADRs 0002–0013 covering ownership, persistence, shared primitives, dispatch, serverless tasks, expressions, calendars, versions, migration, credentials, history and capacity. D1–D8 remain accepted; these proposals require individual operator review before technical decomposition and do not silently close open questions.
+
+Contract paths/versions, maximum wait, deployed profile inventory and measured resource budgets remain owner-confirmation gates. RLS, expression isolation, credentials and live-run migration additionally require R3 review, a second reviewer and explicit operator approval before acceptance. Apply only accepted decisions to implementation plans; retain unresolved questions with accountable roles from open-questions.md.
+
 ## Document map

 The combined design document, [falcone-workflow-design.md](falcone-workflow-design.md), is generated from these chapters and is what Hermes's backlog decomposition reads.
```

Proposed `architecture.md` patch:

```diff
--- a/docs/architecture.md
+++ b/docs/architecture.md
@@ -120,3 +120,14 @@
 Retain Falcone API/gateway, Keycloak, PostgreSQL, Kafka, S3 interface, secret management, console and observability. Replace Temporal server coordination, SDK client calls, interpreter primitives, activities' Temporal Context, schedules, history projection and ancestry checks. Rewrite metadata bindings while preserving public contracts. Keep legacy workers and Temporal during drainage.

 Do not require a new Redis, Elasticsearch, Dapr or Conductor deployment for the baseline. Native execution does not require Kubernetes API access; only optional trusted existing large-task adapters may need tightly scoped namespaced job access. Their compatibility with the restrictive untrusted-code policy must be qualified separately.
+
+## Decision qualification before decomposition
+
+Proposed ADRs 0002–0013 and architecture-review.md record the unresolved choices below; none supersedes D1–D8. Operator review and owner evidence precede decomposition of affected blockers. R3-sensitive acceptance separately requires a second reviewer and explicit operator approval.
+
+- Ownership and persistence (ADR-0002/0003): split technical deliverables by repository; qualify non-bypass runtime RLS, transaction-local tenant scope, separate migration access and platform HA/PITR/IO terms. Connection budgets remain provisional pending M0 measurement.
+- Shared primitives and dispatch (ADR-0004/0005): confirm STO-03 transaction participation, module path/version and durable recovery with its owners. If delivery is late, gate production integration rather than build a parallel module. Lease/heartbeat/scan settings are provisional pending M0; fenced completion never guarantees exactly-once external effects.
+- Serverless and expressions (ADR-0006/0007): ctr-worker-execution-api and ctr-job-checkpoint interfaces remain assumptions until owner-confirmed. Review ACT-01 envelope reuse without inventing another serverless protocol. Pin CEL limits and isolate evaluation outside engine processes and database transactions; arbitrary user code stays in falcone-serverless.
+- Calendars and versions (ADR-0008/0009): fixture legacy schedule aliases/defaults and additive time-zone/DST behavior. Product sets W_max; retain versions referenced by open runs for the longest remaining wait. DSL-06 is native-to-native only, with audited atomic mapping and no Temporal history conversion.
+- Migration and authority (ADR-0010/0011): persist backend routing, fence schedule/trigger handover and retain existing native runs through rollback. Resolve short-lived task credentials from authoritative lineage under current policy; unauthorized new effects fail closed pending controlled reauthorization.
+- History and capacity (ADR-0012/0013): keep SSE cursors monotonic across linked history segments, retain live object references and coordinate restore. Measure Temporal staging in M0 and independently qualify native load, fairness and recovery; all capacity and service objectives remain provisional.
```

Proposed `planning-source.json` patch:

```diff
--- a/docs/planning-source.json
+++ b/docs/planning-source.json
@@ -229,7 +229,7 @@
         {
           "title": "Migrate in-flight runs between flow versions",
           "story": "As a workspace operator, I want to move waiting runs to a corrected version of the same flow so that a definition fix can reach runs that wait for months.",
-          "description": "Native-to-native only: migrate selected waiting or running native runs to another published version of the same flow using an explicit node-occurrence mapping, validated in a dry run and applied atomically per run. This is not a Temporal-history converter (FR-MIG-04). Credential lineage, quota reservations and absolute timer due times carry over unchanged.",
+          "description": "Native-to-native only: dry-run validate explicit node-occurrence mappings and apply atomically per run, preserving credential lineage, quota reservations and absolute timer due times. Proposed ADR-0009 requires R3 acceptance with a second reviewer and operator approval; product sets W_max and live version references prevent artifact deletion. No Temporal-history converter is authorized.",
           "phase": "M3",
           "effort": "L",
           "dependencies": [
@@ -259,7 +259,7 @@
         {
           "title": "Implement the transactional run state machine",
           "story": "As a platform engineer, I want atomic state transitions so that crashes cannot lose accepted work.",
-          "description": "Persist run state, history, ready work and outbox records in one transaction with optimistic revisions.",
+          "description": "Persist run state, history, ready work and outbox records in one transaction with optimistic revisions. Proposed ADR-0003/0004 require operator review of runtime RLS, platform budgets and owner-confirmed STO-03 transaction participation before dependent implementation; no parallel shared module is authorized.",
           "phase": "M1",
           "effort": "L",
           "dependencies": [
@@ -330,7 +330,7 @@
         {
           "title": "Define the native activity worker protocol",
           "story": "As a connector maintainer, I want an engine-neutral task context so that Falcone adapters no longer import Temporal.",
-          "description": "Specify claim, heartbeat, complete and fail messages with run/occurrence/attempt identity and credentials.",
+          "description": "Specify the internal trusted-worker context with run/occurrence/attempt identity and opaque credential references. Proposed ADR-0006 requires contract-owner confirmation of ctr-worker-execution-api envelope compatibility before choosing reuse; serverless invocation/checkpoints retain the upstream contracts and shared fencing module.",
           "phase": "M1",
           "effort": "L",
           "dependencies": [
@@ -830,7 +830,7 @@
         {
           "title": "Consume the falcone-serverless execution and checkpoint contracts",
           "story": "As a platform developer, I want one shared invocation contract so that workflow and serverless can evolve independently.",
-          "description": "Consume falcone-serverless's worker execution API (ctr-worker-execution-api) and job checkpoint contract (ctr-job-checkpoint) instead of defining a workflow-specific protocol. Keep workflow state in falcone-workflow and untrusted computation in falcone-serverless; the serverless Temporal-activity tasks stay while Temporal serves existing runs. Separate legacy largeTask support.",
+          "description": "Consume falcone-serverless worker execution API (ctr-worker-execution-api) and job checkpoint contract (ctr-job-checkpoint), retaining Temporal activities during drainage. Proposed ADR-0006 gates integration on owner-confirmed paths, versions, fixtures, retry/lease/metering/checkpoint ownership and qualified legacy profiles; no workflow-specific serverless protocol or runtime cycle is permitted.",
           "phase": "M0",
           "effort": "L",
           "dependencies": [
@@ -1014,7 +1014,7 @@
         {
           "title": "Implement upgrade, backup and recovery runbooks",
           "story": "As an on-call engineer, I want tested operating procedures so that releases and incidents are recoverable.",
-          "description": "Use expand/contract schema migrations, drain behavior, PostgreSQL HA and coordinated payload backup policies.",
+          "description": "Use expand/contract schema migrations, bounded drain, platform-confirmed PostgreSQL HA/PITR and coordinated payload backup policies. Proposed ADR-0003/0009/0012 require retention of live interpreter/object references, explicit rollback limits and measured restore evidence before qualification.",
           "phase": "M3",
           "effort": "L",
           "dependencies": [
@@ -1085,7 +1085,7 @@
         {
           "title": "Build a migration inventory and differential harness",
           "story": "As a release engineer, I want evidence of semantic parity so that unsupported flows are not cut over.",
-          "description": "Inventory deployed DSLs, open runs, schedules, Temporal patches and SDK usage; use isolated effects for comparisons.",
+          "description": "Inventory deployed DSLs, open runs, schedules, Temporal patches, SDK usage and authoritative contract/image versions; compare outcomes with isolated effects. Proposed ADR-0013 requires the read-only Temporal staging workload baseline in M0 before numeric lease, connection-budget or capacity commitments.",
           "phase": "M0",
           "effort": "L",
           "dependencies": [
```
