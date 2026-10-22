# Evidence and sources

Reviewed 22 October 2026. External documentation is mutable; pin upstream code/version and license before implementation. This report provides a focused code inspection, not a complete production audit or executed benchmark.

## Falcone repository evidence

Pinned inspected commit: [47674add95223e6ccd7f6f0dcd11106469a0a30e](https://github.com/gntik-ai/falcone/tree/47674add95223e6ccd7f6f0dcd11106469a0a30e).

| Inspected path | What it establishes |
|---|---|
| [DslInterpreterWorkflow.ts](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/workflow-worker/src/workflows/DslInterpreterWorkflow.ts) | Generic DSL interpreter, Temporal primitives, approvals, children, version pinning and LLM batch phases |
| [flow-executor.mjs](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/control-plane-executor/src/runtime/flow-executor.mjs) | API boundary, identifiers, definition store, credential creation and role authorization |
| [flow-trigger-registry.mjs](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/control-plane-executor/src/runtime/flow-trigger-registry.mjs) | Cron/webhook/platform-event integration and separate schedule subsystem |
| [flow-monitoring-executor.mjs](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/control-plane-executor/src/runtime/flow-monitoring-executor.mjs) | Temporal history-to-SSE mapping, node IDs and cursor semantics |
| [catalog.mjs](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/workflow-worker/src/activities/catalog.mjs) | Current first-party task registry and legacy/harness echo behavior |
| [execution-token-ref.mjs](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/workflow-worker/src/activities/execution-token-ref.mjs) | Credential binding depends on authoritative run ancestry |
| [large-task-run.mjs](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/workflow-worker/src/activities/large-task-run.mjs) | Heartbeats, job identity, timeouts and cancellation cleanup |
| [flow-definition.json](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/packages/internal-contracts/src/flow-definition.json) | Versioned public DSL schema |
| [flow-definition-mapping.json](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/packages/internal-contracts/src/flow-definition-mapping.json) | FLW validation errors, CEL, retry mapping and schema evolution |
| [workflow-worker/package.json](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/workflow-worker/package.json) | Node/TypeScript worker and Temporal SDK dependencies |
| [workflow-worker/README.md](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/apps/workflow-worker/README.md) | Repository build rationale; early harness descriptions require comparison with current implementation |
| [Schedule-management documentation](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/docs/reference/architecture/flow-schedule-management.md) | Published routes, identity, roles, responses and status/error behavior |
| [Reconnect fix proposal](https://github.com/gntik-ai/falcone/blob/47674add95223e6ccd7f6f0dcd11106469a0a30e/openspec/changes/fix-989-schedule-temporal-reconnect/proposal.md) | Recorded rejected-connection recovery issue and intended behavior |

The workflow-worker contains production-style adapter code as well as legacy harness paths. Reading these files does not establish that a particular cluster deployed or qualified every feature.

## External primary references

- **T1:** [Temporal Server components](https://docs.temporal.io/temporal-service/temporal-server)
- **T2:** [How Temporal works](https://docs.temporal.io/encyclopedia/architecture/how-temporal-works)
- **T3:** [Temporal application workers](https://docs.temporal.io/workers)
- **C1:** [Cadence source and license](https://github.com/cadence-workflow/cadence)
- **C2:** [Cadence activities and timeout concepts](https://cadenceworkflow.io/docs/concepts/activities)
- **N1:** [Conductor OSS source, worker model and license](https://github.com/conductor-oss/conductor). This is the maintained Conductor OSS reference, rather than treating the historical Netflix repository as the current implementation.
- **A1:** [Airflow architecture](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html)
- **A2:** [Airflow executors](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/executor/index.html)
- **D1:** [Dapr Workflow overview](https://docs.dapr.io/developing-applications/building-blocks/workflow/workflow-overview/)
- **D2:** [Dapr workflow backend concepts, versioned v1.15 reference](https://v1-15.docs.dapr.io/developing-applications/building-blocks/workflow/workflow-features-concepts/). Used for the Durable Task relationship, not a claim that v1.15 is the current release.
- **B1:** [DBOS architecture](https://docs.dbos.dev/architecture)
- **B2:** [DBOS TypeScript source and MIT license](https://github.com/dbos-inc/dbos-transact-ts)
- **R1:** [Restate key concepts](https://docs.restate.dev/foundations/key-concepts)
- **R2:** [Restate server license](https://github.com/restatedev/restate/blob/main/LICENSE). The reviewed text identifies BSL 1.1, a restricted additional use grant and a future Apache-2.0 change license. It explicitly distinguishes BSL from an open-source license.

## Provenance and confidence

- **Observed:** code/schema behavior and published primary-source descriptions above.
- **Proposed:** engine implementation, PostgreSQL schema, scheduling/fairness choices, reliability targets, extensions and milestone sequencing.
- **Unverified:** production topology, achieved throughput, restore capability, actual OpenShift version, complete inventory of direct Temporal clients, and object-storage provider currently in use.
- **Not performed:** live cluster access, runtime implementation, failure/load/security tests, Temporal removal or changes to Falcone core/serverless repositories.

Before reusing upstream implementation code, record exact commit, component license and notices. The design and backlog here are original planning material; no upstream engine code is vendored.

