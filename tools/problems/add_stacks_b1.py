#!/usr/bin/env python3
"""Generate stacks problems 13-42 for AlgoPlay."""
from __future__ import annotations

import json
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


def _make_perf_two_stacks():
    rng = random.Random(1601)
    cap = 200
    ops = ["TwoStacks"]
    args = [[cap]]
    s1 = s2 = 0
    for _ in range(1000):
        r = rng.random()
        if r < 0.35:
            ops.append("push1")
            args.append([rng.randint(0, 10**6)])
            if s1 + s2 < cap:
                s1 += 1
        elif r < 0.70:
            ops.append("push2")
            args.append([rng.randint(0, 10**6)])
            if s1 + s2 < cap:
                s2 += 1
        elif r < 0.80:
            ops.append("pop1")
            args.append([])
            if s1 > 0:
                s1 -= 1
        elif r < 0.90:
            ops.append("pop2")
            args.append([])
            if s2 > 0:
                s2 -= 1
        elif r < 0.95:
            ops.append("size1")
            args.append([])
        else:
            ops.append("size2")
            args.append([])
    return {"ops": ops, "args": args}


def _make_perf_robot_collisions():
    rng = random.Random(2201)
    n = 400
    positions = rng.sample(range(1, 10000), n)
    healths = [rng.randint(1, 50) for _ in range(n)]
    directions = "".join(rng.choice("LR") for _ in range(n))
    return {"positions": positions, "healths": healths, "directions": directions}


def _make_perf_range_stack():
    rng = random.Random(3801)
    ops = ["RangeStack"]
    args = [[]]
    sz = 0
    for _ in range(1000):
        if sz == 0 or rng.random() < 0.58:
            ops.append("push")
            args.append([rng.randint(-10**9, 10**9)])
            sz += 1
        else:
            choice = rng.choice(["pop", "top", "getRange"])
            ops.append(choice)
            args.append([])
            if choice == "pop":
                sz -= 1
    return {"ops": ops, "args": args}


def _make_perf_custom_stack():
    rng = random.Random(3901)
    max_sz = 150
    ops = ["CustomStack"]
    args = [[max_sz]]
    for _ in range(1000):
        r = rng.random()
        if r < 0.45:
            ops.append("push")
            args.append([rng.randint(1, 1000)])
        elif r < 0.75:
            ops.append("increment")
            args.append([rng.randint(1, 180), rng.randint(1, 100)])
        else:
            ops.append("pop")
            args.append([])
    return {"ops": ops, "args": args}


def _make_perf_middle_stack():
    rng = random.Random(4001)
    ops = ["MiddleStack"]
    args = [[]]
    for _ in range(1000):
        r = rng.random()
        if r < 0.48:
            ops.append("push")
            args.append([rng.randint(0, 10**6)])
        elif r < 0.65:
            ops.append("pop")
            args.append([])
        elif r < 0.78:
            ops.append("top")
            args.append([])
        elif r < 0.89:
            ops.append("getMiddle")
            args.append([])
        else:
            ops.append("popMiddle")
            args.append([])
    return {"ops": ops, "args": args}


def _make_perf_max_stack():
    rng = random.Random(4101)
    ops = ["MaxStack"]
    args = [[]]
    sz = 0
    for _ in range(1000):
        if sz == 0 or rng.random() < 0.55:
            ops.append("push")
            args.append([rng.randint(-50, 50)])
            sz += 1
        else:
            choice = rng.choice(["pop", "top", "peekMax", "popMax"])
            ops.append(choice)
            args.append([])
            if choice in ("pop", "popMax"):
                sz -= 1
    return {"ops": ops, "args": args}


def _make_perf_freq_stack():
    rng = random.Random(4201)
    ops = ["FreqStack"]
    args = [[]]
    sz = 0
    for _ in range(1000):
        if sz == 0 or rng.random() < 0.58:
            ops.append("push")
            args.append([rng.randint(1, 25)])
            sz += 1
        else:
            ops.append("pop")
            args.append([])
            sz -= 1
    return {"ops": ops, "args": args}


def _make_perf_min_max_expr():
    expr = "42"
    for i in range(1, 180):
        if i % 2 == 0:
            expr = f"min({i - 90},{expr})"
        else:
            expr = f"max({expr},{50 - i})"
    return expr


def _make_perf_ternary():
    rng = random.Random(3301)
    parts = []
    for _ in range(250):
        cond = rng.choice("TF")
        val = str(rng.randint(0, 9))
        parts.append(f"{cond}?{val}:")
    parts.append("7")
    return "".join(parts)


def _make_perf_preorder():
    # Build a valid full binary tree preorder of 401 nodes (200 internal + 201 nulls)
    out = []
    def build(depth, cap):
        if depth == 0 or cap[0] <= 0:
            out.append("#")
            return
        cap[0] -= 1
        out.append(str(cap[0] + 1))
        build(depth - 1, cap)
        build(depth - 1, cap)
    build(9, [200])
    return ",".join(out)


def _make_perf_bool_expr():
    expr = "t"
    for i in range(120):
        if i % 3 == 0:
            expr = f"!({expr})"
        elif i % 3 == 1:
            expr = f"&(t,{expr},t)"
        else:
            expr = f"|(f,{expr},f)"
    return expr


def _make_perf_infix():
    ops_cycle = ["+", "-", "*", "/", "^"]
    tokens = []
    for i in range(120):
        if i > 0:
            tokens.append(ops_cycle[i % 5])
        if i % 6 == 0:
            tokens.extend(["(", f"x{i}", "+", f"y{i}", ")"])
        else:
            tokens.append(f"v{i}")
    return tokens


