# 6. Additional proposals and trade-offs

| Path | Scalability | Developer experience | Operational cost | Falcone compatibility |
|---|---|---|---|---|
| **Recommended: native persisted DSL state machine** | SQL contention and history volume set initial ceiling; partition after measured need | Reuses current visual graph and task catalog | Few new services, but Falcone owns durability and incident response | Direct control of existing contracts; internal migration required |
| **Embed DBOS beneath a Falcone-owned facade/interpreter** | Application workers plus PostgreSQL; qualify actual DSL and concurrency load | Faster access to durable primitives, ongoing library semantics to learn | Lower implementation burden; retain a third-party library dependency | Can still be a custom Falcone service if product contracts remain first-party; requires deliberate approval of reuse |
| **Go engine plus Node adapters** | Potentially efficient concurrency and smaller runtime footprint; benchmark rather than assume | Two language/tooling stacks and CEL equivalence work | Additional build/release/debug surface | Narrow protocol helps, but cross-language numeric/error semantics need fixtures |
| **Temporary Temporal/native dual backend** | Independent backends during migration; more total resource consumption | Stable client facade and gradual adoption | Highest temporary operating cost | Safest way to preserve in-flight runs; never execute the same real side effect twice |
| **Adopt Conductor or Dapr as the engine** | Mature distributed primitives and worker ecosystems | Another model/configuration surface | Replaces one external runtime with another | Useful contingency/reference, but diverges from a fully custom engine goal |
| **Full arbitrary-code replay runtime** | Potentially broad durable-programming capability | Flexible SDK authoring but determinism/versioning constraints | Very high implementation and security burden | Unnecessary unless inventory shows real code-authored workflow demand |
| **Active-active multi-region initially** | Regional resilience but complex ordering and conflict coordination | More failure modes for authors | Consensus, replicated state and stronger on-call requirements | Defer; prefer tested single-region HA and disaster recovery first |

## Optional enhancements after parity

- **Versioned connector registry:** trusted platform adapters with input/output schema, idempotency and cancellation declarations. Third-party tenant plug-ins execute in falcone-serverless rather than engine processes.
- **Policy hooks:** Falcone may choose pluggable decision models for admission or branching. Pin policy version and persist decisions; policy calls cannot become nondeterministic replay inputs.
- **Reusable sub-flows:** immutable library versions scoped to workspace, with explicit cross-workspace sharing permissions rather than arbitrary ID references.
- **Dry-run planner:** validate paths, quotas and connector permissions without executing effects. It predicts feasibility, not actual external outcomes.
- **Event compaction and query projections:** optimize monitoring separately from authoritative state, preserving cursor semantics and retention boundaries.
- **Per-tenant dedicated queues/databases:** offer isolation for heavy tenants only after shared scheduling limits are measured; more operational overhead and migration machinery.

## Accepted technical costs of the recommendation

The custom engine gives Falcone control over product behavior but transfers correctness responsibility to its maintainers. Durable task semantics, schedule races, retries, credentials and recovery are substantial engineering work. A graph executor with a retry loop is insufficient.

Prioritize migration of existing behavior before new orchestration languages, broad plug-in marketplaces or generic multi-region infrastructure. PostgreSQL reduces component count but can become a shared bottleneck; measurements decide when to isolate or partition it.

