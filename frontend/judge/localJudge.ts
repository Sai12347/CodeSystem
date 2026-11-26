/**
 * Local code judge for the Vite dev/preview server.
 *
 * The production judge lives in the Spring Boot backend (com.codesystem.judge), which needs Docker or
 * Maven plus MySQL. This plugin serves the same /api/judge/{health,run,submit} API straight from the
 * Vite server so "Run" and "Submit" work with just `npm run dev`, using the local `javac`/`java` and
 * `python` executables, the shared judge harness (backend/src/main/resources/judge) and the generated
 * problem bank (backend/src/main/resources/problems/*.json, incl. hidden tests).
 *
 * Set ALGOPLAY_JUDGE=backend to disable it and proxy /api/judge to the Spring Boot backend instead.
 */
import { spawn, spawnSync } from 'node:child_process';
import { existsSync, mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, statSync, copyFileSync, writeFileSync } from 'node:fs';
import { createHash } from 'node:crypto';
import os from 'node:os';
import path from 'node:path';
import type { IncomingMessage, ServerResponse } from 'node:http';
import type { Plugin } from 'vite';

type Json = any;

const MAX_CODE_BYTES = 65_536;
const COMPILE_TIMEOUT_MS = 30_000;
const RUN_TIMEOUT_MS = 12_000;
const PER_TEST_LIMIT_MS = 2_500;
const MAX_CONCURRENT = Math.max(1, Math.min(4, os.cpus().length - 1));
const FLOAT_TOL = 1e-5;
const JAVA_IMPORT_LINE = 'import java.util.*; import java.util.function.*; import java.util.stream.*; import java.math.*;';
const PY_PRELUDE_LINE = 'from judge_prelude import *  # noqa: F401,F403';

interface Options {
  /** Repository root (folder that contains backend/ and frontend/). */
  repoRoot: string;
}

interface ExecResult {
  code: number | null;
  timedOut: boolean;
  stdout: string;
  stderr: string;
  error?: string;
}

// ---------------------------------------------------------------------------------------------
// Process helpers
// ---------------------------------------------------------------------------------------------

function run(cmd: string, args: string[], cwd: string, timeoutMs: number, env?: Record<string, string>): Promise<ExecResult> {
  return new Promise((resolve) => {
    let stdout = '';
    let stderr = '';
    let settled = false;
    let child;
    try {
      child = spawn(cmd, args, { cwd, env: { ...process.env, ...(env || {}) }, windowsHide: true });
    } catch (e) {
      resolve({ code: null, timedOut: false, stdout: '', stderr: '', error: String(e) });
      return;
    }
    const timer = setTimeout(() => {
      if (settled) return;
      settled = true;
      child.kill('SIGKILL');
      resolve({ code: null, timedOut: true, stdout, stderr });
    }, timeoutMs);
    child.stdout.on('data', (d: Buffer) => { if (stdout.length < 16_384) stdout += d.toString('utf8'); });
    child.stderr.on('data', (d: Buffer) => { if (stderr.length < 16_384) stderr += d.toString('utf8'); });
    child.on('error', (e: Error) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ code: null, timedOut: false, stdout, stderr, error: e.message });
    });
    child.on('close', (code: number | null) => {
      if (settled) return;
      settled = true;
      clearTimeout(timer);
      resolve({ code, timedOut: false, stdout, stderr });
    });
  });
}

function commandWorks(cmd: string, args: string[], mustContain?: RegExp): boolean {
  try {
    const r = spawnSync(cmd, args, { encoding: 'utf8', timeout: 8000, windowsHide: true });
    if (r.error || r.status !== 0) return false;
    return mustContain ? mustContain.test(`${r.stdout}${r.stderr}`) : true;
  } catch {
    return false;
  }
}

class Semaphore {
  private queue: Array<() => void> = [];
  constructor(private permits: number) {}
  async acquire(): Promise<() => void> {
    if (this.permits > 0) {
      this.permits--;
    } else {
      await new Promise<void>((r) => this.queue.push(r));
    }
    return () => {
      const next = this.queue.shift();
      if (next) next();
      else this.permits++;
    };
  }
}

// ---------------------------------------------------------------------------------------------
// Output comparison (mirrors tools/problems/judgekit.py and OutputComparator.java)
// ---------------------------------------------------------------------------------------------

