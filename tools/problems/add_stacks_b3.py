#!/usr/bin/env python3
"""Generate stacks problems 73-100 (batch 3) for AlgoPlay."""
from __future__ import annotations

import json
import math
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "stacks"

ALLOWED_SUBTOPICS = {
    "LIFO Structure",
    "Valid Parentheses",
    "Expression Parsing",
    "Min Stack",
}
ALLOWED_COMPANIES = {
    "Google", "Amazon", "Microsoft", "Meta", "Apple", "Netflix", "Uber",
    "Goldman Sachs", "Adobe", "Atlassian", "Salesforce", "Oracle",
    "Bloomberg", "LinkedIn",
}


def py_type(t: str) -> str:
    if t == "void":
        return "None"
    if t.endswith("[]"):
        return f"List[{py_type(t[:-2])}]"
    if t.startswith("List<") and t.endswith(">"):
        return f"List[{py_type(t[5:-1])}]"
    return {
        "int": "int",
        "Integer": "int",
        "long": "int",
        "Long": "int",
        "double": "float",
        "Double": "float",
        "boolean": "bool",
        "Boolean": "bool",
        "char": "str",
        "Character": "str",
        "String": "str",
    }[t]


# ---------------------------------------------------------------------------
# Deterministic performance test builders
# ---------------------------------------------------------------------------

def _perf_73():
    # Generate a valid stack-sortable permutation of 1..600 using a random push/pop sequence
    rng = random.Random(7301)
    n = 600
    st = []
    out = []
    nxt = 1
    while nxt <= n or st:
        if nxt <= n and (not st or rng.random() < 0.55):
            st.append(nxt)
            nxt += 1
        else:
            out.append(st.pop())
    # Reverse of a stack-generated output is stack-sortable? Actually simulate directly:
    # A permutation p is stack-sortable iff pushing p can emit 1..n.
    # Reversing the process: start from 1..n in reverse, pop onto input -> guaranteed sortable!
    st = []
    perm = []
    src = list(range(n, 0, -1))
    idx = 0
    while idx < n or st:
        if idx < n and (not st or rng.random() < 0.55):
            st.append(src[idx])
            idx += 1
        else:
            perm.append(st.pop())
    perm.reverse()
    return perm


def _perf_74():
    rng = random.Random(7401)
    arr = list(range(1, 501))
    rng.shuffle(arr)
    return arr


def _perf_75():
    rng = random.Random(7501)
    words = ["a", "bc", "def", "xy", "st", "k", "lm", "pq"]
    cmds = []
    for _ in range(500):
        r = rng.random()
        if r < 0.55:
            cmds.append("TYPE " + rng.choice(words))
        elif r < 0.80:
            cmds.append("UNDO")
        else:
            cmds.append("REDO")
    return cmds


def _perf_76():
    rng = random.Random(7601)
    k = 12
    cap = 120
    ops = ["KStacks"]
    args = [[k, cap]]
    for _ in range(600):
        sid = rng.randint(0, k - 1)
        r = rng.random()
        if r < 0.45:
            ops.append("push")
            args.append([sid, rng.randint(0, 100000)])
        elif r < 0.72:
            ops.append("pop")
            args.append([sid])
        elif r < 0.88:
            ops.append("peek")
            args.append([sid])
        else:
            ops.append("size")
            args.append([sid])
    return {"ops": ops, "args": args}


def _perf_77():
    rng = random.Random(7701)
    events = []
    depth = 0
    for _ in range(600):
        r = rng.random()
        if depth == 0 or (depth < 40 and r < 0.42):
            events.append(f"CALL {rng.randint(10, 50000)}")
            depth += 1
        elif r < 0.72:
            events.append(f"ALLOC {rng.randint(1, 30000)}")
        elif r < 0.86:
            events.append(f"SHRINK {rng.randint(1, 40000)}")
        else:
            events.append("RET")
            depth -= 1
    while depth > 0:
        events.append("RET")
        depth -= 1
    return events


def _perf_78():
    rng = random.Random(7801)
    return [rng.randint(1, 500) for _ in range(800)]


def _perf_79():
    rng = random.Random(7901)
    # Build 20 balanced blocks and rotate them
    parts = []
    for _ in range(20):
        k = rng.randint(3, 15)
        parts.append("(" * k + ")" * k)
    s = "".join(parts)
    rot = rng.randint(1, len(s) - 1)
    return s[rot:] + s[:rot]


def _perf_80():
    rng = random.Random(8001)
    pairs = [("(", ")"), ("[", "]"), ("{", "}")]
    out = []
    st = []
    for _ in range(400):
        r = rng.random()
        if r < 0.35 and len(st) < 30:
            op, cl = rng.choice(pairs)
            out.append(op)
            st.append(cl)
        elif r < 0.65 and st:
            out.append(st.pop())
        elif r < 0.85:
            # Valid quoted string with wild brackets and escapes
            inner = rng.choice(['([}])', 'a\\"b[', '\\\\(]', '{}"\\"'])
            out.append('"' + inner + '"')
        else:
            out.append(rng.choice(["abc", " x ", "z"]))
    while st:
        out.append(st.pop())
    return "".join(out)


def _perf_81():
    rng = random.Random(8101)
    depths = []
    cur = 0
    rem_open = 400
    rem_close = 400
    while rem_open > 0 or rem_close > 0:
        if rem_open > 0 and (cur == 0 or (rem_close > rem_open and rng.random() < 0.5) or rng.random() < 0.45):
            cur += 1
            depths.append(cur)
            rem_open -= 1
        else:
            depths.append(cur)
            cur -= 1
            rem_close -= 1
    return depths


def _perf_82():
    rng = random.Random(8201)
    opens = "([{<"
    closes = ")]}>"
    out = []
    rem_open = 500
    cur = 0
    for _ in range(1000):
        if rem_open > 0 and (cur == 0 or rng.random() < 0.5):
            out.append(rng.choice(opens))
            rem_open -= 1
            cur += 1
        else:
            out.append(rng.choice(closes))
            cur -= 1
    return "".join(out)


def _perf_83():
    rng = random.Random(8301)
    out = []
    rem = 150
    cur = 0
    while rem > 0 or cur > 0:
        if rem > 0 and (cur == 0 or rng.random() < 0.52):
            out.append("(")
            rem -= 1
            cur += 1
        else:
            out.append(")")
            cur -= 1
    return "".join(out)


