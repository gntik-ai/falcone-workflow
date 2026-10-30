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

## Functional gap analysis references

Reviewed 30 October 2026 for the functional gap analysis. Capability claims cite these primary documentation pages; licenses come from the GitHub license API and LICENSE files on the same date.

- **Temporal:** [schedules](https://docs.temporal.io/schedule), [retry policies](https://docs.temporal.io/encyclopedia/retry-policies), [activity timeouts](https://docs.temporal.io/encyclopedia/detecting-activity-failures), [message passing](https://docs.temporal.io/encyclopedia/workflow-message-passing), [signal/update-with-start](https://docs.temporal.io/sending-messages), [worker versioning](https://docs.temporal.io/worker-versioning), [priority and fairness](https://docs.temporal.io/develop/task-queue-priority-fairness), [visibility](https://docs.temporal.io/visibility), [workflow CLI and batch](https://docs.temporal.io/cli/workflow), [continue-as-new](https://docs.temporal.io/workflow-execution/continue-as-new), [ID reuse/conflict](https://docs.temporal.io/workflow-execution/workflowid-runid), [activity operations](https://docs.temporal.io/activity-operations), [parent-close policy](https://docs.temporal.io/parent-close-policy), [Nexus](https://docs.temporal.io/nexus)
- **Conductor OSS:** [task definitions](https://docs.conductor-oss.org/documentation/configuration/taskdef.html), [workflow API](https://docs.conductor-oss.org/documentation/api/workflow.html), [operators](https://docs.conductor-oss.org/documentation/configuration/workflowdef/operators/index.html)
- **Airflow 3.x:** [deferrable operators](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html), [human-in-the-loop](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/hitl.html), [deadline alerts](https://airflow.apache.org/docs/apache-airflow/stable/howto/deadline-alerts.html), [dynamic task mapping](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html), [backfill](https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html), [asset scheduling](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html)
- **Argo Workflows:** [retries](https://argo-workflows.readthedocs.io/en/latest/retries/), [synchronization](https://argo-workflows.readthedocs.io/en/latest/synchronization/), [cron workflows](https://argo-workflows.readthedocs.io/en/latest/cron-workflows/), [memoization](https://argo-workflows.readthedocs.io/en/latest/memoization/), [loops](https://argo-workflows.readthedocs.io/en/latest/walk-through/loops/), [intermediate inputs](https://argo-workflows.readthedocs.io/en/latest/intermediate-inputs/), [archive](https://argo-workflows.readthedocs.io/en/latest/workflow-archive/)
- **Camunda 8:** [instance migration](https://docs.camunda.io/docs/components/concepts/process-instance-migration/), [instance modification](https://docs.camunda.io/docs/components/concepts/process-instance-modification/), [incidents](https://docs.camunda.io/docs/components/concepts/incidents/), [multi-instance](https://docs.camunda.io/docs/components/modeler/bpmn/multi-instance/), [messages](https://docs.camunda.io/docs/components/concepts/messages/), [user tasks](https://docs.camunda.io/docs/components/modeler/bpmn/user-tasks/), [compensation](https://docs.camunda.io/docs/components/modeler/bpmn/compensation-handler/), [error events](https://docs.camunda.io/docs/components/modeler/bpmn/error-events/), [timer events](https://docs.camunda.io/docs/components/modeler/bpmn/timer-events/), [licensing](https://camunda.com/blog/2024/10/camunda-licensing-what-you-need-to-know/) and [8.6 announcements](https://docs.camunda.io/docs/reference/announcements-release-notes/860/860-announcements)
- **Kestra:** [concurrency](https://kestra.io/docs/workflow-components/concurrency), [schedule trigger](https://kestra.io/docs/workflow-components/triggers/schedule-trigger), [SLA](https://kestra.io/docs/workflow-components/sla), [replay](https://kestra.io/docs/concepts/replay), [errors](https://kestra.io/docs/workflow-components/errors), [flowable tasks](https://kestra.io/docs/workflow-components/tasks/flowable-tasks)
- **Prefect 3:** [global concurrency limits](https://www.prefect.io/docs/v3/concepts/global-concurrency-limits), [interactive workflows](https://www.prefect.io/docs/v3/advanced/interactive), [automations](https://www.prefect.io/docs/v3/concepts/automations)
- **n8n:** [error handling](https://docs.n8n.io/flow-logic/error-handling/), [Wait node](https://docs.n8n.io/integrations/builtin/core-nodes/n8n-nodes-base.wait/)
- **Windmill:** [flow approval](https://www.windmill.dev/docs/flows/flow_approval), [concurrency limits](https://www.windmill.dev/docs/flows/concurrency_limit)
- **Hatchet:** [concurrency](https://docs.hatchet.run/home/concurrency), [rate limits](https://docs.hatchet.run/home/rate-limits), [priority](https://docs.hatchet.run/home/priority), [durable execution](https://docs.hatchet.run/home/durable-execution)
- **Inngest:** [flow control](https://www.inngest.com/docs/guides/flow-control), [cancel on events](https://www.inngest.com/docs/features/inngest-functions/cancellation/cancel-on-events), [wait for event](https://www.inngest.com/docs/reference/functions/step-wait-for-event), [idempotency](https://www.inngest.com/docs/guides/handling-idempotency)
- **Restate:** [durable building blocks](https://docs.restate.dev/concepts/durable_building_blocks)
- **DBOS:** [queues](https://docs.dbos.dev/typescript/tutorials/queue-tutorial), [workflow management](https://docs.dbos.dev/typescript/tutorials/workflow-management)
- **Serverless Workflow / Open Workflow DSL:** [DSL reference](https://github.com/serverlessworkflow/specification/blob/main/dsl-reference.md)
- **Dagster and Flyte:** [Dagster sensors](https://dagster.io/docs/guides/automate/sensors), [Flyte map tasks](https://www.union.ai/docs/v2/flyte/user-guide/tasks/task-programming/map.md) (not re-verified)

## Provenance and confidence

- **Observed:** code/schema behavior and published primary-source descriptions above.
- **Proposed:** engine implementation, PostgreSQL schema, scheduling/fairness choices, reliability targets, extensions and milestone sequencing.
- **Unverified:** production topology, achieved throughput, restore capability, actual OpenShift version, complete inventory of direct Temporal clients, and object-storage provider currently in use.
- **Not performed:** live cluster access, runtime implementation, failure/load/security tests, Temporal removal or changes to Falcone core/serverless repositories.

Before reusing upstream implementation code, record exact commit, component license and notices. The design and backlog here are original planning material; no upstream engine code is vendored.