function normalize(v: Json): Json {
  if (v === null || typeof v === 'boolean' || typeof v === 'string') return v;
  if (typeof v === 'number') return v;
  if (Array.isArray(v)) return v.map(normalize);
  if (typeof v === 'object') {
    const out: Record<string, Json> = {};
    for (const k of Object.keys(v).sort()) out[k] = normalize(v[k]);
    return out;
  }
  return v;
}

function canonical(v: Json): string {
  return JSON.stringify(normalize(v));
}

function deepSort(v: Json): Json {
  if (!Array.isArray(v)) return v;
  return v.map(deepSort).sort((a, b) => (canonical(a) < canonical(b) ? -1 : canonical(a) > canonical(b) ? 1 : 0));
}

function topSort(v: Json): Json {
  if (!Array.isArray(v)) return v;
  return [...v].sort((a, b) => (canonical(a) < canonical(b) ? -1 : canonical(a) > canonical(b) ? 1 : 0));
}

function valuesEqual(a: Json, b: Json, tol: number | null): boolean {
  if (typeof a === 'boolean' || typeof b === 'boolean') return a === b;
  if (typeof a === 'number' && typeof b === 'number') {
    if (tol === null) return a === b;
    const diff = Math.abs(a - b);
    return diff <= tol || diff <= tol * Math.max(Math.abs(a), Math.abs(b));
  }
  if (Array.isArray(a) && Array.isArray(b)) {
    return a.length === b.length && a.every((x, i) => valuesEqual(x, b[i], tol));
  }
  if (a && b && typeof a === 'object' && typeof b === 'object' && !Array.isArray(a) && !Array.isArray(b)) {
    const ka = Object.keys(a).sort();
    const kb = Object.keys(b).sort();
    return ka.length === kb.length && ka.every((k, i) => k === kb[i] && valuesEqual(a[k], b[k], tol));
  }
  return a === b;
}

export function compareOutputs(expected: Json, actual: Json, mode = 'exact'): boolean {
  if (actual === undefined) return false;
  switch (mode || 'exact') {
    case 'exact':
      return valuesEqual(normalize(expected), normalize(actual), null);
    case 'float':
      return valuesEqual(expected, actual, FLOAT_TOL);
    case 'sorted':
      if (!Array.isArray(expected) || !Array.isArray(actual)) return valuesEqual(normalize(expected), normalize(actual), null);
      return valuesEqual(topSort(normalize(expected)), topSort(normalize(actual)), null);
    case 'sortedDeep':
      return valuesEqual(deepSort(normalize(expected)), deepSort(normalize(actual)), null);
    case 'anyOf':
      return Array.isArray(expected) && expected.some((e) => valuesEqual(normalize(e), normalize(actual), null));
    default:
      return false;
  }
}

// ---------------------------------------------------------------------------------------------
// Judge
// ---------------------------------------------------------------------------------------------

export class LocalJudge {
  private readonly problemsDir: string;
  private readonly harnessDir: string;
  private readonly cacheDir: string;
  private bank = new Map<string, Json>();
  private bankStamp = '';
  private visibleTests = 0;
  private hiddenTests = 0;
  private pythonCmd: string[] | null | undefined;
  private javaOk: boolean | undefined;
  private harnessBuild: Promise<string> | null = null;
  private harnessKey = '';
  private readonly sem = new Semaphore(MAX_CONCURRENT);

  constructor(opts: Options) {
    this.problemsDir = path.join(opts.repoRoot, 'backend', 'src', 'main', 'resources', 'problems');
    this.harnessDir = path.join(opts.repoRoot, 'backend', 'src', 'main', 'resources', 'judge');
    this.cacheDir = path.join(os.tmpdir(), 'algoplay-judge-cache');
  }

  // ---- problem bank (reloaded automatically when build.py re-emits the topic files) ----
  private loadBank(): void {
    if (!existsSync(this.problemsDir)) return;
    const files = readdirSync(this.problemsDir).filter((f) => f.endsWith('.json')).sort();
    const stamp = files.map((f) => `${f}:${statSync(path.join(this.problemsDir, f)).mtimeMs}`).join('|');
    if (stamp === this.bankStamp) return;
    const bank = new Map<string, Json>();
    let vis = 0;
    let hid = 0;
    for (const f of files) {
      try {
        const root = JSON.parse(readFileSync(path.join(this.problemsDir, f), 'utf8'));
        for (const p of root.problems || []) {
          if (!p?.id) continue;
          bank.set(p.id, p);
          for (const t of p.tests || []) (t.hidden ? hid++ : vis++);
        }
      } catch (e) {
        console.warn(`[algoplay-judge] failed to load ${f}: ${e}`);
      }
    }
    this.bank = bank;
    this.visibleTests = vis;
    this.hiddenTests = hid;
    this.bankStamp = stamp;
  }

