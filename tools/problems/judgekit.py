"""Shared helpers for running code through the CodeSystem judge harness and comparing outputs.

Used by tools/problems/build.py (offline validation of the problem bank). The backend
(com.codesystem.judge) implements the same protocol in Java for live submissions.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
import shutil
import subprocess
import sys
import tempfile
import threading
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

REPO = Path(__file__).resolve().parents[2]
JUDGE_DIR = REPO / "backend" / "src" / "main" / "resources" / "judge"
HARNESS_CACHE_ROOT = REPO / "tools" / "problems" / ".cache"
JAVA_IMPORT_LINE = "import java.util.*; import java.util.function.*; import java.util.stream.*; import java.math.*;"
PY_PRELUDE_LINE = "from judge_prelude import *  # noqa: F401,F403"
FLOAT_TOL = 1e-5
_HARNESS_LOCK = threading.Lock()
_HARNESS_DIR_CACHE: Optional[Path] = None


@dataclass
class RunResult:
    ok: bool                       # harness ran (no compile error / crash / timeout before any output)
    results: list = field(default_factory=list)
    compile_error: Optional[str] = None
    stderr: str = ""
    timed_out: bool = False


def prepare_java_source(code: str) -> str:
    code = re.sub(r"(?m)^\s*package\s+[\w.]+\s*;\s*$", "", code)
    code = re.sub(r"(?m)^\s*public\s+(?=((final|abstract)\s+)?(class|interface|enum|record)\b)", "", code)
    return JAVA_IMPORT_LINE + "\n" + code


def _ensure_java_harness() -> Path:
    """Compile Judge.java, ListNode.java, and TreeNode.java once and reuse their .class files."""
    global _HARNESS_DIR_CACHE
    if _HARNESS_DIR_CACHE is not None and (_HARNESS_DIR_CACHE / "Judge.class").is_file():
        return _HARNESS_DIR_CACHE
    with _HARNESS_LOCK:
        if _HARNESS_DIR_CACHE is not None and (_HARNESS_DIR_CACHE / "Judge.class").is_file():
            return _HARNESS_DIR_CACHE
        names = ("Judge.java", "ListNode.java", "TreeNode.java")
        h = hashlib.sha256()
        for name in names:
            h.update((JUDGE_DIR / "java" / name).read_bytes())
        target = HARNESS_CACHE_ROOT / f"java-harness-{h.hexdigest()[:16]}"
        ready = target / ".ready"
        if ready.is_file() and (target / "Judge.class").is_file():
            _HARNESS_DIR_CACHE = target
            return target
        HARNESS_CACHE_ROOT.mkdir(parents=True, exist_ok=True)
        tmp = Path(tempfile.mkdtemp(prefix="cs-jharness-", dir=str(HARNESS_CACHE_ROOT)))
        try:
            for name in names:
                shutil.copy(JUDGE_DIR / "java" / name, tmp / name)
            out_dir = tmp / "out"
            out_dir.mkdir()
            srcs = [str(tmp / n) for n in names]
            c = subprocess.run(["javac", "-encoding", "UTF-8", "-nowarn", "-d", str(out_dir), *srcs],
                               capture_output=True, text=True, timeout=120)
            if c.returncode != 0:
                raise RuntimeError(f"Failed to compile Java harness:\n{c.stdout}{c.stderr}")
            target.mkdir(parents=True, exist_ok=True)
            for cls in out_dir.iterdir():
                dst = target / cls.name
                if not dst.exists():
                    try:
                        shutil.copy2(cls, dst)
                    except OSError:
                        pass
            try:
                ready.write_text("ok", encoding="utf-8")
            except OSError:
                pass
        finally:
            shutil.rmtree(tmp, ignore_errors=True)
        # Wait briefly if another process is finishing copy
        for _ in range(20):
            if (target / "Judge.class").is_file():
                break
            time.sleep(0.05)
        _HARNESS_DIR_CACHE = target
        return target


def prepare_python_source(code: str) -> str:
    return PY_PRELUDE_LINE + "\n" + code


def _read_results(path: Path) -> list:
    out = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def _write_tests(dirpath: Path, signature: dict, tests: list) -> Path:
    p = dirpath / "tests.json"
    p.write_text(json.dumps({"signature": signature,
                             "tests": [{"id": t["id"], "input": t["input"]} for t in tests]}), encoding="utf-8")
    return p


def run_java(code: str, signature: dict, tests: list, adapter: Optional[str] = None,
             compile_timeout: float = 120, run_timeout: float = 60) -> RunResult:
    harness_dir = _ensure_java_harness()
    tmp = Path(tempfile.mkdtemp(prefix="cs-java-"))
    try:
        (tmp / "Solution.java").write_text(prepare_java_source(code), encoding="utf-8")
        if adapter:
            (tmp / "Adapter.java").write_text(JAVA_IMPORT_LINE + "\n" + adapter, encoding="utf-8")
        tests_path = _write_tests(tmp, signature, tests)
        out_dir = tmp / "out"
        out_dir.mkdir()
        srcs = [str(p) for p in tmp.glob("*.java")]
        try:
            c = subprocess.run(["javac", "-encoding", "UTF-8", "-nowarn", "-cp", str(harness_dir), "-d", str(out_dir), *srcs],
                               capture_output=True, text=True, timeout=compile_timeout)
        except subprocess.TimeoutExpired:
            return RunResult(ok=False, compile_error="Compilation timed out")
        if c.returncode != 0:
            return RunResult(ok=False, compile_error=(c.stdout + c.stderr).replace(str(tmp) + os.sep, ""))
        results_path = tmp / "results.jsonl"
        timed_out = False
        cp = f"{out_dir}{os.pathsep}{harness_dir}"
        try:
            r = subprocess.run(["java", "-Xss64m", "-Xmx512m", "-XX:+UseSerialGC", "-XX:TieredStopAtLevel=1",
                                "-cp", cp, "Judge", str(tests_path), str(results_path)],
                               capture_output=True, text=True, timeout=run_timeout)
            stderr = r.stderr
            crashed = r.returncode != 0
        except subprocess.TimeoutExpired as e:
            timed_out = True
            stderr = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
            crashed = False
        res = _read_results(results_path)
        return RunResult(ok=not crashed, results=res, stderr=stderr[-4000:], timed_out=timed_out)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


def run_python(code: str, signature: dict, tests: list, adapter: Optional[str] = None,
               run_timeout: float = 60) -> RunResult:
    tmp = Path(tempfile.mkdtemp(prefix="cs-py-"))
    try:
        (tmp / "solution.py").write_text(prepare_python_source(code), encoding="utf-8")
        for name in ("judge_lib.py", "judge_prelude.py", "judge_runner.py"):
            shutil.copy(JUDGE_DIR / "python" / name, tmp / name)
        if adapter:
            (tmp / "adapter.py").write_text(adapter, encoding="utf-8")
        tests_path = _write_tests(tmp, signature, tests)
        results_path = tmp / "results.jsonl"
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONIOENCODING="utf-8", PYTHONHASHSEED="0")
        timed_out = False
        try:
            r = subprocess.run([sys.executable, "judge_runner.py", str(tests_path), str(results_path)],
                               cwd=tmp, capture_output=True, text=True, timeout=run_timeout, env=env)
            stderr = r.stderr
            crashed = r.returncode != 0
        except subprocess.TimeoutExpired as e:
            timed_out = True
            stderr = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
            crashed = False
        res = _read_results(results_path)
        compile_error = None
        if crashed and not res and ("SyntaxError" in stderr or "IndentationError" in stderr):
            compile_error = stderr[-4000:]
        return RunResult(ok=not crashed, results=res, stderr=stderr[-4000:], timed_out=timed_out,
                         compile_error=compile_error)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)


# ---------------------------------------------------------------------------
# Output comparison
# ---------------------------------------------------------------------------

def normalize(v: Any) -> Any:
    if isinstance(v, bool) or v is None or isinstance(v, str):
        return v
    if isinstance(v, int):
        return v
    if isinstance(v, float):
        if math.isfinite(v) and v.is_integer() and abs(v) < 2 ** 53:
            return int(v)
        return v
    if isinstance(v, list):
        return [normalize(x) for x in v]
    if isinstance(v, dict):
        return {k: normalize(x) for k, x in v.items()}
    return v


def canonical(v: Any) -> str:
    return json.dumps(normalize(v), sort_keys=True, separators=(",", ":"))


def deep_sort(v: Any) -> Any:
    if isinstance(v, list):
        return sorted((deep_sort(x) for x in v), key=canonical)
    return v


def values_equal(a: Any, b: Any, tol: Optional[float] = None) -> bool:
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        if tol is None:
            return normalize(a) == normalize(b)
        return abs(a - b) <= tol or abs(a - b) <= tol * max(abs(a), abs(b))
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(values_equal(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(values_equal(a[k], b[k], tol) for k in a)
    return a == b


COMPARE_MODES = ("exact", "float", "sorted", "sortedDeep", "anyOf")


def compare(expected: Any, actual: Any, mode: str = "exact") -> bool:
    if mode == "exact":
        return values_equal(normalize(expected), normalize(actual))
    if mode == "float":
        return values_equal(expected, actual, FLOAT_TOL)
    if mode == "sorted":
        if not isinstance(expected, list) or not isinstance(actual, list):
            return values_equal(normalize(expected), normalize(actual))
        return values_equal(sorted(normalize(expected), key=canonical), sorted(normalize(actual), key=canonical))
    if mode == "sortedDeep":
        return values_equal(deep_sort(normalize(expected)), deep_sort(normalize(actual)))
    if mode == "anyOf":
        return any(values_equal(normalize(e), normalize(actual)) for e in expected)
    raise ValueError(f"Unknown compare mode {mode}")
