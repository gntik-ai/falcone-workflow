# Contract fixtures

Shared contract `ctr-contract-fixtures` for engine TypeScript and facade Node ESM tests.
Run `pnpm build` before importing `@falcone-workflow/contract-fixtures`.
Consumers explicitly pin `loadFixture(id, matrixVersion)` or `loadMatrix(matrixVersion)`.
Unknown ids and versions throw. Returned values are independent copies.

Schema version 1 is defined and validated by `src/matrix-schema.ts`. Matrix version
`1` is deliberately empty: CON-01.t2–t8 will add observed behavior. Synthetic test
entries are never shipped as evidence. `createLoader(matrices)` validates externally
supplied versioned copies with the same schema and redaction rules.

Each entry contains an id, area, evidence, exactly one classification and a JSON
fixture. Migration blockers require nonempty owner and resolution strings.
Repository evidence must use the inspected Falcone commit recorded in
`docs/sources.md` and a repository-relative path. Deployment evidence instead
requires a read-only observation and a separate deployed image or source baseline;
null means no deployed baseline has been established.

Identity fields (`tenant`, `workspace`, `run`, with optional `Id`/`_id` suffix),
credential fields, and strings anywhere beneath payload/body fields must contain
only `<redacted:name>` placeholders, including nested arrays. Never capture real
secrets even temporarily. Bearer strings, recognizable key and JWT formats are
rejected everywhere. Use structured synthetic expectations outside payload/body
fields for public contract literals. Automated checks are conservative guards;
review fixture additions for identifying data in free text and unusual field names.
Validation errors never echo rejected values.

Build and tests reuse the existing engine package's installed TypeScript toolchain;
no additional dependencies are required. The package's compiled ESM and declarations
are self-contained and need no runtime dependencies.
