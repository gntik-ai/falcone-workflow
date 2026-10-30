# 5. Open questions and decisions

The operator accepted the architecture direction on 30 October 2026 ([ADR 0001](adr/0001-native-falcone-workflow.md)). The questions it answers are recorded as decided below; the rest remain open with a provisional direction. Publishing the backlog does not silently resolve them.

## Decided (2026-10-30)

| Question | Decision |
|---|---|
| Which repositories own the work? | D1: engine, evaluator, scheduler/timer/lease services and trusted task workers in falcone-workflow; facade, backend routing, console, CLI, quotas, admission and service adapters in falcone; Helm chart in falcone-charts. A cross-repository story is split into one issue per repository. |
| Which engine language does the team want to maintain? | D2: TypeScript on Node.js. Go is no longer an M0 alternative. |
| Must direct Temporal SDK workflows or raw APIs remain compatible? | D3: no. Falcone's workflow API and DSL stay the public contract; both engines run behind the facade during migration; existing Temporal runs finish on Temporal. CON-01 still inventories direct callers as migration items. |
| What authoring experience is required? | D3: the Falcone DSL (visual editor, JSON/YAML contracts and the CLI on the same DSL) is the authoring contract. Code-authored orchestration is not offered. |
| Which serverless invocation, checkpoint, outbox/inbox and lease contracts does the engine use? | D4: falcone-serverless's `ctr-worker-execution-api` and `ctr-job-checkpoint`, and the shared Falcone outbox/inbox and lease/fencing module from falcone-serverless story STO-03. INT-02 consumes them. |
| Where does workflow state live? | D5: a separate database on the shared PostgreSQL cluster with a connection budget, not a schema in Falcone's database. |
| Which license should the new service use? | D6: MIT, the same as Falcone. No upstream code is copied; any reuse is still reviewed. |
| Where do cluster tests run? | D7: dedicated `fw-test-*` namespaces; read access to `in-falcone-staging`; `family-rentals-prod`, `musematic*` and `llmwiki*` are off limits; k3s with Pod Security "restricted" stands in for OpenShift. |
| Are multi-month waits and new compensation semantics required? | D8: keep current waits and approvals, support multi-month waits, compensation is opt-in and versioned. |
| Does CI bootstrap block M0? | No. The repository seed provides CI (typecheck, unit tests and the generated-documentation check); OPS-03 keeps release gates and ownership. |

## Open

| Question | Provisional direction | Gate |
|---|---|---|
| What is the maximum permitted wait? | At least several months (D8). The product owner sets the value; interpreter and definition retention (FR-DSL-06, FR-OPS-03) follows it. | M0 product review |
| Which deployed Falcone version and contracts are authoritative? | Inspected source is a pinned repository snapshot, not a deployed inventory. | M0 / MIG-01 |
| What are starts/s, transitions/run, waiting-run count, schedule count and retention? | Measure on the current Temporal staging deployment in M0 (MIG-01). Do not reuse serverless message throughput as workflow throughput. | M0 / capacity gate |
| Is S3 currently SeaweedFS, RustFS or another deployment? | Provider-neutral Falcone adapter. Prior serverless context named SeaweedFS; actual provider must be confirmed. | INT-03 |
| What corporate OpenShift release and PostgreSQL HA service are available? | Standard restricted namespaced resources; k3s with Pod Security "restricted" is the test stand-in (D7). Record the actual OpenShift version and the HA, backup and connection-budget terms of the shared PostgreSQL cluster before qualification. | OPS-01 |
| Which largeTask.run profiles and native Python/data libraries must survive? | Do not silently run arbitrary tenant native code. Preserve only paths qualified through the falcone-serverless contracts (D4) or block migration. | INT-02 |
| Should the trusted-worker protocol (ACT-01) reuse the `ctr-worker-execution-api` envelope? | D4 covers serverless execution; ACT-01 keeps an internal engine-to-worker protocol on the shared lease/fencing module unless the contract owners decide otherwise. | M1 / ACT-01 |
| How does user/role revocation affect long-lived runs? | Fail closed for new unauthorized effects; record a policy-blocked incident and allow controlled reauthorization. | TEN-02 |
| Which approval actors, segregation-of-duty rules and deadlines apply? | Preserve current verified identity; HUM-04 adds quorum, initiator prohibition and escalation as opt-in mechanisms; the product defines the policies. | HUM-01 / HUM-04 |
| How are retries, failed starts, waits, queued runs, idle capacity and history billed? | Falcone owns policy; engine emits idempotent usage facts and enforces supplied limits. | TEN-03 |
| What are accepted availability, recovery and latency targets? | Proposed targets in architecture.md; no contractual SLA before measurement. | OBS-03 |
| Who owns on-call, database recovery, security qualification and runtime upgrades? | Named Falcone maintainers, SRE, security and product owners required. | OPS-03 |
| Is native GitHub Project/sub-issue setup required? | Issues use labels and Markdown hierarchy; connector does not expose native parent mutation. | Project administration |

## Questions that block implementation choices

The 30 October 2026 decisions settle raw Temporal compatibility, the engine language, the database placement and the serverless contracts. The maximum wait and the required native task profiles still shape M1 and INT-02. Deployed-contract inventory, measured capacity and operational ownership block production commitments.

## Ownership

- **Falcone product owner:** supported semantics, DSL evolution, quotas, compatibility and rollout acceptance.
- **Workflow/runtime maintainers:** state machine, persistence migrations, interpreter versions, connector protocol and correctness tests.
- **Falcone integration team:** facade, console, identity, billing and task adapters.
- **SRE/platform team:** database HA, deployment, dashboards, backups, capacity, on-call incidents and recovery exercises.
- **Security engineers:** threat model, expression isolation, credential lineage, tenant boundary tests, dependency review and security release qualification.
- **Release/QA maintainers:** contract fixtures, crash matrices, compatibility gates and evidence retention.

A small team may combine roles, but accountable owners and an escalation rota must exist before production.
