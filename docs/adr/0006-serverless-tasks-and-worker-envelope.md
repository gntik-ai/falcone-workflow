# ADR-0006: Serverless function and job tasks and the ACT-01 envelope

Status: Accepted (2026-10-30)

Accepted by the operator on 30 October 2026 as written.

## Context

[architecture.md, Repository placement and shared contracts](../architecture.md#repository-placement-and-shared-contracts) and [migration.md, Cross-repository work](../migration.md#cross-repository-work) require D4 contract consumption and prohibit circular execution dependencies. FR-INT-03, FR-INT-04, FR-ACT-01, FR-ACT-05 and FR-INT-06 affect INT-02 (#38), ACT-01 (#22), ACT-03 (#24) and INT-03 (#39).

## Decision

Function and job tasks consume pinned `ctr-worker-execution-api` and `ctr-job-checkpoint` contracts. **Interface assumption to confirm with the owners:** their authoritative repository paths, versions, message schemas and guarantees are absent here. STO-03 module exports are likewise an assumption to confirm with owners under ADR-0004. No endpoint or TypeScript signature in this proposal is an established upstream interface.

Workflow/runtime maintainers and Falcone integration team must obtain owner-reviewed fixtures for stable operation correlation, submit acknowledgement loss, status observation, duplicate completion, cancellation, checkpoint references, retention and version negotiation. Confirm who owns execution leases, logical retries, metering and checkpoint cleanup before decomposition of integration details. These are consumer requirements to negotiate, not assertions about available upstream behavior.

Propose keeping ACT-01's trusted engine-to-worker protocol separate unless the owners demonstrate that the serverless envelope covers all required tenant/workspace, lineage, occurrence, attempt, lease generation and pinned adapter metadata without changing serverless semantics. Reuse the upstream envelope if that review confirms compatibility; otherwise keep only the internal trusted-worker context, using the shared fencing module. This conditional decision does not authorize a second invocation or checkpoint protocol for serverless. Record the envelope review outcome before ACT-01 implementation.

Persist an accepted provider job ID and checkpoint reference before further observation; recover by querying/reconciling, never blind resubmission after an ambiguous submit. Keep workflow continuation in this engine and arbitrary tenant computation in qualified falcone-serverless profiles. Execution primitives must operate without Temporal or a callback into workflow to start themselves. Retain legacy Temporal activities while old runs drain; unsupported native Python/data profiles block their migration, with no silent container fallback here.

## Alternatives

- A workflow-specific serverless execution or checkpoint API contradicts D4 and FR-INT-03.
- Assuming ACT-01 can reuse the envelope without owner evidence hides missing fencing or correlation.
- Running tenant code in trusted workers crosses the established engine boundary.

## Consequences

Contract locations, versions and ACT-01 envelope reuse remain explicit owner-confirmation gates. Simulators must be derived from confirmed contracts before they count as integration evidence. Missing capabilities are findings for the owning repository, not implementations in this ChangeSet.

## Operator resolution (2026-10-30)

The contract owners and versions are confirmed (finding F05): `ctr-worker-execution-api` v1 is defined by [falcone-serverless #124](https://github.com/gntik-ai/falcone-serverless/issues/124) and served by [falcone-serverless #130](https://github.com/gntik-ai/falcone-serverless/issues/130). `ctr-job-checkpoint` v1 is falcone-serverless plan task JOB-01.t1 (target `gntik-ai/falcone`, component functions-api), not yet published as an issue; it is a dependency to link when published. Exact API paths and versions are confirmed from the delivered code as an integration gate; this does not block decomposition. The ACT-01 envelope review above still applies.
