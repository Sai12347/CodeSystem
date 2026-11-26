#!/usr/bin/env python3
"""Build and validate the CodeSystem problem bank.

Source of truth: problems/<topicId>/<NN>-<slug>/
    problem.json   metadata + signature (see problems/AUTHORING.md)
    tests.py       defines visible() and hidden() -> list of {"in": {...}, optional "out": ...}
    solution.py    reference solution (Python)
    Solution.java  reference solution (Java)
    brute.py       optional brute-force Python solution used to cross-check expected outputs
    adapter.py / Adapter.java   only for signature.kind == "adapter"
    starter.py / starter.java   optional custom starter code (required for adapter problems)

For every problem this script:
  1. validates metadata, signature and test inputs,
  2. runs the Python reference -> expected outputs (or checks explicit "out" values),
  3. runs the Java reference and brute.py and requires they agree with the expected outputs,
  4. compiles/runs the starter code in both languages (must run without harness errors),
and then writes
  backend/src/main/resources/problems/<topicId>.json   (all tests incl. hidden, for the judge)
  frontend/src/data/problems/<topicId>.json            (public data: no hidden tests)

Usage:
  python tools/problems/build.py                     # all topics
  python tools/problems/build.py --topic arrays      # one topic (several topics: repeat flag)
  python tools/problems/build.py --topic arrays --problem two-sum   # just validate one problem
  options: --force (ignore cache) --jobs N --no-emit
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import hashlib
import json
import random
import re
import runpy
import sys
import time
import traceback
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import judgekit as jk  # noqa: E402

REPO = jk.REPO
PROBLEMS_DIR = REPO / "problems"
CACHE_DIR = REPO / "tools" / "problems" / ".cache"
BACKEND_OUT = REPO / "backend" / "src" / "main" / "resources" / "problems"
FRONTEND_OUT = REPO / "frontend" / "src" / "data" / "problems"
TOOL_VERSION = "1"

COMPANIES = ["Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Uber", "Goldman Sachs",
             "Adobe", "Atlassian", "Salesforce", "Oracle", "Bloomberg", "LinkedIn"]
DIFFICULTIES = ["Easy", "Medium", "Hard"]
SCALARS = {"int", "long", "double", "boolean", "char", "String", "Integer", "Long", "Double", "Boolean",
           "Character", "ListNode", "TreeNode"}
MAX_TEST_BYTES = 64_000
MAX_TOTAL_BYTES = 200_000
DIR_RE = re.compile(r"^(\d{2,3})-([a-z0-9]+(?:-[a-z0-9]+)*)$")


class ProblemError(Exception):
    pass


# ---------------------------------------------------------------------------
# Type helpers
# ---------------------------------------------------------------------------

def valid_type(t: str, allow_void: bool = False) -> bool:
    if allow_void and t == "void":
        return True
    if t.endswith("[]"):
        return valid_type(t[:-2])
    if t.startswith("List<") and t.endswith(">"):
        return valid_type(t[5:-1])
    return t in SCALARS


def py_type(t: str) -> str:
    if t == "void":
        return "None"
    if t.endswith("[]"):
        return f"List[{py_type(t[:-2])}]"
    if t.startswith("List<"):
        return f"List[{py_type(t[5:-1])}]"
    return {"int": "int", "long": "int", "Integer": "int", "Long": "int", "double": "float", "Double": "float",
            "boolean": "bool", "Boolean": "bool", "char": "str", "Character": "str", "String": "str",
            "ListNode": "Optional[ListNode]", "TreeNode": "Optional[TreeNode]"}[t]


def java_default(t: str) -> str:
    if t in ("int", "long"):
        return "0"
    if t == "double":
        return "0.0"
    if t == "boolean":
        return "false"
    if t == "char":
        return "' '"
    return "null"


def uses(sig: dict, name: str) -> bool:
    return name in json.dumps(sig)


LIST_NODE_DOC_JAVA = """/**
 * Definition for singly-linked list (provided by the judge).
 * public class ListNode {
 *     int val;
 *     ListNode next;
 *     ListNode() {}
 *     ListNode(int val) { this.val = val; }
 *     ListNode(int val, ListNode next) { this.val = val; this.next = next; }
 * }
 */
"""
TREE_NODE_DOC_JAVA = """/**
 * Definition for a binary tree node (provided by the judge).
 * public class TreeNode {
 *     int val;
 *     TreeNode left;
 *     TreeNode right;
 *     TreeNode() {}
 *     TreeNode(int val) { this.val = val; }
 *     TreeNode(int val, TreeNode left, TreeNode right) { this.val = val; this.left = left; this.right = right; }
 * }
 */
