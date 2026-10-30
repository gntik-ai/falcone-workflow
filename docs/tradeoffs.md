# 6. Additional proposals and trade-offs

| Path | Scalability | Developer experience | Operational cost | Falcone compatibility |
|---|---|---|---|---|
| **Selected: native persisted DSL state machine in TypeScript (ADR 0001)** | SQL contention and history volume set initial ceiling; partition after measured need | Reuses current visual graph and task catalog | Few new services, but Falcone owns durability and incident response | Direct control of existing contracts; internal migration required |
| **Embed DBOS beneath a Falcone-owned facade/interpreter** | Application workers plus PostgreSQL; qualify actual DSL and concurrency load | Faster access to durable primitives, ongoing library semantics to learn | Lower implementation burden; retain a third-party library dependency | Can still be a custom Falcone service if product contracts remain first-party; requires deliberate approval of reuse |
| **Temporal/native dual backend during migration (required by D3)** | Independent backends during migration; more total resource consumption | Stable client facade and gradual adoption | Highest temporary operating cost | Safest way to preserve in-flight runs; never execute the same real side effect twice |
| **Adopt Conductor or Dapr as the engine** | Mature distributed primitives and worker ecosystems | Another model/configuration surface | Replaces one external runtime with another | Useful contingency/reference, but diverges from a fully custom engine goal |
| **Active-active multi-region initially** | Regional resilience but complex ordering and conflict coordination | More failure modes for authors | Consensus, replicated state and stronger on-call requirements | Defer; prefer tested single-region HA and disaster recovery first |

## Rejected paths

| Path | Reason |
|---|---|
| Go engine plus Node adapters | Closed by D2: the engine is TypeScript on Node.js. A second language would add build, release and CEL-equivalence work without measured need. |
| Raw Temporal SDK or server compatibility | Closed by D3: Falcone's workflow API and DSL are the public contract; existing Temporal runs finish on Temporal. |
| Code-first durable-function SDKs with deterministic replay, and `patched()`/`getVersion`-style patching (Temporal, Restate, DBOS, Hatchet, Inngest) | Conflicts with D3 and the DSL-only authoring contract; DSL apiVersion pinning plus audited in-flight migration (DSL-06) replaces code patching. |
| Inline script nodes executed by the engine (Windmill or n8n Code nodes, Kestra script tasks) | Engine processes run only trusted code; untrusted code must go through `functions.invoke` to falcone-serverless. |
| BPMN import or execution, and pod-per-step execution (Argo) | BPMN is not the Falcone DSL; pod-per-step conflicts with restricted Kubernetes and the no-CRD constraint. |
| Elasticsearch or another visibility store, active-active multi-region, in-engine plug-in marketplaces | Run search stays on PostgreSQL (OBS-05); multi-region and marketplaces add operations and security surface out of scope for parity. |
| Generic Temporal-history conversion | Forbidden by FR-MIG-04; in-flight Temporal runs drain on Temporal or move only through a validated application-level checkpoint. |

## Optional enhancements after parity

These are not requirements. Each needs a product decision and a versioned DSL or API change before it enters the backlog.

- **Versioned connector registry:** trusted platform adapters with input/output schema, idempotency and cancellation declarations. Third-party tenant plug-ins execute in falcone-serverless rather than engine processes.
- **Policy hooks:** Falcone may choose pluggable decision models for admission or branching. Pin policy version and persist decisions; policy calls cannot become nondeterministic replay inputs.
- **Dry-run planner:** beyond CON-04 test mode, validate paths, quotas and connector permissions without executing effects. It predicts feasibility, not actual external outcomes.
- **Event compaction and query projections:** optimize monitoring separately from authoritative state, preserving cursor semantics and retention boundaries.
- **Per-tenant dedicated queues/databases:** offer isolation for heavy tenants only after shared scheduling limits are measured; more operational overhead and migration machinery.
- **Bounded loops (GAP-24):** a structured do-while/until node with mandatory maximum iterations and a per-iteration history bound; the rest of the graph stays acyclic. Needed for polling and agent loops; history growth relies on continuation (FR-DUR-05).
- **Detached children and parent-close choice (GAP-25):** sub-flow `onParentClose` (terminate, request-cancel or abandon) and `wait: false`. Orphaned work keeps its quota.
- **Environments and promotion (GAP-26):** facade-owned export/import of definition bundles across Falcone stages with deterministic hashes, re-bound credential references and pinned sub-flow versions; credentials are never exported.
- **Per-flow RBAC and payload visibility (GAP-27):** grants for start, cancel, approve and view-payload beyond workspace roles, never weakening Falcone roles (FR-TEN-02).
- **Worker pools and affinity (GAP-28):** route task types to named worker pools, for example heavy LLM batch or a dedicated tenant pool, after shared limits are measured.
- **Memoization (GAP-29):** opt-in, tenant-scoped result reuse only for connectors declared pure, keyed by input hash and version.
- **Lineage (GAP-30):** record the object references each node occurrence consumes and produces.
- **Business calendars (GAP-31):** holiday and working-day functions for schedules and wait-until, with owned and versioned calendar data.
- **Composite event triggers (GAP-32):** AND/OR across several events within a window, with bounded partial-match state and TTL.
- **LLM step patterns (GAP-33):** token-usage events for metering, streaming partial output to SSE, honoring provider Retry-After, tool-call approval through HUM-04 and agent loops through bounded loops; prompt and response retention must follow PII policy.
- **Cross-workspace service contracts (GAP-34):** sub-flows exposed to other workspaces through explicit grants, with cross-tenant lineage and credential scope defined first. This subsumes the earlier reusable sub-flow library idea.
- **Other later extensions from the gap analysis:** a parallel `join` attribute (all, any, n-of-m, race) in a new apiVersion, and trigger debounce, per-key batching and schedule exclusions (the later part of GAP-20).

## Accepted technical costs of the recommendation

The custom engine gives Falcone control over product behavior but transfers correctness responsibility to its maintainers. Durable task semantics, schedule races, retries, credentials and recovery are substantial engineering work. A graph executor with a retry loop is insufficient.

Prioritize migration of existing behavior before new orchestration languages, broad plug-in marketplaces or generic multi-region infrastructure. PostgreSQL reduces component count but can become a shared bottleneck; measurements decide when to isolate or partition it.
