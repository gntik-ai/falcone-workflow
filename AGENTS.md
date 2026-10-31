# falcone-workflow: agent and contributor guide

A Falcone-owned durable workflow engine that replaces Temporal behind Falcone's workflow API ([design](docs/design.md), [architecture](docs/architecture.md), [ADR 0001](docs/adr/0001-native-falcone-workflow.md)). The engine interprets Falcone's existing workflow DSL as an explicit state machine persisted in PostgreSQL, dispatches tasks through leases with fencing, and keeps timers, schedules and inbox/outbox records in the database.

## Operator decisions (2026-10-30)

- Engine language: TypeScript on Node.js.
- No raw Temporal SDK or server compatibility. Falcone's workflow API and DSL stay the public contract. During migration both engines run behind the Falcone facade; existing Temporal runs finish on Temporal.
- The engine uses its own database on the shared PostgreSQL cluster, not a schema inside Falcone's database.
- Untrusted computation runs only in falcone-serverless. falcone-workflow uses the serverless contracts (worker execution API, job checkpoint contract) and the shared outbox/inbox and lease/fencing module instead of defining its own.
- Current waits and approvals are kept, multi-month waits are supported, and compensation is opt-in and versioned.

## Where code lives

| Repository | Owns |
|---|---|
| `gntik-ai/falcone-workflow` (this repo) | the engine, evaluator, scheduler, timer and lease services, and the trusted task workers |
| `gntik-ai/falcone` | the workflow facade and backend routing, the console, CLI, quotas, admission and service adapters |
| `gntik-ai/falcone-charts` | the Helm chart that deploys the engine and its workers |

A story that spans repositories is split into one issue per repository, each with a single owner.

## Hard rules

- Engine processes run only trusted interpreter and connector code. Tenant expressions are bounded; tenant code runs in falcone-serverless.
- External task execution is at least once. Every connector uses a stable operation key, downstream idempotency or explicit ambiguous-outcome handling. No blind retry of a non-idempotent action with an unknown outcome.
- No raw user tokens or secrets in workflow state or history. Use credential references resolved under Falcone policy.
- Restricted pods only: no operator, CRD, ClusterRole, custom RuntimeClass, elevated SCC or host access.
- Security-sensitive areas (tenant isolation, credentials, expression evaluation, migration of live runs) need a second reviewer and explicit operator approval (Hermes R3).

## Build and test

```sh
pnpm install --frozen-lockfile
pnpm typecheck
pnpm test
python3 tools/build_docs.py && git diff --exit-code -- docs/
```

`docs/planning-source.json` is the source of `requirements.md`, `backlog.md` and `backlog.json`; edit it and regenerate. CI (`.github/workflows/ci.yml`) runs the same commands. Agents do not edit `.github/`; the operator owns it.

## Cluster testing (operator decision, 2026-10-30)

- Unit and contract tests run locally and in CI. Every integration, runtime or end-to-end test that needs Kubernetes, PostgreSQL, Kafka or Falcone services runs on the shared cluster, in dedicated `fw-test-*` namespaces created and deleted by the test (the default, `FW_TEST_NAMESPACE_MODE=create`). Namespace creation is a switch because it is not always permitted (operator decision 2026-10-30): with `FW_TEST_NAMESPACE_MODE=shared` a test never creates or deletes namespaces; it uses the existing namespace named in `FW_TEST_NAMESPACE`, creates only new objects named with the run id and labelled `falcone.test/run=<id>`, and never updates, patches, relabels or deletes an object whose label is not this run's id. If creation is denied in `create` mode, the test fails before any mutation and names the switch.
- Integration tests may also read `in-falcone-staging`. Every other namespace is off limits, including `family-rentals-prod`, `musematic*` and `llmwiki*`.
- The cluster is k3s, not OpenShift. Pod Security "restricted" with seccomp `RuntimeDefault`, a read-only root filesystem and an arbitrary non-root UID stand in for OpenShift restricted-v2.
- Never print or commit secrets.

## Falcone findings

A bug or improvement found in Falcone, its charts or falcone-serverless becomes an issue in that repository. It is not worked around silently here.
