#!/usr/bin/env python3
"""Generate linked-lists problems 77-100 (batch 3) for AlgoPlay."""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "linked-lists"
ALLOWED_SUBTOPICS = {
    "Pointers & Nodes",
    "Fast/Slow Pointer",
    "Reversal",
    "Merge & Sort",
    "LRU Design",
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
        "long": "int",
        "double": "float",
        "boolean": "bool",
        "char": "str",
        "String": "str",
        "ListNode": "Optional[ListNode]",
        "TreeNode": "Optional[TreeNode]",
    }[t]


def make_rng_list(seed: int, n: int, lo: int, hi: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(lo, hi) for _ in range(n)]


def make_distinct_list(seed: int, n: int, lo: int, hi: int) -> list[int]:
    rng = random.Random(seed)
    return rng.sample(range(lo, hi + 1), n)


def make_unique_sorted_list(seed: int, n: int, step_max: int = 5, start: int = 1) -> list[int]:
    rng = random.Random(seed)
    out = []
    cur = start
    for _ in range(n):
        cur += rng.randint(1, step_max)
        out.append(cur)
    return out


def make_digits_list(seed: int, n: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(n - 1)]


def make_zero_segmented_list(seed: int, segments: int, max_seg: int = 6) -> list[int]:
    rng = random.Random(seed)
    out = []
    for i in range(segments):
        if i > 0:
            out.append(0)
            if rng.random() < 0.2:
                out.append(0)
        glen = rng.randint(1, max_seg)
        for _ in range(glen):
            v = rng.randint(-500, 500)
            if v == 0:
                v = 1
            out.append(v)
    return out


def make_disjoint_intervals(seed: int, n: int, count: int) -> list[list[int]]:
    rng = random.Random(seed)
    pts = sorted(rng.sample(range(1, n + 1), min(n, 2 * count)))
    intervals = []
    for i in range(0, len(pts) - 1, 2):
        intervals.append([pts[i], pts[i + 1]])
    rng.shuffle(intervals)
    return intervals


def make_tree_with_path(seed: int, size: int, path: list[int], embed: bool) -> list[int | None]:
    rng = random.Random(seed)
    vals: list[int | None] = [rng.randint(1, 50) for _ in range(size)]
    if embed and path:
        # Embed path along a downward root-to-descendant chain starting near node idx
        idx = 1 if size > (1 << min(len(path), 8)) else 0
        for v in path:
            if idx < size:
                vals[idx] = v
                idx = 2 * idx + (1 if rng.random() < 0.5 else 2)
            else:
                break
    return vals


def make_almost_pal(seed: int, half: int, valid: bool, odd: bool) -> list[int]:
    rng = random.Random(seed)
    left = [rng.randint(1, 50) for _ in range(half)]
    mid = [rng.randint(1, 50)] if odd else []
    arr = left + mid + list(reversed(left))
    if valid:
        pos = rng.randint(0, len(arr))
        arr.insert(pos, 999)
    else:
        # Corrupt two far-apart positions so no single deletion can fix it
        arr[0] = 777
        arr[-1] = 888
        arr[1] = 666
        arr[-2] = 555
    return arr


