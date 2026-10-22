# Migration and qualification plan

## Replace behavior, not just imports

The native service is not a drop-in Temporal server. Preserve Falcone's inventoried product interfaces; rewrite the internal Temporal client, workflow and activity integration. Raw Temporal APIs, SDK workflows, encoded histories and Temporal Web compatibility are provisionally outside scope until CON-01 confirms actual callers.

### Boundary mapping

| Current boundary | Native replacement | Evidence required |
|---|---|---|
| DslInterpreterWorkflow + SDK timers/signals/children | Persisted graph continuation and transition evaluator | DSL and race fixtures, version-pinning proof |
| flow-executor Temporal gateway | WorkflowBackend facade and backend locator | Routes, error envelopes, IDs, tenancy and idempotency fixtures |
| flow-trigger-registry schedules | Native schedules with ownership epochs | Pause/resume/trigger, overlap/catch-up and cutover tests |
| Temporal Activity Context/errors | Engine-neutral ActivityContext | Retry, heartbeat, cancellation and ancestry tests |
| execution-token-ref ancestry queries | Native root/parent/attempt lineage | Forged lineage, foreign workspace and revocation tests |
| History-to-SSE mapping | Native durable event projection | Frame shape/order, node occurrence mapping, cursor resume |
| llm.batch staged execution | Persisted job and phase state | Submit ambiguity, polling, cancellation and credential expiry |
| largeTask.run Temporal heartbeats | Authorized job adapter / qualified serverless protocol | Legacy profile support and checkpoint/cleanup behavior |

## Rollout

1. Inventory deployed definitions, open runs, cron schedules, patches, task versions, credentials, quotas and all direct Temporal callers. Record source/image versions separately from inspected repository source.
2. Introduce the backend interface and persist backend ownership for runs and trigger registrations. Preserve old IDs and routing; do not infer backend from an untrusted ID format.
3. Run isolated differential fixtures. Compare meaningful business state and errors, allowing only declared timing/order differences. Never shadow-execute real email, billing, database writes or provider submissions.
4. Canary new runs for a selected tenant/flow cohort. Existing Temporal runs and their pinned workers remain on Temporal. Rollback affects future starts, not ownership of existing native runs.
5. Transfer schedules and event/webhook admission with a durable ownership epoch. Pause old admission, reconcile already admitted events/occurrences and enable the new owner. Outages during the gap use explicit bounded catch-up.
6. Drain or explicitly resolve long-lived legacy runs. Transfer only application-level checkpoints supported by both engines, with deduplicated effects and a recorded cutover boundary. Do not attempt generic Temporal-history conversion.
7. Complete capacity, isolation, backup and failover qualification. Remove the old dependency only when remaining caller/run/schedule inventories are empty or have approved retention exceptions.

No change in this repository authorizes deleting an existing Temporal deployment. Runtime cutover is a later release action with environment-specific evidence.

## Required failure matrix

| Injection point | Expected result |
|---|---|
| Before start commit | No accepted run; safe client retry |
| After start commit, before reply | Same idempotency key returns the same run |
| After task lease, before work | Lease expiry permits recovery |
| After external effect, before completion | Downstream deduplication or explicit reconciliation |
| Late completion after lease reassignment | Old generation rejected |
| Transition commit before outbox publish | Relay eventually publishes |
| Publish before outbox acknowledgement | Duplicate event tolerated by inbox |
| Approval and timeout and cancellation race | One recorded winner; no fabricated timeout on cancellation |
| DB partition/failover | No uncommitted dispatch; fenced ownership on recovery |
| Object upload before DB reference | Orphan sweep; no false referenced payload |
| Mixed engine versions | Pinned interpreter honored or run safely parked |
| Backup restored after outside effects occurred | Reconciliation before resuming ambiguous actions |

Tests must exercise real PostgreSQL transactions and concurrent processes. Mock-only tests are insufficient for durability claims. No such runtime tests were performed for this planning-only publication.

## Cross-repository work

The existing falcone-serverless proposal names Temporal as workflow owner. INT-02 defines the replacement handshake; MIG-03 tracks updates to Falcone core, charts and serverless docs. Do not introduce a circular design in which workflow needs serverless to advance state while serverless needs workflow just to start an execution. A local/mock adapter is acceptable for development but not evidence of production integration.

