"""CodeSystem judge harness (Python).

Usage: python judge_runner.py <tests.json> <results.jsonl>

The submitted code lives in solution.py (prelude + user code). Optional adapter.py defines run(input).
Writes one JSON line per test as soon as it finishes (same schema as the Java harness).
"""
import io
import json
import sys
import threading
import time
import traceback

sys.setrecursionlimit(200_000)
for _stack_mb in (64, 32, 16):
    try:
        threading.stack_size(_stack_mb * 1024 * 1024)
        break
    except (ValueError, RuntimeError):
        pass

MAX_STDOUT = 4096


class _LimitedIO(io.StringIO):
    def write(self, s):
        remaining = MAX_STDOUT - self.tell()
        if remaining > 0:
            super().write(s[:remaining])
        return len(s)


def _describe(exc: BaseException) -> str:
    msg = f"{type(exc).__name__}: {exc}"
    if isinstance(exc, RecursionError):
        msg += " (recursion too deep)"
    tb = traceback.extract_tb(exc.__traceback__)
    for frame in reversed(tb):
        if frame.filename.endswith("solution.py"):
            # solution.py has one prelude import line prepended to the user's code
            msg += f"\n    at line {max(1, frame.lineno - 1)} in {frame.name}"
            break
    return msg


def main():
    tests_path, results_path = sys.argv[1], sys.argv[2]
    with open(tests_path, encoding="utf-8") as f:
        root = json.load(f)
    sig = root["signature"]
    kind = sig.get("kind", "function")

    import judge_lib
    import solution as user_mod  # noqa: E402  (user code)

    adapter_run = None
    if kind == "adapter":
        import adapter  # noqa: E402
        adapter_run = adapter.run

    real_stdout = sys.stdout
    with open(results_path, "w", encoding="utf-8") as out:
        for test in root["tests"]:
            res = {"id": test["id"]}
            buf = _LimitedIO()
            sys.stdout = buf
            start = time.perf_counter()
            try:
                inp = test["input"]
                if kind == "function":
                    res["output"] = _run_function(judge_lib, user_mod, sig, inp)
                elif kind == "design":
                    res["output"] = _run_design(judge_lib, user_mod, sig, inp)
                elif kind == "adapter":
                    res["output"] = adapter_run(inp)
                else:
                    raise ValueError(f"Unknown signature kind {kind}")
                res["status"] = "OK"
            except BaseException as exc:  # noqa: BLE001 - user code may raise anything
                if isinstance(exc, KeyboardInterrupt):
                    raise
                res.pop("output", None)
                res["status"] = "RUNTIME_ERROR"
                res["error"] = _describe(exc)
            finally:
                sys.stdout = real_stdout
            res["timeMs"] = round((time.perf_counter() - start) * 1000, 2)
            res["stdout"] = buf.getvalue()
            try:
                line = json.dumps(res, allow_nan=False)
            except (TypeError, ValueError) as exc:
                line = json.dumps({"id": test["id"], "status": "RUNTIME_ERROR",
                                   "error": f"Return value is not serializable: {exc}",
                                   "timeMs": res["timeMs"], "stdout": res["stdout"]})
            out.write(line + "\n")
            out.flush()


def _run_function(lib, mod, sig, inp):
    cls = getattr(mod, "Solution", None)
    if cls is None:
        raise NameError("class Solution is not defined")
    inst = cls()
    name = sig["method"]
    fn = getattr(inst, name, None)
    if fn is None:
        raise AttributeError(f"Method {name} not found in class Solution. Do not rename the method from the starter code.")
    params = sig["params"]
    args = [lib.convert(inp[p["name"]], p["type"]) for p in params]
    ret = fn(*args)
    output = sig.get("output") or {"mode": "return"}
    mode = output.get("mode", "return")
    if mode == "return":
        return lib.serialize(ret, sig.get("returns", "void"))
    names = [p["name"] for p in params]
    idx = names.index(output["param"])
    if mode == "param":
        return lib.serialize(args[idx], params[idx]["type"])
    if mode == "prefix":
        k = int(ret)
        full = lib.serialize(args[idx], params[idx]["type"])
        if k < 0 or k > len(full):
            raise ValueError(f"Returned length {k} is out of range")
        return full[:k]
    raise ValueError(f"Unknown output mode {mode}")


def _run_design(lib, mod, sig, inp):
    cls_name = sig["className"]
    cls = getattr(mod, cls_name, None)
    if cls is None:
        raise NameError(f"class {cls_name} is not defined")
    ctor_params = (sig.get("constructor") or {}).get("params", [])
    methods = {m["name"]: m for m in sig["methods"]}
    ops, args = inp["ops"], inp["args"]
    out = []
    inst = None
    for i, (op, a) in enumerate(zip(ops, args)):
        if i == 0:
            if op != cls_name:
                raise ValueError(f"First op must be constructor {cls_name}")
            inst = cls(*[lib.convert(x, p["type"]) for x, p in zip(a, ctor_params)])
            out.append(None)
            continue
        spec = methods.get(op)
        if spec is None:
            raise ValueError(f"Unknown operation {op}")
        fn = getattr(inst, op, None)
        if fn is None:
            raise AttributeError(f"Method {op} not found in class {cls_name}")
        r = fn(*[lib.convert(x, p["type"]) for x, p in zip(a, spec["params"])])
        out.append(lib.serialize(r, spec.get("returns", "void")))
    return out


if __name__ == "__main__":
    _err = []

    def _target():
        try:
            main()
        except BaseException:  # noqa: BLE001
            _err.append(traceback.format_exc())

    t = threading.Thread(target=_target)
    t.start()
    t.join()
    if _err:
        sys.stderr.write("HARNESS_ERROR:\n" + _err[0])
        sys.exit(3)
