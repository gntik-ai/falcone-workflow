import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createLoader, loadMatrix, MATRIX_VERSION, INSPECTED_FALCONE_COMMIT } from '@falcone-workflow/contract-fixtures';

test('plain Node ESM imports the package and loads a versioned fixture', () => {
  const matrix = loadMatrix(MATRIX_VERSION);
  matrix.matrixVersion = 'synthetic-only';
  matrix.entries.push({ id: 'node-consumer', area: 'DSL', classification: 'preserved',
    evidence: { kind: 'repository', commit: INSPECTED_FALCONE_COMMIT, path: 'test/synthetic' },
    fixture: { tenant: '<redacted:tenant>' } });
  const loader = createLoader([matrix]);
  assert.deepEqual(loader.loadFixture('node-consumer', 'synthetic-only').fixture, { tenant: '<redacted:tenant>' });
  assert.throws(() => loader.loadFixture('node-consumer', MATRIX_VERSION));
});
