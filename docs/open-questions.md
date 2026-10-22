# 5. Open questions and provisional decisions

Repository creation was confirmed. The following choices were not explicitly answered and remain proposed. Publishing this backlog does not silently resolve them.

| Question | Provisional direction | Gate |
|---|---|---|
| Must direct Temporal SDK workflows or raw APIs remain compatible? | Preserve Falcone interfaces and DSL; permit internal migration. Inventory actual direct callers first. | M0 / CON-01 |
| What authoring experience is required? | Keep existing visual DSL/editor and JSON/YAML contracts; developer CLI uses the same DSL. Arbitrary code-authored orchestration is deferred. | M0 |
| Are multi-month waits and new compensation semantics required? | Preserve current waits/approvals; design for long duration. Compensation is opt-in versioned scope. | M0 product review |
| Which engine language does the team want to maintain? | TypeScript for current ecosystem alignment; Go only if qualification or team preference justifies migration cost. | M0 |
| Which deployed Falcone version and contracts are authoritative? | Inspected source is a pinned repository snapshot, not a deployed inventory. | M0 / MIG-01 |
| What are starts/s, transitions/run, waiting-run count, schedule count and retention? | Do not reuse serverless message throughput as workflow throughput. Measure independently. | Capacity gate |
| Is S3 currently SeaweedFS, RustFS or another deployment? | Provider-neutral Falcone adapter. Prior serverless context named SeaweedFS; actual provider must be confirmed. | INT-03 |
| What corporate OpenShift release and PostgreSQL HA service are available? | Standard restricted namespaced resources; record actual version and privileges before qualification. | OPS-01 |
| Which largeTask.run profiles and native Python/data libraries must survive? | Do not silently run arbitrary tenant native code because no sandbox RuntimeClass is available. Preserve only qualified paths or block migration. | INT-02 |
| How does user/role revocation affect long-lived runs? | Fail closed for new unauthorized effects; record policy-blocked state and allow controlled reauthorization. | TEN-02 |
| Which approval actors, segregation-of-duty rules and deadlines apply? | Preserve current verified identity and explicitly define reviewers per product policy. | HUM-01 |
| How are retries, failed starts, waits, idle capacity and history billed? | Falcone owns policy; engine emits idempotent usage facts and enforces supplied limits. | TEN-03 |
| What are accepted availability, recovery and latency targets? | Proposed targets in architecture.md; no contractual SLA before measurement. | OBS-03 |
| Who owns on-call, database recovery, security qualification and runtime upgrades? | Named Falcone maintainers, SRE, security and product owners required. | OPS-03 |
| Which license should the new service use? | No upstream code copied; choose before implementation and review any reuse. | M0 |
| Is native GitHub Project/sub-issue setup required? | Issues use labels and Markdown hierarchy; connector does not expose native parent mutation. | Project administration |

## Questions that block implementation choices

Confirm raw Temporal compatibility, engine language and required native task profiles before building the core. Deployed-contract inventory, capacity and operational ownership block production commitments. The current documentation and backlog remain useful while those decisions are pending.