TASKS: list[dict] = [
    # =========================================================================
    # 77-80: Pointers & Nodes
    # =========================================================================
    {
        "slug": "77-remove-duplicates-from-unsorted-linked-list",
        "title": "Remove Duplicates from Unsorted Linked List",
        "difficulty": "Easy",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Adobe"],
        "desc": (
            "Given the `head` of an unsorted singly linked list, remove duplicate nodes so that only the "
            "**first occurrence** of each distinct value remains in the list, preserving the original relative order "
            "of the kept nodes.\n\n"
            "Return the head of the modified linked list."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Maintain a hash set of values already seen while traversing the list with `prev` and `curr` pointers.",
            "Whenever `curr.val` is already in the set, unlink `curr` via `prev.next = curr.next`; otherwise add `curr.val` to the set and advance `prev = curr`.",
        ],
        "explanations": [
            "Keeping the first occurrence of each value in [3, 1, 2, 1, 3, 4] yields [3, 1, 2, 4].",
            "Every node has value 5, so only the first node [5] is kept.",
            "All values in [4, -1, 7, 0] are already distinct, so the list is unchanged.",
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "removeUnsortedDuplicates",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None:
            return None
        seen = {head.val}
        prev = head
        curr = head.next
        while curr is not None:
            if curr.val in seen:
                prev.next = curr.next
            else:
                seen.add(curr.val)
                prev = curr
            curr = curr.next
        return head""",
        "java": """        if (head == null) {
            return null;
        }
        Set<Integer> seen = new HashSet<>();
        seen.add(head.val);
        ListNode prev = head;
        ListNode curr = head.next;
        while (curr != null) {
            if (seen.contains(curr.val)) {
                prev.next = curr.next;
            } else {
                seen.add(curr.val);
                prev = curr;
            }
            curr = curr.next;
        }
        return head;""",
        "visible": [
            {"head": [3, 1, 2, 1, 3, 4]},
            {"head": [5, 5, 5, 5]},
            {"head": [4, -1, 7, 0]},
        ],
        "hidden": [
            {"head": []},
            {"head": [42]},
            {"head": [1, 1]},
            {"head": [1, 2, 1]},
            {"head": [-10, 0, -10, 0, 10, -10]},
            {"head": [9, 8, 7, 6, 7, 8, 9]},
            {"head": [2, 3, 2, 3, 2, 3, 4, 4, 5]},
            {"head": make_rng_list(7701, 200, -30, 30)},
            {"head": make_rng_list(7702, 2500, -400, 400)},
        ],
    },
    {
        "slug": "78-linked-list-path-in-binary-tree",
        "title": "Linked List Path in Binary Tree",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Google", "Amazon", "Meta", "Microsoft"],
        "desc": (
            "Given the `head` of a non-empty singly linked list and the `root` of a binary tree, return `true` if "
            "all elements in the linked list starting from `head` correspond to some **downward path** connected in "
            "the binary tree, and `false` otherwise.\n\n"
            "A downward path means a sequence of tree nodes starting at any node in the tree where each subsequent "
            "node is either the left child or the right child of the previous node."
        ),
        "cons": [
            "The number of nodes in the linked list is in the range [1, 100].",
            "The number of nodes in the binary tree is in the range [1, 2500].",
            "1 <= Node.val <= 100",
        ],
        "hints": [
            "Extract the linked list values into a pattern array and compute its KMP failure table (`lps`).",
            "Run a DFS over the binary tree carrying the current KMP matched prefix length `j`; on each tree node advance `j` via `lps` and return `true` as soon as `j == len(pattern)`.",
        ],
        "explanations": [
            "The downward path 4 -> 2 -> 8 exists in the right subtree of root 1.",
            "The downward path 1 -> 4 -> 2 -> 6 exists starting from the root.",
            "No downward path matches 1 -> 4 -> 2 -> 6 -> 8.",
        ],
        "time": "O(n * min(m, h))",
        "space": "O(m + h)",
        "kind": "function",
        "method": "isSubPath",
        "params": [("head", "ListNode"), ("root", "TreeNode")],
        "ret": "boolean",
        "py": """        pat = []
        curr = head
        while curr is not None:
            pat.append(curr.val)
            curr = curr.next
        m = len(pat)
        lps = [0] * m
        j = 0
        for i in range(1, m):
            while j > 0 and pat[i] != pat[j]:
                j = lps[j - 1]
            if pat[i] == pat[j]:
                j += 1
                lps[i] = j

        stack = [(root, 0)]
        while stack:
            node, matched = stack.pop()
            if node is None:
                continue
            k = matched
            while k > 0 and node.val != pat[k]:
                k = lps[k - 1]
            if node.val == pat[k]:
                k += 1
                if k == m:
                    return True
            if node.right is not None:
                stack.append((node.right, k))
            if node.left is not None:
                stack.append((node.left, k))
        return False""",
        "java": """        List<Integer> patList = new ArrayList<>();
        ListNode curr = head;
        while (curr != null) {
            patList.add(curr.val);
            curr = curr.next;
        }
        int m = patList.size();
        int[] pat = new int[m];
        for (int i = 0; i < m; i++) {
            pat[i] = patList.get(i);
        }
        int[] lps = new int[m];
        int j = 0;
        for (int i = 1; i < m; i++) {
            while (j > 0 && pat[i] != pat[j]) {
                j = lps[j - 1];
            }
            if (pat[i] == pat[j]) {
                lps[i] = ++j;
            }
        }

        Deque<TreeNode> nodeStack = new ArrayDeque<>();
        Deque<Integer> matchStack = new ArrayDeque<>();
        if (root != null) {
            nodeStack.push(root);
            matchStack.push(0);
        }
        while (!nodeStack.isEmpty()) {
            TreeNode node = nodeStack.pop();
            int k = matchStack.pop();
            while (k > 0 && node.val != pat[k]) {
                k = lps[k - 1];
            }
            if (node.val == pat[k]) {
                k++;
                if (k == m) {
                    return true;
                }
            }
            if (node.right != null) {
                nodeStack.push(node.right);
                matchStack.push(k);
            }
            if (node.left != null) {
                nodeStack.push(node.left);
                matchStack.push(k);
            }
        }
        return false;""",
        "visible": [
            {
                "head": [4, 2, 8],
                "root": [1, 4, 4, None, 2, 2, None, 1, None, 6, 8, None, None, None, None, 1, 3],
            },
            {
                "head": [1, 4, 2, 6],
                "root": [1, 4, 4, None, 2, 2, None, 1, None, 6, 8, None, None, None, None, 1, 3],
            },
            {
                "head": [1, 4, 2, 6, 8],
                "root": [1, 4, 4, None, 2, 2, None, 1, None, 6, 8, None, None, None, None, 1, 3],
            },
        ],
        "hidden": [
            {"head": [5], "root": [5]},
            {"head": [5], "root": [3]},
            {"head": [1, 1, 1, 2], "root": [1, 1, None, 1, None, 1, None, 2]},
            {"head": [2, 2, 1], "root": [2, None, 2, None, 2, None, 1]},
            {"head": [1, 2, 3], "root": [1, 2, 3]},
            {"head": [1, 2, 1, 2, 3], "root": [1, 2, 1, 1, 2, 2, 3, None, None, 1, None, None, None, None, None, 2, None, 3]},
            {"head": [4, 5, 6, 7], "root": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]},
            {"head": [7, 13, 21, 9, 4, 17, 25], "root": make_tree_with_path(7801, 255, [7, 13, 21, 9, 4, 17, 25], True)},
            {"head": [91, 92, 93, 94, 95, 96, 97, 98], "root": make_tree_with_path(7802, 1023, [91, 92, 93, 94, 95, 96, 97, 98], False)},
        ],
    },
    {
        "slug": "79-rearrange-linked-list-zigzag",
        "title": "Rearrange Linked List in Zigzag Order",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Oracle"],
        "desc": (
            "Given the `head` of a singly linked list of length `n`, rearrange its node values in a single "
            "left-to-right pass so that the list follows the zigzag wave pattern "
            "`node[0].val <= node[1].val >= node[2].val <= node[3].val >= ...`.\n\n"
            "To guarantee a unique output, apply the canonical single-pass procedure for index `i = 0, 1, ..., n - 2`: "
            "when `i` is even, if `node[i].val > node[i + 1].val`, swap `node[i].val` and `node[i + 1].val`; "
            "when `i` is odd, if `node[i].val < node[i + 1].val`, swap `node[i].val` and `node[i + 1].val`.\n\n"
            "Return the head of the rearranged linked list in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Maintain a boolean flag `expectLess` starting as `true` (meaning `curr.val <= curr.next.val` is required at even indices) and flip it at every step.",
            "Swapping `curr.val` with `curr.next.val` when the current pair violates the required inequality never breaks the inequality already established with the previous node.",
        ],
        "explanations": [
            "Scanning [4, 3, 7, 8, 6, 2, 1]: swap (4,3)->[3,4,...], at odd i=1 swap (4,7)->[3,7,4,8,6,2,1], keep (4,8) and (8,6), at even i=4 swap (6,2)->[3,7,4,8,2,6,1], and keep (6,1).",
            "For [1, 2, 3, 4], i=0 keeps (1,2), i=1 swaps (2,3)->[1,3,2,4], and i=2 keeps (2,4).",
            "A single-node list [5] trivially satisfies the zigzag condition.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "zigzagList",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        curr = head
        expect_less = True
        while curr is not None and curr.next is not None:
            if expect_less:
                if curr.val > curr.next.val:
                    curr.val, curr.next.val = curr.next.val, curr.val
            else:
                if curr.val < curr.next.val:
                    curr.val, curr.next.val = curr.next.val, curr.val
            expect_less = not expect_less
            curr = curr.next
        return head""",
        "java": """        ListNode curr = head;
        boolean expectLess = true;
        while (curr != null && curr.next != null) {
            if (expectLess) {
                if (curr.val > curr.next.val) {
                    int tmp = curr.val;
                    curr.val = curr.next.val;
                    curr.next.val = tmp;
                }
            } else {
                if (curr.val < curr.next.val) {
                    int tmp = curr.val;
                    curr.val = curr.next.val;
                    curr.next.val = tmp;
                }
            }
            expectLess = !expectLess;
            curr = curr.next;
        }
        return head;""",
        "visible": [
            {"head": [4, 3, 7, 8, 6, 2, 1]},
            {"head": [1, 2, 3, 4]},
            {"head": [5]},
        ],
        "hidden": [
            {"head": []},
            {"head": [9, 2]},
            {"head": [2, 9]},
            {"head": [11, 15, 20, 5, 10]},
            {"head": [5, 5, 5, 5, 5]},
            {"head": [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]},
            {"head": [-5, -1, -10, 0, -3, 8, -2]},
            {"head": make_rng_list(7901, 200, -1000, 1000)},
            {"head": make_rng_list(7902, 2500, -100000, 100000)},
        ],
    },
    {
        "slug": "80-circular-list-elimination-order",
        "title": "Circular List Elimination Order",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Google", "Amazon", "Bloomberg", "Uber"],
        "desc": (
            "You are given the `head` of a singly linked list of `n` nodes arranged conceptually in a clockwise circle "
            "(where the tail connects back to the head) and a positive integer `k`.\n\n"
            "Starting at the head node, repeatedly count `k` surviving nodes clockwise (inclusive of the current node), "
            "remove the `k`-th node from the circle, append it to an output linked list, and resume counting from the "
            "next surviving node clockwise until all `n` nodes have been eliminated.\n\n"
            "Return the head of the linked list containing all nodes in their exact elimination order. "
            "Aim for `O(n log n)` time."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 2000].",
            "-10^5 <= Node.val <= 10^5",
            "1 <= k <= 10^6",
        ],
        "hints": [
            "Store the `n` nodes in an array and maintain a Fenwick Tree (Binary Indexed Tree) marking each node as alive (`1`) or eliminated (`0`).",
            "Track the 0-based rank `pos` among `rem` remaining nodes: each round updates `pos = (pos + k - 1) % rem`, locates the `(pos + 1)`-th alive node in `O(log n)` via binary lifting on the Fenwick Tree, marks it `0`, and links it to the output tail.",
        ],
        "explanations": [
            "From [1, 2, 3, 4, 5] with k=2: eliminate 2, then 4, then 1, then 5, then 3.",
            "With k=1, nodes are eliminated straight in order [10, 20, 30, 40].",
            "With k=3 on [1, 2, 3]: eliminate 3, then 1 (counting 1, 2, 1), then 2.",
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "kind": "function",
        "method": "eliminationOrder",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode",
        "py": """        nodes = []
        curr = head
        while curr is not None:
            nodes.append(curr)
            curr = curr.next
        n = len(nodes)
        bit = [i & -i for i in range(n + 1)]
        max_pow = 1 << (n.bit_length() - 1)

        dummy = ListNode(0)
        tail = dummy
        pos = 0
        for rem in range(n, 0, -1):
            pos = (pos + k - 1) % rem
            target = pos + 1
            idx = 0
            step = max_pow
            while step > 0:
                nxt = idx + step
                if nxt <= n and bit[nxt] < target:
                    target -= bit[nxt]
                    idx = nxt
                step >>= 1
            chosen = idx + 1
            x = chosen
            while x <= n:
                bit[x] -= 1
                x += x & -x
            node = nodes[chosen - 1]
            tail.next = node
            tail = node
        tail.next = None
        return dummy.next""",
        "java": """        List<ListNode> nodes = new ArrayList<>();
        ListNode curr = head;
        while (curr != null) {
            nodes.add(curr);
            curr = curr.next;
        }
        int n = nodes.size();
        int[] bit = new int[n + 1];
        for (int i = 1; i <= n; i++) {
            bit[i] = i & -i;
        }
        int maxPow = Integer.highestOneBit(n);

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        int pos = 0;
        for (int rem = n; rem >= 1; rem--) {
            pos = (int) (((long) pos + k - 1) % rem);
            int target = pos + 1;
            int idx = 0;
            for (int step = maxPow; step > 0; step >>= 1) {
                int nxt = idx + step;
                if (nxt <= n && bit[nxt] < target) {
                    target -= bit[nxt];
                    idx = nxt;
                }
            }
            int chosen = idx + 1;
            for (int x = chosen; x <= n; x += x & -x) {
                bit[x]--;
            }
            ListNode node = nodes.get(chosen - 1);
            tail.next = node;
            tail = node;
        }
        tail.next = null;
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5], "k": 2},
            {"head": [10, 20, 30, 40], "k": 1},
            {"head": [1, 2, 3], "k": 3},
        ],
        "hidden": [
            {"head": [7], "k": 1},
            {"head": [7], "k": 1000000},
            {"head": [1, 2], "k": 5},
            {"head": [1, 2, 3, 4, 5, 6, 7], "k": 3},
            {"head": [-5, 0, 5, 10, 15, 20], "k": 4},
            {"head": [100, 200, 300, 400, 500], "k": 999983},
            {"head": list(range(1, 21)), "k": 7},
            {"head": make_rng_list(8001, 200, -5000, 5000), "k": 17},
            {"head": make_rng_list(8002, 1500, -100000, 100000), "k": 1000000},
        ],
    },
    # =========================================================================
    # 81-84: Fast/Slow Pointer
    # =========================================================================
    {
        "slug": "81-find-kth-node-from-middle",
        "title": "Find K-th Node from Middle",
        "difficulty": "Easy",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Microsoft", "Oracle", "Salesforce"],
        "desc": (
            "Given the `head` of a non-empty singly linked list of length `n` and a non-negative integer `k`, "
            "define the middle node to be the node at 0-based index `mid = floor(n / 2)` (so for even length `n`, "
            "this is the second of the two middle nodes).\n\n"
            "Return the value of the node located `k` positions **before** the middle node (i.e., at 0-based index "
            "`mid - k`), or `-1` if `mid - k < 0`. Solve it in a **single pass** with `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "1 <= Node.val <= 10^5",
            "0 <= k <= 10^4",
        ],
        "hints": [
            "Advance `fast` by 2 steps and `slow` by 1 step per iteration while counting the number of steps `steps` taken by `slow`.",
            "Initialize a lagging pointer `lag` at `head` once `steps == k` and advance `lag` by 1 step whenever `steps > k`; when `fast` terminates, `slow` sits at `mid` and `lag` sits at `mid - k`.",
        ],
        "explanations": [
            "For [3, 4, 7, 5, 6, 16, 15, 61, 16] (n=9), mid=4 (value 6); 3 steps before index 4 is index 1 (value 4).",
            "For [1, 14, 6, 16, 4, 10] (n=6), mid=3 (value 16); 2 steps before index 3 is index 1 (value 14).",
            "For [1, 2, 3, 4] (n=4), mid=2; 3 steps before index 2 is -1 (out of bounds), so return -1.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "kthFromMiddle",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "int",
        "py": """        fast = head
        lag = head if k == 0 else None
        steps = 0
        while fast is not None and fast.next is not None:
            fast = fast.next.next
            steps += 1
            if steps == k:
                lag = head
            elif steps > k:
                lag = lag.next
        return lag.val if lag is not None else -1""",
        "java": """        ListNode fast = head;
        ListNode lag = (k == 0) ? head : null;
        int steps = 0;
        while (fast != null && fast.next != null) {
            fast = fast.next.next;
            steps++;
            if (steps == k) {
                lag = head;
            } else if (steps > k) {
                lag = lag.next;
            }
        }
        return lag != null ? lag.val : -1;""",
        "visible": [
            {"head": [3, 4, 7, 5, 6, 16, 15, 61, 16], "k": 3},
            {"head": [1, 14, 6, 16, 4, 10], "k": 2},
            {"head": [1, 2, 3, 4], "k": 3},
        ],
        "hidden": [
            {"head": [42], "k": 0},
            {"head": [42], "k": 1},
            {"head": [10, 20], "k": 0},
            {"head": [10, 20], "k": 1},
            {"head": [10, 20], "k": 2},
            {"head": [5, 10, 15, 20, 25], "k": 2},
            {"head": [5, 10, 15, 20, 25], "k": 0},
            {"head": make_rng_list(8101, 201, 1, 100000), "k": 57},
            {"head": make_rng_list(8102, 3000, 1, 100000), "k": 1234},
        ],
    },
    {
        "slug": "82-lcg-sequence-cycle-detection",
        "title": "LCG Sequence Cycle Detection",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Google", "Bloomberg", "Goldman Sachs", "Amazon"],
        "desc": (
            "Consider a Linear Congruential Generator (LCG) defined by four integers `a`, `c`, `m`, and `seed`:\n"
            "- `x_0 = seed % m`\n"
            "- `x_{k+1} = (a * x_k + c) % m` for every `k >= 0`\n\n"
            "Because there are only `m` possible residues in `[0, m - 1]`, the sequence is guaranteed to become "
            "eventually periodic: there exist unique smallest integers `mu >= 0` (the **tail length** before the "
            "cycle starts) and `lambda >= 1` (the **cycle length**) such that `x_{mu + i} = x_{mu + i + lambda}` "
            "for all `i >= 0`.\n\n"
            "Using Floyd's Tortoise-and-Hare cycle detection in `O(1)` extra space, return the 2-element array "
            "`[mu, lambda]`."
        ),
        "cons": [
            "1 <= m <= 2 * 10^5",
            "0 <= a, c, seed <= 10^6",
        ],
        "hints": [
            "Run a slow pointer advancing 1 step per iteration and a fast pointer advancing 2 steps per iteration from `x_0 = seed % m` until they meet inside the cycle (use 64-bit arithmetic for `a * x + c`).",
            "Reset the slow pointer to `x_0` and advance both pointers 1 step at a time until they meet again: the number of steps is `mu`; then keep one pointer fixed and advance the other around the cycle until they meet to measure `lambda`.",
        ],
        "explanations": [
            "Sequence: 1 -> 2 -> 4 -> 8 -> 4 -> ... has tail length mu=2 (values 1, 2) and cycle length lambda=2 (values 4, 8).",
            "Sequence: 3 -> 3 -> ... is a fixed point immediately at index 0, so mu=0 and lambda=1.",
            "Sequence: 0 -> 1 -> 4 -> 3 -> 0 -> ... is purely periodic with mu=0 and lambda=4.",
        ],
        "time": "O(mu + lambda)",
        "space": "O(1)",
        "kind": "function",
        "method": "detectLCGCycle",
        "params": [("a", "int"), ("c", "int"), ("m", "int"), ("seed", "int")],
        "ret": "int[]",
        "py": """        def step(x: int) -> int:
            return (a * x + c) % m

        x0 = seed % m
        tortoise = step(x0)
        hare = step(step(x0))
        while tortoise != hare:
            tortoise = step(tortoise)
            hare = step(step(hare))

        mu = 0
        tortoise = x0
        while tortoise != hare:
            tortoise = step(tortoise)
            hare = step(hare)
            mu += 1

        lam = 1
        hare = step(tortoise)
        while tortoise != hare:
            hare = step(hare)
            lam += 1
        return [mu, lam]""",
        "java": """        long A = a;
        long C = c;
        long M = m;
        long x0 = ((long) seed) % M;
        long tortoise = (A * x0 + C) % M;
        long hare = (A * ((A * x0 + C) % M) + C) % M;
        while (tortoise != hare) {
            tortoise = (A * tortoise + C) % M;
            hare = (A * ((A * hare + C) % M) + C) % M;
        }
        int mu = 0;
        tortoise = x0;
        while (tortoise != hare) {
            tortoise = (A * tortoise + C) % M;
            hare = (A * hare + C) % M;
            mu++;
        }
        int lam = 1;
        hare = (A * tortoise + C) % M;
        while (tortoise != hare) {
            hare = (A * hare + C) % M;
            lam++;
        }
        return new int[]{mu, lam};""",
        "visible": [
            {"a": 2, "c": 0, "m": 12, "seed": 1},
            {"a": 1, "c": 0, "m": 5, "seed": 3},
            {"a": 3, "c": 1, "m": 5, "seed": 0},
        ],
        "hidden": [
            {"a": 0, "c": 0, "m": 1, "seed": 0},
            {"a": 0, "c": 7, "m": 10, "seed": 2},
            {"a": 2, "c": 0, "m": 64, "seed": 1},
            {"a": 5, "c": 1, "m": 16, "seed": 0},
            {"a": 6, "c": 0, "m": 100, "seed": 3},
            {"a": 123, "c": 456, "m": 997, "seed": 789},
            {"a": 1103, "c": 12345, "m": 32768, "seed": 42},
            {"a": 48271, "c": 17, "m": 65521, "seed": 123456},
            {"a": 166452, "c": 101390, "m": 199999, "seed": 999999},
        ],
    },
    {
        "slug": "83-delete-middle-k-nodes-of-linked-list",
        "title": "Delete Middle K Nodes of Linked List",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Meta", "Microsoft", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list of length `n` and an integer `k` (`0 <= k <= n`), remove the "
            "centered contiguous block of `k` nodes starting at 0-based index `L = floor((n - k) / 2)` (leaving the "
            "first `L` nodes and the last `n - k - L` nodes in their original order).\n\n"
            "Return the head of the modified linked list. Solve it in a **single pass** using `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "0 <= k <= n",
        ],
        "hints": [
            "Advance a pointer `cutEnd` by `k` steps from a sentinel `dummy` node so `n - k` nodes remain after `cutEnd`.",
            "Initialize `slow = dummy` and `fast = cutEnd`; while `fast.next` and `fast.next.next` are non-null, advance `fast` by 2 and both `slow` and `cutEnd` by 1. Finally unlink the `k` middle nodes with `slow.next = cutEnd.next`.",
        ],
        "explanations": [
            "For n=6, k=2, L=(6-2)//2=2, so indices 2 and 3 (values 3, 4) are removed, leaving [1, 2, 5, 6].",
            "For n=5, k=2, L=(5-2)//2=1, so indices 1 and 2 (values 20, 30) are removed, leaving [10, 40, 50].",
            "For n=4, k=4, all 4 nodes are removed, leaving an empty list.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "deleteMiddleK",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode",
        "py": """        if k == 0 or head is None:
            return head
        dummy = ListNode(0, head)
        cut_end = dummy
        for _ in range(k):
            cut_end = cut_end.next
        slow = dummy
        fast = cut_end
        while fast.next is not None and fast.next.next is not None:
            fast = fast.next.next
            slow = slow.next
            cut_end = cut_end.next
        slow.next = cut_end.next
        return dummy.next""",
        "java": """        if (k == 0 || head == null) {
            return head;
        }
        ListNode dummy = new ListNode(0, head);
        ListNode cutEnd = dummy;
        for (int i = 0; i < k; i++) {
            cutEnd = cutEnd.next;
        }
        ListNode slow = dummy;
        ListNode fast = cutEnd;
        while (fast.next != null && fast.next.next != null) {
            fast = fast.next.next;
            slow = slow.next;
            cutEnd = cutEnd.next;
        }
        slow.next = cutEnd.next;
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5, 6], "k": 2},
            {"head": [10, 20, 30, 40, 50], "k": 2},
            {"head": [1, 2, 3, 4], "k": 4},
        ],
        "hidden": [
            {"head": [], "k": 0},
            {"head": [7], "k": 0},
            {"head": [7], "k": 1},
            {"head": [1, 2, 3, 4, 5], "k": 0},
            {"head": [1, 2, 3, 4, 5], "k": 1},
            {"head": [1, 2, 3, 4, 5], "k": 3},
            {"head": [1, 2, 3, 4, 5, 6], "k": 1},
            {"head": make_rng_list(8301, 201, -500, 500), "k": 40},
            {"head": make_rng_list(8302, 2500, -100000, 100000), "k": 777},
        ],
    },
    {
        "slug": "84-almost-palindrome-linked-list",
        "title": "Almost Palindrome Linked List",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Meta", "Google", "Amazon", "Uber"],
        "desc": (
            "Given the `head` of a singly linked list of integers, return `true` if the list can become a palindrome "
            "after deleting **at most one** node from anywhere in the list, and `false` otherwise.\n\n"
            "Aim for `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Split the list into `left` (first `ceil(n / 2)` nodes) and `right` (last `floor(n / 2)` nodes) using fast/slow pointers, noting whether `n` is odd (`fast.next == null`), then reverse `right` in-place.",
            "Walk `p1` (in `left`) and `p2` (in reversed `right`) until the first mismatch: deleting `p1` succeeds if remaining `p1.next` matches `p2` element-for-element; deleting `p2` succeeds if remaining `p2.next` matches `p1` and, when `n` is odd, the two leftover nodes at the end of `left` are equal.",
        ],
        "explanations": [
            "[1, 2, 3, 2, 1] is already a palindrome (zero deletions needed).",
            "Deleting 9 from [9, 1, 2, 3, 2, 1] leaves the palindrome [1, 2, 3, 2, 1].",
            "No single deletion can make [1, 2, 3, 4, 5] a palindrome.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "isAlmostPalindrome",
        "params": [("head", "ListNode")],
        "ret": "boolean",
        "py": """        if head is None or head.next is None:
            return True
        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next
        is_odd = fast.next is None

        second = slow.next
        slow.next = None
        rev = None
        while second is not None:
            nxt = second.next
            second.next = rev
            rev = second
            second = nxt

        p1 = head
        p2 = rev
        while p2 is not None and p1.val == p2.val:
            p1 = p1.next
            p2 = p2.next
        if p2 is None:
            return True

        # Option 1: delete p1 from left half
        a, b = p1.next, p2
        ok1 = True
        while a is not None:
            if a.val != b.val:
                ok1 = False
                break
            a = a.next
            b = b.next
        if ok1:
            return True

        # Option 2: delete p2 from right half
        a, b = p1, p2.next
        while b is not None:
            if a.val != b.val:
                return False
            a = a.next
            b = b.next
        if is_odd:
            return a.val == a.next.val
        return True""",
        "java": """        if (head == null || head.next == null) {
            return true;
        }
        ListNode slow = head;
        ListNode fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        boolean isOdd = (fast.next == null);

        ListNode second = slow.next;
        slow.next = null;
        ListNode rev = null;
        while (second != null) {
            ListNode nxt = second.next;
            second.next = rev;
            rev = second;
            second = nxt;
        }

        ListNode p1 = head;
        ListNode p2 = rev;
        while (p2 != null && p1.val == p2.val) {
            p1 = p1.next;
            p2 = p2.next;
        }
        if (p2 == null) {
            return true;
        }

        // Option 1: delete p1 from left half
        ListNode a = p1.next;
        ListNode b = p2;
        boolean ok1 = true;
        while (a != null) {
            if (a.val != b.val) {
                ok1 = false;
                break;
            }
            a = a.next;
            b = b.next;
        }
        if (ok1) {
            return true;
        }

        // Option 2: delete p2 from right half
        a = p1;
        b = p2.next;
        while (b != null) {
            if (a.val != b.val) {
                return false;
            }
            a = a.next;
            b = b.next;
        }
        if (isOdd) {
            return a.val == a.next.val;
        }
        return true;""",
        "visible": [
            {"head": [1, 2, 3, 2, 1]},
            {"head": [9, 1, 2, 3, 2, 1]},
            {"head": [1, 2, 3, 4, 5]},
        ],
        "hidden": [
            {"head": []},
            {"head": [7]},
            {"head": [1, 2]},
            {"head": [1, 2, 3, 1]},
            {"head": [1, 2, 2, 1, 9]},
            {"head": [1, 2, 3, 1, 9]},
            {"head": [1, 2, 3, 3, 2, 9, 1]},
            {"head": make_almost_pal(8401, 200, True, True)},
            {"head": make_almost_pal(8402, 1200, False, False)},
        ],
    },
]

