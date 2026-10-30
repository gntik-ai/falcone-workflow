# ADR-0002: Repository ownership and per-repository story split

Status: Proposed

## Context

[design.md, Repository ownership](../design.md#repository-ownership) and [architecture.md, Repository placement and shared contracts](../architecture.md#repository-placement-and-shared-contracts) establish D1. Product stories cross repository boundaries; treating each story as one implementation ticket would blur ownership of the public API, engine and deployment. FR-CON-01, FR-INT-03 and FR-OPS-01 span CON-02 (#14), INT-02 (#38) and OPS-01 (#43).

## Decision

Propose a decomposition rule that preserves D1: one technical issue per repository, with one accountable owner, explicit deliverables, upstream contract dependencies and independent acceptance evidence. This ADR creates no issues and assigns no implementation outside this repository.

| Repository | Technical deliverables | Accountable role |
|---|---|---|
| `gntik-ai/falcone-workflow` | Interpreter, evaluator, transactional state, timers, scheduler, lease consumers and trusted activity workers | Workflow/runtime maintainers |
| `gntik-ai/falcone` | Public facade, routing, console, CLI, quotas, admission, service adapters and the shared module produced by STO-03 | Falcone integration team |
| `gntik-ai/falcone-serverless` | Qualified user computation, worker execution and checkpoint contracts | Contract owners, coordinated by Falcone integration team |
| `gntik-ai/falcone-charts` | Engine and worker packaging and restricted deployment resources | SRE/platform team |

For CON-02 (#14), separate facade routing from the engine's internal durable-start/read contract. For INT-02 (#38), separate consuming pinned contracts here from upstream contract delivery. For OPS-01 (#43), separate application configuration from chart resources. Record dependencies in both directions as references, without introducing a runtime cycle. Missing upstream capabilities remain findings for their owners; no local substitute facade, chart or serverless protocol is authorized.

## Alternatives

- A single cross-repository ticket obscures review and release boundaries.
- Moving facade or charts here would change D1 and is outside this proposal.
- Decomposing by component without an owner leaves contract integration unaccountable.

## Consequences

Decomposition can produce independently reviewable changes while product stories remain the end-to-end acceptance unit. Workflow/runtime maintainers and Falcone integration team must agree contract versions and ordering before implementation; Release/QA maintainers retain cross-repository fixture evidence. D2–D8 remain unchanged. Operator review of the proposed ADRs precedes backlog decomposition; acceptance of this ADR does not authorize publication or rollout.
