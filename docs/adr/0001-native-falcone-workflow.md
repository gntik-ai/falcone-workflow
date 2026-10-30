# ADR-0001: Native Falcone workflow engine

Status: Accepted (2026-10-30). Proposed 22 October 2026; the operator accepted the direction with decisions D1–D8 below on 30 October 2026.

## Context

Falcone already exposes a workflow DSL and service catalog while Temporal supplies durability, scheduling and task coordination. The requested project is a custom Falcone service replacing that dependency under restricted Kubernetes/OpenShift deployment constraints.

## Decision

Implement explicit durable DSL continuation in PostgreSQL behind Falcone's existing facade. Keep trusted connectors separate from orchestration; delegate untrusted computation to qualified falcone-serverless profiles. Reuse Kafka and S3 through existing Falcone interfaces. Pin interpreter/definition versions. Provide at-least-once task delivery with connector idempotency or explicit reconciliation.

Operator decisions (2026-10-30):

- **D1 Repository split.** Engine, evaluator, scheduler/timer/lease services and trusted task workers in `gntik-ai/falcone-workflow`; workflow facade, backend routing, console, CLI, quotas, admission and service adapters in `gntik-ai/falcone`; Helm chart in `gntik-ai/falcone-charts`. A story spanning repositories is split into one issue per repository. Stories and epics are product-level and may span repositories; the backlog decomposition turns each story into technical issues, one per repository, each with a single owner and explicit cross-repository dependencies.
- **D2 Language.** The engine is TypeScript on Node.js. Go is no longer an M0 alternative.
- **D3 No raw Temporal compatibility.** Falcone's workflow API and DSL stay the public contract. Both engines run behind the Falcone facade during migration; existing Temporal runs finish on Temporal.
- **D4 Shared contracts.** falcone-workflow consumes falcone-serverless's worker execution API (`ctr-worker-execution-api`) and job checkpoint contract (`ctr-job-checkpoint`) and the shared Falcone outbox/inbox and lease/fencing module built by falcone-serverless story STO-03, instead of defining its own. INT-02 consumes those contracts. The serverless Temporal-activity tasks stay while Temporal serves existing runs.
- **D5 Database.** A separate database on the shared PostgreSQL cluster, not a schema in Falcone's database, with a connection budget.
- **D6 License.** MIT, the same as Falcone.
- **D7 Cluster tests.** Dedicated `fw-test-*` namespaces; tests may read `in-falcone-staging`; `family-rentals-prod`, `musematic*` and `llmwiki*` are off limits. k3s with Pod Security "restricted" stands in for OpenShift.
- **D8 Waits and compensation.** Keep current waits and approvals, support multi-month waits, and make compensation opt-in and versioned.

## Consequences

Smaller product-specific surface and ordinary namespaced deployment; substantial ownership of persistence correctness, retries, tenant isolation and operations. SQL state transition throughput must be benchmarked, starting from a capacity baseline measured on the current Temporal staging deployment in M0. API compatibility does not automatically imply identical runtime semantics. Interpreter and definition versions must be retained for at least the longest permitted wait, which is now months. Shared contracts couple release planning with falcone-serverless and Falcone; contract gaps are raised in those repositories rather than worked around here.

## Alternatives

Embedded DBOS, Conductor/Dapr runtime and full code replay are evaluated in ../tradeoffs.md. A Go engine and raw Temporal compatibility are closed by D2 and D3. Restate supplies conceptual references only under the reviewed license distinction.

## Still open

Named operational ownership, the security qualification of the deployed cluster, the maximum permitted wait and the remaining product questions in ../open-questions.md. Acceptance of this ADR does not qualify any runtime.
