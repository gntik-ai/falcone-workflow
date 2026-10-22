# ADR-0001: Native Falcone workflow engine

Status: Proposed. Date: 22 October 2026.

## Context

Falcone already exposes a workflow DSL and service catalog while Temporal supplies durability, scheduling and task coordination. The requested project is a custom Falcone service replacing that dependency under restricted Kubernetes/OpenShift deployment constraints.

## Decision proposed

Implement explicit durable DSL continuation in PostgreSQL behind Falcone's existing facade. Keep trusted connectors separate from orchestration; delegate untrusted computation to qualified falcone-serverless profiles. Reuse Kafka and S3 through existing Falcone interfaces. Pin interpreter/definition versions. Provide at-least-once task delivery with connector idempotency or explicit reconciliation.

Do not recreate Temporal SDK/server compatibility without a demonstrated caller requirement. Keep old Temporal runs on their original backend during migration. Use TypeScript initially to align with inspected contracts and adapters; revisit only at M0 with evidence.

## Consequences

Smaller product-specific surface and ordinary namespaced deployment; substantial ownership of persistence correctness, retries, tenant isolation and operations. SQL state transition throughput must be benchmarked. API compatibility does not automatically imply identical runtime semantics.

## Alternatives

Embedded DBOS, Go engine, Conductor/Dapr runtime, and full code replay are evaluated in ../tradeoffs.md. Restate supplies conceptual references only under the reviewed license distinction.

## Approval required before implementation

Product compatibility scope, engineering language choice, security isolation model and named operational ownership. This ADR is not marked accepted solely because the planning repository was requested.

