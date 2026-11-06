#!/usr/bin/env node
/* ------------------------------------------------------------- CHECK ------- */
/* Cross-platform wrapper for the regression suite.
 *
 * Why this exists: the suite is two steps --
 *   1. extract the inline game/Matter blocks out of www/index.html
 *      (a Python job, scripts/extract.py), then
 *   2. run the headless harness (tests/harness.js).
 * CI runs `python3` happily, but Windows names the interpreter `python`
 * (the `python3` alias is a Microsoft Store stub that fails the suite with
 * "Python was not found"). Instead of pinning one name into npm, this launcher
 * probes python3, python, and py -3, then uses whichever exists locally --
 * so the SAME `npm run check` works on the GitHub runner and the dev laptop.
 */
'use strict';

const { spawnSync } = require('child_process');
const path = require('path');

const root = path.join(__dirname, '..');

function probe(cmd, args) {
  const r = spawnSync(cmd, args.concat(['--version']), { stdio: 'ignore' });
  return r.status === 0;
}

function pickPython() {
  const candidates = [
    ['python3', []],
    ['python', []],
    ['py', ['-3']],
  ];
  for (const [cmd, args] of candidates) {
    try { if (probe(cmd, args)) return [cmd, args]; } catch (_) { /* keep probing */ }
  }
  return null;
}

const py = pickPython();
if (!py) {
  process.stderr.write(
    'check: no Python found (tried python3, python, py -3).\n' +
    'Install Python 3, then re-run `npm run check`.\n');
  process.exit(1);
}

/* `--extract-only`: stop after step 1 (this backs the `npm run extract` alias). */
const extractOnly = process.argv.includes('--extract-only');

/* Step 1: re-extract the generated test copies from the runtime source. */
const [pyCmd, pyArgs] = py;
const ex = spawnSync(pyCmd, pyArgs.concat(['scripts/extract.py']), {
  cwd: root, stdio: 'inherit',
});
/* spawnSync on failure may give null status + a signal instead of an exit code. */
if (ex.error || ((ex.status === null ? ex.signal !== null : ex.status !== 0))) {
  process.stderr.write('check: extract step failed\n');
  process.exit(ex.status === null ? 1 : ex.status);
}
if (extractOnly) process.exit(0);

/* Step 2: run the headless harness -- everything after this point is Node. */
const run = spawnSync('node', ['tests/harness.js'], { cwd: root, stdio: 'inherit' });
process.exit(run.status === null ? (run.signal ? 1 : run.status) : run.status);