def _perf_84():
    rng = random.Random(8401)
    out = []
    rem = 500
    cur = 0
    while rem > 0 or cur > 0:
        if rem > 0 and (cur == 0 or rng.random() < 0.5):
            out.append("(")
            rem -= 1
            cur += 1
        else:
            out.append(")")
            cur -= 1
    # Flip two ')' to '('? No, flip one ')' to '(' so total balance becomes +2
    pos = [i for i, c in enumerate(out) if c == ")"]
    flip_idx = rng.choice(pos[len(pos) // 3 : 2 * len(pos) // 3])
    out[flip_idx] = "("
    return "".join(out)


def _perf_85():
    rng = random.Random(8501)
    frags = []
    for _ in range(120):
        ln = rng.randint(2, 16)
        frags.append("".join(rng.choice("()") for _ in range(ln)))
    return frags


def _perf_86():
    rng = random.Random(8601)
    ops = ["+", "-", "*", "/"]
    letters = "abcdefghijklmnopqrstuvwxyz"

    def build(depth: int) -> str:
        if depth <= 0 or (depth <= 4 and rng.random() < 0.35):
            return rng.choice(letters)
        left = build(depth - 1)
        right = build(depth - 1)
        op = rng.choice(ops)
        if rng.random() < 0.35:
            return f"({left} {op} {right})"
        return f"{left} {op} {right}"

    return build(7)


def _perf_87():
    rng = random.Random(8701)
    ops = ["&", "^", "|"]

    def build(depth: int) -> str:
        if depth <= 0 or (depth <= 4 and rng.random() < 0.3):
            atom = rng.choice(["T", "F"])
            if rng.random() < 0.4:
                atom = "!" + atom
            return atom
        left = build(depth - 1)
        right = build(depth - 1)
        op = rng.choice(ops)
        res = f"({left} {op} {right})" if rng.random() < 0.4 else f"{left} {op} {right}"
        if rng.random() < 0.25:
            res = "!(" + res + ")"
        return res

    return build(7)


def _perf_88():
    rng = random.Random(8801)
    tokens = []
    h = 0
    for _ in range(600):
        if h < 2 or (h < 25 and rng.random() < 0.52):
            tokens.append(str(rng.randint(-50, 50)))
            h += 1
        elif rng.random() < 0.25:
            tokens.append(rng.choice(["neg", "abs"]))
        else:
            tokens.append(rng.choice(["+", "-", "*", "/"]))
            h -= 1
    while h > 1:
        tokens.append(rng.choice(["+", "-", "*", "/"]))
        h -= 1
    return tokens


def _perf_89():
    # Sum of products of bounded degree <= 6 so coefficients stay well inside signed 64-bit
    rng = random.Random(8901)
    terms = []
    for _ in range(18):
        deg = rng.randint(1, 3)
        factors = []
        for _ in range(deg):
            a = rng.randint(1, 4)
            b = rng.randint(0, 5)
            op = rng.choice(["+", "-"])
            factors.append(f"({a} * x {op} {b})")
        terms.append(" * ".join(factors))
    out = terms[0]
    for t in terms[1:]:
        out += f" {rng.choice(['+', '-'])} {t}"
    return out


def _perf_90():
    rng = random.Random(9001)
    ops = ["&", "|", "-", "^"]

    def make_set() -> str:
        sz = rng.randint(0, 8)
        vals = sorted(rng.sample(range(-20, 21), sz))
        return "{" + ", ".join(str(v) for v in vals) + "}"

    def build(depth: int) -> str:
        if depth <= 0 or (depth <= 3 and rng.random() < 0.3):
            return make_set()
        l = build(depth - 1)
        r = build(depth - 1)
        op = rng.choice(ops)
        return f"({l} {op} {r})" if rng.random() < 0.45 else f"{l} {op} {r}"

    return build(5)


def _perf_91():
    rng = random.Random(9101)
    letters = "abcdefgh"

    def build(depth: int) -> str:
        if depth <= 0:
            ch = rng.choice(letters)
            q = rng.choice(["", "?", "{2}", "{1,3}"])
            return ch + q
        n_branches = rng.randint(1, 3)
        branches = []
        for _ in range(n_branches):
            n_items = rng.randint(1, 3)
            items = [build(depth - 1) for _ in range(n_items)]
            branches.append("".join(items))
        grp = "(" + "|".join(branches) + ")"
        q = rng.choice(["", "?", "{2}", "{1,2}"])
        return grp + q

    return build(4)


def _perf_92():
    rng = random.Random(9201)
    ops = ["+", "-", "*", "/"]

    def build(depth: int) -> str:
        if depth <= 0 or (depth <= 4 and rng.random() < 0.3):
            return str(rng.randint(1, 99))
        l = build(depth - 1)
        r = build(depth - 1)
        op = rng.choice(ops)
        return f"({l} {op} {r})" if rng.random() < 0.4 else f"{l} {op} {r}"

    return build(7)


def _perf_93():
    rng = random.Random(9301)
    ops = ["BoundedMinStack"]
    args = [[80]]
    for _ in range(600):
        r = rng.random()
        if r < 0.45:
            ops.append("push")
            args.append([rng.randint(0, 500)])
        elif r < 0.65:
            ops.append("pop")
            args.append([])
        elif r < 0.78:
            ops.append("top")
            args.append([])
        elif r < 0.89:
            ops.append("getMin")
            args.append([])
        else:
            ops.append("getMinIndex")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_94():
    rng = random.Random(9401)
    ops = ["GcdStack"]
    args = [[]]
    sz = 0
    pool = [12, 18, 24, 30, 36, 42, 48, 60, 72, 84, 90, 96, 108, 120, 144, 15, 25, 35, 100]
    for _ in range(600):
        r = rng.random()
        if sz == 0 or r < 0.52:
            ops.append("push")
            args.append([rng.choice(pool)])
            sz += 1
        elif r < 0.72:
            ops.append("pop")
            args.append([])
            sz -= 1
        elif r < 0.85:
            ops.append("top")
            args.append([])
        else:
            ops.append("getGcd")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_95():
    rng = random.Random(9501)
    ops = ["AffineMinStack"]
    args = [[]]
    sz = 0
    for _ in range(600):
        r = rng.random()
        if sz == 0 or r < 0.36:
            ops.append("push")
            args.append([rng.randint(-10000, 10000)])
            sz += 1
        elif r < 0.52:
            ops.append("pop")
            args.append([])
            sz -= 1
        elif r < 0.66:
            ops.append("addAll")
            args.append([rng.randint(-500, 500)])
        elif r < 0.78:
            ops.append("negateAll")
            args.append([])
        elif r < 0.89:
            ops.append("top")
            args.append([])
        else:
            ops.append("getMin")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_96():
    rng = random.Random(9601)
    ops = ["MinDeque"]
    args = [[]]
    sz = 0
    # Push 150 elements, then alternate front/back pops and pushes to stress rebalancing
    for _ in range(150):
        if rng.random() < 0.5:
            ops.append("pushFront")
        else:
            ops.append("pushBack")
        args.append([rng.randint(-100000, 100000)])
        sz += 1
    for i in range(450):
        r = rng.random()
        if sz == 0 or r < 0.35:
            ops.append("pushFront" if i % 2 == 0 else "pushBack")
            args.append([rng.randint(-100000, 100000)])
            sz += 1
        elif r < 0.58:
            ops.append("popFront")
            args.append([])
            sz -= 1
        elif r < 0.81:
            ops.append("popBack")
            args.append([])
            sz -= 1
        else:
            ops.append("getMin")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_97():
    rng = random.Random(9701)
    ops = ["TopKMinStack"]
    args = [[]]
    sz = 0
    for _ in range(600):
        r = rng.random()
        if sz == 0 or r < 0.45:
            ops.append("push")
            args.append([rng.randint(-100000, 100000)])
            sz += 1
        elif r < 0.62:
            ops.append("pop")
            args.append([])
            sz -= 1
        elif r < 0.75:
            ops.append("getMin")
            args.append([])
        else:
            k = rng.randint(1, sz)
            ops.append("getTopKMin")
            args.append([k])
    return {"ops": ops, "args": args}


def _perf_98():
    rng = random.Random(9801)
    ops = ["RunLengthMinStack"]
    args = [[]]
    sz = 0
    for _ in range(550):
        r = rng.random()
        if sz == 0 or r < 0.48:
            val = rng.randint(-5000, 5000)
            cnt = rng.randint(1, 1000000)
            ops.append("pushMany")
            args.append([val, cnt])
            sz += cnt
        elif r < 0.70:
            take = rng.randint(1, min(sz, 1500000))
            ops.append("popMany")
            args.append([take])
            sz -= take
        elif r < 0.85:
            ops.append("top")
            args.append([])
        else:
            ops.append("getMin")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_99():
    rng = random.Random(9901)
    max_sz = 128
    ops = ["IncrementableMinStack"]
    args = [[max_sz]]
    sz = 0
    for _ in range(550):
        r = rng.random()
        if sz == 0 or (sz < max_sz and r < 0.36):
            ops.append("push")
            args.append([rng.randint(-5000, 5000)])
            sz += 1
        elif r < 0.52:
            ops.append("pop")
            args.append([])
            sz -= 1
        elif r < 0.72:
            ops.append("increment")
            args.append([rng.randint(1, max_sz + 10), rng.randint(-1000, 1000)])
        elif r < 0.86:
            ops.append("top")
            args.append([])
        else:
            ops.append("getMin")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_100():
    rng = random.Random(10001)
    ops = ["MinMaxSubarrayStack"]
    args = [[]]
    sz = 0
    for _ in range(600):
        r = rng.random()
        if sz == 0 or r < 0.45:
            ops.append("push")
            args.append([rng.randint(-10000, 10000)])
            sz += 1
        elif r < 0.64:
            ops.append("pop")
            args.append([])
            sz -= 1
        elif r < 0.76:
            ops.append("top")
            args.append([])
        elif r < 0.88:
            ops.append("getMinSubarraySum")
            args.append([])
        else:
            ops.append("getMaxSubarraySum")
            args.append([])
    return {"ops": ops, "args": args}


# ---------------------------------------------------------------------------
# Problem definitions (73-100)
# ---------------------------------------------------------------------------

TASKS = [
    # ------------------------------------------------------------------
    # 73 - Stack Sortable Permutation
    # ------------------------------------------------------------------
    {
        "slug": "73-stack-sortable-permutation",
        "title": "Stack Sortable Permutation",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Microsoft", "Bloomberg"],
        "desc": (
            "You are given an integer array `perm` representing a permutation of `1, 2, ..., n` arriving on an input track from left to right. "
            "You have a single LIFO siding stack. At each step you may either push the next element of `perm` onto the stack or pop the top element of the stack onto the output track.\n\n"
            "Return `true` if it is possible to emit `[1, 2, ..., n]` in strictly ascending order on the output track, and `false` otherwise."
        ),
        "cons": [
            "1 <= perm.length <= 10^5",
            "perm is a permutation of integers from 1 to perm.length."
        ],
        "hints": [
            "Maintain the next expected output integer `need` (starting at 1) alongside a simulation stack.",
            "Push each element of `perm` onto the stack and immediately pop while the stack top equals `need`, incrementing `need`; the permutation is stack-sortable iff `need` reaches `n + 1`."
        ],
        "explanations": [
            "Push 3, push 2, push 1, then pop 1, 2, 3 to produce [1, 2, 3].",
            "2 must stay on the stack while waiting for 1, which traps 3 above 2 after 1 is popped, making [1, 2, 3] impossible.",
            "Push 2, push 1, pop 1, pop 2, push 4, push 3, pop 3, pop 4 produces [1, 2, 3, 4]."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "canSortWithStack",
        "params": [("perm", "int[]")],
        "ret": "boolean",
        "py": """        stack = []
        need = 1
        for x in perm:
            stack.append(x)
            while stack and stack[-1] == need:
                stack.pop()
                need += 1
        return need == len(perm) + 1""",
        "java": """        Deque<Integer> stack = new ArrayDeque<>();
        int need = 1;
        for (int x : perm) {
            stack.push(x);
            while (!stack.isEmpty() && stack.peek() == need) {
                stack.pop();
                need++;
            }
        }
        return need == perm.length + 1;""",
        "visible": [
            {"perm": [3, 2, 1]},
            {"perm": [2, 3, 1]},
            {"perm": [2, 1, 4, 3]},
        ],
        "hidden": [
            {"perm": [1]},
            {"perm": [1, 2, 3, 4, 5]},
            {"perm": [5, 4, 3, 2, 1]},
            {"perm": [3, 1, 2]},
            {"perm": [1, 3, 2]},
            {"perm": [4, 2, 1, 3]},
            {"perm": [4, 1, 3, 2]},
            {"perm": [3, 2, 1, 5, 4, 7, 6]},
            {"perm": _perf_73()},
        ],
    },

    # ------------------------------------------------------------------
    # 74 - Lexicographically Largest Stack Output
    # ------------------------------------------------------------------
    {
        "slug": "74-lexicographically-largest-stack-output",
        "title": "Lexicographically Largest Stack Output",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Meta", "Amazon", "Uber"],
        "desc": (
            "Given a permutation `nums` of `1, 2, ..., n`, you process elements from left to right using a single LIFO stack. "
            "Every element of `nums` must be pushed onto the stack in order, and at any moment you may pop the top element of the stack and append it to the output array until both `nums` and the stack are empty.\n\n"
            "Return the **lexicographically largest** output permutation that can be formed."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "nums is a permutation of integers from 1 to nums.length."
        ],
        "hints": [
            "Precompute `suffixMax[i]`, the maximum value among `nums[i..n - 1]` (with `suffixMax[n] = 0`).",
            "After pushing `nums[i]`, greedily pop from the stack to the output while the stack top is strictly greater than `suffixMax[i + 1]`."
        ],
        "explanations": [
            "Push 2, push 1, push 5, pop 5, push 3, push 4, pop 4, pop 3, pop 1, pop 2 gives [5, 4, 3, 1, 2].",
            "Push 1, 2, 3, 4, then pop all to get [4, 3, 2, 1].",
            "Push 4 and immediately pop 4 (greater than all remaining), then push 2, 3 and pop 3, 2, then push/pop 1 -> [4, 3, 2, 1]."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "largestStackOutput",
        "params": [("nums", "int[]")],
        "ret": "int[]",
        "py": """        n = len(nums)
        suf_max = [0] * (n + 1)
        for i in range(n - 1, -1, -1):
            suf_max[i] = nums[i] if nums[i] > suf_max[i + 1] else suf_max[i + 1]
        stack = []
        out = []
        for i, x in enumerate(nums):
            stack.append(x)
            nxt_max = suf_max[i + 1]
            while stack and stack[-1] > nxt_max:
                out.append(stack.pop())
        return out""",
        "java": """        int n = nums.length;
        int[] sufMax = new int[n + 1];
        for (int i = n - 1; i >= 0; i--) {
            sufMax[i] = Math.max(nums[i], sufMax[i + 1]);
        }
        Deque<Integer> stack = new ArrayDeque<>();
        int[] out = new int[n];
        int idx = 0;
        for (int i = 0; i < n; i++) {
            stack.push(nums[i]);
            int nxtMax = sufMax[i + 1];
            while (!stack.isEmpty() && stack.peek() > nxtMax) {
                out[idx++] = stack.pop();
            }
        }
        return out;""",
        "visible": [
            {"nums": [2, 1, 5, 3, 4]},
            {"nums": [1, 2, 3, 4]},
            {"nums": [4, 2, 3, 1]},
        ],
        "hidden": [
            {"nums": [1]},
            {"nums": [2, 1]},
            {"nums": [1, 2]},
            {"nums": [3, 1, 2]},
            {"nums": [5, 4, 3, 2, 1]},
            {"nums": [3, 5, 2, 4, 1]},
            {"nums": [1, 4, 2, 5, 3, 6]},
            {"nums": [6, 2, 5, 1, 4, 3]},
            {"nums": _perf_74()},
        ],
    },

    # ------------------------------------------------------------------
    # 75 - Resolve Undo-Redo Text Commands
    # ------------------------------------------------------------------
    {
        "slug": "75-resolve-undo-redo-text-commands",
        "title": "Resolve Undo-Redo Text Commands",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Microsoft", "Amazon", "Adobe", "Atlassian"],
        "desc": (
            "You are given an array of command strings `commands` applied sequentially to an initially empty text document with undo/redo history:\n"
            "- `\"TYPE <word>\"`: appends `<word>` (a non-empty lowercase string) to the end of the document, records this action on the undo stack, and **clears the redo stack**.\n"
            "- `\"UNDO\"`: if the undo stack is non-empty, pops the most recent `TYPE` action, removes its appended text from the end of the document, and pushes it onto the redo stack (otherwise does nothing).\n"
            "- `\"REDO\"`: if the redo stack is non-empty, pops the most recent undone action, re-appends its text to the document, and pushes it back onto the undo stack (otherwise does nothing).\n\n"
            "Return the final text document as a single string."
        ),
        "cons": [
            "1 <= commands.length <= 10^4",
            "Each command is 'UNDO', 'REDO', or 'TYPE <word>' where <word> consists of 1 to 20 lowercase English letters."
        ],
        "hints": [
            "Maintain two stacks of strings: `undoStack` holding the currently active typed chunks in order, and `redoStack` holding chunks removed by UNDO.",
            "Remember that any new `TYPE` command must clear `redoStack`, and the final document is simply the concatenation of `undoStack` from bottom to top."
        ],
        "explanations": [
            "Type \"hi\", type \"there\", undo removes \"there\", redo restores \"there\", yielding \"hithere\".",
            "Undo removes \"world\", then typing \"algo\" clears the redo stack, so the subsequent REDO does nothing, leaving \"helloalgo\".",
            "UNDO and REDO on empty stacks are safely ignored, leaving \"ok\"."
        ],
        "time": "O(L)",
        "space": "O(L)",
        "kind": "function",
        "method": "applyUndoRedo",
        "params": [("commands", "String[]")],
        "ret": "String",
        "py": """        undo_stack = []
        redo_stack = []
        for cmd in commands:
            if cmd == "UNDO":
                if undo_stack:
                    redo_stack.append(undo_stack.pop())
            elif cmd == "REDO":
                if redo_stack:
                    undo_stack.append(redo_stack.pop())
            else:
                undo_stack.append(cmd[5:])
                redo_stack.clear()
        return "".join(undo_stack)""",
        "java": """        Deque<String> undo = new ArrayDeque<>();
        Deque<String> redo = new ArrayDeque<>();
        for (String cmd : commands) {
            if (cmd.equals("UNDO")) {
                if (!undo.isEmpty()) redo.push(undo.pop());
            } else if (cmd.equals("REDO")) {
                if (!redo.isEmpty()) undo.push(redo.pop());
            } else {
                undo.push(cmd.substring(5));
                redo.clear();
            }
        }
        StringBuilder sb = new StringBuilder();
        Iterator<String> it = undo.descendingIterator();
        while (it.hasNext()) {
            sb.append(it.next());
        }
        return sb.toString();""",
        "visible": [
            {"commands": ["TYPE hi", "TYPE there", "UNDO", "REDO"]},
            {"commands": ["TYPE hello", "TYPE world", "UNDO", "TYPE algo", "REDO"]},
            {"commands": ["UNDO", "REDO", "TYPE ok", "REDO"]},
        ],
        "hidden": [
            {"commands": ["UNDO"]},
            {"commands": ["REDO"]},
            {"commands": ["TYPE a", "UNDO"]},
            {"commands": ["TYPE a", "TYPE b", "TYPE c", "UNDO", "UNDO", "REDO"]},
            {"commands": ["TYPE x", "TYPE y", "UNDO", "UNDO", "UNDO", "REDO", "REDO", "REDO"]},
            {"commands": ["TYPE ab", "TYPE cd", "UNDO", "TYPE ef", "UNDO", "UNDO", "REDO"]},
            {"commands": ["TYPE one", "TYPE two", "TYPE three", "UNDO", "REDO", "UNDO", "TYPE four"]},
            {"commands": ["TYPE z", "UNDO", "REDO", "UNDO", "REDO", "TYPE end"]},
            {"commands": _perf_75()},
        ],
    },

    # ------------------------------------------------------------------
    # 76 - Design K Stacks in One Array
    # ------------------------------------------------------------------
    {
        "slug": "76-design-k-stacks-in-one-array",
        "title": "Design K Stacks in One Array",
        "difficulty": "Hard",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Design a space-efficient data structure `KStacks` that implements `k` independent LIFO stacks (`0` through `k - 1`) sharing a single fixed-capacity pool of `capacity` slots, with every operation running in `O(1)` time.\n\n"
            "Implement the `KStacks` class:\n"
            "- `KStacks(int k, int capacity)` initializes `k` empty stacks sharing `capacity` total slots.\n"
            "- `boolean push(int stackId, int val)` pushes `val` (`0 <= val <= 10^9`) onto stack `stackId` and returns `true` if a free slot is available; otherwise leaves all stacks unchanged and returns `false`.\n"
            "- `int pop(int stackId)` pops and returns the top element of stack `stackId`, or returns `-1` if stack `stackId` is empty.\n"
            "- `int peek(int stackId)` returns the top element of stack `stackId` without removing it, or returns `-1` if empty.\n"
            "- `int size(int stackId)` returns the current number of elements in stack `stackId`."
        ),
        "cons": [
            "1 <= k <= 1000",
            "1 <= capacity <= 2 * 10^4",
            "0 <= stackId < k and 0 <= val <= 10^9",
            "At most 3 * 10^4 method calls will be made."
        ],
        "hints": [
            "Maintain three flat arrays of length `capacity`: `data` for values, `next` linking both free slots and per-stack chains, plus `top` and `sizes` of length `k` and a `freeHead` pointer.",
            "On `push`, unlink `slot = freeHead`, advance `freeHead = next[slot]`, link `next[slot] = top[stackId]`, and set `top[stackId] = slot`; on `pop`, reverse those exact links to return the slot to the free list in O(1)."
        ],
        "explanations": [
            "With capacity 3 across 2 stacks, pushing 10 and 20 onto stack 0 and 30 onto stack 1 fills the pool; the next push returns false until a pop frees a slot.",
            "Popping and peeking an empty stack return -1, while size returns 0.",
            "Freed slots from stack 0 are immediately reused by stack 2 in O(1)."
        ],
        "time": "O(1) per op",
        "space": "O(capacity + k)",
        "kind": "design",
        "className": "KStacks",
        "ctorParams": [("k", "int"), ("capacity", "int")],
        "methods": [
            ("push", [("stackId", "int"), ("val", "int")], "boolean"),
            ("pop", [("stackId", "int")], "int"),
            ("peek", [("stackId", "int")], "int"),
            ("size", [("stackId", "int")], "int"),
        ],
        "py_class": """class KStacks:
    def __init__(self, k: int, capacity: int):
        self.data = [0] * capacity
        self.nxt = list(range(1, capacity)) + [-1]
        self.top = [-1] * k
        self.sizes = [0] * k
        self.free_head = 0

    def push(self, stackId: int, val: int) -> bool:
        if self.free_head == -1:
            return False
        slot = self.free_head
        self.free_head = self.nxt[slot]
        self.data[slot] = val
        self.nxt[slot] = self.top[stackId]
        self.top[stackId] = slot
        self.sizes[stackId] += 1
        return True

    def pop(self, stackId: int) -> int:
        slot = self.top[stackId]
        if slot == -1:
            return -1
        self.top[stackId] = self.nxt[slot]
        self.nxt[slot] = self.free_head
        self.free_head = slot
        self.sizes[stackId] -= 1
        return self.data[slot]

    def peek(self, stackId: int) -> int:
        slot = self.top[stackId]
        return -1 if slot == -1 else self.data[slot]

    def size(self, stackId: int) -> int:
        return self.sizes[stackId]""",
        "java_class": """class KStacks {
    private final int[] data;
    private final int[] nxt;
    private final int[] top;
    private final int[] sizes;
    private int freeHead;

    public KStacks(int k, int capacity) {
        this.data = new int[capacity];
        this.nxt = new int[capacity];
        for (int i = 0; i < capacity - 1; i++) {
            this.nxt[i] = i + 1;
        }
        this.nxt[capacity - 1] = -1;
        this.top = new int[k];
        Arrays.fill(this.top, -1);
        this.sizes = new int[k];
        this.freeHead = 0;
    }

    public boolean push(int stackId, int val) {
        if (freeHead == -1) return false;
        int slot = freeHead;
        freeHead = nxt[slot];
        data[slot] = val;
        nxt[slot] = top[stackId];
        top[stackId] = slot;
        sizes[stackId]++;
        return true;
    }

    public int pop(int stackId) {
        int slot = top[stackId];
        if (slot == -1) return -1;
        top[stackId] = nxt[slot];
        nxt[slot] = freeHead;
        freeHead = slot;
        sizes[stackId]--;
        return data[slot];
    }

    public int peek(int stackId) {
        int slot = top[stackId];
        return slot == -1 ? -1 : data[slot];
    }

    public int size(int stackId) {
        return sizes[stackId];
    }
}""",
        "visible": [
            {
                "ops": ["KStacks", "push", "push", "push", "push", "pop", "push", "peek", "size"],
                "args": [[2, 3], [0, 10], [0, 20], [1, 30], [1, 40], [0], [1, 40], [1], [1]],
            },
            {
                "ops": ["KStacks", "pop", "peek", "size", "push", "peek", "pop", "pop"],
                "args": [[3, 2], [0], [1], [2], [1, 99], [1], [1], [1]],
            },
            {
                "ops": ["KStacks", "push", "push", "pop", "push", "push", "pop", "pop"],
                "args": [[3, 2], [0, 5], [0, 6], [0], [2, 7], [1, 8], [2], [0]],
            },
        ],
        "hidden": [
            {
                "ops": ["KStacks", "push", "push", "peek", "pop", "push", "pop"],
                "args": [[1, 1], [0, 0], [0, 1], [0], [0], [0, 42], [0]],
            },
            {
                "ops": ["KStacks", "push", "push", "push", "size", "size", "pop", "pop", "pop"],
                "args": [[2, 4], [0, 1], [1, 2], [0, 3], [0], [1], [0], [0], [1]],
            },
            {
                "ops": ["KStacks", "push", "pop", "push", "pop", "push", "pop"],
                "args": [[5, 1], [0, 10], [0], [4, 20], [4], [2, 30], [2]],
            },
            {
                "ops": ["KStacks", "push", "push", "push", "pop", "pop", "push", "push", "peek", "size"],
                "args": [[4, 3], [3, 100], [3, 200], [3, 300], [3], [3], [1, 7], [2, 8], [3], [3]],
            },
            {
                "ops": ["KStacks", "push", "push", "push", "push", "pop", "peek", "pop", "peek"],
                "args": [[3, 5], [0, 1], [1, 2], [2, 3], [0, 4], [0], [0], [0], [0]],
            },
            {
                "ops": ["KStacks", "push", "push", "pop", "push", "pop", "pop", "size", "size"],
                "args": [[2, 2], [0, 1000000000], [1, 0], [1], [0, 500], [0], [0], [0], [1]],
            },
            {
                "ops": ["KStacks", "push", "push", "push", "pop", "push", "pop", "pop", "pop"],
                "args": [[3, 3], [0, 11], [1, 22], [2, 33], [1], [0, 44], [0], [0], [2]],
            },
            {
                "ops": ["KStacks", "push", "push", "push", "push", "size", "pop", "size", "peek"],
                "args": [[2, 3], [1, 9], [1, 8], [1, 7], [0, 6], [0], [1], [1], [1]],
            },
            _perf_76(),
        ],
    },

    # ------------------------------------------------------------------
    # 77 - Call Stack Peak Memory
    # ------------------------------------------------------------------
    {
        "slug": "77-call-stack-peak-memory",
        "title": "Call Stack Peak Memory",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Amazon", "Microsoft", "Apple", "Oracle"],
        "desc": (
            "You are given a valid trace of stack-frame memory `events` executed by a single-threaded program:\n"
            "- `\"CALL <bytes>\"`: pushes a new stack frame initialized with `<bytes>` bytes.\n"
            "- `\"ALLOC <bytes>\"`: allocates `<bytes>` additional bytes owned by the currently active (top) stack frame.\n"
            "- `\"SHRINK <bytes>\"`: frees `min(topFrameBytes, <bytes>)` bytes from the currently active stack frame.\n"
            "- `\"RET\"`: pops the currently active stack frame, immediately releasing all bytes owned by that frame.\n\n"
            "Return the **peak total memory** (in bytes, as a 64-bit integer `long`) held across all active stack frames at any point during execution."
        ),
        "cons": [
            "1 <= events.length <= 10^5",
            "Every byte value is a non-negative integer <= 10^9.",
            "ALLOC, SHRINK, and RET are only called when at least one frame is active."
        ],
        "hints": [
            "Maintain a stack storing the current memory owned by each active frame alongside a running total `curMem` and `peakMem`.",
            "On `SHRINK b`, compute `freed = min(stack[-1], b)` to update both the top frame and `curMem`; on `RET`, pop the top frame and subtract its full memory from `curMem`."
        ],
        "explanations": [
            "CALL 100 -> 100, CALL 50 -> 150, ALLOC 80 -> 230 (peak), RET frees 130 -> 100, RET -> 0.",
            "CALL 10 -> 10, SHRINK 25 reduces frame to 0 -> 0, ALLOC 40 -> 40 (peak), RET -> 0.",
            "First call reaches 70 and returns; second call reaches 90 (peak)."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "peakStackMemory",
        "params": [("events", "String[]")],
        "ret": "long",
        "py": """        stack = []
        cur = 0
        peak = 0
        for ev in events:
            if ev == "RET":
                cur -= stack.pop()
            elif ev[0] == "C":
                val = int(ev[5:])
                stack.append(val)
                cur += val
                if cur > peak:
                    peak = cur
            elif ev[0] == "A":
                val = int(ev[6:])
                stack[-1] += val
                cur += val
                if cur > peak:
                    peak = cur
            else:
                val = int(ev[7:])
                freed = stack[-1] if stack[-1] < val else val
                stack[-1] -= freed
                cur -= freed
        return peak""",
        "java": """        Deque<Long> stack = new ArrayDeque<>();
        long cur = 0L, peak = 0L;
        for (String ev : events) {
            if (ev.equals("RET")) {
                cur -= stack.pop();
            } else if (ev.charAt(0) == 'C') {
                long val = Long.parseLong(ev.substring(5));
                stack.push(val);
                cur += val;
                if (cur > peak) peak = cur;
            } else if (ev.charAt(0) == 'A') {
                long val = Long.parseLong(ev.substring(6));
                long top = stack.pop() + val;
                stack.push(top);
                cur += val;
                if (cur > peak) peak = cur;
            } else {
                long val = Long.parseLong(ev.substring(7));
                long top = stack.pop();
                long freed = Math.min(top, val);
                stack.push(top - freed);
                cur -= freed;
            }
        }
        return peak;""",
        "visible": [
            {"events": ["CALL 100", "CALL 50", "ALLOC 80", "RET", "RET"]},
            {"events": ["CALL 10", "SHRINK 25", "ALLOC 40", "RET"]},
            {"events": ["CALL 30", "ALLOC 40", "RET", "CALL 90", "RET"]},
        ],
        "hidden": [
            {"events": ["CALL 0", "RET"]},
            {"events": ["CALL 1000000000", "ALLOC 1000000000", "CALL 1000000000", "RET"]},
            {"events": ["CALL 50", "CALL 20", "SHRINK 100", "ALLOC 10", "RET", "ALLOC 5"]},
            {"events": ["CALL 10", "CALL 20", "CALL 30", "RET", "CALL 25", "RET", "RET", "RET"]},
            {"events": ["CALL 100", "SHRINK 40", "SHRINK 40", "SHRINK 40", "ALLOC 50"]},
            {"events": ["CALL 5", "ALLOC 5", "CALL 5", "ALLOC 5", "RET", "SHRINK 20", "ALLOC 100"]},
            {"events": ["CALL 1", "CALL 2", "CALL 3", "CALL 4", "CALL 5"]},
            {"events": ["CALL 500", "SHRINK 500", "RET", "CALL 0", "ALLOC 0", "RET"]},
            {"events": _perf_77()},
        ],
    },

    # ------------------------------------------------------------------
    # 78 - Rounds to Make Array Non-Decreasing
    # ------------------------------------------------------------------
    {
        "slug": "78-rounds-to-make-array-non-decreasing",
        "title": "Rounds to Make Array Non-Decreasing",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Meta", "Uber"],
        "desc": (
            "You are given an integer array `nums`. In one round, you simultaneously remove every element `nums[i]` (`i >= 1`) that satisfies `nums[i - 1] > nums[i]`.\n\n"
            "Repeat this process until `nums` becomes non-decreasing (`nums[i - 1] <= nums[i]` for all valid `i`). Return the total number of rounds performed."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "1 <= nums[i] <= 10^9"
        ],
        "hints": [
            "Maintain a stack of `(value, roundsToDie)` pairs scanning left to right, representing surviving barriers to the left.",
            "For each `x`, pop all entries with `value <= x` while tracking `maxRounds = max(maxRounds, popped.rounds)`; if the stack is still non-empty, `x` dies on round `maxRounds + 1`, otherwise `0` (never dies)."
        ],
        "explanations": [
            "Round 1 -> [5,4,4,7,6,11,11], Round 2 -> [5,4,7,11,11], Round 3 -> [5,7,11,11] (non-decreasing), taking 3 rounds.",
            "Already non-decreasing, so 0 rounds are needed.",
            "10 eliminates 1, 2, 3, 4 one per round over 4 rounds."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "totalRounds",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        stack = []
        ans = 0
        for x in nums:
            rounds = 0
            while stack and stack[-1][0] <= x:
                if stack[-1][1] > rounds:
                    rounds = stack[-1][1]
                stack.pop()
            if stack:
                rounds += 1
            else:
                rounds = 0
            if rounds > ans:
                ans = rounds
            stack.append((x, rounds))
        return ans""",
        "java": """        Deque<int[]> stack = new ArrayDeque<>();
        int ans = 0;
        for (int x : nums) {
            int rounds = 0;
            while (!stack.isEmpty() && stack.peek()[0] <= x) {
                rounds = Math.max(rounds, stack.pop()[1]);
            }
            if (!stack.isEmpty()) {
                rounds++;
            } else {
                rounds = 0;
            }
            if (rounds > ans) ans = rounds;
            stack.push(new int[]{x, rounds});
        }
        return ans;""",
        "visible": [
            {"nums": [5, 3, 4, 4, 7, 3, 6, 11, 8, 5, 11]},
            {"nums": [4, 5, 7, 7, 13]},
            {"nums": [10, 1, 2, 3, 4]},
        ],
        "hidden": [
            {"nums": [1]},
            {"nums": [5, 4, 3, 2, 1]},
            {"nums": [7, 14, 4, 14, 13, 2, 6, 13]},
            {"nums": [10, 1, 2, 3, 4, 5, 6, 1, 2, 3]},
            {"nums": [3, 3, 3, 3]},
            {"nums": [2, 1, 2, 1, 2, 1]},
            {"nums": [9, 1, 5, 2, 3, 4, 8, 1, 2]},
            {"nums": [100, 1, 99, 2, 98, 3, 97]},
            {"nums": _perf_78()},
        ],
    },

    # ------------------------------------------------------------------
    # 79 - Balanced Parentheses Rotation Count
    # ------------------------------------------------------------------
    {
        "slug": "79-balanced-parentheses-rotation-count",
        "title": "Balanced Parentheses Rotation Count",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Meta", "Goldman Sachs", "Bloomberg"],
        "desc": (
            "Given a string `s` of length `n` consisting only of `'('` and `')'`, return the number of cyclic left shifts `k` (`0 <= k < n`) such that the rotated string `s[k:] + s[:k]` is a **valid balanced parentheses string**."
        ),
        "cons": [
            "1 <= s.length <= 2 * 10^5",
            "s consists only of '(' and ')'."
        ],
        "hints": [
            "First check that the total balance (`count('(') - count(')')`) is 0; otherwise no rotation can ever be balanced.",
            "Track the prefix balance before each index `k`: a rotation starting at `k` never dips below 0 if and only if `prefixBalance[k]` attains the global minimum prefix balance across `0 <= k < n`."
        ],
        "explanations": [
            "Shifts k=0 and k=2 both produce \"()()\", which is valid; k=1 and k=3 produce \")()(\", which is invalid.",
            "Shifts k=1 and k=3 rotate \")()(\" into \"()()\", giving 2 valid rotations.",
            "Total '(' != total ')', so no cyclic shift can be balanced."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "countBalancedRotations",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        bal = 0
        min_bal = 0
        min_cnt = 0
        for ch in s:
            if bal < min_bal:
                min_bal = bal
                min_cnt = 1
            elif bal == min_bal:
                min_cnt += 1
            bal += 1 if ch == '(' else -1
        return min_cnt if bal == 0 else 0""",
        "java": """        int bal = 0;
        int minBal = 0;
        int minCnt = 0;
        for (int i = 0; i < s.length(); i++) {
            if (bal < minBal) {
                minBal = bal;
                minCnt = 1;
            } else if (bal == minBal) {
                minCnt++;
            }
            bal += (s.charAt(i) == '(') ? 1 : -1;
        }
        return bal == 0 ? minCnt : 0;""",
        "visible": [
            {"s": "()()"},
            {"s": ")()("},
            {"s": ")(("},
        ],
        "hidden": [
            {"s": "("},
            {"s": "()"},
            {"s": ")("},
            {"s": "(()())"},
            {"s": ")))((("},
            {"s": "(()))("},
            {"s": "()()()()"},
            {"s": ")(()())("},
            {"s": _perf_79()},
        ],
    },

    # ------------------------------------------------------------------
    # 80 - Validate Brackets Outside Quotes
    # ------------------------------------------------------------------
    {
        "slug": "80-validate-brackets-outside-quotes",
        "title": "Validate Brackets Outside Quotes",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Microsoft", "Atlassian", "Salesforce"],
        "desc": (
            "Given a code snippet string `s` consisting of brackets `'('`, `')'`, `'['`, `']'`, `'{'`, `'}'`, double quotes `'\"'`, backslashes `'\\\\'`, letters, digits, and spaces, determine whether `s` is structurally valid under string-literal rules:\n"
            "- A double quote `'\"'` outside a string literal opens a string literal, and the next unescaped `'\"'` closes it.\n"
            "- Inside a string literal, all bracket characters are ignored as plain text; a backslash `'\\\\'` escapes the immediately following character (so `'\\\\\"'` does not close the string and `'\\\\\\\\'` is an escaped backslash).\n"
            "- Outside string literals, all brackets `'()'`, `'[]'`, and `'{}'` must be properly matched and nested.\n\n"
            "Return `true` if all string literals are closed and all outside brackets are validly balanced, otherwise `false`."
        ),
        "cons": [
            "0 <= s.length <= 10^5",
            "s contains only printable ASCII characters."
        ],
        "hints": [
            "Combine a boolean state (`inQuote`, `escaped`) with a standard bracket-matching stack.",
            "While `inQuote` is true, consume escaped characters directly and only toggle `inQuote` on an unescaped '\"'; at the end require both `not inQuote` and an empty bracket stack."
        ],
        "explanations": [
            "The unmatched '(' and ']' sit inside the quoted literal and are ignored, while the outer '[' and ']' match.",
            "Inside the string literal, '\\\"' is escaped so the string continues past ')', closes at the next '\"', and the outer '(' matches ')'.",
            "The string literal is never closed (the trailing '\"' is escaped), so return false."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "isValidOutsideQuotes",
        "params": [("s", "String")],
        "ret": "boolean",
        "py": """        match = {')': '(', ']': '[', '}': '{'}
        stack = []
        in_quote = False
        escaped = False
        for ch in s:
            if in_quote:
                if escaped:
                    escaped = False
                elif ch == '\\\\':
                    escaped = True
                elif ch == '"':
                    in_quote = False
            else:
                if ch == '"':
                    in_quote = True
                elif ch in '([{':
                    stack.append(ch)
                elif ch in match:
                    if not stack or stack[-1] != match[ch]:
                        return False
                    stack.pop()
        return (not in_quote) and (not stack)""",
        "java": """        Deque<Character> stack = new ArrayDeque<>();
        boolean inQuote = false;
        boolean escaped = false;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (inQuote) {
                if (escaped) {
                    escaped = false;
                } else if (ch == '\\\\') {
                    escaped = true;
                } else if (ch == '"') {
                    inQuote = false;
                }
            } else {
                if (ch == '"') {
                    inQuote = true;
                } else if (ch == '(' || ch == '[' || ch == '{') {
                    stack.push(ch);
                } else if (ch == ')' || ch == ']' || ch == '}') {
                    char need = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
                    if (stack.isEmpty() || stack.peek() != need) return false;
                    stack.pop();
                }
            }
        }
        return !inQuote && stack.isEmpty();""",
        "visible": [
            {"s": '["(]"]'},
            {"s": '("a\\")b")'},
            {"s": '("hello\\")'},
        ],
        "hidden": [
            {"s": ""},
            {"s": '""'},
            {"s": '({"\\\\"})'},
            {"s": '({"\\\\\\"})'},
            {"s": '([)]'},
            {"s": '"([)]"'},
            {"s": 'a(b"["c)d'},
            {"s": '"{[}"(a["]"]b)'},
            {"s": _perf_80()},
        ],
    },

    # ------------------------------------------------------------------
    # 81 - Reconstruct Parentheses From Depths
    # ------------------------------------------------------------------
    {
        "slug": "81-reconstruct-parentheses-from-depths",
        "title": "Reconstruct Parentheses From Depths",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Amazon", "Bloomberg", "Apple"],
        "desc": (
            "In a valid balanced parentheses string `s`, the nesting depth of each character is defined as follows: scanning left to right with open-count `open` initially `0`, an opening `'('` increments `open` by `1` and has depth `open`; a closing `')'` has depth `open` and then decrements `open` by `1`.\n\n"
            "Given an integer array `depths`, reconstruct and return the unique valid balanced parentheses string `s` whose character depths equal `depths`, or return an empty string `\"\"` if no valid balanced parentheses string has those depths."
        ),
        "cons": [
            "1 <= depths.length <= 10^5",
            "0 <= depths[i] <= 10^5"
        ],
        "hints": [
            "Track the current open count `open` starting at 0: at each position `i`, `'('` uniquely requires `depths[i] == open + 1` while `')'` uniquely requires `depths[i] == open` (with `open > 0`).",
            "If `depths[i]` matches neither `open + 1` nor `open` (when `open > 0`), or if `open != 0` at the end, no valid string exists."
        ],
        "explanations": [
            "Open transitions 0->1('('), 1->2('('), 2->1(')'), 1->0(')') yield depths [1, 2, 2, 1], uniquely giving \"(())\".",
            "Open transitions 0->1, 1->0, 0->1, 1->0 yield depths [1, 1, 1, 1], uniquely giving \"()()\".",
            "Jumping from depth 1 directly to depth 3 is impossible, so return \"\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "reconstructFromDepths",
        "params": [("depths", "int[]")],
        "ret": "String",
        "py": """        out = []
        open_cnt = 0
        for d in depths:
            if d == open_cnt + 1:
                open_cnt += 1
                out.append('(')
            elif open_cnt > 0 and d == open_cnt:
                open_cnt -= 1
                out.append(')')
            else:
                return ""
        return "".join(out) if open_cnt == 0 else \"\"""",
        "java": """        StringBuilder sb = new StringBuilder(depths.length);
        int openCnt = 0;
        for (int d : depths) {
            if (d == openCnt + 1) {
                openCnt++;
                sb.append('(');
            } else if (openCnt > 0 && d == openCnt) {
                openCnt--;
                sb.append(')');
            } else {
                return "";
            }
        }
        return openCnt == 0 ? sb.toString() : "";""",
        "visible": [
            {"depths": [1, 2, 2, 1]},
            {"depths": [1, 1, 1, 1]},
            {"depths": [1, 3, 2, 1]},
        ],
        "hidden": [
            {"depths": [1]},
            {"depths": [0, 0]},
            {"depths": [1, 1]},
            {"depths": [1, 2, 2, 2, 2, 1]},
            {"depths": [1, 2, 3, 3, 2, 1]},
            {"depths": [1, 2, 2]},
            {"depths": [1, 2, 3, 2, 1]},
            {"depths": [1, 2, 2, 1, 1, 2, 3, 3, 2, 1]},
            {"depths": _perf_81()},
        ],
    },

    # ------------------------------------------------------------------
    # 82 - Minimum Replacements to Balance Multi-Brackets
    # ------------------------------------------------------------------
    {
        "slug": "82-minimum-replacements-to-balance-multi-brackets",
        "title": "Minimum Replacements to Balance Multi-Brackets",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Amazon", "Meta", "Microsoft"],
        "desc": (
            "You are given a string `s` consisting of four bracket kinds: `'('`, `')'`, `'['`, `']'`, `'{'`, `'}'`, `'<'`, and `'>'`.\n\n"
            "In one replacement operation, you may replace any opening bracket (`'('`, `'['`, `'{'`, `'<'`) with any other opening bracket, OR replace any closing bracket (`')'`, `']'`, `'}'`, `'>'`) with any other closing bracket. You **cannot** turn an opening bracket into a closing bracket or vice versa.\n\n"
            "Return the **minimum number of replacements** required to make `s` validly balanced, or `-1` if it is impossible."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists only of '(', ')', '[', ']', '{', '}', '<', and '>'."
        ],
        "hints": [
            "Because bracket directions (open vs close) can never change, the string can be balanced if and only if treating all opens as '(' and all closes as ')' forms a valid parentheses string.",
            "Simulate a stack of opening brackets: on each closing bracket, pop the top opening bracket and add 1 to the cost whenever their bracket kinds do not match."
        ],
        "explanations": [
            "'<' matches '>', '[' matches ')', and '{' matches '}'; only the '[' vs ')' pair mismatches, needing 1 replacement.",
            "Every matched pair already has the same kind, needing 0 replacements.",
            "An extra closing bracket occurs when the stack is empty, making balancing impossible (-1)."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "minBracketReplacements",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        match = {')': '(', ']': '[', '}': '{', '>': '<'}
        stack = []
        reps = 0
        for ch in s:
            if ch in '([{<':
                stack.append(ch)
            else:
                if not stack:
                    return -1
                if stack.pop() != match[ch]:
                    reps += 1
        return reps if not stack else -1""",
        "java": """        Deque<Character> stack = new ArrayDeque<>();
        int reps = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{' || ch == '<') {
                stack.push(ch);
            } else {
                if (stack.isEmpty()) return -1;
                char top = stack.pop();
                char need = ch == ')' ? '(' : (ch == ']' ? '[' : (ch == '}' ? '{' : '<'));
                if (top != need) reps++;
            }
        }
        return stack.isEmpty() ? reps : -1;""",
        "visible": [
            {"s": "{[<>)}"},
            {"s": "([]{<>})"},
            {"s": "[{}]]"},
        ],
        "hidden": [
            {"s": "("},
            {"s": ">"},
            {"s": "(]"},
            {"s": "[<(>)]"},
            {"s": "{{[[<<]]}}"},
            {"s": "([{}])<>"},
            {"s": "(([[>>))"},
            {"s": "<{(})>"},
            {"s": _perf_82()},
        ],
    },

    # ------------------------------------------------------------------
    # 83 - Count Ways to Color Balanced Brackets
    # ------------------------------------------------------------------
    {
        "slug": "83-count-ways-to-color-balanced-brackets",
        "title": "Count Ways to Color Balanced Brackets",
        "difficulty": "Hard",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Meta", "Goldman Sachs", "Uber"],
        "desc": (
            "You are given a valid balanced parentheses string `s` consisting of `'('` and `')'`. "
            "You must assign each character `s[i]` a color from `{0, 1, 2}` (`0` = uncolored, `1` = red, `2` = blue) subject to two rules:\n"
            "1. For every matched pair `( ... )`, **exactly one** of its two brackets is colored (`1` or `2`) and the other is uncolored (`0`).\n"
            "2. No two **adjacent** characters `s[i]` and `s[i + 1]` may have the same non-zero color (adjacent `0` and `0` is allowed).\n\n"
            "Return the total number of valid colorings modulo `10^9 + 7`."
        ),
        "cons": [
            "2 <= s.length <= 1000",
            "s is guaranteed to be a valid balanced parentheses string."
        ],
        "hints": [
            "Every balanced string is a forest of irreducible blocks `(inner)`; maintain a 3x3 DP table `dp[leftColor][rightColor]` counting valid colorings of a segment by its first and last bracket colors.",
            "Use a stack of level DP tables: push `None` on `'('`, and on `')'` pop the inner table, wrap it into the 4 valid outer `(cL, cR)` colorings respecting adjacency to the inner endpoints, then merge the resulting block onto the parent level's table."
        ],
        "explanations": [
            "A single pair \"()\" has 4 valid colorings: (0,1), (0,2), (1,0), and (2,0).",
            "In \"(())\", each of the 4 outer colorings forbids exactly 1 of the 4 inner colorings, giving 4 * 3 = 12 ways.",
            "\"(()())\" has 14 inner ways for \"()()\", and each of the 4 outer colorings is compatible with 10 of them, totaling 40 ways."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "countBracketColorings",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        MOD = 10**9 + 7
        VALID_PAIRS = ((0, 1), (0, 2), (1, 0), (2, 0))

        def merge(a, b):
            if a is None:
                return b
            res = [[0] * 3 for _ in range(3)]
            for l1 in range(3):
                for r1 in range(3):
                    va = a[l1][r1]
                    if va == 0:
                        continue
                    for l2 in range(3):
                        if r1 != 0 and r1 == l2:
                            continue
                        for r2 in range(3):
                            vb = b[l2][r2]
                            if vb:
                                res[l1][r2] = (res[l1][r2] + va * vb) % MOD
            return res

        frames = [None]
        for ch in s:
            if ch == '(':
                frames.append(None)
            else:
                inner = frames.pop()
                block = [[0] * 3 for _ in range(3)]
                if inner is None:
                    for cl, cr in VALID_PAIRS:
                        block[cl][cr] = 1
                else:
                    for cl, cr in VALID_PAIRS:
                        tot = 0
                        for a in range(3):
                            if cl != 0 and cl == a:
                                continue
                            for b in range(3):
                                if cr != 0 and cr == b:
                                    continue
                                tot += inner[a][b]
                        block[cl][cr] = tot % MOD
                frames[-1] = merge(frames[-1], block)

        root = frames[0]
        ans = 0
        for r in root:
            for v in r:
                ans = (ans + v) % MOD
        return ans""",
        "java": """        final long MOD = 1_000_000_007L;
        int[][] validPairs = {{0, 1}, {0, 2}, {1, 0}, {2, 0}};
        List<long[][]> frames = new ArrayList<>();
        frames.add(null);
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                frames.add(null);
            } else {
                long[][] inner = frames.remove(frames.size() - 1);
                long[][] block = new long[3][3];
                if (inner == null) {
                    for (int[] p : validPairs) block[p[0]][p[1]] = 1L;
                } else {
                    for (int[] p : validPairs) {
                        int cl = p[0], cr = p[1];
                        long tot = 0;
                        for (int a = 0; a < 3; a++) {
                            if (cl != 0 && cl == a) continue;
                            for (int b = 0; b < 3; b++) {
                                if (cr != 0 && cr == b) continue;
                                tot += inner[a][b];
                            }
                        }
                        block[cl][cr] = tot % MOD;
                    }
                }
                int topIdx = frames.size() - 1;
                frames.set(topIdx, mergeTables(frames.get(topIdx), block, MOD));
            }
        }
        long[][] root = frames.get(0);
        long ans = 0;
        for (int i = 0; i < 3; i++) {
            for (int j = 0; j < 3; j++) {
                ans = (ans + root[i][j]) % MOD;
            }
        }
        return (int) ans;""",
        "java_helpers": """    private long[][] mergeTables(long[][] a, long[][] b, long MOD) {
        if (a == null) return b;
        long[][] res = new long[3][3];
        for (int l1 = 0; l1 < 3; l1++) {
            for (int r1 = 0; r1 < 3; r1++) {
                long va = a[l1][r1];
                if (va == 0) continue;
                for (int l2 = 0; l2 < 3; l2++) {
                    if (r1 != 0 && r1 == l2) continue;
                    for (int r2 = 0; r2 < 3; r2++) {
                        long vb = b[l2][r2];
                        if (vb != 0) {
                            res[l1][r2] = (res[l1][r2] + va * vb) % MOD;
                        }
                    }
                }
            }
        }
        return res;
    }""",
        "visible": [
            {"s": "()"},
            {"s": "(())"},
            {"s": "(()())"},
        ],
        "hidden": [
            {"s": "()()"},
            {"s": "((()))"},
            {"s": "()()()"},
            {"s": "((())())"},
            {"s": "(()(()))"},
            {"s": "()(()())()"},
            {"s": "(((())))"},
            {"s": "((()())(()()))"},
            {"s": _perf_83()},
        ],
    },

    # ------------------------------------------------------------------
    # 84 - Count Single Flips to Balance Parentheses
    # ------------------------------------------------------------------
    {
        "slug": "84-count-single-flips-to-balance-parentheses",
        "title": "Count Single Flips to Balance Parentheses",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Amazon", "Meta", "Bloomberg"],
        "desc": (
            "Given a string `s` of length `n` consisting of `'('` and `')'`, return the number of indices `i` (`0 <= i < n`) such that flipping `s[i]` (changing `'('` to `')'` or `')'` to `'('`) transforms `s` into a **valid balanced parentheses string**."
        ),
        "cons": [
            "1 <= s.length <= 2 * 10^5",
            "s consists only of '(' and ')'."
        ],
        "hints": [
            "Flipping one character changes the total balance by -2 (for '(' -> ')') or +2 (for ')' -> '('), so a valid flip can only exist when the initial total balance is +2 or -2.",
            "Precompute prefix balance `pref[i]`, prefix minimum `prefMin[i]`, and suffix minimum `sufMin[i]`: flipping index `i` keeps every prefix non-negative iff `prefMin[i - 1] >= 0` and `sufMin[i] >= 2` (when total == +2) or `sufMin[i] >= -2` (when total == -2)."
        ],
        "explanations": [
            "Flipping index 1 produces \"()()\" and flipping index 2 produces \"(())\", giving 2 valid indices.",
            "Flipping index 1 produces \"(()())\" and flipping index 2 produces \"()(())\", giving 2 valid indices.",
            "Already balanced (total balance 0), so any single flip makes it unbalanced (0 valid indices)."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "countSingleFlips",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        n = len(s)
        pref = [0] * n
        cur = 0
        for i, ch in enumerate(s):
            cur += 1 if ch == '(' else -1
            pref[i] = cur
        total = cur
        if total != 2 and total != -2:
            return 0
        suf_min = [0] * n
        suf_min[-1] = pref[-1]
        for i in range(n - 2, -1, -1):
            suf_min[i] = pref[i] if pref[i] < suf_min[i + 1] else suf_min[i + 1]
        target_ch = '(' if total == 2 else ')'
        need_suf = 2 if total == 2 else -2
        ans = 0
        pref_min = 0
        for i in range(n):
            if pref_min >= 0 and s[i] == target_ch and suf_min[i] >= need_suf:
                ans += 1
            if pref[i] < pref_min:
                pref_min = pref[i]
        return ans""",
        "java": """        int n = s.length();
        int[] pref = new int[n];
        int cur = 0;
        for (int i = 0; i < n; i++) {
            cur += (s.charAt(i) == '(') ? 1 : -1;
            pref[i] = cur;
        }
        if (cur != 2 && cur != -2) return 0;
        int[] sufMin = new int[n];
        sufMin[n - 1] = pref[n - 1];
        for (int i = n - 2; i >= 0; i--) {
            sufMin[i] = Math.min(pref[i], sufMin[i + 1]);
        }
        char target = (cur == 2) ? '(' : ')';
        int needSuf = (cur == 2) ? 2 : -2;
        int ans = 0;
        int prefMin = 0;
        for (int i = 0; i < n; i++) {
            if (prefMin >= 0 && s.charAt(i) == target && sufMin[i] >= needSuf) {
                ans++;
            }
            if (pref[i] < prefMin) prefMin = pref[i];
        }
        return ans;""",
        "visible": [
            {"s": "((()"},
            {"s": "())())"},
            {"s": "()(())"},
        ],
        "hidden": [
            {"s": "("},
            {"s": "(("},
            {"s": "))"},
            {"s": ")(("},
            {"s": "()((()"},
            {"s": "))(("},
            {"s": "(()(()"},
            {"s": ")(())("},
            {"s": _perf_84()},
        ],
    },

    # ------------------------------------------------------------------
    # 85 - Maximum Balanced Length From Bracket Fragments
    # ------------------------------------------------------------------
    {
        "slug": "85-maximum-balanced-length-from-bracket-fragments",
        "title": "Maximum Balanced Length From Bracket Fragments",
        "difficulty": "Hard",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Meta", "Amazon", "Goldman Sachs"],
        "desc": (
            "You are given an array of non-empty bracket strings `fragments`, each consisting of `'('` and `')'`. "
            "You may arrange and concatenate **all** strings in `fragments` in any order you choose (using each fragment exactly once).\n\n"
            "Return the **maximum possible length** of a valid balanced parentheses **subsequence** contained in the concatenated string."
        ),
        "cons": [
            "1 <= fragments.length <= 2 * 10^4",
            "1 <= fragments[i].length <= 10^4",
            "The sum of lengths of all strings in fragments does not exceed 10^5."
        ],
        "hints": [
            "First reduce every fragment with a stack: each internal matched pair adds 2 to the answer, leaving `c` unmatched ')' followed by `o` unmatched '('.",
            "Order the reduced `(c, o)` fragments using Johnson's rule: place all fragments with `o >= c` first sorted by `c` ascending, then all fragments with `o < c` sorted by `o` descending, and greedily match cross-fragment pairs."
        ],
        "explanations": [
            "Arranging as \"((\" + \")(\" + \"))\" forms \"(()())\", which is completely balanced of length 6.",
            "\"()\" contributes 2 internal chars; placing \")(\" before \")\" matches 1 extra pair across them for total length 4.",
            "\"(()\" + \"))\" matches 2 pairs total (1 internal + 1 cross-fragment) for length 4."
        ],
        "time": "O(L + m log m)",
        "space": "O(m)",
        "kind": "function",
        "method": "maxBalancedLength",
        "params": [("fragments", "String[]")],
        "ret": "int",
        "py": """        base_pairs = 0
        pos_group = []  # (c, o) with o >= c
        neg_group = []  # (c, o) with o < c
        for f in fragments:
            o = 0
            c = 0
            for ch in f:
                if ch == '(':
                    o += 1
                elif o > 0:
                    o -= 1
                    base_pairs += 1
                else:
                    c += 1
            if o >= c:
                pos_group.append((c, o))
            else:
                neg_group.append((c, o))
        pos_group.sort(key=lambda x: x[0])
        neg_group.sort(key=lambda x: -x[1])
        avail = 0
        cross_pairs = 0
        for c, o in pos_group + neg_group:
            m = avail if avail < c else c
            cross_pairs += m
            avail = avail - m + o
        return 2 * (base_pairs + cross_pairs)""",
        "java": """        int basePairs = 0;
        List<int[]> posGroup = new ArrayList<>();
        List<int[]> negGroup = new ArrayList<>();
        for (String f : fragments) {
            int o = 0, c = 0;
            for (int i = 0; i < f.length(); i++) {
                if (f.charAt(i) == '(') {
                    o++;
                } else if (o > 0) {
                    o--;
                    basePairs++;
                } else {
                    c++;
                }
            }
            if (o >= c) posGroup.add(new int[]{c, o});
            else negGroup.add(new int[]{c, o});
        }
        posGroup.sort((a, b) -> Integer.compare(a[0], b[0]));
        negGroup.sort((a, b) -> Integer.compare(b[1], a[1]));
        int avail = 0;
        int crossPairs = 0;
        for (int[] p : posGroup) {
            int m = Math.min(avail, p[0]);
            crossPairs += m;
            avail = avail - m + p[1];
        }
        for (int[] p : negGroup) {
            int m = Math.min(avail, p[0]);
            crossPairs += m;
            avail = avail - m + p[1];
        }
        return 2 * (basePairs + crossPairs);""",
        "visible": [
            {"fragments": [")(", "((", "))"]},
            {"fragments": ["()", ")(", ")"]},
            {"fragments": ["))", "(()"]},
        ],
        "hidden": [
            {"fragments": ["("]},
            {"fragments": [")"]},
            {"fragments": ["()", "()"]},
            {"fragments": [")))((", "))(((", ")(("]},
            {"fragments": [")(((", ")))", ")("]},
            {"fragments": ["(((", ")))", "))((", "()()"]},
            {"fragments": [")))))(", "(((()", "))(("]},
            {"fragments": ["))(", ")((", "))(((", "((())"]},
            {"fragments": _perf_85()},
        ],
    },

    # ------------------------------------------------------------------
    # 86 - Infix to Prefix Conversion
    # ------------------------------------------------------------------
    {
        "slug": "86-infix-to-prefix-conversion",
        "title": "Infix to Prefix Conversion",
        "difficulty": "Easy",
        "subtopic": "Expression Parsing",
        "companies": ["Amazon", "Microsoft", "Oracle", "Adobe"],
        "desc": (
            "Given a valid infix expression string `s` consisting of single lowercase letter operands (`'a'`-`'z'`), binary operators `'+'`, `'-'`, `'*'`, `'/'`, parentheses `'('` and `')'`, and optional spaces, convert `s` into its equivalent **Prefix (Polish) Notation** string with no spaces.\n\n"
            "Standard precedence and associativity apply: `'*'` and `'/'` have higher precedence than `'+'` and `'-'`, and all four binary operators are **left-associative**."
        ),
        "cons": [
            "1 <= s.length <= 2 * 10^4",
            "s is a valid infix expression containing lowercase letters 'a'-'z', '+', '-', '*', '/', '(', ')', and ' '."
        ],
        "hints": [
            "Scan `s` from right to left, treating ')' as an opening parenthesis and '(' as a closing parenthesis.",
            "Because scanning right-to-left flips left-associativity into right-associativity, pop operators from the stack only when their precedence is **strictly greater** than the current operator's precedence, then reverse the collected output."
        ],
        "explanations": [
            "(a + b) * c has root '*' with left subtree '+ab' and right 'c', yielding \"*+abc\".",
            "Left-associative a - b - c parses as (a - b) - c, yielding \"--abc\".",
            "a + b * c - d parses as (a + (b * c)) - d, yielding \"-+a*bcd\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "infixToPrefix",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        prec = {'+': 1, '-': 1, '*': 2, '/': 2}
        ops = []
        out = []
        for ch in reversed(s):
            if ch == ' ':
                continue
            if 'a' <= ch <= 'z':
                out.append(ch)
            elif ch == ')':
                ops.append(ch)
            elif ch == '(':
                while ops and ops[-1] != ')':
                    out.append(ops.pop())
                ops.pop()
            else:
                p = prec[ch]
                while ops and ops[-1] != ')' and prec[ops[-1]] > p:
                    out.append(ops.pop())
                ops.append(ch)
        while ops:
            out.append(ops.pop())
        out.reverse()
        return "".join(out)""",
        "java": """        Deque<Character> ops = new ArrayDeque<>();
        StringBuilder out = new StringBuilder();
        for (int i = s.length() - 1; i >= 0; i--) {
            char ch = s.charAt(i);
            if (ch == ' ') continue;
            if (ch >= 'a' && ch <= 'z') {
                out.append(ch);
            } else if (ch == ')') {
                ops.push(ch);
            } else if (ch == '(') {
                while (!ops.isEmpty() && ops.peek() != ')') {
                    out.append(ops.pop());
                }
                ops.pop();
            } else {
                int p = (ch == '*' || ch == '/') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != ')') {
                    char top = ops.peek();
                    int tp = (top == '*' || top == '/') ? 2 : 1;
                    if (tp > p) out.append(ops.pop());
                    else break;
                }
                ops.push(ch);
            }
        }
        while (!ops.isEmpty()) {
            out.append(ops.pop());
        }
        return out.reverse().toString();""",
        "visible": [
            {"s": "(a + b) * c"},
            {"s": "a - b - c"},
            {"s": "a + b * c - d"},
        ],
        "hidden": [
            {"s": "x"},
            {"s": "((a))"},
            {"s": "a * b / c"},
            {"s": "a - (b - c)"},
            {"s": "(a + b) * (c - d)"},
            {"s": "a + b + c + d"},
            {"s": "a * (b + c * (d - e)) / f"},
            {"s": "((a / b) + (c * d)) - e"},
            {"s": _perf_86()},
        ],
    },

    # ------------------------------------------------------------------
    # 87 - Evaluate Boolean Infix Expression
    # ------------------------------------------------------------------
    {
        "slug": "87-evaluate-boolean-infix-expression",
        "title": "Evaluate Boolean Infix Expression",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Given a valid infix boolean expression string `expr` containing boolean literals `'T'` (`true`) and `'F'` (`false`), operators `'!'` (unary NOT), `'&'` (AND), `'^'` (XOR), `'|'` (OR), parentheses `'('` and `')'`, and optional spaces, evaluate `expr` and return its boolean result.\n\n"
            "Operator precedence (from highest to lowest):\n"
            "1. `'!'` (unary prefix NOT, right-associative so `!!T == T`)\n"
            "2. `'&'` (logical AND, left-associative)\n"
            "3. `'^'` (logical XOR, left-associative)\n"
            "4. `'|'` (logical OR, left-associative)"
        ),
        "cons": [
            "1 <= expr.length <= 2 * 10^4",
            "expr is a syntactically valid infix boolean expression containing 'T', 'F', '!', '&', '^', '|', '(', ')', and ' '."
        ],
        "hints": [
            "Use Shunting-Yard with a boolean value stack and an operator stack with precedences {'|': 1, '^': 2, '&': 3, '!': 4}.",
            "Because unary '!' is right-associative with the highest precedence, push '!' directly onto the operator stack; for binary operators, evaluate while the top operator has precedence >= current, popping 1 value for '!' and 2 values for binary ops."
        ],
        "explanations": [
            "'!' has highest precedence (!F = T), then '&' (T & T = T), then '|' (T | F = T).",
            "Inside parentheses T & !F = T & T = T, then !!T = T.",
            "'&' binds tighter than '^' and '|': T & F = F, then T ^ F = T, then F | T = T."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "evalBooleanInfix",
        "params": [("expr", "String")],
        "ret": "boolean",
        "py": """        prec = {'|': 1, '^': 2, '&': 3, '!': 4}
        vals = []
        ops = []

        def apply_top():
            op = ops.pop()
            if op == '!':
                vals.append(not vals.pop())
            else:
                b = vals.pop()
                a = vals.pop()
                if op == '&':
                    vals.append(a and b)
                elif op == '|':
                    vals.append(a or b)
                else:
                    vals.append(a != b)

        for ch in expr:
            if ch == ' ':
                continue
            if ch == 'T':
                vals.append(True)
            elif ch == 'F':
                vals.append(False)
            elif ch == '(' or ch == '!':
                ops.append(ch)
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_top()
                ops.pop()
            else:
                p = prec[ch]
                while ops and ops[-1] != '(' and prec[ops[-1]] >= p:
                    apply_top()
                ops.append(ch)
        while ops:
            apply_top()
        return vals[-1]""",
        "java": """        Deque<Boolean> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        for (int i = 0; i < expr.length(); i++) {
            char ch = expr.charAt(i);
            if (ch == ' ') continue;
            if (ch == 'T') {
                vals.push(true);
            } else if (ch == 'F') {
                vals.push(false);
            } else if (ch == '(' || ch == '!') {
                ops.push(ch);
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyOp(vals, ops);
                }
                ops.pop();
            } else {
                int p = prec(ch);
                while (!ops.isEmpty() && ops.peek() != '(' && prec(ops.peek()) >= p) {
                    applyOp(vals, ops);
                }
                ops.push(ch);
            }
        }
        while (!ops.isEmpty()) {
            applyOp(vals, ops);
        }
        return vals.peek();""",
        "java_helpers": """    private int prec(char op) {
        if (op == '|') return 1;
        if (op == '^') return 2;
        if (op == '&') return 3;
        if (op == '!') return 4;
        return 0;
    }

    private void applyOp(Deque<Boolean> vals, Deque<Character> ops) {
        char op = ops.pop();
        if (op == '!') {
            vals.push(!vals.pop());
        } else {
            boolean b = vals.pop();
            boolean a = vals.pop();
            if (op == '&') vals.push(a && b);
            else if (op == '|') vals.push(a || b);
            else vals.push(a ^ b);
        }
    }""",
        "visible": [
            {"expr": "!F & T | F"},
            {"expr": "!!(T & !F)"},
            {"expr": "F | T ^ T & F"},
        ],
        "hidden": [
            {"expr": "T"},
            {"expr": "F"},
            {"expr": "!!!T"},
            {"expr": "T ^ T ^ T"},
            {"expr": "!(T | F) & T"},
            {"expr": "(T | F) & !(T ^ F)"},
            {"expr": "F & T | !F ^ T"},
            {"expr": "!(!T | !F) ^ (T & !F)"},
            {"expr": _perf_87()},
        ],
    },

    # ------------------------------------------------------------------
    # 88 - Postfix Expression Peak Stack Depth
    # ------------------------------------------------------------------
    {
        "slug": "88-postfix-expression-peak-stack-depth",
        "title": "Postfix Expression Peak Stack Depth",
        "difficulty": "Easy",
        "subtopic": "Expression Parsing",
        "companies": ["Amazon", "Microsoft", "LinkedIn", "Apple"],
        "desc": (
            "You are given an array of string `tokens` representing a candidate expression in **Postfix (Reverse Polish) Notation** containing:\n"
            "- Integer operands (e.g., `\"42\"`, `\"-7\"`): push 1 value onto the operand stack.\n"
            "- Unary operators (`\"neg\"`, `\"abs\"`): pop 1 value and push 1 result (requires stack height `>= 1`).\n"
            "- Binary operators (`\"+\"`, `\"-\"`, `\"*\"`, `\"/\"`): pop 2 values and push 1 result (requires stack height `>= 2`).\n\n"
            "The expression is valid if no operator ever causes a stack underflow and the final stack height after processing all tokens is **exactly `1`**. "
            "Return the **maximum stack height** reached at any point during evaluation if valid, or `-1` if invalid."
        ),
        "cons": [
            "1 <= tokens.length <= 10^5",
            "Each token is 'neg', 'abs', '+', '-', '*', '/', or a valid 32-bit integer string."
        ],
        "hints": [
            "You do not need to store actual numeric values — only track the integer stack height `h` and its peak `peak`.",
            "Increment `h` on operands, check `h >= 1` for unary ops (leaving `h` unchanged), check `h >= 2` and decrement `h` for binary ops, and verify `h == 1` at the end."
        ],
        "explanations": [
            "Heights: 2(1), 1(2), +(1), 3(2), *(1) -> valid with peak height 2.",
            "Heights: 4(1), 13(2), 5(3), /(2), +(1), abs(1) -> valid with peak height 3.",
            "Binary '+' arrives when stack height is 1, causing an underflow -> return -1."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "postfixPeakDepth",
        "params": [("tokens", "String[]")],
        "ret": "int",
        "py": """        h = 0
        peak = 0
        for tok in tokens:
            if tok == "neg" or tok == "abs":
                if h < 1:
                    return -1
            elif tok in ("+", "-", "*", "/"):
                if h < 2:
                    return -1
                h -= 1
            else:
                h += 1
                if h > peak:
                    peak = h
        return peak if h == 1 else -1""",
        "java": """        int h = 0, peak = 0;
        for (String tok : tokens) {
            if (tok.equals("neg") || tok.equals("abs")) {
                if (h < 1) return -1;
            } else if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/")) {
                if (h < 2) return -1;
                h--;
            } else {
                h++;
                if (h > peak) peak = h;
            }
        }
        return h == 1 ? peak : -1;""",
        "visible": [
            {"tokens": ["2", "1", "+", "3", "*"]},
            {"tokens": ["4", "13", "5", "/", "+", "abs"]},
            {"tokens": ["5", "+", "2"]},
        ],
        "hidden": [
            {"tokens": ["7"]},
            {"tokens": ["neg"]},
            {"tokens": ["3", "4"]},
            {"tokens": ["1", "2", "3", "4", "+", "+", "+"]},
            {"tokens": ["-5", "neg", "abs", "2", "*"]},
            {"tokens": ["1", "2", "+", "+"]},
            {"tokens": ["1", "2", "3", "+", "neg", "4", "*", "-"]},
            {"tokens": ["10", "20", "30", "40", "*", "abs", "/", "-"]},
            {"tokens": _perf_88()},
        ],
    },

    # ------------------------------------------------------------------
    # 89 - Expand Polynomial Expression
    # ------------------------------------------------------------------
    {
        "slug": "89-expand-polynomial-expression",
        "title": "Expand Polynomial Expression",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Meta", "Amazon", "Salesforce"],
        "desc": (
            "Given a valid mathematical expression string `expr` over a single variable `'x'`, consisting of non-negative integers, `'x'`, binary operators `'+'`, `'-'`, `'*'`, parentheses `'('` and `')'`, and optional spaces, expand and simplify `expr` into a canonical polynomial.\n\n"
            "Return a 64-bit integer array (`long[]`) of coefficients `[c_0, c_1, ..., c_d]` where `c_i` is the coefficient of `x^i`, with **no trailing zeros** (except returning `[0]` if the polynomial simplifies identically to `0`). "
            "Standard precedence applies (`'*'` > `'+'`, `'-'`, all left-associative)."
        ),
        "cons": [
            "1 <= expr.length <= 2000",
            "expr contains digits, 'x', '+', '-', '*', '(', ')', and ' ' (no implicit multiplication like '2x'; multiplication is always written '2 * x').",
            "The degree of every intermediate polynomial is at most 15 and all intermediate/final coefficients fit in a 64-bit signed integer."
        ],
        "hints": [
            "Run two-stack Shunting-Yard where each entry on the operand stack is a polynomial coefficient list (`c` -> `[c]`, `'x'` -> `[0, 1]`).",
            "Implement helper operations for polynomial addition, subtraction, and convolution multiplication, trimming trailing zeros after every operation while keeping at least `[0]`."
        ],
        "explanations": [
            "(x + 1) * (x + 2) = 2 + 3x + x^2, whose coefficient array is [2, 3, 1].",
            "(x - 1) * (x + 1) - x * x = (x^2 - 1) - x^2 = -1, giving [-1].",
            "2 * (x + 3) - 2 * x - 6 simplifies identically to 0, giving [0]."
        ],
        "time": "O(n * D^2)",
        "space": "O(n * D)",
        "kind": "function",
        "method": "expandPolynomial",
        "params": [("expr", "String")],
        "ret": "long[]",
        "py": """        def trim(p):
            while len(p) > 1 and p[-1] == 0:
                p.pop()
            return p

        def apply_op(vals, ops):
            op = ops.pop()
            b = vals.pop()
            a = vals.pop()
            if op == '+' or op == '-':
                sign = 1 if op == '+' else -1
                m = max(len(a), len(b))
                res = [0] * m
                for k in range(m):
                    va = a[k] if k < len(a) else 0
                    vb = b[k] if k < len(b) else 0
                    res[k] = va + sign * vb
                vals.append(trim(res))
            else:
                res = [0] * (len(a) + len(b) - 1)
                for i, va in enumerate(a):
                    if va == 0:
                        continue
                    for j, vb in enumerate(b):
                        res[i + j] += va * vb
                vals.append(trim(res))

        prec = {'+': 1, '-': 1, '*': 2}
        vals = []
        ops = []
        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch == ' ':
                i += 1
            elif ch == 'x':
                vals.append([0, 1])
                i += 1
            elif '0' <= ch <= '9':
                num = 0
                while i < n and '0' <= expr[i] <= '9':
                    num = num * 10 + (ord(expr[i]) - 48)
                    i += 1
                vals.append([num])
            elif ch == '(':
                ops.append(ch)
                i += 1
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_op(vals, ops)
                ops.pop()
                i += 1
            else:
                p = prec[ch]
                while ops and ops[-1] != '(' and prec[ops[-1]] >= p:
                    apply_op(vals, ops)
                ops.append(ch)
                i += 1
        while ops:
            apply_op(vals, ops)
        return vals[-1]""",
        "java": """        Deque<long[]> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = expr.length();
        while (i < n) {
            char ch = expr.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch == 'x') {
                vals.push(new long[]{0L, 1L});
                i++;
            } else if (ch >= '0' && ch <= '9') {
                long num = 0;
                while (i < n && expr.charAt(i) >= '0' && expr.charAt(i) <= '9') {
                    num = num * 10 + (expr.charAt(i) - '0');
                    i++;
                }
                vals.push(new long[]{num});
            } else if (ch == '(') {
                ops.push(ch);
                i++;
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyOp(vals, ops);
                }
                ops.pop();
                i++;
            } else {
                int p = (ch == '*') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != '(' && ((ops.peek() == '*') ? 2 : 1) >= p) {
                    applyOp(vals, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyOp(vals, ops);
        }
        return vals.peek();""",
        "java_helpers": """    private long[] trim(long[] p) {
        int end = p.length - 1;
        while (end > 0 && p[end] == 0L) end--;
        return Arrays.copyOf(p, end + 1);
    }

    private void applyOp(Deque<long[]> vals, Deque<Character> ops) {
        char op = ops.pop();
        long[] b = vals.pop();
        long[] a = vals.pop();
        if (op == '+' || op == '-') {
            long sign = (op == '+') ? 1L : -1L;
            int m = Math.max(a.length, b.length);
            long[] res = new long[m];
            for (int k = 0; k < m; k++) {
                long va = k < a.length ? a[k] : 0L;
                long vb = k < b.length ? b[k] : 0L;
                res[k] = va + sign * vb;
            }
            vals.push(trim(res));
        } else {
            long[] res = new long[a.length + b.length - 1];
            for (int i = 0; i < a.length; i++) {
                if (a[i] == 0L) continue;
                for (int j = 0; j < b.length; j++) {
                    res[i + j] += a[i] * b[j];
                }
            }
            vals.push(trim(res));
        }
    }""",
        "visible": [
            {"expr": "(x + 1) * (x + 2)"},
            {"expr": "(x - 1) * (x + 1) - x * x"},
            {"expr": "2 * (x + 3) - 2 * x - 6"},
        ],
        "hidden": [
            {"expr": "0"},
            {"expr": "x"},
            {"expr": "(x + 1) * (x + 1) * (x + 1)"},
            {"expr": "0 * (x * x + 5 * x + 9)"},
            {"expr": "3 * x * x - (x + 2) * (2 * x - 1)"},
            {"expr": "(2 * x - 3) * (2 * x - 3) - 4 * x * x + 12 * x"},
            {"expr": "(x + 2) * (x - 2) * (x * x + 4)"},
            {"expr": "5 - (3 - (x - 1))"},
            {"expr": _perf_89()},
        ],
    },

    # ------------------------------------------------------------------
    # 90 - Evaluate Set Expression
    # ------------------------------------------------------------------
    {
        "slug": "90-evaluate-set-expression",
        "title": "Evaluate Set Expression",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Amazon", "Meta", "Oracle"],
        "desc": (
            "Given a valid set-algebra expression string `expr` composed of finite integer set literals (e.g., `{1, 2, -3}` or `{}`), binary set operators, parentheses `'('` and `')'`, and optional spaces, evaluate `expr` and return the resulting set as a **strictly ascending `int[]`**.\n\n"
            "Operators and precedence:\n"
            "- `'&'` (intersection): precedence `2` (highest), left-associative.\n"
            "- `'|'` (union), `'-'` (set difference `A \\ B`), `'^'` (symmetric difference): precedence `1`, left-associative."
        ),
        "cons": [
            "2 <= expr.length <= 10^4",
            "Set literals contain comma-separated signed 32-bit integers (with optional spaces) inside '{' and '}'.",
            "expr is a valid set expression."
        ],
        "hints": [
            "Parse each `{...}` literal into a hash set of integers and push it onto the operand stack; be careful not to confuse a negative sign inside `{...}` with the set-difference operator '-'.",
            "Use Shunting-Yard with `'&'` having precedence 2 and `'|'`, `'-'`, `'^'` having precedence 1 (all left-associative), then sort the final set."
        ],
        "explanations": [
            "'&' has higher precedence: {2,3,4} & {3,4,5} = {3,4}, then {1,2,3} | {3,4} = [1, 2, 3, 4].",
            "({1,2,3} | {4}) = {1,2,3,4}; removing {2,4} leaves [1, 3].",
            "Symmetric difference of {1,2} and {2,3} contains elements in exactly one set: [1, 3]."
        ],
        "time": "O(n + S log S)",
        "space": "O(n + S)",
        "kind": "function",
        "method": "evalSetExpression",
        "params": [("expr", "String")],
        "ret": "int[]",
        "py": """        prec = {'|': 1, '-': 1, '^': 1, '&': 2}
        vals = []
        ops = []

        def apply_top():
            op = ops.pop()
            b = vals.pop()
            a = vals.pop()
            if op == '&':
                vals.append(a & b)
            elif op == '|':
                vals.append(a | b)
            elif op == '-':
                vals.append(a - b)
            else:
                vals.append(a ^ b)

        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch == ' ':
                i += 1
            elif ch == '{':
                j = expr.index('}', i)
                inner = expr[i + 1:j].strip()
                s = set()
                if inner:
                    for part in inner.split(','):
                        s.add(int(part.strip()))
                vals.append(s)
                i = j + 1
            elif ch == '(':
                ops.append(ch)
                i += 1
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_top()
                ops.pop()
                i += 1
            else:
                p = prec[ch]
                while ops and ops[-1] != '(' and prec[ops[-1]] >= p:
                    apply_top()
                ops.append(ch)
                i += 1
        while ops:
            apply_top()
        return sorted(vals[-1])""",
        "java": """        Deque<Set<Integer>> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = expr.length();
        while (i < n) {
            char ch = expr.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch == '{') {
                int j = expr.indexOf('}', i);
                String inner = expr.substring(i + 1, j).trim();
                Set<Integer> s = new HashSet<>();
                if (!inner.isEmpty()) {
                    for (String part : inner.split(",")) {
                        s.add(Integer.parseInt(part.trim()));
                    }
                }
                vals.push(s);
                i = j + 1;
            } else if (ch == '(') {
                ops.push(ch);
                i++;
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyOp(vals, ops);
                }
                ops.pop();
                i++;
            } else {
                int p = (ch == '&') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != '(' && ((ops.peek() == '&') ? 2 : 1) >= p) {
                    applyOp(vals, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyOp(vals, ops);
        }
        Set<Integer> resSet = vals.peek();
        int[] ans = new int[resSet.size()];
        int idx = 0;
        for (int v : resSet) ans[idx++] = v;
        Arrays.sort(ans);
        return ans;""",
        "java_helpers": """    private void applyOp(Deque<Set<Integer>> vals, Deque<Character> ops) {
        char op = ops.pop();
        Set<Integer> b = vals.pop();
        Set<Integer> a = vals.pop();
        Set<Integer> res = new HashSet<>();
        if (op == '&') {
            for (int v : a) if (b.contains(v)) res.add(v);
        } else if (op == '|') {
            res.addAll(a);
            res.addAll(b);
        } else if (op == '-') {
            for (int v : a) if (!b.contains(v)) res.add(v);
        } else {
            for (int v : a) if (!b.contains(v)) res.add(v);
            for (int v : b) if (!a.contains(v)) res.add(v);
        }
        vals.push(res);
    }""",
        "visible": [
            {"expr": "{1, 2, 3} | {2, 3, 4} & {3, 4, 5}"},
            {"expr": "({1, 2, 3} | {4}) - {2, 4}"},
            {"expr": "{1, 2} ^ {2, 3}"},
        ],
        "hidden": [
            {"expr": "{}"},
            {"expr": "{-5, 0, 5, -5}"},
            {"expr": "{1, 2, 3} - {1, 2, 3}"},
            {"expr": "{1, 2, 3} - {2} - {3}"},
            {"expr": "{1, 2, 3} - ({2} - {3})"},
            {"expr": "({-1, -2, 3} ^ {-2, 4}) & {-1, 4, 9}"},
            {"expr": "{} | {10, -10} & {10}"},
            {"expr": "({1,2} | {3,4}) ^ ({2,3} | {4,5})"},
            {"expr": _perf_90()},
        ],
    },

    # ------------------------------------------------------------------
    # 91 - Regex Match Length Bounds
    # ------------------------------------------------------------------
    {
        "slug": "91-regex-match-length-bounds",
        "title": "Regex Match Length Bounds",
        "difficulty": "Hard",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Meta", "Amazon", "Bloomberg"],
        "desc": (
            "You are given a valid bounded regular expression string `regex` composed of:\n"
            "- Lowercase English letters `'a'`-`'z'`, each matching a single character (length `1`).\n"
            "- Grouping parentheses `'('` and `')'`.\n"
            "- Alternation `'|'` separating non-empty branches inside the current group or top level.\n"
            "- Postfix quantifiers applied to the immediately preceding atom (either a single letter or a `(...)` group), with at most one quantifier per atom:\n"
            "  - `'?'`: 0 or 1 repetition.\n"
            "  - `'{k}'`: exactly `k` repetitions (`0 <= k <= 100`).\n"
            "  - `'{a,b}'`: between `a` and `b` repetitions inclusive (`0 <= a <= b <= 100`).\n\n"
            "Return a 2-element 64-bit integer array `[minLen, maxLen]` giving the shortest and longest string lengths matched by `regex`."
        ),
        "cons": [
            "1 <= regex.length <= 10^4",
            "regex is syntactically valid with no empty branches and at most one quantifier per atom.",
            "All intermediate and final lengths fit in a 64-bit signed integer."
        ],
        "hints": [
            "Maintain a stack of group frames saving `(altMin, altMax, curMin, curMax)` before each `'('`, while keeping the most recent atom's range `(lastMin, lastMax)` separate until the next token arrives.",
            "A quantifier immediately updates `(lastMin, lastMax)` (`?` sets `lastMin = 0`, `{a,b}` multiplies by `(a, b)`); on `'|'` or `')'`, flush `last` into `cur` and fold `cur` into the group's `(altMin, altMax)`."
        ],
        "explanations": [
            "Shortest match is \"aee\" (length 3) by skipping (b|cd) and taking 2 e's; longest is \"acdeee\" (length 6).",
            "First branch (ab|c){2} has lengths [2, 4] and second branch defg has length [4, 4], giving [2, 4].",
            "a? has length [0, 1], repeated 3 times gives [0, 3]."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "regexLengthBounds",
        "params": [("regex", "String")],
        "ret": "long[]",
        "py": """        stack = []
        has_alt = False
        alt_min = 0
        alt_max = 0
        cur_min = 0
        cur_max = 0
        has_last = False
        last_min = 0
        last_max = 0

        i = 0
        n = len(regex)
        while i < n:
            ch = regex[i]
            if 'a' <= ch <= 'z':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                has_last = True
                last_min = 1
                last_max = 1
                i += 1
            elif ch == '(':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                    has_last = False
                stack.append((has_alt, alt_min, alt_max, cur_min, cur_max))
                has_alt = False
                alt_min = alt_max = cur_min = cur_max = 0
                i += 1
            elif ch == '|':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                    has_last = False
                if not has_alt:
                    has_alt = True
                    alt_min, alt_max = cur_min, cur_max
                else:
                    if cur_min < alt_min:
                        alt_min = cur_min
                    if cur_max > alt_max:
                        alt_max = cur_max
                cur_min = cur_max = 0
                i += 1
            elif ch == ')':
                if has_last:
                    cur_min += last_min
                    cur_max += last_max
                    has_last = False
                if not has_alt:
                    g_min, g_max = cur_min, cur_max
                else:
                    g_min = cur_min if cur_min < alt_min else alt_min
                    g_max = cur_max if cur_max > alt_max else alt_max
                has_alt, alt_min, alt_max, cur_min, cur_max = stack.pop()
                has_last = True
                last_min, last_max = g_min, g_max
                i += 1
            elif ch == '?':
                last_min = 0
                i += 1
            elif ch == '{':
                j = regex.index('}', i)
                body = regex[i + 1:j]
                if ',' in body:
                    p1, p2 = body.split(',')
                    lo, hi = int(p1), int(p2)
                else:
                    lo = hi = int(body)
                last_min *= lo
                last_max *= hi
                i = j + 1
            else:
                i += 1

        if has_last:
            cur_min += last_min
            cur_max += last_max
        if not has_alt:
            return [cur_min, cur_max]
        return [min(alt_min, cur_min), max(alt_max, cur_max)]""",
        "java": """        Deque<long[]> stack = new ArrayDeque<>();
        long hasAlt = 0, altMin = 0, altMax = 0, curMin = 0, curMax = 0;
        boolean hasLast = false;
        long lastMin = 0, lastMax = 0;
        int i = 0, n = regex.length();
        while (i < n) {
            char ch = regex.charAt(i);
            if (ch >= 'a' && ch <= 'z') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                }
                hasLast = true;
                lastMin = 1;
                lastMax = 1;
                i++;
            } else if (ch == '(') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                    hasLast = false;
                }
                stack.push(new long[]{hasAlt, altMin, altMax, curMin, curMax});
                hasAlt = 0; altMin = 0; altMax = 0; curMin = 0; curMax = 0;
                i++;
            } else if (ch == '|') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                    hasLast = false;
                }
                if (hasAlt == 0) {
                    hasAlt = 1;
                    altMin = curMin;
                    altMax = curMax;
                } else {
                    altMin = Math.min(altMin, curMin);
                    altMax = Math.max(altMax, curMax);
                }
                curMin = 0; curMax = 0;
                i++;
            } else if (ch == ')') {
                if (hasLast) {
                    curMin += lastMin;
                    curMax += lastMax;
                    hasLast = false;
                }
                long gMin = (hasAlt == 0) ? curMin : Math.min(altMin, curMin);
                long gMax = (hasAlt == 0) ? curMax : Math.max(altMax, curMax);
                long[] prev = stack.pop();
                hasAlt = prev[0];
                altMin = prev[1];
                altMax = prev[2];
                curMin = prev[3];
                curMax = prev[4];
                hasLast = true;
                lastMin = gMin;
                lastMax = gMax;
                i++;
            } else if (ch == '?') {
                lastMin = 0;
                i++;
            } else if (ch == '{') {
                int j = regex.indexOf('}', i);
                String body = regex.substring(i + 1, j);
                int comma = body.indexOf(',');
                long lo, hi;
                if (comma >= 0) {
                    lo = Long.parseLong(body.substring(0, comma));
                    hi = Long.parseLong(body.substring(comma + 1));
                } else {
                    lo = hi = Long.parseLong(body);
                }
                lastMin *= lo;
                lastMax *= hi;
                i = j + 1;
            } else {
                i++;
            }
        }
        if (hasLast) {
            curMin += lastMin;
            curMax += lastMax;
        }
        if (hasAlt == 0) return new long[]{curMin, curMax};
        return new long[]{Math.min(altMin, curMin), Math.max(altMax, curMax)};""",
        "visible": [
            {"regex": "a(b|cd)?e{2,3}"},
            {"regex": "(ab|c){2}|defg"},
            {"regex": "(a?){3}"},
        ],
        "hidden": [
            {"regex": "a"},
            {"regex": "a?"},
            {"regex": "a{0}"},
            {"regex": "abc{0,4}"},
            {"regex": "(a|bb|ccc){2,5}"},
            {"regex": "((a|bc)?d){3}"},
            {"regex": "x(y{2,4}|z(ab|c){1,3})w?"},
            {"regex": "((a{10}){10}){2}"},
            {"regex": _perf_91()},
        ],
    },

    # ------------------------------------------------------------------
    # 92 - Infix Expression Tree Height
    # ------------------------------------------------------------------
    {
        "slug": "92-infix-expression-tree-height",
        "title": "Infix Expression Tree Height",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Amazon", "Microsoft", "Apple"],
        "desc": (
            "Given a valid infix arithmetic expression string `s` consisting of non-negative integers, binary operators `'+'`, `'-'`, `'*'`, `'/'`, parentheses `'('` and `')'`, and optional spaces, determine the **height of its Abstract Syntax Tree (expression tree)** under standard precedence (`'*'`, `'/'` > `'+'`, `'-'`, all left-associative).\n\n"
            "The height of a single integer leaf node is `0`, and the height of an operator node with left subtree `L` and right subtree `R` is `1 + max(height(L), height(R))`."
        ),
        "cons": [
            "1 <= s.length <= 2 * 10^4",
            "s is a valid infix arithmetic expression containing digits, '+', '-', '*', '/', '(', ')', and ' '."
        ],
        "hints": [
            "You do not need to allocate tree nodes — run Shunting-Yard with an integer stack storing subtree heights (every number literal pushes height 0).",
            "Whenever an operator is popped and applied, pop `hRight` and `hLeft` from the height stack and push `1 + max(hLeft, hRight)`."
        ],
        "explanations": [
            "1 + 2 * 3 parses as +(1, *(2, 3)): *(2, 3) has height 1, and the root '+' has height 2.",
            "(1 + 2) * (3 + 4) has two height-1 children under '*', so the tree height is 2.",
            "Left-associative 1 + 2 + 3 + 4 forms a left-leaning chain (((1+2)+3)+4) of height 3."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "expressionTreeHeight",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        prec = {'+': 1, '-': 1, '*': 2, '/': 2}
        heights = []
        ops = []

        def apply_top():
            ops.pop()
            hr = heights.pop()
            hl = heights.pop()
            heights.append(1 + (hl if hl > hr else hr))

        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == ' ':
                i += 1
            elif '0' <= ch <= '9':
                while i < n and '0' <= s[i] <= '9':
                    i += 1
                heights.append(0)
            elif ch == '(':
                ops.append(ch)
                i += 1
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_top()
                ops.pop()
                i += 1
            else:
                p = prec[ch]
                while ops and ops[-1] != '(' and prec[ops[-1]] >= p:
                    apply_top()
                ops.append(ch)
                i += 1
        while ops:
            apply_top()
        return heights[-1]""",
        "java": """        Deque<Integer> heights = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = s.length();
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch >= '0' && ch <= '9') {
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') i++;
                heights.push(0);
            } else if (ch == '(') {
                ops.push(ch);
                i++;
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyOp(heights, ops);
                }
                ops.pop();
                i++;
            } else {
                int p = (ch == '*' || ch == '/') ? 2 : 1;
                while (!ops.isEmpty() && ops.peek() != '(' && ((ops.peek() == '*' || ops.peek() == '/') ? 2 : 1) >= p) {
                    applyOp(heights, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyOp(heights, ops);
        }
        return heights.peek();""",
        "java_helpers": """    private void applyOp(Deque<Integer> heights, Deque<Character> ops) {
        ops.pop();
        int hr = heights.pop();
        int hl = heights.pop();
        heights.push(1 + Math.max(hl, hr));
    }""",
        "visible": [
            {"s": "1 + 2 * 3"},
            {"s": "(1 + 2) * (3 + 4)"},
            {"s": "1 + 2 + 3 + 4"},
        ],
        "hidden": [
            {"s": "42"},
            {"s": "(((99)))"},
            {"s": "1 + 2"},
            {"s": "(1 + 2) + (3 + 4)"},
            {"s": "1 * 2 + 3 * 4"},
            {"s": "1 + (2 + (3 + (4 + 5)))"},
            {"s": "((1 + 2) * (3 - 4)) / ((5 + 6) * (7 - 8))"},
            {"s": "10 / 2 / 5 + 3 * 4 * 5"},
            {"s": _perf_92()},
        ],
    },

    # ------------------------------------------------------------------
    # 93 - Bounded Min Index Stack
    # ------------------------------------------------------------------
    {
        "slug": "93-bounded-min-index-stack",
        "title": "Bounded Min Index Stack",
        "difficulty": "Easy",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Oracle"],
        "desc": (
            "Design a fixed-capacity stack `BoundedMinStack` supporting `O(1)` minimum value and minimum index queries.\n\n"
            "Implement the `BoundedMinStack` class:\n"
            "- `BoundedMinStack(int capacity)` initializes an empty stack holding at most `capacity` elements.\n"
            "- `boolean push(int val)` pushes `val` (`0 <= val <= 10^9`) onto the top and returns `true` if `size < capacity`; otherwise leaves the stack unchanged and returns `false`.\n"
            "- `int pop()` removes and returns the top element, or returns `-1` if the stack is empty.\n"
            "- `int top()` returns the top element without removing it, or returns `-1` if the stack is empty.\n"
            "- `int getMin()` returns the minimum element currently in the stack, or returns `-1` if empty.\n"
            "- `int getMinIndex()` returns the **0-based index from the bottom** of the earliest (deepest) occurrence of the current minimum element, or returns `-1` if empty."
        ),
        "cons": [
            "1 <= capacity <= 10^4",
            "0 <= val <= 10^9",
            "At most 3 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Store `(val, runningMin, runningMinIndex)` for each pushed element.",
            "Update `(runningMin, runningMinIndex)` only when `val < previousMin` (strict inequality) so ties always preserve the deepest 0-based index."
        ],
        "explanations": [
            "Stack becomes [5, 2, 2] (capacity 3); pushing 1 fails. Current min is 2 at earliest index 1. After two pops, only [5] remains with min 5 at index 0.",
            "All queries on an empty stack return -1.",
            "After pushing 7 then 3, min is 3 at index 1; popping 3 restores min 7 at index 0."
        ],
        "time": "O(1) per op",
        "space": "O(capacity)",
        "kind": "design",
        "className": "BoundedMinStack",
        "ctorParams": [("capacity", "int")],
        "methods": [
            ("push", [("val", "int")], "boolean"),
            ("pop", [], "int"),
            ("top", [], "int"),
            ("getMin", [], "int"),
            ("getMinIndex", [], "int"),
        ],
        "py_class": """class BoundedMinStack:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.vals = []
        self.mins = []
        self.min_idx = []

    def push(self, val: int) -> bool:
        if len(self.vals) == self.cap:
            return False
        idx = len(self.vals)
        self.vals.append(val)
        if idx == 0 or val < self.mins[-1]:
            self.mins.append(val)
            self.min_idx.append(idx)
        else:
            self.mins.append(self.mins[-1])
            self.min_idx.append(self.min_idx[-1])
        return True

    def pop(self) -> int:
        if not self.vals:
            return -1
        self.mins.pop()
        self.min_idx.pop()
        return self.vals.pop()

    def top(self) -> int:
        return self.vals[-1] if self.vals else -1

    def getMin(self) -> int:
        return self.mins[-1] if self.mins else -1

    def getMinIndex(self) -> int:
        return self.min_idx[-1] if self.min_idx else -1""",
        "java_class": """class BoundedMinStack {
    private final int[] vals;
    private final int[] mins;
    private final int[] minIdx;
    private int sz;

    public BoundedMinStack(int capacity) {
        this.vals = new int[capacity];
        this.mins = new int[capacity];
        this.minIdx = new int[capacity];
        this.sz = 0;
    }

    public boolean push(int val) {
        if (sz == vals.length) return false;
        vals[sz] = val;
        if (sz == 0 || val < mins[sz - 1]) {
            mins[sz] = val;
            minIdx[sz] = sz;
        } else {
            mins[sz] = mins[sz - 1];
            minIdx[sz] = minIdx[sz - 1];
        }
        sz++;
        return true;
    }

    public int pop() {
        if (sz == 0) return -1;
        return vals[--sz];
    }

    public int top() {
        return sz == 0 ? -1 : vals[sz - 1];
    }

    public int getMin() {
        return sz == 0 ? -1 : mins[sz - 1];
    }

    public int getMinIndex() {
        return sz == 0 ? -1 : minIdx[sz - 1];
    }
}""",
        "visible": [
            {
                "ops": ["BoundedMinStack", "push", "push", "push", "push", "getMin", "getMinIndex", "pop", "pop", "getMin", "getMinIndex"],
                "args": [[3], [5], [2], [2], [1], [], [], [], [], [], []],
            },
            {
                "ops": ["BoundedMinStack", "pop", "top", "getMin", "getMinIndex"],
                "args": [[2], [], [], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "push", "getMin", "getMinIndex", "pop", "getMin", "getMinIndex"],
                "args": [[4], [7], [3], [], [], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["BoundedMinStack", "push", "push", "top", "getMin", "getMinIndex", "pop", "getMin"],
                "args": [[1], [0], [5], [], [], [], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "push", "push", "getMinIndex", "pop", "getMinIndex"],
                "args": [[5], [4], [4], [4], [], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "push", "push", "getMin", "getMinIndex", "pop", "getMin", "getMinIndex"],
                "args": [[3], [10], [8], [6], [], [], [], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "push", "push", "pop", "push", "getMin", "getMinIndex"],
                "args": [[2], [9], [3], [1], [], [2], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "pop", "pop", "push", "top", "getMinIndex"],
                "args": [[3], [100], [], [], [50], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "push", "push", "push", "getMin", "getMinIndex"],
                "args": [[4], [1000000000], [999999999], [1000000000], [0], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "push", "push", "pop", "push", "getMinIndex", "top"],
                "args": [[3], [5], [5], [2], [], [5], [], []],
            },
            {
                "ops": ["BoundedMinStack", "push", "push", "pop", "push", "pop", "getMin", "getMinIndex"],
                "args": [[2], [8], [4], [], [9], [], [], []],
            },
            _perf_93(),
        ],
    },

    # ------------------------------------------------------------------
    # 94 - GCD Stack
    # ------------------------------------------------------------------
    {
        "slug": "94-gcd-stack",
        "title": "GCD Stack",
        "difficulty": "Easy",
        "subtopic": "Min Stack",
        "companies": ["Google", "Amazon", "Meta", "Goldman Sachs"],
        "desc": (
            "Design a stack `GcdStack` of positive integers that supports standard LIFO operations alongside retrieving the **Greatest Common Divisor (GCD)** of all elements currently in the stack in `O(1)` time.\n\n"
            "Implement the `GcdStack` class:\n"
            "- `GcdStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes positive integer `val` onto the top of the stack.\n"
            "- `void pop()` removes the top element of the stack.\n"
            "- `int top()` returns the top element of the stack.\n"
            "- `int getGcd()` returns the GCD of all elements currently in the stack."
        ),
        "cons": [
            "1 <= val <= 10^9",
            "Methods pop, top, and getGcd are always called on non-empty stacks.",
            "At most 3 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Just like `min`, `gcd` is associative, so maintaining a parallel prefix-GCD stack lets every `pop`, `top`, and `getGcd` run in O(1).",
            "On `push(val)`, push `val` onto the value stack and `gcd(val, gcdStack[-1])` (or `val` if empty) onto the GCD stack."
        ],
        "explanations": [
            "gcd(12) = 12, gcd(12, 18) = 6, gcd(12, 18, 9) = 3; after popping 9, gcd(12, 18) returns to 6.",
            "After pushing 7 and 14, gcd is 7; pushing 15 drops gcd to 1; popping 15 restores gcd to 7.",
            "A single element 100 has gcd 100 and top 100."
        ],
        "time": "O(log M) push, O(1) pop/top/getGcd",
        "space": "O(n)",
        "kind": "design",
        "className": "GcdStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "void"),
            ("top", [], "int"),
            ("getGcd", [], "int"),
        ],
        "py_class": """class GcdStack:
    def __init__(self):
        self.vals = []
        self.gcds = []

    def push(self, val: int) -> None:
        import math
        self.vals.append(val)
        if not self.gcds:
            self.gcds.append(val)
        else:
            self.gcds.append(math.gcd(self.gcds[-1], val))

    def pop(self) -> None:
        self.vals.pop()
        self.gcds.pop()

    def top(self) -> int:
        return self.vals[-1]

    def getGcd(self) -> int:
        return self.gcds[-1]""",
        "java_class": """class GcdStack {
    private final Deque<Integer> vals = new ArrayDeque<>();
    private final Deque<Integer> gcds = new ArrayDeque<>();

    public GcdStack() {
    }

    private int gcd(int a, int b) {
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    public void push(int val) {
        vals.push(val);
        if (gcds.isEmpty()) gcds.push(val);
        else gcds.push(gcd(gcds.peek(), val));
    }

    public void pop() {
        vals.pop();
        gcds.pop();
    }

    public int top() {
        return vals.peek();
    }

    public int getGcd() {
        return gcds.peek();
    }
}""",
        "visible": [
            {
                "ops": ["GcdStack", "push", "push", "getGcd", "push", "getGcd", "pop", "getGcd", "top"],
                "args": [[], [12], [18], [], [9], [], [], [], []],
            },
            {
                "ops": ["GcdStack", "push", "push", "getGcd", "push", "getGcd", "pop", "getGcd"],
                "args": [[], [7], [14], [], [15], [], [], []],
            },
            {
                "ops": ["GcdStack", "push", "top", "getGcd"],
                "args": [[], [100], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["GcdStack", "push", "push", "getGcd", "pop", "getGcd"],
                "args": [[], [1], [1000000000], [], [], []],
            },
            {
                "ops": ["GcdStack", "push", "push", "push", "getGcd", "pop", "pop", "getGcd"],
                "args": [[], [24], [36], [60], [], [], [], []],
            },
            {
                "ops": ["GcdStack", "push", "pop", "push", "push", "getGcd"],
                "args": [[], [5], [], [30], [45], []],
            },
            {
                "ops": ["GcdStack", "push", "push", "push", "getGcd", "pop", "getGcd", "pop", "getGcd"],
                "args": [[], [1000000000], [500000000], [250000000], [], [], [], [], []],
            },
            {
                "ops": ["GcdStack", "push", "push", "getGcd", "push", "getGcd", "pop", "top"],
                "args": [[], [17], [19], [], [34], [], [], []],
            },
            {
                "ops": ["GcdStack", "push", "push", "push", "push", "getGcd", "pop", "getGcd"],
                "args": [[], [48], [64], [80], [16], [], [], []],
            },
            {
                "ops": ["GcdStack", "push", "push", "pop", "push", "getGcd", "top"],
                "args": [[], [90], [15], [], [60], [], []],
            },
            {
                "ops": ["GcdStack", "push", "push", "push", "pop", "push", "getGcd"],
                "args": [[], [21], [14], [10], [], [35], []],
            },
            _perf_94(),
        ],
    },

    # ------------------------------------------------------------------
    # 95 - Affine Min Stack
    # ------------------------------------------------------------------
    {
        "slug": "95-affine-min-stack",
        "title": "Affine Min Stack",
        "difficulty": "Medium",
        "subtopic": "Min Stack",
        "companies": ["Google", "Meta", "Bloomberg", "Goldman Sachs"],
        "desc": (
            "Design a stack `AffineMinStack` supporting global addition (`addAll`), global sign flip (`negateAll`), and minimum queries, all in **`O(1)` time** per operation.\n\n"
            "Implement the `AffineMinStack` class:\n"
            "- `AffineMinStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes `val` onto the top of the stack.\n"
            "- `void pop()` removes the top element of the stack.\n"
            "- `void addAll(int delta)` adds `delta` to every element currently in the stack.\n"
            "- `void negateAll()` multiplies every element currently in the stack by `-1`.\n"
            "- `long top()` returns the current top element of the stack.\n"
            "- `long getMin()` returns the current minimum element in the stack."
        ),
        "cons": [
            "-10^9 <= val, delta <= 10^9",
            "Methods pop, top, and getMin are always called on non-empty stacks.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Maintain a global affine transform `actual = sign * stored + offset` with `sign` in `{+1, -1}` and `offset` initially `0`; on `addAll(d)` set `offset += d`, and on `negateAll()` flip both `sign = -sign` and `offset = -offset`.",
            "Because `negateAll()` turns the stored maximum into the actual minimum, track BOTH `storedMin` and `storedMax` stacks: `getMin()` returns `storedMin[-1] + offset` when `sign == 1` and `-storedMax[-1] + offset` when `sign == -1`."
        ],
        "explanations": [
            "Push 5, 2 -> [5, 2]; addAll(3) -> [8, 5]; negateAll -> [-8, -5] (min -8, top -5); push 10 -> [-8, -5, 10]; negateAll -> [8, 5, -10] (min -10).",
            "Negating [4, -1] twice restores [4, -1], and popping -1 leaves [4] with min 4.",
            "addAll and negateAll on an empty stack leave the affine state valid for subsequent pushes."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "AffineMinStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "void"),
            ("addAll", [("delta", "int")], "void"),
            ("negateAll", [], "void"),
            ("top", [], "long"),
            ("getMin", [], "long"),
        ],
        "py_class": """class AffineMinStack:
    def __init__(self):
        self.vals = []
        self.mins = []
        self.maxs = []
        self.sign = 1
        self.offset = 0

    def push(self, val: int) -> None:
        stored = self.sign * (val - self.offset)
        self.vals.append(stored)
        if not self.mins:
            self.mins.append(stored)
            self.maxs.append(stored)
        else:
            self.mins.append(stored if stored < self.mins[-1] else self.mins[-1])
            self.maxs.append(stored if stored > self.maxs[-1] else self.maxs[-1])

    def pop(self) -> None:
        self.vals.pop()
        self.mins.pop()
        self.maxs.pop()

    def addAll(self, delta: int) -> None:
        self.offset += delta

    def negateAll(self) -> None:
        self.sign = -self.sign
        self.offset = -self.offset

    def top(self) -> int:
        return self.sign * self.vals[-1] + self.offset

    def getMin(self) -> int:
        if self.sign == 1:
            return self.mins[-1] + self.offset
        return -self.maxs[-1] + self.offset""",
        "java_class": """class AffineMinStack {
    private final Deque<Long> vals = new ArrayDeque<>();
    private final Deque<Long> mins = new ArrayDeque<>();
    private final Deque<Long> maxs = new ArrayDeque<>();
    private long sign = 1L;
    private long offset = 0L;

    public AffineMinStack() {
    }

    public void push(int val) {
        long stored = sign * ((long) val - offset);
        vals.push(stored);
        if (mins.isEmpty()) {
            mins.push(stored);
            maxs.push(stored);
        } else {
            mins.push(Math.min(stored, mins.peek()));
            maxs.push(Math.max(stored, maxs.peek()));
        }
    }

    public void pop() {
        vals.pop();
        mins.pop();
        maxs.pop();
    }

    public void addAll(int delta) {
        offset += delta;
    }

    public void negateAll() {
        sign = -sign;
        offset = -offset;
    }

    public long top() {
        return sign * vals.peek() + offset;
    }

    public long getMin() {
        if (sign == 1L) return mins.peek() + offset;
        return -maxs.peek() + offset;
    }
}""",
        "visible": [
            {
                "ops": ["AffineMinStack", "push", "push", "addAll", "negateAll", "getMin", "top", "push", "negateAll", "getMin"],
                "args": [[], [5], [2], [3], [], [], [], [10], [], []],
            },
            {
                "ops": ["AffineMinStack", "push", "push", "negateAll", "negateAll", "getMin", "pop", "getMin"],
                "args": [[], [4], [-1], [], [], [], [], []],
            },
            {
                "ops": ["AffineMinStack", "addAll", "negateAll", "push", "top", "getMin"],
                "args": [[], [100], [], [7], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["AffineMinStack", "push", "negateAll", "top", "getMin"],
                "args": [[], [0], [], [], []],
            },
            {
                "ops": ["AffineMinStack", "push", "push", "push", "negateAll", "addAll", "getMin", "pop", "getMin"],
                "args": [[], [1], [10], [5], [], [20], [], [], []],
            },
            {
                "ops": ["AffineMinStack", "push", "addAll", "addAll", "negateAll", "top", "getMin"],
                "args": [[], [1000000000], [1000000000], [1000000000], [], [], []],
            },
            {
                "ops": ["AffineMinStack", "push", "negateAll", "push", "negateAll", "push", "getMin", "pop", "getMin", "pop", "getMin"],
                "args": [[], [3], [], [4], [], [5], [], [], [], [], []],
            },
            {
                "ops": ["AffineMinStack", "push", "push", "pop", "negateAll", "addAll", "push", "getMin", "top"],
                "args": [[], [-5], [8], [], [], [-3], [1], [], []],
            },
            {
                "ops": ["AffineMinStack", "push", "push", "addAll", "negateAll", "addAll", "negateAll", "top", "getMin"],
                "args": [[], [2], [-6], [4], [], [-2], [], [], []],
            },
            {
                "ops": ["AffineMinStack", "push", "pop", "negateAll", "addAll", "push", "push", "getMin"],
                "args": [[], [9], [], [], [10], [-2], [3], []],
            },
            {
                "ops": ["AffineMinStack", "push", "push", "push", "negateAll", "pop", "negateAll", "pop", "top", "getMin"],
                "args": [[], [100], [-100], [50], [], [], [], [], [], []],
            },
            _perf_95(),
        ],
    },

    # ------------------------------------------------------------------
    # 96 - Amortized Min Deque
    # ------------------------------------------------------------------
    {
        "slug": "96-amortized-min-deque",
        "title": "Amortized Min Deque",
        "difficulty": "Hard",
        "subtopic": "Min Stack",
        "companies": ["Google", "Meta", "Amazon", "Bloomberg", "Uber"],
        "desc": (
            "Design a double-ended queue `MinDeque` using **two min-stacks** that supports insertions and removals at **both ends** as well as retrieving the current minimum element, all in **amortized `O(1)` time** per operation.\n\n"
            "Implement the `MinDeque` class:\n"
            "- `MinDeque()` initializes an empty deque.\n"
            "- `void pushFront(int val)` inserts `val` at the front of the deque.\n"
            "- `void pushBack(int val)` inserts `val` at the back of the deque.\n"
            "- `int popFront()` removes and returns the front element.\n"
            "- `int popBack()` removes and returns the back element.\n"
            "- `int getMin()` returns the minimum element currently in the deque."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Methods popFront, popBack, and getMin are always called on non-empty deques.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Maintain two min-stacks: `left` (whose top is the deque front) and `right` (whose top is the deque back), so `getMin()` is simply `min(left.min, right.min)`.",
            "When popping from an empty stack while the other stack has `m` elements, move only the bottom `ceil(m / 2)` elements (reversed) to the empty stack and rebuild prefix minimums on both halves; by potential `||left| - |right||`, every operation is amortized O(1)."
        ],
        "explanations": [
            "Deque becomes [3, 5, 1] (min 1); popBack removes 1 -> [3, 5] (min 3); popFront removes 3 -> [5] (min 5).",
            "Pushing 10, 20, 30 to back then alternating popFront (10) and popBack (30) leaves [20] with min 20.",
            "Single element pushed to front can be popped from back cleanly."
        ],
        "time": "O(1) amortized per op",
        "space": "O(n)",
        "kind": "design",
        "className": "MinDeque",
        "ctorParams": [],
        "methods": [
            ("pushFront", [("val", "int")], "void"),
            ("pushBack", [("val", "int")], "void"),
            ("popFront", [], "int"),
            ("popBack", [], "int"),
            ("getMin", [], "int"),
        ],
        "py_class": """class MinDeque:
    def __init__(self):
        self.lv = []
        self.lm = []
        self.rv = []
        self.rm = []

    def _push(self, vs, ms, val: int) -> None:
        vs.append(val)
        ms.append(val if not ms or val < ms[-1] else ms[-1])

    def _rebalance(self, src_v, src_m, dst_v, dst_m) -> None:
        m = len(src_v)
        half = (m + 1) // 2
        to_dst = src_v[:half]
        stay = src_v[half:]
        src_v.clear()
        src_m.clear()
        for x in reversed(to_dst):
            self._push(dst_v, dst_m, x)
        for x in stay:
            self._push(src_v, src_m, x)

    def pushFront(self, val: int) -> None:
        self._push(self.lv, self.lm, val)

    def pushBack(self, val: int) -> None:
        self._push(self.rv, self.rm, val)

    def popFront(self) -> int:
        if not self.lv:
            self._rebalance(self.rv, self.rm, self.lv, self.lm)
        self.lm.pop()
        return self.lv.pop()

    def popBack(self) -> int:
        if not self.rv:
            self._rebalance(self.lv, self.lm, self.rv, self.rm)
        self.rm.pop()
        return self.rv.pop()

    def getMin(self) -> int:
        if self.lm and self.rm:
            return self.lm[-1] if self.lm[-1] < self.rm[-1] else self.rm[-1]
        return self.lm[-1] if self.lm else self.rm[-1]""",
        "java_class": """class MinDeque {
    private final List<Integer> lv = new ArrayList<>();
    private final List<Integer> lm = new ArrayList<>();
    private final List<Integer> rv = new ArrayList<>();
    private final List<Integer> rm = new ArrayList<>();

    public MinDeque() {
    }

    private void pushSide(List<Integer> vs, List<Integer> ms, int val) {
        vs.add(val);
        int mn = ms.isEmpty() ? val : Math.min(val, ms.get(ms.size() - 1));
        ms.add(mn);
    }

    private void rebalance(List<Integer> srcV, List<Integer> srcM, List<Integer> dstV, List<Integer> dstM) {
        int m = srcV.size();
        int half = (m + 1) / 2;
        int[] tmp = new int[m];
        for (int i = 0; i < m; i++) tmp[i] = srcV.get(i);
        srcV.clear();
        srcM.clear();
        for (int i = half - 1; i >= 0; i--) {
            pushSide(dstV, dstM, tmp[i]);
        }
        for (int i = half; i < m; i++) {
            pushSide(srcV, srcM, tmp[i]);
        }
    }

    public void pushFront(int val) {
        pushSide(lv, lm, val);
    }

    public void pushBack(int val) {
        pushSide(rv, rm, val);
    }

    public int popFront() {
        if (lv.isEmpty()) rebalance(rv, rm, lv, lm);
        lm.remove(lm.size() - 1);
        return lv.remove(lv.size() - 1);
    }

    public int popBack() {
        if (rv.isEmpty()) rebalance(lv, lm, rv, rm);
        rm.remove(rm.size() - 1);
        return rv.remove(rv.size() - 1);
    }

    public int getMin() {
        if (!lm.isEmpty() && !rm.isEmpty()) {
            return Math.min(lm.get(lm.size() - 1), rm.get(rm.size() - 1));
        }
        return !lm.isEmpty() ? lm.get(lm.size() - 1) : rm.get(rm.size() - 1);
    }
}""",
        "visible": [
            {
                "ops": ["MinDeque", "pushBack", "pushFront", "pushBack", "getMin", "popBack", "getMin", "popFront", "getMin"],
                "args": [[], [5], [3], [1], [], [], [], [], []],
            },
            {
                "ops": ["MinDeque", "pushBack", "pushBack", "pushBack", "popFront", "popBack", "getMin"],
                "args": [[], [10], [20], [30], [], [], []],
            },
            {
                "ops": ["MinDeque", "pushFront", "getMin", "popBack"],
                "args": [[], [-7], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["MinDeque", "pushBack", "getMin", "popFront"],
                "args": [[], [42], [], []],
            },
            {
                "ops": ["MinDeque", "pushFront", "pushFront", "pushFront", "pushFront", "popBack", "getMin", "popBack", "getMin"],
                "args": [[], [4], [3], [2], [1], [], [], [], []],
            },
            {
                "ops": ["MinDeque", "pushBack", "pushBack", "pushBack", "pushBack", "pushBack", "popFront", "getMin", "popBack", "getMin"],
                "args": [[], [1], [5], [2], [4], [3], [], [], [], []],
            },
            {
                "ops": ["MinDeque", "pushFront", "pushBack", "popFront", "popBack", "pushBack", "getMin"],
                "args": [[], [8], [9], [], [], [-1000000000], []],
            },
            {
                "ops": ["MinDeque", "pushBack", "pushBack", "pushBack", "popFront", "pushFront", "popBack", "getMin"],
                "args": [[], [7], [7], [7], [], [6], [], []],
            },
            {
                "ops": ["MinDeque", "pushFront", "pushFront", "popBack", "pushBack", "popFront", "getMin"],
                "args": [[], [10], [-5], [], [-2], [], []],
            },
            {
                "ops": ["MinDeque", "pushBack", "pushBack", "pushBack", "pushBack", "popFront", "popFront", "popFront", "getMin"],
                "args": [[], [2], [9], [1], [8], [], [], [], []],
            },
            {
                "ops": ["MinDeque", "pushFront", "pushBack", "pushFront", "pushBack", "popBack", "popFront", "getMin"],
                "args": [[], [100], [50], [25], [75], [], [], []],
            },
            _perf_96(),
        ],
    },

    # ------------------------------------------------------------------
    # 97 - Top-K Min Stack
    # ------------------------------------------------------------------
    {
        "slug": "97-top-k-min-stack",
        "title": "Top-K Min Stack",
        "difficulty": "Hard",
        "subtopic": "Min Stack",
        "companies": ["Google", "Meta", "Goldman Sachs", "Bloomberg"],
        "desc": (
            "Design a stack `TopKMinStack` that supports standard LIFO push/pop, full-stack minimum (`getMin`), and **top-`k` minimum queries (`getTopKMin(k)`)** returning the minimum among the `k` most recently pushed elements currently on the stack — with `O(log n)` `push` and **`O(1)` `pop`, `getMin`, and `getTopKMin`**!\n\n"
            "Implement the `TopKMinStack` class:\n"
            "- `TopKMinStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes `val` onto the top of the stack.\n"
            "- `int pop()` removes and returns the top element of the stack.\n"
            "- `int getMin()` returns the minimum element across the entire stack.\n"
            "- `int getTopKMin(int k)` returns the minimum among the top `k` elements (`1 <= k <= currentSize`)."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Methods pop and getMin are always called on non-empty stacks, and getTopKMin(k) always satisfies 1 <= k <= currentSize.",
            "At most 2 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Maintain a dynamic sparse table on the stack: for each stack position `i`, store `up[i][j]` = minimum of the `2^j` elements ending at index `i` (`2^j <= i + 1`).",
            "On `push(val)` compute `up[i][j] = min(up[i][j-1], up[i - 2^(j-1)][j-1])` in O(log n); on `pop()` simply remove the last row in O(1); on `getTopKMin(k)`, let `p = floor(log2(k))` and return `min(up[n-1][p], up[n - k + 2^p - 1][p])` in O(1)."
        ],
        "explanations": [
            "Stack [1, 5, 3, 7]: top-1 min is 7, top-2 min is min(3,7)=3, top-3 min is min(5,3,7)=3, top-4/getMin is 1.",
            "After popping 2 from [8, 4, 9, 2], stack is [8, 4, 9] so top-2 min is 4 and top-1 min is 9.",
            "Single element -5 has getTopKMin(1) = -5 and getMin() = -5."
        ],
        "time": "O(log n) push, O(1) pop/getMin/getTopKMin",
        "space": "O(n log n)",
        "kind": "design",
        "className": "TopKMinStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "int"),
            ("getMin", [], "int"),
            ("getTopKMin", [("k", "int")], "int"),
        ],
        "py_class": """class TopKMinStack:
    def __init__(self):
        self.up = []
        self.pref_min = []

    def push(self, val: int) -> None:
        idx = len(self.up)
        row = [val]
        j = 1
        while (1 << j) <= idx + 1:
            prev = self.up[idx - (1 << (j - 1))][j - 1]
            cur = row[j - 1]
            row.append(cur if cur < prev else prev)
            j += 1
        self.up.append(row)
        self.pref_min.append(val if not self.pref_min or val < self.pref_min[-1] else self.pref_min[-1])

    def pop(self) -> int:
        self.pref_min.pop()
        return self.up.pop()[0]

    def getMin(self) -> int:
        return self.pref_min[-1]

    def getTopKMin(self, k: int) -> int:
        n = len(self.up)
        p = k.bit_length() - 1
        a = self.up[n - 1][p]
        b = self.up[n - k + (1 << p) - 1][p]
        return a if a < b else b""",
        "java_class": """class TopKMinStack {
    private final List<int[]> up = new ArrayList<>();
    private final List<Integer> prefMin = new ArrayList<>();

    public TopKMinStack() {
    }

    public void push(int val) {
        int idx = up.size();
        int len = 32 - Integer.numberOfLeadingZeros(idx + 1);
        int[] row = new int[len];
        row[0] = val;
        for (int j = 1; j < len; j++) {
            row[j] = Math.min(row[j - 1], up.get(idx - (1 << (j - 1)))[j - 1]);
        }
        up.add(row);
        int mn = prefMin.isEmpty() ? val : Math.min(val, prefMin.get(prefMin.size() - 1));
        prefMin.add(mn);
    }

    public int pop() {
        prefMin.remove(prefMin.size() - 1);
        return up.remove(up.size() - 1)[0];
    }

    public int getMin() {
        return prefMin.get(prefMin.size() - 1);
    }

    public int getTopKMin(int k) {
        int n = up.size();
        int p = 31 - Integer.numberOfLeadingZeros(k);
        int a = up.get(n - 1)[p];
        int b = up.get(n - k + (1 << p) - 1)[p];
        return Math.min(a, b);
    }
}""",
        "visible": [
            {
                "ops": ["TopKMinStack", "push", "push", "push", "push", "getTopKMin", "getTopKMin", "getTopKMin", "getTopKMin", "getMin"],
                "args": [[], [1], [5], [3], [7], [1], [2], [3], [4], []],
            },
            {
                "ops": ["TopKMinStack", "push", "push", "push", "push", "pop", "getTopKMin", "getTopKMin"],
                "args": [[], [8], [4], [9], [2], [], [2], [1]],
            },
            {
                "ops": ["TopKMinStack", "push", "getTopKMin", "getMin"],
                "args": [[], [-5], [1], []],
            },
        ],
        "hidden": [
            {
                "ops": ["TopKMinStack", "push", "push", "push", "push", "push", "getTopKMin", "getTopKMin", "getTopKMin"],
                "args": [[], [10], [20], [30], [40], [50], [1], [3], [5]],
            },
            {
                "ops": ["TopKMinStack", "push", "push", "push", "push", "push", "getTopKMin", "getTopKMin", "getTopKMin"],
                "args": [[], [50], [40], [30], [20], [10], [1], [3], [5]],
            },
            {
                "ops": ["TopKMinStack", "push", "push", "pop", "push", "push", "getTopKMin", "getMin"],
                "args": [[], [9], [1], [], [6], [7], [2], []],
            },
            {
                "ops": ["TopKMinStack", "push", "push", "push", "push", "push", "push", "getTopKMin", "getTopKMin", "getTopKMin"],
                "args": [[], [-100], [50], [40], [30], [20], [10], [5], [6], [4]],
            },
            {
                "ops": ["TopKMinStack", "push", "pop", "push", "push", "getTopKMin", "getMin"],
                "args": [[], [1000000000], [], [-1000000000], [0], [2], []],
            },
            {
                "ops": ["TopKMinStack", "push", "push", "push", "push", "push", "push", "push", "getTopKMin", "getTopKMin"],
                "args": [[], [5], [2], [8], [1], [9], [3], [7], [3], [5]],
            },
            {
                "ops": ["TopKMinStack", "push", "push", "push", "pop", "pop", "push", "getTopKMin", "getMin"],
                "args": [[], [3], [3], [3], [], [], [4], [2], []],
            },
            {
                "ops": ["TopKMinStack", "push", "push", "push", "push", "pop", "push", "getTopKMin", "getTopKMin"],
                "args": [[], [12], [6], [15], [2], [], [9], [3], [2]],
            },
            _perf_97(),
        ],
    },

    # ------------------------------------------------------------------
    # 98 - Run-Length Min Stack
    # ------------------------------------------------------------------
    {
        "slug": "98-run-length-min-stack",
        "title": "Run-Length Min Stack",
        "difficulty": "Medium",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Google", "Microsoft", "Atlassian"],
        "desc": (
            "Design a compressed stack `RunLengthMinStack` that supports pushing and popping huge runs of identical integers in **amortized `O(1)` time**, while answering `top` and `getMin` in **`O(1)` time**.\n\n"
            "Implement the `RunLengthMinStack` class:\n"
            "- `RunLengthMinStack()` initializes an empty stack.\n"
            "- `void pushMany(int val, int count)` pushes `count` copies (`1 <= count <= 10^9`) of `val` onto the top of the stack.\n"
            "- `long popMany(int count)` pops the top `count` elements (`1 <= count <= currentSize`) and returns the **sum of the popped elements** as a 64-bit integer (`long`).\n"
            "- `int top()` returns the top element of the stack.\n"
            "- `int getMin()` returns the minimum element currently in the stack."
        ),
        "cons": [
            "-10^6 <= val <= 10^6",
            "1 <= count <= 10^9",
            "Methods popMany, top, and getMin are always called with valid non-empty stack sizes, and all popped sums fit in a 64-bit signed integer.",
            "At most 3 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Compress identical consecutive pushes into run entries `(val, runCount, runningMin)` on a stack.",
            "On `pushMany`, coalesce into the top run if `top.val == val` (which never changes `runningMin`); on `popMany(count)`, consume full or partial runs from the top until `count` reaches 0."
        ],
        "explanations": [
            "Push 5 copies of 10 and 3 copies of 4 (min 4). Popping 5 elements pops three 4's and two 10's (sum = 12 + 20 = 32), leaving three 10's (top 10, min 10).",
            "Pushing 10^6 copies of -3 then popping 500000 returns -1500000 while leaving -3 as top and min.",
            "Two consecutive pushMany calls with value 7 merge cleanly into one run."
        ],
        "time": "O(1) amortized per op",
        "space": "O(number of runs)",
        "kind": "design",
        "className": "RunLengthMinStack",
        "ctorParams": [],
        "methods": [
            ("pushMany", [("val", "int"), ("count", "int")], "void"),
            ("popMany", [("count", "int")], "long"),
            ("top", [], "int"),
            ("getMin", [], "int"),
        ],
        "py_class": """class RunLengthMinStack:
    def __init__(self):
        self.runs = []  # [val, count, running_min]

    def pushMany(self, val: int, count: int) -> None:
        if self.runs and self.runs[-1][0] == val:
            self.runs[-1][1] += count
        else:
            mn = val if not self.runs or val < self.runs[-1][2] else self.runs[-1][2]
            self.runs.append([val, count, mn])

    def popMany(self, count: int) -> int:
        total = 0
        rem = count
        while rem > 0:
            entry = self.runs[-1]
            if entry[1] <= rem:
                total += entry[0] * entry[1]
                rem -= entry[1]
                self.runs.pop()
            else:
                total += entry[0] * rem
                entry[1] -= rem
                rem = 0
        return total

    def top(self) -> int:
        return self.runs[-1][0]

    def getMin(self) -> int:
        return self.runs[-1][2]""",
        "java_class": """class RunLengthMinStack {
    private final List<long[]> runs = new ArrayList<>(); // {val, count, runningMin}

    public RunLengthMinStack() {
    }

    public void pushMany(int val, int count) {
        if (!runs.isEmpty() && runs.get(runs.size() - 1)[0] == val) {
            runs.get(runs.size() - 1)[1] += count;
        } else {
            long mn = runs.isEmpty() ? val : Math.min((long) val, runs.get(runs.size() - 1)[2]);
            runs.add(new long[]{val, count, mn});
        }
    }

    public long popMany(int count) {
        long total = 0L;
        long rem = count;
        while (rem > 0) {
            long[] entry = runs.get(runs.size() - 1);
            if (entry[1] <= rem) {
                total += entry[0] * entry[1];
                rem -= entry[1];
                runs.remove(runs.size() - 1);
            } else {
                total += entry[0] * rem;
                entry[1] -= rem;
                rem = 0;
            }
        }
        return total;
    }

    public int top() {
        return (int) runs.get(runs.size() - 1)[0];
    }

    public int getMin() {
        return (int) runs.get(runs.size() - 1)[2];
    }
}""",
        "visible": [
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "getMin", "popMany", "top", "getMin"],
                "args": [[], [10, 5], [4, 3], [], [5], [], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "popMany", "top", "getMin"],
                "args": [[], [-3, 1000000], [500000], [], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "popMany", "top", "getMin"],
                "args": [[], [7, 2], [7, 4], [3], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["RunLengthMinStack", "pushMany", "popMany", "pushMany", "getMin"],
                "args": [[], [5, 1], [1], [2, 10], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "pushMany", "popMany", "getMin", "top"],
                "args": [[], [1, 100], [2, 100], [3, 100], [150], [], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "popMany", "pushMany", "getMin"],
                "args": [[], [1000000, 1000000000], [-1000000, 1000000000], [1000000000], [0, 5], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "pushMany", "popMany", "popMany", "getMin"],
                "args": [[], [8, 2], [3, 3], [9, 4], [4], [2], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "pushMany", "popMany", "top", "getMin"],
                "args": [[], [-10, 1], [0, 5], [-20, 2], [2], [], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "popMany", "pushMany", "popMany", "top"],
                "args": [[], [4, 10], [4, 10], [15], [6, 3], [4], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "pushMany", "popMany", "getMin"],
                "args": [[], [100, 50], [50, 50], [25, 50], [100], []],
            },
            {
                "ops": ["RunLengthMinStack", "pushMany", "pushMany", "pushMany", "popMany", "top", "getMin"],
                "args": [[], [0, 1000], [5, 1000], [-5, 1000], [1000], [], []],
            },
            _perf_98(),
        ],
    },

    # ------------------------------------------------------------------
    # 99 - Incrementable Min Stack
    # ------------------------------------------------------------------
    {
        "slug": "99-incrementable-min-stack",
        "title": "Incrementable Min Stack",
        "difficulty": "Hard",
        "subtopic": "Min Stack",
        "companies": ["Google", "Meta", "Amazon", "Bloomberg"],
        "desc": (
            "Design a bounded stack `IncrementableMinStack` that supports adding a signed `delta` to the **bottom `k` elements** while answering `top` and `getMin` in **`O(log maxSize)` time**.\n\n"
            "Implement the `IncrementableMinStack` class:\n"
            "- `IncrementableMinStack(int maxSize)` initializes an empty stack with maximum capacity `maxSize`.\n"
            "- `void push(int val)` pushes `val` onto the top of the stack if current size `< maxSize` (otherwise ignores the call).\n"
            "- `long pop()` removes and returns the top element of the stack.\n"
            "- `void increment(int k, int delta)` adds `delta` (positive, zero, or negative) to the **bottom `k` elements** of the stack (if fewer than `k` elements exist, updates all elements in the stack).\n"
            "- `long top()` returns the current top element of the stack.\n"
            "- `long getMin()` returns the current minimum element in the stack."
        ),
        "cons": [
            "1 <= maxSize <= 2 * 10^4",
            "-10^9 <= val, delta <= 10^9, 0 <= k <= 10^5",
            "Methods pop, top, and getMin are always called on non-empty stacks.",
            "At most 2 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Unlike a plain increment stack, updating only the bottom `k` elements can change which index holds the global minimum.",
            "Back the stack slots `[0..maxSize - 1]` with a lazy-propagation range-minimum segment tree: `push` performs a point-assign at `size` (pushing down stale lazy tags along the root-to-leaf path), `increment(k, delta)` performs a range-add on `[0, min(k, size) - 1]`, and `getMin()` queries range-min on `[0, size - 1]`."
        ],
        "explanations": [
            "Push 2, 5, 1 -> [2, 5, 1] (min 1); increment(2, 10) -> [12, 15, 1] (min 1); pop returns 1 -> [12, 15] (min 12); increment(1, -20) -> [-8, 15] (min -8).",
            "Pushing beyond maxSize 2 is ignored; incrementing k=5 affects all 2 existing elements.",
            "Re-pushing into a previously popped slot overwrites its value cleanly without leaking old lazy offsets."
        ],
        "time": "O(log maxSize) per op",
        "space": "O(maxSize)",
        "kind": "design",
        "className": "IncrementableMinStack",
        "ctorParams": [("maxSize", "int")],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "long"),
            ("increment", [("k", "int"), ("delta", "int")], "void"),
            ("top", [], "long"),
            ("getMin", [], "long"),
        ],
        "py_class": """class IncrementableMinStack:
    def __init__(self, maxSize: int):
        self.cap = maxSize
        self.sz = 0
        self.mn = [0] * (4 * maxSize + 4)
        self.lazy = [0] * (4 * maxSize + 4)

    def _push_down(self, node: int) -> None:
        lz = self.lazy[node]
        if lz != 0:
            lc = node << 1
            rc = lc | 1
            self.mn[lc] += lz
            self.lazy[lc] += lz
            self.mn[rc] += lz
            self.lazy[rc] += lz
            self.lazy[node] = 0

    def _point_set(self, node: int, l: int, r: int, pos: int, val: int) -> None:
        if l == r:
            self.mn[node] = val
            self.lazy[node] = 0
            return
        self._push_down(node)
        mid = (l + r) >> 1
        if pos <= mid:
            self._point_set(node << 1, l, mid, pos, val)
        else:
            self._point_set((node << 1) | 1, mid + 1, r, pos, val)
        lc = node << 1
        a = self.mn[lc]
        b = self.mn[lc | 1]
        self.mn[node] = a if a < b else b

    def _range_add(self, node: int, l: int, r: int, ql: int, qr: int, delta: int) -> None:
        if ql <= l and r <= qr:
            self.mn[node] += delta
            self.lazy[node] += delta
            return
        self._push_down(node)
        mid = (l + r) >> 1
        if ql <= mid:
            self._range_add(node << 1, l, mid, ql, qr, delta)
        if qr > mid:
            self._range_add((node << 1) | 1, mid + 1, r, ql, qr, delta)
        lc = node << 1
        a = self.mn[lc]
        b = self.mn[lc | 1]
        self.mn[node] = a if a < b else b

    def _range_min(self, node: int, l: int, r: int, ql: int, qr: int) -> int:
        if ql <= l and r <= qr:
            return self.mn[node]
        self._push_down(node)
        mid = (l + r) >> 1
        if qr <= mid:
            return self._range_min(node << 1, l, mid, ql, qr)
        if ql > mid:
            return self._range_min((node << 1) | 1, mid + 1, r, ql, qr)
        a = self._range_min(node << 1, l, mid, ql, qr)
        b = self._range_min((node << 1) | 1, mid + 1, r, ql, qr)
        return a if a < b else b

    def push(self, val: int) -> None:
        if self.sz == self.cap:
            return
        self._point_set(1, 0, self.cap - 1, self.sz, val)
        self.sz += 1

    def pop(self) -> int:
        res = self._range_min(1, 0, self.cap - 1, self.sz - 1, self.sz - 1)
        self.sz -= 1
        return res

    def increment(self, k: int, delta: int) -> None:
        if self.sz == 0 or k <= 0 or delta == 0:
            return
        r = (k if k < self.sz else self.sz) - 1
        self._range_add(1, 0, self.cap - 1, 0, r, delta)

    def top(self) -> int:
        return self._range_min(1, 0, self.cap - 1, self.sz - 1, self.sz - 1)

    def getMin(self) -> int:
        return self._range_min(1, 0, self.cap - 1, 0, self.sz - 1)""",
        "java_class": """class IncrementableMinStack {
    private final int cap;
    private int sz;
    private final long[] mn;
    private final long[] lazy;

    public IncrementableMinStack(int maxSize) {
        this.cap = maxSize;
        this.sz = 0;
        this.mn = new long[4 * maxSize + 4];
        this.lazy = new long[4 * maxSize + 4];
    }

    private void pushDown(int node) {
        long lz = lazy[node];
        if (lz != 0L) {
            int lc = node << 1;
            int rc = lc | 1;
            mn[lc] += lz;
            lazy[lc] += lz;
            mn[rc] += lz;
            lazy[rc] += lz;
            lazy[node] = 0L;
        }
    }

    private void pointSet(int node, int l, int r, int pos, long val) {
        if (l == r) {
            mn[node] = val;
            lazy[node] = 0L;
            return;
        }
        pushDown(node);
        int mid = (l + r) >>> 1;
        if (pos <= mid) pointSet(node << 1, l, mid, pos, val);
        else pointSet((node << 1) | 1, mid + 1, r, pos, val);
        mn[node] = Math.min(mn[node << 1], mn[(node << 1) | 1]);
    }

    private void rangeAdd(int node, int l, int r, int ql, int qr, long delta) {
        if (ql <= l && r <= qr) {
            mn[node] += delta;
            lazy[node] += delta;
            return;
        }
        pushDown(node);
        int mid = (l + r) >>> 1;
        if (ql <= mid) rangeAdd(node << 1, l, mid, ql, qr, delta);
        if (qr > mid) rangeAdd((node << 1) | 1, mid + 1, r, ql, qr, delta);
        mn[node] = Math.min(mn[node << 1], mn[(node << 1) | 1]);
    }

    private long rangeMin(int node, int l, int r, int ql, int qr) {
        if (ql <= l && r <= qr) return mn[node];
        pushDown(node);
        int mid = (l + r) >>> 1;
        if (qr <= mid) return rangeMin(node << 1, l, mid, ql, qr);
        if (ql > mid) return rangeMin((node << 1) | 1, mid + 1, r, ql, qr);
        return Math.min(rangeMin(node << 1, l, mid, ql, qr), rangeMin((node << 1) | 1, mid + 1, r, ql, qr));
    }

    public void push(int val) {
        if (sz == cap) return;
        pointSet(1, 0, cap - 1, sz, val);
        sz++;
    }

    public long pop() {
        long res = rangeMin(1, 0, cap - 1, sz - 1, sz - 1);
        sz--;
        return res;
    }

    public void increment(int k, int delta) {
        if (sz == 0 || k <= 0 || delta == 0) return;
        int r = Math.min(k, sz) - 1;
        rangeAdd(1, 0, cap - 1, 0, r, delta);
    }

    public long top() {
        return rangeMin(1, 0, cap - 1, sz - 1, sz - 1);
    }

    public long getMin() {
        return rangeMin(1, 0, cap - 1, 0, sz - 1);
    }
}""",
        "visible": [
            {
                "ops": ["IncrementableMinStack", "push", "push", "push", "getMin", "increment", "getMin", "pop", "getMin", "increment", "getMin"],
                "args": [[5], [2], [5], [1], [], [2, 10], [], [], [], [1, -20], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "push", "push", "increment", "top", "getMin"],
                "args": [[2], [3], [7], [1], [5, -4], [], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "push", "increment", "pop", "push", "top", "getMin"],
                "args": [[3], [5], [10], [2, 3], [], [1], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["IncrementableMinStack", "push", "increment", "top", "getMin", "pop"],
                "args": [[1], [10], [1, -15], [], [], []],
            },
            {
                "ops": ["IncrementableMinStack", "increment", "push", "top", "getMin"],
                "args": [[4], [3, 100], [7], [], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "push", "push", "increment", "getMin", "increment", "getMin"],
                "args": [[4], [1], [2], [3], [1, 10], [], [2, 10], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "push", "increment", "increment", "top", "getMin"],
                "args": [[3], [1000000000], [1000000000], [2, 1000000000], [1, 1000000000], [], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "push", "push", "push", "increment", "pop", "pop", "getMin", "top"],
                "args": [[4], [10], [20], [30], [40], [3, -25], [], [], [], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "pop", "push", "increment", "push", "getMin", "top"],
                "args": [[2], [50], [], [5], [1, 10], [8], [], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "push", "push", "increment", "increment", "pop", "push", "getMin"],
                "args": [[5], [0], [0], [0], [0, 99], [2, -5], [], [-3], []],
            },
            {
                "ops": ["IncrementableMinStack", "push", "push", "push", "increment", "getMin", "pop", "getMin", "pop", "getMin"],
                "args": [[4], [-10], [5], [-2], [2, 20], [], [], [], [], []],
            },
            _perf_99(),
        ],
    },

    # ------------------------------------------------------------------
    # 100 - Min-Max Subarray Sum Stack
    # ------------------------------------------------------------------
    {
        "slug": "100-min-max-subarray-sum-stack",
        "title": "Min-Max Subarray Sum Stack",
        "difficulty": "Medium",
        "subtopic": "Min Stack",
        "companies": ["Google", "Meta", "Amazon", "Goldman Sachs"],
        "desc": (
            "Design a stack `MinMaxSubarrayStack` of signed integers that supports `push`, `pop`, `top`, and querying BOTH the **minimum** and **maximum sum of any non-empty contiguous subarray** currently in the stack (ordered from bottom to top), all in **`O(1)` time** per operation.\n\n"
            "Implement the `MinMaxSubarrayStack` class:\n"
            "- `MinMaxSubarrayStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes `val` onto the top of the stack.\n"
            "- `void pop()` removes the top element of the stack.\n"
            "- `int top()` returns the top element of the stack.\n"
            "- `long getMinSubarraySum()` returns the minimum sum over all non-empty contiguous segments of elements currently in the stack.\n"
            "- `long getMaxSubarraySum()` returns the maximum sum over all non-empty contiguous segments of elements currently in the stack."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Methods pop, top, getMinSubarraySum, and getMaxSubarraySum are always called on non-empty stacks.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Because pushing only appends at the top of the stack, Kadane's recurrence naturally augments each stack frame in O(1) time.",
            "Store `(val, curMinEnding, bestMin, curMaxEnding, bestMax)` per stack frame: pushing updates both Kadane states from the previous top, and popping automatically restores the exact prior states in O(1)."
        ],
        "explanations": [
            "Stack [3, -5, -2]: min subarray is [-5, -2] (-7) and max subarray is [3] (3). Pushing 10 raises max subarray to [10] (10); popping 10 restores max to 3.",
            "All-negative stack [-4, -1, -3]: min subarray is the whole stack (-8) and max subarray is [-1] (-1).",
            "Single element 7 has min subarray sum 7 and max subarray sum 7."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "MinMaxSubarrayStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "void"),
            ("top", [], "int"),
            ("getMinSubarraySum", [], "long"),
            ("getMaxSubarraySum", [], "long"),
        ],
        "py_class": """class MinMaxSubarrayStack:
    def __init__(self):
        # Each entry: (val, cur_min, best_min, cur_max, best_max)
        self.st = []

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, val, val, val))
        else:
            _, p_cmin, p_bmin, p_cmax, p_bmax = self.st[-1]
            cmin = val if val < p_cmin + val else p_cmin + val
            bmin = cmin if cmin < p_bmin else p_bmin
            cmax = val if val > p_cmax + val else p_cmax + val
            bmax = cmax if cmax > p_bmax else p_bmax
            self.st.append((val, cmin, bmin, cmax, bmax))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMinSubarraySum(self) -> int:
        return self.st[-1][2]

    def getMaxSubarraySum(self) -> int:
        return self.st[-1][4]""",
        "java_class": """class MinMaxSubarrayStack {
    private final List<long[]> st = new ArrayList<>();

    public MinMaxSubarrayStack() {
    }

    public void push(int val) {
        long v = val;
        if (st.isEmpty()) {
            st.add(new long[]{v, v, v, v, v});
        } else {
            long[] p = st.get(st.size() - 1);
            long cmin = Math.min(v, p[1] + v);
            long bmin = Math.min(p[2], cmin);
            long cmax = Math.max(v, p[3] + v);
            long bmax = Math.max(p[4], cmax);
            st.add(new long[]{v, cmin, bmin, cmax, bmax});
        }
    }

    public void pop() {
        st.remove(st.size() - 1);
    }

    public int top() {
        return (int) st.get(st.size() - 1)[0];
    }

    public long getMinSubarraySum() {
        return st.get(st.size() - 1)[2];
    }

    public long getMaxSubarraySum() {
        return st.get(st.size() - 1)[4];
    }
}""",
        "visible": [
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "push", "getMinSubarraySum", "getMaxSubarraySum", "push", "getMaxSubarraySum", "pop", "getMaxSubarraySum"],
                "args": [[], [3], [-5], [-2], [], [], [10], [], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "push", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [-4], [-1], [-3], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "top", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [7], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "push", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [2], [4], [6], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "push", "push", "getMinSubarraySum", "getMaxSubarraySum", "pop", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [5], [-3], [5], [-10], [], [], [], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [1000000000], [1000000000], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [-1000000000], [-1000000000], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "pop", "push", "push", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [100], [], [-2], [0], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "push", "push", "push", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [-2], [1], [-3], [4], [-1], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "push", "pop", "push", "getMinSubarraySum", "getMaxSubarraySum", "top"],
                "args": [[], [0], [0], [-1], [], [2], [], [], []],
            },
            {
                "ops": ["MinMaxSubarrayStack", "push", "push", "push", "push", "pop", "pop", "getMinSubarraySum", "getMaxSubarraySum"],
                "args": [[], [8], [-9], [4], [7], [], [], [], []],
            },
            _perf_100(),
        ],
    },
]


def main():
    assert len(TASKS) == 28, f"Expected 28 tasks, got {len(TASKS)}"
    expected_prefixes = list(range(73, 101))
    actual_prefixes = [int(t["slug"].split("-", 1)[0]) for t in TASKS]
    assert actual_prefixes == expected_prefixes, f"Prefix mismatch: {actual_prefixes}"

    existing_slugs: dict[str, Path] = {}
    existing_titles: dict[str, Path] = {}
    for p in (ROOT / "problems").rglob("problem.json"):
        m = re.match(r"^(\d{2,3})-(.+)$", p.parent.name)
        if m:
            existing_slugs[m.group(2)] = p.parent
        meta = json.loads(p.read_text(encoding="utf-8"))
        existing_titles[meta["title"].lower()] = p.parent

    for p in TASKS:
        assert p["subtopic"] in ALLOWED_SUBTOPICS, f"Bad subtopic {p['subtopic']}"
        for c in p["companies"]:
            assert c in ALLOWED_COMPANIES, f"Bad company {c}"
        assert len(p["visible"]) == 3, f"{p['slug']}: need 3 visible tests"
        assert len(p["hidden"]) == 9, f"{p['slug']}: need 9 hidden tests"
        assert len(p["explanations"]) == 3, f"{p['slug']}: need 3 example explanations"
        assert len(p["hints"]) >= 2, f"{p['slug']}: need at least 2 hints"
        assert len(p["desc"].strip()) >= 60, f"{p['slug']}: description too short"

        # Ensure all 12 test inputs are unique
        seen_inputs = set()
        for t in p["visible"] + p["hidden"]:
            key = json.dumps(t, sort_keys=True)
            assert key not in seen_inputs, f"{p['slug']}: duplicate test input {key[:120]}"
            seen_inputs.add(key)

        slug_only = p["slug"].split("-", 1)[1]
        folder = BASE / p["slug"]
        if slug_only in existing_slugs and existing_slugs[slug_only] != folder:
            raise AssertionError(f"Duplicate global slug '{slug_only}' already at {existing_slugs[slug_only]}")
        if p["title"].lower() in existing_titles and existing_titles[p["title"].lower()] != folder:
            raise AssertionError(f"Duplicate global title '{p['title']}' already at {existing_titles[p['title'].lower()]}")
        existing_slugs[slug_only] = folder
        existing_titles[p["title"].lower()] = folder

        folder.mkdir(parents=True, exist_ok=True)

        if p["kind"] == "function":
            params = [{"name": n, "type": t} for n, t in p["params"]]
            sig = {
                "kind": "function",
                "method": p["method"],
                "params": params,
                "returns": p["ret"],
            }
            pyparams = "".join(f", {n}: {py_type(t)}" for n, t in p["params"])
            py_src = (
                f"class Solution:\n"
                f"    def {p['method']}(self{pyparams}) -> {py_type(p['ret'])}:\n"
                + p["py"]
                + "\n"
            )
            jparams = ", ".join(f"{t} {n}" for n, t in p["params"])
            helpers = ("\n\n" + p["java_helpers"]) if p.get("java_helpers") else ""
            java_src = (
                f"class Solution {{\n"
                f"    public {p['ret']} {p['method']}({jparams}) {{\n"
                + p["java"]
                + f"\n    }}{helpers}\n}}\n"
            )
        elif p["kind"] == "design":
            ctor_params = [{"name": n, "type": t} for n, t in p["ctorParams"]]
            methods = [
                {
                    "name": mname,
                    "params": [{"name": pn, "type": pt} for pn, pt in mparams],
                    "returns": mret,
                }
                for mname, mparams, mret in p["methods"]
            ]
            sig = {
                "kind": "design",
                "className": p["className"],
                "constructor": {"params": ctor_params},
                "methods": methods,
            }
            py_src = p["py_class"].rstrip() + "\n"
            java_src = p["java_class"].rstrip() + "\n"
        else:
            raise ValueError(f"Unknown kind {p['kind']}")

        meta = {
            "title": p["title"],
            "difficulty": p["difficulty"],
            "subtopic": p["subtopic"],
            "companies": p["companies"],
            "description": p["desc"],
            "constraints": p["cons"],
            "hints": p["hints"],
            "examples": [{"explanation": e} for e in p["explanations"]],
            "timeComplexity": p["time"],
            "spaceComplexity": p["space"],
            "compare": p.get("compare", "exact"),
            "signature": sig,
        }
        (folder / "problem.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")
        (folder / "solution.py").write_text(py_src, encoding="utf-8")
        (folder / "Solution.java").write_text(java_src, encoding="utf-8")

        vis_code = repr([{"in": x} for x in p["visible"]])
        hid_code = repr([{"in": x} for x in p["hidden"]])
        (folder / "tests.py").write_text(
            f"def visible():\n    return {vis_code}\n\ndef hidden():\n    return {hid_code}\n",
            encoding="utf-8",
        )

    print(f"Generated {len(TASKS)} stack problems (73-100) in {BASE}")


if __name__ == "__main__":
    main()