  // ---- toolchain detection ----
  isJavaAvailable(): boolean {
    if (this.javaOk === undefined) {
      this.javaOk = commandWorks('javac', ['-version']) && commandWorks('java', ['-version']);
    }
    return this.javaOk;
  }

  resolvePython(): string[] | null {
    if (this.pythonCmd !== undefined) return this.pythonCmd;
    const configured = process.env.JUDGE_PYTHON_COMMAND;
    const candidates: string[][] = [];
    if (configured) candidates.push(configured.split(' '));
    candidates.push(['python3'], ['python'], ['py', '-3']);
    this.pythonCmd = null;
    for (const c of candidates) {
      if (commandWorks(c[0], [...c.slice(1), '--version'], /Python 3\./)) {
        this.pythonCmd = c;
        break;
      }
    }
    return this.pythonCmd;
  }

  health(): Json {
    this.loadBank();
    return {
      status: 'UP',
      engine: 'local-dev-judge',
      loadedProblems: this.bank.size,
      totalVisibleTests: this.visibleTests,
      totalHiddenTests: this.hiddenTests,
      javaAvailable: this.isJavaAvailable(),
      pythonAvailable: this.resolvePython() !== null,
    };
  }

  /** Compiles Judge/ListNode/TreeNode once per harness version; submissions then only compile their own code. */
  private ensureJavaHarness(): Promise<string> {
    const javaDir = path.join(this.harnessDir, 'java');
    const names = ['Judge.java', 'ListNode.java', 'TreeNode.java'];
    const h = createHash('sha256');
    for (const n of names) h.update(readFileSync(path.join(javaDir, n)));
    const key = h.digest('hex').slice(0, 16);
    if (this.harnessBuild && this.harnessKey === key) return this.harnessBuild;
    this.harnessKey = key;
    this.harnessBuild = (async () => {
      const outDir = path.join(this.cacheDir, `java-${key}`);
      if (existsSync(path.join(outDir, 'Judge.class'))) return outDir;
      const srcDir = mkdtempSync(path.join(os.tmpdir(), 'algoplay-harness-'));
      try {
        for (const n of names) copyFileSync(path.join(javaDir, n), path.join(srcDir, n));
        const tmpOut = path.join(srcDir, 'out');
        mkdirSync(tmpOut);
        const r = await run('javac', ['-encoding', 'UTF-8', '-nowarn', '-d', tmpOut, ...names], srcDir, 120_000);
        if (r.code !== 0) throw new Error(`Failed to compile judge harness: ${r.error || r.stderr || r.stdout}`);
        mkdirSync(outDir, { recursive: true });
        for (const f of readdirSync(tmpOut)) copyFileSync(path.join(tmpOut, f), path.join(outDir, f));
        return outDir;
      } finally {
        rmSync(srcDir, { recursive: true, force: true });
      }
    })();
    this.harnessBuild.catch(() => { this.harnessBuild = null; });
    return this.harnessBuild;
  }

