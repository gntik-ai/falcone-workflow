# ADR-0003: Persistence roles, tenant RLS and platform budgets

Status: Proposed

## Context

[architecture.md, Recommended stack and rationale](../architecture.md#recommended-stack-and-rationale) requires a separate database on the shared PostgreSQL cluster (D5), but HA, backup and resource isolation depend on the platform. [architecture.md, Data model and invariants](../architecture.md#data-model-and-invariants) makes transactions authoritative. FR-DUR-01, FR-DUR-02, FR-DUR-06, FR-TEN-01 and FR-OPS-01 affect DUR-01 (#19), TEN-01 (#34), OPS-01 (#43) and OPS-02 (#44).

## Decision

Propose an engine-owned database with separately provisioned migration and runtime roles. The runtime role is neither a table owner nor a superuser and cannot bypass RLS or perform DDL. Migration access is limited to reviewed migrations and unavailable to application workers. Enforce tenant/workspace ownership in composite keys, foreign keys and RLS; tenant-scoped tables use forced RLS so an accidental owner path does not silently bypass the boundary. Cross-tenant maintenance uses a separately reviewed platform procedure, never an ordinary runtime endpoint.

Set verified tenant/workspace context transaction-locally, fail closed when it is absent and test pool reuse across tenants. A shared scanner must claim work only through a reviewed tenant-scoped path; this proposal does not grant it unrestricted cross-tenant reads. Persist state, events, first ready work and outbox records atomically under a checked revision; Kafka is transport only.

SRE/platform team must document synchronous failover semantics, encryption, WAL and object-version backups, PITR window, restore access and measured recovery before qualification. Namespaced deployment is not evidence that these services exist. Connection-budget, pool-size, CPU, IO and capacity numbers are provisional pending M0 measurement under ADR-0013. Allocate the connection budget across replicas and engine roles, reserving recovery/migration headroom; admission must shed load before exhausting it. Escalate interference with Falcone transactions to the platform owner. Moving to a dedicated instance would require operator consideration, not an automatic change to D5.

Acceptance requires R3 review with a second reviewer (Security engineers) and explicit operator approval for tenant RLS and isolation. Isolation tests must cover absent context, forged scope, pooled connections and all persisted record types.

## Alternatives

- A schema inside Falcone's database conflicts with D5.
- Application predicates alone offer no database-level defense against scope omissions.
- A privileged runtime role simplifies scanning but bypasses the intended isolation boundary.

## Consequences

Database correctness and platform recovery become explicit dependencies rather than implied guarantees. Workflow/runtime maintainers own schema and transactional correctness; SRE/platform team owns service terms and recovery evidence. Shared-cluster IO isolation remains a measured risk. No database, role or policy is created by this documentation.