TASKS.extend([
    # =========================================================================
    # 85-89: Reversal
    # =========================================================================
    {
        "slug": "85-reverse-nodes-in-k-group-from-end",
        "title": "Reverse Nodes in K-Group from End",
        "difficulty": "Hard",
        "subtopic": "Reversal",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list and a positive integer `k`, group the nodes into consecutive "
            "blocks of size `k` starting from the **end (tail)** of the list.\n\n"
            "Reverse every full group of `k` nodes in-place, while leaving any leftover prefix of fewer than `k` "
            "nodes at the beginning of the list in its original order. Return the head of the modified linked list "
            "in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "1 <= k <= 10^4",
        ],
        "hints": [
            "Count the total number of nodes `n` first: the leftover prefix at the front has length `skip = n % k`, followed by `groups = n // k` full groups of size `k`.",
            "Advance a `prev` pointer past the first `skip` nodes using a sentinel `dummy`, then reverse each of the `groups` consecutive blocks of length `k` in-place.",
        ],
        "explanations": [
            "For [1, 2, 3, 4, 5] with k=2, the leftover prefix is [1], and the trailing 2-groups [2, 3] and [4, 5] reverse to [1, 3, 2, 5, 4].",
            "For [1, 2, 3, 4, 5] with k=3, prefix [1, 2] stays unchanged and trailing 3-group [3, 4, 5] reverses to [1, 2, 5, 4, 3].",
            "When k=6 exceeds n=4, the entire list is a leftover prefix and remains [1, 2, 3, 4].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseKGroupFromEnd",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode",
        "py": """        if head is None or k <= 1:
            return head
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next
        if n < k:
            return head
        skip = n % k
        groups = n // k
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(skip):
            prev = prev.next
        for _ in range(groups):
            tail = prev.next
            c = tail
            rprev = None
            for _ in range(k):
                nxt = c.next
                c.next = rprev
                rprev = c
                c = nxt
            prev.next = rprev
            tail.next = c
            prev = tail
        return dummy.next""",
        "java": """        if (head == null || k <= 1) {
            return head;
        }
        int n = 0;
        ListNode curr = head;
        while (curr != null) {
            n++;
            curr = curr.next;
        }
        if (n < k) {
            return head;
        }
        int skip = n % k;
        int groups = n / k;
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        for (int i = 0; i < skip; i++) {
            prev = prev.next;
        }
        for (int g = 0; g < groups; g++) {
            ListNode tail = prev.next;
            ListNode c = tail;
            ListNode rprev = null;
            for (int i = 0; i < k; i++) {
                ListNode nxt = c.next;
                c.next = rprev;
                rprev = c;
                c = nxt;
            }
            prev.next = rprev;
            tail.next = c;
            prev = tail;
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5], "k": 2},
            {"head": [1, 2, 3, 4, 5], "k": 3},
            {"head": [1, 2, 3, 4], "k": 6},
        ],
        "hidden": [
            {"head": [], "k": 3},
            {"head": [7], "k": 1},
            {"head": [1, 2, 3, 4, 5, 6], "k": 1},
            {"head": [1, 2, 3, 4, 5, 6], "k": 3},
            {"head": [1, 2, 3, 4, 5, 6], "k": 6},
            {"head": [10, 20, 30, 40, 50, 60, 70], "k": 4},
            {"head": [-5, -4, -3, -2, -1], "k": 2},
            {"head": make_rng_list(8501, 203, -500, 500), "k": 7},
            {"head": make_rng_list(8502, 2500, -100000, 100000), "k": 13},
        ],
    },
    {
        "slug": "86-multiply-two-linked-list-numbers",
        "title": "Multiply Two Linked List Numbers",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Microsoft", "Meta", "Oracle"],
        "desc": (
            "You are given two non-empty singly linked lists `l1` and `l2` representing two non-negative integers in "
            "**most-significant-digit-first** order. Each node contains a single decimal digit (`0` through `9`), and "
            "neither number contains leading zeros except the number `0` itself.\n\n"
            "Multiply the two integers and return their product as a singly linked list in "
            "most-significant-digit-first order (with no leading zeros except a single `0` if the product is zero). "
            "Because the numbers can have up to 200 digits, they may exceed 64-bit integer limits."
        ),
        "cons": [
            "The number of nodes in each list is in the range [1, 200].",
            "0 <= Node.val <= 9",
            "Neither input has leading zeros unless it is the single digit 0.",
        ],
        "hints": [
            "Reverse both linked lists (or extract their digits in least-significant-digit-first order) so position `i` in `l1` times position `j` in `l2` contributes directly to output digit `i + j`.",
            "Accumulate all partial products into an array of size `n + m`, propagate carries from least significant to most significant, strip leading zeros, and build the resulting linked list.",
        ],
        "explanations": [
            "123 * 45 = 5535, represented as [5, 5, 3, 5].",
            "99 * 99 = 9801, represented as [9, 8, 0, 1].",
            "0 * 5678 = 0, represented as a single node [0].",
        ],
        "time": "O(n * m)",
        "space": "O(n + m)",
        "kind": "function",
        "method": "multiplyLists",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "ListNode",
        "py": """        def to_rev_digits(node: Optional[ListNode]) -> list[int]:
            digs = []
            while node is not None:
                digs.append(node.val)
                node = node.next
            digs.reverse()
            return digs

        a = to_rev_digits(l1)
        b = to_rev_digits(l2)
        if (len(a) == 1 and a[0] == 0) or (len(b) == 1 and b[0] == 0):
            return ListNode(0)

        res = [0] * (len(a) + len(b))
        for i, da in enumerate(a):
            for j, db in enumerate(b):
                res[i + j] += da * db
        carry = 0
        for i in range(len(res)):
            total = res[i] + carry
            res[i] = total % 10
            carry = total // 10
        while len(res) > 1 and res[-1] == 0:
            res.pop()

        head = None
        for d in res:
            head = ListNode(d, head)
        return head""",
        "java": """        List<Integer> a = new ArrayList<>();
        for (ListNode c = l1; c != null; c = c.next) {
            a.add(c.val);
        }
        List<Integer> b = new ArrayList<>();
        for (ListNode c = l2; c != null; c = c.next) {
            b.add(c.val);
        }
        Collections.reverse(a);
        Collections.reverse(b);
        if ((a.size() == 1 && a.get(0) == 0) || (b.size() == 1 && b.get(0) == 0)) {
            return new ListNode(0);
        }

        int[] res = new int[a.size() + b.size()];
        for (int i = 0; i < a.size(); i++) {
            int da = a.get(i);
            for (int j = 0; j < b.size(); j++) {
                res[i + j] += da * b.get(j);
            }
        }
        int carry = 0;
        for (int i = 0; i < res.length; i++) {
            int total = res[i] + carry;
            res[i] = total % 10;
            carry = total / 10;
        }
        int top = res.length - 1;
        while (top > 0 && res[top] == 0) {
            top--;
        }
        ListNode head = null;
        for (int i = 0; i <= top; i++) {
            head = new ListNode(res[i], head);
        }
        return head;""",
        "visible": [
            {"l1": [1, 2, 3], "l2": [4, 5]},
            {"l1": [9, 9], "l2": [9, 9]},
            {"l1": [0], "l2": [5, 6, 7, 8]},
        ],
        "hidden": [
            {"l1": [0], "l2": [0]},
            {"l1": [1], "l2": [9, 8, 7, 6, 5]},
            {"l1": [9, 9, 9, 9], "l2": [9, 9, 9]},
            {"l1": [1, 0, 0, 0], "l2": [2, 0, 0]},
            {"l1": [5, 0, 5], "l2": [0]},
            {"l1": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0, 9, 8, 7, 6, 5, 4, 3, 2, 1], "l2": [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, 6, 7, 8, 9]},
            {"l1": [9] * 30, "l2": [9] * 30},
            {"l1": make_digits_list(8601, 60), "l2": make_digits_list(8602, 55)},
            {"l1": make_digits_list(8603, 180), "l2": make_digits_list(8604, 180)},
        ],
    },
    {
        "slug": "87-reverse-segments-between-zero-nodes",
        "title": "Reverse Segments Between Zero Nodes",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Google", "Adobe", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list of integers where nodes with value `0` act as fixed delimiters, "
            "reverse every maximal contiguous segment of non-zero nodes in-place while keeping every `0` node at its "
            "exact original position.\n\n"
            "Segments at the very start of the list (before the first `0`), at the very end (after the last `0`), or "
            "when there are no `0` nodes at all are also reversed. Return the head of the modified linked list in "
            "`O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Use a sentinel `dummy` node and a `prev` pointer that always points immediately before the current position.",
            "When `prev.next.val == 0`, simply advance `prev`; otherwise reverse nodes starting at `prev.next` until encountering `0` or `null`, stitch the reversed segment back between `prev` and the delimiter, and move `prev` to the segment's new tail.",
        ],
        "explanations": [
            "Segments [1, 2, 3], [4, 5], and [6] reverse to [3, 2, 1], [5, 4], and [6], giving [3, 2, 1, 0, 5, 4, 0, 6].",
            "Zeros stay fixed while [1, 2] reverses to [2, 1] and [3, 4, 5] reverses to [5, 4, 3].",
            "With no zeros, the whole list [7, 8, 9] reverses to [9, 8, 7].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseBetweenZeros",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0, head)
        prev = dummy
        while prev.next is not None:
            if prev.next.val == 0:
                prev = prev.next
            else:
                seg_tail = prev.next
                curr = seg_tail
                rprev = None
                while curr is not None and curr.val != 0:
                    nxt = curr.next
                    curr.next = rprev
                    rprev = curr
                    curr = nxt
                prev.next = rprev
                seg_tail.next = curr
                prev = seg_tail
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        while (prev.next != null) {
            if (prev.next.val == 0) {
                prev = prev.next;
            } else {
                ListNode segTail = prev.next;
                ListNode curr = segTail;
                ListNode rprev = null;
                while (curr != null && curr.val != 0) {
                    ListNode nxt = curr.next;
                    curr.next = rprev;
                    rprev = curr;
                    curr = nxt;
                }
                prev.next = rprev;
                segTail.next = curr;
                prev = segTail;
            }
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 0, 4, 5, 0, 6]},
            {"head": [0, 1, 2, 0, 0, 3, 4, 5]},
            {"head": [7, 8, 9]},
        ],
        "hidden": [
            {"head": []},
            {"head": [0]},
            {"head": [0, 0, 0]},
            {"head": [5]},
            {"head": [0, -1, -2, -3, 0]},
            {"head": [1, 0, 2, 0, 3, 0, 4]},
            {"head": [10, 20, 0, 0, 30, 40, 50, 0]},
            {"head": make_zero_segmented_list(8701, 40, 6)},
            {"head": make_zero_segmented_list(8702, 450, 7)},
        ],
    },
    {
        "slug": "88-reverse-sublist-between-min-and-max",
        "title": "Reverse Sublist Between Min and Max",
        "difficulty": "Easy",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Microsoft", "Atlassian", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list containing **distinct** integers, locate the node with the "
            "minimum value and the node with the maximum value.\n\n"
            "Reverse the contiguous sublist starting from whichever of those two nodes appears **first** in the list "
            "and ending at whichever appears **second** (inclusive of both endpoints). Return the head of the "
            "modified linked list in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "All node values in the list are distinct.",
        ],
        "hints": [
            "Run a first pass to find the 1-based positions `minPos` and `maxPos` of the minimum and maximum values, then set `left = min(minPos, maxPos)` and `right = max(minPos, maxPos)`.",
            "Run a second pass using a `dummy` node to reverse the sublist between positions `left` and `right` in-place.",
        ],
        "explanations": [
            "Minimum is 1 (pos 3) and maximum is 6 (pos 5); reversing [1, 4, 6] gives [3, 5, 6, 4, 1, 2].",
            "Maximum is 9 (pos 2) and minimum is 2 (pos 4); reversing [9, 4, 2] gives [7, 2, 4, 9, 5].",
            "Minimum is 1 (pos 1) and maximum is 4 (pos 4), so the entire list reverses to [4, 3, 2, 1].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseBetweenMinMax",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None:
            return head
        min_val = head.val
        max_val = head.val
        min_pos = 1
        max_pos = 1
        pos = 1
        curr = head
        while curr is not None:
            if curr.val < min_val:
                min_val = curr.val
                min_pos = pos
            if curr.val > max_val:
                max_val = curr.val
                max_pos = pos
            curr = curr.next
            pos += 1
        left = min(min_pos, max_pos)
        right = max(min_pos, max_pos)
        if left == right:
            return head

        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next
        tail = prev.next
        curr = tail
        rprev = None
        for _ in range(right - left + 1):
            nxt = curr.next
            curr.next = rprev
            rprev = curr
            curr = nxt
        prev.next = rprev
        tail.next = curr
        return dummy.next""",
        "java": """        if (head == null || head.next == null) {
            return head;
        }
        int minVal = head.val;
        int maxVal = head.val;
        int minPos = 1;
        int maxPos = 1;
        int pos = 1;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val < minVal) {
                minVal = curr.val;
                minPos = pos;
            }
            if (curr.val > maxVal) {
                maxVal = curr.val;
                maxPos = pos;
            }
            curr = curr.next;
            pos++;
        }
        int left = Math.min(minPos, maxPos);
        int right = Math.max(minPos, maxPos);
        if (left == right) {
            return head;
        }

        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        for (int i = 0; i < left - 1; i++) {
            prev = prev.next;
        }
        ListNode tail = prev.next;
        curr = tail;
        ListNode rprev = null;
        for (int i = 0; i < right - left + 1; i++) {
            ListNode nxt = curr.next;
            curr.next = rprev;
            rprev = curr;
            curr = nxt;
        }
        prev.next = rprev;
        tail.next = curr;
        return dummy.next;""",
        "visible": [
            {"head": [3, 5, 1, 4, 6, 2]},
            {"head": [7, 9, 4, 2, 5]},
            {"head": [1, 2, 3, 4]},
        ],
        "hidden": [
            {"head": []},
            {"head": [42]},
            {"head": [10, -5]},
            {"head": [-5, 10]},
            {"head": [5, 1, 10, 3]},
            {"head": [5, 10, 1, 3]},
            {"head": [100, 50, 0, -50, -100]},
            {"head": make_distinct_list(8801, 200, -5000, 5000)},
            {"head": make_distinct_list(8802, 2500, -100000, 100000)},
        ],
    },
    {
        "slug": "89-reverse-disjoint-intervals-in-linked-list",
        "title": "Reverse Disjoint Intervals in Linked List",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Google", "Meta", "Amazon", "Salesforce"],
        "desc": (
            "Given the `head` of a singly linked list of length `n` and a 2D integer array `intervals`, where each "
            "`intervals[i] = [l, r]` (`1 <= l <= r <= n`) specifies a 1-indexed inclusive range of positions, all "
            "intervals in `intervals` are guaranteed to be **pairwise disjoint** (they may be given in any order, "
            "and two intervals may be directly adjacent such as `[1, 2]` and `[3, 4]`).\n\n"
            "Reverse the nodes within every interval `[l, r]` in-place and return the head of the modified linked "
            "list. Aim for `O(n + m log m)` time where `m = intervals.length`."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "0 <= intervals.length <= 5000",
            "For every interval [l, r], 1 <= l <= r <= n, and all intervals are pairwise disjoint.",
        ],
        "hints": [
            "Sort `intervals` by their starting index `l` so that every interval can be processed in a single left-to-right sweep over the linked list.",
            "Maintain `prev` at 1-based index `pos`: for each `[l, r]`, advance `prev` until `pos == l - 1`, reverse the `r - l + 1` nodes starting at `prev.next`, and then set `prev` to the reversed segment's tail and `pos = r`.",
        ],
        "explanations": [
            "Sorting gives [1, 3] and [5, 7]; reversing positions 1..3 and 5..7 turns [1..7] into [3, 2, 1, 4, 7, 6, 5].",
            "Adjacent intervals [1, 2] and [3, 5] reverse [10, 20] -> [20, 10] and [30, 40, 50] -> [50, 40, 30].",
            "No intervals to reverse leaves [1, 2, 3] unchanged.",
        ],
        "time": "O(n + m log m)",
        "space": "O(m)",
        "kind": "function",
        "method": "reverseDisjointIntervals",
        "params": [("head", "ListNode"), ("intervals", "int[][]")],
        "ret": "ListNode",
        "py": """        if head is None or not intervals:
            return head
        ordered = sorted(intervals, key=lambda x: x[0])
        dummy = ListNode(0, head)
        prev = dummy
        pos = 0
        for l, r in ordered:
            while pos < l - 1:
                prev = prev.next
                pos += 1
            tail = prev.next
            curr = tail
            rprev = None
            for _ in range(r - l + 1):
                nxt = curr.next
                curr.next = rprev
                rprev = curr
                curr = nxt
            prev.next = rprev
            tail.next = curr
            prev = tail
            pos = r
        return dummy.next""",
        "java": """        if (head == null || intervals == null || intervals.length == 0) {
            return head;
        }
        int[][] ordered = new int[intervals.length][];
        System.arraycopy(intervals, 0, ordered, 0, intervals.length);
        Arrays.sort(ordered, (a, b) -> Integer.compare(a[0], b[0]));

        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        int pos = 0;
        for (int[] iv : ordered) {
            int l = iv[0];
            int r = iv[1];
            while (pos < l - 1) {
                prev = prev.next;
                pos++;
            }
            ListNode tail = prev.next;
            ListNode curr = tail;
            ListNode rprev = null;
            for (int i = 0; i < r - l + 1; i++) {
                ListNode nxt = curr.next;
                curr.next = rprev;
                rprev = curr;
                curr = nxt;
            }
            prev.next = rprev;
            tail.next = curr;
            prev = tail;
            pos = r;
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5, 6, 7], "intervals": [[5, 7], [1, 3]]},
            {"head": [10, 20, 30, 40, 50], "intervals": [[3, 5], [1, 2]]},
            {"head": [1, 2, 3], "intervals": []},
        ],
        "hidden": [
            {"head": [], "intervals": []},
            {"head": [5], "intervals": [[1, 1]]},
            {"head": [1, 2, 3, 4], "intervals": [[1, 4]]},
            {"head": [1, 2, 3, 4, 5], "intervals": [[2, 2], [4, 4], [1, 1]]},
            {"head": [1, 2, 3, 4, 5, 6], "intervals": [[5, 6], [3, 4], [1, 2]]},
            {"head": [9, 8, 7, 6, 5, 4, 3, 2], "intervals": [[4, 6], [2, 3]]},
            {"head": [-1, -2, -3, -4, -5, -6, -7, -8, -9], "intervals": [[7, 9], [1, 2], [4, 5]]},
            {"head": make_rng_list(8901, 200, -1000, 1000), "intervals": make_disjoint_intervals(8902, 200, 30)},
            {"head": make_rng_list(8903, 2500, -100000, 100000), "intervals": make_disjoint_intervals(8904, 2500, 300)},
        ],
    },
    # =========================================================================
    # 90-94: Merge & Sort
    # =========================================================================
    {
        "slug": "90-union-of-two-sorted-linked-lists",
        "title": "Union of Two Sorted Linked Lists",
        "difficulty": "Easy",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Microsoft", "LinkedIn", "Oracle"],
        "desc": (
            "Given the heads of two singly linked lists `l1` and `l2`, each sorted in **non-decreasing** order "
            "(each list may contain duplicate values), return a new singly linked list sorted in **strictly "
            "increasing** order containing every distinct value that appears in `l1` or `l2` (their set union).\n\n"
            "If both lists are empty, return `null` (`None` in Python). Aim for `O(n + m)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in each list is in the range [0, 5000].",
            "-10^5 <= Node.val <= 10^5",
            "Both l1 and l2 are sorted in non-decreasing order.",
        ],
        "hints": [
            "Walk two pointers through `l1` and `l2` selecting the smaller current node at each step, just like merging two sorted lists.",
            "Only append a chosen node to `tail` when the output list is still empty (`tail == dummy`) or `node.val != tail.val`, and terminate with `tail.next = null` at the end.",
        ],
        "explanations": [
            "Distinct values across [1, 2, 2, 4] and [2, 3, 4, 5] in sorted order are [1, 2, 3, 4, 5].",
            "All duplicates of 0 and 1 collapse to [0, 1].",
            "With l1 empty, deduplicating l2 gives [-3, 0, 4].",
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "kind": "function",
        "method": "unionSortedLists",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0)
        tail = dummy
        while l1 is not None or l2 is not None:
            if l2 is None or (l1 is not None and l1.val <= l2.val):
                node = l1
                l1 = l1.next
            else:
                node = l2
                l2 = l2.next
            if tail is dummy or node.val != tail.val:
                tail.next = node
                tail = node
        tail.next = None
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null || l2 != null) {
            ListNode node;
            if (l2 == null || (l1 != null && l1.val <= l2.val)) {
                node = l1;
                l1 = l1.next;
            } else {
                node = l2;
                l2 = l2.next;
            }
            if (tail == dummy || node.val != tail.val) {
                tail.next = node;
                tail = node;
            }
        }
        tail.next = null;
        return dummy.next;""",
        "visible": [
            {"l1": [1, 2, 2, 4], "l2": [2, 3, 4, 5]},
            {"l1": [0, 0, 0], "l2": [0, 1, 1]},
            {"l1": [], "l2": [-3, -3, 0, 4, 4]},
        ],
        "hidden": [
            {"l1": [], "l2": []},
            {"l1": [7, 7, 7], "l2": []},
            {"l1": [1], "l2": [1]},
            {"l1": [1, 3, 5], "l2": [2, 4, 6]},
            {"l1": [-100, -100, 0, 0], "l2": [-100, 0, 100, 100]},
            {"l1": [1, 1, 2, 2, 3, 3], "l2": [1, 2, 3]},
            {"l1": [1, 2, 3], "l2": [10, 10, 20, 20]},
            {"l1": sorted(make_rng_list(9001, 200, -50, 50)), "l2": sorted(make_rng_list(9002, 200, -50, 50))},
            {"l1": sorted(make_rng_list(9003, 1500, -600, 600)), "l2": sorted(make_rng_list(9004, 1500, -600, 600))},
        ],
    },
    {
        "slug": "91-kth-smallest-in-sorted-linked-lists",
        "title": "K-th Smallest in Sorted Linked Lists",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Google", "Amazon", "Meta", "Uber"],
        "desc": (
            "You are given an array `lists` of `m` singly linked lists, where each linked list is sorted in "
            "**non-decreasing** order (some lists may be empty), and a 1-indexed integer `k`.\n\n"
            "Return the `k`-th smallest value across all nodes of all lists combined (counting duplicates with their "
            "multiplicity). It is guaranteed that `1 <= k <= N`, where `N` is the total number of nodes across all "
            "lists. Aim for `O((m + k) log m)` time and `O(m)` space."
        ),
        "cons": [
            "1 <= lists.length <= 500",
            "0 <= lists[i].length <= 2000",
            "1 <= N <= 10^4 (total nodes across all lists)",
            "1 <= k <= N",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Push the head of every non-empty linked list into a min-heap ordered by `node.val`.",
            "Repeatedly pop the smallest node `k` times, pushing `node.next` back into the heap whenever it is non-null; the value popped on the `k`-th step is the answer.",
        ],
        "explanations": [
            "All values sorted are [1, 1, 2, 3, 4, 4, 5, 6]; the 5th smallest is 4.",
            "All values sorted are [-5, -2, 0, 3, 7, 10]; the 3rd smallest is 0.",
            "Only one non-empty list [9, 12, 15]; the 1st smallest is 9.",
        ],
        "time": "O((m + k) log m)",
        "space": "O(m)",
        "kind": "function",
        "method": "kthSmallestInLists",
        "params": [("lists", "ListNode[]"), ("k", "int")],
        "ret": "int",
        "py_full": """import heapq


class Solution:
    def kthSmallestInLists(self, lists: List[Optional[ListNode]], k: int) -> int:
        heap: list[tuple[int, int, ListNode]] = []
        for idx, head in enumerate(lists):
            if head is not None:
                heapq.heappush(heap, (head.val, idx, head))
        ans = 0
        for _ in range(k):
            val, idx, node = heapq.heappop(heap)
            ans = val
            if node.next is not None:
                heapq.heappush(heap, (node.next.val, idx, node.next))
        return ans
""",
        "java_full": """class Solution {
    public int kthSmallestInLists(ListNode[] lists, int k) {
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
        for (ListNode head : lists) {
            if (head != null) {
                pq.offer(head);
            }
        }
        int ans = 0;
        for (int i = 0; i < k; i++) {
            ListNode node = pq.poll();
            ans = node.val;
            if (node.next != null) {
                pq.offer(node.next);
            }
        }
        return ans;
    }
}
""",
        "visible": [
            {"lists": [[1, 4, 5], [1, 3, 4], [2, 6]], "k": 5},
            {"lists": [[-5, 0, 10], [-2, 3, 7]], "k": 3},
            {"lists": [[], [9, 12, 15], []], "k": 1},
        ],
        "hidden": [
            {"lists": [[42]], "k": 1},
            {"lists": [[1, 2, 3], [4, 5, 6]], "k": 6},
            {"lists": [[2, 2, 2], [2, 2], [2]], "k": 4},
            {"lists": [[10], [5], [1], [8], [3]], "k": 3},
            {"lists": [[-10, -5, 0], [-8, -5, 2], [-10, 1, 9]], "k": 2},
            {"lists": [[1, 100], [2, 200], [3, 300], [4, 400]], "k": 7},
            {"lists": [[], [], [5, 10, 15], [5, 10], []], "k": 5},
            {"lists": [sorted(make_rng_list(9100 + i, 25, -500, 500)) for i in range(10)], "k": 137},
            {"lists": [sorted(make_rng_list(9150 + i, 100, -100000, 100000)) for i in range(25)], "k": 1823},
        ],
    },
    {
        "slug": "92-sort-linked-list-by-frequency",
        "title": "Sort Linked List by Frequency",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Bloomberg", "Apple", "Meta"],
        "desc": (
            "Given the `head` of a singly linked list of integers, sort its nodes in **decreasing order of value "
            "frequency** (values that occur more frequently appear earlier in the list).\n\n"
            "If two distinct values have the **same frequency**, place the **smaller numeric value** first. "
            "Return the head of the sorted linked list."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Count the frequency of every node value in one pass using a hash map.",
            "Sort the nodes using the composite comparator `(-freq[node.val], node.val)` and relink their `next` pointers (ending with `tail.next = null`).",
        ],
        "explanations": [
            "2 and 3 both occur twice (2 < 3), while 1, 4, and 8 occur once each (1 < 4 < 8), producing [2, 2, 3, 3, 1, 4, 8].",
            "Values -1 occurs three times and 2 occurs twice, producing [-1, -1, -1, 2, 2].",
            "All values occur once, so tie-breaking sorts them in ascending order [-5, 0, 3, 9].",
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "kind": "function",
        "method": "sortByFrequency",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None:
            return head
        freq: dict[int, int] = {}
        nodes: list[ListNode] = []
        curr = head
        while curr is not None:
            freq[curr.val] = freq.get(curr.val, 0) + 1
            nodes.append(curr)
            curr = curr.next
        nodes.sort(key=lambda node: (-freq[node.val], node.val))
        for i in range(len(nodes) - 1):
            nodes[i].next = nodes[i + 1]
        nodes[-1].next = None
        return nodes[0]""",
        "java": """        if (head == null || head.next == null) {
            return head;
        }
        Map<Integer, Integer> freq = new HashMap<>();
        List<ListNode> nodes = new ArrayList<>();
        ListNode curr = head;
        while (curr != null) {
            freq.merge(curr.val, 1, Integer::sum);
            nodes.add(curr);
            curr = curr.next;
        }
        nodes.sort((a, b) -> {
            int cmp = Integer.compare(freq.get(b.val), freq.get(a.val));
            return cmp != 0 ? cmp : Integer.compare(a.val, b.val);
        });
        for (int i = 0; i < nodes.size() - 1; i++) {
            nodes.get(i).next = nodes.get(i + 1);
        }
        nodes.get(nodes.size() - 1).next = null;
        return nodes.get(0);""",
        "visible": [
            {"head": [4, 2, 2, 8, 3, 3, 1]},
            {"head": [2, -1, 2, -1, -1]},
            {"head": [9, -5, 3, 0]},
        ],
        "hidden": [
            {"head": []},
            {"head": [7]},
            {"head": [5, 5, 5, 5]},
            {"head": [1, 2, 1, 2, 3, 3]},
            {"head": [10, 10, 5, 5, 5, 20, 20, 20, 20]},
            {"head": [-2, -2, -1, -1, -3, -3, 0]},
            {"head": [100000, -100000, 100000, 0, -100000, 0]},
            {"head": make_rng_list(9201, 200, -25, 25)},
            {"head": make_rng_list(9202, 2500, -200, 200)},
        ],
    },
    {
        "slug": "93-three-way-partition-linked-list",
        "title": "Three-Way Partition Linked List",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Google", "Amazon", "Microsoft", "Goldman Sachs"],
        "desc": (
            "Given the `head` of a singly linked list and two integers `low` and `high` (`low <= high`), partition the "
            "linked list into three consecutive sections:\n"
            "1. All nodes with `val < low`\n"
            "2. All nodes with `low <= val <= high`\n"
            "3. All nodes with `val > high`\n\n"
            "Preserve the **original relative order** of nodes within each of the three sections. Return the head of "
            "the partitioned linked list in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val, low, high <= 10^5",
            "low <= high",
        ],
        "hints": [
            "Create three sentinel dummy heads (`lessDummy`, `midDummy`, `highDummy`) and three corresponding tail pointers.",
            "Route each node to its bucket in a single pass, terminate `highTail.next = null`, then connect `midTail.next = highDummy.next` and `lessTail.next = midDummy.next` (in that order, so empty buckets collapse automatically).",
        ],
        "explanations": [
            "With [low, high] = [3, 5]: (<3) is [1, 2], (3..5) is [4, 3, 5], (>5) is [8, 6], giving [1, 2, 4, 3, 5, 8, 6].",
            "When low == high == 2: (<2) is [1, 0], (==2) is [2, 2], (>2) is [5, 3], giving [1, 0, 2, 2, 5, 3].",
            "All nodes fall in the middle range [0, 10], so the list stays [7, 3, 9, 1].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "threeWayPartition",
        "params": [("head", "ListNode"), ("low", "int"), ("high", "int")],
        "ret": "ListNode",
        "py": """        less_d = ListNode(0)
        mid_d = ListNode(0)
        high_d = ListNode(0)
        less_t, mid_t, high_t = less_d, mid_d, high_d
        curr = head
        while curr is not None:
            if curr.val < low:
                less_t.next = curr
                less_t = curr
            elif curr.val <= high:
                mid_t.next = curr
                mid_t = curr
            else:
                high_t.next = curr
                high_t = curr
            curr = curr.next
        high_t.next = None
        mid_t.next = high_d.next
        less_t.next = mid_d.next
        return less_d.next""",
        "java": """        ListNode lessD = new ListNode(0);
        ListNode midD = new ListNode(0);
        ListNode highD = new ListNode(0);
        ListNode lessT = lessD;
        ListNode midT = midD;
        ListNode highT = highD;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val < low) {
                lessT.next = curr;
                lessT = curr;
            } else if (curr.val <= high) {
                midT.next = curr;
                midT = curr;
            } else {
                highT.next = curr;
                highT = curr;
            }
            curr = curr.next;
        }
        highT.next = null;
        midT.next = highD.next;
        lessT.next = midD.next;
        return lessD.next;""",
        "visible": [
            {"head": [8, 4, 1, 6, 3, 2, 5], "low": 3, "high": 5},
            {"head": [5, 2, 1, 3, 2, 0], "low": 2, "high": 2},
            {"head": [7, 3, 9, 1], "low": 0, "high": 10},
        ],
        "hidden": [
            {"head": [], "low": 0, "high": 5},
            {"head": [10], "low": 0, "high": 5},
            {"head": [10, 9, 8, 7], "low": 100, "high": 200},
            {"head": [10, 9, 8, 7], "low": -50, "high": -10},
            {"head": [10, 1, 9, 2, 8, 3], "low": 4, "high": 7},
            {"head": [-5, 0, 5, -10, 10, -1, 1], "low": -1, "high": 1},
            {"head": [3, 3, 3, 1, 1, 5, 5], "low": 3, "high": 3},
            {"head": make_rng_list(9301, 200, -500, 500), "low": -100, "high": 100},
            {"head": make_rng_list(9302, 2500, -100000, 100000), "low": -25000, "high": 25000},
        ],
    },
    {
        "slug": "94-maximum-sum-path-two-sorted-lists",
        "title": "Maximum Sum Path Across Two Sorted Lists",
        "difficulty": "Hard",
        "subtopic": "Merge & Sort",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Goldman Sachs"],
        "desc": (
            "You are given the heads of two singly linked lists `l1` and `l2`, each sorted in **strictly increasing** "
            "order of positive integers.\n\n"
            "A valid path starts at the head of either `l1` or `l2` and moves forward node by node. Whenever you "
            "reach a value that appears in **both** lists, you may optionally switch to the other list at that "
            "common node (counting the shared value only once) and continue walking forward until reaching the end "
            "of a list.\n\n"
            "Return the **maximum possible sum** of node values along any valid path as a 64-bit integer (`long` in "
            "Java, `int` in Python). Aim for `O(n + m)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in each list is in the range [0, 5000].",
            "1 <= Node.val <= 10^6",
            "Both l1 and l2 are sorted in strictly increasing order.",
        ],
        "hints": [
            "Walk two pointers `p1` and `p2` through `l1` and `l2` simultaneously like a merge step, maintaining two running segment sums `sum1` and `sum2` since the last common node.",
            "Whenever `p1.val == p2.val`, add `max(sum1, sum2) + p1.val` to the answer, reset both segment sums to `0`, and advance both pointers; after the loop, drain any remaining nodes into `sum1`/`sum2` and add `max(sum1, sum2)`.",
        ],
        "explanations": [
            "Switching at common nodes 4 and 8 along 2 -> 4 -> 6 -> 8 -> 10 gives the maximum sum 2 + 4 + 6 + 8 + 10 = 30.",
            "The lists share no common values, so take the list with larger total sum: [10, 20, 30] sums to 60.",
            "Both lists are identical [1, 3, 5], so the maximum sum is 1 + 3 + 5 = 9.",
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "kind": "function",
        "method": "maxSumPath",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "long",
        "py": """        p1, p2 = l1, l2
        sum1 = 0
        sum2 = 0
        ans = 0
        while p1 is not None and p2 is not None:
            if p1.val < p2.val:
                sum1 += p1.val
                p1 = p1.next
            elif p2.val < p1.val:
                sum2 += p2.val
                p2 = p2.next
            else:
                ans += max(sum1, sum2) + p1.val
                sum1 = 0
                sum2 = 0
                p1 = p1.next
                p2 = p2.next
        while p1 is not None:
            sum1 += p1.val
            p1 = p1.next
        while p2 is not None:
            sum2 += p2.val
            p2 = p2.next
        return ans + max(sum1, sum2)""",
        "java": """        ListNode p1 = l1;
        ListNode p2 = l2;
        long sum1 = 0L;
        long sum2 = 0L;
        long ans = 0L;
        while (p1 != null && p2 != null) {
            if (p1.val < p2.val) {
                sum1 += p1.val;
                p1 = p1.next;
            } else if (p2.val < p1.val) {
                sum2 += p2.val;
                p2 = p2.next;
            } else {
                ans += Math.max(sum1, sum2) + p1.val;
                sum1 = 0L;
                sum2 = 0L;
                p1 = p1.next;
                p2 = p2.next;
            }
        }
        while (p1 != null) {
            sum1 += p1.val;
            p1 = p1.next;
        }
        while (p2 != null) {
            sum2 += p2.val;
            p2 = p2.next;
        }
        return ans + Math.max(sum1, sum2);""",
        "visible": [
            {"l1": [2, 4, 5, 8, 10], "l2": [4, 6, 8, 9]},
            {"l1": [1, 2, 3], "l2": [10, 20, 30]},
            {"l1": [1, 3, 5], "l2": [1, 3, 5]},
        ],
        "hidden": [
            {"l1": [], "l2": []},
            {"l1": [], "l2": [100, 200, 300]},
            {"l1": [50], "l2": [50]},
            {"l1": [1, 3, 5, 7, 9], "l2": [3, 5, 100]},
            {"l1": [1, 4, 5, 8, 9, 11, 19], "l2": [2, 3, 4, 11, 12]},
            {"l1": [100000, 200000, 300000, 400000], "l2": [150000, 200000, 250000, 400000, 500000]},
            {"l1": [1, 2, 10, 11, 20, 21], "l2": [5, 10, 15, 20, 25]},
            {"l1": make_unique_sorted_list(9401, 200, 4, 1), "l2": make_unique_sorted_list(9402, 200, 4, 1)},
            {"l1": make_unique_sorted_list(9403, 1800, 3, 500000), "l2": make_unique_sorted_list(9404, 1800, 3, 500000)},
        ],
    },
])

TASKS.extend([
    # =========================================================================
    # 95-100: LRU Design
    # =========================================================================
    {
        "slug": "95-design-pinned-lru-cache",
        "title": "Design Pinned LRU Cache",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Netflix"],
        "desc": (
            "Design an LRU cache `PinnedLRUCache` that supports pinning entries so they cannot be evicted:\n"
            "- `PinnedLRUCache(int capacity)` initializes the cache with positive `capacity`.\n"
            "- `int get(int key)` returns the value of `key` if present, otherwise `-1`. If `key` is present and "
            "currently **unpinned**, it is promoted to the most recently used (MRU) position.\n"
            "- `boolean put(int key, int value)` inserts or updates `key` with `value`. If `key` already exists, "
            "update its value (and promote it to MRU if unpinned) and return `true`. If `key` does not exist and "
            "the cache is at `capacity`, evict the least recently used **unpinned** entry; if **all** entries are "
            "currently pinned (no entry can be evicted), leave the cache unchanged and return `false`. Otherwise "
            "insert `key` as an unpinned MRU entry and return `true`.\n"
            "- `boolean pin(int key)` pins `key` (preventing eviction while still counting toward `capacity`) and "
            "returns `true` if `key` exists in the cache (even if already pinned), or `false` if `key` is absent.\n"
            "- `boolean unpin(int key)` unpins `key` and returns `true` if `key` exists in the cache (if it was "
            "pinned, place it at the MRU position among unpinned entries), or `false` if `key` is absent.\n\n"
            "All operations must run in `O(1)` time."
        ),
        "cons": [
            "1 <= capacity <= 1000",
            "0 <= key, value <= 10^5",
            "At most 2000 calls will be made to get, put, pin, and unpin.",
        ],
        "hints": [
            "Maintain a hash map `key -> Node` for all cached entries (both pinned and unpinned) and a doubly linked list containing **only** the unpinned entries in MRU-to-LRU order.",
            "`pin(key)` simply unlinks the node from the unpinned DLL (marking `pinned = true`), while `unpin(key)` marks `pinned = false` and inserts it at the head (MRU) of the unpinned DLL; eviction on `put` checks whether the unpinned DLL is empty.",
        ],
        "explanations": [
            "Key 1 is pinned so put(3, 30) evicts unpinned key 2 instead of key 1; pinning key 3 makes the cache full of pinned entries so put(4, 40) returns false.",
            "Unpinning key 1 puts it at MRU ahead of key 2, so put(3, 30) evicts key 2 instead of key 1.",
            "Pinning or unpinning a missing key returns false; updating an existing pinned key still succeeds and returns true.",
        ],
        "time": "O(1) per operation",
        "space": "O(capacity)",
        "kind": "design",
        "className": "PinnedLRUCache",
        "ctor_params": [("capacity", "int")],
        "methods": [
            {"name": "get", "params": [("key", "int")], "ret": "int"},
            {"name": "put", "params": [("key", "int"), ("value", "int")], "ret": "boolean"},
            {"name": "pin", "params": [("key", "int")], "ret": "boolean"},
            {"name": "unpin", "params": [("key", "int")], "ret": "boolean"},
        ],
        "py_full": """class _PinNode:
    __slots__ = ("key", "val", "pinned", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0):
        self.key = key
        self.val = val
        self.pinned = False
        self.prev: Optional[_PinNode] = None
        self.next: Optional[_PinNode] = None


class PinnedLRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, _PinNode] = {}
        self.head = _PinNode()
        self.tail = _PinNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _PinNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        node.prev = None
        node.next = None

    def _add_front(self, node: _PinNode) -> None:
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        if not node.pinned:
            self._unlink(node)
            self._add_front(node)
        return node.val

    def put(self, key: int, value: int) -> bool:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            if not node.pinned:
                self._unlink(node)
                self._add_front(node)
            return True
        if len(self.map) == self.cap:
            if self.tail.prev is self.head:
                return False
            victim = self.tail.prev
            self._unlink(victim)
            del self.map[victim.key]
        node = _PinNode(key, value)
        self.map[key] = node
        self._add_front(node)
        return True

    def pin(self, key: int) -> bool:
        node = self.map.get(key)
        if node is None:
            return False
        if not node.pinned:
            self._unlink(node)
            node.pinned = True
        return True

    def unpin(self, key: int) -> bool:
        node = self.map.get(key)
        if node is None:
            return False
        if node.pinned:
            node.pinned = False
            self._add_front(node)
        return True
""",
        "java_full": """class PinnedLRUCache {
    private static class Node {
        int key, val;
        boolean pinned;
        Node prev, next;

        Node(int k, int v) {
            this.key = k;
            this.val = v;
        }
    }

    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0);
    private final Node tail = new Node(0, 0);

    public PinnedLRUCache(int capacity) {
        this.cap = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
        node.prev = null;
        node.next = null;
    }

    private void addFront(Node node) {
        Node nxt = head.next;
        head.next = node;
        node.prev = head;
        node.next = nxt;
        nxt.prev = node;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        if (!node.pinned) {
            unlink(node);
            addFront(node);
        }
        return node.val;
    }

    public boolean put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            if (!node.pinned) {
                unlink(node);
                addFront(node);
            }
            return true;
        }
        if (map.size() == cap) {
            if (tail.prev == head) {
                return false;
            }
            Node victim = tail.prev;
            unlink(victim);
            map.remove(victim.key);
        }
        node = new Node(key, value);
        map.put(key, node);
        addFront(node);
        return true;
    }

    public boolean pin(int key) {
        Node node = map.get(key);
        if (node == null) {
            return false;
        }
        if (!node.pinned) {
            unlink(node);
            node.pinned = true;
        }
        return true;
    }

    public boolean unpin(int key) {
        Node node = map.get(key);
        if (node == null) {
            return false;
        }
        if (node.pinned) {
            node.pinned = false;
            addFront(node);
        }
        return true;
    }
}
""",
        "visible": [
            {
                "ops": ["PinnedLRUCache", "put", "put", "pin", "put", "get", "get", "pin", "put", "get"],
                "args": [[2], [1, 10], [2, 20], [1], [3, 30], [2], [1], [3], [4, 40], [4]],
            },
            {
                "ops": ["PinnedLRUCache", "put", "put", "pin", "unpin", "put", "get", "get"],
                "args": [[2], [1, 10], [2, 20], [1], [1], [3, 30], [1], [2]],
            },
            {
                "ops": ["PinnedLRUCache", "pin", "unpin", "put", "pin", "put", "get"],
                "args": [[1], [9], [9], [1, 5], [1], [1, 99], [1]],
            },
        ],
        "hidden_fn": "gen_hidden_95",
    },
    {
        "slug": "96-design-weighted-lru-cache",
        "title": "Design Weighted LRU Cache",
        "difficulty": "Hard",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Uber", "Netflix"],
        "desc": (
            "Design a byte-bounded LRU cache `WeightedLRUCache` where each entry consumes a positive integer `weight` "
            "toward a total budget `maxWeight`:\n"
            "- `WeightedLRUCache(int maxWeight)` initializes an empty cache with total weight budget `maxWeight`.\n"
            "- `int get(int key)` returns the value of `key` if it exists and promotes `key` to the most recently "
            "used (MRU) position; otherwise returns `-1`.\n"
            "- `boolean put(int key, int value, int weight)` stores `(key, value, weight)`:\n"
            "  - If `weight > maxWeight`, the item can never fit: leave the cache completely unchanged and return `false`.\n"
            "  - Otherwise, if `key` already exists, remove its old entry first (releasing its old weight). Then, "
            "while `currentWeight + weight > maxWeight`, evict the least recently used (LRU) entry. Finally insert "
            "`(key, value, weight)` at the MRU position and return `true`.\n"
            "- `int currentWeight()` returns the sum of weights of all entries currently in the cache.\n\n"
            "Aim for `O(1)` amortized time per operation."
        ),
        "cons": [
            "1 <= maxWeight <= 10^6",
            "0 <= key, value <= 10^5",
            "1 <= weight <= 10^6",
            "At most 2000 calls will be made to get, put, and currentWeight.",
        ],
        "hints": [
            "Maintain a standard LRU doubly linked list and hash map `key -> Node(key, val, weight)` plus a running integer `totalWeight`.",
            "On `put`, reject immediately if `weight > maxWeight`; otherwise unlink any existing entry for `key`, evict from the tail while `totalWeight + weight > maxWeight`, and insert the new node at the head. Each entry is inserted once and evicted at most once, giving `O(1)` amortized time.",
        ],
        "explanations": [
            "Putting (1,10,w=4) and (2,20,w=5) brings weight to 9; putting (3,30,w=7) evicts both 1 and 2 since 5+7>10, leaving weight 7.",
            "Item (2,20,w=11) exceeds maxWeight=10 so put returns false and leaves key 1 intact.",
            "Updating key 1 from weight 6 to weight 2 frees weight first so key 2 is not evicted.",
        ],
        "time": "O(1) amortized",
        "space": "O(n)",
        "kind": "design",
        "className": "WeightedLRUCache",
        "ctor_params": [("maxWeight", "int")],
        "methods": [
            {"name": "get", "params": [("key", "int")], "ret": "int"},
            {"name": "put", "params": [("key", "int"), ("value", "int"), ("weight", "int")], "ret": "boolean"},
            {"name": "currentWeight", "params": [], "ret": "int"},
        ],
        "py_full": """class _WNode:
    __slots__ = ("key", "val", "weight", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0, weight: int = 0):
        self.key = key
        self.val = val
        self.weight = weight
        self.prev: Optional[_WNode] = None
        self.next: Optional[_WNode] = None


