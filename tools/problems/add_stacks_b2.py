#!/usr/bin/env python3
"""Generate stacks problems 43-72 (batch 2) for AlgoPlay."""
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

def _perf_43():
    rng = random.Random(4301)
    chars = []
    letters = 0
    for _ in range(1200):
        if letters > 0 and rng.random() < 0.42:
            chars.append(str(rng.randint(0, 9)))
            letters -= 1
        else:
            chars.append(chr(ord("a") + rng.randint(0, 25)))
            letters += 1
    return "".join(chars)


def _perf_44():
    rng = random.Random(4401)
    s = "AB"
    for _ in range(400):
        pos = rng.randint(0, len(s))
        block = rng.choice(["AB", "CD", "EF"])
        s = s[:pos] + block + s[pos:]
    return s


def _perf_45():
    rng = random.Random(4501)
    primes = [2, 3, 5, 7, 11, 13]
    nums = []
    for _ in range(150):
        p = rng.choice(primes[:4])
        q = rng.choice(primes)
        nums.append(p * q)
        if rng.random() < 0.25:
            nums.append(rng.choice([17, 19, 23, 29, 31, 37, 41, 43]))
    return nums


def _perf_46():
    lines = ["root"]
    for i in range(1, 35):
        lines.append("\t" * i + f"dir{i:02d}")
        if i % 3 == 0:
            lines.append("\t" * (i + 1) + f"report_{i:02d}.txt")
    lines.append("\t" * 35 + "deepest_leaf_artifact_file.json")
    for j in range(10):
        lines.append(f"top{j}")
        lines.append(f"\tsub{j}")
        lines.append(f"\t\titem{j}.log")
    return "\n".join(lines)


def _perf_47():
    rng = random.Random(4701)
    digits = str(rng.randint(1, 9)) + "".join(str(rng.randint(0, 9)) for _ in range(1499))
    return {"num": digits, "k": 600}


def _perf_48():
    rng = random.Random(4801)
    ops = ["TextEditor"]
    args = [[]]
    words = ["abc", "defg", "xy", "hello", "stack", "gap", "edit", "z"]
    for _ in range(500):
        r = rng.random()
        if r < 0.4:
            ops.append("addText")
            args.append([rng.choice(words)])
        elif r < 0.6:
            ops.append("deleteText")
            args.append([rng.randint(1, 6)])
        elif r < 0.8:
            ops.append("cursorLeft")
            args.append([rng.randint(1, 10)])
        else:
            ops.append("cursorRight")
            args.append([rng.randint(1, 10)])
    return {"ops": ops, "args": args}


def _perf_49():
    rng = random.Random(4901)
    ops = ["DinnerPlates"]
    args = [[3]]
    for i in range(700):
        r = rng.random()
        if r < 0.52:
            ops.append("push")
            args.append([rng.randint(1, 10000)])
        elif r < 0.72:
            ops.append("pop")
            args.append([])
        else:
            ops.append("popAtStack")
            args.append([rng.randint(0, 60)])
    return {"ops": ops, "args": args}


def _perf_50():
    rng = random.Random(5001)
    target = 100000
    n = 600
    position = rng.sample(range(0, target), n)
    speed = [rng.randint(1, 50) for _ in range(n)]
    return {"target": target, "position": position, "speed": speed}


def _perf_51():
    rng = random.Random(5101)
    n = 400
    positions = sorted(rng.sample(range(1, 20000), n))
    cars = [[p, rng.randint(1, 40)] for p in positions]
    return {"cars": cars}


def _perf_52():
    parts = ["a"]
    for i in range(400):
        op = "+-*/"[i % 4]
        var = chr(ord("a") + (i % 26))
        if i % 7 == 0:
            parts = ["("] + parts + [op, var, ")"]
        else:
            parts.extend([op, "(", var, op, "b", ")"])
    return "".join(parts)


def _perf_53():
    rng = random.Random(5301)
    return "".join(rng.choice("()") for _ in range(1500))


def _perf_54():
    rng = random.Random(5401)
    pairs = [("(", ")"), ("[", "]"), ("{", "}")]
    chunks = []
    for _ in range(250):
        o, c = rng.choice(pairs)
        o2, c2 = rng.choice(pairs)
        chunks.append(o + o2 + c2 + c)
    return "".join(chunks) + "][()" * 50


def _perf_55():
    rng = random.Random(5501)
    pairs = [("(", ")"), ("[", "]"), ("{", "}")]
    s = "a"
    for _ in range(300):
        o, c = rng.choice(pairs)
        if rng.random() < 0.5:
            s = o + s + "x" + c
        else:
            s = s + o + "b" + c
    return s


def _perf_56():
    rng = random.Random(5601)
    return "".join(rng.choice("()") for _ in range(1600))


def _perf_57():
    blocks = ["10", "1100", "110100", "111000", "10"]
    return "1" + "".join(blocks * 6) + "0"


def _perf_58():
    rng = random.Random(5801)
    pairs = [("(", ")"), ("[", "]"), ("{", "}")]
    out = []
    for i in range(400):
        if i % 40 == 17:
            out.append(")")
        else:
            o, c = rng.choice(pairs)
            out.append(o + "()" + c)
    return "".join(out)


def _perf_59():
    rng = random.Random(5901)
    n = 600
    s_chars = []
    open_c = []
    close_c = []
    for i in range(n):
        r = rng.random()
        if r < 0.65:
            s_chars.append("?")
            open_c.append(rng.randint(1, 1000))
            close_c.append(rng.randint(1, 1000))
        elif r < 0.82:
            s_chars.append("(")
            open_c.append(0)
            close_c.append(0)
        else:
            s_chars.append(")")
            open_c.append(0)
            close_c.append(0)
    return {"s": "".join(s_chars), "openCost": open_c, "closeCost": close_c}


def _perf_60():
    rng = random.Random(6001)
    tokens = []
    n_blocks = 200
    for _ in range(n_blocks - 1):
        tokens.append(rng.choice(["+", "-"]))
    for _ in range(n_blocks):
        op = rng.choice(["+", "-", "*", "/"])
        tokens.append(op)
        tokens.append(str(rng.randint(-50, 50)))
        b = rng.randint(1, 20)
        tokens.append(str(b))
    return tokens


def _perf_61():
    rng = random.Random(6101)
    toks = ["a"]
    for i in range(1, 300):
        v = chr(ord("a") + (i % 26))
        op = rng.choice(["+", "-", "*"])
        toks.append(v)
        toks.append(op)
    return " ".join(toks)


def _perf_62():
    return "{a,b,c}{d,{e,f}}{g,h}{i,{j,k}}"


def _perf_63():
    expr = "(add x39 1)"
    for i in range(39, 0, -1):
        expr = f"(let x{i} (add x{i - 1} {i % 5 + 1}) {expr})"
    return f"(let x0 2 {expr})"


def _perf_64():
    rng = random.Random(6401)
    expr = "a"
    for i in range(1, 250):
        v = chr(ord("a") + (i % 26))
        op = rng.choice(["+", "-"])
        if rng.random() < 0.55:
            expr = f"{v}{op}({expr})"
        else:
            expr = f"({expr}){op}{v}"
    return expr


def _perf_65():
    parts = ["2^3^2"]
    for i in range(1, 150):
        op = "+-*"[i % 3]
        if i % 5 == 0:
            parts.append(f"{op}(1+2)^3")
        else:
            parts.append(f"{op}{i % 7 + 1}^{i % 4}")
    return "".join(parts)


def _perf_66():
    s = "[1,-2,3]"
    for i in range(4, 150):
        val = i if i % 2 == 0 else -i
        if i % 3 == 0:
            s = f"[{val},{s}]"
        else:
            s = f"[{s},{val}]"
    return s


def _perf_67():
    rng = random.Random(6701)
    ops = ["MinQueue"]
    args = [[]]
    sz = 0
    for _ in range(800):
        if sz == 0 or rng.random() < 0.55:
            ops.append("enqueue")
            args.append([rng.randint(-10**6, 10**6)])
            sz += 1
        else:
            choice = rng.choice(["dequeue", "front", "getMin"])
            ops.append(choice)
            args.append([])
            if choice == "dequeue":
                sz -= 1
    return {"ops": ops, "args": args}


def _perf_68():
    rng = random.Random(6801)
    ops = ["OffsetMinStack"]
    args = [[]]
    sz = 0
    for _ in range(800):
        r = rng.random()
        if sz == 0 or r < 0.42:
            ops.append("push")
            args.append([rng.randint(-10**6, 10**6)])
            sz += 1
        elif r < 0.62:
            ops.append("addAll")
            args.append([rng.randint(-10**5, 10**5)])
        elif r < 0.76:
            ops.append("pop")
            args.append([])
            sz -= 1
        elif r < 0.88:
            ops.append("top")
            args.append([])
        else:
            ops.append("getMin")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_69():
    rng = random.Random(6901)
    ops = ["TransactionalStack"]
    args = [[]]
    st = []
    tx = []
    for _ in range(750):
        r = rng.random()
        if len(st) == 0 or r < 0.36:
            v = rng.randint(-10000, 10000)
            ops.append("push")
            args.append([v])
            st.append(v)
            if tx:
                tx[-1].append(("pop", 0))
        elif r < 0.50:
            ops.append("pop")
            args.append([])
            v = st.pop()
            if tx:
                tx[-1].append(("push", v))
        elif r < 0.62:
            ops.append("begin")
            args.append([])
            tx.append([])
        elif r < 0.72:
            ops.append("rollback")
            args.append([])
            if tx:
                for kind, val in reversed(tx.pop()):
                    if kind == "pop":
                        st.pop()
                    else:
                        st.append(val)
        elif r < 0.80:
            ops.append("commit")
            args.append([])
            if tx:
                log = tx.pop()
                if tx:
                    tx[-1].extend(log)
        elif r < 0.90:
            ops.append("top")
            args.append([])
        else:
            ops.append("getMin")
            args.append([])
    return {"ops": ops, "args": args}


def _perf_70():
    rng = random.Random(7001)
    ops = ["SecondMinStack"]
    args = [[]]
    sz = 0
    for _ in range(800):
        if sz < 2 or rng.random() < 0.55:
            ops.append("push")
            args.append([rng.randint(-10**6, 10**6)])
            sz += 1
        else:
            choice = rng.choice(["pop", "top", "getMin", "getSecondMin"])
            ops.append(choice)
            args.append([])
            if choice == "pop":
                sz -= 1
    return {"ops": ops, "args": args}


def _perf_71():
    rng = random.Random(7101)
    ops = ["CountMinStack"]
    args = [[]]
    sz = 0
    for _ in range(800):
        if sz == 0 or rng.random() < 0.55:
            ops.append("push")
            args.append([rng.randint(-20, 20)])
            sz += 1
        else:
            choice = rng.choice(["pop", "top", "getMin", "getMinCount"])
            ops.append(choice)
            args.append([])
            if choice == "pop":
                sz -= 1
    return {"ops": ops, "args": args}


def _perf_72():
    rng = random.Random(7201)
    ops = ["PersistentMinStack"]
    args = [[]]
    sizes = [0]
    for _ in range(700):
        non_empty = [v for v, s in enumerate(sizes) if s > 0]
        r = rng.random()
        if not non_empty or r < 0.48:
            base = rng.randrange(len(sizes))
            ops.append("push")
            args.append([base, rng.randint(-10**6, 10**6)])
            sizes.append(sizes[base] + 1)
        elif r < 0.68:
            base = rng.choice(non_empty)
            ops.append("pop")
            args.append([base])
            sizes.append(sizes[base] - 1)
        elif r < 0.84:
            base = rng.choice(non_empty)
            ops.append("top")
            args.append([base])
        else:
            base = rng.choice(non_empty)
            ops.append("getMin")
            args.append([base])
    return {"ops": ops, "args": args}


