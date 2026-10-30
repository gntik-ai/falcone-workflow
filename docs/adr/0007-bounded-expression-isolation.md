# ADR-0007: Bounded expression evaluation outside engine processes

Status: Accepted (2026-10-30)

Accepted by the operator on 30 October 2026 as written. The operator explicitly gave the R3 approval this ADR requires.

## Context

[architecture.md, Recommended stack and rationale](../architecture.md#recommended-stack-and-rationale) calls for bounded CEL worker processes; [design.md, Recommended boundary](../design.md#recommended-boundary) forbids arbitrary tenant code in the engine. FR-DSL-03, FR-DSL-04 and FR-DSL-08 affect DSL-02 (#17) and DSL-01 (#16). Language choice D2 does not establish expression isolation or resource bounds.

## Decision

Propose a pool of separate evaluator processes running trusted, pinned CEL implementation code, with no network, filesystem capabilities or arbitrary-code escape exposed to expressions. A worker thread or an in-process promise timeout alone is insufficient isolation. Deployment-level confinement and termination must be qualified by Security engineers. Arbitrary user computation remains exclusively in falcone-serverless; the evaluator interprets bounded expression data only.

Each interpreter version pins the CEL library, supported functions and configured limits for expression length, input bytes, evaluation cost/steps, wall time, memory and result bytes. Reject excessive input before evaluation; terminate and replace a process that exceeds execution limits. Exact limits are provisional pending M0 adversarial measurement, with versioned configuration required before production. Do not add external service calls as expression functions.

Evaluate outside database transactions against an immutable input snapshot and persisted evaluation time. Clock functions use that time, never restart wall time. Commit selected branches and bounded results under the expected run revision; a revision conflict discards the result and reloads committed state. Recovery uses persisted outcomes or the same pinned inputs and time. Apply the same limits to trigger filters, mappings and concurrency-key expressions, preserving verified tenant scope.

Malformed, incompatible or excessive expressions produce stable typed errors and a node incident where required; they must not crash the engine or silently select another branch. Preserve apiVersion v1.0 null, numeric, missing-reference and error behavior through differential fixtures; incompatibility blocks migration rather than changing semantics.

Acceptance requires R3 review with a second reviewer (Security engineers) and explicit operator approval. Evidence includes adversarial resource exhaustion, capability escape attempts, worker termination, restart determinism and compatibility fixtures.

## Alternatives

- Unbounded in-process evaluation risks engine availability and cannot enforce a hard memory limit.
- Arbitrary JavaScript evaluation conflicts with the data-only interpreter boundary.
- Resolving expressions through network services during a transaction creates unbounded lock duration and nondeterminism.

## Consequences

Separate processes add startup, IPC and scheduling costs to benchmark under ADR-0013. Process separation is a proposed mechanism, not proof of security qualification. Versioning must retain both CEL behavior and cost limits for long-lived runs under ADR-0009.
