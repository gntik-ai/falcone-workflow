import assert from "node:assert/strict";
import { test } from "node:test";
import { ENGINE_NAME } from "./index.js";

test("exports the engine name", () => {
  assert.equal(ENGINE_NAME, "falcone-workflow");
});