  async evaluate(body: Json, visibleOnly: boolean): Promise<Json> {
    const mode = visibleOnly ? 'run' : 'submit';
    const problemId = String(body?.problemId ?? '').trim();
    const language = String(body?.language ?? '').trim().toLowerCase();
    const code = typeof body?.code === 'string' ? body.code : '';
    const fail = (status: string, msg: string) => errorResponse(problemId, language, mode, status, msg);

    if (!problemId) return fail('RUNTIME_ERROR', 'Missing problemId.');
    if (language !== 'java' && language !== 'python') return fail('RUNTIME_ERROR', `Unsupported language '${language}'. Use 'java' or 'python'.`);
    if (!code.trim()) return fail('COMPILATION_ERROR', 'Submission code is empty.');
    if (Buffer.byteLength(code, 'utf8') > MAX_CODE_BYTES) return fail('COMPILATION_ERROR', 'Submission exceeds 64 KB limit.');

    this.loadBank();
    const problem = this.bank.get(problemId);
    if (!problem) return fail('RUNTIME_ERROR', `Problem '${problemId}' not found in judge bank. Run: python tools/problems/build.py`);
    const tests: Json[] = (problem.tests || []).filter((t: Json) => !visibleOnly || !t.hidden);
    if (!tests.length) return fail('RUNTIME_ERROR', 'No test cases configured for problem.');

    if (language === 'java' && !this.isJavaAvailable()) {
      return fail('RUNTIME_ERROR', 'Java (JDK 17+ with javac) is not installed or not on PATH, so Java code cannot be compiled.');
    }
    if (language === 'python' && !this.resolvePython()) {
      return fail('RUNTIME_ERROR', 'Python 3 is not installed or not on PATH, so Python code cannot be executed.');
    }

    const release = await this.sem.acquire();
    const work = mkdtempSync(path.join(os.tmpdir(), 'algoplay-judge-'));
    try {
      const testsPath = path.join(work, 'tests.json');
      const resultsPath = path.join(work, 'results.jsonl');
      writeFileSync(testsPath, JSON.stringify({
        signature: problem.signature,
        tests: tests.map((t) => ({ id: t.id, input: t.input })),
      }), 'utf8');
      const adapter: string | null = problem.adapter ? problem.adapter[language] ?? null : null;

      let outcome: { timedOut: boolean; compileError: string | null; stderr: string };
      if (language === 'java') {
        const harness = await this.ensureJavaHarness();
        let src = code.replace(/^\s*package\s+[\w.]+\s*;\s*$/gm, '');
        src = src.replace(/^\s*public\s+(?=((final|abstract)\s+)?(class|interface|enum|record)\b)/gm, '');
        writeFileSync(path.join(work, 'Solution.java'), `${JAVA_IMPORT_LINE}\n${src}`, 'utf8');
        const sources = ['Solution.java'];
        if (adapter && adapter.trim()) {
          writeFileSync(path.join(work, 'Adapter.java'), `${JAVA_IMPORT_LINE}\n${adapter}`, 'utf8');
          sources.push('Adapter.java');
        }
        const outDir = path.join(work, 'out');
        mkdirSync(outDir);
        const c = await run('javac', ['-encoding', 'UTF-8', '-nowarn', '-cp', harness, '-d', outDir, ...sources], work, COMPILE_TIMEOUT_MS);
        if (c.timedOut) {
          outcome = { timedOut: false, compileError: `Compilation timed out after ${COMPILE_TIMEOUT_MS / 1000}s.`, stderr: '' };
        } else if (c.code !== 0) {
          outcome = { timedOut: false, compileError: truncate(sanitize(`${c.error ?? ''}${c.stdout}\n${c.stderr}`.trim(), work, true), 4000), stderr: '' };
        } else {
          const cp = [outDir, harness].join(path.delimiter);
          const r = await run('java', ['-Xss64m', '-Xmx256m', '-XX:+UseSerialGC', '-XX:TieredStopAtLevel=1', '-cp', cp, 'Judge', testsPath, resultsPath], work, RUN_TIMEOUT_MS);
          outcome = { timedOut: r.timedOut, compileError: null, stderr: truncate(sanitize(r.stderr, work), 4000) };
        }
      } else {
        const py = this.resolvePython()!;
        for (const n of ['judge_lib.py', 'judge_prelude.py', 'judge_runner.py']) {
          copyFileSync(path.join(this.harnessDir, 'python', n), path.join(work, n));
        }
        writeFileSync(path.join(work, 'solution.py'), `${PY_PRELUDE_LINE}\n${code}`, 'utf8');
        if (adapter && adapter.trim()) writeFileSync(path.join(work, 'adapter.py'), adapter, 'utf8');
        const r = await run(py[0], [...py.slice(1), 'judge_runner.py', testsPath, resultsPath], work, RUN_TIMEOUT_MS, {
          PYTHONDONTWRITEBYTECODE: '1', PYTHONIOENCODING: 'utf-8', PYTHONHASHSEED: '0',
        });
        const stderr = truncate(sanitize(`${r.error ?? ''}${r.stderr}`, work), 4000);
        const syntax = !r.timedOut && r.code !== 0 && !existsSync(resultsPath) && /SyntaxError|IndentationError/.test(stderr);
        outcome = { timedOut: r.timedOut, compileError: syntax ? formatPythonSyntaxError(stderr) : null, stderr };
      }

      if (outcome.compileError !== null) {
        return {
          problemId, language, mode, status: 'COMPILATION_ERROR',
          passedCount: 0, totalCount: tests.length,
          visiblePassed: 0, visibleTotal: tests.filter((t) => !t.hidden).length,
          hiddenPassed: 0, hiddenTotal: tests.filter((t) => t.hidden).length,
          executionTimeMs: 0, compileError: outcome.compileError, error: null, results: [],
        };
      }
      return buildVerdict(problem, problemId, language, mode, tests, readResults(resultsPath), outcome);
    } catch (e) {
      return fail('RUNTIME_ERROR', `Internal judge error: ${e instanceof Error ? e.message : String(e)}`);
    } finally {
      release();
      rmSync(work, { recursive: true, force: true });
    }
  }
}