TASKS = [
    # ------------------------------------------------------------------
    # 13 - Baseball Game Score
    # ------------------------------------------------------------------
    {
        "slug": "13-baseball-game-score",
        "title": "Baseball Game Score",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": (
            "You are keeping the scores for a baseball game with unusual rules. "
            "At the beginning of the game, you start with an empty record.\n\n"
            "You are given a list of strings `operations`, where `operations[i]` is the `i`-th operation you must apply to the record and is one of the following:\n"
            "- An integer `x`: record a new score of `x`.\n"
            "- `'+'`: record a new score that is the sum of the previous two scores.\n"
            "- `'D'`: record a new score that is double the previous score.\n"
            "- `'C'`: invalidate the previous score, removing it from the record.\n\n"
            "Return the sum of all the scores remaining on the record after applying all operations."
        ),
        "cons": [
            "1 <= operations.length <= 1000",
            "operations[i] is 'C', 'D', '+', or a string representing an integer in [-3 * 10^4, 3 * 10^4].",
            "For '+', there are always at least two previous scores on the record.",
            "For 'C' and 'D', there is always at least one previous score on the record.",
            "All intermediate calculations and the final sum fit in a 32-bit signed integer."
        ],
        "hints": [
            "Maintain a stack of active scores so the most recent one or two scores are always accessible in O(1) time.",
            "For 'C', pop the top element; for 'D', push 2 * stack[-1]; for '+', push stack[-1] + stack[-2]."
        ],
        "explanations": [
            "Record evolves: [5] -> [5, 2] -> [5] -> [5, 10] -> [5, 10, 15], sum = 30.",
            "Record evolves: [5] -> [5, -2] -> [5, -2, 4] -> [5, -2] (C) -> [5, -2, -4] (D) -> [5, -2, -4, 9] -> [5, -2, -4, 9, 5] (+) -> [5, -2, -4, 9, 5, 14] (+), totaling 27.",
            "The single score 1 is invalidated by 'C', leaving an empty record with sum 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "calPoints",
        "params": [("operations", "String[]")],
        "ret": "int",
        "py": """        stack = []
        for op in operations:
            if op == "C":
                stack.pop()
            elif op == "D":
                stack.append(stack[-1] * 2)
            elif op == "+":
                stack.append(stack[-1] + stack[-2])
            else:
                stack.append(int(op))
        return sum(stack)""",
        "java": """        Deque<Integer> stack = new ArrayDeque<>();
        for (String op : operations) {
            if (op.equals("C")) {
                stack.pop();
            } else if (op.equals("D")) {
                stack.push(stack.peek() * 2);
            } else if (op.equals("+")) {
                int top = stack.pop();
                int next = top + stack.peek();
                stack.push(top);
                stack.push(next);
            } else {
                stack.push(Integer.parseInt(op));
            }
        }
        int total = 0;
        for (int v : stack) total += v;
        return total;""",
        "visible": [
            {"operations": ["5", "2", "C", "D", "+"]},
            {"operations": ["5", "-2", "4", "C", "D", "9", "+", "+"]},
            {"operations": ["1", "C"]},
        ],
        "hidden": [
            {"operations": ["42"]},
            {"operations": ["-10", "D", "D", "C"]},
            {"operations": ["0", "0", "+", "D", "+"]},
            {"operations": ["10", "20", "C", "C", "5"]},
            {"operations": ["-5", "-10", "+", "D", "+"]},
            {"operations": ["1", "2", "+", "+", "+", "+"]},
            {"operations": ["100", "C", "200", "C", "300", "C"]},
            {"operations": ["3", "6", "9", "D", "C", "+", "D"]},
            {"operations": (["3", "5", "+", "C", "D", "-2", "+"] * 120)},
        ],
    },

    # ------------------------------------------------------------------
    # 14 - Crawler Log Folder
    # ------------------------------------------------------------------
    {
        "slug": "14-crawler-log-folder",
        "title": "Crawler Log Folder",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Microsoft", "Amazon", "Meta"],
        "desc": (
            "A file system maintains a log each time a user performs a change-folder operation starting from the main (root) folder:\n"
            "- `\"../\"`: move to the parent folder of the current folder (if already in the main folder, remain in the main folder).\n"
            "- `\"./\"`: remain in the same folder.\n"
            "- `\"x/\"`: move to the child folder named `x` (guaranteed to exist).\n\n"
            "Given a list of strings `logs` representing the sequence of operations performed by the user, return the minimum number of operations needed to return to the main folder after all log operations are complete."
        ),
        "cons": [
            "1 <= logs.length <= 10^3",
            "2 <= logs[i].length <= 10",
            "logs[i] contains lowercase English letters, digits, '.', and '/'.",
            "logs[i] follows the format described in the statement."
        ],
        "hints": [
            "Directory navigation follows LIFO order: entering a child folder pushes onto the path stack, and '../' pops if non-empty.",
            "Since only the final depth is needed, you can either maintain an explicit stack or simply track its size without dropping below 0."
        ],
        "explanations": [
            "Entering d1, d2, backing out to d1, entering d21, and staying leaves depth 2.",
            "Entering d1, d2, staying, entering d3, entering d31 leaves depth 3.",
            "All parent operations at root stay at depth 0, and moving into d1 then backing out returns to depth 0."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "minOperations",
        "params": [("logs", "String[]")],
        "ret": "int",
        "py": """        depth = 0
        for log in logs:
            if log == "../":
                if depth > 0:
                    depth -= 1
            elif log != "./":
                depth += 1
        return depth""",
        "java": """        int depth = 0;
        for (String log : logs) {
            if (log.equals("../")) {
                if (depth > 0) depth--;
            } else if (!log.equals("./")) {
                depth++;
            }
        }
        return depth;""",
        "visible": [
            {"logs": ["d1/", "d2/", "../", "d21/", "./"]},
            {"logs": ["d1/", "d2/", "./", "d3/", "../", "d31/"]},
            {"logs": ["d1/", "../", "../", "../"]},
        ],
        "hidden": [
            {"logs": ["./"]},
            {"logs": ["../"]},
            {"logs": ["a/"]},
            {"logs": ["../", "../", "a/", "b/", "../", "c/"]},
            {"logs": ["a/", "b/", "c/", "../", "../", "../"]},
            {"logs": ["./", "./", "x/", "./", "../", "./"]},
            {"logs": ["d1/", "d2/", "d3/", "d4/", "d5/"]},
            {"logs": ["f1/", "../", "f2/", "../", "f3/", "f4/"]},
            {"logs": ["dir/"] * 400 + ["../"] * 150 + ["./"] * 100 + ["sub/"] * 200},
        ],
    },

    # ------------------------------------------------------------------
    # 15 - Make The String Great
    # ------------------------------------------------------------------
    {
        "slug": "15-make-the-string-great",
        "title": "Make The String Great",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Microsoft"],
        "desc": (
            "Given a string `s` of lowercase and uppercase English letters, a *good* string is one that does not have two adjacent characters `s[i]` and `s[i + 1]` where:\n"
            "- `s[i]` is a lowercase letter and `s[i + 1]` is the same letter in uppercase, OR\n"
            "- `s[i]` is an uppercase letter and `s[i + 1]` is the same letter in lowercase.\n\n"
            "To make the string good, repeatedly choose any two adjacent characters that violate this rule and remove both of them until no such pair exists. "
            "Return the resulting good string (note that an empty string is also good, and the final result is guaranteed to be unique)."
        ),
        "cons": [
            "1 <= s.length <= 10^4",
            "s contains only lowercase and uppercase English letters."
        ],
        "hints": [
            "Two English letters are the same letter in opposite cases if and only if the absolute difference of their ASCII codes is 32.",
            "Process characters left to right using a stack: if the top of the stack cancels with the current character, pop it; otherwise push the current character."
        ],
        "explanations": [
            "Removing 'eE' from \"leEeetcode\" leaves \"leetcode\", which has no adjacent opposite-case pairs.",
            "Removing 'bB' leaves \"aAcC\", then removing 'aA' and 'cC' yields an empty string \"\".",
            "A single character \"s\" is already good."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "makeGood",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        stack = []
        for ch in s:
            if stack and abs(ord(stack[-1]) - ord(ch)) == 32:
                stack.pop()
            else:
                stack.append(ch)
        return "".join(stack)""",
        "java": """        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            int len = sb.length();
            if (len > 0 && Math.abs(sb.charAt(len - 1) - ch) == 32) {
                sb.deleteCharAt(len - 1);
            } else {
                sb.append(ch);
            }
        }
        return sb.toString();""",
        "visible": [
            {"s": "leEeetcode"},
            {"s": "abBAcC"},
            {"s": "s"},
        ],
        "hidden": [
            {"s": "aA"},
            {"s": "Aa"},
            {"s": "aa"},
            {"s": "AA"},
            {"s": "abcCBA"},
            {"s": "PpQqRrSs"},
            {"s": "mC"},
            {"s": "qFxXfQo"},
            {"s": "abcde" * 200 + "EDCBA" * 200},
        ],
    },

    # ------------------------------------------------------------------
    # 16 - Two Stacks in One Array (Design)
    # ------------------------------------------------------------------
    {
        "slug": "16-two-stacks-in-one-array",
        "title": "Two Stacks in One Array",
        "difficulty": "Easy",
        "subtopic": "LIFO Structure",
        "companies": ["Amazon", "Microsoft", "Oracle", "Adobe"],
        "desc": (
            "Design a data structure `TwoStacks` that implements two independent stacks sharing a single fixed-capacity storage of size `capacity`.\n\n"
            "Implement the `TwoStacks` class:\n"
            "- `TwoStacks(int capacity)` initializes two empty stacks sharing total capacity `capacity`.\n"
            "- `boolean push1(int val)` pushes non-negative integer `val` onto Stack 1 if total elements across both stacks is strictly less than `capacity`, returning `true`; otherwise does nothing and returns `false`.\n"
            "- `boolean push2(int val)` pushes non-negative integer `val` onto Stack 2 if total elements across both stacks is strictly less than `capacity`, returning `true`; otherwise does nothing and returns `false`.\n"
            "- `int pop1()` removes and returns the top element of Stack 1, or `-1` if Stack 1 is empty.\n"
            "- `int pop2()` removes and returns the top element of Stack 2, or `-1` if Stack 2 is empty.\n"
            "- `int size1()` returns the current number of elements in Stack 1.\n"
            "- `int size2()` returns the current number of elements in Stack 2.\n\n"
            "All operations must run in `O(1)` time."
        ),
        "cons": [
            "1 <= capacity <= 10^4",
            "0 <= val <= 10^9",
            "At most 2 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Allocate a single array of length capacity and let Stack 1 grow forward from index 0 while Stack 2 grows backward from index capacity - 1.",
            "The shared storage is full if and only if top1 + 1 == top2."
        ],
        "explanations": [
            "With capacity 3, pushing 10 and 20 onto Stack 1 and 30 onto Stack 2 fills the buffer, so pushing 40 returns false. Popping Stack 1 frees a slot so pushing 40 onto Stack 2 succeeds.",
            "Popping from empty stacks returns -1 and sizes remain 0.",
            "With capacity 1, either stack can occupy the single slot and release it for the other."
        ],
        "time": "O(1) per op",
        "space": "O(capacity)",
        "kind": "design",
        "className": "TwoStacks",
        "ctorParams": [("capacity", "int")],
        "methods": [
            ("push1", [("val", "int")], "boolean"),
            ("push2", [("val", "int")], "boolean"),
            ("pop1", [], "int"),
            ("pop2", [], "int"),
            ("size1", [], "int"),
            ("size2", [], "int"),
        ],
        "py_class": """class TwoStacks:
    def __init__(self, capacity: int):
        self.arr = [0] * capacity
        self.cap = capacity
        self.top1 = -1
        self.top2 = capacity

    def push1(self, val: int) -> bool:
        if self.top1 + 1 == self.top2:
            return False
        self.top1 += 1
        self.arr[self.top1] = val
        return True

    def push2(self, val: int) -> bool:
        if self.top1 + 1 == self.top2:
            return False
        self.top2 -= 1
        self.arr[self.top2] = val
        return True

    def pop1(self) -> int:
        if self.top1 == -1:
            return -1
        val = self.arr[self.top1]
        self.top1 -= 1
        return val

    def pop2(self) -> int:
        if self.top2 == self.cap:
            return -1
        val = self.arr[self.top2]
        self.top2 += 1
        return val

    def size1(self) -> int:
        return self.top1 + 1

    def size2(self) -> int:
        return self.cap - self.top2""",
        "java_class": """class TwoStacks {
    private final int[] arr;
    private final int cap;
    private int top1;
    private int top2;

    public TwoStacks(int capacity) {
        this.arr = new int[capacity];
        this.cap = capacity;
        this.top1 = -1;
        this.top2 = capacity;
    }

    public boolean push1(int val) {
        if (top1 + 1 == top2) return false;
        arr[++top1] = val;
        return true;
    }

    public boolean push2(int val) {
        if (top1 + 1 == top2) return false;
        arr[--top2] = val;
        return true;
    }

    public int pop1() {
        if (top1 == -1) return -1;
        return arr[top1--];
    }

    public int pop2() {
        if (top2 == cap) return -1;
        return arr[top2++];
    }

    public int size1() {
        return top1 + 1;
    }

    public int size2() {
        return cap - top2;
    }
}""",
        "visible": [
            {
                "ops": ["TwoStacks", "push1", "push1", "push2", "push2", "pop1", "push2", "size1", "size2"],
                "args": [[3], [10], [20], [30], [40], [], [40], [], []],
            },
            {
                "ops": ["TwoStacks", "pop1", "pop2", "size1", "size2"],
                "args": [[2], [], [], [], []],
            },
            {
                "ops": ["TwoStacks", "push1", "push2", "pop1", "push2", "pop2"],
                "args": [[1], [7], [8], [], [8], []],
            },
        ],
        "hidden": [
            {
                "ops": ["TwoStacks", "push2", "push2", "push1", "pop2", "pop2", "pop2"],
                "args": [[2], [5], [6], [7], [], [], []],
            },
            {
                "ops": ["TwoStacks", "push1", "push1", "push1", "pop1", "pop1", "pop1", "pop1"],
                "args": [[2], [0], [1], [2], [], [], [], []],
            },
            {
                "ops": ["TwoStacks", "push1", "push2", "size1", "size2", "pop1", "pop2", "size1", "size2"],
                "args": [[5], [100], [200], [], [], [], [], [], []],
            },
            {
                "ops": ["TwoStacks", "push1", "push1", "push1", "push2", "pop1", "push2", "pop2", "pop1"],
                "args": [[3], [1], [2], [3], [4], [], [4], [], []],
            },
            {
                "ops": ["TwoStacks", "push2", "push1", "push2", "push1", "pop1", "pop2", "pop1", "pop2"],
                "args": [[4], [9], [8], [7], [6], [], [], [], []],
            },
            {
                "ops": ["TwoStacks", "push1", "pop2", "pop1", "push2", "pop1", "pop2"],
                "args": [[2], [99], [], [], [88], [], []],
            },
            {
                "ops": ["TwoStacks", "push1", "push1", "pop1", "push2", "push2", "push2", "size1", "size2"],
                "args": [[3], [10], [20], [], [30], [40], [50], [], []],
            },
            {
                "ops": ["TwoStacks", "push1", "push2", "pop1", "push1", "pop2", "push2", "pop1", "pop2"],
                "args": [[2], [0], [1000000000], [], [555], [], [777], [], []],
            },
            _make_perf_two_stacks(),
        ],
    },

    # ------------------------------------------------------------------
    # 17 - Removing Stars From a String
    # ------------------------------------------------------------------
    {
        "slug": "17-removing-stars-from-a-string",
        "title": "Removing Stars From a String",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Amazon", "Google", "Meta", "Microsoft"],
        "desc": (
            "You are given a string `s` consisting of lowercase English letters and stars `'*'`.\n\n"
            "In one operation, you can:\n"
            "- Choose a star `'*'` in `s`.\n"
            "- Remove the closest non-star character to its left, as well as the star itself.\n\n"
            "Return the string after all stars have been removed. The input guarantees that the operation is always possible (every star has a non-star character to its left) and the final string is unique."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists of lowercase English letters and stars '*'.",
            "Every star in s can always remove a non-star character to its left."
        ],
        "hints": [
            "A star behaves just like a backspace key: it deletes the most recently kept character.",
            "Iterate through s pushing letters onto a stack (or StringBuilder) and popping whenever you encounter '*'."
        ],
        "explanations": [
            "The first two stars remove 't' and 'e', leaving \"lecod*e\"; the third star removes 'd', leaving \"lecoe\".",
            "Each star cancels one character to its left until all characters are erased, returning \"\".",
            "With no stars present, \"abcdef\" remains unchanged."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "removeStars",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        stack = []
        for ch in s:
            if ch == '*':
                stack.pop()
            else:
                stack.append(ch)
        return "".join(stack)""",
        "java": """        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '*') {
                sb.deleteCharAt(sb.length() - 1);
            } else {
                sb.append(ch);
            }
        }
        return sb.toString();""",
        "visible": [
            {"s": "leet**cod*e"},
            {"s": "erase*****"},
            {"s": "abcdef"},
        ],
        "hidden": [
            {"s": "a"},
            {"s": "a*"},
            {"s": "ab*c*d*"},
            {"s": "abc***def***"},
            {"s": "abb*cdfg*****x*"},
            {"s": "a*b*c*d*e"},
            {"s": "zzzz**yy*x"},
            {"s": "hello****world*****"},
            {"s": ("abcd**" * 500) + "z"},
        ],
    },

    # ------------------------------------------------------------------
    # 18 - Remove K Adjacent Duplicates
    # ------------------------------------------------------------------
    {
        "slug": "18-remove-k-adjacent-duplicates",
        "title": "Remove K Adjacent Duplicates",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Bloomberg", "Meta", "Google", "Amazon", "Goldman Sachs"],
        "desc": (
            "You are given a lowercase English string `s` and an integer `k`. "
            "A *k-duplicate removal* chooses `k` adjacent and equal letters from `s` and removes them, concatenating the left and right sides of the deleted substring.\n\n"
            "Repeatedly perform k-duplicate removals on `s` until no more can be made, and return the final string. "
            "It is guaranteed that the final answer is unique regardless of the order of removals."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "2 <= k <= 10^4",
            "s contains only lowercase English letters."
        ],
        "hints": [
            "Maintain a stack of (character, consecutiveCount) pairs.",
            "When the current character matches the top of the stack, increment its count and pop the entry as soon as the count reaches k."
        ],
        "explanations": [
            "No two adjacent characters are equal, so \"abcd\" stays unchanged.",
            "Remove \"eee\" -> \"ddbbbdaa\", then \"bbb\" -> \"dddaa\", then \"ddd\" -> \"aa\".",
            "Repeatedly removing adjacent pairs ('bb', 'gg', 'tt', 'cc', 'ii', 'pp', 'oo', 'aa', then 'ii') leaves \"ps\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "removeDuplicates",
        "params": [("s", "String"), ("k", "int")],
        "ret": "String",
        "py": """        stack = []
        for ch in s:
            if stack and stack[-1][0] == ch:
                stack[-1][1] += 1
                if stack[-1][1] == k:
                    stack.pop()
            else:
                stack.append([ch, 1])
        return "".join(ch * cnt for ch, cnt in stack)""",
        "java": """        int n = s.length();
        char[] chars = new char[n];
        int[] counts = new int[n];
        int top = 0;
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (top > 0 && chars[top - 1] == ch) {
                if (++counts[top - 1] == k) {
                    top--;
                }
            } else {
                chars[top] = ch;
                counts[top] = 1;
                top++;
            }
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < top; i++) {
            for (int c = 0; c < counts[i]; c++) {
                sb.append(chars[i]);
            }
        }
        return sb.toString();""",
        "visible": [
            {"s": "abcd", "k": 2},
            {"s": "deeedbbcccbdaa", "k": 3},
            {"s": "pbbcggttciiippooaais", "k": 2},
        ],
        "hidden": [
            {"s": "a", "k": 2},
            {"s": "aaaa", "k": 2},
            {"s": "aaaaa", "k": 2},
            {"s": "aaabbbccc", "k": 3},
            {"s": "aabbbba", "k": 4},
            {"s": "abcde", "k": 100},
            {"s": "yfttttfbbbbnnnnffbgffffgbbbbgssssgthyyyy", "k": 4},
            {"s": "abccba", "k": 2},
            {"s": ("a" * 2 + "b" * 2 + "c" * 3 + "b" + "a") * 300, "k": 3},
        ],
    },

    # ------------------------------------------------------------------
    # 19 - Build an Array With Stack Operations
    # ------------------------------------------------------------------
    {
        "slug": "19-build-an-array-with-stack-operations",
        "title": "Build an Array With Stack Operations",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Apple"],
        "desc": (
            "You are given a strictly increasing integer array `target` and an integer `n`.\n\n"
            "You have an empty stack and a stream of integers `[1, 2, ..., n]` read in ascending order. "
            "Use the following two operations to make the stack (from bottom to top) equal to `target`:\n"
            "- `\"Push\"`: read the next integer from the stream and push it onto the stack.\n"
            "- `\"Pop\"`: remove the integer on the top of the stack.\n\n"
            "Once the stack equals `target`, stop reading immediately and do not perform any further operations. "
            "Return the list of stack operations needed to build `target`."
        ),
        "cons": [
            "1 <= target.length <= 100",
            "1 <= n <= 1000",
            "1 <= target[i] <= n",
            "target is strictly increasing."
        ],
        "hints": [
            "For every stream integer from 1 up to target[-1], you must always emit 'Push'.",
            "If the stream integer is not the next needed element in target, immediately emit 'Pop'; otherwise advance the pointer in target."
        ],
        "explanations": [
            "Push 1 (keep), Push 2 then Pop 2 (skip), Push 3 (keep) produces [1, 3].",
            "Push 1, 2, 3 without popping produces [1, 2, 3].",
            "Push 1 and 2 produces [1, 2]; stop immediately without reading 3 or 4."
        ],
        "time": "O(target[-1])",
        "space": "O(target[-1])",
        "kind": "function",
        "method": "buildArray",
        "params": [("target", "int[]"), ("n", "int")],
        "ret": "List<String>",
        "py": """        ops = []
        cur = 1
        for val in target:
            while cur < val:
                ops.append("Push")
                ops.append("Pop")
                cur += 1
            ops.append("Push")
            cur += 1
        return ops""",
        "java": """        List<String> ops = new ArrayList<>();
        int cur = 1;
        for (int val : target) {
            while (cur < val) {
                ops.add("Push");
                ops.add("Pop");
                cur++;
            }
            ops.add("Push");
            cur++;
        }
        return ops;""",
        "visible": [
            {"target": [1, 3], "n": 3},
            {"target": [1, 2, 3], "n": 3},
            {"target": [1, 2], "n": 4},
        ],
        "hidden": [
            {"target": [1], "n": 1},
            {"target": [5], "n": 5},
            {"target": [2, 4, 6], "n": 6},
            {"target": [1, 4, 7, 10], "n": 10},
            {"target": [3], "n": 10},
            {"target": [1, 2, 3, 4, 5], "n": 5},
            {"target": [2, 3, 4], "n": 4},
            {"target": [10, 20, 30], "n": 50},
            {"target": list(range(10, 501, 10)), "n": 500},
        ],
    },

    # ------------------------------------------------------------------
    # 20 - Maximum Score From Removing Substrings
    # ------------------------------------------------------------------
    {
        "slug": "20-maximum-score-from-removing-substrings",
        "title": "Maximum Score From Removing Substrings",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "You are given a lowercase English string `s` and two positive integers `x` and `y`. "
            "You can perform two types of operations any number of times:\n"
            "- Remove substring `\"ab\"` and gain `x` points.\n"
            "- Remove substring `\"ba\"` and gain `y` points.\n\n"
            "When a substring is removed, the remaining left and right parts are concatenated. "
            "Return the maximum total points you can gain by applying these operations in any order."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "1 <= x, y <= 10^4",
            "s consists of lowercase English letters."
        ],
        "hints": [
            "Within any maximal block of 'a' and 'b' characters, every removal removes one 'a' and one 'b', so the total number of removals is fixed at min(count_a, count_b).",
            "Therefore, it is always optimal to greedily remove as many copies of the higher-scoring pair as possible using a stack pass, and then remove the lower-scoring pair in a second stack pass."
        ],
        "explanations": [
            "Since y = 5 > x = 4, greedily remove \"ba\" pairs first (three times for 15 points), then one \"ab\" for 4 points, totaling 19.",
            "Since x = 5 > y = 4, greedily remove \"ab\" pairs first (four times for 20 points), totaling 20.",
            "No \"ab\" or \"ba\" pairs exist in \"ccc\", so the score is 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "maximumGain",
        "params": [("s", "String"), ("x", "int"), ("y", "int")],
        "ret": "int",
        "py": """        def remove_pair(text: str, first: str, second: str, pts: int):
            stack = []
            gain = 0
            for ch in text:
                if stack and stack[-1] == first and ch == second:
                    stack.pop()
                    gain += pts
                else:
                    stack.append(ch)
            return "".join(stack), gain

        if x >= y:
            rem, g1 = remove_pair(s, 'a', 'b', x)
            _, g2 = remove_pair(rem, 'b', 'a', y)
        else:
            rem, g1 = remove_pair(s, 'b', 'a', y)
            _, g2 = remove_pair(rem, 'a', 'b', x)
        return g1 + g2""",
        "java": """        char first = x >= y ? 'a' : 'b';
        char second = x >= y ? 'b' : 'a';
        int hi = Math.max(x, y);
        int lo = Math.min(x, y);
        int score = 0;
        StringBuilder s1 = new StringBuilder();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            int len = s1.length();
            if (len > 0 && s1.charAt(len - 1) == first && ch == second) {
                s1.deleteCharAt(len - 1);
                score += hi;
            } else {
                s1.append(ch);
            }
        }
        StringBuilder s2 = new StringBuilder();
        for (int i = 0; i < s1.length(); i++) {
            char ch = s1.charAt(i);
            int len = s2.length();
            if (len > 0 && s2.charAt(len - 1) == second && ch == first) {
                s2.deleteCharAt(len - 1);
                score += lo;
            } else {
                s2.append(ch);
            }
        }
        return score;""",
        "visible": [
            {"s": "cdbcbbaaabab", "x": 4, "y": 5},
            {"s": "aabbaaxybbaabb", "x": 5, "y": 4},
            {"s": "ccc", "x": 3, "y": 7},
        ],
        "hidden": [
            {"s": "a", "x": 10, "y": 20},
            {"s": "ab", "x": 10, "y": 20},
            {"s": "ba", "x": 10, "y": 20},
            {"s": "ababab", "x": 5, "y": 5},
            {"s": "aaabbb", "x": 1, "y": 100},
            {"s": "bbbaaa", "x": 100, "y": 1},
            {"s": "aabbabbaa", "x": 7, "y": 3},
            {"s": "babababab", "x": 3, "y": 9},
            {"s": ("aabbaabxbaab" * 250), "x": 13, "y": 29},
        ],
    },

    # ------------------------------------------------------------------
    # 21 - Robot Lexicographically Smallest String
    # ------------------------------------------------------------------
    {
        "slug": "21-robot-lexicographically-smallest-string",
        "title": "Robot Lexicographically Smallest String",
        "difficulty": "Medium",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Amazon", "Uber", "Meta"],
        "desc": (
            "You are given a lowercase English string `s` and a robot that currently holds an empty stack buffer `t`.\n\n"
            "While either `s` or `t` is non-empty, you may perform one of the following two operations:\n"
            "1. Remove the first character of `s` and push it onto the top of `t`.\n"
            "2. Pop the top character of `t` and write it onto paper.\n\n"
            "Return the lexicographically smallest string that can be written onto paper after all characters have been processed."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists of lowercase English letters."
        ],
        "hints": [
            "Precompute suffixMin[i], the smallest character appearing in s[i..n-1].",
            "After pushing s[i] onto stack t, greedily pop and write the top of t as long as t[-1] <= suffixMin[i + 1] (since no strictly smaller character remains in s)."
        ],
        "explanations": [
            "Push 'z', 'z', 'a' onto t, then pop all three in reverse to write \"azz\".",
            "Push 'b', push 'a', pop 'a' (smallest remaining is 'c'), pop 'b', push 'c', pop 'c' -> \"abc\".",
            "Push 'b', 'd', 'd', 'a', pop 'a', then pop 'd', 'd', 'b' -> \"addb\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "robotWithString",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        n = len(s)
        suf_min = ['{'] * (n + 1)
        for i in range(n - 1, -1, -1):
            suf_min[i] = s[i] if s[i] < suf_min[i + 1] else suf_min[i + 1]
        stack = []
        out = []
        for i, ch in enumerate(s):
            stack.append(ch)
            nxt = suf_min[i + 1]
            while stack and stack[-1] <= nxt:
                out.append(stack.pop())
        return "".join(out)""",
        "java": """        int n = s.length();
        char[] sufMin = new char[n + 1];
        sufMin[n] = '{';
        for (int i = n - 1; i >= 0; i--) {
            char c = s.charAt(i);
            sufMin[i] = c < sufMin[i + 1] ? c : sufMin[i + 1];
        }
        char[] stack = new char[n];
        int top = 0;
        StringBuilder out = new StringBuilder(n);
        for (int i = 0; i < n; i++) {
            stack[top++] = s.charAt(i);
            char nxt = sufMin[i + 1];
            while (top > 0 && stack[top - 1] <= nxt) {
                out.append(stack[--top]);
            }
        }
        return out.toString();""",
        "visible": [
            {"s": "zza"},
            {"s": "bac"},
            {"s": "bdda"},
        ],
        "hidden": [
            {"s": "a"},
            {"s": "abcde"},
            {"s": "edcba"},
            {"s": "vzhofnpo"},
            {"s": "bydizfve"},
            {"s": "aaaa"},
            {"s": "cbabc"},
            {"s": "mmxzaab"},
            {"s": "zyxwvutsrqponmlkjihgfedcba" * 80},
        ],
    },

    # ------------------------------------------------------------------
    # 22 - Robot Collisions
    # ------------------------------------------------------------------
    {
        "slug": "22-robot-collisions",
        "title": "Robot Collisions",
        "difficulty": "Hard",
        "subtopic": "LIFO Structure",
        "companies": ["Google", "Meta", "Amazon", "Uber"],
        "desc": (
            "There are `n` robots on a 1D line, each with a distinct initial position `positions[i]`, an integer health `healths[i]`, and a movement direction `directions[i]` (`'L'` for left or `'R'` for right). "
            "All robots start moving simultaneously at the same speed.\n\n"
            "Whenever two robots meet at the same point, they collide:\n"
            "- The robot with lower health is removed from the line, and the robot with higher health has its health decreased by `1` and continues moving.\n"
            "- If both robots have the same health, both are removed from the line.\n\n"
            "Return a list containing the final healths of all surviving robots in the exact order they appeared in the input (or an empty list if none survive)."
        ),
        "cons": [
            "1 <= positions.length == healths.length == directions.length <= 10^5",
            "1 <= positions[i], healths[i] <= 10^9",
            "All values in positions are distinct.",
            "directions[i] is either 'L' or 'R'."
        ],
        "hints": [
            "Sort the robot indices by their starting position from left to right so collisions occur strictly between adjacent moving fronts.",
            "Maintain a stack of indices of surviving right-moving robots; each left-moving robot collides with the top of the stack until it is destroyed or the stack becomes empty."
        ],
        "explanations": [
            "All robots move right, so no collisions occur and healths remain [2, 17, 9, 15, 10].",
            "Sorted by position: 2(R,15), 3(R,10), 5(L,15), 6(L,12). Robot at 5 destroys robot at 3 (becoming hp 14) then loses to robot at 2 (leaving hp 14); robot at 6 then loses to robot at 2, leaving [13].",
            "Adjacent opposing pairs (pos 1 vs 2 with hp 10, and pos 5 vs 6 with hp 11) have equal health and destroy each other, leaving []."
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "kind": "function",
        "method": "survivedRobotsHealths",
        "params": [("positions", "int[]"), ("healths", "int[]"), ("directions", "String")],
        "ret": "List<Integer>",
        "py": """        n = len(positions)
        hp = list(healths)
        order = sorted(range(n), key=lambda i: positions[i])
        stack = []
        for idx in order:
            if directions[idx] == 'R':
                stack.append(idx)
            else:
                while stack and hp[idx] > 0:
                    top = stack[-1]
                    if hp[top] < hp[idx]:
                        stack.pop()
                        hp[top] = 0
                        hp[idx] -= 1
                    elif hp[top] > hp[idx]:
                        hp[top] -= 1
                        hp[idx] = 0
                    else:
                        stack.pop()
                        hp[top] = 0
                        hp[idx] = 0
        return [h for h in hp if h > 0]""",
        "java": """        int n = positions.length;
        Integer[] order = new Integer[n];
        int[] hp = Arrays.copyOf(healths, n);
        for (int i = 0; i < n; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> Integer.compare(positions[a], positions[b]));
        Deque<Integer> stack = new ArrayDeque<>();
        for (int idx : order) {
            if (directions.charAt(idx) == 'R') {
                stack.push(idx);
            } else {
                while (!stack.isEmpty() && hp[idx] > 0) {
                    int top = stack.peek();
                    if (hp[top] < hp[idx]) {
                        stack.pop();
                        hp[top] = 0;
                        hp[idx]--;
                    } else if (hp[top] > hp[idx]) {
                        hp[top]--;
                        hp[idx] = 0;
                    } else {
                        stack.pop();
                        hp[top] = 0;
                        hp[idx] = 0;
                    }
                }
            }
        }
        List<Integer> ans = new ArrayList<>();
        for (int h : hp) {
            if (h > 0) ans.add(h);
        }
        return ans;""",
        "visible": [
            {"positions": [5, 4, 3, 2, 1], "healths": [2, 17, 9, 15, 10], "directions": "RRRRR"},
            {"positions": [3, 5, 2, 6], "healths": [10, 15, 15, 12], "directions": "RLRL"},
            {"positions": [1, 2, 5, 6], "healths": [10, 10, 11, 11], "directions": "RLRL"},
        ],
        "hidden": [
            {"positions": [10], "healths": [5], "directions": "L"},
            {"positions": [1, 2], "healths": [5, 5], "directions": "RL"},
            {"positions": [1, 2], "healths": [5, 5], "directions": "LR"},
            {"positions": [10, 20, 30], "healths": [100, 1, 1], "directions": "RLL"},
            {"positions": [30, 20, 10], "healths": [100, 1, 1], "directions": "LRR"},
            {"positions": [4, 1, 3, 2], "healths": [20, 5, 5, 5], "directions": "LRRR"},
            {"positions": [1, 40], "healths": [10, 11], "directions": "RL"},
            {"positions": [11, 44, 16], "healths": [1, 20, 17], "directions": "RLR"},
            _make_perf_robot_collisions(),
        ],
    },

    # ------------------------------------------------------------------
    # 23 - Maximum Nesting Depth of Parentheses
    # ------------------------------------------------------------------
    {
        "slug": "23-maximum-nesting-depth-of-parentheses",
        "title": "Maximum Nesting Depth of Parentheses",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Bloomberg", "Apple"],
        "desc": (
            "Given a valid parentheses string `s` (which may also contain digits and arithmetic operators `'+'`, `'-'`, `'*'`, `'/'`), "
            "return the maximum nesting depth of `s`.\n\n"
            "The nesting depth at any position is the number of enclosing pairs of parentheses surrounding that position. "
            "If `s` contains no parentheses, its nesting depth is `0`."
        ),
        "cons": [
            "1 <= s.length <= 10^4",
            "s consists of digits '0'-'9', operators '+', '-', '*', '/', and parentheses '(' and ')'.",
            "It is guaranteed that s is a valid parentheses string."
        ],
        "hints": [
            "Each '(' increases the current nesting depth by 1, and each ')' decreases it by 1.",
            "Track the running depth across a single left-to-right scan and record its maximum value."
        ],
        "explanations": [
            "The digit 8 lies inside 3 nested pairs of parentheses.",
            "The digit 3 lies inside 3 nested pairs of parentheses.",
            "There are no parentheses in \"1+2*3\", so the maximum nesting depth is 0."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "maxDepth",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        cur = best = 0
        for ch in s:
            if ch == '(':
                cur += 1
                if cur > best:
                    best = cur
            elif ch == ')':
                cur -= 1
        return best""",
        "java": """        int cur = 0, best = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                cur++;
                if (cur > best) best = cur;
            } else if (ch == ')') {
                cur--;
            }
        }
        return best;""",
        "visible": [
            {"s": "(1+(2*3)+((8)/4))+1"},
            {"s": "(1)+((2))+(((3)))"},
            {"s": "1+2*3"},
        ],
        "hidden": [
            {"s": "0"},
            {"s": "()"},
            {"s": "()()()()"},
            {"s": "((((()))))"},
            {"s": "((1+2)*(3+(4*(5))))"},
            {"s": "((()())(()(())))"},
            {"s": "1+(2*3)/(4-5)"},
            {"s": "((((1)))+((((2)))))"},
            {"s": "(" * 400 + "1" + ")" * 400 + "(" * 200 + ")" * 200},
        ],
    },

    # ------------------------------------------------------------------
    # 24 - Remove Outermost Parentheses
    # ------------------------------------------------------------------
    {
        "slug": "24-remove-outermost-parentheses",
        "title": "Remove Outermost Parentheses",
        "difficulty": "Easy",
        "subtopic": "Valid Parentheses",
        "companies": ["Google", "Microsoft", "Amazon"],
        "desc": (
            "A valid parentheses string `s` is *primitive* if it is non-empty and cannot be split into two non-empty valid parentheses strings `A + B`.\n\n"
            "Given a valid parentheses string `s`, consider its primitive decomposition `s = P_1 + P_2 + ... + P_k`, where each `P_i` is a primitive valid parentheses string. "
            "Return `s` after removing the outermost `'('` and `')'` of every primitive string in its primitive decomposition."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s[i] is either '(' or ')'.",
            "s is a valid parentheses string."
        ],
        "hints": [
            "Track the current open-parenthesis depth as you scan s from left to right.",
            "Include '(' only when depth > 0 before incrementing, and include ')' only when depth > 0 after decrementing."
        ],
        "explanations": [
            "Primitive decomposition is \"(()())\" + \"(())\"; removing outer parentheses gives \"()()\" + \"()\" = \"()()()\".",
            "Primitive decomposition is \"(()())\" + \"(())\" + \"(()(()))\" -> \"()()()()(())\".",
            "Primitive decomposition is \"()\" + \"()\"; stripping outer parentheses leaves \"\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "removeOuterParentheses",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        out = []
        depth = 0
        for ch in s:
            if ch == '(':
                if depth > 0:
                    out.append(ch)
                depth += 1
            else:
                depth -= 1
                if depth > 0:
                    out.append(ch)
        return "".join(out)""",
        "java": """        StringBuilder out = new StringBuilder();
        int depth = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                if (depth > 0) out.append(ch);
                depth++;
            } else {
                depth--;
                if (depth > 0) out.append(ch);
            }
        }
        return out.toString();""",
        "visible": [
            {"s": "(()())(())"},
            {"s": "(()())(())(()(()))"},
            {"s": "()()"},
        ],
        "hidden": [
            {"s": "()"},
            {"s": "(())"},
            {"s": "((()))"},
            {"s": "((())(()))"},
            {"s": "()(()())()"},
            {"s": "(((())))((()))"},
            {"s": "(()(()(())))"},
            {"s": "()()()()()"},
            {"s": "((()())(()))" * 200},
        ],
    },

    # ------------------------------------------------------------------
    # 25 - Score of Parentheses
    # ------------------------------------------------------------------
    {
        "slug": "25-score-of-parentheses",
        "title": "Score of Parentheses",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Google", "Meta", "Bloomberg"],
        "desc": (
            "Given a balanced parentheses string `s`, return the score of `s` according to the following rules:\n"
            "- `\"()\"` has score `1`.\n"
            "- `AB` has score `A + B`, where `A` and `B` are balanced parentheses strings.\n"
            "- `(A)` has score `2 * A`, where `A` is a balanced parentheses string."
        ),
        "cons": [
            "2 <= s.length <= 50",
            "s consists only of '(' and ')'.",
            "s is a balanced parentheses string."
        ],
        "hints": [
            "Use a stack where each frame stores the accumulated score at the current nesting depth.",
            "When seeing '(', push 0 for the new depth; when seeing ')', pop inner score v and add max(2 * v, 1) to the new stack top."
        ],
        "explanations": [
            "A single \"()\" has score 1.",
            "\"(())\" wraps \"()\" (score 1), so its score is 2 * 1 = 2.",
            "\"(()(()))\" evaluates to 2 * (1 + 2 * 1) = 6."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "scoreOfParentheses",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        stack = [0]
        for ch in s:
            if ch == '(':
                stack.append(0)
            else:
                v = stack.pop()
                stack[-1] += max(2 * v, 1)
        return stack[0]""",
        "java": """        Deque<Integer> stack = new ArrayDeque<>();
        stack.push(0);
        for (int i = 0; i < s.length(); i++) {
            if (s.charAt(i) == '(') {
                stack.push(0);
            } else {
                int v = stack.pop();
                int w = stack.pop();
                stack.push(w + Math.max(2 * v, 1));
            }
        }
        return stack.pop();""",
        "visible": [
            {"s": "()"},
            {"s": "(())"},
            {"s": "(()(()))"},
        ],
        "hidden": [
            {"s": "()()"},
            {"s": "((()))"},
            {"s": "(()())"},
            {"s": "()()()()()"},
            {"s": "((()())(()))"},
            {"s": "((((()))))"},
            {"s": "(()(()(())))"},
            {"s": "(" * 20 + ")" * 20},
            {"s": "(" * 15 + "()()" + ")" * 15 + "()" * 5},
        ],
    },

    # ------------------------------------------------------------------
    # 26 - Reverse Substrings Between Parentheses
    # ------------------------------------------------------------------
    {
        "slug": "26-reverse-substrings-between-parentheses",
        "title": "Reverse Substrings Between Parentheses",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Meta", "Google", "Amazon", "Adobe"],
        "desc": (
            "You are given a string `s` consisting of lowercase English letters and balanced parentheses `'('` and `')'`.\n\n"
            "Reverse the substrings enclosed inside each pair of matching parentheses, starting from the innermost pair, and remove all parentheses from the final result. "
            "Return the resulting string."
        ),
        "cons": [
            "1 <= s.length <= 2000",
            "s contains only lowercase English letters and parentheses '(' and ')'.",
            "All parentheses in s are guaranteed to be balanced."
        ],
        "hints": [
            "First match each '(' with its corresponding ')' using a stack, storing bidirectional jumps pair[open] = close and pair[close] = open.",
            "Walk through s starting at index 0 with direction +1; whenever you hit a parenthesis, teleport to pair[i] and flip your traversal direction to achieve O(n) total time."
        ],
        "explanations": [
            "Reversing \"abcd\" inside the single pair of parentheses produces \"dcba\".",
            "First \"love\" reverses to \"evol\", then \"uevoli\" reverses to \"iloveu\".",
            "Innermost \"oc\" -> \"co\", then \"etco\" -> \"octe\", then \"edocteel\" -> \"leetcode\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "reverseParentheses",
        "params": [("s", "String")],
        "ret": "String",
        "py": """        n = len(s)
        pair = [0] * n
        stack = []
        for i, ch in enumerate(s):
            if ch == '(':
                stack.append(i)
            elif ch == ')':
                j = stack.pop()
                pair[i] = j
                pair[j] = i
        out = []
        i, d = 0, 1
        while i < n:
            if s[i] in '()':
                i = pair[i]
                d = -d
            else:
                out.append(s[i])
            i += d
        return "".join(out)""",
        "java": """        int n = s.length();
        int[] pair = new int[n];
        Deque<Integer> stack = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                stack.push(i);
            } else if (ch == ')') {
                int j = stack.pop();
                pair[i] = j;
                pair[j] = i;
            }
        }
        StringBuilder out = new StringBuilder();
        int i = 0, d = 1;
        while (i < n) {
            char ch = s.charAt(i);
            if (ch == '(' || ch == ')') {
                i = pair[i];
                d = -d;
            } else {
                out.append(ch);
            }
            i += d;
        }
        return out.toString();""",
        "visible": [
            {"s": "(abcd)"},
            {"s": "(u(love)i)"},
            {"s": "(ed(et(oc))el)"},
        ],
        "hidden": [
            {"s": "abc"},
            {"s": "()"},
            {"s": "a(())b"},
            {"s": "a(bcdefghijkl(mno)p)q"},
            {"s": "((ab)(cd))"},
            {"s": "(((abc)))"},
            {"s": "(ab)(cd)(ef)"},
            {"s": "ta()usw((((a))))"},
            {"s": "(" * 200 + "abcdefgh" + ")" * 200 + "(" * 199 + "xyz" + ")" * 199},
        ],
    },

    # ------------------------------------------------------------------
    # 27 - Valid Parenthesis String With Wildcards
    # ------------------------------------------------------------------
    {
        "slug": "27-valid-parenthesis-string-with-wildcards",
        "title": "Valid Parenthesis String With Wildcards",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Meta", "Google", "Microsoft", "LinkedIn"],
        "desc": (
            "Given a string `s` containing only three types of characters: `'('`, `')'`, and `'*'`, return `true` if `s` is valid and `false` otherwise.\n\n"
            "The following rules define a valid string:\n"
            "- Every `'('` must have a corresponding `')'` appearing after it.\n"
            "- Every `')'` must have a corresponding `'('` appearing before it.\n"
            "- Each `'*'` may independently be treated as a single `'('`, a single `')'`, or an empty string `\"\"`."
        ),
        "cons": [
            "1 <= s.length <= 10^4",
            "s[i] is '(', ')', or '*'."
        ],
        "hints": [
            "Maintain two stacks of indices: one for unmatched '(' characters and one for '*' wildcards.",
            "When seeing ')', prefer popping from the '(' stack before falling back to the '*' stack; after the scan, match every remaining '(' with a '*' whose index is strictly greater."
        ],
        "explanations": [
            "\"()\" is already a valid pair of parentheses.",
            "Treating '*' as empty yields \"()\", which is valid.",
            "Treating '*' as '(' yields \"(())\", which is valid."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "checkValidString",
        "params": [("s", "String")],
        "ret": "boolean",
        "py": """        opens = []
        stars = []
        for i, ch in enumerate(s):
            if ch == '(':
                opens.append(i)
            elif ch == '*':
                stars.append(i)
            else:
                if opens:
                    opens.pop()
                elif stars:
                    stars.pop()
                else:
                    return False
        while opens and stars:
            if opens[-1] < stars[-1]:
                opens.pop()
                stars.pop()
            else:
                return False
        return not opens""",
        "java": """        Deque<Integer> opens = new ArrayDeque<>();
        Deque<Integer> stars = new ArrayDeque<>();
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == '(') {
                opens.push(i);
            } else if (ch == '*') {
                stars.push(i);
            } else {
                if (!opens.isEmpty()) {
                    opens.pop();
                } else if (!stars.isEmpty()) {
                    stars.pop();
                } else {
                    return false;
                }
            }
        }
        while (!opens.isEmpty() && !stars.isEmpty()) {
            if (opens.peek() < stars.peek()) {
                opens.pop();
                stars.pop();
            } else {
                return false;
            }
        }
        return opens.isEmpty();""",
        "visible": [
            {"s": "()"},
            {"s": "(*)"},
            {"s": "(*))"},
        ],
        "hidden": [
            {"s": "*"},
            {"s": "("},
            {"s": ")"},
            {"s": "*("},
            {"s": ")*"},
            {"s": "(*()"},
            {"s": "(((((*)))**"},
            {"s": "(((((()*)(*)*))())())(()())())))((**)))))(()())()"},
            {"s": "(" * 1000 + "*" * 500 + ")" * 500},
        ],
    },

    # ------------------------------------------------------------------
    # 28 - Check If Parentheses Can Be Valid With Locks
    # ------------------------------------------------------------------
    {
        "slug": "28-check-if-parentheses-can-be-valid-with-locks",
        "title": "Check If Parentheses Can Be Valid With Locks",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Amazon", "Google", "Meta"],
        "desc": (
            "You are given a parentheses string `s` consisting of `'('` and `')'`, and a binary string `locked` of the same length:\n"
            "- If `locked[i] == '1'`, you cannot change `s[i]`.\n"
            "- If `locked[i] == '0'`, you may change `s[i]` to either `'('` or `')'`.\n\n"
            "Return `true` if you can make `s` a valid parentheses string, and `false` otherwise."
        ),
        "cons": [
            "1 <= s.length == locked.length <= 10^5",
            "s[i] is either '(' or ')'.",
            "locked[i] is either '0' or '1'."
        ],
        "hints": [
            "Any odd-length string can never be balanced. For even-length strings, unlocked positions act like wildcards that must become either '(' or ')'.",
            "Track indices of locked '(' in one stack and unlocked positions in another; match each locked ')' against a locked '(' first, then against an unlocked index, and finally pair remaining locked '(' with later unlocked indices."
        ],
        "explanations": [
            "Changing unlocked positions s[0] to '(', s[2] to '(', and s[4] to ')' gives \"()()()\", which is valid.",
            "\"()()\" is already valid even with all positions unlocked.",
            "Odd length 1 can never form a balanced parentheses string."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "canBeValid",
        "params": [("s", "String"), ("locked", "String")],
        "ret": "boolean",
        "py": """        n = len(s)
        if n % 2 == 1:
            return False
        open_locked = []
        unlocked = []
        for i in range(n):
            if locked[i] == '0':
                unlocked.append(i)
            elif s[i] == '(':
                open_locked.append(i)
            else:
                if open_locked:
                    open_locked.pop()
                elif unlocked:
                    unlocked.pop()
                else:
                    return False
        while open_locked and unlocked and open_locked[-1] < unlocked[-1]:
            open_locked.pop()
            unlocked.pop()
        return not open_locked""",
        "java": """        int n = s.length();
        if (n % 2 == 1) return false;
        Deque<Integer> openLocked = new ArrayDeque<>();
        Deque<Integer> unlocked = new ArrayDeque<>();
        for (int i = 0; i < n; i++) {
            if (locked.charAt(i) == '0') {
                unlocked.push(i);
            } else if (s.charAt(i) == '(') {
                openLocked.push(i);
            } else {
                if (!openLocked.isEmpty()) {
                    openLocked.pop();
                } else if (!unlocked.isEmpty()) {
                    unlocked.pop();
                } else {
                    return false;
                }
            }
        }
        while (!openLocked.isEmpty() && !unlocked.isEmpty() && openLocked.peek() < unlocked.peek()) {
            openLocked.pop();
            unlocked.pop();
        }
        return openLocked.isEmpty();""",
        "visible": [
            {"s": "))()))", "locked": "010100"},
            {"s": "()()", "locked": "0000"},
            {"s": ")", "locked": "0"},
        ],
        "hidden": [
            {"s": "()", "locked": "11"},
            {"s": ")(", "locked": "11"},
            {"s": ")(", "locked": "00"},
            {"s": ")(", "locked": "10"},
            {"s": "((", "locked": "01"},
            {"s": "(((())", "locked": "111100"},
            {"s": "())(()(()(())()())(())((())(()())((())))))(((((((())(()))))(", "locked": "100011110110011011010111100111011101111110000101001101001111"},
            {"s": "))))", "locked": "0011"},
            {"s": ")(" * 1000, "locked": "0" * 2000},
        ],
    },

    # ------------------------------------------------------------------
    # 29 - Minimum Insertions to Balance Parentheses
    # ------------------------------------------------------------------
    {
        "slug": "29-minimum-insertions-to-balance-parentheses",
        "title": "Minimum Insertions to Balance Parentheses",
        "difficulty": "Medium",
        "subtopic": "Valid Parentheses",
        "companies": ["Meta", "Google", "Amazon"],
        "desc": (
            "Given a parentheses string `s` containing only `'('` and `')'`, a string is considered *balanced* under the double-close rule if:\n"
            "- Every `'('` has a corresponding two consecutive `'))'` appearing after it.\n"
            "- Every pair of consecutive `'))'` matches a `'('` appearing before it.\n\n"
            "For example, `\"())\"`, `\"())(())))\"`, and `\"(())())))\"` are balanced, whereas `\")()\"`, `\"(()))\"`, and `\"(())))\"` are not.\n\n"
            "You may insert `'('` or `')'` at any position of `s`. Return the minimum number of insertions needed to make `s` balanced."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists only of '(' and ')'."
        ],
        "hints": [
            "Track the count of unmatched '(' characters on an implicit stack while scanning left to right.",
            "When encountering ')', consume a second consecutive ')' if present (otherwise insert one ')'), and match that pair with an open '(' (or insert one '(' if none are open); at the end, each remaining '(' needs two ')' insertions."
        ],
        "explanations": [
            "The second '(' has only one matching ')', so inserting one ')' makes \"(())))\" balanced.",
            "\"())\" already satisfies the rule with 0 insertions.",
            "Insert '(' before the leading '))' and two ')' after the trailing '(' for 3 insertions total."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "minInsertions",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        insertions = 0
        opens = 0
        i = 0
        n = len(s)
        while i < n:
            if s[i] == '(':
                opens += 1
                i += 1
            else:
                if i + 1 < n and s[i + 1] == ')':
                    i += 2
                else:
                    insertions += 1
                    i += 1
                if opens > 0:
                    opens -= 1
                else:
                    insertions += 1
        return insertions + 2 * opens""",
        "java": """        int insertions = 0;
        int opens = 0;
        int n = s.length();
        for (int i = 0; i < n; ) {
            if (s.charAt(i) == '(') {
                opens++;
                i++;
            } else {
                if (i + 1 < n && s.charAt(i + 1) == ')') {
                    i += 2;
                } else {
                    insertions++;
                    i++;
                }
                if (opens > 0) {
                    opens--;
                } else {
                    insertions++;
                }
            }
        }
        return insertions + 2 * opens;""",
        "visible": [
            {"s": "(()))"},
            {"s": "())"},
            {"s": "))())("},
        ],
        "hidden": [
            {"s": "("},
            {"s": ")"},
            {"s": "))"},
            {"s": "(((((("},
            {"s": ")))))))"},
            {"s": "(()))(()))()())))"},
            {"s": "())(())))"},
            {"s": "()()()()"},
            {"s": "(()))" * 500 + "(" * 100},
        ],
    },

    # ------------------------------------------------------------------
    # 30 - XML Tag Validator
    # ------------------------------------------------------------------
    {
        "slug": "30-xml-tag-validator",
        "title": "XML Tag Validator",
        "difficulty": "Hard",
        "subtopic": "Valid Parentheses",
        "companies": ["Microsoft", "Google", "Amazon", "Salesforce"],
        "desc": (
            "Given a string `code` representing an XML-like snippet, return `true` if `code` is valid according to all of the following rules, and `false` otherwise:\n"
            "1. The entire `code` must be wrapped in a single valid closed tag (`<TAG_NAME>...</TAG_NAME>`), with no characters outside that outermost tag.\n"
            "2. A valid `TAG_NAME` consists strictly of uppercase English letters `'A'-'Z'` and has length between `1` and `9` inclusive.\n"
            "3. Every start tag `<TAG_NAME>` must be closed by a matching end tag `</TAG_NAME>` in proper LIFO nesting order.\n"
            "4. Inside tags, a CDATA section has the form `<![CDATA[CDATA_CONTENT]]>`, where `CDATA_CONTENT` may contain any characters (including `<`, `>`, or unmatched tags) and terminates at the first occurrence of `]]>`. CDATA sections cannot appear outside the outer tag.\n"
            "5. Any `'<'` outside a CDATA section must begin a valid start tag, a valid end tag, or a valid CDATA section."
        ),
        "cons": [
            "1 <= code.length <= 2000",
            "code consists of printable ASCII characters."
        ],
        "hints": [
            "Scan left to right with a stack of open tag names, handling '<![CDATA[', '</', and '<' in that priority order.",
            "Ensure that the stack never becomes empty before reaching the very end of code (otherwise there are multiple root tags or trailing text)."
        ],
        "explanations": [
            "The snippet is wrapped in a single <DIV> tag and contains valid text and matching tags.",
            "The unmatched '<div>]>' inside the CDATA section is ignored, and the outer <DIV> tag closes cleanly.",
            "The tags <A> and <B> are interleaved (<A><B></A></B>) rather than properly nested."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "isValidXml",
        "params": [("code", "String")],
        "ret": "boolean",
        "py": """        n = len(code)
        stack = []
        i = 0
        while i < n:
            if i > 0 and not stack:
                return False
            if code.startswith("<![CDATA[", i):
                if not stack:
                    return False
                end = code.find("]]>", i + 9)
                if end == -1:
                    return False
                i = end + 3
            elif code.startswith("</", i):
                end = code.find(">", i + 2)
                if end == -1:
                    return False
                tag = code[i + 2:end]
                if not stack or stack[-1] != tag:
                    return False
                stack.pop()
                i = end + 1
            elif code[i] == "<":
                end = code.find(">", i + 1)
                if end == -1:
                    return False
                tag = code[i + 1:end]
                if not (1 <= len(tag) <= 9) or not all('A' <= c <= 'Z' for c in tag):
                    return False
                stack.append(tag)
                i = end + 1
            else:
                if not stack:
                    return False
                i += 1
        return not stack""",
        "java": """        int n = code.length();
        Deque<String> stack = new ArrayDeque<>();
        int i = 0;
        while (i < n) {
            if (i > 0 && stack.isEmpty()) return false;
            if (code.startsWith("<![CDATA[", i)) {
                if (stack.isEmpty()) return false;
                int end = code.indexOf("]]>", i + 9);
                if (end == -1) return false;
                i = end + 3;
            } else if (code.startsWith("</", i)) {
                int end = code.indexOf('>', i + 2);
                if (end == -1) return false;
                String tag = code.substring(i + 2, end);
                if (stack.isEmpty() || !stack.peek().equals(tag)) return false;
                stack.pop();
                i = end + 1;
            } else if (code.charAt(i) == '<') {
                int end = code.indexOf('>', i + 1);
                if (end == -1) return false;
                String tag = code.substring(i + 1, end);
                if (tag.length() < 1 || tag.length() > 9) return false;
                for (int k = 0; k < tag.length(); k++) {
                    char c = tag.charAt(k);
                    if (c < 'A' || c > 'Z') return false;
                }
                stack.push(tag);
                i = end + 1;
            } else {
                if (stack.isEmpty()) return false;
                i++;
            }
        }
        return stack.isEmpty();""",
        "visible": [
            {"code": "<DIV>This is the first line <![CDATA[<div>]]></DIV>"},
            {"code": "<DIV>>>  ![cdata[]] <![CDATA[<div>]>]]>]]>>]</DIV>"},
            {"code": "<A>  <B> </A>   </B>"},
        ],
        "hidden": [
            {"code": "<A></A><B></B>"},
            {"code": "<![CDATA[abc]]>"},
            {"code": "<A><B><C>ok</C></B></A>"},
            {"code": "<ABCDEFGHIJ></ABCDEFGHIJ>"},
            {"code": "<ABCDEFGHI></ABCDEFGHI>"},
            {"code": "<aA></aA>"},
            {"code": "<></>"},
            {"code": "<DIV>unclosed <![CDATA[abc</DIV>"},
            {"code": "<ROOT>" + "<TAG>x</TAG>" * 80 + "<![CDATA[<BROKEN>]]>" + "</ROOT>"},
        ],
    },

    # ------------------------------------------------------------------
    # 31 - Evaluate Min-Max Expression
    # ------------------------------------------------------------------
    {
        "slug": "31-evaluate-min-max-expression",
        "title": "Evaluate Min-Max Expression",
        "difficulty": "Easy",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": (
            "Given a valid expression string `expr` composed of signed 32-bit integers and nested binary functions `min(a,b)` and `max(a,b)`, evaluate the expression and return its integer result.\n\n"
            "The expression follows the exact grammar (with no whitespace):\n"
            "- `expr := integer | \"min(\" expr \",\" expr \")\" | \"max(\" expr \",\" expr \")\"`\n\n"
            "Do not use any built-in expression evaluator such as `eval()`."
        ),
        "cons": [
            "1 <= expr.length <= 2 * 10^4",
            "expr is a valid min-max expression with no whitespace.",
            "Every integer literal fits in a signed 32-bit integer."
        ],
        "hints": [
            "Use two stacks: one for pending operators ('min' or 'max') and one for evaluated integer arguments.",
            "Whenever you encounter ')', pop the top two values and the top operator, apply min or max, and push the result back onto the value stack."
        ],
        "explanations": [
            "min(7, -2) evaluates to -2, and max(3, -2) evaluates to 3.",
            "max(1, 5) = 5 and max(2, 4) = 4, so min(5, 4) = 4.",
            "A standalone integer literal evaluates directly to -42."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "evaluateMinMax",
        "params": [("expr", "String")],
        "ret": "int",
        "py": """        ops = []
        vals = []
        i = 0
        n = len(expr)
        while i < n:
            ch = expr[i]
            if ch == 'm':
                ops.append('n' if expr[i + 1] == 'i' else 'x')
                i += 4
            elif ch == ',':
                i += 1
            elif ch == ')':
                b = vals.pop()
                a = vals.pop()
                op = ops.pop()
                vals.append(a if (a < b if op == 'n' else a > b) else b)
                i += 1
            else:
                sign = 1
                if ch == '-':
                    sign = -1
                    i += 1
                num = 0
                while i < n and expr[i].isdigit():
                    num = num * 10 + (ord(expr[i]) - 48)
                    i += 1
                vals.append(sign * num)
        return vals[0]""",
        "java": """        Deque<Character> ops = new ArrayDeque<>();
        Deque<Integer> vals = new ArrayDeque<>();
        int i = 0, n = expr.length();
        while (i < n) {
            char ch = expr.charAt(i);
            if (ch == 'm') {
                ops.push(expr.charAt(i + 1) == 'i' ? 'n' : 'x');
                i += 4;
            } else if (ch == ',') {
                i++;
            } else if (ch == ')') {
                int b = vals.pop();
                int a = vals.pop();
                char op = ops.pop();
                vals.push(op == 'n' ? Math.min(a, b) : Math.max(a, b));
                i++;
            } else {
                int sign = 1;
                if (ch == '-') {
                    sign = -1;
                    i++;
                }
                int num = 0;
                while (i < n && expr.charAt(i) >= '0' && expr.charAt(i) <= '9') {
                    num = num * 10 + (expr.charAt(i) - '0');
                    i++;
                }
                vals.push(sign * num);
            }
        }
        return vals.pop();""",
        "visible": [
            {"expr": "max(3,min(7,-2))"},
            {"expr": "min(max(1,5),max(2,4))"},
            {"expr": "-42"},
        ],
        "hidden": [
            {"expr": "0"},
            {"expr": "min(5,5)"},
            {"expr": "max(-100,-50)"},
            {"expr": "min(10,min(20,min(30,5)))"},
            {"expr": "max(min(1,2),min(3,max(4,0)))"},
            {"expr": "min(max(-10,min(0,5)),max(min(8,3),-1))"},
            {"expr": "max(1000000000,-1000000000)"},
            {"expr": "min(max(10,20),min(max(15,25),max(18,12)))"},
            {"expr": _make_perf_min_max_expr()},
        ],
    },

    # ------------------------------------------------------------------
    # 32 - Infix to Postfix Conversion
    # ------------------------------------------------------------------
    {
        "slug": "32-infix-to-postfix-conversion",
        "title": "Infix to Postfix Conversion",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Microsoft", "Amazon", "Oracle"],
        "desc": (
            "Given an array of strings `tokens` representing a valid mathematical expression in standard infix notation, convert it to Reverse Polish Notation (postfix notation) using Dijkstra's Shunting-Yard algorithm and return the resulting list of tokens.\n\n"
            "Each token is one of:\n"
            "- An operand (alphanumeric identifier or integer literal).\n"
            "- A binary operator in `{\"+\", \"-\", \"*\", \"/\", \"^\"}`.\n"
            "- A parenthesis `\"(\"` or `\")\"`.\n\n"
            "Operator precedence and associativity:\n"
            "- `\"^\"` has highest precedence (`3`) and is **right-associative** (e.g., `a ^ b ^ c` groups as `a ^ (b ^ c)`).\n"
            "- `\"*\"` and `\"/\"` have precedence (`2`) and are **left-associative**.\n"
            "- `\"+\"` and `\"-\"` have lowest precedence (`1`) and are **left-associative**."
        ),
        "cons": [
            "1 <= tokens.length <= 10^4",
            "tokens represents a valid infix expression with balanced parentheses.",
            "Every operand consists of alphanumeric characters."
        ],
        "hints": [
            "Append operands directly to the output list, and use an operator stack to defer operators until higher-precedence subexpressions finish.",
            "When pushing operator op, pop operators from the stack to output while the stack top is an operator with strictly higher precedence, or equal precedence when op is left-associative (i.e., op != '^')."
        ],
        "explanations": [
            "Multiplication binds tighter than addition, yielding [\"a\", \"b\", \"c\", \"*\", \"+\"].",
            "Parentheses force a + b to evaluate before multiplying by c, yielding [\"a\", \"b\", \"+\", \"c\", \"*\"].",
            "Exponentiation is right-associative, so a ^ b ^ c evaluates b ^ c first: [\"a\", \"b\", \"c\", \"^\", \"^\"]."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "infixToPostfix",
        "params": [("tokens", "String[]")],
        "ret": "List<String>",
        "py": """        prec = {"+": 1, "-": 1, "*": 2, "/": 2, "^": 3}
        out = []
        ops = []
        for tok in tokens:
            if tok == "(":
                ops.append(tok)
            elif tok == ")":
                while ops and ops[-1] != "(":
                    out.append(ops.pop())
                ops.pop()
            elif tok in prec:
                p = prec[tok]
                while ops and ops[-1] in prec:
                    tp = prec[ops[-1]]
                    if tp > p or (tp == p and tok != "^"):
                        out.append(ops.pop())
                    else:
                        break
                ops.append(tok)
            else:
                out.append(tok)
        while ops:
            out.append(ops.pop())
        return out""",
        "java": """        List<String> out = new ArrayList<>();
        Deque<String> ops = new ArrayDeque<>();
        for (String tok : tokens) {
            if (tok.equals("(")) {
                ops.push(tok);
            } else if (tok.equals(")")) {
                while (!ops.isEmpty() && !ops.peek().equals("(")) {
                    out.add(ops.pop());
                }
                ops.pop();
            } else if (tok.equals("+") || tok.equals("-") || tok.equals("*") || tok.equals("/") || tok.equals("^")) {
                int p = tok.equals("^") ? 3 : (tok.equals("*") || tok.equals("/") ? 2 : 1);
                while (!ops.isEmpty() && !ops.peek().equals("(")) {
                    String top = ops.peek();
                    int tp = top.equals("^") ? 3 : (top.equals("*") || top.equals("/") ? 2 : 1);
                    if (tp > p || (tp == p && !tok.equals("^"))) {
                        out.add(ops.pop());
                    } else {
                        break;
                    }
                }
                ops.push(tok);
            } else {
                out.add(tok);
            }
        }
        while (!ops.isEmpty()) {
            out.add(ops.pop());
        }
        return out;""",
        "visible": [
            {"tokens": ["a", "+", "b", "*", "c"]},
            {"tokens": ["(", "a", "+", "b", ")", "*", "c"]},
            {"tokens": ["a", "^", "b", "^", "c"]},
        ],
        "hidden": [
            {"tokens": ["42"]},
            {"tokens": ["(", "(", "x", ")", ")"]},
            {"tokens": ["a", "-", "b", "-", "c"]},
            {"tokens": ["a", "/", "b", "*", "c"]},
            {"tokens": ["(", "a", "^", "b", ")", "^", "c"]},
            {"tokens": ["3", "+", "4", "*", "2", "/", "(", "1", "-", "5", ")", "^", "2", "^", "3"]},
            {"tokens": ["a", "+", "b", "*", "(", "c", "^", "d", "-", "e", ")", "^", "(", "f", "+", "g", "*", "h", ")", "-", "i"]},
            {"tokens": ["(", "x1", "+", "x2", ")", "*", "(", "y1", "-", "y2", ")"]},
            {"tokens": _make_perf_infix()},
        ],
    },

    # ------------------------------------------------------------------
    # 33 - Ternary Expression Parser
    # ------------------------------------------------------------------
    {
        "slug": "33-ternary-expression-parser",
        "title": "Ternary Expression Parser",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Meta", "Amazon", "Adobe"],
        "desc": (
            "Given a string `expression` representing a valid nested ternary expression, evaluate it and return the result as a single-character string.\n\n"
            "Every condition is either `'T'` (true) or `'F'` (false), every leaf value is either a single digit `'0'-'9'` or `'T'`/`'F'`, and ternary operators are **right-associative** (grouped from right to left). "
            "Each expression has the form `cond?trueExpr:falseExpr`."
        ),
        "cons": [
            "1 <= expression.length <= 10^4",
            "expression consists only of digits '0'-'9', 'T', 'F', '?', and ':'.",
            "expression is guaranteed to be a valid ternary expression."
        ],
        "hints": [
            "Because ternary expressions are right-associative, scanning from right to left ensures inner branches are evaluated before outer conditions.",
            "Maintain a stack: skip ':', push values and '?', and whenever the stack top is '?' upon reading a condition 'T' or 'F', pop '?', pop trueVal and falseVal, and push the selected branch."
        ],
        "explanations": [
            "Condition 'T' selects the true branch \"2\".",
            "Condition 'F' skips \"1\" and evaluates the right branch \"T?4:5\", yielding \"4\".",
            "Innermost \"T?F:5\" evaluates to \"F\", then outer \"T?F:3\" selects \"F\"."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "parseTernary",
        "params": [("expression", "String")],
        "ret": "String",
        "py": """        stack = []
        for i in range(len(expression) - 1, -1, -1):
            ch = expression[i]
            if stack and stack[-1] == '?':
                stack.pop()
                t_val = stack.pop()
                f_val = stack.pop()
                stack.append(t_val if ch == 'T' else f_val)
            elif ch != ':':
                stack.append(ch)
        return stack[-1]""",
        "java": """        Deque<Character> stack = new ArrayDeque<>();
        for (int i = expression.length() - 1; i >= 0; i--) {
            char ch = expression.charAt(i);
            if (!stack.isEmpty() && stack.peek() == '?') {
                stack.pop();
                char tVal = stack.pop();
                char fVal = stack.pop();
                stack.push(ch == 'T' ? tVal : fVal);
            } else if (ch != ':') {
                stack.push(ch);
            }
        }
        return String.valueOf(stack.peek());""",
        "visible": [
            {"expression": "T?2:3"},
            {"expression": "F?1:T?4:5"},
            {"expression": "T?T?F:5:3"},
        ],
        "hidden": [
            {"expression": "7"},
            {"expression": "F"},
            {"expression": "F?T:F"},
            {"expression": "T?T?T?1:2:3:4"},
            {"expression": "F?T?1:2:F?3:4"},
            {"expression": "T?F?1:2:T?3:4"},
            {"expression": "T?T:F?T?1:2:F?3:4"},
            {"expression": "F?0:F?1:F?2:T?9:8"},
            {"expression": _make_perf_ternary()},
        ],
    },

    # ------------------------------------------------------------------
    # 34 - Verify Preorder Serialization
    # ------------------------------------------------------------------
    {
        "slug": "34-verify-preorder-serialization",
        "title": "Verify Preorder Serialization",
        "difficulty": "Medium",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Amazon", "Meta", "Microsoft"],
        "desc": (
            "One way to serialize a binary tree is to use preorder traversal: record each non-null node's integer value, and record `'#'` for every null sentinel child.\n\n"
            "Given a string `preorder` of comma-separated values, return `true` if it is a valid preorder traversal serialization of a binary tree, and `false` otherwise, without reconstructing the tree."
        ),
        "cons": [
            "1 <= preorder.length <= 2 * 10^4",
            "preorder consists of comma-separated non-negative integers and '#' characters.",
            "Input is guaranteed to be well-formatted with no leading, trailing, or consecutive commas."
        ],
        "hints": [
            "Using a stack, push each token; whenever the top three tokens are [non-'#', '#', '#'], that leaf subtree is complete and can be collapsed into a single '#'.",
            "Repeat the collapse after every push; the serialization is valid if and only if the final stack is exactly ['#']."
        ],
        "explanations": [
            "Every non-null node has exactly two subtrees that collapse cleanly to a single '#'.",
            "Node 1 only has one child sentinel '#', leaving its right child missing.",
            "After collapsing \"9,#,#\" into \"#\", an extra dangling \"1\" remains, which is invalid."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "isValidSerialization",
        "params": [("preorder", "String")],
        "ret": "boolean",
        "py": """        stack = []
        for tok in preorder.split(","):
            stack.append(tok)
            while len(stack) >= 3 and stack[-1] == "#" and stack[-2] == "#" and stack[-3] != "#":
                stack.pop()
                stack.pop()
                stack[-1] = "#"
        return stack == ["#"]""",
        "java": """        String[] tokens = preorder.split(",");
        List<String> stack = new ArrayList<>();
        for (String tok : tokens) {
            stack.add(tok);
            while (stack.size() >= 3
                    && stack.get(stack.size() - 1).equals("#")
                    && stack.get(stack.size() - 2).equals("#")
                    && !stack.get(stack.size() - 3).equals("#")) {
                stack.remove(stack.size() - 1);
                stack.remove(stack.size() - 1);
                stack.set(stack.size() - 1, "#");
            }
        }
        return stack.size() == 1 && stack.get(0).equals("#");""",
        "visible": [
            {"preorder": "9,3,4,#,#,1,#,#,2,#,6,#,#"},
            {"preorder": "1,#"},
            {"preorder": "9,#,#,1"},
        ],
        "hidden": [
            {"preorder": "#"},
            {"preorder": "1,#,#"},
            {"preorder": "#,#,#"},
            {"preorder": "1,2,3,#,#,#,#"},
            {"preorder": "1,#,2,#,3,#,#"},
            {"preorder": "9,3,4,#,#,1,#,#,#,2,#,6,#,#"},
            {"preorder": "7,2,#,2,#,#,#,6,#"},
            {"preorder": "10,20,#,#,30,40,#,#,50,#,#"},
            {"preorder": _make_perf_preorder()},
        ],
    },

    # ------------------------------------------------------------------
    # 35 - Parsing a Boolean Expression
    # ------------------------------------------------------------------
    {
        "slug": "35-parsing-a-boolean-expression",
        "title": "Parsing a Boolean Expression",
        "difficulty": "Hard",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Meta", "Amazon", "Microsoft"],
        "desc": (
            "A *boolean expression* is an expression that evaluates to either `true` or `false`. It takes one of the following forms:\n"
            "- `'t'` evaluates to `true`.\n"
            "- `'f'` evaluates to `false`.\n"
            "- `'!(subExpr)'` evaluates to the logical NOT of the inner expression `subExpr`.\n"
            "- `'&(subExpr1,subExpr2,...)'` evaluates to the logical AND of one or more comma-separated inner expressions.\n"
            "- `'|(subExpr1,subExpr2,...)'` evaluates to the logical OR of one or more comma-separated inner expressions.\n\n"
            "Given a valid boolean expression string `expression`, return its boolean evaluation."
        ),
        "cons": [
            "1 <= expression.length <= 2 * 10^4",
            "expression consists of '(', ')', '&', '|', '!', 't', 'f', and ','.",
            "expression is guaranteed to be a valid boolean expression."
        ],
        "hints": [
            "Ignore commas and push operators, '(', 't', and 'f' onto a stack.",
            "Whenever you encounter ')', pop boolean operands until '(', pop the operator just before '(', evaluate the subexpression, and push 't' or 'f' back onto the stack."
        ],
        "explanations": [
            "|(f) evaluates to false, and &(false) evaluates to false.",
            "|(f,f,f,t) contains at least one 't', so logical OR returns true.",
            "&(f,t) evaluates to false, and applying logical NOT yields true."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "parseBoolExpr",
        "params": [("expression", "String")],
        "ret": "boolean",
        "py": """        stack = []
        for ch in expression:
            if ch == ',':
                continue
            if ch != ')':
                stack.append(ch)
            else:
                has_t = False
                has_f = False
                while stack[-1] != '(':
                    v = stack.pop()
                    if v == 't':
                        has_t = True
                    else:
                        has_f = True
                stack.pop()
                op = stack.pop()
                if op == '!':
                    res = 't' if has_f else 'f'
                elif op == '&':
                    res = 'f' if has_f else 't'
                else:
                    res = 't' if has_t else 'f'
                stack.append(res)
        return stack[-1] == 't'""",
        "java": """        Deque<Character> stack = new ArrayDeque<>();
        for (int i = 0; i < expression.length(); i++) {
            char ch = expression.charAt(i);
            if (ch == ',') continue;
            if (ch != ')') {
                stack.push(ch);
            } else {
                boolean hasT = false, hasF = false;
                while (stack.peek() != '(') {
                    char v = stack.pop();
                    if (v == 't') hasT = true;
                    else hasF = true;
                }
                stack.pop();
                char op = stack.pop();
                char res;
                if (op == '!') res = hasF ? 't' : 'f';
                else if (op == '&') res = hasF ? 'f' : 't';
                else res = hasT ? 't' : 'f';
                stack.push(res);
            }
        }
        return stack.peek() == 't';""",
        "visible": [
            {"expression": "&(|(f))"},
            {"expression": "|(f,f,f,t)"},
            {"expression": "!(&(f,t))"},
        ],
        "hidden": [
            {"expression": "t"},
            {"expression": "f"},
            {"expression": "!(t)"},
            {"expression": "!(f)"},
            {"expression": "&(t,t,t)"},
            {"expression": "|(&(t,f,t),!(t))"},
            {"expression": "&(|(t,f),!(f),&(t,!(f)))"},
            {"expression": "!(!(!(!(t))))"},
            {"expression": _make_perf_bool_expr()},
        ],
    },

    # ------------------------------------------------------------------
    # 36 - Full Arithmetic Expression Evaluator (Basic Calculator III)
    # ------------------------------------------------------------------
    {
        "slug": "36-full-arithmetic-expression-evaluator",
        "title": "Full Arithmetic Expression Evaluator",
        "difficulty": "Hard",
        "subtopic": "Expression Parsing",
        "companies": ["Meta", "Google", "Amazon", "Microsoft", "Uber", "Bloomberg"],
        "desc": (
            "Given a string `s` representing a valid mathematical expression, evaluate it and return its integer result.\n\n"
            "The expression string contains non-negative integers, binary operators `'+'`, `'-'`, `'*'`, `'/'`, parentheses `'('` and `')'`, and spaces `' '`:\n"
            "- Multiplication `'*'` and division `'/'` have higher precedence than addition `'+'` and subtraction `'-'`, and operators of equal precedence evaluate left-to-right.\n"
            "- Integer division truncates toward zero (e.g., `7 / 2 = 3` and `-7 / 2 = -3`).\n"
            "- Unary `'-'` may appear at the start of the expression or immediately after `'('` (e.g., `\"-(2+3)\"` or `\"(-7)/2\"`), and no two binary operators appear consecutively.\n"
            "- All intermediate and final values fit in a 32-bit signed integer. Do not use any built-in expression evaluator such as `eval()`."
        ),
        "cons": [
            "1 <= s.length <= 2 * 10^4",
            "s consists of digits, '+', '-', '*', '/', '(', ')', and ' '.",
            "s is a valid expression with no division by zero.",
            "Every intermediate value and the final answer fit in a 32-bit signed integer."
        ],
        "hints": [
            "Maintain a stack of additive terms for the current parenthesis level: '+' and '-' push signed terms, while '*' and '/' combine immediately with the top term.",
            "When seeing '(', save the current term stack and pending operator onto a frame stack; when seeing ')', sum the current frame to get the parenthesized value and restore the outer frame."
        ],
        "explanations": [
            "6 - 4 / 2 = 6 - 2 = 4.",
            "2 * (5 + 10) / 3 + (3 + 8) = 30 / 3 + 11 = 10 + 11 = 21.",
            "(2 + 18 + 5 - (6 + 2) * 5) + 3 = (25 - 40) + 3 = -12."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "evaluateExpression",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        def apply_op(terms, op, val):
            if op == '+':
                terms.append(val)
            elif op == '-':
                terms.append(-val)
            elif op == '*':
                terms[-1] *= val
            else:
                terms[-1] = int(terms[-1] / val)

        frames = []
        terms = []
        op = '+'
        num = 0
        for ch in s:
            if ch == ' ':
                continue
            if ch.isdigit():
                num = num * 10 + (ord(ch) - 48)
            elif ch == '(':
                frames.append((terms, op))
                terms = []
                op = '+'
                num = 0
            elif ch == ')':
                apply_op(terms, op, num)
                val = sum(terms)
                terms, op = frames.pop()
                num = val
            else:
                apply_op(terms, op, num)
                op = ch
                num = 0
        apply_op(terms, op, num)
        return sum(terms)""",
        "java": """        Deque<List<Integer>> frameTerms = new ArrayDeque<>();
        Deque<Character> frameOps = new ArrayDeque<>();
        List<Integer> terms = new ArrayList<>();
        char op = '+';
        int num = 0;
        for (int i = 0; i < s.length(); i++) {
            char ch = s.charAt(i);
            if (ch == ' ') continue;
            if (ch >= '0' && ch <= '9') {
                num = num * 10 + (ch - '0');
            } else if (ch == '(') {
                frameTerms.push(terms);
                frameOps.push(op);
                terms = new ArrayList<>();
                op = '+';
                num = 0;
            } else if (ch == ')') {
                if (op == '+') terms.add(num);
                else if (op == '-') terms.add(-num);
                else if (op == '*') terms.set(terms.size() - 1, terms.get(terms.size() - 1) * num);
                else terms.set(terms.size() - 1, terms.get(terms.size() - 1) / num);
                int val = 0;
                for (int t : terms) val += t;
                terms = frameTerms.pop();
                op = frameOps.pop();
                num = val;
            } else {
                if (op == '+') terms.add(num);
                else if (op == '-') terms.add(-num);
                else if (op == '*') terms.set(terms.size() - 1, terms.get(terms.size() - 1) * num);
                else terms.set(terms.size() - 1, terms.get(terms.size() - 1) / num);
                op = ch;
                num = 0;
            }
        }
        if (op == '+') terms.add(num);
        else if (op == '-') terms.add(-num);
        else if (op == '*') terms.set(terms.size() - 1, terms.get(terms.size() - 1) * num);
        else terms.set(terms.size() - 1, terms.get(terms.size() - 1) / num);
        int ans = 0;
        for (int t : terms) ans += t;
        return ans;""",
        "visible": [
            {"s": "6-4/2"},
            {"s": "2*(5+5*2)/3+(6/2+8)"},
            {"s": "(2+6*3+5-(3*14/7+2)*5)+3"},
        ],
        "hidden": [
            {"s": "42"},
            {"s": "-(2+3)*4"},
            {"s": "(-7)/2"},
            {"s": "((10-3)*2)/(1+1)"},
            {"s": "1-(2-(3-(4-5)))"},
            {"s": "100 / (2 * (3 + 2)) + 7 * (8 - 3)"},
            {"s": "0 - (5 * (6 - 10)) / 3"},
            {"s": "(((3+5)*2-4)/3)*((9-2)+1)"},
            {"s": "+".join(["(3*4-10/2)"] * 200)},
        ],
    },

    # ------------------------------------------------------------------
    # 37 - Number of Atoms
    # ------------------------------------------------------------------
    {
        "slug": "37-number-of-atoms",
        "title": "Number of Atoms",
        "difficulty": "Hard",
        "subtopic": "Expression Parsing",
        "companies": ["Google", "Amazon", "Meta", "Bloomberg"],
        "desc": (
            "Given a string `formula` representing a valid chemical formula, return the canonical count of each atom.\n\n"
            "Rules of the formula:\n"
            "- An atomic element always starts with an uppercase English letter, followed by zero or more lowercase English letters.\n"
            "- If a positive integer immediately follows an element or a closing parenthesis `')'`, it multiplies the count of that element or parenthesized group; if omitted, the multiplier is `1`.\n"
            "- Return the result as a string listing all distinct elements in **lexicographical order**, each followed by its total count if that count is strictly greater than `1` (omit the count if it equals `1`)."
        ),
        "cons": [
            "1 <= formula.length <= 1000",
            "formula consists of English letters, digits, '(', and ')'.",
            "formula is guaranteed to be a valid chemical formula, and all final atom counts fit in a 32-bit signed integer."
        ],
        "hints": [
            "Maintain a stack of frequency maps where each map represents the atom counts inside one parenthesized scope.",
            "Push an empty map on '('; on ')', parse the trailing multiplier, pop the top map, multiply all its counts, and merge them into the new top map."
        ],
        "explanations": [
            "There are 2 H atoms and 1 O atom, sorted lexicographically as \"H2O\".",
            "Mg(OH)2 contains 1 Mg, 2 O, and 2 H atoms; sorted lexicographically this gives \"H2MgO2\".",
            "K4(ON(SO3)2)2 expands to 4 K, 2 N, 14 O, and 4 S -> \"K4N2O14S4\"."
        ],
        "time": "O(n + k log k)",
        "space": "O(n)",
        "kind": "function",
        "method": "countOfAtoms",
        "params": [("formula", "String")],
        "ret": "String",
        "py": """        stack = [{}]
        i = 0
        n = len(formula)
        while i < n:
            if formula[i] == '(':
                stack.append({})
                i += 1
            elif formula[i] == ')':
                i += 1
                mult = 0
                while i < n and formula[i].isdigit():
                    mult = mult * 10 + (ord(formula[i]) - 48)
                    i += 1
                mult = mult or 1
                top = stack.pop()
                cur = stack[-1]
                for atom, cnt in top.items():
                    cur[atom] = cur.get(atom, 0) + cnt * mult
            else:
                j = i + 1
                while j < n and formula[j].islower():
                    j += 1
                atom = formula[i:j]
                i = j
                cnt = 0
                while i < n and formula[i].isdigit():
                    cnt = cnt * 10 + (ord(formula[i]) - 48)
                    i += 1
                cnt = cnt or 1
                cur = stack[-1]
                cur[atom] = cur.get(atom, 0) + cnt
        parts = []
        for atom in sorted(stack[0]):
            cnt = stack[0][atom]
            parts.append(atom if cnt == 1 else f"{atom}{cnt}")
        return "".join(parts)""",
        "java": """        Deque<Map<String, Integer>> stack = new ArrayDeque<>();
        stack.push(new HashMap<>());
        int i = 0, n = formula.length();
        while (i < n) {
            char ch = formula.charAt(i);
            if (ch == '(') {
                stack.push(new HashMap<>());
                i++;
            } else if (ch == ')') {
                i++;
                int mult = 0;
                while (i < n && Character.isDigit(formula.charAt(i))) {
                    mult = mult * 10 + (formula.charAt(i) - '0');
                    i++;
                }
                if (mult == 0) mult = 1;
                Map<String, Integer> top = stack.pop();
                Map<String, Integer> cur = stack.peek();
                for (Map.Entry<String, Integer> e : top.entrySet()) {
                    cur.put(e.getKey(), cur.getOrDefault(e.getKey(), 0) + e.getValue() * mult);
                }
            } else {
                int j = i + 1;
                while (j < n && Character.isLowerCase(formula.charAt(j))) j++;
                String atom = formula.substring(i, j);
                i = j;
                int cnt = 0;
                while (i < n && Character.isDigit(formula.charAt(i))) {
                    cnt = cnt * 10 + (formula.charAt(i) - '0');
                    i++;
                }
                if (cnt == 0) cnt = 1;
                Map<String, Integer> cur = stack.peek();
                cur.put(atom, cur.getOrDefault(atom, 0) + cnt);
            }
        }
        TreeMap<String, Integer> sorted = new TreeMap<>(stack.peek());
        StringBuilder sb = new StringBuilder();
        for (Map.Entry<String, Integer> e : sorted.entrySet()) {
            sb.append(e.getKey());
            if (e.getValue() > 1) sb.append(e.getValue());
        }
        return sb.toString();""",
        "visible": [
            {"formula": "H2O"},
            {"formula": "Mg(OH)2"},
            {"formula": "K4(ON(SO3)2)2"},
        ],
        "hidden": [
            {"formula": "He"},
            {"formula": "Be32"},
            {"formula": "(H2O)"},
            {"formula": "((H2O)2O)3"},
            {"formula": "Fe(CN)6(NH4)4"},
            {"formula": "C6H12O6"},
            {"formula": "(B2O39He17BeBe49)39"},
            {"formula": "Ca(OH)2(H2O)3(CaCl2)2"},
            {"formula": "(" + "NaCl(H2O)2" * 20 + ")3(K2SO4)5"},
        ],
    },

    # ------------------------------------------------------------------
    # 38 - Min-Max Range Stack (Design)
    # ------------------------------------------------------------------
    {
        "slug": "38-min-max-range-stack",
        "title": "Min-Max Range Stack",
        "difficulty": "Easy",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Bloomberg", "Microsoft", "Goldman Sachs"],
        "desc": (
            "Design a stack `RangeStack` that supports standard stack operations plus retrieving the value range (`max - min`) of all elements currently in the stack in constant `O(1)` time.\n\n"
            "Implement the `RangeStack` class:\n"
            "- `RangeStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes the 32-bit signed integer `val` onto the stack.\n"
            "- `void pop()` removes the top element of the stack.\n"
            "- `int top()` returns the top element of the stack.\n"
            "- `long getRange()` returns `(long) maxVal - (long) minVal` across all elements currently in the stack.\n\n"
            "Every operation must run in `O(1)` time."
        ),
        "cons": [
            "-2^31 <= val <= 2^31 - 1",
            "Methods pop, top, and getRange are always called on non-empty stacks.",
            "At most 3 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Alongside each pushed value, store the running minimum and running maximum at that stack depth.",
            "Compute max - min using 64-bit signed integers (long in Java) so extreme 32-bit bounds do not overflow."
        ],
        "explanations": [
            "After pushing 4, 1, 9, range is 9 - 1 = 8; after popping 9, stack is [4, 1] with top 1 and range 4 - 1 = 3.",
            "With a single element 7, max equals min so getRange returns 0.",
            "With -2147483648 and 2147483647, the 64-bit range is 4294967295."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "RangeStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "void"),
            ("top", [], "int"),
            ("getRange", [], "long"),
        ],
        "py_class": """class RangeStack:
    def __init__(self):
        self.st = []

    def push(self, val: int) -> None:
        if not self.st:
            self.st.append((val, val, val))
        else:
            _, mn, mx = self.st[-1]
            self.st.append((val, val if val < mn else mn, val if val > mx else mx))

    def pop(self) -> None:
        self.st.pop()

    def top(self) -> int:
        return self.st[-1][0]

    def getRange(self) -> int:
        _, mn, mx = self.st[-1]
        return mx - mn""",
        "java_class": """class RangeStack {
    private final Deque<int[]> st = new ArrayDeque<>();

    public RangeStack() {}

    public void push(int val) {
        if (st.isEmpty()) {
            st.push(new int[]{val, val, val});
        } else {
            int[] prev = st.peek();
            st.push(new int[]{val, Math.min(val, prev[1]), Math.max(val, prev[2])});
        }
    }

    public void pop() {
        st.pop();
    }

    public int top() {
        return st.peek()[0];
    }

    public long getRange() {
        int[] cur = st.peek();
        return (long) cur[2] - (long) cur[1];
    }
}""",
        "visible": [
            {
                "ops": ["RangeStack", "push", "push", "push", "getRange", "pop", "top", "getRange"],
                "args": [[], [4], [1], [9], [], [], [], []],
            },
            {
                "ops": ["RangeStack", "push", "getRange", "top"],
                "args": [[], [7], [], []],
            },
            {
                "ops": ["RangeStack", "push", "push", "getRange", "pop", "getRange"],
                "args": [[], [-2147483648], [2147483647], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["RangeStack", "push", "push", "push", "getRange", "pop", "getRange"],
                "args": [[], [5], [5], [5], [], [], []],
            },
            {
                "ops": ["RangeStack", "push", "push", "push", "getRange", "pop", "getRange", "pop", "getRange"],
                "args": [[], [1], [2], [3], [], [], [], [], []],
            },
            {
                "ops": ["RangeStack", "push", "push", "push", "getRange", "pop", "getRange", "pop", "getRange"],
                "args": [[], [10], [5], [-5], [], [], [], [], []],
            },
            {
                "ops": ["RangeStack", "push", "pop", "push", "push", "getRange"],
                "args": [[], [100], [], [-20], [-5], []],
            },
            {
                "ops": ["RangeStack", "push", "push", "push", "push", "pop", "getRange", "pop", "getRange"],
                "args": [[], [0], [10], [-10], [10], [], [], [], []],
            },
            {
                "ops": ["RangeStack", "push", "push", "getRange", "pop", "push", "getRange"],
                "args": [[], [2147483647], [-2147483648], [], [], [0], []],
            },
            {
                "ops": ["RangeStack", "push", "push", "push", "top", "pop", "top", "getRange"],
                "args": [[], [-100], [50], [200], [], [], [], []],
            },
            {
                "ops": ["RangeStack", "push", "push", "push", "push", "getRange", "pop", "pop", "getRange"],
                "args": [[], [-3], [-3], [12], [-3], [], [], [], []],
            },
            _make_perf_range_stack(),
        ],
    },

    # ------------------------------------------------------------------
    # 39 - Design a Stack With Increment Operation (Design)
    # ------------------------------------------------------------------
    {
        "slug": "39-design-a-stack-with-increment-operation",
        "title": "Design a Stack With Increment Operation",
        "difficulty": "Medium",
        "subtopic": "Min Stack",
        "companies": ["Google", "Amazon", "Meta", "Uber"],
        "desc": (
            "Design a bounded stack `CustomStack` that supports incrementing the bottom `k` elements in `O(1)` time.\n\n"
            "Implement the `CustomStack` class:\n"
            "- `CustomStack(int maxSize)` initializes the stack with maximum capacity `maxSize`.\n"
            "- `void push(int x)` adds `x` to the top of the stack if the stack has not reached `maxSize`; otherwise does nothing.\n"
            "- `int pop()` pops and returns the top of the stack, or `-1` if the stack is empty.\n"
            "- `void increment(int k, int val)` increments the bottom `k` elements of the stack by `val`. If there are fewer than `k` elements in the stack, increment all elements currently in the stack.\n\n"
            "Every operation (`push`, `pop`, and `increment`) must run in `O(1)` time."
        ),
        "cons": [
            "1 <= maxSize, x, k <= 1000",
            "0 <= val <= 100",
            "At most 2 * 10^4 calls will be made across push, pop, and increment."
        ],
        "hints": [
            "Maintain a parallel lazy-increment array inc[] of the same length as the stack.",
            "For increment(k, val), only add val to inc[min(k, size) - 1]; when popping index i, add inc[i] to the popped value and propagate inc[i] down to inc[i - 1]."
        ],
        "explanations": [
            "Pushing 1, 2, popping 2, pushing 2, 3, 4 (4 ignored as maxSize=3), incrementing bottom 5 by 100 and bottom 2 by 100 yields [201, 202, 103], popping 103, 202, 201, then -1.",
            "Incrementing an empty stack has no effect and popping returns -1.",
            "With maxSize=1, only the first push succeeds and receives the lazy increment before popping."
        ],
        "time": "O(1) per op",
        "space": "O(maxSize)",
        "kind": "design",
        "className": "CustomStack",
        "ctorParams": [("maxSize", "int")],
        "methods": [
            ("push", [("x", "int")], "void"),
            ("pop", [], "int"),
            ("increment", [("k", "int"), ("val", "int")], "void"),
        ],
        "py_class": """class CustomStack:
    def __init__(self, maxSize: int):
        self.max_size = maxSize
        self.stack = []
        self.inc = []

    def push(self, x: int) -> None:
        if len(self.stack) < self.max_size:
            self.stack.append(x)
            self.inc.append(0)

    def pop(self) -> int:
        if not self.stack:
            return -1
        add = self.inc.pop()
        if self.inc:
            self.inc[-1] += add
        return self.stack.pop() + add

    def increment(self, k: int, val: int) -> None:
        idx = min(k, len(self.stack)) - 1
        if idx >= 0:
            self.inc[idx] += val""",
        "java_class": """class CustomStack {
    private final int[] stack;
    private final int[] inc;
    private int top;

    public CustomStack(int maxSize) {
        this.stack = new int[maxSize];
        this.inc = new int[maxSize];
        this.top = 0;
    }

    public void push(int x) {
        if (top < stack.length) {
            stack[top] = x;
            inc[top] = 0;
            top++;
        }
    }

    public int pop() {
        if (top == 0) return -1;
        int idx = --top;
        int add = inc[idx];
        if (idx > 0) inc[idx - 1] += add;
        return stack[idx] + add;
    }

    public void increment(int k, int val) {
        int idx = Math.min(k, top) - 1;
        if (idx >= 0) inc[idx] += val;
    }
}""",
        "visible": [
            {
                "ops": ["CustomStack", "push", "push", "pop", "push", "push", "push", "increment", "increment", "pop", "pop", "pop", "pop"],
                "args": [[3], [1], [2], [], [2], [3], [4], [5, 100], [2, 100], [], [], [], []],
            },
            {
                "ops": ["CustomStack", "increment", "pop", "push", "pop"],
                "args": [[2], [3, 50], [], [7], []],
            },
            {
                "ops": ["CustomStack", "push", "push", "increment", "pop", "pop"],
                "args": [[1], [10], [20], [5, 3], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["CustomStack", "push", "push", "increment", "push", "pop", "pop", "pop"],
                "args": [[3], [1], [2], [1, 10], [3], [], [], []],
            },
            {
                "ops": ["CustomStack", "push", "push", "push", "increment", "increment", "increment", "pop", "pop", "pop"],
                "args": [[3], [5], [6], [7], [1, 1], [2, 2], [3, 3], [], [], []],
            },
            {
                "ops": ["CustomStack", "push", "increment", "pop", "push", "pop"],
                "args": [[2], [10], [1, 99], [], [20], []],
            },
            {
                "ops": ["CustomStack", "push", "push", "pop", "increment", "push", "increment", "pop", "pop"],
                "args": [[4], [1], [2], [], [2, 5], [3], [1, 7], [], []],
            },
            {
                "ops": ["CustomStack", "push", "push", "increment", "pop", "pop", "push", "pop"],
                "args": [[2], [100], [200], [2, 0], [], [], [300], []],
            },
            {
                "ops": ["CustomStack", "pop", "pop", "push", "increment", "pop"],
                "args": [[5], [], [], [42], [10, 8], []],
            },
            {
                "ops": ["CustomStack", "push", "push", "push", "increment", "pop", "push", "increment", "pop", "pop", "pop"],
                "args": [[3], [1], [2], [3], [3, 10], [], [4], [2, 20], [], [], []],
            },
            {
                "ops": ["CustomStack", "push", "push", "push", "push", "increment", "pop", "pop", "pop"],
                "args": [[2], [10], [20], [30], [40], [100, 100], [], [], []],
            },
            _make_perf_custom_stack(),
        ],
    },

    # ------------------------------------------------------------------
    # 40 - Middle Stack (Design)
    # ------------------------------------------------------------------
    {
        "slug": "40-middle-stack",
        "title": "Middle Stack",
        "difficulty": "Medium",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Microsoft", "Google", "Goldman Sachs"],
        "desc": (
            "Design a stack `MiddleStack` that supports standard stack operations plus `O(1)` access and deletion of the middle element.\n\n"
            "For a non-empty stack of size `n` indexed `0` (bottom) to `n - 1` (top), the *middle* element is defined as the element at index `(n - 1) // 2` (the lower middle when `n` is even).\n\n"
            "Implement the `MiddleStack` class:\n"
            "- `MiddleStack()` initializes an empty stack.\n"
            "- `void push(int val)` pushes non-negative integer `val` onto the top of the stack.\n"
            "- `int pop()` removes and returns the top element, or `-1` if the stack is empty.\n"
            "- `int top()` returns the top element without removing it, or `-1` if the stack is empty.\n"
            "- `int getMiddle()` returns the middle element without removing it, or `-1` if the stack is empty.\n"
            "- `int popMiddle()` removes and returns the middle element, or `-1` if the stack is empty.\n\n"
            "All operations must run in `O(1)` time."
        ),
        "cons": [
            "0 <= val <= 10^9",
            "At most 3 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Split the stack into two double-ended queues: left (bottom half) and right (top half), maintaining len(left) == len(right) or len(left) == len(right) + 1.",
            "With this invariant, the middle element is always the back of left, and the top element is the back of right (or back of left if right is empty)."
        ],
        "explanations": [
            "Stack becomes [1, 2, 3, 4]: middle is index 1 (value 2); popMiddle removes 2 leaving [1, 3, 4] with middle 3 and top 4; pop removes 4 leaving [1, 3] with middle 1.",
            "All queries on an empty MiddleStack return -1.",
            "Repeatedly popping the middle from [10, 20, 30] returns 20, then 10, then 30, then -1."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "MiddleStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "int"),
            ("top", [], "int"),
            ("getMiddle", [], "int"),
            ("popMiddle", [], "int"),
        ],
        "py_class": """class MiddleStack:
    def __init__(self):
        self.left = deque()
        self.right = deque()

    def _rebalance(self) -> None:
        while len(self.left) > len(self.right) + 1:
            self.right.appendleft(self.left.pop())
        while len(self.left) < len(self.right):
            self.left.append(self.right.popleft())

    def push(self, val: int) -> None:
        self.right.append(val)
        self._rebalance()

    def pop(self) -> int:
        if self.right:
            v = self.right.pop()
        elif self.left:
            v = self.left.pop()
        else:
            return -1
        self._rebalance()
        return v

    def top(self) -> int:
        if self.right:
            return self.right[-1]
        return self.left[-1] if self.left else -1

    def getMiddle(self) -> int:
        return self.left[-1] if self.left else -1

    def popMiddle(self) -> int:
        if not self.left:
            return -1
        v = self.left.pop()
        self._rebalance()
        return v""",
        "java_class": """class MiddleStack {
    private final Deque<Integer> left = new ArrayDeque<>();
    private final Deque<Integer> right = new ArrayDeque<>();

    public MiddleStack() {}

    private void rebalance() {
        while (left.size() > right.size() + 1) {
            right.addFirst(left.removeLast());
        }
        while (left.size() < right.size()) {
            left.addLast(right.removeFirst());
        }
    }

    public void push(int val) {
        right.addLast(val);
        rebalance();
    }

    public int pop() {
        int v;
        if (!right.isEmpty()) {
            v = right.removeLast();
        } else if (!left.isEmpty()) {
            v = left.removeLast();
        } else {
            return -1;
        }
        rebalance();
        return v;
    }

    public int top() {
        if (!right.isEmpty()) return right.peekLast();
        return left.isEmpty() ? -1 : left.peekLast();
    }

    public int getMiddle() {
        return left.isEmpty() ? -1 : left.peekLast();
    }

    public int popMiddle() {
        if (left.isEmpty()) return -1;
        int v = left.removeLast();
        rebalance();
        return v;
    }
}""",
        "visible": [
            {
                "ops": ["MiddleStack", "push", "push", "push", "push", "getMiddle", "popMiddle", "getMiddle", "top", "pop", "getMiddle"],
                "args": [[], [1], [2], [3], [4], [], [], [], [], [], []],
            },
            {
                "ops": ["MiddleStack", "top", "pop", "getMiddle", "popMiddle"],
                "args": [[], [], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "push", "push", "popMiddle", "popMiddle", "popMiddle", "popMiddle"],
                "args": [[], [10], [20], [30], [], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["MiddleStack", "push", "top", "getMiddle", "pop", "getMiddle"],
                "args": [[], [5], [], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "push", "getMiddle", "top", "popMiddle", "top", "getMiddle"],
                "args": [[], [1], [2], [], [], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "push", "push", "push", "push", "popMiddle", "popMiddle", "pop", "pop", "pop"],
                "args": [[], [10], [20], [30], [40], [50], [], [], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "popMiddle", "push", "push", "getMiddle", "pop", "pop"],
                "args": [[], [0], [], [7], [8], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "push", "push", "pop", "push", "getMiddle", "popMiddle", "top"],
                "args": [[], [100], [200], [300], [], [400], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "push", "push", "push", "pop", "pop", "pop", "pop", "top"],
                "args": [[], [9], [8], [7], [6], [], [], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "push", "popMiddle", "push", "push", "popMiddle", "getMiddle", "top"],
                "args": [[], [1], [2], [], [3], [4], [], [], []],
            },
            {
                "ops": ["MiddleStack", "push", "push", "push", "push", "push", "push", "getMiddle", "popMiddle", "getMiddle", "popMiddle"],
                "args": [[], [1], [2], [3], [4], [5], [6], [], [], [], []],
            },
            _make_perf_middle_stack(),
        ],
    },

    # ------------------------------------------------------------------
    # 41 - Max Stack (Design)
    # ------------------------------------------------------------------
    {
        "slug": "41-max-stack",
        "title": "Max Stack",
        "difficulty": "Hard",
        "subtopic": "Min Stack",
        "companies": ["LinkedIn", "Amazon", "Meta", "Google", "Microsoft", "Bloomberg"],
        "desc": (
            "Design a max stack data structure `MaxStack` that supports standard stack operations and also supports finding and removing the stack's maximum element.\n\n"
            "Implement the `MaxStack` class:\n"
            "- `MaxStack()` initializes the stack object.\n"
            "- `void push(int x)` pushes element `x` onto the stack.\n"
            "- `int pop()` removes and returns the element on top of the stack.\n"
            "- `int top()` returns the element on top of the stack without removing it.\n"
            "- `int peekMax()` retrieves the maximum element in the stack without removing it.\n"
            "- `int popMax()` retrieves the maximum element in the stack and removes it. If there is more than one maximum element, remove only the **top-most** one.\n\n"
            "Aim for `O(log n)` time per operation (`O(1)` amortized for `top`)."
        ),
        "cons": [
            "-2^31 <= x <= 2^31 - 1",
            "Methods pop, top, peekMax, and popMax are always called on non-empty stacks.",
            "At most 3 * 10^4 calls will be made across all methods."
        ],
        "hints": [
            "Assign a strictly increasing sequence ID to every pushed element so ties in value are broken by largest ID (closest to the top).",
            "Maintain both a regular stack and a max-heap storing (value, id), along with a set of lazily deleted IDs that are skipped whenever they surface at the top of either structure."
        ],
        "explanations": [
            "Stack is [5, 1, 5]: top is 5, popMax removes the top-most 5 leaving [5, 1], top is 1, peekMax is 5, pop returns 1, and top is 5.",
            "Duplicate maximums are removed from top-most to bottom-most by repeated popMax calls.",
            "Extreme 32-bit signed integers are compared without overflow."
        ],
        "time": "O(log n) amortized per op",
        "space": "O(n)",
        "kind": "design",
        "className": "MaxStack",
        "ctorParams": [],
        "methods": [
            ("push", [("x", "int")], "void"),
            ("pop", [], "int"),
            ("top", [], "int"),
            ("peekMax", [], "int"),
            ("popMax", [], "int"),
        ],
        "py_class": """class MaxStack:
    def __init__(self):
        self.stack = []
        self.heap = []
        self.removed = set()
        self.next_id = 0

    def _clean_stack(self) -> None:
        while self.stack and self.stack[-1][1] in self.removed:
            self.stack.pop()

    def _clean_heap(self) -> None:
        while self.heap and -self.heap[0][1] in self.removed:
            heapq.heappop(self.heap)

    def push(self, x: int) -> None:
        uid = self.next_id
        self.next_id += 1
        self.stack.append((x, uid))
        heapq.heappush(self.heap, (-x, -uid))

    def pop(self) -> int:
        self._clean_stack()
        val, uid = self.stack.pop()
        self.removed.add(uid)
        return val

    def top(self) -> int:
        self._clean_stack()
        return self.stack[-1][0]

    def peekMax(self) -> int:
        self._clean_heap()
        return -self.heap[0][0]

    def popMax(self) -> int:
        self._clean_heap()
        neg_val, neg_uid = heapq.heappop(self.heap)
        self.removed.add(-neg_uid)
        return -neg_val""",
        "java_class": """class MaxStack {
    private final Deque<int[]> stack = new ArrayDeque<>();
    private final PriorityQueue<int[]> heap = new PriorityQueue<>(
        (a, b) -> a[0] != b[0] ? Integer.compare(b[0], a[0]) : Integer.compare(b[1], a[1])
    );
    private final Set<Integer> removed = new HashSet<>();
    private int nextId = 0;

    public MaxStack() {}

    private void cleanStack() {
        while (!stack.isEmpty() && removed.contains(stack.peek()[1])) {
            stack.pop();
        }
    }

    private void cleanHeap() {
        while (!heap.isEmpty() && removed.contains(heap.peek()[1])) {
            heap.poll();
        }
    }

    public void push(int x) {
        int id = nextId++;
        int[] item = new int[]{x, id};
        stack.push(item);
        heap.offer(item);
    }

    public int pop() {
        cleanStack();
        int[] item = stack.pop();
        removed.add(item[1]);
        return item[0];
    }

    public int top() {
        cleanStack();
        return stack.peek()[0];
    }

    public int peekMax() {
        cleanHeap();
        return heap.peek()[0];
    }

    public int popMax() {
        cleanHeap();
        int[] item = heap.poll();
        removed.add(item[1]);
        return item[0];
    }
}""",
        "visible": [
            {
                "ops": ["MaxStack", "push", "push", "push", "top", "popMax", "top", "peekMax", "pop", "top"],
                "args": [[], [5], [1], [5], [], [], [], [], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "push", "popMax", "popMax", "top"],
                "args": [[], [7], [7], [3], [], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "peekMax", "popMax", "top"],
                "args": [[], [-2147483648], [2147483647], [], [], []],
            },
        ],
        "hidden": [
            {
                "ops": ["MaxStack", "push", "peekMax", "popMax"],
                "args": [[], [42], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "push", "popMax", "top", "pop", "peekMax"],
                "args": [[], [1], [5], [2], [], [], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "push", "push", "popMax", "pop", "popMax", "pop"],
                "args": [[], [-5], [-2], [-10], [-2], [], [], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "pop", "push", "peekMax", "popMax"],
                "args": [[], [10], [20], [], [15], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "push", "popMax", "push", "peekMax", "pop", "top"],
                "args": [[], [9], [2], [9], [], [3], [], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "push", "push", "popMax", "popMax", "popMax", "top"],
                "args": [[], [1], [2], [3], [4], [], [], [], []],
            },
            {
                "ops": ["MaxStack", "push", "push", "push", "push", "popMax", "popMax", "popMax", "top"],
                "args": [[], [4], [3], [2], [1], [], [], [], []],
            },
            {
                "ops": ["MaxStack", "push", "pop", "push", "push", "popMax", "pop"],
                "args": [[], [100], [], [50], [50], [], []],
            },
            _make_perf_max_stack(),
        ],
    },

    # ------------------------------------------------------------------
    # 42 - Maximum Frequency Stack (Design)
    # ------------------------------------------------------------------
    {
        "slug": "42-maximum-frequency-stack",
        "title": "Maximum Frequency Stack",
        "difficulty": "Hard",
        "subtopic": "Min Stack",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg", "Apple"],
        "desc": (
            "Design a stack-like data structure `FreqStack` that pushes elements to the stack and pops the most frequent element from the stack.\n\n"
            "Implement the `FreqStack` class:\n"
            "- `FreqStack()` constructs an empty frequency stack.\n"
            "- `void push(int val)` pushes an integer `val` onto the top of the stack.\n"
            "- `int pop()` removes and returns the most frequent element in the stack. If there is a tie for the most frequent element, the element closest to the stack's top is removed and returned.\n\n"
            "Both `push` and `pop` must run in `O(1)` time."
        ),
        "cons": [
            "0 <= val <= 10^9",
            "At most 2 * 10^4 calls will be made to push and pop.",
            "It is guaranteed that there will be at least one element in the stack before calling pop."
        ],
        "hints": [
            "Maintain a frequency map freq[val] and a map of stacks group[f] storing all values pushed at frequency level f in push order.",
            "Track maxFreq: pop always removes the top of group[maxFreq], decrements freq[val], and decrements maxFreq whenever group[maxFreq] becomes empty."
        ],
        "explanations": [
            "After pushing [5,7,5,7,4,5], 5 has freq 3 so pop returns 5; then 5 and 7 tie at freq 2 with 7 closer to top so pop returns 7; next 5 (freq 2), then 4 (closest to top among freq 1).",
            "When all values are distinct, FreqStack behaves identically to a standard LIFO stack.",
            "After popping down to empty and pushing again, frequencies reset cleanly."
        ],
        "time": "O(1) per op",
        "space": "O(n)",
        "kind": "design",
        "className": "FreqStack",
        "ctorParams": [],
        "methods": [
            ("push", [("val", "int")], "void"),
            ("pop", [], "int"),
        ],
        "py_class": """class FreqStack:
    def __init__(self):
        self.freq = {}
        self.group = {}
        self.max_freq = 0

    def push(self, val: int) -> None:
        f = self.freq.get(val, 0) + 1
        self.freq[val] = f
        if f > self.max_freq:
            self.max_freq = f
        if f not in self.group:
            self.group[f] = []
        self.group[f].append(val)

    def pop(self) -> int:
        val = self.group[self.max_freq].pop()
        self.freq[val] -= 1
        if not self.group[self.max_freq]:
            self.max_freq -= 1
        return val""",
        "java_class": """class FreqStack {
    private final Map<Integer, Integer> freq = new HashMap<>();
    private final Map<Integer, Deque<Integer>> group = new HashMap<>();
    private int maxFreq = 0;

    public FreqStack() {}

    public void push(int val) {
        int f = freq.getOrDefault(val, 0) + 1;
        freq.put(val, f);
        if (f > maxFreq) maxFreq = f;
        group.computeIfAbsent(f, k -> new ArrayDeque<>()).push(val);
    }

    public int pop() {
        Deque<Integer> st = group.get(maxFreq);
        int val = st.pop();
        freq.put(val, freq.get(val) - 1);
        if (st.isEmpty()) maxFreq--;
        return val;
    }
}""",
        "visible": [
            {
                "ops": ["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop"],
                "args": [[], [5], [7], [5], [7], [4], [5], [], [], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "pop", "pop", "pop"],
                "args": [[], [1], [2], [3], [], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "pop", "pop", "push", "push", "pop"],
                "args": [[], [9], [9], [], [], [4], [9], []],
            },
        ],
        "hidden": [
            {
                "ops": ["FreqStack", "push", "pop"],
                "args": [[], [0], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "pop", "pop", "pop"],
                "args": [[], [8], [8], [8], [], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "push", "pop", "push", "pop", "pop", "pop", "pop"],
                "args": [[], [1], [2], [1], [2], [], [2], [], [], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop", "pop"],
                "args": [[], [4], [0], [9], [3], [4], [], [], [], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "push", "pop", "push", "pop", "push", "pop", "pop"],
                "args": [[], [10], [20], [10], [30], [], [30], [], [20], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "push", "push", "push", "pop", "pop", "pop", "pop", "pop", "pop"],
                "args": [[], [1], [1], [2], [2], [3], [3], [], [], [], [], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "pop", "push", "pop", "pop", "pop"],
                "args": [[], [1000000000], [5], [1000000000], [], [5], [], [], []],
            },
            {
                "ops": ["FreqStack", "push", "push", "push", "push", "push", "pop", "push", "pop", "pop"],
                "args": [[], [2], [3], [2], [4], [3], [], [4], [], []],
            },
            _make_perf_freq_stack(),
        ],
    },
]


def main():
    assert len(TASKS) == 30, f"Expected 30 tasks, got {len(TASKS)}"
    expected_prefixes = list(range(13, 43))
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
            java_src = (
                f"class Solution {{\n"
                f"    public {p['ret']} {p['method']}({jparams}) {{\n"
                + p["java"]
                + "\n    }\n}\n"
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

    print(f"Generated {len(TASKS)} stack problems (13-42) in {BASE}")


if __name__ == "__main__":
    main()
