import { assertRedacted } from "./redaction.js";

export const INSPECTED_FALCONE_COMMIT = "47674add95223e6ccd7f6f0dcd11106469a0a30e";
export const MATRIX_SCHEMA_VERSION = 1;
export type Area = "route" | "DSL" | "error" | "role" | "schedule" | "monitoring" | "task envelope";
export type Evidence =
  | { kind: "repository"; commit: string; path: string }
  | { kind: "deployed observation"; baseline: string; observation: string; readOnly: true };
export type Classification =
  | { classification: "preserved" | "intentionally versioned" }
  | { classification: "migration blocker"; owner: string; resolution: string };
export type Json = null | boolean | number | string | Json[] | { [key: string]: Json };
export type MatrixEntry = { id: string; area: Area; evidence: Evidence; fixture: Json } & Classification;
export interface CompatibilityMatrix {
  schemaVersion: 1;
  matrixVersion: string;
  inspectedFalconeCommit: string;
  deployedBaseline: string | null;
  entries: MatrixEntry[];
}

function object(value: unknown): Record<string, unknown> {
  if (value === null || typeof value !== "object" || Array.isArray(value)) throw new Error("Expected schema object");
  return value as Record<string, unknown>;
}
function fields(value: Record<string, unknown>, required: string[]): void {
  if (Object.keys(value).length !== required.length || required.some(key => !Object.hasOwn(value, key))) {
    throw new Error("Unexpected or missing schema field");
  }
}
function nonempty(value: unknown): asserts value is string {
  if (typeof value !== "string" || !value.trim()) throw new Error("Expected nonempty string");
}
function json(value: unknown): void {
  if (value === null || typeof value === "string" || typeof value === "boolean") return;
  if (typeof value === "number" && Number.isFinite(value)) return;
  if (Array.isArray(value)) { value.forEach(json); return; }
  for (const child of Object.values(object(value))) json(child);
}
/** Strict runtime schema, shared by Node and TypeScript consumers. */
export function validateMatrix(value: unknown): CompatibilityMatrix {
  const matrix = object(value);
  fields(matrix, ["schemaVersion", "matrixVersion", "inspectedFalconeCommit", "deployedBaseline", "entries"]);
  if (matrix.schemaVersion !== MATRIX_SCHEMA_VERSION) throw new Error("Unsupported schema version");
  nonempty(matrix.matrixVersion);
  if (matrix.inspectedFalconeCommit !== INSPECTED_FALCONE_COMMIT) throw new Error("Unexpected inspected Falcone commit");
  if (matrix.deployedBaseline !== null) nonempty(matrix.deployedBaseline);
  if (!Array.isArray(matrix.entries)) throw new Error("Expected entries array");
  const ids = new Set<string>();
  for (const value of matrix.entries) {
    const entry = object(value);
    const blocker = entry.classification === "migration blocker";
    fields(entry, ["id", "area", "evidence", "fixture", "classification", ...(blocker ? ["owner", "resolution"] : [])]);
    nonempty(entry.id);
    if (ids.has(entry.id)) throw new Error("Duplicate entry id");
    ids.add(entry.id);
    if (!["route", "DSL", "error", "role", "schedule", "monitoring", "task envelope"].includes(entry.area as string)) throw new Error("Invalid area");
    if (!["preserved", "intentionally versioned", "migration blocker"].includes(entry.classification as string)) throw new Error("Invalid classification");
    if (blocker) { nonempty(entry.owner); nonempty(entry.resolution); }
    const evidence = object(entry.evidence);
    if (evidence.kind === "repository") {
      fields(evidence, ["kind", "commit", "path"]);
      if (evidence.commit !== matrix.inspectedFalconeCommit) throw new Error("Repository evidence must use inspected commit");
      nonempty(evidence.path);
      if (evidence.path.startsWith("/") || evidence.path.split("/").includes("..")) throw new Error("Expected repository-relative path");
    } else if (evidence.kind === "deployed observation") {
      fields(evidence, ["kind", "baseline", "observation", "readOnly"]);
      nonempty(evidence.baseline); nonempty(evidence.observation);
      if (evidence.readOnly !== true || evidence.baseline !== matrix.deployedBaseline) throw new Error("Deployed evidence requires its own baseline and read-only observation");
    } else throw new Error("Invalid evidence kind");
    json(entry.fixture);
  }
  assertRedacted(matrix);
  return structuredClone(matrix) as unknown as CompatibilityMatrix;
}
