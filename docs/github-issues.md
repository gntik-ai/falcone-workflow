# Published GitHub backlog

48 issues are published: 12 epics and 36 stories. The 30 October 2026 revision adds 11 stories, marked "(unpublished)" below; they have no GitHub issue yet and are created by the next import, after which their links replace the marker. The revised backlog has 12 epics, 47 stories and 98 functional requirements.

The same revision changes the body (and for INT-02 the title) of published issues; [backlog.json](backlog.json) holds the intended text. Regenerating the documents does not modify GitHub issues: the publisher applies those edits separately.

Parent and dependency relationships use Markdown links and epic checklists. Native GitHub sub-issue relationships, blocked-by relationships and Project board membership are not configured; the available connector does not expose those mutations.

## EP-CON — Falcone contracts and developer experience

Epic: [#1](https://github.com/gntik-ai/falcone-workflow/issues/1)

- [CON-01 — Inventory and freeze the Falcone workflow contracts](https://github.com/gntik-ai/falcone-workflow/issues/13)
- [CON-02 — Implement the Falcone facade and backend routing](https://github.com/gntik-ai/falcone-workflow/issues/14)
- [CON-03 — Provide CLI and console integration contracts](https://github.com/gntik-ai/falcone-workflow/issues/15)
- CON-04 — Add test mode with mocked outputs and simulated time (unpublished)

## EP-DSL — DSL interpretation and versioning

Epic: [#2](https://github.com/gntik-ai/falcone-workflow/issues/2)

- [DSL-01 — Qualify and compile the existing Falcone DSL](https://github.com/gntik-ai/falcone-workflow/issues/16)
- [DSL-02 — Implement bounded expressions and graph semantics](https://github.com/gntik-ai/falcone-workflow/issues/17)
- [DSL-03 — Pin definitions, children and interpreter semantics](https://github.com/gntik-ai/falcone-workflow/issues/18)
- DSL-04 — Add error boundaries and failure handlers (unpublished)
- DSL-05 — Add dynamic fan-out over runtime collections (unpublished)
- DSL-06 — Migrate in-flight runs between flow versions (unpublished)

## EP-DUR — Durable state and recovery

Epic: [#3](https://github.com/gntik-ai/falcone-workflow/issues/3)

- [DUR-01 — Implement the transactional run state machine](https://github.com/gntik-ai/falcone-workflow/issues/19)
- [DUR-02 — Add task leases, fencing and recovery scans](https://github.com/gntik-ai/falcone-workflow/issues/20)
- [DUR-03 — Bound history and verify disaster recovery](https://github.com/gntik-ai/falcone-workflow/issues/21)

## EP-ACT — Task execution and long-running work

Epic: [#4](https://github.com/gntik-ai/falcone-workflow/issues/4)

- [ACT-01 — Define the native activity worker protocol](https://github.com/gntik-ai/falcone-workflow/issues/22)
- [ACT-02 — Implement retries, deadlines and side-effect safety](https://github.com/gntik-ai/falcone-workflow/issues/23)
- [ACT-03 — Support asynchronous jobs and checkpoints](https://github.com/gntik-ai/falcone-workflow/issues/24)

## EP-TIM — Timers and schedules

Epic: [#5](https://github.com/gntik-ai/falcone-workflow/issues/5)

- [TIM-01 — Implement durable timers and race resolution](https://github.com/gntik-ai/falcone-workflow/issues/25)
- [TIM-02 — Replace flow schedules with compatible controls](https://github.com/gntik-ai/falcone-workflow/issues/26)
- [TIM-03 — Coordinate schedule cutover and backfill](https://github.com/gntik-ai/falcone-workflow/issues/27)

## EP-EVT — Events and trigger delivery

Epic: [#6](https://github.com/gntik-ai/falcone-workflow/issues/6)

- [EVT-01 — Add inbox and outbox integration](https://github.com/gntik-ai/falcone-workflow/issues/28)
- [EVT-02 — Preserve webhook and platform-event triggers](https://github.com/gntik-ai/falcone-workflow/issues/29)
- [EVT-03 — Implement correlated signals and event waits](https://github.com/gntik-ai/falcone-workflow/issues/30)
- EVT-04 — Add callback-token and event-or-timeout waits (unpublished)
- EVT-05 — Publish lifecycle events and add trigger filters (unpublished)

## EP-HUM — Human approvals and compensation

Epic: [#7](https://github.com/gntik-ai/falcone-workflow/issues/7)

- [HUM-01 — Preserve human approval behavior](https://github.com/gntik-ai/falcone-workflow/issues/31)
- [HUM-02 — Add versioned saga compensation](https://github.com/gntik-ai/falcone-workflow/issues/32)
- [HUM-03 — Provide audited operator repair actions](https://github.com/gntik-ai/falcone-workflow/issues/33)
- HUM-04 — Add human-task forms, quorum and escalation (unpublished)

## EP-TEN — Security, tenancy and Falcone quotas

Epic: [#8](https://github.com/gntik-ai/falcone-workflow/issues/8)

- [TEN-01 — Preserve tenant and workspace authorization](https://github.com/gntik-ai/falcone-workflow/issues/34)
- [TEN-02 — Replace Temporal-bound credentials safely](https://github.com/gntik-ai/falcone-workflow/issues/35)
- [TEN-03 — Implement fair admission and quota accounting](https://github.com/gntik-ai/falcone-workflow/issues/36)
- TEN-04 — Add flow concurrency, rate limits and priority (unpublished)

## EP-INT — Falcone services and serverless integration

Epic: [#9](https://github.com/gntik-ai/falcone-workflow/issues/9)

- [INT-01 — Port the existing first-party task catalog](https://github.com/gntik-ai/falcone-workflow/issues/37)
- [INT-02 — Consume the falcone-serverless execution and checkpoint contracts](https://github.com/gntik-ai/falcone-workflow/issues/38)
- [INT-03 — Preserve asynchronous batch and object-storage behavior](https://github.com/gntik-ai/falcone-workflow/issues/39)

## EP-OBS — Monitoring, audit and performance

Epic: [#10](https://github.com/gntik-ai/falcone-workflow/issues/10)

- [OBS-01 — Implement run history and resumable SSE](https://github.com/gntik-ai/falcone-workflow/issues/40)
- [OBS-02 — Add operational metrics and tracing](https://github.com/gntik-ai/falcone-workflow/issues/41)
- [OBS-03 — Qualify performance and reliability targets](https://github.com/gntik-ai/falcone-workflow/issues/42)
- OBS-04 — Add SLA and deadline alerts (unpublished)
- OBS-05 — Add run search, labels and search attributes (unpublished)

## EP-OPS — Deployment, CI/CD and operations

Epic: [#11](https://github.com/gntik-ai/falcone-workflow/issues/11)

- [OPS-01 — Package restricted Kubernetes and OpenShift deployment](https://github.com/gntik-ai/falcone-workflow/issues/43)
- [OPS-02 — Implement upgrade, backup and recovery runbooks](https://github.com/gntik-ai/falcone-workflow/issues/44)
- [OPS-03 — Establish CI, security qualification and ownership](https://github.com/gntik-ai/falcone-workflow/issues/45)
- OPS-04 — Provide bulk run operations and operator tooling (unpublished)

## EP-MIG — Temporal migration and retirement

Epic: [#12](https://github.com/gntik-ai/falcone-workflow/issues/12)

- [MIG-01 — Build a migration inventory and differential harness](https://github.com/gntik-ai/falcone-workflow/issues/46)
- [MIG-02 — Implement staged routing and in-flight drainage](https://github.com/gntik-ai/falcone-workflow/issues/47)
- [MIG-03 — Qualify retirement and synchronize Falcone documentation](https://github.com/gntik-ai/falcone-workflow/issues/48)