function readResults(p: string): Map<string, Json> {
  const map = new Map<string, Json>();
  if (!existsSync(p)) return map;
  for (const line of readFileSync(p, 'utf8').split(/\r?\n/)) {
    const s = line.trim();
    if (!s) continue;
    try {
      const node = JSON.parse(s);
      if (node?.id) map.set(String(node.id), node);
    } catch { /* ignore partial line */ }
  }
  return map;
}

function buildVerdict(problem: Json, problemId: string, language: string, mode: string, tests: Json[],
  raw: Map<string, Json>, outcome: { timedOut: boolean; stderr: string }): Json {
  const compareMode = problem.compare || 'exact';
  const results: Json[] = [];
  let passed = 0, visPassed = 0, visTotal = 0, hidPassed = 0, hidTotal = 0, totalMs = 0;
  let sawTle = outcome.timedOut, sawRe = false, sawWa = false;
  let firstError: string | null = null;

  for (const tc of tests) {
    const hidden = !!tc.hidden;
    hidden ? hidTotal++ : visTotal++;
    const res = raw.get(tc.id);
    const input = hidden ? null : tc.display ?? null;
    const expected = hidden ? null : JSON.stringify(tc.expected);

    if (!res) {
      const err = outcome.timedOut
        ? 'Execution timed out before completing this test case.'
        : (outcome.stderr && outcome.stderr.trim()) || 'Process terminated unexpectedly before completing this test case.';
      outcome.timedOut ? (sawTle = true) : (sawRe = true);
      firstError ??= err;
      results.push({
        id: tc.id, hidden, passed: false, status: outcome.timedOut ? 'TIME_LIMIT_EXCEEDED' : 'RUNTIME_ERROR', timeMs: 0,
        input, expected, actual: null, stdout: null,
        error: hidden ? (outcome.timedOut ? 'Time Limit Exceeded' : 'Runtime Error') : err,
      });
      continue;
    }

    const ms = Number(res.timeMs) || 0;
    totalMs += ms;
    const stdout = hidden ? null : (res.stdout || null);
    if (ms > PER_TEST_LIMIT_MS) {
      sawTle = true;
      const err = `Test exceeded per-test time limit of ${PER_TEST_LIMIT_MS} ms.`;
      firstError ??= err;
      results.push({ id: tc.id, hidden, passed: false, status: 'TIME_LIMIT_EXCEEDED', timeMs: round2(ms), input, expected, actual: null, stdout, error: err });
      continue;
    }
    if (res.status !== 'OK') {
      sawRe = true;
      const rawErr = String(res.error || 'Runtime error');
      const err = hidden ? hiddenError(rawErr) : rawErr;
      firstError ??= err;
      results.push({ id: tc.id, hidden, passed: false, status: 'RUNTIME_ERROR', timeMs: round2(ms), input, expected, actual: null, stdout, error: err });
      continue;
    }
    const ok = compareOutputs(tc.expected, res.output, compareMode);
    if (ok) {
      passed++;
      hidden ? hidPassed++ : visPassed++;
    } else {
      sawWa = true;
    }
    results.push({
      id: tc.id, hidden, passed: ok, status: ok ? 'PASSED' : 'WRONG_ANSWER', timeMs: round2(ms),
      input, expected, actual: hidden ? null : JSON.stringify(res.output ?? null), stdout, error: null,
    });
  }

  const status = sawTle ? 'TIME_LIMIT_EXCEEDED' : sawRe ? 'RUNTIME_ERROR' : (sawWa || passed < tests.length) ? 'WRONG_ANSWER' : 'ACCEPTED';
  return {
    problemId, language, mode, status,
    passedCount: passed, totalCount: tests.length,
    visiblePassed: visPassed, visibleTotal: visTotal, hiddenPassed: hidPassed, hiddenTotal: hidTotal,
    executionTimeMs: round2(totalMs), compileError: null, error: firstError, results,
  };
}

