import assert from "node:assert/strict";
import { test } from "node:test";
import { createLoader, validateMatrix, INSPECTED_FALCONE_COMMIT, loadMatrix, MATRIX_VERSION, type CompatibilityMatrix } from "../src/loader.js";

function sample(): CompatibilityMatrix {
  return { schemaVersion: 1, matrixVersion: "test-only", inspectedFalconeCommit: INSPECTED_FALCONE_COMMIT,
    deployedBaseline: null, entries: [{ id: "synthetic", area: "route", classification: "preserved",
      evidence: { kind: "repository", commit: INSPECTED_FALCONE_COMMIT, path: "test/synthetic" },
      fixture: { tenantId: "<redacted:tenant>", workspace_id: "<redacted:workspace>", runId: "<redacted:run>", payload: "<redacted:payload>" } }] };
}
test("all shipped matrices validate; inspected pin matches documented source", async () => {
  const { readFile } = await import("node:fs/promises");
  const source = await readFile(new URL("../../../../docs/sources.md", import.meta.url), "utf8");
  assert.ok(source.includes(`Pinned inspected commit: [${INSPECTED_FALCONE_COMMIT}]`));
  assert.deepEqual(validateMatrix(loadMatrix(MATRIX_VERSION)).entries, []);
});
test("TypeScript loader selects id and version and isolates consumer mutations", () => {
  const matrix = sample();
  const loader = createLoader([matrix, { ...sample(), matrixVersion: "other" }]);
  const entry = loader.loadFixture("synthetic", "test-only");
  assert.equal(entry.id, "synthetic");
  entry.id = "changed";
  matrix.entries.length = 0;
  assert.equal(loader.loadFixture("synthetic", "test-only").id, "synthetic");
  assert.throws(() => loader.loadFixture("missing", "test-only"));
  assert.throws(() => loader.loadFixture("synthetic", "missing"));
  assert.throws(() => createLoader([sample(), sample()]));
});
test("classification is singular and blockers require nonempty owner and resolution", () => {
  for (const classification of [undefined, [], ["preserved", "migration blocker"], "unknown"]) {
    const matrix = sample();
    Object.assign(matrix.entries[0]!, { classification });
    assert.throws(() => validateMatrix(matrix));
  }
  for (const metadata of [{}, { owner: "team" }, { owner: "team", resolution: " " }]) {
    const matrix = sample();
    Object.assign(matrix.entries[0]!, { classification: "migration blocker", ...metadata });
    assert.throws(() => validateMatrix(matrix));
  }
  const matrix = sample();
  Object.assign(matrix.entries[0]!, { classification: "migration blocker", owner: "team", resolution: "Track resolution in issue" });
  assert.doesNotThrow(() => validateMatrix(matrix));
  matrix.entries[0]!.classification = "intentionally versioned";
  assert.throws(() => validateMatrix(matrix)); // blocker metadata cannot hide under another classification
});
test("evidence distinguishes inspected code from deployed observations", () => {
  const matrix = sample();
  matrix.entries[0]!.evidence = { kind: "deployed observation", baseline: "image@sha256:synthetic", observation: "Synthetic read-only check", readOnly: true };
  assert.throws(() => validateMatrix(matrix));
  matrix.deployedBaseline = "image@sha256:synthetic";
  assert.doesNotThrow(() => validateMatrix(matrix));
  Object.assign(matrix.entries[0]!.evidence, { readOnly: false });
  assert.throws(() => validateMatrix(matrix));
});
test("schema rejects unknown fields, areas, duplicate ids, and versions", () => {
  for (const change of [{ schemaVersion: 2 }, { unexpected: true }]) assert.throws(() => validateMatrix({ ...sample(), ...change }));
  const matrix = sample();
  matrix.entries.push(matrix.entries[0]!);
  assert.throws(() => validateMatrix(matrix));
  const badArea = sample(); Object.assign(badArea.entries[0]!, { area: "unknown" });
  assert.throws(() => validateMatrix(badArea));
});
test("loader rejects unredacted identities, credentials, bearer strings and payloads", () => {
  const unsafe = [
    { tenantId: "customer-example" }, { workspace_id: "customer-example" }, { run_id: "actual-run" },
    { nested: [{ access_token: "synthetic-sensitive-value" }] },
    { message: ["Bearer", "synthetic-value"].join(" ") },
    { payload: { email: "person@example.invalid" } }, { password: "synthetic-sensitive-value" }
  ];
  for (const fixture of unsafe) {
    const matrix = sample(); matrix.entries[0]!.fixture = fixture;
    assert.throws(() => createLoader([matrix]), /redaction|placeholder/);
  }
});