class WeightedLRUCache:
    def __init__(self, maxWeight: int):
        self.max_weight = maxWeight
        self.total_weight = 0
        self.map: dict[int, _WNode] = {}
        self.head = _WNode()
        self.tail = _WNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _WNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _add_front(self, node: _WNode) -> None:
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._add_front(node)
        return node.val

    def put(self, key: int, value: int, weight: int) -> bool:
        if weight > self.max_weight:
            return False
        old = self.map.get(key)
        if old is not None:
            self._unlink(old)
            self.total_weight -= old.weight
            del self.map[key]
        while self.total_weight + weight > self.max_weight:
            victim = self.tail.prev
            self._unlink(victim)
            self.total_weight -= victim.weight
            del self.map[victim.key]
        node = _WNode(key, value, weight)
        self.map[key] = node
        self._add_front(node)
        self.total_weight += weight
        return True

    def currentWeight(self) -> int:
        return self.total_weight
""",
        "java_full": """class WeightedLRUCache {
    private static class Node {
        int key, val, weight;
        Node prev, next;

        Node(int k, int v, int w) {
            this.key = k;
            this.val = v;
            this.weight = w;
        }
    }

    private final int maxWeight;
    private int totalWeight = 0;
    private final Map<Integer, Node> map = new HashMap<>();
    private final Node head = new Node(0, 0, 0);
    private final Node tail = new Node(0, 0, 0);

    public WeightedLRUCache(int maxWeight) {
        this.maxWeight = maxWeight;
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void addFront(Node node) {
        Node nxt = head.next;
        head.next = node;
        node.prev = head;
        node.next = nxt;
        nxt.prev = node;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        unlink(node);
        addFront(node);
        return node.val;
    }

    public boolean put(int key, int value, int weight) {
        if (weight > maxWeight) {
            return false;
        }
        Node old = map.get(key);
        if (old != null) {
            unlink(old);
            totalWeight -= old.weight;
            map.remove(key);
        }
        while (totalWeight + weight > maxWeight) {
            Node victim = tail.prev;
            unlink(victim);
            totalWeight -= victim.weight;
            map.remove(victim.key);
        }
        Node node = new Node(key, value, weight);
        map.put(key, node);
        addFront(node);
        totalWeight += weight;
        return true;
    }

    public int currentWeight() {
        return totalWeight;
    }
}
""",
        "visible": [
            {
                "ops": ["WeightedLRUCache", "put", "put", "currentWeight", "put", "get", "get", "get", "currentWeight"],
                "args": [[10], [1, 10, 4], [2, 20, 5], [], [3, 30, 7], [1], [2], [3], []],
            },
            {
                "ops": ["WeightedLRUCache", "put", "put", "get", "currentWeight"],
                "args": [[10], [1, 10, 6], [2, 20, 11], [1], []],
            },
            {
                "ops": ["WeightedLRUCache", "put", "put", "put", "get", "get", "currentWeight"],
                "args": [[10], [1, 10, 6], [2, 20, 4], [1, 15, 2], [2], [1], []],
            },
        ],
        "hidden_fn": "gen_hidden_96",
    },
    {
        "slug": "97-design-segmented-lru-cache",
        "title": "Design Segmented LRU Cache",
        "difficulty": "Hard",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "desc": (
            "Design a **Segmented LRU (SLRU)** cache `SLRUCache` consisting of two separate LRU doubly linked lists: "
            "a **probation** segment (segment `1`) with capacity `probationCap` and a **protected** segment "
            "(segment `2`) with capacity `protectedCap`.\n"
            "- `SLRUCache(int probationCap, int protectedCap)` initializes both segments as empty.\n"
            "- `int get(int key)`: if `key` is absent, return `-1`. If `key` is in `protected`, move it to the MRU "
            "of `protected` and return its value. If `key` is in `probation`, **promote** it to the MRU of "
            "`protected` (if `protected` was already at `protectedCap`, first demote the LRU entry of `protected` to "
            "the MRU of `probation`) and return its value.\n"
            "- `void put(int key, int value)`:\n"
            "  - If `key` is in `protected`: update its value and move it to the MRU of `protected`.\n"
            "  - If `key` is in `probation`: update its value and **promote** it to the MRU of `protected` "
            "(demoting `protected`'s LRU to `probation`'s MRU if `protected` was full).\n"
            "  - If `key` is new: insert `(key, value)` at the MRU of `probation`; if `probation` exceeds "
            "`probationCap`, evict the LRU entry of `probation`.\n"
            "- `int segmentOf(int key)` returns `0` if `key` is not in the cache, `1` if in `probation`, or `2` if "
            "in `protected`.\n\n"
            "All operations must run in `O(1)` time."
        ),
        "cons": [
            "1 <= probationCap, protectedCap <= 1000",
            "0 <= key, value <= 10^5",
            "At most 2000 calls will be made to get, put, and segmentOf.",
        ],
        "hints": [
            "Represent each segment (`probation` and `protected`) as a small doubly linked list helper with sentinel head/tail pointers and a `size` counter, plus a single hash map `key -> Node` where each node records `seg` (`1` or `2`).",
            "Notice that when a node in `probation` is promoted into a full `protected` segment, `probation` first shrinks by 1 and then receives 1 demoted node from `protected`, so `probation` never overflows during a promotion.",
        ],
        "explanations": [
            "Keys 1 and 2 enter probation (cap 2); get(1) promotes 1 to protected (seg 2); put(3,30) enters probation without evicting 2; put(4,40) evicts probation LRU 2.",
            "When protected (cap 1) already holds key 1, promoting key 2 demotes key 1 back to probation MRU (seg 1).",
            "Updating key 1 via put(1, 99) while in probation promotes it to protected (seg 2) with the new value.",
        ],
        "time": "O(1) per operation",
        "space": "O(probationCap + protectedCap)",
        "kind": "design",
        "className": "SLRUCache",
        "ctor_params": [("probationCap", "int"), ("protectedCap", "int")],
        "methods": [
            {"name": "get", "params": [("key", "int")], "ret": "int"},
            {"name": "put", "params": [("key", "int"), ("value", "int")], "ret": "void"},
            {"name": "segmentOf", "params": [("key", "int")], "ret": "int"},
        ],
        "py_full": """class _SNode:
    __slots__ = ("key", "val", "seg", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0, seg: int = 1):
        self.key = key
        self.val = val
        self.seg = seg
        self.prev: Optional[_SNode] = None
        self.next: Optional[_SNode] = None


class _DLL:
    def __init__(self):
        self.head = _SNode()
        self.tail = _SNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def add_front(self, node: _SNode) -> None:
        nxt = self.head.next
        self.head.next = node
        node.prev = self.head
        node.next = nxt
        nxt.prev = node
        self.size += 1

    def unlink(self, node: _SNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1

    def pop_back(self) -> _SNode:
        node = self.tail.prev
        self.unlink(node)
        return node


class SLRUCache:
    def __init__(self, probationCap: int, protectedCap: int):
        self.prob_cap = probationCap
        self.prot_cap = protectedCap
        self.prob = _DLL()
        self.prot = _DLL()
        self.map: dict[int, _SNode] = {}

    def _promote(self, node: _SNode) -> None:
        self.prob.unlink(node)
        if self.prot.size == self.prot_cap:
            demoted = self.prot.pop_back()
            demoted.seg = 1
            self.prob.add_front(demoted)
        node.seg = 2
        self.prot.add_front(node)

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        if node.seg == 2:
            self.prot.unlink(node)
            self.prot.add_front(node)
        else:
            self._promote(node)
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            if node.seg == 2:
                self.prot.unlink(node)
                self.prot.add_front(node)
            else:
                self._promote(node)
            return
        if self.prob.size == self.prob_cap:
            victim = self.prob.pop_back()
            del self.map[victim.key]
        node = _SNode(key, value, 1)
        self.map[key] = node
        self.prob.add_front(node)

    def segmentOf(self, key: int) -> int:
        node = self.map.get(key)
        return 0 if node is None else node.seg
""",
        "java_full": """class SLRUCache {
    private static class Node {
        int key, val, seg;
        Node prev, next;

        Node(int k, int v, int s) {
            this.key = k;
            this.val = v;
            this.seg = s;
        }
    }

    private static class DLL {
        final Node head = new Node(0, 0, 0);
        final Node tail = new Node(0, 0, 0);
        int size = 0;

        DLL() {
            head.next = tail;
            tail.prev = head;
        }

        void addFront(Node node) {
            Node nxt = head.next;
            head.next = node;
            node.prev = head;
            node.next = nxt;
            nxt.prev = node;
            size++;
        }

        void unlink(Node node) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
            size--;
        }

        Node popBack() {
            Node node = tail.prev;
            unlink(node);
            return node;
        }
    }

    private final int probCap;
    private final int protCap;
    private final DLL prob = new DLL();
    private final DLL prot = new DLL();
    private final Map<Integer, Node> map = new HashMap<>();

    public SLRUCache(int probationCap, int protectedCap) {
        this.probCap = probationCap;
        this.protCap = protectedCap;
    }

    private void promote(Node node) {
        prob.unlink(node);
        if (prot.size == protCap) {
            Node demoted = prot.popBack();
            demoted.seg = 1;
            prob.addFront(demoted);
        }
        node.seg = 2;
        prot.addFront(node);
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        if (node.seg == 2) {
            prot.unlink(node);
            prot.addFront(node);
        } else {
            promote(node);
        }
        return node.val;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            if (node.seg == 2) {
                prot.unlink(node);
                prot.addFront(node);
            } else {
                promote(node);
            }
            return;
        }
        if (prob.size == probCap) {
            Node victim = prob.popBack();
            map.remove(victim.key);
        }
        node = new Node(key, value, 1);
        map.put(key, node);
        prob.addFront(node);
    }

    public int segmentOf(int key) {
        Node node = map.get(key);
        return node == null ? 0 : node.seg;
    }
}
""",
        "visible": [
            {
                "ops": ["SLRUCache", "put", "put", "get", "segmentOf", "put", "put", "segmentOf", "segmentOf"],
                "args": [[2, 2], [1, 10], [2, 20], [1], [1], [3, 30], [4, 40], [2], [3]],
            },
            {
                "ops": ["SLRUCache", "put", "put", "get", "get", "segmentOf", "segmentOf"],
                "args": [[2, 1], [1, 10], [2, 20], [1], [2], [1], [2]],
            },
            {
                "ops": ["SLRUCache", "put", "segmentOf", "put", "segmentOf", "get"],
                "args": [[2, 2], [1, 10], [1], [1, 99], [1], [1]],
            },
        ],
        "hidden_fn": "gen_hidden_97",
    },
    {
        "slug": "98-design-removable-queue",
        "title": "Design Removable Queue",
        "difficulty": "Easy",
        "subtopic": "LRU Design",
        "companies": ["Amazon", "Uber", "LinkedIn", "Atlassian"],
        "desc": (
            "Design a FIFO queue `RemovableQueue` of unique integer IDs that also supports `O(1)` cancellation of "
            "any ID currently waiting in the queue:\n"
            "- `RemovableQueue()` initializes an empty queue.\n"
            "- `boolean enqueue(int id)` appends `id` to the back of the queue and returns `true` if `id` is not "
            "already present; if `id` is already in the queue, does nothing and returns `false`.\n"
            "- `int dequeue()` removes and returns the front `id` of the queue, or returns `-1` if the queue is empty.\n"
            "- `boolean cancel(int id)` removes `id` from anywhere in the queue and returns `true`, or returns "
            "`false` if `id` is not currently in the queue.\n"
            "- `int peekFront()` returns the front `id` without removing it, or `-1` if the queue is empty.\n"
            "- `int size()` returns the current number of elements in the queue.\n\n"
            "All operations must run in `O(1)` time."
        ),
        "cons": [
            "0 <= id <= 10^5",
            "At most 2500 calls will be made across all methods.",
        ],
        "hints": [
            "Store the queued items in a doubly linked list with sentinel `head` and `tail` nodes so adding to the back and removing from the front or middle all take `O(1)` time.",
            "Pair the doubly linked list with a hash map `id -> Node` to check duplicates on `enqueue` and locate the exact node to unlink on `cancel` in `O(1)`.",
        ],
        "explanations": [
            "Enqueue 10, 20, 30; cancel(20) removes 20 in O(1); dequeue returns 10, then 30, then -1.",
            "Duplicate enqueue(5) returns false; after dequeue() removes 5, enqueue(5) succeeds again.",
            "Canceling a missing ID returns false, and peekFront/dequeue on an empty queue return -1.",
        ],
        "time": "O(1) per operation",
        "space": "O(n)",
        "kind": "design",
        "className": "RemovableQueue",
        "ctor_params": [],
        "methods": [
            {"name": "enqueue", "params": [("id", "int")], "ret": "boolean"},
            {"name": "dequeue", "params": [], "ret": "int"},
            {"name": "cancel", "params": [("id", "int")], "ret": "boolean"},
            {"name": "peekFront", "params": [], "ret": "int"},
            {"name": "size", "params": [], "ret": "int"},
        ],
        "py_full": """class _QNode:
    __slots__ = ("val", "prev", "next")

    def __init__(self, val: int = 0):
        self.val = val
        self.prev: Optional[_QNode] = None
        self.next: Optional[_QNode] = None


