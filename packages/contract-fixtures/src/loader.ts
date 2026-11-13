import { INSPECTED_FALCONE_COMMIT, validateMatrix, type CompatibilityMatrix, type MatrixEntry } from "./matrix-schema.js";
export * from "./matrix-schema.js";
export { assertRedacted } from "./redaction.js";

// CON-01.t2–t8 populate this matrix; no observed behaviors are claimed here.
export const MATRIX_VERSION = "1";
const matrices: unknown[] = [{
  schemaVersion: 1, matrixVersion: MATRIX_VERSION,
  inspectedFalconeCommit: INSPECTED_FALCONE_COMMIT, deployedBaseline: null, entries: []
}];

export function createLoader(input: readonly unknown[]) {
  const versions = new Map<string, CompatibilityMatrix>();
  for (const value of input) {
    const matrix = validateMatrix(value);
    if (versions.has(matrix.matrixVersion)) throw new Error("Duplicate matrix version");
    versions.set(matrix.matrixVersion, matrix);
  }
  return {
    loadMatrix(version: string): CompatibilityMatrix {
      const matrix = versions.get(version);
      if (!matrix) throw new Error("Unknown matrix version");
      return structuredClone(matrix);
    },
    loadFixture(id: string, version: string): MatrixEntry {
      const entry = this.loadMatrix(version).entries.find(entry => entry.id === id);
      if (!entry) throw new Error("Unknown fixture id");
      return entry;
    }
  };
}
const loader = createLoader(matrices);
export const loadMatrix = loader.loadMatrix.bind(loader);
export const loadFixture = loader.loadFixture.bind(loader);
