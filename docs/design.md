# falcone-workflow design proposal

Date: 22 October 2026. Source baseline inspected: Falcone commit `47674add95223e6ccd7f6f0dcd11106469a0a30e`. This is a repository snapshot, not a verified deployed version.

## Purpose and scope

Build a first-party Falcone service that replaces the Temporal engine behind Falcone workflows while retaining Falcone's APIs, DSL, console, identity, tenancy and service integrations. This is not a proposal to install a different generic workflow platform.

The user confirmed the project and repository. The three scope questions about raw Temporal compatibility, authoring modes and long-lived workflows were not explicitly answered. The plan therefore uses provisional defaults and marks them in [open questions](open-questions.md). Existing code already establishes visual-DSL, external-call and human-approval requirements. Optional compensation and repair extensions must remain versioned.

## Six-part specification

1. [Survey and comparative analysis](survey.md): Temporal, Cadence, Conductor OSS, Apache Airflow, Dapr Workflow, DBOS and an explicitly source-available Restate reference.
2. [Functional requirements](requirements.md): 72 testable statements in 12 categories.
3. [Baseline architecture](architecture.md): component diagram, stack, transaction semantics, data flow, capacity targets and responsibilities.
4. [Detailed backlog](backlog.md): 12 epics, 36 stories, acceptance criteria, dependencies and rough effort; [JSON import payloads](backlog.json).
5. [Open questions](open-questions.md): decisions required before implementation/cutover.
6. [Trade-offs](tradeoffs.md): implementation alternatives and phased delivery.

## Recommended boundary

Retain the current Falcone DSL and develop an explicit durable state machine for its nodes. Run only trusted interpreter and connector code in engine processes. Tenant expressions receive strict limits; arbitrary tenant code belongs in qualified falcone-serverless execution profiles. Waiting workflows occupy persisted records, not dedicated pods or permanently blocked worker threads.

Use Falcone PostgreSQL as the initial authoritative store with a dedicated schema and operational resource budget. Use existing Kafka for event transport, not as a second authoritative workflow log. Large payloads remain behind Falcone's S3 abstraction. Keep identity through Keycloak/Falcone and credential references through the existing secret-management boundary.

## Evidence-driven scope

The inspected interpreter supports sequence, parallel, task, branch, wait, approval and sub-flow. It pins definitions and uses Temporal activities, timers, signals and child workflows. The facade owns definition versions, execution lifecycle and role checks. Flow cron scheduling is separate from Falcone's standalone scheduling-engine. Monitoring translates Temporal history to SSE.

The task catalog includes database, storage, functions, events, HTTP, email, LLM completion/batch and large-task execution. Those are replacement requirements, not greenfield feature suggestions. Source comments and historical READMEs sometimes describe early stubs; the implementation and contract fixtures must take precedence. In particular the dispatch catalog retains an echo fallback for harness/legacy paths; the new production worker must reject unknown task types.

## Delivery gates

- **M0 — scope and feasibility:** inventory actual deployments, preserve DSL fixtures, settle engine language and shared serverless protocol, validate restricted deployment constraints.
- **M1 — durable core:** transactional state, leases/fencing, timers, bounded evaluator, authentication and native worker context. Crash/concurrency tests are mandatory.
- **M2 — Falcone completeness:** port task catalog, triggers, schedules, approvals, quotas, SSE and optional compensation.
- **M3 — qualification and migration:** restore/load/soak tests, differential semantics, canary cohorts, schedule transfer, long-lived run drainage, then retirement.

Do not remove Temporal merely because M1 demonstrations succeed. Some deployed workflows may remain on the old engine for their full lifetime.

