# falcone-workflow

Custom durable workflow orchestration for Falcone, intended to replace its Temporal integration.

**Status: proposed design and implementation backlog; no runtime is implemented or production-qualified.** Repository publication is authorized. Compatibility scope and proposed extensions still need product confirmation.

The service owns durable workflow state, scheduling and orchestration. Falcone owns identity, workspace policy, quotas, interfaces and product experience. `falcone-serverless` owns qualified untrusted computation.

## Start here

- [Design overview](docs/design.md)
- [Reference engines and comparative analysis](docs/survey.md)
- [72 functional requirements](docs/requirements.md)
- [Architecture and durability semantics](docs/architecture.md)
- [12 epics and 36 stories](docs/backlog.md)
- [Published GitHub issue index](docs/github-issues.md)
- [Migration and qualification](docs/migration.md)
- [Open questions and provisional decisions](docs/open-questions.md)
- [Trade-offs and alternative paths](docs/tradeoffs.md)
- [Evidence and sources](docs/sources.md)

The initial recommendation is a native Falcone DSL interpreter with transactional PostgreSQL state, leased task dispatch, durable timers, inbox/outbox integration and existing Falcone service adapters. It does not promise raw Temporal SDK compatibility or exactly-once arbitrary external effects.

## Planning sources

`docs/planning-source.json` is the structured source for requirements and issue payloads. Run `python3 tools/build_docs.py` to regenerate `requirements.md`, `backlog.md` and `backlog.json`. The generator validates unique issue IDs, complete requirement coverage and dependency cycles. Regeneration does not modify GitHub issues.

No upstream implementation has been copied. The project is MIT licensed, like Falcone ([LICENSE](LICENSE)); reuse of third-party code needs review.

## Build

```sh
pnpm install --frozen-lockfile
pnpm typecheck
pnpm test
```

See [AGENTS.md](AGENTS.md) for the operator decisions, repository split and testing rules.

