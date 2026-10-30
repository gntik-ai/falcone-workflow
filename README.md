# falcone-workflow

Custom durable workflow orchestration for Falcone, intended to replace its Temporal integration.

**Status: architecture direction accepted on 30 October 2026 ([ADR 0001](docs/adr/0001-native-falcone-workflow.md)); no runtime is implemented or production-qualified.** Remaining product questions are listed in [open questions](docs/open-questions.md).

The service owns durable workflow state, scheduling and orchestration: the engine, evaluator, scheduler/timer/lease services and trusted task workers. Falcone owns the workflow facade, backend routing, console, CLI, identity, workspace policy, quotas and admission; `falcone-charts` owns the Helm chart. `falcone-serverless` owns qualified untrusted computation and the execution and checkpoint contracts this service consumes.

## Start here

- [Combined design document](docs/falcone-workflow-design.md) (generated; read by Hermes backlog decomposition)
- [Design overview and operator decisions](docs/design.md)
- [Reference engines and comparative analysis](docs/survey.md)
- [98 functional requirements](docs/requirements.md)
- [Architecture and durability semantics](docs/architecture.md)
- [12 epics and 47 stories](docs/backlog.md)
- [Published GitHub issue index](docs/github-issues.md)
- [Migration and qualification](docs/migration.md)
- [Decisions and open questions](docs/open-questions.md)
- [Trade-offs and alternative paths](docs/tradeoffs.md)
- [Evidence and sources](docs/sources.md)

The accepted direction is a native Falcone DSL interpreter in TypeScript with transactional state in its own database on the shared PostgreSQL cluster, leased task dispatch, durable timers, the shared Falcone inbox/outbox and lease/fencing module and existing Falcone service adapters. It does not provide raw Temporal SDK compatibility or exactly-once arbitrary external effects.

## Planning sources

`docs/planning-source.json` is the structured source for requirements and issue payloads. Run `python3 tools/build_docs.py` to regenerate `requirements.md`, `backlog.md`, `backlog.json` and the combined `falcone-workflow-design.md`, which embeds the hand-written chapters. The generator validates unique issue and requirement IDs, complete requirement coverage, dependency cycles, the issue index in `github-issues.md` and the design-document structure. Regeneration does not modify GitHub issues.

No upstream implementation has been copied. The project is MIT licensed, like Falcone ([LICENSE](LICENSE)); reuse of third-party code needs review.

## Build

```sh
pnpm install --frozen-lockfile
pnpm typecheck
pnpm test
```

See [AGENTS.md](AGENTS.md) for the operator decisions, repository split and testing rules.