TASKS = [
    # ------------------------------------------------------------------
    # 43 - Clear Digits With Left Letters
    # ------------------------------------------------------------------
    {
        "slug": "43-clear-digits-with-left-letters",
        "title": "Clear Digits With Left Letters",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": (
            "You are given a string `s` consisting of lowercase English letters and digits (`'0'`-`'9'`).\n\n"
            "Repeatedly perform the following operation while any digit remains in `s`:\n"
            "- Find the leftmost digit in `s` and delete it, together with the closest remaining non-digit character to its left (if one exists).\n\n"
            "Return the resulting string after all digits have been removed."
        ),
        "cons": [
            "1 <= s.length <= 10^4",
            "s consists only of lowercase English letters and digits '0'-'9'."
        ],
        "hints": [
            "Process characters from left to right using a stack of surviving letters.",
            "Push each letter onto the stack; whenever you see a digit, pop the top letter if the stack is non-empty."
        ],
        "explanations": [
            "\"abc\" has no digits, so all characters remain.",
            "Digit '3' removes 'b' (leaving \"c4\"), then digit '4' removes 'c', leaving \"\".",
            "Digit '1' removes 'b' and digit '2' removes 'a', leaving \"cd\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "clearDigits",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        stack = []
        for ch in s:
            if ch.isdigit():
                if stack:
                    stack.pop()
            else:
                stack.append(ch)
        return "".join(stack)""",
        "java": """        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (Character.isDigit(ch)) {
                if (sb.length() > 0) sb.deleteCharAt(sb.length() - 1);
            } else {
                sb.append(ch);
            }
        }
        return sb.toString();""",
        "visible": [
            {"s": "abc"},
            {"s": "cb34"},
            {"s": "ab12cd"},
        ],
        "hidden": [
            {"s": "a"},
            {"s": "9"},
            {"s": "123abc"},
            {"s": "a1b2c3"},
            {"s": "ab1c2d3e"},
            {"s": "xyz987"},
            {"s": "a99b8c"},
            {"s": "leet2code34"},
            {"s": _perf_43()},
        ],
    },

    # ------------------------------------------------------------------
    # 44 - Minimum String Length After AB and CD Removals
    # ------------------------------------------------------------------
    {
        "slug": "44-minimum-string-length-after-ab-cd-removals",
        "title": "Minimum String Length After AB and CD Removals",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Amazon", "Microsoft", "Adobe"],
        "desc": (
            "You are given a string `s` consisting only of uppercase English letters.\n\n"
            "In one operation, you may remove any occurrence of either the substring `\"AB\"` or the substring `\"CD\"` from `s`. "
            "After a removal, the remaining left and right parts concatenate directly, which may form new `\"AB\"` or `\"CD\"` substrings.\n\n"
            "Return the minimum possible length of the resulting string after performing any number of operations."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists only of uppercase English letters."
        ],
        "hints": [
            "Because \"AB\" and \"CD\" use disjoint pairs of characters, greedily cancelling them as soon as they meet is always optimal.",
            "Scan left to right with a stack: pop when the stack top and current character form \"AB\" or \"CD\", otherwise push."
        ],
        "explanations": [
            "Removing \"AB\" yields \"FCACDB\", removing \"CD\" yields \"FCAB\", and removing \"AB\" leaves \"FC\" of length 2.",
            "No \"AB\" or \"CD\" substring can ever be formed, so length stays 5.",
            "Inner \"CD\" cancels first, bringing 'A' and 'B' together so they also cancel, leaving length 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "minLength",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        stack = []
        for ch in s:
            if stack and ((stack[-1] == 'A' and ch == 'B') or (stack[-1] == 'C' and ch == 'D')):
                stack.pop()
            else:
                stack.append(ch)
        return len(stack)""",
        "java": """        char[] st = new char[s.length()];
        int top = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (top > 0 && ((st[top - 1] == 'A' && ch == 'B') || (st[top - 1] == 'C' && ch == 'D'))) {
                top--;
            } else {
                st[top++] = ch;
            }
        }
        return top;""",
        "visible": [
            {"s": "ABFCACDB"},
            {"s": "ACBBD"},
            {"s": "ACDB"},
        ],
        "hidden": [
            {"s": "A"},
            {"s": "AB"},
            {"s": "CD"},
            {"s": "BA"},
            {"s": "AACDBB"},
            {"s": "CCABDD"},
            {"s": "ABCDABCD"},
            {"s": "AAACCCDDDBBB"},
            {"s": _perf_44()},
        ],
    },

    # ------------------------------------------------------------------
    # 45 - Replace Non-Coprime Numbers in Array
    # ------------------------------------------------------------------
    {
        "slug": "45-replace-non-coprime-numbers-in-array",
        "title": "Replace Non-Coprime Numbers in Array",
        "difficulty": "Hard",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Meta", "Bloomberg"],
        "desc": (
            "You are given an array of positive integers `nums`. Repeatedly perform the following steps until no valid pair remains:\n"
            "1. Find any two adjacent numbers in `nums` that are **non-coprime** (i.e., `gcd(x, y) > 1`).\n"
            "2. Delete both numbers and replace them with their least common multiple `lcm(x, y)`.\n\n"
            "It can be proven that the final array is identical regardless of the order in which adjacent non-coprime pairs are merged. "
            "Return the final modified array. It is guaranteed that all values in the final array are at most `10^8`."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "1 <= nums[i] <= 10^5",
            "All values in the final array are at most 10^8."
        ],
        "hints": [
            "Maintain a stack representing the reduced prefix of the array.",
            "When processing x, repeatedly pop the stack top y while gcd(y, x) > 1 and set x = lcm(y, x), then push x."
        ],
        "explanations": [
            "[6,4] merges to 12, [12,3] merges to 12, then [2,7,6] stays until [6,2] merges to 6; final array is [12,7,6].",
            "All adjacent merges collapse [2,2,1,1,3,3,3] into [2,1,1,3].",
            "Merging 6 and 4 gives 12, then merging 12 with 9 gives 36, and 36 with 5 is coprime."
        ],
        "time": "O(n log M)",
        "space": "O(n)",
        "kind": "function",
        "method": "replaceNonCoprimes",
        "params": [("nums", "int[]")],
        "ret": "List<Integer>",
        "py": """        def gcd(a: int, b: int) -> int:
            while b:
                a, b = b, a % b
            return a

        stack = []
        for x in nums:
            cur = x
            while stack:
                g = gcd(stack[-1], cur)
                if g == 1:
                    break
                cur = (stack.pop() // g) * cur
            stack.append(cur)
        return stack""",
        "java": """        List<Integer> stack = new ArrayList<>();
        for (int x : nums) {
            long cur = x;
            while (!stack.isEmpty()) {
                long top = stack.get(stack.size() - 1);
                long g = gcd(top, cur);
                if (g == 1) break;
                stack.remove(stack.size() - 1);
                cur = (top / g) * cur;
            }
            stack.add((int) cur);
        }
        return stack;""",
        "java_helpers": """    private long gcd(long a, long b) {
        while (b != 0) {
            long t = a % b;
            a = b;
            b = t;
        }
        return a;
    }""",
        "visible": [
            {"nums": [6, 4, 3, 2, 7, 6, 2]},
            {"nums": [2, 2, 1, 1, 3, 3, 3]},
            {"nums": [6, 4, 9, 5]},
        ],
        "hidden": [
            {"nums": [1]},
            {"nums": [2, 3, 5, 7, 11]},
            {"nums": [2, 4, 8, 16, 32]},
            {"nums": [287, 41, 49, 287, 899, 23, 23, 20677, 5, 825]},
            {"nums": [3, 5, 15, 7, 21]},
            {"nums": [12, 18, 25, 10, 4]},
            {"nums": [6, 10, 15]},
            {"nums": [100, 1, 100, 50, 25]},
            {"nums": _perf_45()},
        ],
    },

    # ------------------------------------------------------------------
    # 46 - Longest Absolute File Path
    # ------------------------------------------------------------------
    {
        "slug": "46-longest-absolute-file-path",
        "title": "Longest Absolute File Path",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Apple", "Microsoft"],
        "desc": (
            "Suppose a file system is serialized into a string `input` where entries are separated by newline characters `'\\n'`, "
            "and the nesting depth of each entry is given by the number of leading tab characters `'\\t'`.\n\n"
            "- A directory name contains no period `'.'`, whereas a file name always contains at least one period `'.'` (e.g., `\"file.ext\"`).\n"
            "- Every entry at depth `d > 0` belongs to the most recent preceding directory at depth `d - 1`.\n"
            "- The absolute path of an entry joins its ancestor directories and its own name with single `'/'` separators.\n\n"
            "Return the length of the longest absolute path to a **file** in the file system. If there are no files, return `0`."
        ),
        "cons": [
            "1 <= input.length <= 10^4",
            "input contains English letters, digits, spaces, '.', '_', '\\n', and '\\t'."
        ],
        "hints": [
            "Use a stack storing the cumulative path length (including trailing '/') at each active directory depth.",
            "For each line, count leading '\\t' characters to get depth, pop the stack down to that depth, and update the answer if the entry contains '.'."
        ],
        "explanations": [
            "\"dir/subdir2/file.ext\" has length 20, which is longer than \"dir/subdir1\" (not a file).",
            "\"dir/subdir2/subsubdir2/file2.ext\" has length 32.",
            "\"a\" is a directory and contains no files, so the answer is 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "lengthLongestPath",
        "params": [("input", "String")],
        "ret": "int",
        "py": """        stack = [0]
        best = 0
        for line in input.split('\\n'):
            depth = 0
            while depth < len(line) and line[depth] == '\\t':
                depth += 1
            name = line[depth:]
            while len(stack) > depth + 1:
                stack.pop()
            cur_len = stack[-1] + len(name)
            if '.' in name:
                if cur_len > best:
                    best = cur_len
            else:
                stack.append(cur_len + 1)
        return best""",
        "java": """        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(0);
        int best = 0;
        String[] lines = input.split("\\n");
        for (String line : lines) {
            int depth = 0;
            while (depth < line.length() && line.charAt(depth) == '\\t') {
                depth++;
            }
            String name = line.substring(depth);
            while (stack.size() > depth + 1) {
                stack.pop();
            }
            int curLen = stack.peek() + name.length();
            if (name.indexOf('.') >= 0) {
                if (curLen > best) best = curLen;
            } else {
                stack.push(curLen + 1);
            }
        }
        return best;""",
        "visible": [
            {"input": "dir\n\tsubdir1\n\tsubdir2\n\t\tfile.ext"},
            {"input": "dir\n\tsubdir1\n\t\tfile1.ext\n\t\tsubsubdir1\n\tsubdir2\n\t\tsubsubdir2\n\t\t\tfile2.ext"},
            {"input": "a"},
        ],
        "hidden": [
            {"input": "file.txt"},
            {"input": "a\n\tb\n\t\tc"},
            {"input": "a\n\tb.txt\na2\n\tb2.txt"},
            {"input": "dir\n\t        file.txt\n\tfile2.txt"},
            {"input": "root\n\ta\n\t\tb\n\t\t\tc.py\n\tlongerdirectoryname\n\t\tx.c"},
            {"input": "a\n\tb1\n\t\tf1.txt\n\t\t\tignored\n\tb2\n\t\tf2.txt"},
            {"input": "top1.a\ntop2.longext\ndir\n\ta.b"},
            {"input": "d1\n\td2\n\t\td3\n\t\t\td4\n\t\t\t\timg.png\nd5\n\tshort.md"},
            {"input": _perf_46()},
        ],
    },

    # ------------------------------------------------------------------
    # 47 - Remove K Digits
    # ------------------------------------------------------------------
    {
        "slug": "47-remove-k-digits",
        "title": "Remove K Digits",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Given a non-negative integer represented as a string of digits `num` and an integer `k`, remove exactly `k` digits from `num` so that the resulting number is the **smallest possible**.\n\n"
            "Return the resulting number as a string with no leading zeros (if all digits are removed or only zeros remain, return `\"0\"`)."
        ),
        "cons": [
            "1 <= k <= num.length <= 10^5",
            "num consists only of digits '0'-'9' and has no leading zeros except possibly \"0\" itself."
        ],
        "hints": [
            "Iterate through the digits left to right using a monotonic increasing stack: whenever the current digit is smaller than the stack top and k > 0, pop the larger digit and decrement k.",
            "If k > 0 after processing all digits, pop the remaining k digits from the end of the stack, strip leading zeros, and return \"0\" if empty."
        ],
        "explanations": [
            "Removing digits 4, 3, and 2 from \"1432219\" yields the smallest possible number \"1219\".",
            "Removing the leading '1' from \"10200\" leaves \"0200\", which strips leading zeros to \"200\".",
            "Removing all 2 digits from \"10\" leaves nothing, so return \"0\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "removeKdigits",
        "params": [("num", "String"), ("k", "int")],
        "ret": "String",
        "py": """        stack = []
        rem = k
        for ch in num:
            while rem > 0 and stack and stack[-1] > ch:
                stack.pop()
                rem -= 1
            stack.append(ch)
        if rem > 0:
            stack = stack[:-rem]
        res = "".join(stack).lstrip("0")
        return res if res else "0"
""",
        "java": """        int n = num.length();
        char[] st = new char[n];
        int top = 0;
        int rem = k;
        for (int i = 0; i < n; i++) {
            char ch = num.charAt(i);
            while (rem > 0 && top > 0 && st[top - 1] > ch) {
                top--;
                rem--;
            }
            st[top++] = ch;
        }
        top -= rem;
        int start = 0;
        while (start < top && st[start] == '0') start++;
        return start == top ? "0" : new String(st, start, top - start);""",
        "visible": [
            {"num": "1432219", "k": 3},
            {"num": "10200", "k": 1},
            {"num": "10", "k": 2},
        ],
        "hidden": [
            {"num": "9", "k": 1},
            {"num": "112", "k": 1},
            {"num": "123456", "k": 3},
            {"num": "654321", "k": 3},
            {"num": "10001", "k": 4},
            {"num": "10001", "k": 1},
            {"num": "5337", "k": 2},
            {"num": "9999999999", "k": 5},
            _perf_47(),
        ],
    },

    # ------------------------------------------------------------------
    # 48 - Design Text Editor With Cursor
    # ------------------------------------------------------------------
    {
        "slug": "48-design-text-editor-with-cursor",
        "title": "Design Text Editor With Cursor",
        "difficulty": "Hard",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Meta", "Microsoft", "Atlassian", "Amazon"],
        "desc": (
            "Design a text editor with a movable cursor that supports inserting, deleting, and navigating text efficiently.\n\n"
            "Implement the `TextEditor` class:\n"
            "- `TextEditor()` initializes the editor with empty text and the cursor at position `0`.\n"
            "- `void addText(String text)` inserts `text` immediately to the left of the cursor; the cursor ends up right after the inserted text.\n"
            "- `int deleteText(int k)` deletes up to `k` characters immediately to the left of the cursor and returns the number of characters actually deleted.\n"
            "- `String cursorLeft(int k)` moves the cursor up to `k` positions to the left and returns the last `min(10, len)` characters to the left of the cursor.\n"
            "- `String cursorRight(int k)` moves the cursor up to `k` positions to the right and returns the last `min(10, len)` characters to the left of the cursor."
        ),
        "cons": [
            "1 <= text.length, k <= 40",
            "text consists of lowercase English letters.",
            "At most 2 * 10^4 calls in total will be made to addText, deleteText, cursorLeft, and cursorRight."
        ],
        "hints": [
            "Represent the buffer as two stacks (a gap buffer): leftStack holds characters before the cursor and rightStack holds characters after the cursor in reverse order.",
            "addText pushes onto leftStack, deleteText pops from leftStack, cursorLeft moves characters from leftStack to rightStack, and cursorRight moves from rightStack to leftStack."
        ],
        "explanations": [
            "Typing \"leetcode\", deleting 4 leaves \"leet\", adding \"practice\" gives \"leetpractice\", moving left/right and deleting updates the cursor window.",
            "Deleting or moving past the left/right edges cleanly stops at the boundary.",
            "When more than 10 characters exist left of the cursor, cursorLeft and cursorRight return only the 10 characters closest to the cursor."
        ],
        "time": "O(text.length) / O(k) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "TextEditor",
        "ctorParams": [],
        "methods": [
            ("addText", [("text", "String")], "void"),
            ("deleteText", [("k", "int")], "int"),
            ("cursorLeft", [("k", "int")], "String"),
            ("cursorRight", [("k", "int")], "String"),
        ],
        "py_class": """class TextEditor:
    def __init__(self):
        self.left = []
        self.right = []

    def addText(self, text: str) -> None:
        self.left.extend(text)

    def deleteText(self, k: int) -> int:
        cnt = min(k, len(self.left))
        for _ in range(cnt):
            self.left.pop()
        return cnt

    def cursorLeft(self, k: int) -> str:
        moves = min(k, len(self.left))
        for _ in range(moves):
            self.right.append(self.left.pop())
        return "".join(self.left[-10:])

    def cursorRight(self, k: int) -> str:
        moves = min(k, len(self.right))
        for _ in range(moves):
            self.left.append(self.right.pop())
        return "".join(self.left[-10:])""",
        "java_class": """class TextEditor {
    private final StringBuilder left = new StringBuilder();
    private final StringBuilder right = new StringBuilder();

    public TextEditor() {}

    public void addText(String text) {
        left.append(text);
    }

    public int deleteText(int k) {
        int cnt = Math.min(k, left.length());
        left.setLength(left.length() - cnt);
        return cnt;
    }

    public String cursorLeft(int k) {
        int moves = Math.min(k, left.length());
        for (int i = 0; i < moves; i++) {
            int last = left.length() - 1;
            right.append(left.charAt(last));
            left.setLength(last);
        }
        return leftTail();
    }

    public String cursorRight(int k) {
        int moves = Math.min(k, right.length());
        for (int i = 0; i < moves; i++) {
            int last = right.length() - 1;
            left.append(right.charAt(last));
            right.setLength(last);
        }
        return leftTail();
    }

    private String leftTail() {
        int start = Math.max(0, left.length() - 10);
        return left.substring(start);
    }
}""",
        "visible": [
            {
                "ops": ["TextEditor", "addText", "deleteText", "addText", "cursorRight", "cursorLeft", "deleteText", "cursorLeft", "cursorRight"],
                "args": [[], ["leetcode"], [4], ["practice"], [3], [8], [10], [2], [6]],
            },
            {
                "ops": ["TextEditor", "deleteText", "cursorLeft", "cursorRight", "addText", "cursorLeft", "deleteText"],
                "args": [[], [5], [3], [3], ["hi"], [5], [2]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "cursorRight", "cursorLeft"],
                "args": [[], ["abcdefghijklmnop"], [3], [1], [12]],
            },
        ],
        "hidden": [
            {
                "ops": ["TextEditor", "addText", "deleteText", "deleteText"],
                "args": [[], ["abc"], [2], [5]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "addText", "cursorRight"],
                "args": [[], ["world"], [5], ["hello"], [5]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "deleteText", "cursorRight", "cursorLeft"],
                "args": [[], ["abcdef"], [2], [2], [10], [1]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "addText", "deleteText", "cursorRight"],
                "args": [[], ["1234567890".replace("1", "a").replace("2", "b").replace("3", "c").replace("4", "d").replace("5", "e").replace("6", "f").replace("7", "g").replace("8", "h").replace("9", "i").replace("0", "j")], [5], ["xyz"], [2], [10]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "addText", "cursorLeft", "addText", "cursorRight"],
                "args": [[], ["cc"], [1], ["bb"], [1], ["aa"], [10]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "deleteText", "addText", "cursorRight", "deleteText"],
                "args": [[], ["algorithm"], [4], [10], ["data"], [10], [3]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "cursorRight", "deleteText", "cursorLeft"],
                "args": [[], ["zzzzzzzzzzzz"], [1], [1], [12], [1]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "addText", "cursorRight", "deleteText", "cursorLeft"],
                "args": [[], ["stack"], [2], ["min"], [1], [4], [2]],
            },
            _perf_48(),
        ],
    },

    # ------------------------------------------------------------------
    # 49 - Dinner Plate Stacks
    # ------------------------------------------------------------------
    {
        "slug": "49-dinner-plate-stacks",
        "title": "Dinner Plate Stacks",
        "difficulty": "Hard",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Bloomberg", "Uber"],
        "desc": (
            "You have an infinite sequence of stacks arranged left-to-right at indices `0, 1, 2, ...`, where every stack has the same fixed maximum `capacity`.\n\n"
            "Implement the `DinnerPlates` class:\n"
            "- `DinnerPlates(int capacity)` initializes the object with maximum stack capacity `capacity`.\n"
            "- `void push(int val)` pushes `val` onto the **leftmost** stack whose current size is strictly less than `capacity`.\n"
            "- `int pop()` removes and returns the top value of the **rightmost** non-empty stack, or returns `-1` if all stacks are empty.\n"
            "- `int popAtStack(int index)` removes and returns the top value of the stack at `index`, or returns `-1` if that stack is empty or does not exist."
        ),
        "cons": [
            "1 <= capacity <= 2 * 10^4",
            "1 <= val <= 2 * 10^4",
            "0 <= index <= 10^5",
            "At most 2 * 10^5 calls will be made in total to push, pop, and popAtStack."
        ],
        "hints": [
            "Maintain a list of stacks together with a min-heap of stack indices that currently have room below capacity.",
            "Lazily pop empty trailing stacks on pop/popAtStack, and lazily discard stale heap indices (out-of-bounds or full) during push."
        ],
        "explanations": [
            "Pushing 1..5 fills stacks [1,2], [3,4], [5]; popAtStack(0) returns 2 leaving space at stack 0 so push(20) goes to stack 0 and push(21) goes to stack 2.",
            "Popping from an empty structure or an out-of-range stack index returns -1.",
            "With capacity 1, each element occupies its own stack and popping middle stacks opens leftmost slots for subsequent pushes."
        ],
        "time": "O(log n) amortized per op",
        "space": "O(n)",
        "kind": "design",
        "className": "DinnerPlates",
        "ctorParams": [("capacity", "int")],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "int"),
            ("popAtStack", [("index", "int")], "int"),
        ],
        "py_class": """import heapq

class DinnerPlates:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.stacks = []
        self.avail = []

    def push(self, val: int) -> None:
        while self.avail and (self.avail[0] >= len(self.stacks) or len(self.stacks[self.avail[0]]) == self.cap):
            heapq.heappop(self.avail)
        if self.avail:
            idx = self.avail[0]
            self.stacks[idx].append(val)
            if len(self.stacks[idx]) == self.cap:
                heapq.heappop(self.avail)
        else:
            self.stacks.append([val])
            if self.cap > 1:
                heapq.heappush(self.avail, len(self.stacks) - 1)

    def pop(self) -> int:
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        if not self.stacks:
            return -1
        idx = len(self.stacks) - 1
        val = self.stacks[idx].pop()
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        if idx < len(self.stacks):
            heapq.heappush(self.avail, idx)
        return val

    def popAtStack(self, index: int) -> int:
        if index < 0 or index >= len(self.stacks) or not self.stacks[index]:
            return -1
        val = self.stacks[index].pop()
        while self.stacks and not self.stacks[-1]:
            self.stacks.pop()
        if index < len(self.stacks):
            heapq.heappush(self.avail, index)
        return val""",
        "java_class": """class DinnerPlates {
    private final int cap;
    private final List<Deque<Integer>> stacks = new ArrayList<>();
    private final PriorityQueue<Integer> avail = new PriorityQueue<>();

    public DinnerPlates(int capacity) {
        this.cap = capacity;
    }

    public void push(int val) {
        while (!avail.isEmpty() && (avail.peek() >= stacks.size() || stacks.get(avail.peek()).size() == cap)) {
            avail.poll();
        }
        if (!avail.isEmpty()) {
            int idx = avail.peek();
            stacks.get(idx).push(val);
            if (stacks.get(idx).size() == cap) {
                avail.poll();
            }
        } else {
            Deque<Integer> st = new ArrayDeque<>();
            st.push(val);
            stacks.add(st);
            if (cap > 1) {
                avail.offer(stacks.size() - 1);
            }
        }
    }

    public int pop() {
        while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) {
            stacks.remove(stacks.size() - 1);
        }
        if (stacks.isEmpty()) return -1;
        int idx = stacks.size() - 1;
        int val = stacks.get(idx).pop();
        while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) {
            stacks.remove(stacks.size() - 1);
        }
        if (idx < stacks.size()) {
            avail.offer(idx);
        }
        return val;
    }

    public int popAtStack(int index) {
        if (index < 0 || index >= stacks.size() || stacks.get(index).isEmpty()) {
            return -1;
        }
        int val = stacks.get(index).pop();
        while (!stacks.isEmpty() && stacks.get(stacks.size() - 1).isEmpty()) {
            stacks.remove(stacks.size() - 1);
        }
        if (index < stacks.size()) {
            avail.offer(index);
        }
        return val;
    }
}""",
        "visible": [
            {
                "ops": ["DinnerPlates", "push", "push", "push", "push", "push", "popAtStack", "push", "push", "popAtStack", "popAtStack", "pop", "pop", "pop", "pop", "pop"],
                "args": [[2], [1], [2], [3], [4], [5], [0], [20], [21], [0], [2], [], [], [], [], []],
            },
            {
                "ops": ["DinnerPlates", "pop", "popAtStack", "push", "popAtStack", "pop"],
                "args": [[3], [], [0], [7], [1], []],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "push", "popAtStack", "push", "popAtStack", "pop", "pop"],
                "args": [[1], [10], [20], [30], [1], [25], [1], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["DinnerPlates", "push", "pop", "push", "pop"],
                "args": [[1], [4], [], [8], []],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "push", "popAtStack", "popAtStack", "pop", "push", "pop"],
                "args": [[2], [1], [2], [3], [0], [0], [], [9], []],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "push", "push", "popAtStack", "pop", "pop", "push", "popAtStack"],
                "args": [[1], [5], [6], [7], [8], [0], [], [], [99], [0]],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "push", "push", "push", "push", "popAtStack", "popAtStack", "popAtStack", "push", "push", "pop"],
                "args": [[2], [1], [2], [3], [4], [5], [6], [1], [1], [0], [10], [11], []],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "popAtStack", "popAtStack", "popAtStack", "pop"],
                "args": [[2], [11], [22], [0], [0], [0], []],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "push", "popAtStack", "popAtStack", "pop", "pop", "pop"],
                "args": [[3], [1], [2], [3], [5], [0], [], [], []],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "push", "push", "popAtStack", "pop", "pop", "push", "push", "pop", "pop"],
                "args": [[2], [1], [2], [3], [4], [0], [], [], [7], [8], [], []],
            },
            {
                "ops": ["DinnerPlates", "push", "push", "push", "push", "push", "popAtStack", "popAtStack", "pop", "pop", "pop", "pop"],
                "args": [[1], [1], [2], [3], [4], [5], [2], [1], [], [], [], []],
            },
            _perf_49(),
        ],
    },

    # ------------------------------------------------------------------
    # 50 - Car Fleet Count
    # ------------------------------------------------------------------
    {
        "slug": "50-car-fleet-count",
        "title": "Car Fleet Count",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Meta", "Uber", "Bloomberg"],
        "desc": (
            "There are `n` cars driving along a one-lane highway toward a destination at mile `target`. "
            "Car `i` starts at mile `position[i]` and moves at constant speed `speed[i]` miles per hour.\n\n"
            "A car cannot pass another car ahead of it; if a faster car catches up to a slower car (at or before `target`), they merge into a single **car fleet** moving at the slower car's speed.\n\n"
            "Return the total number of distinct car fleets that arrive at `target`."
        ),
        "cons": [
            "1 <= position.length == speed.length <= 10^5",
            "0 < target <= 10^6",
            "0 <= position[i] < target and all position[i] are distinct.",
            "1 <= speed[i] <= 10^6"
        ],
        "hints": [
            "Sort cars in descending order of starting position so you inspect them from closest to target to farthest.",
            "Maintain a stack of arrival times: if a trailing car's arrival time is <= the stack top, it merges into that fleet; otherwise push its arrival time as a new fleet."
        ],
        "explanations": [
            "Cars at 10 (time 1) and 8 (time 1) meet at 12; car at 5 (time 7) and car at 3 (time 3) merge; car at 0 (time 12) arrives alone, making 3 fleets.",
            "A single car always forms 1 fleet.",
            "Car at 4 arrives in 48h, car at 2 arrives in 32.67h (catches car at 4), and car at 0 arrives in 25h (also catches up), yielding 1 fleet."
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "kind": "function",
        "method": "carFleet",
        "params": [("target", "int"), ("position", "int[]"), ("speed", "int[]")],
        "ret": "int",
        "py": """        cars = sorted(zip(position, speed), reverse=True)
        stack = []  # (dist, speed) representing time = dist / speed
        for pos, spd in cars:
            dist = target - pos
            if not stack or dist * stack[-1][1] > stack[-1][0] * spd:
                stack.append((dist, spd))
        return len(stack)""",
        "java": """        int n = position.length;
        Integer[] idx = new Integer[n];
        for (int i = 0; i < n; i++) idx[i] = i;
        Arrays.sort(idx, (a, b) -> Integer.compare(position[b], position[a]));
        Deque<long[]> stack = new ArrayDeque<>();
        for (int i : idx) {
            long dist = (long) target - position[i];
            long spd = speed[i];
            if (stack.isEmpty() || dist * stack.peek()[1] > stack.peek()[0] * spd) {
                stack.push(new long[]{dist, spd});
            }
        }
        return stack.size();""",
        "visible": [
            {"target": 12, "position": [10, 8, 0, 5, 3], "speed": [2, 4, 1, 1, 3]},
            {"target": 10, "position": [3], "speed": [3]},
            {"target": 100, "position": [0, 2, 4], "speed": [4, 2, 1]},
        ],
        "hidden": [
            {"target": 10, "position": [0, 4, 2], "speed": [2, 1, 3]},
            {"target": 10, "position": [6, 8], "speed": [3, 2]},
            {"target": 10, "position": [8, 3, 7, 4, 6, 5], "speed": [4, 4, 4, 4, 4, 4]},
            {"target": 20, "position": [0, 5, 10, 15], "speed": [4, 3, 2, 1]},
            {"target": 20, "position": [0, 5, 10, 15], "speed": [1, 2, 3, 4]},
            {"target": 1000000, "position": [0, 1, 2], "speed": [1000000, 999999, 999998]},
            {"target": 15, "position": [1, 2, 3, 10, 12], "speed": [14, 13, 12, 5, 3]},
            {"target": 10, "position": [0, 2, 4, 6, 8], "speed": [1, 2, 1, 2, 1]},
            _perf_50(),
        ],
    },

    # ------------------------------------------------------------------
    # 51 - Car Fleet Collision Times
    # ------------------------------------------------------------------
    {
        "slug": "51-car-fleet-collision-times",
        "title": "Car Fleet Collision Times",
        "difficulty": "Hard",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Uber", "Meta", "Amazon"],
        "desc": (
            "There are `n` cars traveling along a single-lane road in the same direction, given as `cars[i] = [position_i, speed_i]` sorted in strictly increasing order of `position_i`.\n\n"
            "When a car catches up to a slower car ahead of it, they collide and merge into a single fleet traveling at the slower car's speed (the slower car's speed never changes).\n\n"
            "Return a floating-point array `answer` of length `n` where `answer[i]` is the time (in seconds) at which car `i` collides with the next car ahead of it, or `-1.0` if car `i` never collides. Answers within `10^-5` of the true value are accepted."
        ),
        "cons": [
            "1 <= cars.length <= 10^5",
            "1 <= position_i, speed_i <= 10^6",
            "position_i < position_{i+1} for all valid i."
        ],
        "hints": [
            "Process cars from right to left while maintaining a stack of candidate cars ahead that could be the first collision target.",
            "Pop a candidate j from the stack if speed[i] <= speed[j] (unreachable) or if j collides with another car earlier than i would reach j."
        ],
        "explanations": [
            "Car 0 catches car 1 at t = 1.0; car 1 is slower than car 2 so it never collides; car 2 catches car 3 at t = 3.0.",
            "Car 2 collides with car 3 at t = 1.5; car 1 catches car 2 at t = 1.0 before car 2 merges; car 0 catches the fleet at t = 2.0.",
            "A single car has no car ahead to collide with, so it returns [-1.0]."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "compare": "float",
        "kind": "function",
        "method": "getCollisionTimes",
        "params": [("cars", "int[][]")],
        "ret": "double[]",
        "py": """        n = len(cars)
        ans = [-1.0] * n
        stack = []
        for i in range(n - 1, -1, -1):
            p, s = cars[i]
            while stack:
                j = stack[-1]
                pj, sj = cars[j]
                if s <= sj or (ans[j] > 0 and (pj - p) / (s - sj) >= ans[j]):
                    stack.pop()
                else:
                    break
            if stack:
                j = stack[-1]
                ans[i] = (cars[j][0] - p) / (s - cars[j][1])
            stack.append(i)
        return ans""",
        "java": """        int n = cars.length;
        double[] ans = new double[n];
        Arrays.fill(ans, -1.0);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = n - 1; i >= 0; i--) {
            int p = cars[i][0], s = cars[i][1];
            while (!stack.isEmpty()) {
                int j = stack.peek();
                int pj = cars[j][0], sj = cars[j][1];
                if (s <= sj || (ans[j] > 0 && (double) (pj - p) / (s - sj) >= ans[j])) {
                    stack.pop();
                } else {
                    break;
                }
            }
            if (!stack.isEmpty()) {
                int j = stack.peek();
                ans[i] = (double) (cars[j][0] - p) / (s - cars[j][1]);
            }
            stack.push(i);
        }
        return ans;""",
        "visible": [
            {"cars": [[1, 2], [2, 1], [4, 3], [7, 2]]},
            {"cars": [[3, 4], [5, 4], [6, 3], [9, 1]]},
            {"cars": [[5, 2]]},
        ],
        "hidden": [
            {"cars": [[1, 1], [2, 2], [3, 3]]},
            {"cars": [[1, 5], [2, 4], [3, 3], [4, 2], [5, 1]]},
            {"cars": [[1, 10], [4, 5], [5, 1]]},
            {"cars": [[1, 3], [3, 3], [5, 1]]},
            {"cars": [[1, 4], [4, 5], [7, 1], [13, 4]]},
            {"cars": [[2, 7], [5, 3], [8, 5], [10, 2], [15, 1]]},
            {"cars": [[1, 6], [2, 5], [5, 4], [6, 2], [12, 1]]},
            {"cars": [[10, 9], [12, 8], [15, 6], [20, 10], [22, 2]]},
            _perf_51(),
        ],
    },

    # ------------------------------------------------------------------
    # 52 - Redundant Brackets Detection
    # ------------------------------------------------------------------
    {
        "slug": "52-redundant-brackets-detection",
        "title": "Redundant Brackets Detection",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Microsoft", "Oracle", "Adobe"],
        "desc": (
            "Given a valid mathematical expression string `s` consisting of lowercase English letters (variables), binary operators `'+'`, `'-'`, `'*'`, `'/'`, and balanced parentheses `'('` and `')'`, determine whether `s` contains any **redundant parentheses**.\n\n"
            "A pair of matching parentheses is redundant if there is no operator (`'+'`, `'-'`, `'*'`, or `'/'`) directly enclosed within that pair (for example, `\"(a)\"`, `\"((a+b))\"`, or `\"()\"`). Return `true` if any redundant pair exists, and `false` otherwise."
        ),
        "cons": [
            "1 <= s.length <= 10^4",
            "s has balanced parentheses and contains only lowercase letters, '+', '-', '*', '/', '(', and ')'."
        ],
        "hints": [
            "Push characters onto a stack until you reach a closing parenthesis ')'.",
            "Pop elements until matching '(' while checking whether at least one operator was popped; if none was found, that parenthesis pair is redundant."
        ],
        "explanations": [
            "The outer pair around (a+b) wraps only an already-parenthesized subexpression with no operator directly inside, so it is redundant.",
            "Each pair of parentheses directly encloses an operator ('+' or '*'), so none is redundant.",
            "(a) encloses a single variable with no operator, so it is redundant."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "hasRedundantBrackets",
        "params": [("s", "String")],
        "ret": "boolean",
        "py": """        stack = []
        ops = {'+', '-', '*', '/'}
        for ch in s:
            if ch == ')':
                has_op = False
                while stack and stack[-1] != '(':
                    if stack.pop() in ops:
                        has_op = True
                if stack:
                    stack.pop()
                if not has_op:
                    return True
            else:
                stack.append(ch)
        return False""",
        "java": """        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ')') {
                boolean hasOp = false;
                while (!stack.isEmpty() && stack.peek() != '(') {
                    char top = stack.pop();
                    if (top == '+' || top == '-' || top == '*' || top == '/') {
                        hasOp = true;
                    }
                }
                if (!stack.isEmpty()) stack.pop();
                if (!hasOp) return true;
            } else {
                stack.push(ch);
            }
        }
        return false;""",
        "visible": [
            {"s": "((a+b))"},
            {"s": "(a+(b*c))"},
            {"s": "(a)+b"},
        ],
        "hidden": [
            {"s": "a+b"},
            {"s": "()"},
            {"s": "(a)"},
            {"s": "(a+b)*(c-d)"},
            {"s": "((a+b)*(c-d))"},
            {"s": "(a+(b)/c)"},
            {"s": "(((a+b)+c)+d)"},
            {"s": "a+((b*c))"},
            {"s": _perf_52()},
        ],
    },
]

TASKS.extend([
    # ------------------------------------------------------------------
    # 53 - Minimum Reversals to Balance Brackets
    # ------------------------------------------------------------------
    {
        "slug": "53-minimum-reversals-to-balance-brackets",
        "title": "Minimum Reversals to Balance Brackets",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Goldman Sachs"],
        "desc": (
            "You are given a string `s` consisting only of `'('` and `')'`.\n\n"
            "In a single operation, you may flip any one character (`'('` becomes `')'`, or `')'` becomes `'('`). "
            "Return the minimum number of flips required to transform `s` into a valid balanced parentheses string, or return `-1` if it is impossible."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists only of '(' and ')'."
        ],
        "hints": [
            "An odd-length string can never be balanced, so immediately return -1.",
            "Cancel all already-matched \"()\" pairs using a stack; the leftover string consists of c closing brackets followed by o opening brackets, requiring ceil(c / 2) + ceil(o / 2) flips."
        ],
        "explanations": [
            "After cancelling matched pairs, \"))((\" remains; flipping one ')' and one '(' makes \"()()\" in 2 flips.",
            "\"((()\" cancels to \"((\", which needs 1 flip to become \"()\".",
            "Odd length 3 cannot be balanced, so return -1."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "minReversals",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        if len(s) % 2 == 1:
            return -1
        stack = []
        for ch in s:
            if ch == ')' and stack and stack[-1] == '(':
                stack.pop()
            else:
                stack.append(ch)
        opens = sum(1 for ch in stack if ch == '(')
        closes = len(stack) - opens
        return (opens + 1) // 2 + (closes + 1) // 2""",
        "java": """        if (s.length() % 2 == 1) return -1;
        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ')' && !stack.isEmpty() && stack.peek() == '(') {
                stack.pop();
            } else {
                stack.push(ch);
            }
        }
        int opens = 0, closes = 0;
        for (char ch : stack) {
            if (ch == '(') opens++;
            else closes++;
        }
        return (opens + 1) / 2 + (closes + 1) / 2;""",
        "visible": [
            {"s": "))(("},
            {"s": "((()"},
            {"s": "(()"},
        ],
        "hidden": [
            {"s": "()"},
            {"s": ")("},
            {"s": "(((("},
            {"s": "))))"},
            {"s": ")))((("},
            {"s": "()()()"},
            {"s": ")(()())("},
            {"s": "((())))(()"},
            {"s": _perf_53()},
        ],
    },

    # ------------------------------------------------------------------
    # 54 - Longest Balanced Bracket Prefix
    # ------------------------------------------------------------------
    {
        "slug": "54-longest-balanced-bracket-prefix",
        "title": "Longest Balanced Bracket Prefix",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Amazon", "Apple"],
        "desc": (
            "Given a string `s` consisting of the six bracket characters `'('`, `')'`, `'['`, `']'`, `'{'`, and `'}'`, "
            "return the length of the longest **prefix** of `s` that is a valid, properly nested balanced bracket string.\n\n"
            "If no non-empty prefix of `s` is balanced, return `0`."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists only of '(', ')', '[', ']', '{', and '}'."
        ],
        "hints": [
            "Track unmatched opening brackets on a stack as you scan from left to right.",
            "Whenever a closing bracket fails to match the stack top, stop immediately because no longer prefix can recover; whenever the stack becomes empty at index i, update the best length to i + 1."
        ],
        "explanations": [
            "The prefix \"()[]{}\" of length 6 is balanced, while the next character ']' cannot match anything.",
            "The prefix \"([])\" of length 4 is balanced; the trailing '(' never closes.",
            "The string begins with a closing bracket ')', so no non-empty prefix is balanced."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "longestBalancedPrefix",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        match = {')': '(', ']': '[', '}': '{'}
        stack = []
        best = 0
        for i, ch in enumerate(s):
            if ch in '([{':
                stack.append(ch)
            else:
                if not stack or stack[-1] != match[ch]:
                    break
                stack.pop()
                if not stack:
                    best = i + 1
        return best""",
        "java": """        Deque<Character> stack = new ArrayDeque<>();
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(ch);
            } else {
                if (stack.isEmpty()) break;
                char top = stack.peek();
                if ((ch == ')' && top == '(') || (ch == ']' && top == '[') || (ch == '}' && top == '{')) {
                    stack.pop();
                    if (stack.isEmpty()) best = i + 1;
                } else {
                    break;
                }
            }
        }
        return best;""",
        "visible": [
            {"s": "()[]{}]("},
            {"s": "([])("},
            {"s": ")()"},
        ],
        "hidden": [
            {"s": "("},
            {"s": "[]"},
            {"s": "{[()]}"},
            {"s": "([)]()"},
            {"s": "{()}[](("},
            {"s": "()()()[}]"},
            {"s": "[[[]]]{}("},
            {"s": "{{}}[]()()"},
            {"s": _perf_54()},
        ],
    },

    # ------------------------------------------------------------------
    # 55 - Matching Bracket Index Map
    # ------------------------------------------------------------------
    {
        "slug": "55-matching-bracket-index-map",
        "title": "Matching Bracket Index Map",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Microsoft", "Adobe", "Atlassian", "Google"],
        "desc": (
            "Given a string `s` containing lowercase English letters and properly balanced brackets (`'('`, `')'`, `'['`, `']'`, `'{'`, `'}'`), "
            "return an integer array `ans` of length `s.length` where:\n"
            "- If `s[i]` is a bracket, `ans[i]` is the 0-based index of its matching partner bracket.\n"
            "- If `s[i]` is a lowercase letter, `ans[i] = -1`."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s contains lowercase English letters and properly balanced brackets '()', '[]', and '{}'."
        ],
        "hints": [
            "Initialize the answer array with -1 everywhere and push the index of every opening bracket onto a stack.",
            "When encountering a closing bracket at index i, pop its partner index j from the stack and assign ans[i] = j and ans[j] = i."
        ],
        "explanations": [
            "Bracket at 0 matches 4, bracket at 1 matches 3, and 'a' at index 2 maps to -1.",
            "Each pair maps symmetrically to its partner's index while letters map to -1.",
            "\"abc\" has no brackets, so every entry is -1."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "matchingBracketIndices",
        "params": [("s", "String")],
        "ret": "int[]",
        "py": """        n = len(s)
        ans = [-1] * n
        stack = []
        for i, ch in enumerate(s):
            if ch in '([{':
                stack.append(i)
            elif ch in ')]}':
                j = stack.pop()
                ans[i] = j
                ans[j] = i
        return ans""",
        "java": """        int n = s.length();
        int[] ans = new int[n];
        Arrays.fill(ans, -1);
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(i);
            } else if (ch == ')' || ch == ']' || ch == '}') {
                int j = stack.pop();
                ans[i] = j;
                ans[j] = i;
            }
        }
        return ans;""",
        "visible": [
            {"s": "([a])"},
            {"s": "a{b(c)d}e"},
            {"s": "abc"},
        ],
        "hidden": [
            {"s": "()"},
            {"s": "a"},
            {"s": "()[]{}"},
            {"s": "{[()]}"},
            {"s": "x(y[z]w)v"},
            {"s": "(a)(b)(c)"},
            {"s": "((((a))))"},
            {"s": "[{a(b)c}d]"},
            {"s": _perf_55()},
        ],
    },

    # ------------------------------------------------------------------
    # 56 - Count Valid Parentheses Substrings
    # ------------------------------------------------------------------
    {
        "slug": "56-count-valid-parentheses-substrings",
        "title": "Count Valid Parentheses Substrings",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Meta", "Amazon", "Goldman Sachs"],
        "desc": (
            "Given a string `s` consisting only of `'('` and `')'`, return the total number of non-empty contiguous substrings of `s` that form a valid balanced parentheses string.\n\n"
            "Because the count may exceed the 32-bit signed integer range, return the answer as a 64-bit integer (`long`)."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists only of '(' and ')'."
        ],
        "hints": [
            "Maintain a stack of unmatched '(' indices and an array dp where dp[i] is the number of valid substrings ending at index i.",
            "When s[i] == ')' matches a popped '(' at index j, every valid substring ending at j - 1 can be extended by s[j..i], so dp[i] = 1 + (dp[j - 1] if j > 0 else 0)."
        ],
        "explanations": [
            "\"()()\" contains 3 valid substrings: \"()\" at [0,1], \"()\" at [2,3], and \"()()\" at [0,3].",
            "\"(()())\" contains 4 valid substrings: \"()\" at [1,2], \"()\" at [3,4], \"()()\" at [1,4], and \"(()())\" at [0,5].",
            "\"))((\" contains no valid parentheses substrings."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "countValidSubstrings",
        "params": [("s", "String")],
        "ret": "long",
        "py": """        n = len(s)
        dp = [0] * n
        stack = []
        total = 0
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            elif stack:
                j = stack.pop()
                dp[i] = 1 + (dp[j - 1] if j > 0 else 0)
                total += dp[i]
        return total""",
        "java": """        int n = s.length();
        long[] dp = new long[n];
        Deque<Integer> stack = new ArrayDeque<>();
        long total = 0;
        for (int i = 0; i < n; i++) {
            if (s.charAt(i) == '(') {
                stack.push(i);
            } else if (!stack.isEmpty()) {
                int j = stack.pop();
                dp[i] = 1L + (j > 0 ? dp[j - 1] : 0L);
                total += dp[i];
            }
        }
        return total;""",
        "visible": [
            {"s": "()()"},
            {"s": "(()())"},
            {"s": "))(("},
        ],
        "hidden": [
            {"s": "("},
            {"s": ")"},
            {"s": "()"},
            {"s": "((()))"},
            {"s": "()()()()"},
            {"s": ")()())"},
            {"s": "(()(()))"},
            {"s": "()(()())()"},
            {"s": _perf_56()},
        ],
    },

    # ------------------------------------------------------------------
    # 57 - Special Binary String Rearrangement
    # ------------------------------------------------------------------
    {
        "slug": "57-special-binary-string-rearrangement",
        "title": "Special Binary String Rearrangement",
        "difficulty": "Hard",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Meta", "Amazon", "Uber"],
        "desc": (
            "A **special binary string** is a binary string with the following two properties:\n"
            "1. The number of `'0'`s equals the number of `'1'`s.\n"
            "2. Every prefix of the string has at least as many `'1'`s as `'0'`s (equivalently, treating `'1'` as `'('` and `'0'` as `')'`, it is a valid balanced parentheses string).\n\n"
            "Given a special binary string `s`, in one move you may choose two consecutive, non-empty special substrings of `s` and swap them. "
            "Return the **lexicographically largest** string obtainable after any number of moves."
        ),
        "cons": [
            "2 <= s.length <= 200",
            "s is guaranteed to be a valid special binary string."
        ],
        "hints": [
            "Every special binary string decomposes into a sequence of irreducible mountain blocks of the form '1' + inner + '0'.",
            "Use a stack of child lists to iteratively optimize every nested level: on '1' push a new frame; on '0' pop the frame, sort its child blocks in descending lexicographical order, wrap them in '1'...'0', and append to the parent frame."
        ],
        "explanations": [
            "Inside the outer '1'...'0', the two adjacent special substrings \"10\" and \"1100\" swap to produce \"11100100\".",
            "\"10\" has only one irreducible block, so it remains \"10\".",
            "Top-level blocks \"10\" and \"1100\" swap to form \"110010\"."
        ],
        "time": "O(n^2 log n)",
        "space": "O(n^2)",
        "kind": "function",
        "method": "makeLargestSpecial",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        frames = [[]]
        for ch in s:
            if ch == '1':
                frames.append([])
            else:
                inner = frames.pop()
                inner.sort(reverse=True)
                frames[-1].append("1" + "".join(inner) + "0")
        frames[0].sort(reverse=True)
        return "".join(frames[0])""",
        "java": """        Deque<List<String>> frames = new ArrayDeque<>();
        frames.push(new ArrayList<>());
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '1') {
                frames.push(new ArrayList<>());
            } else {
                List<String> inner = frames.pop();
                inner.sort(Collections.reverseOrder());
                StringBuilder sb = new StringBuilder("1");
                for (String part : inner) sb.append(part);
                sb.append('0');
                frames.peek().add(sb.toString());
            }
        }
        List<String> top = frames.pop();
        top.sort(Collections.reverseOrder());
        StringBuilder ans = new StringBuilder();
        for (String part : top) ans.append(part);
        return ans.toString();""",
        "visible": [
            {"s": "11011000"},
            {"s": "10"},
            {"s": "101100"},
        ],
        "hidden": [
            {"s": "1100"},
            {"s": "101010"},
            {"s": "101100111000"},
            {"s": "1101001100"},
            {"s": "1101101000"},
            {"s": "11100011011000"},
            {"s": "10110100111000"},
            {"s": "110101100010"},
            {"s": _perf_57()},
        ],
    },

    # ------------------------------------------------------------------
    # 58 - Longest Balanced Multi-Bracket Substring
    # ------------------------------------------------------------------
    {
        "slug": "58-longest-balanced-multi-bracket-substring",
        "title": "Longest Balanced Multi-Bracket Substring",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Given a string `s` consisting of the six bracket types `'('`, `')'`, `'['`, `']'`, `'{'`, and `'}'`, "
            "return the length of the longest contiguous substring of `s` that is validly balanced across all three bracket types."
        ),
        "cons": [
            "0 <= s.length <= 10^5",
            "s consists only of '(', ')', '[', ']', '{', and '}'."
        ],
        "hints": [
            "Push (bracketChar, index) pairs onto a stack initialized with a sentinel ('#', -1).",
            "When a closing bracket matches the top opening bracket, pop it and update the answer with i - stack.top.index; if it does not match, push the closing bracket itself as a new boundary barrier."
        ],
        "explanations": [
            "The substring \"[()]\" has length 4, while the mismatched ']' at index 5 breaks any longer valid span.",
            "The substring \"{[()]}[]\" from index 1 to 8 has length 8.",
            "No pair of matching brackets is validly nested in \"([)]\", so the answer is 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "longestMultiBracketSubstring",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        match = {')': '(', ']': '[', '}': '{'}
        stack = [('#', -1)]
        best = 0
        for i, ch in enumerate(s):
            if ch in '([{':
                stack.append((ch, i))
            elif stack[-1][0] == match[ch]:
                stack.pop()
                span = i - stack[-1][1]
                if span > best:
                    best = span
            else:
                stack.append((ch, i))
        return best""",
        "java": """        Deque<int[]> stack = new ArrayDeque<>();
        stack.push(new int[]{'#', -1});
        int best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == '[' || ch == '{') {
                stack.push(new int[]{ch, i});
            } else {
                char need = ch == ')' ? '(' : (ch == ']' ? '[' : '{');
                if (stack.peek()[0] == need) {
                    stack.pop();
                    int span = i - stack.peek()[1];
                    if (span > best) best = span;
                } else {
                    stack.push(new int[]{ch, i});
                }
            }
        }
        return best;""",
        "visible": [
            {"s": "([()])]"},
            {"s": "){[()]}[]("},
            {"s": "([)]"},
        ],
        "hidden": [
            {"s": ""},
            {"s": "()"},
            {"s": "([{}])"},
            {"s": "((({}[])))"},
            {"s": "[()]{}((("},
            {"s": "][()]({})"},
            {"s": "({[}])()[]{}"},
            {"s": "{[()]}][{()}]()"},
            {"s": _perf_58()},
        ],
    },

    # ------------------------------------------------------------------
    # 59 - Minimum Cost to Balance Wildcard Parentheses
    # ------------------------------------------------------------------
    {
        "slug": "59-minimum-cost-to-balance-wildcard-parentheses",
        "title": "Minimum Cost to Balance Wildcard Parentheses",
        "difficulty": "Hard",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Meta", "Goldman Sachs", "Amazon"],
        "desc": (
            "You are given a string `s` of length `n` consisting of `'('`, `')'`, and wildcard `'?'`, along with two integer arrays `openCost` and `closeCost` of length `n`.\n\n"
            "Every `'?'` at index `i` must be replaced by either `'('` at cost `openCost[i]` or `')'` at cost `closeCost[i]` (entries for non-`'?'` indices are `0` and unused). "
            "Return the minimum total cost to make `s` a valid balanced parentheses string, or `-1` if it is impossible."
        ),
        "cons": [
            "1 <= s.length == openCost.length == closeCost.length <= 10^5",
            "s[i] is '(', ')', or '?'.",
            "0 <= openCost[i], closeCost[i] <= 10^6 (and 0 whenever s[i] != '?')."
        ],
        "hints": [
            "Greedily assign every '?' to ')' first while pushing (openCost[i] - closeCost[i]) into a min-heap as you scan left to right tracking the bracket balance.",
            "Whenever balance drops below 0, pop the minimum delta from the heap to flip a prior '?' from ')' to '(' (increasing balance by 2); if the heap is empty or the final balance is non-zero, return -1."
        ],
        "explanations": [
            "Replacing index 1 with ')' (cost 2) and index 2 with '(' (cost 3) yields \"()()\" for total cost 5; flipping index 1 to '(' and index 2 to ')' costs 1 + 5 = 6, so 5 is optimal.",
            "Replacing the two '?' with '(' then ')' gives \"()\" at cost 4 + 3 = 7.",
            "Starting with ')' makes balancing impossible regardless of wildcard choices, so return -1."
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "kind": "function",
        "method": "minCostToBalance",
        "params": [("s", "String"), ("openCost", "int[]"), ("closeCost", "int[]")],
        "ret": "long",
        "py": """        import heapq
        n = len(s)
        if n % 2 == 1:
            return -1
        bal = 0
        cost = 0
        pq = []
        for i, ch in enumerate(s):
            if ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
            else:
                bal -= 1
                cost += closeCost[i]
                heapq.heappush(pq, openCost[i] - closeCost[i])
            while bal < 0:
                if not pq:
                    return -1
                cost += heapq.heappop(pq)
                bal += 2
        return cost if bal == 0 else -1""",
        "java": """        int n = s.length();
        if (n % 2 == 1) return -1L;
        int bal = 0;
        long cost = 0L;
        PriorityQueue<Long> pq = new PriorityQueue<>();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                bal++;
            } else if (ch == ')') {
                bal--;
            } else {
                bal--;
                cost += closeCost[i];
                pq.offer((long) openCost[i] - (long) closeCost[i]);
            }
            while (bal < 0) {
                if (pq.isEmpty()) return -1L;
                cost += pq.poll();
                bal += 2;
            }
        }
        return bal == 0 ? cost : -1L;""",
        "visible": [
            {"s": "(??)", "openCost": [0, 1, 3, 0], "closeCost": [0, 2, 5, 0]},
            {"s": "??", "openCost": [4, 10], "closeCost": [1, 3]},
            {"s": ")?", "openCost": [0, 1], "closeCost": [0, 1]},
        ],
        "hidden": [
            {"s": "?", "openCost": [1], "closeCost": [1]},
            {"s": "()", "openCost": [0, 0], "closeCost": [0, 0]},
            {"s": "((??", "openCost": [0, 0, 5, 6], "closeCost": [0, 0, 2, 3]},
            {"s": "((?(", "openCost": [0, 0, 1, 0], "closeCost": [0, 0, 1, 0]},
            {"s": "????", "openCost": [10, 1, 100, 2], "closeCost": [1, 10, 1, 100]},
            {"s": "????", "openCost": [5, 1, 8, 2], "closeCost": [2, 9, 1, 7]},
            {"s": "?)(?", "openCost": [3, 0, 0, 9], "closeCost": [9, 0, 0, 4]},
            {"s": "(????)", "openCost": [0, 5, 2, 8, 1, 0], "closeCost": [0, 1, 6, 3, 9, 0]},
            _perf_59(),
        ],
    },

    # ------------------------------------------------------------------
    # 60 - Evaluate Prefix Polish Expression
    # ------------------------------------------------------------------
    {
        "slug": "60-evaluate-prefix-polish-expression",
        "title": "Evaluate Prefix Polish Expression",
        "difficulty": "Easy",
        "subtopic": "Expression Parsing",
        "companies": ["Amazon", "Microsoft", "LinkedIn", "Oracle"],
        "desc": (
            "You are given an array of string `tokens` representing a valid arithmetic expression in **Prefix (Polish) Notation**.\n\n"
            "Valid operators are `'+'`, `'-'`, `'*'`, and `'/'`. Each operand is an integer (possibly negative). "
            "Division between two integers truncates toward zero (e.g., `7 / 2 = 3` and `-7 / 2 = -3`).\n\n"
            "Evaluate the expression and return its integer result. It is guaranteed that there is no division by zero and that every intermediate and final value fits in a 32-bit signed integer."
        ),
        "cons": [
            "1 <= tokens.length <= 10^4",
            "tokens[i] is '+', '-', '*', '/', or a valid integer string.",
            "The expression is valid and all intermediate/final values fit in a 32-bit signed integer."
        ],
        "hints": [
            "Scan the tokens array from right to left while maintaining a stack of operand values.",
            "When encountering an operator, pop the top value as the left operand a and the next value as the right operand b, then push (a op b)."
        ],
        "explanations": [
            "* (+ 2 1) 3 = (2 + 1) * 3 = 9.",
            "+ 4 (/ 13 5) = 4 + 2 = 6.",
            "- 10 (* 2 3) = 10 - 6 = 4."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "evalPrefix",
        "params": [("tokens", "String[]")],
        "ret": "int",
        "py": """        stack = []
        for tok in reversed(tokens):
            if tok in ('+', '-', '*', '/'):
                a = stack.pop()
                b = stack.pop()
                if tok == '+':
                    stack.append(a + b)
                elif tok == '-':
                    stack.append(a - b)
                elif tok == '*':
                    stack.append(a * b)
                else:
                    stack.append(int(a / b))
            else:
                stack.append(int(tok))
        return stack[-1]""",
        "java": """        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = tokens.length - 1; i >= 0; i--) {
            String tok = tokens[i];
            if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/")) {
                int a = stack.pop();
                int b = stack.pop();
                if (tok.equals("+")) stack.push(a + b);
                else if (tok.equals("-")) stack.push(a - b);
                else if (tok.equals("*")) stack.push(a * b);
                else stack.push(a / b);
            } else {
                stack.push(Integer.parseInt(tok));
            }
        }
        return stack.peek();""",
        "visible": [
            {"tokens": ["*", "+", "2", "1", "3"]},
            {"tokens": ["+", "4", "/", "13", "5"]},
            {"tokens": ["-", "10", "*", "2", "3"]},
        ],
        "hidden": [
            {"tokens": ["42"]},
            {"tokens": ["/", "-7", "2"]},
            {"tokens": ["/", "7", "-2"]},
            {"tokens": ["-", "5", "12"]},
            {"tokens": ["+", "*", "2", "3", "*", "4", "5"]},
            {"tokens": ["/", "+", "10", "*", "6", "/", "9", "+", "3", "-11", "2"]},
            {"tokens": ["-", "-", "20", "5", "3"]},
            {"tokens": ["*", "+", "-4", "9", "-", "3", "8"]},
            {"tokens": _perf_60()},
        ],
    },

    # ------------------------------------------------------------------
    # 61 - Postfix to Minimal Infix Expression
    # ------------------------------------------------------------------
    {
        "slug": "61-postfix-to-minimal-infix",
        "title": "Postfix to Minimal Infix Expression",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Microsoft", "Meta", "Amazon"],
        "desc": (
            "Given a valid space-separated **postfix (Reverse Polish Notation)** expression `expr` consisting of single lowercase variables (`'a'`-`'z'`) and binary operators `'+'`, `'-'`, and `'*'`, "
            "convert it into an equivalent infix expression (without spaces) using the **minimum number of parentheses** needed to preserve the exact evaluation semantics.\n\n"
            "Standard precedence and associativity rules apply:\n"
            "- `'*'` has higher precedence than `'+'` and `'-'`.\n"
            "- `'+'` and `'-'` have equal precedence and associate left-to-right.\n"
            "- A left operand needs parentheses if and only if its root operator has strictly lower precedence than the parent operator; a right operand needs parentheses if its root operator has strictly lower precedence, or equal precedence when the parent operator is `'-'`."
        ),
        "cons": [
            "1 <= expr.length <= 5000",
            "Tokens are separated by single spaces; each token is a single lowercase letter 'a'-'z' or one of '+', '-', '*'."
        ],
        "hints": [
            "Maintain a stack where each entry stores (infixString, rootPrecedence), with variables having precedence 3, '*' having precedence 2, and '+'/'-' having precedence 1.",
            "When popping right then left for operator op with precedence p, wrap left iff leftPrec < p and wrap right iff rightPrec < p or (rightPrec == p and op == '-')."
        ],
        "explanations": [
            "(a + b) has lower precedence than '*', so it becomes \"(a+b)*c\".",
            "a - (b - c) requires parentheses on the right child because '-' is non-associative, yielding \"a-(b-c)\".",
            "a + (b * c) needs no parentheses because '*' has higher precedence than '+', yielding \"a+b*c\"."
        ],
        "time": "O(n^2) worst-case string length",
        "space": "O(n^2) worst-case",
        "kind": "function",
        "method": "postfixToInfix",
        "params": [("expr", "String")],
        "ret": "String",
        "py": """        prec_map = {'+': 1, '-': 1, '*': 2}
        stack = []
        for tok in expr.split():
            if tok in prec_map:
                p = prec_map[tok]
                r_str, r_p = stack.pop()
                l_str, l_p = stack.pop()
                if l_p < p:
                    l_str = f"({l_str})"
                if r_p < p or (r_p == p and tok == '-'):
                    r_str = f"({r_str})"
                stack.append((f"{l_str}{tok}{r_str}", p))
            else:
                stack.append((tok, 3))
        return stack[-1][0]""",
        "java": """        Deque<String> exprSt = new ArrayDeque<>();
        Deque<Integer> precSt = new ArrayDeque<>();
        for (String tok : expr.split(" ")) {
            if (tok.equals("+") || tok.equals("-") || tok.equals("*")) {
                int p = tok.equals("*") ? 2 : 1;
                String rStr = exprSt.pop();
                int rP = precSt.pop();
                String lStr = exprSt.pop();
                int lP = precSt.pop();
                if (lP < p) lStr = "(" + lStr + ")";
                if (rP < p || (rP == p && tok.equals("-"))) rStr = "(" + rStr + ")";
                exprSt.push(lStr + tok + rStr);
                precSt.push(p);
            } else {
                exprSt.push(tok);
                precSt.push(3);
            }
        }
        return exprSt.peek();""",
        "visible": [
            {"expr": "a b + c *"},
            {"expr": "a b c - -"},
            {"expr": "a b c * +"},
        ],
        "hidden": [
            {"expr": "x"},
            {"expr": "a b - c -"},
            {"expr": "a b c + -"},
            {"expr": "a b c - +"},
            {"expr": "a b + c d + *"},
            {"expr": "a b * c *"},
            {"expr": "a b c * *"},
            {"expr": "a b - c d - * e +"},
            {"expr": _perf_61()},
        ],
    },

    # ------------------------------------------------------------------
    # 62 - Brace Expansion Expression
    # ------------------------------------------------------------------
    {
        "slug": "62-brace-expansion-expression",
        "title": "Brace Expansion Expression",
        "difficulty": "Hard",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Meta", "Amazon", "Salesforce"],
        "desc": (
            "Under a shell-like brace expansion grammar, an expression represents a set of lowercase words built from the following rules:\n"
            "- A single lowercase letter `x` represents the singleton set `{\"x\"}`.\n"
            "- A comma-separated brace group `{e1,e2,...,ek}` represents the **union** of the sets produced by `e1, e2, ..., ek`.\n"
            "- Concatenating two adjacent expressions `e1e2` represents the **Cartesian product** (all string concatenations `w1 + w2` with `w1` in `e1` and `w2` in `e2`).\n\n"
            "Given a valid brace expression string `expression`, return the **sorted list of all distinct words** represented by `expression`."
        ),
        "cons": [
            "1 <= expression.length <= 60",
            "expression consists of lowercase English letters, '{', '}', and ','.",
            "The output list contains at most 5000 distinct words."
        ],
        "hints": [
            "Maintain a stack of brace frames, each saving (unionSet, currentProductSet) before entering '{'.",
            "On a letter, append it to every string in currentProductSet; on ',', merge currentProductSet into unionSet and reset currentProductSet to {\"\"}; on '}', combine unionSet | currentProductSet with the popped frame's currentProductSet via Cartesian product."
        ],
        "explanations": [
            "{a,b} produces {a, b} and {c,{d,e}} produces {c, d, e}; their Cartesian product is [\"ac\",\"ad\",\"ae\",\"bc\",\"bd\",\"be\"].",
            "The union of {a,z}, a{b,c} = {ab,ac}, and {ab,z} deduplicates and sorts to [\"a\",\"ab\",\"ac\",\"z\"].",
            "Simple concatenation with a single group yields [\"prexpost\",\"preypost\"]."
        ],
        "time": "O(W log W)",
        "space": "O(W)",
        "kind": "function",
        "method": "braceExpansion",
        "params": [("expression", "String")],
        "ret": "List<String>",
        "py": """        stack = []
        union_set = set()
        cur_set = {""}
        for ch in expression:
            if ch == '{':
                stack.append((union_set, cur_set))
                union_set = set()
                cur_set = {""}
            elif ch == ',':
                union_set |= cur_set
                cur_set = {""}
            elif ch == '}':
                union_set |= cur_set
                prev_union, prev_cur = stack.pop()
                cur_set = {a + b for a in prev_cur for b in union_set}
                union_set = prev_union
            else:
                cur_set = {a + ch for a in cur_set}
        return sorted(union_set | cur_set)""",
        "java": """        Deque<Set<String>> unionSt = new ArrayDeque<>();
        Deque<Set<String>> curSt = new ArrayDeque<>();
        Set<String> unionSet = new HashSet<>();
        Set<String> curSet = new HashSet<>();
        curSet.add("");
        for (int i = 0; i < expression.length(); i++) {
            char ch = expression.charAt(i);
            if (ch == '{') {
                unionSt.push(unionSet);
                curSt.push(curSet);
                unionSet = new HashSet<>();
                curSet = new HashSet<>();
                curSet.add("");
            } else if (ch == ',') {
                unionSet.addAll(curSet);
                curSet = new HashSet<>();
                curSet.add("");
            } else if (ch == '}') {
                unionSet.addAll(curSet);
                Set<String> prevUnion = unionSt.pop();
                Set<String> prevCur = curSt.pop();
                Set<String> nextCur = new HashSet<>();
                for (String a : prevCur) {
                    for (String b : unionSet) {
                        nextCur.add(a + b);
                    }
                }
                curSet = nextCur;
                unionSet = prevUnion;
            } else {
                Set<String> nextCur = new HashSet<>();
                for (String a : curSet) {
                    nextCur.add(a + ch);
                }
                curSet = nextCur;
            }
        }
        unionSet.addAll(curSet);
        List<String> ans = new ArrayList<>(unionSet);
        Collections.sort(ans);
        return ans;""",
        "visible": [
            {"expression": "{a,b}{c,{d,e}}"},
            {"expression": "{{a,z},a{b,c},{ab,z}}"},
            {"expression": "pre{x,y}post"},
        ],
        "hidden": [
            {"expression": "a"},
            {"expression": "{a}"},
            {"expression": "{a,a,a}"},
            {"expression": "{a,b}c{d,e}"},
            {"expression": "a{b,{c,d}}e"},
            {"expression": "{a,b}{b,a}"},
            {"expression": "{{a,b},{b,c}}"},
            {"expression": "x{a{b,c},d{e,f}}y"},
            {"expression": _perf_62()},
        ],
    },
])

TASKS.extend([
    # ------------------------------------------------------------------
    # 63 - Parse Lisp Expression
    # ------------------------------------------------------------------
    {
        "slug": "63-parse-lisp-expression",
        "title": "Parse Lisp Expression",
        "difficulty": "Hard",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Meta", "Amazon", "Bloomberg"],
        "desc": (
            "You are given a string `expression` representing a valid Lisp-like expression to evaluate to a single integer.\n\n"
            "An expression can be:\n"
            "- An integer literal (possibly negative).\n"
            "- A variable name (starts with a lowercase letter followed by zero or more lowercase letters or digits), evaluated in the innermost enclosing lexical scope.\n"
            "- `(add e1 e2)` returning `eval(e1) + eval(e2)`.\n"
            "- `(mult e1 e2)` returning `eval(e1) * eval(e2)`.\n"
            "- `(let v1 e1 v2 e2 ... vk ek expr)` which opens a new scope, assigns `v1 = eval(e1)`, `v2 = eval(e2)`, ..., sequentially left-to-right (so later bindings can reference earlier ones in the same `let` and shadow outer scopes), and returns `eval(expr)`.\n\n"
            "All intermediate and final values fit in a 32-bit signed integer."
        ),
        "cons": [
            "1 <= expression.length <= 2000",
            "expression is a valid Lisp expression with single spaces separating tokens inside parentheses.",
            "Every referenced variable is bound in an enclosing scope, and all values fit in a 32-bit signed integer."
        ],
        "hints": [
            "Maintain a stack of lexical scope maps (one dictionary per active 'let' block) and resolve variable lookups from the top of the stack downward.",
            "Parse sequentially with a cursor index: on '(', dispatch on 'add', 'mult', or 'let'; inside 'let', check whether a token is followed by ')' (final expression) or ' ' (variable binding pair)."
        ],
        "explanations": [
            "Outer let binds x = 2; inner let shadows x = 3 and binds y = 4, so (add x y) = 7; outer mult computes 2 * 7 = 14.",
            "In (let x 3 x 2 x), x is first bound to 3 then rebound to 2, so the final x evaluates to 2.",
            "x = 1, y = 2, then x is updated to (add 1 2) = 3, and the final (add x y) evaluates to 3 + 2 = 5."
        ],
        "time": "O(n * d)",
        "space": "O(n)",
        "kind": "function",
        "method": "evaluateLisp",
        "params": [("expression", "String")],
        "ret": "int",
        "py": """        n = len(expression)
        idx = 0
        scopes = []

        def lookup(var: str) -> int:
            for sc in reversed(scopes):
                if var in sc:
                    return sc[var]
            return 0

        def read_token() -> str:
            nonlocal idx
            start = idx
            while idx < n and expression[idx] not in (' ', ')'):
                idx += 1
            return expression[start:idx]

        def eval_atom(tok: str) -> int:
            if tok[0] == '-' or tok[0].isdigit():
                return int(tok)
            return lookup(tok)

        def eval_expr() -> int:
            nonlocal idx
            if expression[idx] != '(':
                return eval_atom(read_token())
            idx += 1  # skip '('
            op = read_token()
            idx += 1  # skip ' '
            if op == 'add':
                a = eval_expr()
                idx += 1  # skip ' '
                b = eval_expr()
                idx += 1  # skip ')'
                return a + b
            if op == 'mult':
                a = eval_expr()
                idx += 1
                b = eval_expr()
                idx += 1
                return a * b
            # let
            scopes.append({})
            while True:
                if expression[idx] == '(':
                    res = eval_expr()
                    idx += 1  # skip ')'
                    scopes.pop()
                    return res
                tok = read_token()
                if expression[idx] == ')':
                    res = eval_atom(tok)
                    idx += 1  # skip ')'
                    scopes.pop()
                    return res
                idx += 1  # skip ' '
                val = eval_expr()
                scopes[-1][tok] = val
                idx += 1  # skip ' '

        return eval_expr()""",
        "java": """        this.s = expression;
        this.idx = 0;
        this.scopes = new ArrayList<>();
        return evalExpr();""",
        "java_helpers": """    private String s;
    private int idx;
    private List<Map<String, Integer>> scopes;

    private int lookup(String var) {
        for (int i = scopes.size() - 1; i >= 0; i--) {
            Integer v = scopes.get(i).get(var);
            if (v != null) return v;
        }
        return 0;
    }

    private String readToken() {
        int start = idx;
        while (idx < s.length() && s.charAt(idx) != ' ' && s.charAt(idx) != ')') {
            idx++;
        }
        return s.substring(start, idx);
    }

    private int evalAtom(String tok) {
        char c = tok.charAt(0);
        if (c == '-' || (c >= '0' && c <= '9')) {
            return Integer.parseInt(tok);
        }
        return lookup(tok);
    }

    private int evalExpr() {
        if (s.charAt(idx) != '(') {
            return evalAtom(readToken());
        }
        idx++; // skip '('
        String op = readToken();
        idx++; // skip ' '
        if (op.equals("add")) {
            int a = evalExpr();
            idx++;
            int b = evalExpr();
            idx++;
            return a + b;
        }
        if (op.equals("mult")) {
            int a = evalExpr();
            idx++;
            int b = evalExpr();
            idx++;
            return a * b;
        }
        scopes.add(new HashMap<>());
        while (true) {
            if (s.charAt(idx) == '(') {
                int res = evalExpr();
                idx++;
                scopes.remove(scopes.size() - 1);
                return res;
            }
            String tok = readToken();
            if (s.charAt(idx) == ')') {
                int res = evalAtom(tok);
                idx++;
                scopes.remove(scopes.size() - 1);
                return res;
            }
            idx++;
            int val = evalExpr();
            scopes.get(scopes.size() - 1).put(tok, val);
            idx++;
        }
    }""",
        "visible": [
            {"expression": "(let x 2 (mult x (let x 3 y 4 (add x y))))"},
            {"expression": "(let x 3 x 2 x)"},
            {"expression": "(let x 1 y 2 x (add x y) (add x y))"},
        ],
        "hidden": [
            {"expression": "42"},
            {"expression": "-7"},
            {"expression": "(add 1 2)"},
            {"expression": "(mult -3 (add 2 -5))"},
            {"expression": "(let a1 3 b2 (add a1 1) b2)"},
            {"expression": "(let x 2 (add (let x 3 (let x 4 x)) x))"},
            {"expression": "(let x 7 -12)"},
            {"expression": "(let x 2 y (mult x 3) (let z (add x y) (mult z (add y -1))))"},
            {"expression": _perf_63()},
        ],
    },

    # ------------------------------------------------------------------
    # 64 - Remove Parentheses From Sign Expression
    # ------------------------------------------------------------------
    {
        "slug": "64-remove-parentheses-sign-expression",
        "title": "Remove Parentheses From Sign Expression",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Adobe"],
        "desc": (
            "Given a valid algebraic expression string `s` consisting of single lowercase variables (`'a'`-`'z'`), `'+'`, `'-'`, `'('`, and `')'` (with no spaces and no consecutive binary operators outside parentheses; unary `'-'` may appear at the start of `s` or immediately after `'('`), "
            "remove all parentheses while preserving exact mathematical equivalence by propagating outer signs.\n\n"
            "Return the simplified parenthesization-free string with no leading `'+'` sign (for example, `\"-(a-b)\"` becomes `\"-a+b\"`, and `\"-(-a)\"` becomes `\"a\"`)."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s is a valid expression of lowercase letters 'a'-'z', '+', '-', '(', and ')' with at least one variable."
        ],
        "hints": [
            "Maintain a stack of active sign multipliers (+1 or -1), initialized with [1], along with a local sign variable for the operator immediately preceding the next term or '('.",
            "When seeing '(', push (stack.top * localSign) and reset localSign to +1; on ')', pop the stack; on a variable, apply effectiveSign = stack.top * localSign."
        ],
        "explanations": [
            "The outer minus negates b and double-negates (c+d), yielding \"a-b+c+d\".",
            "Negating (a-b) flips 'a' to '-a' and '-b' to '+b', giving \"-a+b\".",
            "Two nested negations cancel on 'a', and leading '+' is omitted, yielding \"a\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "removeParentheses",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        sign_stack = [1]
        local_sign = 1
        out = []
        for ch in s:
            if ch == '+':
                local_sign = 1
            elif ch == '-':
                local_sign = -1
            elif ch == '(':
                sign_stack.append(sign_stack[-1] * local_sign)
                local_sign = 1
            elif ch == ')':
                sign_stack.pop()
            else:
                eff = sign_stack[-1] * local_sign
                if eff == -1:
                    out.append('-')
                elif out:
                    out.append('+')
                out.append(ch)
                local_sign = 1
        return "".join(out)""",
        "java": """        Deque<Integer> signStack = new ArrayDeque<>();
        signStack.push(1);
        int localSign = 1;
        StringBuilder out = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '+') {
                localSign = 1;
            } else if (ch == '-') {
                localSign = -1;
            } else if (ch == '(') {
                signStack.push(signStack.peek() * localSign);
                localSign = 1;
            } else if (ch == ')') {
                signStack.pop();
            } else {
                int eff = signStack.peek() * localSign;
                if (eff == -1) {
                    out.append('-');
                } else if (out.length() > 0) {
                    out.append('+');
                }
                out.append(ch);
                localSign = 1;
            }
        }
        return out.toString();""",
        "visible": [
            {"s": "a-(b-(c+d))"},
            {"s": "-(a-b)"},
            {"s": "-(-a)"},
        ],
        "hidden": [
            {"s": "a"},
            {"s": "(a+b)-(c-d)"},
            {"s": "a-(-(b+c))"},
            {"s": "-((a+b)-(c+d))"},
            {"s": "a+(b-(c-(d-e)))"},
            {"s": "-(-(-a-b))"},
            {"s": "(((x)))"},
            {"s": "p-(q+r)-(s-(t+u))"},
            {"s": _perf_64()},
        ],
    },

    # ------------------------------------------------------------------
    # 65 - Evaluate Expression With Exponentiation
    # ------------------------------------------------------------------
    {
        "slug": "65-evaluate-expression-with-exponentiation",
        "title": "Evaluate Expression With Exponentiation",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Amazon", "Meta", "Oracle"],
        "desc": (
            "Given a valid mathematical expression string `s` consisting of non-negative integers, binary operators `'+'`, `'-'`, `'*'`, and `'^'` (exponentiation), parentheses `'('` and `')'`, and optional spaces `' '`, evaluate `s` and return its 64-bit integer result (`long`).\n\n"
            "Precedence and associativity rules:\n"
            "- `'^'` has the highest precedence and is **right-associative** (so `2^3^2 = 2^(3^2) = 512`, and `0^0 = 1`).\n"
            "- `'*'` has medium precedence and is left-associative.\n"
            "- `'+'` and `'-'` have the lowest precedence and are left-associative.\n\n"
            "All exponents are non-negative integers, and all intermediate and final values fit in a 64-bit signed integer."
        ),
        "cons": [
            "1 <= s.length <= 10^4",
            "s contains digits, '+', '-', '*', '^', '(', ')', and ' ' (no unary minus).",
            "Every exponent is non-negative and every intermediate/final value fits in a 64-bit signed integer."
        ],
        "hints": [
            "Use Shunting-Yard with an operand value stack and an operator stack.",
            "Before pushing a left-associative operator (+, -, *), pop and evaluate top operators with precedence >= current; before pushing right-associative '^', pop only operators with strictly greater precedence."
        ],
        "explanations": [
            "Because '^' is right-associative, 2^3^2 evaluates as 2^(3^2) = 2^9 = 512.",
            "2^3 = 8, 3 * 8 = 24, then 24 + 4 = 28.",
            "(2 + 1)^(1 + 2) * 2 - 5 = 3^3 * 2 - 5 = 54 - 5 = 49."
        ],
        "time": "O(n log E)",
        "space": "O(n)",
        "kind": "function",
        "method": "evalWithPower",
        "params": [("s", "String")],
        "ret": "long",
        "py": """        def prec(op: str) -> int:
            if op in ('+', '-'):
                return 1
            if op == '*':
                return 2
            if op == '^':
                return 3
            return 0

        vals = []
        ops = []

        def apply_top() -> None:
            op = ops.pop()
            b = vals.pop()
            a = vals.pop()
            if op == '+':
                vals.append(a + b)
            elif op == '-':
                vals.append(a - b)
            elif op == '*':
                vals.append(a * b)
            else:
                res = 1
                base = a
                exp = b
                while exp > 0:
                    if exp & 1:
                        res *= base
                    base *= base
                    exp >>= 1
                vals.append(res)

        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == ' ':
                i += 1
            elif ch.isdigit():
                num = 0
                while i < n and s[i].isdigit():
                    num = num * 10 + (ord(s[i]) - 48)
                    i += 1
                vals.append(num)
            elif ch == '(':
                ops.append(ch)
                i += 1
            elif ch == ')':
                while ops and ops[-1] != '(':
                    apply_top()
                ops.pop()
                i += 1
            else:
                p = prec(ch)
                while ops and ops[-1] != '(' and (prec(ops[-1]) > p or (ch != '^' and prec(ops[-1]) == p)):
                    apply_top()
                ops.append(ch)
                i += 1
        while ops:
            apply_top()
        return vals[-1]""",
        "java": """        Deque<Long> vals = new ArrayDeque<>();
        Deque<Character> ops = new ArrayDeque<>();
        int i = 0, n = s.length();
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == ' ') {
                i++;
            } else if (ch >= '0' && ch <= '9') {
                long num = 0;
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    num = num * 10 + (s.charAt(i) - '0');
                    i++;
                }
                vals.push(num);
            } else if (ch == '(') {
                ops.push(ch);
                i++;
            } else if (ch == ')') {
                while (!ops.isEmpty() && ops.peek() != '(') {
                    applyTop(vals, ops);
                }
                ops.pop();
                i++;
            } else {
                int p = prec(ch);
                while (!ops.isEmpty() && ops.peek() != '('
                        && (prec(ops.peek()) > p || (ch != '^' && prec(ops.peek()) == p))) {
                    applyTop(vals, ops);
                }
                ops.push(ch);
                i++;
            }
        }
        while (!ops.isEmpty()) {
            applyTop(vals, ops);
        }
        return vals.peek();""",
        "java_helpers": """    private int prec(char op) {
        if (op == '+' || op == '-') return 1;
        if (op == '*') return 2;
        if (op == '^') return 3;
        return 0;
    }

    private void applyTop(Deque<Long> vals, Deque<Character> ops) {
        char op = ops.pop();
        long b = vals.pop();
        long a = vals.pop();
        if (op == '+') vals.push(a + b);
        else if (op == '-') vals.push(a - b);
        else if (op == '*') vals.push(a * b);
        else {
            long res = 1L, base = a, exp = b;
            while (exp > 0) {
                if ((exp & 1L) != 0) res *= base;
                base *= base;
                exp >>= 1;
            }
            vals.push(res);
        }
    }""",
        "visible": [
            {"s": "2^3^2"},
            {"s": "3 * 2^3 + 4"},
            {"s": "(2 + 1)^(1 + 2) * 2 - 5"},
        ],
        "hidden": [
            {"s": "0^0"},
            {"s": "(2^3)^2"},
            {"s": "2^0^3"},
            {"s": "10 - 2^3 - 1"},
            {"s": "2^(1+2)^2"},
            {"s": "3^2 * 2^3 - 5^2"},
            {"s": "((1+1)^(2+1))^(1+1)"},
            {"s": "100 - 3 * (2^4 - 6) + 2^10"},
            {"s": _perf_65()},
        ],
    },

    # ------------------------------------------------------------------
    # 66 - Inverse Depth Sum of Nested List
    # ------------------------------------------------------------------
    {
        "slug": "66-inverse-depth-sum-nested-list",
        "title": "Inverse Depth Sum of Nested List",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["LinkedIn", "Meta", "Google", "Amazon"],
        "desc": (
            "You are given a string `s` representing a valid nested list of signed integers formatted with square brackets `'['`, `']'` and commas `','` (e.g., `\"[1,[4,[6]]]\"`).\n\n"
            "The **depth** of an integer is the number of bracket pairs enclosing it (outermost elements have depth `1`). "
            "Let `maxDepth` be the maximum depth among all integers present in `s` (or `0` if `s` contains no integers). "
            "The **inverse weight** of an integer at depth `d` is `maxDepth - d + 1`.\n\n"
            "Return the sum of `value * (maxDepth - depth + 1)` over all integers in `s`."
        ),
        "cons": [
            "2 <= s.length <= 5 * 10^4",
            "s is a valid bracketed nested list of integers with no spaces.",
            "All integer values are in [-10^4, 10^4], and the final sum fits in a 32-bit signed integer."
        ],
        "hints": [
            "Track nesting depth using a stack of '[' brackets (or depth counter) while parsing signed integers.",
            "Use the identity sum(val * (maxDepth - d + 1)) = (maxDepth + 1) * sum(val) - sum(val * d) to compute the answer in a single pass."
        ],
        "explanations": [
            "Integers are 1 (depth 1), 4 (depth 2), 6 (depth 3); maxDepth = 3, so inverse sum = 1*3 + 4*2 + 6*1 = 17.",
            "Integers are 1,1 (depth 2), 2 (depth 1), 1,1 (depth 2); maxDepth = 2, so inverse sum = (1+1+1+1)*1 + 2*2 = 8.",
            "No integers exist inside \"[[]]\", so the result is 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "inverseDepthSum",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        stack = []
        plain_sum = 0
        depth_sum = 0
        max_depth = 0
        i = 0
        n = len(s)
        while i < n:
            ch = s[i]
            if ch == '[':
                stack.append('[')
                i += 1
            elif ch == ']':
                stack.pop()
                i += 1
            elif ch == ',':
                i += 1
            else:
                sign = 1
                if ch == '-':
                    sign = -1
                    i += 1
                val = 0
                while i < n and s[i].isdigit():
                    val = val * 10 + (ord(s[i]) - 48)
                    i += 1
                val *= sign
                d = len(stack)
                if d > max_depth:
                    max_depth = d
                plain_sum += val
                depth_sum += val * d
        return (max_depth + 1) * plain_sum - depth_sum""",
        "java": """        Deque<Character> stack = new ArrayDeque<>();
        int plainSum = 0;
        int depthSum = 0;
        int maxDepth = 0;
        int i = 0, n = s.length();
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == '[') {
                stack.push(ch);
                i++;
            } else if (ch == ']') {
                stack.pop();
                i++;
            } else if (ch == ',') {
                i++;
            } else {
                int sign = 1;
                if (ch == '-') {
                    sign = -1;
                    i++;
                }
                int val = 0;
                while (i < n && s.charAt(i) >= '0' && s.charAt(i) <= '9') {
                    val = val * 10 + (s.charAt(i) - '0');
                    i++;
                }
                val *= sign;
                int d = stack.size();
                if (d > maxDepth) maxDepth = d;
                plainSum += val;
                depthSum += val * d;
            }
        }
        return (maxDepth + 1) * plainSum - depthSum;""",
        "visible": [
            {"s": "[1,[4,[6]]]"},
            {"s": "[[1,1],2,[1,1]]"},
            {"s": "[[]]"},
        ],
        "hidden": [
            {"s": "[]"},
            {"s": "[5]"},
            {"s": "[-5,[10,[-3]]]"},
            {"s": "[1,[[]]]"},
            {"s": "[[[1]],[[2]],[3],4]"},
            {"s": "[0,[0,[0]]]"},
            {"s": "[[1,2,3],[4,[5,6]],7]"},
            {"s": "[-10,[-20,[-30,[-40]]]]"},
            {"s": _perf_66()},
        ],
    },

    # ------------------------------------------------------------------
    # 67 - Min Queue Using Two Stacks
    # ------------------------------------------------------------------
    {
        "slug": "67-min-queue-using-two-stacks",
        "title": "Min Queue Using Two Stacks",
        "difficulty": "Medium",
        "subtopic": "Min Stack",
        "companies": ["Google", "Amazon", "Bloomberg", "Microsoft"],
        "desc": (
            "Design a FIFO queue `MinQueue` that supports standard queue operations plus retrieving the minimum element currently in the queue, all in **amortized `O(1)`** time using two min-stacks.\n\n"
            "Implement the `MinQueue` class:\n"
            "- `MinQueue()` initializes an empty queue.\n"
            "- `void enqueue(int val)` appends `val` to the back of the queue.\n"
            "- `int dequeue()` removes and returns the front element of the queue.\n"
            "- `int front()` returns the front element without removing it.\n"
            "- `int getMin()` returns the minimum value among all elements currently in the queue."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Methods dequeue, front, and getMin are always called on non-empty queues.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Maintain two min-stacks: inStack stores newly enqueued items with their running min, and outStack serves front/dequeue with its own running min.",
            "When outStack is empty during dequeue or front, pour every element from inStack into outStack while rebuilding outStack's running min; getMin() is simply the minimum of the non-empty stacks' running mins."
        ],
        "explanations": [
            "After enqueuing 5, 2, 7, front is 5 and getMin is 2; after dequeuing 5 and 2, only 7 remains so getMin becomes 7.",
            "When all elements are equal, dequeue and getMin consistently return that value.",
            "Interleaving enqueues and dequeues triggers stack pours while preserving exact FIFO order and O(1) amortized minimums."
        ],
        "time": "O(1) amortized per op",
        "space": "O(n)",
        "kind": "design",
        "className": "MinQueue",
        "ctorParams": [],
        "methods": [
            ("enqueue", [("val", "int")], "void"),
            ("dequeue", [], "int"),
            ("front", [], "int"),
            ("getMin", [], "int"),
        ],
        "py_class": """class MinQueue:
    def __init__(self):
        self.in_st = []
        self.out_st = []

    def _pour(self) -> None:
        if not self.out_st:
            while self.in_st:
                val, _ = self.in_st.pop()
                mn = val if not self.out_st or val < self.out_st[-1][1] else self.out_st[-1][1]
                self.out_st.append((val, mn))

    def enqueue(self, val: int) -> None:
        mn = val if not self.in_st or val < self.in_st[-1][1] else self.in_st[-1][1]
        self.in_st.append((val, mn))

    def dequeue(self) -> int:
        self._pour()
        return self.out_st.pop()[0]

    def front(self) -> int:
        self._pour()
        return self.out_st[-1][0]

    def getMin(self) -> int:
        if not self.in_st:
            return self.out_st[-1][1]
        if not self.out_st:
            return self.in_st[-1][1]
        return min(self.in_st[-1][1], self.out_st[-1][1])""",
        "java_class": """class MinQueue {
    private final Deque<int[]> inSt = new ArrayDeque<>();
    private final Deque<int[]> outSt = new ArrayDeque<>();

    public MinQueue() {}

    private void pour() {
        if (outSt.isEmpty()) {
            while (!inSt.isEmpty()) {
                int val = inSt.pop()[0];
                int mn = outSt.isEmpty() ? val : Math.min(val, outSt.peek()[1]);
                outSt.push(new int[]{val, mn});
            }
        }
    }

    public void enqueue(int val) {
        int mn = inSt.isEmpty() ? val : Math.min(val, inSt.peek()[1]);
        inSt.push(new int[]{val, mn});
    }

    public int dequeue() {
        pour();
        return outSt.pop()[0];
    }

    public int front() {
        pour();
        return outSt.peek()[0];
    }

    public int getMin() {
        if (inSt.isEmpty()) return outSt.peek()[1];
        if (outSt.isEmpty()) return inSt.peek()[1];
        return Math.min(inSt.peek()[1], outSt.peek()[1]);
    }
}""",
        "visible": [
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "enqueue", "front", "getMin", "dequeue", "dequeue", "getMin"],
                "args": [[], [5], [2], [7], [], [], [], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "getMin", "dequeue", "getMin"],
                "args": [[], [4], [4], [], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "dequeue", "enqueue", "getMin", "front", "dequeue", "getMin"],
                "args": [[], [10], [3], [], [1], [], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["MinQueue", "enqueue", "front", "getMin", "dequeue"],
                "args": [[], [-9], [], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "enqueue", "getMin", "dequeue", "getMin", "dequeue", "getMin"],
                "args": [[], [1], [2], [3], [], [], [], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "enqueue", "getMin", "dequeue", "getMin", "dequeue", "getMin"],
                "args": [[], [3], [2], [1], [], [], [], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "dequeue", "enqueue", "enqueue", "getMin", "front"],
                "args": [[], [100], [], [-50], [25], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "enqueue", "enqueue", "dequeue", "enqueue", "getMin", "dequeue", "getMin"],
                "args": [[], [-10], [5], [-10], [8], [], [-20], [], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "getMin", "dequeue", "enqueue", "getMin"],
                "args": [[], [1000000000], [-1000000000], [], [], [0], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "front", "enqueue", "dequeue", "front", "getMin"],
                "args": [[], [7], [9], [], [6], [], [], []],
            },
            {
                "ops": ["MinQueue", "enqueue", "enqueue", "enqueue", "dequeue", "dequeue", "enqueue", "getMin", "front"],
                "args": [[], [4], [1], [5], [], [], [2], [], []],
            },
            _perf_67(),
        ],
    },

    # ------------------------------------------------------------------
    # 68 - Min Stack With Add-All Offset
    # ------------------------------------------------------------------
    {
        "slug": "68-min-stack-with-add-all",
        "title": "Min Stack With Add-All Offset",
        "difficulty": "Medium",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Google", "Goldman Sachs", "Uber"],
        "desc": (
            "Design a stack `OffsetMinStack` that supports standard stack operations, adding a constant `delta` to **every** element currently in the stack, and querying the current minimum — all in strict `O(1)` time.\n\n"
            "Implement the `OffsetMinStack` class:\n"
            "- `OffsetMinStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes `val` onto the stack (prior `addAll` calls do NOT affect newly pushed values).\n"
            "- `void pop()` removes the top element of the stack.\n"
            "- `void addAll(int delta)` adds `delta` (which may be negative) to every element currently in the stack.\n"
            "- `long top()` returns the current value of the top element.\n"
            "- `long getMin()` returns the current minimum value across all elements in the stack."
        ),
        "cons": [
            "-10^9 <= val, delta <= 10^9",
            "Methods pop, top, and getMin are always called on non-empty stacks.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Maintain a single 64-bit global lazy offset; addAll(delta) simply adds delta to offset in O(1).",
            "When pushing val, store adjusted = val - offset together with the running minimum of adjusted values; since shifting all elements by offset preserves their ordering, top() = topAdj + offset and getMin() = topMinAdj + offset."
        ],
        "explanations": [
            "Push 5, 2 -> min 2; addAll(10) shifts elements to [15, 12] -> getMin 12; push(3) gives [15, 12, 3] -> top 3, getMin 3; pop removes 3 leaving [15, 12] -> getMin 12.",
            "Negative addAll shifts all stored elements downward without affecting future pushes.",
            "When the stack empties and refills, the global offset continues working seamlessly."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "OffsetMinStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "void"),
            ("addAll", [("delta", "int")], "void"),
            ("top", [], "long"),
            ("getMin", [], "long"),
        ],
        "py_class": """class OffsetMinStack:
    def __init__(self):
        self.st = []
        self.offset = 0

    def push(self, val: int) -> None:
        adj = val - self.offset
        mn = adj if not self.st or adj < self.st[-1][1] else self.st[-1][1]
        self.st.append((adj, mn))

    def pop(self) -> None:
        self.st.pop()

    def addAll(self, delta: int) -> None:
        self.offset += delta

    def top(self) -> int:
        return self.st[-1][0] + self.offset

    def getMin(self) -> int:
        return self.st[-1][1] + self.offset""",
        "java_class": """class OffsetMinStack {
    private final Deque<long[]> st = new ArrayDeque<>();
    private long offset = 0L;

    public OffsetMinStack() {}

    public void push(int val) {
        long adj = (long) val - offset;
        long mn = st.isEmpty() ? adj : Math.min(adj, st.peek()[1]);
        st.push(new long[]{adj, mn});
    }

    public void pop() {
        st.pop();
    }

    public void addAll(int delta) {
        offset += delta;
    }

    public long top() {
        return st.peek()[0] + offset;
    }

    public long getMin() {
        return st.peek()[1] + offset;
    }
}""",
        "visible": [
            {
                "ops": ["OffsetMinStack", "push", "push", "getMin", "addAll", "top", "getMin", "push", "top", "getMin", "pop", "getMin"],
                "args": [[], [5], [2], [], [10], [], [], [3], [], [], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "addAll", "push", "getMin", "top"],
                "args": [[], [10], [-15], [0], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "addAll", "pop", "push", "top", "getMin"],
                "args": [[], [4], [100], [], [7], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["OffsetMinStack", "addAll", "push", "top", "getMin"],
                "args": [[], [50], [1], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "addAll", "addAll", "top", "getMin"],
                "args": [[], [1000000000], [1000000000], [1000000000], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "push", "addAll", "pop", "top", "getMin"],
                "args": [[], [-5], [-10], [5], [], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "push", "push", "addAll", "getMin", "pop", "getMin", "pop", "getMin"],
                "args": [[], [3], [1], [2], [-4], [], [], [], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "addAll", "push", "addAll", "getMin", "pop", "getMin"],
                "args": [[], [10], [5], [12], [-3], [], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "push", "addAll", "top", "getMin"],
                "args": [[], [0], [0], [0], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "addAll", "push", "addAll", "push", "top", "getMin"],
                "args": [[], [-1000000000], [-1000000000], [0], [-1000000000], [5], [], []],
            },
            {
                "ops": ["OffsetMinStack", "push", "push", "addAll", "push", "pop", "addAll", "top", "getMin"],
                "args": [[], [8], [4], [2], [1], [], [-6], [], []],
            },
            _perf_68(),
        ],
    },

    # ------------------------------------------------------------------
    # 69 - Transactional Min Stack
    # ------------------------------------------------------------------
    {
        "slug": "69-transactional-min-stack",
        "title": "Transactional Min Stack",
        "difficulty": "Hard",
        "subtopic": "Min Stack",
        "companies": ["Atlassian", "Bloomberg", "Google", "Meta", "Oracle"],
        "desc": (
            "Design a min-stack `TransactionalStack` that supports nested database-style transactions (`begin`, `rollback`, `commit`) alongside `O(1)` minimum queries.\n\n"
            "Implement the `TransactionalStack` class:\n"
            "- `TransactionalStack()` initializes an empty stack with no active transaction.\n"
            "- `void push(int val)` pushes `val` onto the stack.\n"
            "- `int pop()` removes and returns the top element of the stack.\n"
            "- `int top()` returns the top element of the stack.\n"
            "- `int getMin()` returns the minimum element currently in the stack.\n"
            "- `void begin()` opens a new nested transaction block.\n"
            "- `boolean rollback()` reverts all `push` and `pop` operations performed since the most recent open `begin()` and closes that transaction; returns `true` if a transaction was active, or `false` if no transaction is open.\n"
            "- `boolean commit()` merges the most recent open transaction's changes into its enclosing transaction (or base state) and closes it; returns `true` if a transaction was active, or `false` otherwise."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Methods pop, top, and getMin are always called on non-empty stacks.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Maintain a standard O(1) min-stack plus a stack of transaction undo logs, where each undo log records the inverse of every push or pop performed during that transaction.",
            "Store each transaction's undo log as a singly linked list in reverse chronological order with (head, tail) pointers so push/pop prepend in O(1), commit splices into the parent list in O(1), and rollback replays from head in amortized O(1)."
        ],
        "explanations": [
            "Push 5 -> begin -> push 2 (min 2) -> rollback restores [5] (min 5); next begin -> push 1 -> commit makes [5, 1] permanent (min 1).",
            "Calling rollback or commit when no transaction is open returns false.",
            "Nested transactions allow committing an inner block into an outer block and later rolling back both together."
        ],
        "time": "O(1) amortized per op",
        "space": "O(n)",
        "kind": "design",
        "className": "TransactionalStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "int"),
            ("top", [], "int"),
            ("getMin", [], "int"),
            ("begin", [], "void"),
            ("rollback", [], "boolean"),
            ("commit", [], "boolean"),
        ],
        "py_class": """class TransactionalStack:
    def __init__(self):
        self.st = []  # (val, running_min)
        self.tx = []  # list of [head, tail] where node is [is_push_undo, val, next]

    def _raw_push(self, val: int) -> None:
        mn = val if not self.st or val < self.st[-1][1] else self.st[-1][1]
        self.st.append((val, mn))

    def _raw_pop(self) -> int:
        return self.st.pop()[0]

    def _record(self, is_push_undo: bool, val: int) -> None:
        if self.tx:
            frame = self.tx[-1]
            node = [is_push_undo, val, frame[0]]
            frame[0] = node
            if frame[1] is None:
                frame[1] = node

    def push(self, val: int) -> None:
        self._raw_push(val)
        self._record(False, 0)  # undo push by popping

    def pop(self) -> int:
        val = self._raw_pop()
        self._record(True, val)  # undo pop by pushing val
        return val

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]

    def begin(self) -> None:
        self.tx.append([None, None])

    def rollback(self) -> bool:
        if not self.tx:
            return False
        cur = self.tx.pop()[0]
        while cur is not None:
            if cur[0]:
                self._raw_push(cur[1])
            else:
                self._raw_pop()
            cur = cur[2]
        return True

    def commit(self) -> bool:
        if not self.tx:
            return False
        child = self.tx.pop()
        if self.tx and child[0] is not None:
            parent = self.tx[-1]
            child[1][2] = parent[0]
            parent[0] = child[0]
            if parent[1] is None:
                parent[1] = child[1]
        return True""",
        "java_class": """class TransactionalStack {
    private static class UndoNode {
        boolean pushUndo;
        int val;
        UndoNode next;
        UndoNode(boolean pushUndo, int val, UndoNode next) {
            this.pushUndo = pushUndo;
            this.val = val;
            this.next = next;
        }
    }

    private final Deque<int[]> st = new ArrayDeque<>();
    private final Deque<UndoNode[]> tx = new ArrayDeque<>();

    public TransactionalStack() {}

    private void rawPush(int val) {
        int mn = st.isEmpty() ? val : Math.min(val, st.peek()[1]);
        st.push(new int[]{val, mn});
    }

    private int rawPop() {
        return st.pop()[0];
    }

    private void record(boolean pushUndo, int val) {
        if (!tx.isEmpty()) {
            UndoNode[] frame = tx.peek();
            UndoNode node = new UndoNode(pushUndo, val, frame[0]);
            frame[0] = node;
            if (frame[1] == null) frame[1] = node;
        }
    }

    public void push(int val) {
        rawPush(val);
        record(false, 0);
    }

    public int pop() {
        int val = rawPop();
        record(true, val);
        return val;
    }

    public int top() {
        return st.peek()[0];
    }

    public int getMin() {
        return st.peek()[1];
    }

    public void begin() {
        tx.push(new UndoNode[]{null, null});
    }

    public boolean rollback() {
        if (tx.isEmpty()) return false;
        UndoNode cur = tx.pop()[0];
        while (cur != null) {
            if (cur.pushUndo) rawPush(cur.val);
            else rawPop();
            cur = cur.next;
        }
        return true;
    }

    public boolean commit() {
        if (tx.isEmpty()) return false;
        UndoNode[] child = tx.pop();
        if (!tx.isEmpty() && child[0] != null) {
            UndoNode[] parent = tx.peek();
            child[1].next = parent[0];
            parent[0] = child[0];
            if (parent[1] == null) parent[1] = child[1];
        }
        return true;
    }
}""",
        "visible": [
            {
                "ops": ["TransactionalStack", "push", "begin", "push", "getMin", "rollback", "getMin", "begin", "push", "commit", "getMin", "top"],
                "args": [[], [5], [], [2], [], [], [], [], [1], [], [], []],
            },
            {
                "ops": ["TransactionalStack", "rollback", "commit", "push", "top"],
                "args": [[], [], [], [9], []],
            },
            {
                "ops": ["TransactionalStack", "push", "begin", "push", "begin", "pop", "push", "commit", "top", "rollback", "top", "getMin"],
                "args": [[], [5], [], [2], [], [], [8], [], [], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["TransactionalStack", "begin", "push", "pop", "rollback", "push", "top"],
                "args": [[], [], [7], [], [], [3], []],
            },
            {
                "ops": ["TransactionalStack", "push", "push", "begin", "pop", "getMin", "rollback", "getMin", "top"],
                "args": [[], [10], [2], [], [], [], [], [], []],
            },
            {
                "ops": ["TransactionalStack", "begin", "begin", "begin", "push", "commit", "commit", "rollback", "push", "getMin"],
                "args": [[], [], [], [], [4], [], [], [], [9], []],
            },
            {
                "ops": ["TransactionalStack", "push", "begin", "commit", "rollback", "top"],
                "args": [[], [1], [], [], [], []],
            },
            {
                "ops": ["TransactionalStack", "push", "begin", "push", "begin", "push", "rollback", "top", "getMin", "commit", "top", "getMin"],
                "args": [[], [6], [], [3], [], [1], [], [], [], [], [], []],
            },
            {
                "ops": ["TransactionalStack", "push", "push", "begin", "pop", "pop", "push", "rollback", "top", "getMin"],
                "args": [[], [-5], [4], [], [], [], [100], [], [], []],
            },
            {
                "ops": ["TransactionalStack", "begin", "push", "begin", "commit", "push", "commit", "getMin", "top"],
                "args": [[], [], [8], [], [], [2], [], [], []],
            },
            {
                "ops": ["TransactionalStack", "push", "begin", "push", "pop", "push", "begin", "pop", "rollback", "top", "rollback", "top"],
                "args": [[], [11], [], [22], [], [33], [], [], [], [], [], []],
            },
            _perf_69(),
        ],
    },

    # ------------------------------------------------------------------
    # 70 - Second Minimum Stack
    # ------------------------------------------------------------------
    {
        "slug": "70-second-minimum-stack",
        "title": "Second Minimum Stack",
        "difficulty": "Easy",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Apple"],
        "desc": (
            "Design a stack `SecondMinStack` that supports standard stack operations plus retrieving both the smallest and the second smallest values currently in the stack in `O(1)` time.\n\n"
            "Implement the `SecondMinStack` class:\n"
            "- `SecondMinStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes `val` onto the stack.\n"
            "- `void pop()` removes the top element of the stack.\n"
            "- `int top()` returns the top element of the stack.\n"
            "- `int getMin()` returns the smallest value in the stack.\n"
            "- `int getSecondMin()` returns the second smallest value in the stack (counting duplicates; e.g., for `[2, 5, 2]`, the sorted elements are `[2, 2, 5]`, so `getMin()` is `2` and `getSecondMin()` is `2`)."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Methods pop, top, and getMin are called only when the stack has at least 1 element.",
            "Method getSecondMin is called only when the stack has at least 2 elements.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Alongside each pushed value, store the running smallest (min1) and running second smallest (min2) at that stack depth.",
            "When pushing val: if val < min1 then (newMin1, newMin2) = (val, min1); else if val < min2 then (min1, val); else keep (min1, min2)."
        ],
        "explanations": [
            "After pushing 5, 2, 8, sorted values are [2, 5, 8] -> min 2, secondMin 5; pushing 1 makes [1, 2, 5, 8] -> min 1, secondMin 2; popping 1 restores min 2, secondMin 5.",
            "With duplicate minimums [3, 3, 7], both getMin and getSecondMin return 3.",
            "Negative values and decreasing pushes update min1 and min2 in O(1) per operation."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "SecondMinStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "void"),
            ("top", [], "int"),
            ("getMin", [], "int"),
            ("getSecondMin", [], "int"),
        ],
        "py_class": """class SecondMinStack:
    def __init__(self):
        self.st = []  # (val, min1, min2)

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, 10**18))
        else:
            _, m1, m2 = self.st[-1]
            if val < m1:
                self.st.append((val, val, m1))
            elif val < m2:
                self.st.append((val, m1, val))
            else:
                self.st.append((val, m1, m2))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]

    def getSecondMin(self) -> int:
        return self.st[-1][2]""",
        "java_class": """class SecondMinStack {
    private final Deque<long[]> st = new ArrayDeque<>();

    public SecondMinStack() {}

    public void push(int val) {
        if (st.isEmpty()) {
            st.push(new long[]{val, val, Long.MAX_VALUE});
        } else {
            long[] prev = st.peek();
            long m1 = prev[1], m2 = prev[2];
            if (val < m1) {
                st.push(new long[]{val, val, m1});
            } else if (val < m2) {
                st.push(new long[]{val, m1, val});
            } else {
                st.push(new long[]{val, m1, m2});
            }
        }
    }

    public void pop() {
        st.pop();
    }

    public int top() {
        return (int) st.peek()[0];
    }

    public int getMin() {
        return (int) st.peek()[1];
    }

    public int getSecondMin() {
        return (int) st.peek()[2];
    }
}""",
        "visible": [
            {
                "ops": ["SecondMinStack", "push", "push", "push", "getMin", "getSecondMin", "push", "getMin", "getSecondMin", "pop", "getSecondMin"],
                "args": [[], [5], [2], [8], [], [], [1], [], [], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "push", "getMin", "getSecondMin"],
                "args": [[], [3], [3], [7], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "getMin", "getSecondMin", "push", "getMin", "getSecondMin"],
                "args": [[], [0], [-5], [], [], [-10], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["SecondMinStack", "push", "push", "top", "getMin", "getSecondMin"],
                "args": [[], [10], [20], [], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "push", "pop", "getSecondMin"],
                "args": [[], [5], [5], [5], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "push", "getSecondMin", "pop", "getSecondMin"],
                "args": [[], [1000000000], [-1000000000], [0], [], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "pop", "push", "push", "getMin", "getSecondMin"],
                "args": [[], [-99], [], [4], [9], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "push", "push", "getSecondMin", "pop", "getSecondMin", "pop", "getSecondMin"],
                "args": [[], [9], [7], [8], [6], [], [], [], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "push", "getMin", "getSecondMin", "pop", "top"],
                "args": [[], [1], [2], [1], [], [], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "push", "push", "getMin", "getSecondMin"],
                "args": [[], [4], [3], [2], [1], [], []],
            },
            {
                "ops": ["SecondMinStack", "push", "push", "push", "push", "getMin", "getSecondMin"],
                "args": [[], [1], [2], [3], [4], [], []],
            },
            _perf_70(),
        ],
    },

    # ------------------------------------------------------------------
    # 71 - Min Stack With Minimum Count
    # ------------------------------------------------------------------
    {
        "slug": "71-min-stack-with-min-count",
        "title": "Min Stack With Minimum Count",
        "difficulty": "Easy",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Google", "Meta", "Goldman Sachs"],
        "desc": (
            "Design a stack `CountMinStack` that supports standard stack operations plus querying both the current minimum value and how many times that minimum value appears in the stack — all in `O(1)` time.\n\n"
            "Implement the `CountMinStack` class:\n"
            "- `CountMinStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes `val` onto the stack.\n"
            "- `void pop()` removes the top element of the stack.\n"
            "- `int top()` returns the top element of the stack.\n"
            "- `int getMin()` returns the minimum value currently in the stack.\n"
            "- `int getMinCount()` returns the number of elements in the stack equal to `getMin()`."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Methods pop, top, getMin, and getMinCount are always called on non-empty stacks.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Store (val, curMin, minCount) at each stack level — or keep a secondary stack of [minVal, count] pairs.",
            "On push(val): if val < curMin start count at 1; if val == curMin increment count; if val > curMin carry over (curMin, minCount)."
        ],
        "explanations": [
            "After pushing [4, 2, 5, 2], minimum is 2 with count 2; popping 2 drops count to 1; popping 5 and 2 leaves [4] with min 4 and count 1.",
            "Pushing three 7s yields min 7 with count 3.",
            "When a strictly smaller value -1 arrives, min becomes -1 with count 1; popping it restores the previous minimum and count."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "CountMinStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "void"),
            ("top", [], "int"),
            ("getMin", [], "int"),
            ("getMinCount", [], "int"),
        ],
        "py_class": """class CountMinStack:
    def __init__(self):
        self.st = []  # (val, min_val, min_cnt)

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, 1))
        else:
            _, mn, cnt = self.st[-1]
            if val < mn:
                self.st.append((val, val, 1))
            elif val == mn:
                self.st.append((val, mn, cnt + 1))
            else:
                self.st.append((val, mn, cnt))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getMin(self) -> int:
        return self.st[-1][1]

    def getMinCount(self) -> int:
        return self.st[-1][2]""",
        "java_class": """class CountMinStack {
    private final Deque<int[]> st = new ArrayDeque<>();

    public CountMinStack() {}

    public void push(int val) {
        if (st.isEmpty()) {
            st.push(new int[]{val, val, 1});
        } else {
            int[] prev = st.peek();
            if (val < prev[1]) {
                st.push(new int[]{val, val, 1});
            } else if (val == prev[1]) {
                st.push(new int[]{val, prev[1], prev[2] + 1});
            } else {
                st.push(new int[]{val, prev[1], prev[2]});
            }
        }
    }

    public void pop() {
        st.pop();
    }

    public int top() {
        return st.peek()[0];
    }

    public int getMin() {
        return st.peek()[1];
    }

    public int getMinCount() {
        return st.peek()[2];
    }
}""",
        "visible": [
            {
                "ops": ["CountMinStack", "push", "push", "push", "push", "getMin", "getMinCount", "pop", "getMinCount", "pop", "pop", "getMin", "getMinCount"],
                "args": [[], [4], [2], [5], [2], [], [], [], [], [], [], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "getMin", "getMinCount"],
                "args": [[], [7], [7], [7], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "getMin", "getMinCount", "pop", "getMin", "getMinCount"],
                "args": [[], [3], [3], [-1], [], [], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["CountMinStack", "push", "top", "getMin", "getMinCount"],
                "args": [[], [0], [], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "pop", "push", "push", "getMin", "getMinCount"],
                "args": [[], [-10], [], [5], [5], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "push", "getMinCount", "pop", "getMinCount"],
                "args": [[], [-5], [-5], [-5], [-5], [], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "push", "getMin", "getMinCount"],
                "args": [[], [10], [8], [6], [4], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "push", "getMin", "getMinCount"],
                "args": [[], [4], [6], [8], [10], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "push", "pop", "getMin", "getMinCount"],
                "args": [[], [1], [2], [1], [0], [], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "getMin", "getMinCount"],
                "args": [[], [-1000000000], [1000000000], [-1000000000], [], []],
            },
            {
                "ops": ["CountMinStack", "push", "push", "push", "pop", "push", "getMin", "getMinCount"],
                "args": [[], [2], [1], [1], [], [1], [], []],
            },
            _perf_71(),
        ],
    },

    # ------------------------------------------------------------------
    # 72 - Persistent Min Stack
    # ------------------------------------------------------------------
    {
        "slug": "72-persistent-min-stack",
        "title": "Persistent Min Stack",
        "difficulty": "Hard",
        "subtopic": "Min Stack",
        "companies": ["Google", "Meta", "Bloomberg", "Atlassian", "Amazon"],
        "desc": (
            "Design an immutable, versioned **Persistent Min Stack** (`PersistentMinStack`) where every `push` and `pop` leaves all previous versions intact and produces a new sequential version ID (`1, 2, 3, ...`), all in `O(1)` time and `O(1)` extra space per operation.\n\n"
            "Implement the `PersistentMinStack` class:\n"
            "- `PersistentMinStack()` initializes version `0` as an empty stack.\n"
            "- `int push(int version, int val)` creates a new version equal to `version` with `val` pushed on top, and returns the new version ID.\n"
            "- `int pop(int version)` creates a new version equal to `version` with its top element removed, and returns the new version ID.\n"
            "- `int top(int version)` returns the top element of `version`.\n"
            "- `int getMin(int version)` returns the minimum element currently in `version`."
        ),
        "cons": [
            "-10^9 <= val <= 10^9",
            "Every version argument is a previously created version ID (0 <= version <= latestVersion).",
            "Methods pop, top, and getMin are always called on non-empty versions.",
            "At most 5 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Represent stack nodes as persistent tree nodes storing (val, runningMin, parentNode), with node 0 as the empty sentinel.",
            "Keep an array nodeOfVersion mapping each version ID to its head node: push creates one new child node in O(1), and pop simply maps the new version ID to parent[nodeOfVersion[version]] in O(1)."
        ],
        "explanations": [
            "v1 = [5], v2 = [5, 2] (min 2), v3 branches from v1 to [5, 8] (min 5), v4 pops v2 back to [5] (top 5, min 5).",
            "Popping a single-element version produces an empty version that can be pushed onto again cleanly.",
            "Multiple branches from the same ancestor version remain completely independent."
        ],
        "time": "O(1) per op",
        "space": "O(1) per op",
        "kind": "design",
        "className": "PersistentMinStack",
        "ctorParams": [],
        "methods": [
            ("push", [("version", "int"), ("val", "int")], "int"),
            ("pop", [("version", "int")], "int"),
            ("top", [("version", "int")], "int"),
            ("getMin", [("version", "int")], "int"),
        ],
        "py_class": """class PersistentMinStack:
    def __init__(self):
        self.val = [0]
        self.min_val = [0]
        self.parent = [0]
        self.ver_node = [0]  # version 0 -> empty sentinel node 0

    def push(self, version: int, val: int) -> int:
        p = self.ver_node[version]
        mn = val if p == 0 or val < self.min_val[p] else self.min_val[p]
        node_id = len(self.val)
        self.val.append(val)
        self.min_val.append(mn)
        self.parent.append(p)
        self.ver_node.append(node_id)
        return len(self.ver_node) - 1

    def pop(self, version: int) -> int:
        p = self.ver_node[version]
        self.ver_node.append(self.parent[p])
        return len(self.ver_node) - 1

    def top(self, version: int) -> int:
        return self.val[self.ver_node[version]]

    def getMin(self, version: int) -> int:
        return self.min_val[self.ver_node[version]]""",
        "java_class": """class PersistentMinStack {
    private final List<Integer> val = new ArrayList<>();
    private final List<Integer> minVal = new ArrayList<>();
    private final List<Integer> parent = new ArrayList<>();
    private final List<Integer> verNode = new ArrayList<>();

    public PersistentMinStack() {
        val.add(0);
        minVal.add(0);
        parent.add(0);
        verNode.add(0);
    }

    public int push(int version, int x) {
        int p = verNode.get(version);
        int mn = (p == 0) ? x : Math.min(x, minVal.get(p));
        int nodeId = val.size();
        val.add(x);
        minVal.add(mn);
        parent.add(p);
        verNode.add(nodeId);
        return verNode.size() - 1;
    }

    public int pop(int version) {
        int p = verNode.get(version);
        verNode.add(parent.get(p));
        return verNode.size() - 1;
    }

    public int top(int version) {
        return val.get(verNode.get(version));
    }

    public int getMin(int version) {
        return minVal.get(verNode.get(version));
    }
}""",
        "visible": [
            {
                "ops": ["PersistentMinStack", "push", "push", "push", "getMin", "getMin", "pop", "top", "getMin"],
                "args": [[], [0, 5], [1, 2], [1, 8], [2], [3], [2], [4], [4]],
            },
            {
                "ops": ["PersistentMinStack", "push", "pop", "push", "top", "getMin"],
                "args": [[], [0, 10], [1], [2, 3], [3], [3]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "push", "push", "getMin", "getMin", "top", "top"],
                "args": [[], [0, 7], [1, 9], [1, -4], [0, 12], [2], [3], [3], [4]],
            },
        ],
        "hidden": [
            {
                "ops": ["PersistentMinStack", "push", "top", "getMin"],
                "args": [[], [0, -1], [1], [1]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "push", "pop", "pop", "top", "getMin"],
                "args": [[], [0, 10], [1, 5], [2, 1], [3], [4], [5], [5]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "pop", "push", "getMin", "getMin"],
                "args": [[], [0, 4], [1, 4], [2], [3, 6], [2], [4]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "push", "pop", "getMin", "getMin"],
                "args": [[], [0, 100], [1, -100], [2, 50], [3], [3], [4]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "push", "pop", "push", "top", "getMin"],
                "args": [[], [0, 3], [1, 2], [2, 1], [2], [4, 5], [5], [5]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "pop", "pop", "push", "top", "getMin"],
                "args": [[], [0, -1000000000], [1, 1000000000], [2], [3], [4, 0], [5], [5]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "push", "top", "getMin", "top", "getMin"],
                "args": [[], [0, 8], [1, 3], [2, 1], [1], [1], [3], [3]],
            },
            {
                "ops": ["PersistentMinStack", "push", "push", "pop", "push", "pop", "top", "getMin"],
                "args": [[], [0, 5], [1, 9], [2], [3, 2], [4], [5], [5]],
            },
            _perf_72(),
        ],
    },
])


def main():
    assert len(TASKS) == 30, f"Expected 30 tasks, got {len(TASKS)}"
    expected_prefixes = list(range(43, 73))
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

    print(f"Generated {len(TASKS)} stack problems (43-72) in {BASE}")


if __name__ == "__main__":
    main()