class RemovableQueue:
    def __init__(self):
        self.head = _QNode()
        self.tail = _QNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.map: dict[int, _QNode] = {}

    def _unlink(self, node: _QNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def enqueue(self, id: int) -> bool:
        if id in self.map:
            return False
        node = _QNode(id)
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node
        self.map[id] = node
        return True

    def dequeue(self) -> int:
        if not self.map:
            return -1
        node = self.head.next
        self._unlink(node)
        del self.map[node.val]
        return node.val

    def cancel(self, id: int) -> bool:
        node = self.map.pop(id, None)
        if node is None:
            return False
        self._unlink(node)
        return True

    def peekFront(self) -> int:
        if not self.map:
            return -1
        return self.head.next.val

    def size(self) -> int:
        return len(self.map)
""",
        "java_full": """class RemovableQueue {
    private static class Node {
        int val;
        Node prev, next;

        Node(int v) {
            this.val = v;
        }
    }

    private final Node head = new Node(0);
    private final Node tail = new Node(0);
    private final Map<Integer, Node> map = new HashMap<>();

    public RemovableQueue() {
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    public boolean enqueue(int id) {
        if (map.containsKey(id)) {
            return false;
        }
        Node node = new Node(id);
        Node prev = tail.prev;
        prev.next = node;
        node.prev = prev;
        node.next = tail;
        tail.prev = node;
        map.put(id, node);
        return true;
    }

    public int dequeue() {
        if (map.isEmpty()) {
            return -1;
        }
        Node node = head.next;
        unlink(node);
        map.remove(node.val);
        return node.val;
    }

    public boolean cancel(int id) {
        Node node = map.remove(id);
        if (node == null) {
            return false;
        }
        unlink(node);
        return true;
    }

    public int peekFront() {
        if (map.isEmpty()) {
            return -1;
        }
        return head.next.val;
    }

    public int size() {
        return map.size();
    }
}
""",
        "visible": [
            {
                "ops": ["RemovableQueue", "enqueue", "enqueue", "enqueue", "cancel", "size", "dequeue", "dequeue", "dequeue"],
                "args": [[], [10], [20], [30], [20], [], [], [], []],
            },
            {
                "ops": ["RemovableQueue", "enqueue", "enqueue", "peekFront", "dequeue", "enqueue", "peekFront"],
                "args": [[], [5], [5], [], [], [5], []],
            },
            {
                "ops": ["RemovableQueue", "peekFront", "dequeue", "cancel", "size"],
                "args": [[], [], [], [7], []],
            },
        ],
        "hidden_fn": "gen_hidden_98",
    },
    {
        "slug": "99-design-clock-replacement-cache",
        "title": "Design Clock Replacement Cache",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Google", "Microsoft", "Apple", "Oracle"],
        "desc": (
            "Design a **Clock (Second-Chance)** page replacement cache `ClockCache` backed by a circular doubly "
            "linked list of frames and a `hand` pointer:\n"
            "- `ClockCache(int capacity)` initializes an empty cache of positive `capacity`.\n"
            "- `int get(int key)` returns the value of `key` if present and sets its reference bit `ref = 1` "
            "(without moving `hand`); otherwise returns `-1`.\n"
            "- `void put(int key, int value)`:\n"
            "  - If `key` already exists: update its value and set its reference bit `ref = 1` (without moving `hand`).\n"
            "  - If `key` is new and `size < capacity`: insert a new frame `(key, value, ref = 1)` immediately "
            "**before** `hand` in clockwise order (if the ring was empty, this single frame points to itself and "
            "`hand` points to it).\n"
            "  - If `key` is new and `size == capacity`: sweep `hand` clockwise — while `hand.ref == 1`, set "
            "`hand.ref = 0` and advance `hand = hand.next`. Once a frame with `hand.ref == 0` is found, evict its "
            "key, overwrite that frame in-place with `(key, value, ref = 1)`, and advance `hand = hand.next`.\n\n"
            "Aim for `O(1)` amortized time per operation."
        ),
        "cons": [
            "1 <= capacity <= 1000",
            "0 <= key, value <= 10^5",
            "At most 2000 calls will be made to get and put.",
        ],
        "hints": [
            "Maintain a circular doubly linked list of frames with a `hand` pointer and a hash map `key -> Node(key, val, ref)`.",
            "Inserting a new frame directly before `hand` preserves FIFO order from `hand`; during eviction, each `ref` bit cleared from `1` to `0` was set by a prior `get` or `put`, guaranteeing `O(1)` amortized cost.",
        ],
        "explanations": [
            "Ring starts 1(1)->2(1) with hand at 1. put(3,30) clears 1 and 2 to ref=0, replaces 1 with 3(1), hand moves to 2(0). put(4,40) immediately replaces 2(0) with 4(1).",
            "After put(3,30) leaves hand at 2(0), get(2) sets 2.ref=1, so put(4,40) sweeps past 2 and 3, then replaces 2 (the first frame encountered again with ref=0).",
            "With capacity 1, put(2, 20) clears 1's ref bit and replaces it in-place.",
        ],
        "time": "O(1) amortized",
        "space": "O(capacity)",
        "kind": "design",
        "className": "ClockCache",
        "ctor_params": [("capacity", "int")],
        "methods": [
            {"name": "get", "params": [("key", "int")], "ret": "int"},
            {"name": "put", "params": [("key", "int"), ("value", "int")], "ret": "void"},
        ],
        "py_full": """class _ClockNode:
    __slots__ = ("key", "val", "ref", "prev", "next")

    def __init__(self, key: int, val: int):
        self.key = key
        self.val = val
        self.ref = 1
        self.prev: Optional[_ClockNode] = self
        self.next: Optional[_ClockNode] = self


class ClockCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.hand: Optional[_ClockNode] = None
        self.map: dict[int, _ClockNode] = {}

    def get(self, key: int) -> int:
        node = self.map.get(key)
        if node is None:
            return -1
        node.ref = 1
        return node.val

    def put(self, key: int, value: int) -> None:
        node = self.map.get(key)
        if node is not None:
            node.val = value
            node.ref = 1
            return
        if len(self.map) < self.cap:
            node = _ClockNode(key, value)
            if self.hand is None:
                self.hand = node
            else:
                prev = self.hand.prev
                prev.next = node
                node.prev = prev
                node.next = self.hand
                self.hand.prev = node
            self.map[key] = node
            return
        while self.hand.ref == 1:
            self.hand.ref = 0
            self.hand = self.hand.next
        del self.map[self.hand.key]
        self.hand.key = key
        self.hand.val = value
        self.hand.ref = 1
        self.map[key] = self.hand
        self.hand = self.hand.next
""",
        "java_full": """class ClockCache {
    private static class Node {
        int key, val, ref;
        Node prev, next;

        Node(int k, int v) {
            this.key = k;
            this.val = v;
            this.ref = 1;
            this.prev = this;
            this.next = this;
        }
    }

    private final int cap;
    private Node hand = null;
    private final Map<Integer, Node> map = new HashMap<>();

    public ClockCache(int capacity) {
        this.cap = capacity;
    }

    public int get(int key) {
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        node.ref = 1;
        return node.val;
    }

    public void put(int key, int value) {
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            node.ref = 1;
            return;
        }
        if (map.size() < cap) {
            node = new Node(key, value);
            if (hand == null) {
                hand = node;
            } else {
                Node prev = hand.prev;
                prev.next = node;
                node.prev = prev;
                node.next = hand;
                hand.prev = node;
            }
            map.put(key, node);
            return;
        }
        while (hand.ref == 1) {
            hand.ref = 0;
            hand = hand.next;
        }
        map.remove(hand.key);
        hand.key = key;
        hand.val = value;
        hand.ref = 1;
        map.put(key, hand);
        hand = hand.next;
    }
}
""",
        "visible": [
            {
                "ops": ["ClockCache", "put", "put", "put", "get", "put", "get", "get", "get"],
                "args": [[2], [1, 10], [2, 20], [3, 30], [1], [4, 40], [2], [3], [4]],
            },
            {
                "ops": ["ClockCache", "put", "put", "put", "get", "put", "get", "get", "get"],
                "args": [[2], [1, 10], [2, 20], [3, 30], [2], [4, 40], [2], [3], [4]],
            },
            {
                "ops": ["ClockCache", "put", "get", "put", "get", "get"],
                "args": [[1], [1, 5], [1], [2, 9], [1], [2]],
            },
        ],
        "hidden_fn": "gen_hidden_99",
    },
    {
        "slug": "100-design-lru-k-cache",
        "title": "Design LRU-K Cache",
        "difficulty": "Hard",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Design an **LRU-K** cache `LRUKCache` that evicts entries using their backward `k`-th access time "
            "(used in database buffer pools to resist one-time sequential scans):\n"
            "- `LRUKCache(int capacity, int k)` initializes an empty cache with positive `capacity` and history window "
            "`k >= 1`.\n"
            "- Maintain a monotonically increasing logical clock `tick` (starting at `0`) that increments by `1` on "
            "every `put` call and every successful `get` hit (cache misses on `get` do not advance `tick`). Each "
            "cached key stores a FIFO queue of up to its `k` most recent access ticks while in the cache.\n"
            "- `int get(int key)`: if `key` is absent, return `-1`; otherwise record a new access tick for `key` and "
            "return its value.\n"
            "- `void put(int key, int value)`: if `key` already exists, update its value and record a new access tick. "
            "If `key` is new and the cache is at `capacity`, evict one entry according to the **LRU-K rule**:\n"
            "  1. Any entry with **fewer than `k`** accesses is evicted before any entry with `k` accesses; among "
            "entries with `< k` accesses, evict the one with the **earliest first access**.\n"
            "  2. If all cached entries have `k` accesses, evict the entry whose **`k`-th most recent access** "
            "(the oldest tick in its length-`k` history) is the **smallest**.\n"
            "  Then insert `(key, value)` with a fresh single-element access history `[tick]`.\n\n"
            "Aim for `O(log capacity)` amortized time per operation."
        ),
        "cons": [
            "1 <= capacity <= 1000",
            "1 <= k <= 10",
            "0 <= key, value <= 10^5",
            "At most 2000 calls will be made to get and put.",
        ],
        "hints": [
            "For every cached key, maintain a bounded deque `hist` of length at most `k`: `tier = 0 if len(hist) < k else 1`, and `hist[0]` is ALWAYS the exact comparison key (earliest access when `tier == 0`, or `k`-th most recent access when `tier == 1`).",
            "Use a lazy-deletion min-heap storing `(tier, hist[0], version, key)` with a globally monotonic `version` counter so re-inserted keys never collide with stale heap entries.",
        ],
        "explanations": [
            "With cap=2, k=2: key 1 reaches 2 accesses via get(1) while key 2 has only 1, so put(3,30) evicts key 2; after get(3), key 1's 2nd-recent tick (1) < key 3's (4), so put(4,40) evicts key 1.",
            "With k=1, LRU-1 behaves identically to a standard LRU cache: get(1) refreshes 1, so put(3,30) evicts key 2.",
            "Updating an existing key via put(1, 15) counts as an access, giving key 1 two accesses so put(3, 30) evicts key 2.",
        ],
        "time": "O(log n) amortized",
        "space": "O(n * k)",
        "kind": "design",
        "className": "LRUKCache",
        "ctor_params": [("capacity", "int"), ("k", "int")],
        "methods": [
            {"name": "get", "params": [("key", "int")], "ret": "int"},
            {"name": "put", "params": [("key", "int"), ("value", "int")], "ret": "void"},
        ],
        "py_full": """from collections import deque
import heapq


class LRUKCache:
    def __init__(self, capacity: int, k: int):
        self.cap = capacity
        self.k = k
        self.tick = 0
        self.seq = 0
        self.vals: dict[int, int] = {}
        self.hist: dict[int, deque[int]] = {}
        self.ver: dict[int, int] = {}
        self.heap: list[tuple[int, int, int, int]] = []

    def _record_access(self, key: int) -> None:
        self.tick += 1
        dq = self.hist[key]
        dq.append(self.tick)
        if len(dq) > self.k:
            dq.popleft()
        self.seq += 1
        self.ver[key] = self.seq
        tier = 0 if len(dq) < self.k else 1
        heapq.heappush(self.heap, (tier, dq[0], self.seq, key))

    def get(self, key: int) -> int:
        if key not in self.vals:
            return -1
        self._record_access(key)
        return self.vals[key]

    def put(self, key: int, value: int) -> None:
        if key in self.vals:
            self.vals[key] = value
            self._record_access(key)
            return
        if len(self.vals) == self.cap:
            while self.heap:
                _, _, v, cand = heapq.heappop(self.heap)
                if cand in self.vals and self.ver[cand] == v:
                    del self.vals[cand]
                    del self.hist[cand]
                    del self.ver[cand]
                    break
        self.vals[key] = value
        self.hist[key] = deque()
        self._record_access(key)
""",
        "java_full": """class LRUKCache {
    private static class Entry {
        int tier;
        int refTick;
        int ver;
        int key;

        Entry(int tier, int refTick, int ver, int key) {
            this.tier = tier;
            this.refTick = refTick;
            this.ver = ver;
            this.key = key;
        }
    }

    private final int cap;
    private final int k;
    private int tick = 0;
    private int seq = 0;
    private final Map<Integer, Integer> vals = new HashMap<>();
    private final Map<Integer, Deque<Integer>> hist = new HashMap<>();
    private final Map<Integer, Integer> ver = new HashMap<>();
    private final PriorityQueue<Entry> pq = new PriorityQueue<>((a, b) -> {
        if (a.tier != b.tier) return Integer.compare(a.tier, b.tier);
        if (a.refTick != b.refTick) return Integer.compare(a.refTick, b.refTick);
        return Integer.compare(a.ver, b.ver);
    });

    public LRUKCache(int capacity, int k) {
        this.cap = capacity;
        this.k = k;
    }

    private void recordAccess(int key) {
        tick++;
        Deque<Integer> dq = hist.get(key);
        dq.addLast(tick);
        if (dq.size() > k) {
            dq.removeFirst();
        }
        seq++;
        ver.put(key, seq);
        int tier = dq.size() < k ? 0 : 1;
        pq.offer(new Entry(tier, dq.peekFirst(), seq, key));
    }

    public int get(int key) {
        Integer val = vals.get(key);
        if (val == null) {
            return -1;
        }
        recordAccess(key);
        return val;
    }

    public void put(int key, int value) {
        if (vals.containsKey(key)) {
            vals.put(key, value);
            recordAccess(key);
            return;
        }
        if (vals.size() == cap) {
            while (!pq.isEmpty()) {
                Entry e = pq.poll();
                Integer curVer = ver.get(e.key);
                if (curVer != null && curVer == e.ver) {
                    vals.remove(e.key);
                    hist.remove(e.key);
                    ver.remove(e.key);
                    break;
                }
            }
        }
        vals.put(key, value);
        hist.put(key, new ArrayDeque<>());
        recordAccess(key);
    }
}
""",
        "visible": [
            {
                "ops": ["LRUKCache", "put", "put", "get", "put", "get", "get", "put", "get", "get"],
                "args": [[2, 2], [1, 10], [2, 20], [1], [3, 30], [2], [3], [4, 40], [1], [3]],
            },
            {
                "ops": ["LRUKCache", "put", "put", "get", "put", "get", "get", "get"],
                "args": [[2, 1], [1, 10], [2, 20], [1], [3, 30], [2], [1], [3]],
            },
            {
                "ops": ["LRUKCache", "put", "put", "put", "put", "get", "get", "get"],
                "args": [[2, 2], [1, 10], [2, 20], [1, 15], [3, 30], [2], [1], [3]],
            },
        ],
        "hidden_fn": "gen_hidden_100",
    },
])


# =============================================================================
# Hidden Test Generators for Design Problems (95-100)
# =============================================================================


def gen_hidden_95() -> list[dict]:
    tests = [
        {"ops": ["PinnedLRUCache", "get", "put", "pin", "put", "get"], "args": [[1], [1], [1, 10], [1], [2, 20], [1]]},
        {"ops": ["PinnedLRUCache", "put", "pin", "pin", "unpin", "unpin", "put", "get"], "args": [[1], [1, 5], [1], [1], [1], [1], [2, 9], [1]]},
        {"ops": ["PinnedLRUCache", "put", "put", "put", "get", "get", "get"], "args": [[2], [1, 1], [2, 2], [3, 3], [1], [2], [3]]},
        {"ops": ["PinnedLRUCache", "put", "put", "pin", "get", "put", "get", "get"], "args": [[2], [1, 10], [2, 20], [1], [2], [3, 30], [1], [2]]},
        {"ops": ["PinnedLRUCache", "put", "put", "put", "pin", "pin", "put", "unpin", "put", "get", "get"], "args": [[3], [1, 1], [2, 2], [3, 3], [1], [2], [4, 4], [1], [5, 5], [3], [4]]},
        {"ops": ["PinnedLRUCache", "put", "put", "pin", "pin", "put", "get", "unpin", "put", "get", "get"], "args": [[2], [10, 100], [20, 200], [10], [20], [30, 300], [30], [20], [30, 300], [20], [30]]},
        {"ops": ["PinnedLRUCache", "put", "put", "put", "pin", "get", "get", "put", "get", "get"], "args": [[3], [1, 1], [2, 2], [3, 3], [2], [1], [2], [4, 4], [3], [2]]},
    ]
    for seed, cap, count, key_hi in [(9501, 6, 120, 12), (9502, 50, 700, 90)]:
        rng = random.Random(seed)
        ops = ["PinnedLRUCache"]
        args = [[cap]]
        for _ in range(count):
            r = rng.random()
            k = rng.randint(1, key_hi)
            if r < 0.35:
                ops.append("put")
                args.append([k, rng.randint(0, 10000)])
            elif r < 0.65:
                ops.append("get")
                args.append([k])
            elif r < 0.82:
                ops.append("pin")
                args.append([k])
            else:
                ops.append("unpin")
                args.append([k])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_96() -> list[dict]:
    tests = [
        {"ops": ["WeightedLRUCache", "currentWeight", "get", "put", "currentWeight"], "args": [[5], [], [1], [1, 10, 6], []]},
        {"ops": ["WeightedLRUCache", "put", "get", "currentWeight"], "args": [[5], [1, 10, 5], [1], []]},
        {"ops": ["WeightedLRUCache", "put", "put", "put", "get", "get", "get", "currentWeight"], "args": [[6], [1, 1, 2], [2, 2, 2], [3, 3, 2], [1], [2], [3], []]},
        {"ops": ["WeightedLRUCache", "put", "put", "put", "get", "put", "get", "get", "currentWeight"], "args": [[6], [1, 1, 2], [2, 2, 2], [3, 3, 2], [1], [4, 4, 4], [2], [3], []]},
        {"ops": ["WeightedLRUCache", "put", "put", "put", "get", "get", "currentWeight"], "args": [[10], [1, 10, 3], [2, 20, 7], [1, 11, 8], [2], [1], []]},
        {"ops": ["WeightedLRUCache", "put", "put", "put", "put", "currentWeight", "get", "get"], "args": [[10], [1, 1, 1], [2, 2, 1], [3, 3, 1], [4, 4, 10], [], [3], [4]]},
        {"ops": ["WeightedLRUCache", "put", "put", "put", "get", "currentWeight"], "args": [[10], [1, 10, 5], [1, 20, 11], [1, 30, 5], [1], []]},
    ]
    for seed, max_w, count, key_hi in [(9601, 25, 120, 15), (9602, 200, 700, 100)]:
        rng = random.Random(seed)
        ops = ["WeightedLRUCache"]
        args = [[max_w]]
        for _ in range(count):
            r = rng.random()
            k = rng.randint(1, key_hi)
            if r < 0.5:
                ops.append("put")
                args.append([k, rng.randint(0, 10000), rng.randint(1, max_w + 5)])
            elif r < 0.85:
                ops.append("get")
                args.append([k])
            else:
                ops.append("currentWeight")
                args.append([])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_97() -> list[dict]:
    tests = [
        {"ops": ["SLRUCache", "get", "segmentOf", "put", "segmentOf", "get", "segmentOf"], "args": [[1, 1], [5], [5], [5, 50], [5], [5], [5]]},
        {"ops": ["SLRUCache", "put", "put", "get", "get", "segmentOf", "segmentOf"], "args": [[1, 1], [1, 10], [2, 20], [1], [2], [1], [2]]},
        {"ops": ["SLRUCache", "put", "get", "put", "get", "put", "get", "segmentOf", "segmentOf", "segmentOf"], "args": [[1, 1], [1, 10], [1], [2, 20], [2], [3, 30], [1], [1], [2], [3]]},
        {"ops": ["SLRUCache", "put", "put", "put", "segmentOf", "segmentOf", "segmentOf"], "args": [[2, 2], [1, 1], [2, 2], [3, 3], [1], [2], [3]]},
        {"ops": ["SLRUCache", "put", "put", "get", "get", "get", "put", "get", "segmentOf", "segmentOf", "segmentOf"], "args": [[2, 2], [1, 1], [2, 2], [1], [2], [1], [3, 3], [3], [1], [2], [3]]},
        {"ops": ["SLRUCache", "put", "get", "put", "get", "segmentOf"], "args": [[2, 2], [1, 10], [1], [1, 99], [1], [1]]},
        {"ops": ["SLRUCache", "put", "put", "get", "put", "get", "put", "put", "segmentOf", "segmentOf", "segmentOf", "segmentOf"], "args": [[2, 1], [1, 1], [2, 2], [1], [3, 3], [2], [4, 4], [5, 5], [1], [2], [3], [4]]},
    ]
    for seed, p1, p2, count, key_hi in [(9701, 4, 4, 120, 14), (9702, 25, 35, 700, 100)]:
        rng = random.Random(seed)
        ops = ["SLRUCache"]
        args = [[p1, p2]]
        for _ in range(count):
            r = rng.random()
            k = rng.randint(1, key_hi)
            if r < 0.45:
                ops.append("put")
                args.append([k, rng.randint(0, 10000)])
            elif r < 0.8:
                ops.append("get")
                args.append([k])
            else:
                ops.append("segmentOf")
                args.append([k])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_98() -> list[dict]:
    tests = [
        {"ops": ["RemovableQueue", "enqueue", "cancel", "peekFront", "dequeue", "size"], "args": [[], [1], [1], [], [], []]},
        {"ops": ["RemovableQueue", "enqueue", "enqueue", "cancel", "peekFront", "dequeue"], "args": [[], [1], [2], [1], [], []]},
        {"ops": ["RemovableQueue", "enqueue", "enqueue", "cancel", "peekFront", "dequeue", "dequeue"], "args": [[], [1], [2], [2], [], [], []]},
        {"ops": ["RemovableQueue", "enqueue", "cancel", "cancel", "enqueue", "dequeue"], "args": [[], [42], [42], [42], [42], []]},
        {"ops": ["RemovableQueue", "enqueue", "enqueue", "enqueue", "enqueue", "cancel", "cancel", "size", "dequeue", "dequeue"], "args": [[], [1], [2], [3], [4], [2], [3], [], [], []]},
        {"ops": ["RemovableQueue", "enqueue", "enqueue", "dequeue", "cancel", "size", "peekFront"], "args": [[], [10], [20], [], [10], [], []]},
        {"ops": ["RemovableQueue", "enqueue", "enqueue", "enqueue", "dequeue", "enqueue", "cancel", "dequeue", "dequeue"], "args": [[], [1], [2], [3], [], [1], [2], [], []]},
    ]
    for seed, count, key_hi in [(9801, 140, 20), (9802, 800, 120)]:
        rng = random.Random(seed)
        ops = ["RemovableQueue"]
        args = [[]]
        for _ in range(count):
            r = rng.random()
            if r < 0.42:
                ops.append("enqueue")
                args.append([rng.randint(0, key_hi)])
            elif r < 0.65:
                ops.append("dequeue")
                args.append([])
            elif r < 0.85:
                ops.append("cancel")
                args.append([rng.randint(0, key_hi)])
            elif r < 0.93:
                ops.append("peekFront")
                args.append([])
            else:
                ops.append("size")
                args.append([])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_99() -> list[dict]:
    tests = [
        {"ops": ["ClockCache", "get", "put", "get"], "args": [[1], [1], [1, 10], [1]]},
        {"ops": ["ClockCache", "put", "put", "get", "get"], "args": [[2], [1, 10], [1, 20], [1], [2]]},
        {"ops": ["ClockCache", "put", "put", "put", "put", "get", "get", "get", "get"], "args": [[3], [1, 1], [2, 2], [3, 3], [4, 4], [1], [2], [3], [4]]},
        {"ops": ["ClockCache", "put", "put", "put", "put", "get", "put", "get", "get", "get"], "args": [[3], [1, 1], [2, 2], [3, 3], [4, 4], [2], [5, 5], [2], [3], [5]]},
        {"ops": ["ClockCache", "put", "put", "put", "put", "put", "get", "get", "get"], "args": [[2], [1, 1], [2, 2], [3, 3], [2, 22], [4, 4], [2], [3], [4]]},
        {"ops": ["ClockCache", "put", "put", "put", "get", "get", "put", "put", "get", "get", "get"], "args": [[3], [10, 1], [20, 2], [30, 3], [10], [20], [40, 4], [50, 5], [10], [20], [30]]},
        {"ops": ["ClockCache", "put", "put", "put", "put", "put", "put", "get", "get", "get", "get"], "args": [[4], [1, 1], [2, 2], [3, 3], [4, 4], [5, 5], [6, 6], [1], [2], [3], [6]]},
    ]
    for seed, cap, count, key_hi in [(9901, 6, 140, 15), (9902, 40, 800, 90)]:
        rng = random.Random(seed)
        ops = ["ClockCache"]
        args = [[cap]]
        for _ in range(count):
            k = rng.randint(1, key_hi)
            if rng.random() < 0.52:
                ops.append("put")
                args.append([k, rng.randint(0, 10000)])
            else:
                ops.append("get")
                args.append([k])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_100() -> list[dict]:
    tests = [
        {"ops": ["LRUKCache", "get", "put", "get", "put", "get", "get"], "args": [[1, 2], [1], [1, 10], [1], [2, 20], [1], [2]]},
        {"ops": ["LRUKCache", "put", "put", "put", "get", "get", "get"], "args": [[2, 3], [1, 1], [2, 2], [3, 3], [1], [2], [3]]},
        {"ops": ["LRUKCache", "put", "put", "get", "get", "put", "get", "get", "get"], "args": [[2, 3], [1, 1], [2, 2], [1], [1], [3, 3], [1], [2], [3]]},
        {"ops": ["LRUKCache", "put", "put", "get", "put", "get", "put", "get", "get"], "args": [[2, 2], [1, 1], [2, 2], [2], [3, 3], [1], [1, 100], [1], [2]]},
        {"ops": ["LRUKCache", "put", "put", "put", "get", "get", "get", "put", "get", "get", "get"], "args": [[3, 2], [1, 1], [2, 2], [3, 3], [3], [2], [1], [4, 4], [1], [2], [3]]},
        {"ops": ["LRUKCache", "put", "put", "get", "get", "get", "put", "get", "put", "get", "get"], "args": [[2, 2], [1, 10], [2, 20], [1], [2], [1], [3, 30], [2], [4, 40], [1], [3]]},
        {"ops": ["LRUKCache", "put", "put", "get", "get", "get", "put", "get", "get"], "args": [[2, 4], [1, 1], [2, 2], [1], [1], [2], [3, 3], [1], [2]]},
    ]
    for seed, cap, k, count, key_hi in [(10001, 5, 2, 140, 12), (10002, 30, 3, 750, 70)]:
        rng = random.Random(seed)
        ops = ["LRUKCache"]
        args = [[cap, k]]
        for _ in range(count):
            key = rng.randint(1, key_hi)
            if rng.random() < 0.5:
                ops.append("put")
                args.append([key, rng.randint(0, 10000)])
            else:
                ops.append("get")
                args.append([key])
        tests.append({"ops": ops, "args": args})
    return tests


HIDDEN_GENERATORS = {
    "gen_hidden_95": gen_hidden_95,
    "gen_hidden_96": gen_hidden_96,
    "gen_hidden_97": gen_hidden_97,
    "gen_hidden_98": gen_hidden_98,
    "gen_hidden_99": gen_hidden_99,
    "gen_hidden_100": gen_hidden_100,
}


def main():
    assert len(TASKS) == 24, f"Expected 24 tasks, got {len(TASKS)}"
    expected_nums = list(range(77, 101))
    actual_nums = [int(p["slug"].split("-", 1)[0]) for p in TASKS]
    assert actual_nums == expected_nums, f"Prefix mismatch: {actual_nums} != {expected_nums}"

    target_folders = {BASE / p["slug"] for p in TASKS}

    existing_slugs = set()
    existing_titles = set()
    for p in (ROOT / "problems").rglob("problem.json"):
        if p.parent in target_folders:
            continue
        m = re.match(r"^(\d{2,3})-(.+)$", p.parent.name)
        if m:
            existing_slugs.add(m.group(2))
        meta = json.loads(p.read_text(encoding="utf-8"))
        existing_titles.add(meta["title"].lower())

    batch_slugs = set()
    batch_titles = set()
    for p in TASKS:
        assert p["subtopic"] in ALLOWED_SUBTOPICS, f"Invalid subtopic: {p['subtopic']}"
        slug_only = p["slug"].split("-", 1)[1]
        assert slug_only not in existing_slugs, f"Global duplicate slug: {slug_only}"
        assert p["title"].lower() not in existing_titles, f"Global duplicate title: {p['title']}"
        assert slug_only not in batch_slugs, f"Batch duplicate slug: {slug_only}"
        assert p["title"].lower() not in batch_titles, f"Batch duplicate title: {p['title']}"
        batch_slugs.add(slug_only)
        batch_titles.add(p["title"].lower())

    for p in TASKS:
        folder = BASE / p["slug"]
        folder.mkdir(parents=True, exist_ok=True)

        if p["kind"] == "function":
            sig = {
                "kind": "function",
                "method": p["method"],
                "params": [{"name": n, "type": t} for n, t in p["params"]],
                "returns": p["ret"],
            }
        else:
            sig = {
                "kind": "design",
                "className": p["className"],
                "constructor": {
                    "params": [{"name": n, "type": t} for n, t in p["ctor_params"]],
                },
                "methods": [
                    {
                        "name": m["name"],
                        "params": [{"name": n, "type": t} for n, t in m["params"]],
                        "returns": m["ret"],
                    }
                    for m in p["methods"]
                ],
            }

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

        if "py_full" in p:
            py_src = p["py_full"].rstrip() + "\n"
        else:
            pyparams = "".join(f", {n}: {py_type(t)}" for n, t in p["params"])
            py_src = (
                f"class Solution:\n"
                f"    def {p['method']}(self{pyparams}) -> {py_type(p['ret'])}:\n"
                + p["py"]
                + "\n"
            )
        (folder / "solution.py").write_text(py_src, encoding="utf-8")

        if "java_full" in p:
            java_src = p["java_full"].rstrip() + "\n"
        else:
            jparams = ", ".join(f"{t} {n}" for n, t in p["params"])
            java_src = (
                f"class Solution {{\n"
                f"    public {p['ret']} {p['method']}({jparams}) {{\n"
                + p["java"]
                + "\n    }\n}\n"
            )
        (folder / "Solution.java").write_text(java_src, encoding="utf-8")

        vis_list = [{"in": x} for x in p["visible"]]
        hid_raw = HIDDEN_GENERATORS[p["hidden_fn"]]() if "hidden_fn" in p else p["hidden"]
        hid_list = [{"in": x} for x in hid_raw]
        assert len(vis_list) == 3, f"{p['slug']}: expected 3 visible tests, got {len(vis_list)}"
        assert len(hid_list) == 9, f"{p['slug']}: expected 9 hidden tests, got {len(hid_list)}"

        (folder / "tests.py").write_text(
            f"def visible():\n    return {repr(vis_list)}\n\ndef hidden():\n    return {repr(hid_list)}\n",
            encoding="utf-8",
        )

    print(f"Generated {len(TASKS)} linked-lists problems (77-100)")


if __name__ == "__main__":
    main()