"""
LIST_NODE_DOC_PY = """# Definition for singly-linked list (provided by the judge).
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
"""
TREE_NODE_DOC_PY = """# Definition for a binary tree node (provided by the judge).
# class TreeNode:
#     def __init__(self, val=0, left=None, right=None):
#         self.val = val
#         self.left = left
#         self.right = right
"""


def gen_starters(sig: dict) -> tuple[str, str]:
    jdoc = (LIST_NODE_DOC_JAVA if uses(sig, "ListNode") else "") + (TREE_NODE_DOC_JAVA if uses(sig, "TreeNode") else "")
    pdoc = (LIST_NODE_DOC_PY if uses(sig, "ListNode") else "") + (TREE_NODE_DOC_PY if uses(sig, "TreeNode") else "")

    def jparams(ps):
        return ", ".join(f"{p['type']} {p['name']}" for p in ps)

    def pparams(ps):
        return "".join(f", {p['name']}: {py_type(p['type'])}" for p in ps)

    if sig["kind"] == "function":
        ret = sig.get("returns", "void")
        body = "        // Write your solution here\n"
        if ret != "void":
            body += f"        return {java_default(ret)};\n"
        java = f"{jdoc}class Solution {{\n    public {ret} {sig['method']}({jparams(sig['params'])}) {{\n{body}    }}\n}}\n"
        py = (f"{pdoc}class Solution:\n    def {sig['method']}(self{pparams(sig['params'])}) -> {py_type(ret)}:\n"
              f"        # Write your solution here\n        pass\n")
        return java, py
    if sig["kind"] == "design":
        cls = sig["className"]
        cps = (sig.get("constructor") or {}).get("params", [])
        jm = [f"    public {cls}({jparams(cps)}) {{\n        \n    }}\n"]
        pm = [f"    def __init__(self{pparams(cps)}):\n        pass\n"]
        for m in sig["methods"]:
            ret = m.get("returns", "void")
            body = "        \n" if ret == "void" else f"        return {java_default(ret)};\n"
            jm.append(f"    public {ret} {m['name']}({jparams(m['params'])}) {{\n{body}    }}\n")
            pm.append(f"    def {m['name']}(self{pparams(m['params'])}) -> {py_type(ret)}:\n        pass\n")
        java = f"{jdoc}class {cls} {{\n" + "\n".join(jm) + "}\n"
        py = f"{pdoc}class {cls}:\n" + "\n".join(pm)
        return java, py
    raise ProblemError("adapter problems must provide starter.java and starter.py")


# ---------------------------------------------------------------------------
# Loading & validation
# ---------------------------------------------------------------------------

def load_topics() -> list[dict]:
    return json.loads((PROBLEMS_DIR / "topics.json").read_text(encoding="utf-8"))


def read_opt(d: Path, name: str):
    p = d / name
    return p.read_text(encoding="utf-8") if p.exists() else None


def validate_meta(meta: dict, topic: dict, slug: str):
    req = ["title", "difficulty", "subtopic", "description", "constraints", "hints", "timeComplexity",
           "spaceComplexity", "signature", "companies"]
    for k in req:
        if k not in meta:
            raise ProblemError(f"problem.json missing '{k}'")
    if meta["difficulty"] not in DIFFICULTIES:
        raise ProblemError(f"difficulty must be one of {DIFFICULTIES}")
    if meta["subtopic"] not in topic["subtopics"]:
        raise ProblemError(f"subtopic '{meta['subtopic']}' not in topic subtopics {topic['subtopics']}")
    for c in meta["companies"]:
        if c not in COMPANIES:
            raise ProblemError(f"unknown company '{c}' (allowed: {COMPANIES})")
    if not isinstance(meta["constraints"], list) or not meta["constraints"]:
        raise ProblemError("constraints must be a non-empty list")
    if not isinstance(meta["hints"], list) or not meta["hints"]:
        raise ProblemError("hints must be a non-empty list")
    if len(meta["description"].strip()) < 60:
        raise ProblemError("description is too short")
    mode = meta.get("compare", "exact")
    if mode not in jk.COMPARE_MODES:
        raise ProblemError(f"compare must be one of {jk.COMPARE_MODES}")
    sig = meta["signature"]
    kind = sig.get("kind")
    if kind == "function":
        if not re.match(r"^[a-z][A-Za-z0-9]*$", sig.get("method", "")):
            raise ProblemError("signature.method must be camelCase")
        for p in sig.get("params", []):
            if not valid_type(p.get("type", "")):
                raise ProblemError(f"bad param type {p.get('type')}")
        if not valid_type(sig.get("returns", "void"), allow_void=True):
            raise ProblemError(f"bad return type {sig.get('returns')}")
        out = sig.get("output") or {"mode": "return"}
        if out.get("mode", "return") not in ("return", "param", "prefix"):
            raise ProblemError("bad output mode")
        if out.get("mode", "return") != "return" and out.get("param") not in [p["name"] for p in sig["params"]]:
            raise ProblemError("output.param must name a parameter")
        if out.get("mode") == "prefix" and sig.get("returns") != "int":
            raise ProblemError("prefix output mode requires an int return type")
    elif kind == "design":
        if not re.match(r"^[A-Z][A-Za-z0-9]*$", sig.get("className", "")):
            raise ProblemError("signature.className must be PascalCase")
        for p in (sig.get("constructor") or {}).get("params", []):
            if not valid_type(p["type"]):
                raise ProblemError(f"bad constructor param type {p['type']}")
        for m in sig.get("methods", []):
            for p in m.get("params", []):
                if not valid_type(p["type"]):
                    raise ProblemError(f"bad param type {p['type']} in {m['name']}")
            if not valid_type(m.get("returns", "void"), allow_void=True):
                raise ProblemError(f"bad return type in {m['name']}")
    elif kind == "adapter":
        if "inputs" not in sig:
            raise ProblemError("adapter signature needs 'inputs' (list of {name,type,description}) for display")
    else:
        raise ProblemError("signature.kind must be function, design or adapter")


def load_tests(d: Path, sig: dict) -> list[dict]:
    ns = runpy.run_path(str(d / "tests.py"), run_name="tests")
    random.seed(0)
    vis, hid = ns["visible"](), ns["hidden"]()
    if not (2 <= len(vis) <= 3):
        raise ProblemError(f"need 2-3 visible tests, got {len(vis)}")
    if not (8 <= len(hid) <= 15):
        raise ProblemError(f"need 8-15 hidden tests, got {len(hid)}")
    tests = []
    for prefix, lst, hidden in (("v", vis, False), ("h", hid, True)):
        for i, t in enumerate(lst, 1):
            if not isinstance(t, dict) or "in" not in t:
                raise ProblemError(f"test {prefix}{i} must be a dict with key 'in'")
            inp = t["in"]
            if sig["kind"] == "function":
                names = [p["name"] for p in sig["params"]]
                if sorted(inp.keys()) != sorted(names):
                    raise ProblemError(f"test {prefix}{i} input keys {sorted(inp)} != params {sorted(names)}")
            elif sig["kind"] == "design":
                if set(inp.keys()) != {"ops", "args"} or len(inp["ops"]) != len(inp["args"]):
                    raise ProblemError(f"test {prefix}{i} design input must be {{ops, args}} of equal length")
                if inp["ops"][0] != sig["className"]:
                    raise ProblemError(f"test {prefix}{i}: first op must be {sig['className']}")
            size = len(json.dumps(inp, separators=(",", ":")))
            if size > MAX_TEST_BYTES:
                raise ProblemError(f"test {prefix}{i} input is {size} bytes (max {MAX_TEST_BYTES})")
            tc = {"id": f"{prefix}{i}", "hidden": hidden, "input": inp}
            if "out" in t:
                tc["explicit"] = t["out"]
            tests.append(tc)
    total = sum(len(json.dumps(t["input"], separators=(",", ":"))) for t in tests)
    if total > MAX_TOTAL_BYTES:
        raise ProblemError(f"total test input size {total} bytes exceeds {MAX_TOTAL_BYTES}")
    seen = set()
    for t in tests:
        key = jk.canonical(t["input"])
        if key in seen:
            raise ProblemError(f"duplicate test input in {t['id']}")
        seen.add(key)
    return tests


def fmt(v) -> str:
    return json.dumps(v, separators=(",", ":"), ensure_ascii=False)


def display_input(sig: dict, inp: dict) -> str:
    if sig["kind"] == "design":
        return f"{fmt(inp['ops'])}\n{fmt(inp['args'])}"
    if sig["kind"] == "function":
        order = [p["name"] for p in sig["params"]]
    else:
        order = [p["name"] for p in sig["inputs"]] if sig.get("inputs") else list(inp.keys())
        order = [k for k in order if k in inp] + [k for k in inp if k not in order]
    return ", ".join(f"{k} = {fmt(inp[k])}" for k in order)


def sample_array(sig: dict, inp: dict) -> list:
    if sig["kind"] == "function":
        for p in sig["params"]:
            if p["type"] in ("int[]", "List<Integer>", "long[]") and isinstance(inp.get(p["name"]), list):
                return inp[p["name"]][:12]
    for v in inp.values():
        if isinstance(v, list) and v and all(isinstance(x, int) and not isinstance(x, bool) for x in v):
            return v[:12]
    return []


# ---------------------------------------------------------------------------
# Building one problem
# ---------------------------------------------------------------------------

def harness_hash() -> str:
    h = hashlib.sha256(TOOL_VERSION.encode())
    for p in sorted((jk.JUDGE_DIR).rglob("*")):
        if p.is_file():
            h.update(p.read_bytes())
    h.update((Path(__file__).resolve().parent / "judgekit.py").read_bytes())
    h.update(Path(__file__).resolve().read_bytes())
    return h.hexdigest()


def dir_hash(d: Path, base: str) -> str:
    h = hashlib.sha256(base.encode())
    for p in sorted(d.rglob("*")):
        if p.is_file() and "__pycache__" not in p.parts:
            h.update(p.relative_to(d).as_posix().encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def first_failure(results, tests, expected_by_id, mode, label):
    by_id = {r["id"]: r for r in results}
    for t in tests:
        r = by_id.get(t["id"])
        if r is None:
            return f"{label}: no result for test {t['id']} (timeout or crash)"
        if r["status"] != "OK":
            return f"{label}: test {t['id']} raised {r.get('error')}"
        if not jk.compare(expected_by_id[t["id"]], r["output"], mode):
            return (f"{label}: test {t['id']} output mismatch\n  input:    {fmt(t['input'])[:300]}\n"
                    f"  expected: {fmt(expected_by_id[t['id']])[:300]}\n  got:      {fmt(r['output'])[:300]}")
    return None


def build_problem(topic: dict, d: Path, base_hash: str, force: bool) -> dict:
    m = DIR_RE.match(d.name)
    if not m:
        raise ProblemError(f"directory name '{d.name}' must look like 01-some-slug")
    order, slug = int(m.group(1)), m.group(2)
    h = dir_hash(d, base_hash)
    cache_file = CACHE_DIR / f"{topic['id']}__{slug}.json"
    if not force and cache_file.exists():
        cached = json.loads(cache_file.read_text(encoding="utf-8"))
        if cached.get("hash") == h:
            return cached["record"]

    meta = json.loads((d / "problem.json").read_text(encoding="utf-8"))
    validate_meta(meta, topic, slug)
    sig = meta["signature"]
    mode = meta.get("compare", "exact")
    tests = load_tests(d, sig)

    py_ref = read_opt(d, "solution.py")
    java_ref = read_opt(d, "Solution.java")
    if not py_ref or not java_ref:
        raise ProblemError("solution.py and Solution.java are both required")
    adapter_py = read_opt(d, "adapter.py") if sig["kind"] == "adapter" else None
    adapter_java = read_opt(d, "Adapter.java") if sig["kind"] == "adapter" else None
    if sig["kind"] == "adapter" and (not adapter_py or not adapter_java):
        raise ProblemError("adapter problems need adapter.py and Adapter.java")

    # 1) Python reference
    pr = jk.run_python(py_ref, sig, tests, adapter_py, run_timeout=120)
    if pr.compile_error:
        raise ProblemError(f"solution.py failed to load:\n{pr.compile_error}")
    by_id = {r["id"]: r for r in pr.results}
    expected = {}
    py_times = []
    for t in tests:
        r = by_id.get(t["id"])
        if r is None:
            raise ProblemError(f"solution.py produced no result for {t['id']} (timeout={pr.timed_out})\n{pr.stderr}")
        if r["status"] != "OK":
            raise ProblemError(f"solution.py raised on {t['id']}: {r.get('error')}")
        py_times.append(r["timeMs"])
        if "explicit" in t:
            if mode == "anyOf":
                if not isinstance(t["explicit"], list) or not t["explicit"]:
                    raise ProblemError(f"{t['id']}: anyOf expects 'out' to be a non-empty list of acceptable answers")
            if not jk.compare(t["explicit"], r["output"], mode):
                raise ProblemError(f"solution.py disagrees with explicit 'out' on {t['id']}:\n"
                                   f"  out: {fmt(t['explicit'])[:300]}\n  got: {fmt(r['output'])[:300]}")
            expected[t["id"]] = t["explicit"]
        else:
            if mode == "anyOf":
                raise ProblemError(f"{t['id']}: compare 'anyOf' requires an explicit 'out' list for every test")
            expected[t["id"]] = r["output"]

    # 2) Java reference
    jr = jk.run_java(java_ref, sig, tests, adapter_java, run_timeout=120)
    if jr.compile_error:
        raise ProblemError(f"Solution.java failed to compile:\n{jr.compile_error[:3000]}")
    err = first_failure(jr.results, tests, expected, mode, "Solution.java")
    if err:
        raise ProblemError(err + ("\n" + jr.stderr if jr.stderr else ""))

    # 3) Brute force cross-check (partial results are fine if it is slow on large tests)
    brute = read_opt(d, "brute.py")
    brute_checked = 0
    if brute:
        br = jk.run_python(brute, sig, tests, adapter_py, run_timeout=60)
        if br.compile_error:
            raise ProblemError(f"brute.py failed to load:\n{br.compile_error}")
        for r in br.results:
            if r["status"] != "OK":
                raise ProblemError(f"brute.py raised on {r['id']}: {r.get('error')}")
            if not jk.compare(expected[r["id"]], r["output"], mode):
                t = next(t for t in tests if t["id"] == r["id"])
                raise ProblemError(f"brute.py disagrees on {r['id']}\n  input: {fmt(t['input'])[:300]}\n"
                                   f"  expected: {fmt(expected[r['id']])[:300]}\n  brute: {fmt(r['output'])[:300]}")
            brute_checked += 1

    # 4) Starter code must run under the harness
    starter_java = read_opt(d, "starter.java")
    starter_py = read_opt(d, "starter.py")
    if starter_java is None or starter_py is None:
        gj, gp = gen_starters(sig)
        starter_java = starter_java or gj
        starter_py = starter_py or gp
    sj = jk.run_java(starter_java, sig, tests[:2], adapter_java, run_timeout=60)
    if sj.compile_error or not sj.ok:
        raise ProblemError(f"Java starter code does not compile/run:\n{(sj.compile_error or sj.stderr)[:2000]}")
    starter_all = jk.run_python(starter_py, sig, tests, adapter_py, run_timeout=60)
    if starter_all.compile_error or not starter_all.ok:
        raise ProblemError(f"Python starter code does not load/run:\n{(starter_all.compile_error or starter_all.stderr)[:2000]}")
    trivially_passes = all(r["status"] == "OK" and jk.compare(expected[r["id"]], r["output"], mode)
                           for r in starter_all.results) and len(starter_all.results) == len(tests)
    if trivially_passes:
        raise ProblemError("the empty starter code passes every test - tests are too weak")

    explanations = meta.get("examples", [])
    visible = [t for t in tests if not t["hidden"]]
    record = {
        "public": {
            "id": slug,
            "order": order,
            "topicId": topic["id"],
            "topic": topic["name"],
            "title": meta["title"],
            "slug": slug,
            "difficulty": meta["difficulty"],
            "subtopic": meta["subtopic"],
            "companies": meta["companies"],
            "leetcode": meta.get("leetcode"),
            "description": meta["description"].strip(),
            "constraints": meta["constraints"],
            "hints": meta["hints"],
            "timeComplexity": meta["timeComplexity"],
            "spaceComplexity": meta["spaceComplexity"],
            "compare": mode,
            "examples": [
                {"input": display_input(sig, t["input"]), "output": fmt(expected[t["id"]]),
                 **({"explanation": explanations[i]["explanation"]}
                    if i < len(explanations) and explanations[i].get("explanation") else {})}
                for i, t in enumerate(visible)
            ],
            "starterCode": {"java": starter_java, "python": starter_py},
            "solutionCode": {"java": java_ref, "python": py_ref},
            "sampleArray": sample_array(sig, visible[0]["input"]),
            "visibleTestCount": len(visible),
            "hiddenTestCount": len(tests) - len(visible),
        },
        "judge": {
            "id": slug,
            "topicId": topic["id"],
            "title": meta["title"],
            "signature": sig,
            "compare": mode,
            "adapter": {"java": adapter_java, "python": adapter_py} if sig["kind"] == "adapter" else None,
            "tests": [{"id": t["id"], "hidden": t["hidden"], "input": t["input"], "expected": expected[t["id"]],
                       "display": display_input(sig, t["input"]) if not t["hidden"] else None} for t in tests],
        },
        "stats": {"pyMaxMs": max(py_times), "bruteChecked": brute_checked, "tests": len(tests)},
    }
    CACHE_DIR.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(json.dumps({"hash": h, "record": record}), encoding="utf-8")
    return record


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--topic", action="append")
    ap.add_argument("--problem")
    ap.add_argument("--problems", help="Comma-separated list of slugs to build/validate")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--no-emit", action="store_true")
    args = ap.parse_args()

    slug_filter = set(s.strip() for s in args.problems.split(",") if s.strip()) if args.problems else None

    topics = load_topics()
    topic_by_id = {t["id"]: t for t in topics}
    selected = args.topic or [t["id"] for t in topics]
    for tid in selected:
        if tid not in topic_by_id:
            sys.exit(f"unknown topic {tid}")
    base = harness_hash()

    jobs = []
    for tid in selected:
        tdir = PROBLEMS_DIR / tid
        if not tdir.exists():
            continue
        for d in sorted(p for p in tdir.iterdir() if p.is_dir() and not p.name.startswith((".", "_"))):
            m = DIR_RE.match(d.name)
            if args.problem and (not m or m.group(2) != args.problem):
                continue
            if slug_filter and (not m or m.group(2) not in slug_filter):
                continue
            jobs.append((topic_by_id[tid], d))
    if not jobs:
        sys.exit("no problems found")

    results: dict = {}
    failures = []
    t0 = time.time()
    with cf.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        fut = {ex.submit(build_problem, t, d, base, args.force): (t, d) for t, d in jobs}
        for f in cf.as_completed(fut):
            t, d = fut[f]
            name = f"{t['id']}/{d.name}"
            try:
                rec = f.result()
                results[(t["id"], d.name)] = rec
                s = rec["stats"]
                print(f"  OK   {name}  ({s['tests']} tests, py max {s['pyMaxMs']}ms, brute-checked {s['bruteChecked']})")
            except ProblemError as e:
                failures.append((name, str(e)))
                print(f"  FAIL {name}\n       " + str(e).replace("\n", "\n       "))
            except Exception:  # noqa: BLE001
                failures.append((name, traceback.format_exc()))
                print(f"  FAIL {name}\n" + traceback.format_exc())

    # global uniqueness of slugs/titles across everything that built
    seen_slug, seen_title = {}, {}
    for (tid, dname), rec in results.items():
        p = rec["public"]
        for key, seen, label in ((p["slug"], seen_slug, "slug"), (p["title"].lower(), seen_title, "title")):
            if key in seen and seen[key] != f"{tid}/{dname}":
                failures.append((f"{tid}/{dname}", f"duplicate {label} also used by {seen[key]}"))
            seen[key] = f"{tid}/{dname}"

    print(f"\n{len(results)} built, {len(failures)} failed in {time.time() - t0:.1f}s")
    if failures:
        print("FAILURES:")
        for n, e in failures:
            print(f" - {n}: {e.splitlines()[0]}")

    if args.no_emit or args.problem or args.problems:
        sys.exit(1 if failures else 0)

    if failures:
        print("Not emitting topic files because of failures.")
        sys.exit(1)

    BACKEND_OUT.mkdir(parents=True, exist_ok=True)
    FRONTEND_OUT.mkdir(parents=True, exist_ok=True)
    for tid in selected:
        # numeric order so that 100-xyz sorts after 99-abc (plain string order would put it after 10-...)
        recs = [results[k] for k in sorted((k for k in results if k[0] == tid),
                                           key=lambda k: (results[k]["public"]["order"], k[1]))]
        if not recs:
            continue
        pub = [r["public"] for r in recs]
        for i, p in enumerate(pub, 1):
            p["number"] = i
        (FRONTEND_OUT / f"{tid}.json").write_text(json.dumps(pub, ensure_ascii=False, indent=1), encoding="utf-8")
        (BACKEND_OUT / f"{tid}.json").write_text(
            json.dumps({"topicId": tid, "problems": [r["judge"] for r in recs]}, ensure_ascii=False,
                       separators=(",", ":")), encoding="utf-8")
        print(f"emitted {tid}: {len(recs)} problems")


if __name__ == "__main__":
    main()