function errorResponse(problemId: string, language: string, mode: string, status: string, msg: string): Json {
  return {
    problemId, language, mode, status,
    passedCount: 0, totalCount: 0, visiblePassed: 0, visibleTotal: 0, hiddenPassed: 0, hiddenTotal: 0,
    executionTimeMs: 0,
    compileError: status === 'COMPILATION_ERROR' ? msg : null,
    error: status === 'COMPILATION_ERROR' ? null : msg,
    results: [],
  };
}

/** Strips the harness traceback and reports the user's own line number (solution.py has a 1-line prelude). */
function formatPythonSyntaxError(stderr: string): string {
  const idx = stderr.lastIndexOf('File "solution.py"');
  const body = idx >= 0 ? stderr.slice(idx) : stderr;
  return body.replace(/File "solution\.py", line (\d+)/g, (_m, n) => `File "solution.py", line ${Math.max(1, Number(n) - 1)}`).trim();
}

function hiddenError(raw: string): string {
  const first = raw.split(/\r?\n/, 1)[0];
  const colon = first.indexOf(':');
  return colon > 0 ? `${first.slice(0, colon)} on hidden test case` : 'Runtime Error on hidden test case';
}

function sanitize(text: string, workDir: string, javaCompile = false): string {
  if (!text) return '';
  let out = text.split(workDir + path.sep).join('').split(workDir + '/').join('').split(workDir).join('');
  if (javaCompile) {
    // Solution.java has one import line prepended: report the user's own line numbers.
    out = out.replace(/(Solution\.java|Adapter\.java):(\d+):/g, (_m, f, n) => `${f}:${Math.max(1, Number(n) - 1)}:`);
  }
  return out;
}

function truncate(s: string, max: number): string {
  if (!s) return '';
  return s.length <= max ? s : `${s.slice(0, max)}\n... (truncated)`;
}

function round2(v: number): number {
  return Math.round(v * 100) / 100;
}

// ---------------------------------------------------------------------------------------------
// Vite plugin
// ---------------------------------------------------------------------------------------------

function readBody(req: IncomingMessage): Promise<string> {
  return new Promise((resolve, reject) => {
    let data = '';
    req.on('data', (chunk) => {
      data += chunk;
      if (data.length > 1_000_000) {
        reject(new Error('Request body too large'));
        req.destroy();
      }
    });
    req.on('end', () => resolve(data));
    req.on('error', reject);
  });
}

function sendJson(res: ServerResponse, status: number, body: Json): void {
  res.statusCode = status;
  res.setHeader('Content-Type', 'application/json');
  res.end(JSON.stringify(body));
}

export function localJudgePlugin(opts: Options): Plugin {
  const enabled = (process.env.ALGOPLAY_JUDGE || 'local').toLowerCase() !== 'backend';
  const judge = new LocalJudge(opts);

  const middleware = async (req: IncomingMessage, res: ServerResponse, next: () => void) => {
    const url = (req.url || '').split('?')[0];
    if (!url.startsWith('/api/judge/')) return next();
    try {
      if (url === '/api/judge/health' && req.method === 'GET') return sendJson(res, 200, judge.health());
      if ((url === '/api/judge/run' || url === '/api/judge/submit') && req.method === 'POST') {
        let body: Json;
        try {
          body = JSON.parse((await readBody(req)) || '{}');
        } catch {
          return sendJson(res, 400, { error: 'Invalid JSON body' });
        }
        return sendJson(res, 200, await judge.evaluate(body, url.endsWith('/run')));
      }
      return sendJson(res, 404, { error: `Unknown judge endpoint ${req.method} ${url}` });
    } catch (e) {
      return sendJson(res, 500, { error: e instanceof Error ? e.message : String(e) });
    }
  };

  return {
    name: 'algoplay-local-judge',
    configureServer(server) {
      if (!enabled) return;
      server.middlewares.use(middleware);
      const h = judge.health();
      server.config.logger.info(
        `  [algoplay-judge] local compiler ready: ${h.loadedProblems} problems, java=${h.javaAvailable}, python=${h.pythonAvailable}`,
      );
    },
    configurePreviewServer(server) {
      if (!enabled) return;
      server.middlewares.use(middleware);
    },
  };
}
