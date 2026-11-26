#!/usr/bin/env python3
"""Generate linked-lists problems 47-76 (batch 2) for AlgoPlay."""
from __future__ import annotations

import json
import random
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "linked-lists"


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


def make_unique_sorted_list(seed: int, n: int, step_max: int = 5, start: int = -500) -> list[int]:
    rng = random.Random(seed)
    out = []
    cur = start
    for _ in range(n):
        cur += rng.randint(1, step_max)
        out.append(cur)
    return out


def make_zero_delimited_list(seed: int, groups: int, max_len: int = 5, hi: int = 100) -> list[int]:
    rng = random.Random(seed)
    out = [0]
    for _ in range(groups):
        glen = rng.randint(1, max_len)
        for _ in range(glen):
            out.append(rng.randint(1, hi))
        out.append(0)
    return out


def make_k_sorted_list(seed: int, n: int, k: int) -> list[int]:
    rng = random.Random(seed)
    base = sorted(rng.randint(-5000, 5000) for _ in range(n))
    # Shuffle within disjoint blocks of size k+1 so every element moves at most k steps
    out = list(base)
    step = k + 1
    for i in range(0, n, step):
        chunk = out[i : i + step]
        rng.shuffle(chunk)
        out[i : i + step] = chunk
    return out


def make_bitonic_list(seed: int, inc_len: int, dec_len: int) -> list[int]:
    rng = random.Random(seed)
    inc = sorted(rng.randint(-10000, 10000) for _ in range(inc_len))
    peak = inc[-1] if inc else 10000
    dec = sorted((rng.randint(-10000, peak) for _ in range(dec_len)), reverse=True)
    return inc + dec


def make_perm_list(seed: int, n: int) -> list[int]:
    rng = random.Random(seed)
    arr = list(range(n))
    rng.shuffle(arr)
    return arr


def make_subset(seed: int, n: int, m: int) -> list[int]:
    rng = random.Random(seed)
    return rng.sample(range(n), m)


def make_digits_list(seed: int, n: int) -> list[int]:
    rng = random.Random(seed)
    return [rng.randint(1, 9)] + [rng.randint(0, 9) for _ in range(n - 1)]


TASKS: list[dict] = [
    # -------------------------------------------------------------------------
    # 47-52: Pointers & Nodes
    # -------------------------------------------------------------------------
    {
        "slug": "47-split-linked-list-in-parts",
        "title": "Split Linked List in Parts",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Google", "Oracle", "Microsoft"],
        "desc": (
            "Given the `head` of a singly linked list and an integer `k`, split the linked list into `k` consecutive "
            "linked list parts.\n\n"
            "The length of each part should be as equal as possible: no two parts should have a size differing by more "
            "than one, and earlier parts must have a size greater than or equal to later parts. Parts that contain zero "
            "nodes should be represented as `null` (`None` in Python).\n\n"
            "Return an array of length `k` containing the heads of the `k` parts in order."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 1000].",
            "0 <= Node.val <= 1000",
            "1 <= k <= 50",
        ],
        "hints": [
            "First count the total number of nodes `n`. Each part gets `n // k` nodes, and the first `n % k` parts each get one extra node.",
            "Walk through the list cutting each part's tail (`tail.next = null`) before advancing to the start of the next part.",
        ],
        "explanations": [
            "3 nodes split into 5 parts gives lengths [1, 1, 1, 0, 0], so the last two parts are empty.",
            "10 nodes split into 3 parts gives lengths [4, 3, 3]: [1,2,3,4], [5,6,7], [8,9,10].",
            "An empty list split into 3 parts produces three empty parts.",
        ],
        "time": "O(n + k)",
        "space": "O(k)",
        "kind": "function",
        "method": "splitListToParts",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode[]",
        "py": """        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next
        base, rem = divmod(n, k)
        res: List[Optional[ListNode]] = [None] * k
        curr = head
        for i in range(k):
            part_len = base + (1 if i < rem else 0)
            if part_len == 0 or curr is None:
                continue
            res[i] = curr
            for _ in range(part_len - 1):
                curr = curr.next
            nxt = curr.next
            curr.next = None
            curr = nxt
        return res""",
        "java": """        int n = 0;
        ListNode curr = head;
        while (curr != null) {
            n++;
            curr = curr.next;
        }
        int base = n / k;
        int rem = n % k;
        ListNode[] res = new ListNode[k];
        curr = head;
        for (int i = 0; i < k; i++) {
            int partLen = base + (i < rem ? 1 : 0);
            if (partLen == 0 || curr == null) {
                continue;
            }
            res[i] = curr;
            for (int j = 0; j < partLen - 1; j++) {
                curr = curr.next;
            }
            ListNode nxt = curr.next;
            curr.next = null;
            curr = nxt;
        }
        return res;""",
        "visible": [
            {"head": [1, 2, 3], "k": 5},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "k": 3},
            {"head": [], "k": 3},
        ],
        "hidden": [
            {"head": [42], "k": 1},
            {"head": [42], "k": 4},
            {"head": [1, 2, 3, 4], "k": 2},
            {"head": [1, 2, 3, 4], "k": 4},
            {"head": [1, 2, 3, 4, 5, 6, 7], "k": 1},
            {"head": [1, 2, 3, 4, 5, 6, 7], "k": 3},
            {"head": [9, 8, 7, 6, 5], "k": 7},
            {"head": make_rng_list(4701, 53, 0, 1000), "k": 10},
            {"head": make_rng_list(4702, 1000, 0, 1000), "k": 37},
        ],
    },
    {
        "slug": "48-merge-nodes-in-between-zeros",
        "title": "Merge Nodes in Between Zeros",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Microsoft", "Meta", "Bloomberg"],
        "desc": (
            "You are given the `head` of a singly linked list containing a series of integers separated by `0`s. "
            "Both the beginning and end of the linked list have `Node.val == 0`, and there are no two consecutive "
            "nodes with `Node.val == 0`.\n\n"
            "For every two consecutive `0`s, merge all nodes strictly between them into a single node whose value is "
            "the sum of all the merged nodes. The modified list must not contain any `0`s.\n\n"
            "Return the head of the modified linked list."
        ),
        "cons": [
            "The number of nodes in the list is in the range [3, 2 * 10^4].",
            "0 <= Node.val <= 1000",
            "There are no two consecutive nodes with Node.val == 0.",
            "The first and last nodes both have Node.val == 0.",
        ],
        "hints": [
            "Reuse existing nodes in-place by maintaining a `write` pointer for the output list and a `read` pointer scanning segments between zeros.",
            "Whenever `read.val == 0`, store the accumulated segment sum into `write.val`, and if more segments remain (`read.next != null`), advance `write` to `write.next`; otherwise terminate with `write.next = null`.",
        ],
        "explanations": [
            "Between the first two zeros is [3, 1] summing to 4; between the next two is [4, 5, 2] summing to 11.",
            "Segments [1], [3], and [2, 2] sum to 1, 3, and 4 respectively.",
            "Only one segment [7] lies between the two bounding zeros, producing [7].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "mergeNodes",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        write = head
        read = head.next
        acc = 0
        while read is not None:
            if read.val == 0:
                write.val = acc
                acc = 0
                if read.next is not None:
                    write = write.next
                else:
                    write.next = None
            else:
                acc += read.val
            read = read.next
        return head""",
        "java": """        ListNode write = head;
        ListNode read = head.next;
        int acc = 0;
        while (read != null) {
            if (read.val == 0) {
                write.val = acc;
                acc = 0;
                if (read.next != null) {
                    write = write.next;
                } else {
                    write.next = null;
                }
            } else {
                acc += read.val;
            }
            read = read.next;
        }
        return head;""",
        "visible": [
            {"head": [0, 3, 1, 0, 4, 5, 2, 0]},
            {"head": [0, 1, 0, 3, 0, 2, 2, 0]},
            {"head": [0, 7, 0]},
        ],
        "hidden": [
            {"head": [0, 1000, 0]},
            {"head": [0, 1, 2, 3, 4, 5, 0]},
            {"head": [0, 1, 0, 1, 0, 1, 0, 1, 0]},
            {"head": [0, 1000, 1000, 1000, 0, 500, 500, 0]},
            {"head": [0, 9, 8, 0, 7, 0, 6, 5, 4, 0, 3, 2, 1, 0]},
            {"head": [0, 10, 20, 0, 30, 40, 0]},
            {"head": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0]},
            {"head": make_zero_delimited_list(4801, 40, 4, 500)},
            {"head": make_zero_delimited_list(4802, 500, 5, 1000)},
        ],
    },
    {
        "slug": "49-insert-gcd-nodes-in-linked-list",
        "title": "Insert GCD Nodes in Linked List",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Google", "Amazon", "Apple", "Adobe"],
        "desc": (
            "Given the `head` of a singly linked list in which each node contains a positive integer value, insert a "
            "new node between every pair of adjacent nodes whose value is equal to the greatest common divisor (GCD) "
            "of the two adjacent nodes.\n\n"
            "Return the head of the modified linked list after all insertions. If the list contains only one node, "
            "return it unchanged."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 5000].",
            "1 <= Node.val <= 10^4",
        ],
        "hints": [
            "Traverse with pointer `curr`; while `curr.next != null`, compute `g = gcd(curr.val, curr.next.val)` using the Euclidean algorithm.",
            "Insert `newNode = ListNode(g, curr.next)` right after `curr`, then advance `curr` directly to `newNode.next` so you do not process the newly inserted node as an original endpoint.",
        ],
        "explanations": [
            "gcd(18, 6)=6, gcd(6, 10)=2, and gcd(10, 3)=1 are inserted between consecutive pairs.",
            "A single-node list has no adjacent pairs, so [7] remains [7].",
            "Adjacent pairs (12, 18) and (18, 24) yield GCDs 6 and 6.",
        ],
        "time": "O(n log(maxVal))",
        "space": "O(1)",
        "kind": "function",
        "method": "insertGreatestCommonDivisors",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py_full": """import math


class Solution:
    def insertGreatestCommonDivisors(self, head: Optional[ListNode]) -> Optional[ListNode]:
        curr = head
        while curr is not None and curr.next is not None:
            nxt = curr.next
            node = ListNode(math.gcd(curr.val, nxt.val), nxt)
            curr.next = node
            curr = nxt
        return head
""",
        "java_full": """class Solution {
    private int gcd(int a, int b) {
        while (b != 0) {
            int t = a % b;
            a = b;
            b = t;
        }
        return a;
    }

    public ListNode insertGreatestCommonDivisors(ListNode head) {
        ListNode curr = head;
        while (curr != null && curr.next != null) {
            ListNode nxt = curr.next;
            ListNode node = new ListNode(gcd(curr.val, nxt.val), nxt);
            curr.next = node;
            curr = nxt;
        }
        return head;
    }
}
""",
        "visible": [
            {"head": [18, 6, 10, 3]},
            {"head": [7]},
            {"head": [12, 18, 24]},
        ],
        "hidden": [
            {"head": [1, 1]},
            {"head": [13, 17, 19, 23]},
            {"head": [100, 100, 100]},
            {"head": [48, 36, 24, 12, 6]},
            {"head": [9999, 6666, 3333]},
            {"head": [10000, 9999]},
            {"head": [2, 4, 8, 16, 32, 64]},
            {"head": make_rng_list(4901, 50, 1, 500)},
            {"head": make_rng_list(4902, 1500, 1, 10000)},
        ],
    },
    {
        "slug": "50-remove-zero-sum-consecutive-nodes",
        "title": "Remove Zero Sum Consecutive Nodes",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Google", "Meta", "Uber"],
        "desc": (
            "Given the `head` of a singly linked list of integers, repeatedly delete consecutive sequences of nodes "
            "whose values sum to `0` until no non-empty consecutive zero-sum sequence remains.\n\n"
            "To guarantee a unique output when multiple zero-sum sequences overlap, process nodes from left to right "
            "and always remove the earliest-ending zero-sum sequence first (equivalently, starting from a sentinel node "
            "before `head` with prefix sum `0`, link every surviving node directly to the node immediately following "
            "the rightmost occurrence of that same prefix sum). Return the head of the resulting linked list."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 5000].",
            "-1000 <= Node.val <= 1000",
        ],
        "hints": [
            "Two nodes share the exact same running prefix sum if and only if the contiguous sublist strictly between them sums to 0.",
            "In a first pass from a sentinel dummy node, map each prefix sum to the last node achieving it; in a second pass, set `curr.next = last[prefix].next` to jump past all zero-sum segments in O(n) total time.",
        ],
        "explanations": [
            "The prefix [1, 2, -3] sums to 0 and is removed, leaving [3, 1].",
            "The subarray [3, -3] sums to 0 and is removed, leaving [1, 2, 4].",
            "The contiguous sequence [2, 3, -3, -2] sums to 0 and is removed, leaving [1].",
        ],
        "time": "O(n)",
        "space": "O(n)",
        "kind": "function",
        "method": "removeZeroSumSublists",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0, head)
        last: dict[int, ListNode] = {}
        prefix = 0
        curr: Optional[ListNode] = dummy
        while curr is not None:
            prefix += curr.val
            last[prefix] = curr
            curr = curr.next
        prefix = 0
        curr = dummy
        while curr is not None:
            prefix += curr.val
            curr.next = last[prefix].next
            curr = curr.next
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0, head);
        Map<Integer, ListNode> last = new HashMap<>();
        int prefix = 0;
        for (ListNode curr = dummy; curr != null; curr = curr.next) {
            prefix += curr.val;
            last.put(prefix, curr);
        }
        prefix = 0;
        for (ListNode curr = dummy; curr != null; curr = curr.next) {
            prefix += curr.val;
            curr.next = last.get(prefix).next;
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, -3, 3, 1]},
            {"head": [1, 2, 3, -3, 4]},
            {"head": [1, 2, 3, -3, -2]},
        ],
        "hidden": [
            {"head": []},
            {"head": [0]},
            {"head": [0, 0, 0]},
            {"head": [1, -1]},
            {"head": [2, -1, -1, 1, 1]},
            {"head": [1, 3, 2, -3, -2, 5, 5, -5, 1]},
            {"head": [5, -3, -4, 1, 6, -2, -5]},
            {"head": [1, 2, 3, 4, 5]},
            {"head": make_rng_list(5001, 1500, -15, 15)},
        ],
    },
    {
        "slug": "51-linked-list-components",
        "title": "Linked List Components",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Google", "Amazon", "Microsoft", "Meta"],
        "desc": (
            "You are given the `head` of a singly linked list containing unique integer values and an integer array "
            "`nums` that is a subset of the linked list values.\n\n"
            "Return the number of connected components in `nums`, where two values belong to the same connected "
            "component if they appear consecutively in the linked list."
        ),
        "cons": [
            "The number of nodes in the list is n, with 1 <= n <= 10^4.",
            "0 <= Node.val < n, and all values in the linked list are unique.",
            "1 <= nums.length <= n, all values in nums are unique, and every value in nums appears in the linked list.",
        ],
        "hints": [
            "Insert all elements of `nums` into a hash set for O(1) membership lookups.",
            "Walk the linked list once and increment the component counter whenever a node's value is in the set and either it is the tail or its successor's value is not in the set.",
        ],
        "explanations": [
            "Nodes 0 and 1 are adjacent (component 1), and 3 is isolated (component 2), giving 2 components.",
            "Nodes 0 and 1 form one component, and 3 and 4 form a second component.",
            "All nodes in the list are present in nums, forming 1 single connected component.",
        ],
        "time": "O(n)",
        "space": "O(m)",
        "kind": "function",
        "method": "numComponents",
        "params": [("head", "ListNode"), ("nums", "int[]")],
        "ret": "int",
        "py": """        present = set(nums)
        ans = 0
        curr = head
        while curr is not None:
            if curr.val in present and (curr.next is None or curr.next.val not in present):
                ans += 1
            curr = curr.next
        return ans""",
        "java": """        Set<Integer> present = new HashSet<>();
        for (int x : nums) {
            present.add(x);
        }
        int ans = 0;
        ListNode curr = head;
        while (curr != null) {
            if (present.contains(curr.val) && (curr.next == null || !present.contains(curr.next.val))) {
                ans++;
            }
            curr = curr.next;
        }
        return ans;""",
        "visible": [
            {"head": [0, 1, 2, 3], "nums": [0, 1, 3]},
            {"head": [0, 1, 2, 3, 4], "nums": [0, 3, 1, 4]},
            {"head": [2, 0, 1], "nums": [0, 1, 2]},
        ],
        "hidden": [
            {"head": [0], "nums": [0]},
            {"head": [0, 1, 2, 3, 4, 5], "nums": [0, 2, 4]},
            {"head": [0, 1, 2, 3, 4, 5], "nums": [1, 3, 5]},
            {"head": [3, 4, 0, 2, 1], "nums": [4]},
            {"head": [4, 3, 2, 1, 0], "nums": [0, 1, 2]},
            {"head": [1, 2, 0, 4, 3], "nums": [3, 4, 0, 2, 1]},
            {"head": [0, 1, 2, 3, 4, 5, 6, 7], "nums": [1, 2, 5, 6]},
            {"head": make_perm_list(5101, 200), "nums": make_subset(5102, 200, 95)},
            {"head": make_perm_list(5103, 2000), "nums": make_subset(5104, 2000, 1000)},
        ],
    },
    {
        "slug": "52-delete-nodes-present-in-array",
        "title": "Delete Nodes Present in Array",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Google", "Meta", "Apple"],
        "desc": (
            "You are given an array of integers `nums` and the `head` of a singly linked list. Remove all nodes from "
            "the linked list whose value appears in `nums`, preserving the relative order of all remaining nodes, "
            "and return the head of the modified linked list.\n\n"
            "If all nodes are removed or the list is empty, return `null` (`None` in Python)."
        ),
        "cons": [
            "1 <= nums.length <= 10^4",
            "1 <= nums[i] <= 10^5",
            "The number of nodes in the list is in the range [0, 10^4].",
            "1 <= Node.val <= 10^5",
        ],
        "hints": [
            "Convert `nums` into a hash set so checking whether a node must be deleted takes O(1) time.",
            "Use a sentinel dummy node before `head` and unlink `curr.next` whenever `curr.next.val` belongs to the forbidden set.",
        ],
        "explanations": [
            "Removing values 1, 2, and 3 leaves only [4, 5].",
            "Removing value 1 removes every second node, leaving [2, 2, 2].",
            "Value 5 does not occur in [1, 2, 3, 4], so the list is unchanged.",
        ],
        "time": "O(n + m)",
        "space": "O(m)",
        "kind": "function",
        "method": "modifiedList",
        "params": [("nums", "int[]"), ("head", "ListNode")],
        "ret": "ListNode",
        "py": """        ban = set(nums)
        dummy = ListNode(0, head)
        curr = dummy
        while curr.next is not None:
            if curr.next.val in ban:
                curr.next = curr.next.next
            else:
                curr = curr.next
        return dummy.next""",
        "java": """        Set<Integer> ban = new HashSet<>();
        for (int x : nums) {
            ban.add(x);
        }
        ListNode dummy = new ListNode(0, head);
        ListNode curr = dummy;
        while (curr.next != null) {
            if (ban.contains(curr.next.val)) {
                curr.next = curr.next.next;
            } else {
                curr = curr.next;
            }
        }
        return dummy.next;""",
        "visible": [
            {"nums": [1, 2, 3], "head": [1, 2, 3, 4, 5]},
            {"nums": [1], "head": [1, 2, 1, 2, 1, 2]},
            {"nums": [5], "head": [1, 2, 3, 4]},
        ],
        "hidden": [
            {"nums": [1, 2], "head": []},
            {"nums": [7], "head": [7]},
            {"nums": [7, 8, 9], "head": [7, 8, 9, 7, 8]},
            {"nums": [1, 5], "head": [1, 2, 3, 4, 5]},
            {"nums": [2, 2, 2, 4], "head": [2, 1, 4, 3, 2, 4]},
            {"nums": [100000], "head": [100000, 1, 100000]},
            {"nums": [10, 20, 30], "head": [5, 10, 15, 20, 25, 30, 35]},
            {"nums": make_rng_list(5201, 50, 1, 100), "head": make_rng_list(5202, 200, 1, 100)},
            {"nums": make_rng_list(5203, 1000, 1, 2000), "head": make_rng_list(5204, 2500, 1, 2000)},
        ],
    },
    # -------------------------------------------------------------------------
    # 53-58: Fast/Slow Pointer
    # -------------------------------------------------------------------------
    {
        "slug": "53-merge-in-between-linked-lists",
        "title": "Merge In Between Linked Lists",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Microsoft", "Meta", "Adobe"],
        "desc": (
            "You are given two singly linked lists `list1` and `list2`, along with two 0-indexed integers `a` and `b` "
            "satisfying `1 <= a <= b < length(list1) - 1`.\n\n"
            "Remove `list1`'s nodes from index `a` to index `b` inclusive, and splice `list2` in their place. "
            "Return the head of the resulting linked list."
        ),
        "cons": [
            "3 <= list1.length <= 10^4",
            "1 <= a <= b < list1.length - 1",
            "1 <= list2.length <= 10^4",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Use two pointers separated by an offset of `b - a + 2`: when the slow pointer stops at index `a - 1`, the fast pointer sits at index `b + 1`.",
            "Connect `prevA.next = list2`, walk to the tail of `list2`, and connect `tail2.next = afterB` in O(1) extra space.",
        ],
        "explanations": [
            "Nodes at indices 3 and 4 (values 3 and 4) are replaced by [1000000, 1000001, 1000002].",
            "Nodes at indices 2 through 5 are replaced by [100, 101, 102, 103, 104].",
            "Only index 1 (value 2) is replaced by [9].",
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "kind": "function",
        "method": "mergeInBetween",
        "params": [("list1", "ListNode"), ("a", "int"), ("b", "int"), ("list2", "ListNode")],
        "ret": "ListNode",
        "py": """        prev_a = list1
        for _ in range(a - 1):
            prev_a = prev_a.next
        after_b = prev_a
        for _ in range(b - a + 2):
            after_b = after_b.next
        prev_a.next = list2
        tail2 = list2
        while tail2.next is not None:
            tail2 = tail2.next
        tail2.next = after_b
        return list1""",
        "java": """        ListNode prevA = list1;
        for (int i = 0; i < a - 1; i++) {
            prevA = prevA.next;
        }
        ListNode afterB = prevA;
        for (int i = 0; i < b - a + 2; i++) {
            afterB = afterB.next;
        }
        prevA.next = list2;
        ListNode tail2 = list2;
        while (tail2.next != null) {
            tail2 = tail2.next;
        }
        tail2.next = afterB;
        return list1;""",
        "visible": [
            {"list1": [10, 1, 13, 6, 9, 5], "a": 3, "b": 4, "list2": [1000000, 1000001, 1000002]},
            {"list1": [0, 1, 2, 3, 4, 5, 6], "a": 2, "b": 5, "list2": [100, 101, 102, 103, 104]},
            {"list1": [1, 2, 3], "a": 1, "b": 1, "list2": [9]},
        ],
        "hidden": [
            {"list1": [1, 2, 3], "a": 1, "b": 1, "list2": [9, 8, 7]},
            {"list1": [1, 2, 3, 4, 5], "a": 1, "b": 3, "list2": [99]},
            {"list1": [1, 2, 3, 4, 5], "a": 2, "b": 2, "list2": [-1, -2]},
            {"list1": [1, 2, 3, 4, 5], "a": 3, "b": 3, "list2": [50, 60]},
            {"list1": [10, 20, 30, 40, 50, 60], "a": 1, "b": 4, "list2": [100, 200]},
            {"list1": [5, 4, 3, 2, 1], "a": 1, "b": 1, "list2": [0]},
            {"list1": [-5, -4, -3, -2, -1, 0], "a": 2, "b": 4, "list2": [7, 8, 9, 10]},
            {"list1": make_rng_list(5301, 100, -1000, 1000), "a": 17, "b": 63, "list2": make_rng_list(5302, 40, -1000, 1000)},
            {"list1": make_rng_list(5303, 1500, -10000, 10000), "a": 250, "b": 1200, "list2": make_rng_list(5304, 800, -10000, 10000)},
        ],
    },
    {
        "slug": "54-min-max-distance-between-critical-points",
        "title": "Min and Max Distance Between Critical Points",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Google", "Amazon", "Microsoft", "Bloomberg"],
        "desc": (
            "A critical point in a singly linked list is a node that is either a **local maximum** "
            "(`prev.val < curr.val > next.val`) or a **local minimum** (`prev.val > curr.val < next.val`). "
            "The first and last nodes cannot be critical points because they lack both neighbors.\n\n"
            "Given the `head` of a linked list, return an integer array of length 2 `[minDistance, maxDistance]` "
            "representing the minimum and maximum distances (difference in node positions) between any two distinct "
            "critical points. If there are fewer than two critical points, return `[-1, -1]`."
        ),
        "cons": [
            "The number of nodes in the list is in the range [2, 10^4].",
            "1 <= Node.val <= 10^5",
        ],
        "hints": [
            "Slide three consecutive pointers (`prev`, `curr`, `curr.next`) across the list in a single pass while tracking the current index.",
            "The maximum distance is always between the first and last critical points; the minimum distance is the smallest gap between any two consecutive critical points.",
        ],
        "explanations": [
            "The list [3, 1] has no interior nodes, hence 0 critical points and [-1, -1].",
            "Critical points are at indices 2 (val 1), 4 (val 5), and 5 (val 1), giving min distance 5-4=1 and max distance 5-2=3.",
            "Critical points are at indices 1 (val 3) and 4 (val 3), so both min and max distance are 4-1=3.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "nodesBetweenCriticalPoints",
        "params": [("head", "ListNode")],
        "ret": "int[]",
        "py": """        first_idx = -1
        prev_idx = -1
        min_dist = 10**9
        prev = head
        curr = head.next
        idx = 1
        while curr is not None and curr.next is not None:
            nxt = curr.next
            if (curr.val > prev.val and curr.val > nxt.val) or (curr.val < prev.val and curr.val < nxt.val):
                if first_idx == -1:
                    first_idx = idx
                else:
                    diff = idx - prev_idx
                    if diff < min_dist:
                        min_dist = diff
                prev_idx = idx
            prev = curr
            curr = nxt
            idx += 1
        if min_dist == 10**9:
            return [-1, -1]
        return [min_dist, prev_idx - first_idx]""",
        "java": """        int firstIdx = -1;
        int prevIdx = -1;
        int minDist = Integer.MAX_VALUE;
        ListNode prev = head;
        ListNode curr = head.next;
        int idx = 1;
        while (curr != null && curr.next != null) {
            ListNode nxt = curr.next;
            if ((curr.val > prev.val && curr.val > nxt.val) || (curr.val < prev.val && curr.val < nxt.val)) {
                if (firstIdx == -1) {
                    firstIdx = idx;
                } else {
                    minDist = Math.min(minDist, idx - prevIdx);
                }
                prevIdx = idx;
            }
            prev = curr;
            curr = nxt;
            idx++;
        }
        if (minDist == Integer.MAX_VALUE) {
            return new int[]{-1, -1};
        }
        return new int[]{minDist, prevIdx - firstIdx};""",
        "visible": [
            {"head": [3, 1]},
            {"head": [5, 3, 1, 2, 5, 1, 2]},
            {"head": [1, 3, 2, 2, 3, 2, 2, 2, 7]},
        ],
        "hidden": [
            {"head": [1, 2, 3, 4, 5]},
            {"head": [5, 4, 3, 2, 1]},
            {"head": [2, 2, 2, 2]},
            {"head": [1, 5, 1]},
            {"head": [1, 5, 1, 5]},
            {"head": [10, 2, 2, 10, 2, 10]},
            {"head": [1, 2, 1, 2, 1, 2, 1]},
            {"head": make_rng_list(5401, 100, 1, 100)},
            {"head": make_rng_list(5402, 2500, 1, 100000)},
        ],
    },
]

TASKS.extend([
    {
        "slug": "55-happy-number-cycle-check",
        "title": "Happy Number Cycle Check",
        "difficulty": "Easy",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Google", "Amazon", "Apple", "Uber", "Meta"],
        "desc": (
            "Starting with a positive integer `n`, repeatedly replace the number by the sum of the squares of its "
            "base-10 digits. This defines an implicit singly linked list of states where each integer points to its "
            "digit-square sum.\n\n"
            "Return `true` if this sequence eventually reaches `1` (making `n` a happy number), or `false` if it "
            "enters a cycle that never includes `1`. Solve in `O(1)` extra space using Floyd's fast and slow pointers."
        ),
        "cons": [
            "1 <= n <= 2^31 - 1",
        ],
        "hints": [
            "Treat the transition `next(x) = sum of squares of digits of x` as following a `.next` pointer in an implicit linked list.",
            "Advance `slow = next(slow)` by one step and `fast = next(next(fast))` by two steps; the loop terminates when `fast == 1` (happy) or `slow == fast` (cycle).",
        ],
        "explanations": [
            "19 -> 82 -> 68 -> 100 -> 1, reaching 1 so return true.",
            "2 -> 4 -> 16 -> 37 -> 58 -> 89 -> 145 -> 42 -> 20 -> 4 enters a cycle without 1, so return false.",
            "7 -> 49 -> 97 -> 130 -> 10 -> 1 reaches 1, so return true.",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "kind": "function",
        "method": "isHappy",
        "params": [("n", "int")],
        "ret": "boolean",
        "py_full": """class Solution:
    def isHappy(self, n: int) -> bool:
        def step(x: int) -> int:
            total = 0
            while x > 0:
                x, d = divmod(x, 10)
                total += d * d
            return total

        slow = n
        fast = step(n)
        while fast != 1 and slow != fast:
            slow = step(slow)
            fast = step(step(fast))
        return fast == 1
""",
        "java_full": """class Solution {
    private int step(int x) {
        int total = 0;
        while (x > 0) {
            int d = x % 10;
            total += d * d;
            x /= 10;
        }
        return total;
    }

    public boolean isHappy(int n) {
        int slow = n;
        int fast = step(n);
        while (fast != 1 && slow != fast) {
            slow = step(slow);
            fast = step(step(fast));
        }
        return fast == 1;
    }
}
""",
        "visible": [
            {"n": 19},
            {"n": 2},
            {"n": 7},
        ],
        "hidden": [
            {"n": 1},
            {"n": 4},
            {"n": 10},
            {"n": 1111111},
            {"n": 100},
            {"n": 999},
            {"n": 123456},
            {"n": 1000000000},
            {"n": 2147483647},
        ],
    },
    {
        "slug": "56-circular-array-loop-detection",
        "title": "Circular Array Loop Detection",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Google", "Meta", "Amazon", "Bloomberg"],
        "desc": (
            "You are given a circular array `nums` of non-zero integers representing an implicit linked list of length "
            "`n`, where index `i` points to index `((i + nums[i]) % n + n) % n`.\n\n"
            "Return `true` if there exists a cycle in `nums` such that:\n"
            "- Every step in the cycle moves in the **same direction** (either all `nums[idx] > 0` or all `nums[idx] < 0`), and\n"
            "- The cycle contains **more than one** distinct index (no self-loops of length 1).\n\n"
            "Otherwise, return `false`. Aim for `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "1 <= nums.length <= 5000",
            "-1000 <= nums[i] <= 1000",
            "nums[i] != 0",
        ],
        "hints": [
            "Run Floyd's fast and slow pointers from each unvisited starting index, stopping immediately if direction changes or a 1-step self-loop is encountered.",
            "To guarantee O(n) total time with O(1) extra space, whenever a search from index `i` fails to find a valid cycle, walk the same-direction path from `i` and zero out all visited cells so they are never explored again.",
        ],
        "explanations": [
            "Indices 0 -> 2 -> 3 -> 0 form a forward cycle of length 3 with all positive values.",
            "Every negative index jumps to index 5 (+6) causing a sign change, and index 5 jumps to itself (a length-1 self-loop), so no valid cycle exists.",
            "Indices 3 -> 4 -> 3 form a forward cycle of length 2 with all positive values.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "circularArrayLoop",
        "params": [("nums", "int[]")],
        "ret": "boolean",
        "py": """        n = len(nums)

        def next_idx(idx: int, forward: bool) -> int:
            if (nums[idx] > 0) != forward:
                return -1
            nxt = (idx + nums[idx]) % n
            if nxt == idx or (nums[nxt] > 0) != forward or nums[nxt] == 0:
                return -1
            return nxt

        for i in range(n):
            if nums[i] == 0:
                continue
            forward = nums[i] > 0
            slow = i
            fast = i
            while True:
                slow = next_idx(slow, forward)
                if slow == -1:
                    break
                fast = next_idx(fast, forward)
                if fast != -1:
                    fast = next_idx(fast, forward)
                if fast == -1:
                    break
                if slow == fast:
                    return True
            curr = i
            while nums[curr] != 0 and (nums[curr] > 0) == forward:
                nxt = (curr + nums[curr]) % n
                nums[curr] = 0
                curr = nxt
        return False""",
        "java_full": """class Solution {
    private int nextIdx(int[] nums, int idx, boolean forward) {
        int n = nums.length;
        if ((nums[idx] > 0) != forward) {
            return -1;
        }
        int nxt = ((idx + nums[idx]) % n + n) % n;
        if (nxt == idx || nums[nxt] == 0 || (nums[nxt] > 0) != forward) {
            return -1;
        }
        return nxt;
    }

    public boolean circularArrayLoop(int[] nums) {
        int n = nums.length;
        for (int i = 0; i < n; i++) {
            if (nums[i] == 0) {
                continue;
            }
            boolean forward = nums[i] > 0;
            int slow = i;
            int fast = i;
            while (true) {
                slow = nextIdx(nums, slow, forward);
                if (slow == -1) {
                    break;
                }
                fast = nextIdx(nums, fast, forward);
                if (fast != -1) {
                    fast = nextIdx(nums, fast, forward);
                }
                if (fast == -1) {
                    break;
                }
                if (slow == fast) {
                    return true;
                }
            }
            int curr = i;
            while (nums[curr] != 0 && (nums[curr] > 0) == forward) {
                int nxt = ((curr + nums[curr]) % n + n) % n;
                nums[curr] = 0;
                curr = nxt;
            }
        }
        return false;
    }
}
""",
        "visible": [
            {"nums": [2, -1, 1, 2, 2]},
            {"nums": [-1, -2, -3, -4, -5, 6]},
            {"nums": [1, -1, 5, 1, 4]},
        ],
        "hidden": [
            {"nums": [1]},
            {"nums": [-1, 2]},
            {"nums": [1, 1]},
            {"nums": [-1, -1]},
            {"nums": [2, 2, 2, 2, 2, 4, 7]},
            {"nums": [-2, 1, -1, -2, -2]},
            {"nums": [3, 1, 2]},
            {"nums": [1, 1, 1, 1, -4]},
            {"nums": [1] * 2499 + [-2499]},
        ],
    },
    {
        "slug": "57-linked-list-cycle-length",
        "title": "Linked List Cycle Length",
        "difficulty": "Easy",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Oracle"],
        "desc": (
            "You are given an implicit singly linked list of `n` nodes labeled `0` through `n - 1` represented by an "
            "integer array `next`, where `next[i]` is the index of node `i`'s successor (or `-1` if node `i` has no "
            "successor), together with a starting node index `start`.\n\n"
            "Starting from `start`, follow the `next` pointers. If the traversal enters a cycle, return the exact "
            "number of distinct nodes in that cycle (a self-loop `next[i] == i` has cycle length `1`). If the "
            "traversal reaches `-1` without entering a cycle, return `0`.\n\n"
            "Solve in `O(n)` time and `O(1)` extra space using Floyd's fast and slow pointers."
        ),
        "cons": [
            "1 <= next.length <= 10^4",
            "-1 <= next[i] < next.length",
            "0 <= start < next.length",
        ],
        "hints": [
            "Initialize `slow = start` and `fast = start`; advance `slow` by 1 step and `fast` by 2 steps until either `fast == -1` / `next[fast] == -1` (no cycle) or `slow == fast` (meeting point inside the cycle).",
            "Once `slow == fast`, keep `slow` fixed and walk another pointer step by step around the cycle until it returns to `slow`, counting the number of steps.",
        ],
        "explanations": [
            "Path from 0 is 0 -> 1 -> 2 -> 3 -> 1, so the cycle {1, 2, 3} has length 3.",
            "Path from 0 is 0 -> 1 -> 2 -> -1, which terminates with no cycle (length 0).",
            "Path from 0 is 0 -> 1 -> 2 -> 2, entering a self-loop at node 2 of length 1.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "cycleLength",
        "params": [("next", "int[]"), ("start", "int")],
        "ret": "int",
        "py": """        slow = start
        fast = start
        while fast != -1 and next[fast] != -1:
            slow = next[slow]
            fast = next[next[fast]]
            if slow == fast:
                length = 1
                curr = next[slow]
                while curr != slow:
                    curr = next[curr]
                    length += 1
                return length
        return 0""",
        "java": """        int slow = start;
        int fast = start;
        while (fast != -1 && next[fast] != -1) {
            slow = next[slow];
            fast = next[next[fast]];
            if (slow == fast) {
                int length = 1;
                int curr = next[slow];
                while (curr != slow) {
                    curr = next[curr];
                    length++;
                }
                return length;
            }
        }
        return 0;""",
        "visible": [
            {"next": [1, 2, 3, 1], "start": 0},
            {"next": [1, 2, -1], "start": 0},
            {"next": [1, 2, 2], "start": 0},
        ],
        "hidden": [
            {"next": [-1], "start": 0},
            {"next": [0], "start": 0},
            {"next": [1, 0, 3, 2], "start": 2},
            {"next": [1, 2, 3, 4, 0], "start": 3},
            {"next": [1, 2, 3, 4, -1], "start": 0},
            {"next": [1, 2, 3, 4, 5, 2], "start": 0},
            {"next": [2, 3, 4, 1, 5, 0], "start": 1},
            {"next": [i + 1 for i in range(499)] + [-1], "start": 0},
            {"next": [i + 1 for i in range(2999)] + [750], "start": 0},
        ],
    },
    {
        "slug": "58-subtract-second-half-from-first",
        "title": "Subtract Second Half From First",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Google", "Bloomberg", "Atlassian"],
        "desc": (
            "Given the `head` of a singly linked list of length `n`, modify the first `floor(n / 2)` nodes in-place "
            "so that for each 0-based index `0 <= i < floor(n / 2)`, the `i`-th node's value becomes "
            "`node[i].val - node[n - 1 - i].val`, where `node[n - 1 - i]` is its mirror node in the second half.\n\n"
            "Leave the middle node (when `n` is odd) and all nodes in the second half unchanged, and return the head "
            "of the modified list. Solve in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Use fast and slow pointers (`while fast.next and fast.next.next`) so `slow` stops at the last node before the strict second half (`slow.next` has length `floor(n / 2)`).",
            "Reverse `slow.next`, walk the first half and reversed second half in lockstep to subtract values, then reverse the second half back and re-attach it to `slow.next`.",
        ],
        "explanations": [
            "Pairs (10, 40) and (20, 30) update the first two nodes to 10-40=-30 and 20-30=-10, keeping [30, 40].",
            "First 2 nodes subtract mirror nodes [5, 4] giving [1-5, 2-4] = [-4, -2]; middle 3 and second half [4, 5] stay unchanged.",
            "With 1 node, floor(1/2) = 0 nodes change, so [7] stays [7].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "subtractSecondHalf",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py_full": """class Solution:
    def subtractSecondHalf(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head

        def reverse(node: Optional[ListNode]) -> Optional[ListNode]:
            prev = None
            curr = node
            while curr is not None:
                nxt = curr.next
                curr.next = prev
                prev = curr
                curr = nxt
            return prev

        slow = head
        fast = head
        while fast.next is not None and fast.next.next is not None:
            slow = slow.next
            fast = fast.next.next

        rev = reverse(slow.next)
        p1 = head
        p2 = rev
        while p2 is not None:
            p1.val -= p2.val
            p1 = p1.next
            p2 = p2.next
        slow.next = reverse(rev)
        return head
""",
        "java_full": """class Solution {
    private ListNode reverse(ListNode node) {
        ListNode prev = null;
        ListNode curr = node;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    public ListNode subtractSecondHalf(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode slow = head;
        ListNode fast = head;
        while (fast.next != null && fast.next.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode rev = reverse(slow.next);
        ListNode p1 = head;
        ListNode p2 = rev;
        while (p2 != null) {
            p1.val -= p2.val;
            p1 = p1.next;
            p2 = p2.next;
        }
        slow.next = reverse(rev);
        return head;
    }
}
""",
        "visible": [
            {"head": [10, 20, 30, 40]},
            {"head": [1, 2, 3, 4, 5]},
            {"head": [7]},
        ],
        "hidden": [
            {"head": []},
            {"head": [5, 2]},
            {"head": [3, 9, 3]},
            {"head": [-5, -2, 0, 2, 5]},
            {"head": [100, 100, 100, 100]},
            {"head": [1, 10, 100, 1000, 10000, 100000]},
            {"head": [8, 6, 4, 2, 1, 3, 5]},
            {"head": make_rng_list(5801, 101, -1000, 1000)},
            {"head": make_rng_list(5802, 2000, -100000, 100000)},
        ],
    },
    # -------------------------------------------------------------------------
    # 59-64: Reversal
    # -------------------------------------------------------------------------
    {
        "slug": "59-plus-one-linked-list",
        "title": "Plus One Linked List",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Google", "Amazon", "Meta", "Microsoft"],
        "desc": (
            "Given a non-negative integer represented as a non-empty singly linked list of decimal digits (with the "
            "**most significant digit** at `head` and no leading zeros except for the number `0` itself), add `1` "
            "to the integer and return the head of the resulting linked list.\n\n"
            "Aim for `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "0 <= Node.val <= 9",
            "The integer does not contain leading zeros except when it is 0 itself.",
        ],
        "hints": [
            "You can reverse the list, add 1 with carry propagation, and reverse back in O(n) time and O(1) space.",
            "Even better, attach a sentinel `0` node before `head` and find the rightmost node whose value is not `9`; increment that node by 1 and set every trailing `9` after it to `0`.",
        ],
        "explanations": [
            "123 + 1 = 124.",
            "999 + 1 = 1000, requiring a new leading 1 node.",
            "0 + 1 = 1.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "plusOne",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        sentinel = ListNode(0, head)
        not_nine = sentinel
        curr = head
        while curr is not None:
            if curr.val != 9:
                not_nine = curr
            curr = curr.next
        not_nine.val += 1
        curr = not_nine.next
        while curr is not None:
            curr.val = 0
            curr = curr.next
        return sentinel if sentinel.val == 1 else sentinel.next""",
        "java": """        ListNode sentinel = new ListNode(0, head);
        ListNode notNine = sentinel;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val != 9) {
                notNine = curr;
            }
            curr = curr.next;
        }
        notNine.val++;
        curr = notNine.next;
        while (curr != null) {
            curr.val = 0;
            curr = curr.next;
        }
        return sentinel.val == 1 ? sentinel : sentinel.next;""",
        "visible": [
            {"head": [1, 2, 3]},
            {"head": [9, 9, 9]},
            {"head": [0]},
        ],
        "hidden": [
            {"head": [9]},
            {"head": [8]},
            {"head": [1, 9]},
            {"head": [1, 0, 9, 9]},
            {"head": [9, 0, 9, 9]},
            {"head": [9, 9, 9, 9, 9, 9, 9]},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            {"head": [9] * 500},
            {"head": make_digits_list(5901, 2000) + [9] * 50},
        ],
    },
    {
        "slug": "60-double-a-number-represented-as-linked-list",
        "title": "Double a Number Represented as a Linked List",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Google", "Apple", "Salesforce"],
        "desc": (
            "You are given the `head` of a non-empty singly linked list representing a non-negative integer without "
            "leading zeros (except for the number `0` itself), with the **most significant digit** at `head`.\n\n"
            "Return the `head` of the linked list after doubling the represented integer. Aim for `O(n)` time and "
            "`O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "0 <= Node.val <= 9",
            "The number has no leading zeros except for 0 itself.",
        ],
        "hints": [
            "Reversing the list, doubling each digit with carry, and reversing back solves the problem in O(n) time and O(1) space.",
            "Alternatively, observe that doubling any digit `d` produces a carry of `1` into the left neighbor if and only if `d >= 5` (since `2*4 + 1 = 9 < 10`), enabling a single left-to-right pass.",
        ],
        "explanations": [
            "189 * 2 = 378.",
            "999 * 2 = 1998, prepending a new leading 1 node.",
            "0 * 2 = 0.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "doubleIt",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head.val >= 5:
            head = ListNode(0, head)
        curr = head
        while curr is not None:
            carry = 1 if (curr.next is not None and curr.next.val >= 5) else 0
            curr.val = (curr.val * 2) % 10 + carry
            curr = curr.next
        return head""",
        "java": """        if (head.val >= 5) {
            head = new ListNode(0, head);
        }
        ListNode curr = head;
        while (curr != null) {
            int carry = (curr.next != null && curr.next.val >= 5) ? 1 : 0;
            curr.val = (curr.val * 2) % 10 + carry;
            curr = curr.next;
        }
        return head;""",
        "visible": [
            {"head": [1, 8, 9]},
            {"head": [9, 9, 9]},
            {"head": [0]},
        ],
        "hidden": [
            {"head": [1]},
            {"head": [5]},
            {"head": [4, 9]},
            {"head": [5, 0, 0]},
            {"head": [4, 4, 4, 5]},
            {"head": [9, 0, 9, 0, 9]},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            {"head": [5] * 300},
            {"head": make_digits_list(6001, 2000)},
        ],
    },
    {
        "slug": "61-subtract-two-linked-list-numbers",
        "title": "Subtract Two Linked List Numbers",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Adobe"],
        "desc": (
            "You are given two non-empty singly linked lists `l1` and `l2` representing two non-negative integers "
            "with the **most significant digit** at the head of each list (neither number contains leading zeros "
            "except when representing `0` itself).\n\n"
            "Return a singly linked list representing the absolute difference `|num(l1) - num(l2)|` with the most "
            "significant digit at the head and no unnecessary leading zeros. If both numbers are equal, return a "
            "single node with value `0`."
        ),
        "cons": [
            "The number of nodes in each list is in the range [1, 10^4].",
            "0 <= Node.val <= 9",
            "Neither input list has leading zeros except for the single-node list [0].",
        ],
        "hints": [
            "First compare the magnitudes of `l1` and `l2` (longer list is larger; on equal lengths compare digit-by-digit from head) so you always subtract the smaller number from the larger one.",
            "Reverse both lists, perform schoolbook subtraction from least significant digit with a borrow flag, reverse the resulting list, and strip any leading zero nodes (leaving at least one node).",
        ],
        "explanations": [
            "100 - 12 = 88 (leading zero stripped).",
            "|45 - 123| = 78.",
            "500 - 500 = 0.",
        ],
        "time": "O(n + m)",
        "space": "O(max(n, m))",
        "kind": "function",
        "method": "subtractTwoNumbers",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "ListNode",
        "py_full": """class Solution:
    def subtractTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        def length(node: Optional[ListNode]) -> int:
            c = 0
            while node is not None:
                c += 1
                node = node.next
            return c

        def reverse(node: Optional[ListNode]) -> Optional[ListNode]:
            prev = None
            while node is not None:
                nxt = node.next
                node.next = prev
                prev = node
                node = nxt
            return prev

        n1, n2 = length(l1), length(l2)
        if n1 < n2:
            big, small = l2, l1
        elif n1 > n2:
            big, small = l1, l2
        else:
            p1, p2 = l1, l2
            while p1 is not None and p1.val == p2.val:
                p1 = p1.next
                p2 = p2.next
            if p1 is None:
                return ListNode(0)
            big, small = (l1, l2) if p1.val > p2.val else (l2, l1)

        r1 = reverse(big)
        r2 = reverse(small)
        borrow = 0
        res = None
        while r1 is not None:
            v2 = r2.val if r2 is not None else 0
            diff = r1.val - v2 - borrow
            if diff < 0:
                diff += 10
                borrow = 1
            else:
                borrow = 0
            res = ListNode(diff, res)
            r1 = r1.next
            if r2 is not None:
                r2 = r2.next

        while res is not None and res.val == 0 and res.next is not None:
            res = res.next
        return res
""",
        "java_full": """class Solution {
    private int length(ListNode node) {
        int c = 0;
        while (node != null) {
            c++;
            node = node.next;
        }
        return c;
    }

    private ListNode reverse(ListNode node) {
        ListNode prev = null;
        while (node != null) {
            ListNode nxt = node.next;
            node.next = prev;
            prev = node;
            node = nxt;
        }
        return prev;
    }

    public ListNode subtractTwoNumbers(ListNode l1, ListNode l2) {
        int n1 = length(l1);
        int n2 = length(l2);
        ListNode big;
        ListNode small;
        if (n1 < n2) {
            big = l2;
            small = l1;
        } else if (n1 > n2) {
            big = l1;
            small = l2;
        } else {
            ListNode p1 = l1;
            ListNode p2 = l2;
            while (p1 != null && p1.val == p2.val) {
                p1 = p1.next;
                p2 = p2.next;
            }
            if (p1 == null) {
                return new ListNode(0);
            }
            if (p1.val > p2.val) {
                big = l1;
                small = l2;
            } else {
                big = l2;
                small = l1;
            }
        }

        ListNode r1 = reverse(big);
        ListNode r2 = reverse(small);
        int borrow = 0;
        ListNode res = null;
        while (r1 != null) {
            int v2 = r2 != null ? r2.val : 0;
            int diff = r1.val - v2 - borrow;
            if (diff < 0) {
                diff += 10;
                borrow = 1;
            } else {
                borrow = 0;
            }
            res = new ListNode(diff, res);
            r1 = r1.next;
            if (r2 != null) {
                r2 = r2.next;
            }
        }
        while (res != null && res.val == 0 && res.next != null) {
            res = res.next;
        }
        return res;
    }
}
""",
        "visible": [
            {"l1": [1, 0, 0], "l2": [1, 2]},
            {"l1": [4, 5], "l2": [1, 2, 3]},
            {"l1": [5, 0, 0], "l2": [5, 0, 0]},
        ],
        "hidden": [
            {"l1": [0], "l2": [0]},
            {"l1": [0], "l2": [9, 9]},
            {"l1": [1, 0, 0, 0, 0], "l2": [1]},
            {"l1": [1, 0, 0, 0], "l2": [9, 9, 9]},
            {"l1": [9, 9, 9, 9], "l2": [9, 9, 9, 8]},
            {"l1": [3, 2, 1], "l2": [3, 2, 5]},
            {"l1": [7, 0, 0, 1], "l2": [6, 9, 9, 9]},
            {"l1": make_digits_list(6101, 200), "l2": make_digits_list(6102, 200)},
            {"l1": make_digits_list(6103, 1500), "l2": make_digits_list(6104, 1495)},
        ],
    },
    {
        "slug": "62-longest-palindromic-sublist-length",
        "title": "Longest Palindromic Sublist Length",
        "difficulty": "Hard",
        "subtopic": "Reversal",
        "companies": ["Google", "Amazon", "Meta", "Microsoft"],
        "desc": (
            "Given the `head` of a singly linked list of integers, return the length of the longest contiguous "
            "sublist whose node values form a palindrome.\n\n"
            "Solve in `O(1)` extra space by reversing the already-visited prefix on the fly as you traverse the list "
            "and expanding outward from each center."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 2000].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "As you step `curr` forward, reverse `curr.next = prev` so that `prev` points to the reversed prefix and `nxt` points to the unvisited suffix.",
            "From every node `curr`, count matching elements between `prev` and `nxt` for odd-length palindromes (`2 * common + 1`), and between `curr` and `nxt` for even-length palindromes (`2 * common`).",
        ],
        "explanations": [
            "The sublist [2, 3, 7, 3, 2] is a palindrome of length 5.",
            "The entire list [1, 2, 2, 1] is an even-length palindrome of length 4.",
            "All values are distinct, so the longest palindrome has length 1.",
        ],
        "time": "O(n^2)",
        "space": "O(1)",
        "kind": "function",
        "method": "maxPalindromeLength",
        "params": [("head", "ListNode")],
        "ret": "int",
        "py_full": """class Solution:
    def maxPalindromeLength(self, head: Optional[ListNode]) -> int:
        def count_common(a: Optional[ListNode], b: Optional[ListNode]) -> int:
            c = 0
            while a is not None and b is not None and a.val == b.val:
                c += 1
                a = a.next
                b = b.next
            return c

        ans = 0
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            odd = 2 * count_common(prev, nxt) + 1
            even = 2 * count_common(curr, nxt)
            if odd > ans:
                ans = odd
            if even > ans:
                ans = even
            prev = curr
            curr = nxt
        return ans
""",
        "java_full": """class Solution {
    private int countCommon(ListNode a, ListNode b) {
        int c = 0;
        while (a != null && b != null && a.val == b.val) {
            c++;
            a = a.next;
            b = b.next;
        }
        return c;
    }

    public int maxPalindromeLength(ListNode head) {
        int ans = 0;
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            ans = Math.max(ans, 2 * countCommon(prev, nxt) + 1);
            ans = Math.max(ans, 2 * countCommon(curr, nxt));
            prev = curr;
            curr = nxt;
        }
        return ans;
    }
}
""",
        "visible": [
            {"head": [2, 3, 7, 3, 2, 12, 24]},
            {"head": [1, 2, 2, 1]},
            {"head": [1, 2, 3, 4, 5]},
        ],
        "hidden": [
            {"head": []},
            {"head": [9]},
            {"head": [4, 4]},
            {"head": [7, 7, 7, 7, 7]},
            {"head": [1, 2, 3, 4, 3, 2, 1, 9]},
            {"head": [9, 1, 2, 3, 3, 2, 1]},
            {"head": [1, 2, 1, 2, 1, 2, 1]},
            {"head": make_rng_list(6201, 150, 0, 3)},
            {"head": [1] * 300 + [2, 3, 4] + list(range(200)) + list(range(199, -1, -1))},
        ],
    },
    {
        "slug": "63-reverse-alternate-nodes-and-append",
        "title": "Reverse Alternate Nodes and Append",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Uber"],
        "desc": (
            "Given the `head` of a singly linked list, extract all nodes at **even 1-based positions** (the 2nd, 4th, "
            "6th, ... nodes), reverse their order, and append them to the end of the remaining odd-positioned nodes "
            "(the 1st, 3rd, 5th, ... nodes).\n\n"
            "Return the head of the modified linked list in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Walk along the odd-positioned chain with pointer `odd`, detaching each successor `even = odd.next` as you go.",
            "Prepend each detached `even` node to the front of a `revEven` list (`even.next = revEven; revEven = even`) so it is automatically built in reversed order, then attach `odd.next = revEven` at the end.",
        ],
        "explanations": [
            "Odd positions [10, 9, 7, 5] stay first; even positions [4, 1, 3] reverse to [3, 1, 4] and append.",
            "Odd positions [1, 3, 5] followed by reversed even positions [4, 2] gives [1, 3, 5, 4, 2].",
            "Odd [1, 3] followed by reversed even [4, 2] gives [1, 3, 4, 2].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseAlternateAndAppend",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None:
            return head
        odd = head
        rev_even = None
        while odd.next is not None:
            even = odd.next
            odd.next = even.next
            even.next = rev_even
            rev_even = even
            if odd.next is not None:
                odd = odd.next
        odd.next = rev_even
        return head""",
        "java": """        if (head == null || head.next == null) {
            return head;
        }
        ListNode odd = head;
        ListNode revEven = null;
        while (odd.next != null) {
            ListNode even = odd.next;
            odd.next = even.next;
            even.next = revEven;
            revEven = even;
            if (odd.next != null) {
                odd = odd.next;
            }
        }
        odd.next = revEven;
        return head;""",
        "visible": [
            {"head": [10, 4, 9, 1, 7, 3, 5]},
            {"head": [1, 2, 3, 4, 5]},
            {"head": [1, 2, 3, 4]},
        ],
        "hidden": [
            {"head": []},
            {"head": [42]},
            {"head": [1, 2]},
            {"head": [1, 2, 3]},
            {"head": [5, 5, 5, 5, 5]},
            {"head": [-1, -2, -3, -4, -5, -6]},
            {"head": [10, 20, 30, 40, 50, 60, 70, 80]},
            {"head": make_rng_list(6301, 101, -1000, 1000)},
            {"head": make_rng_list(6302, 2500, -100000, 100000)},
        ],
    },
    {
        "slug": "64-reverse-strictly-decreasing-runs",
        "title": "Reverse Strictly Decreasing Runs",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Google", "Meta", "Amazon", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list of integers, partition the list into maximal contiguous "
            "**strictly decreasing** runs (a run extends from node `u` to `u.next` if and only if `u.val > u.next.val`) "
            "and reverse every run in-place.\n\n"
            "Return the head of the modified linked list in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Use a sentinel dummy node and maintain `prevTail` pointing to the tail of the previously processed run.",
            "For each new run starting at `curr`, keep reversing nodes into `revHead` while the next node's value is strictly less than the previous node's value; then link `prevTail.next = revHead` and advance `prevTail` to the original run head (now the run's tail).",
        ],
        "explanations": [
            "Maximal strictly decreasing runs are [5, 3, 1], [4, 2], [2], and [7, 6]; reversing each yields [1, 3, 5, 2, 4, 2, 6, 7].",
            "The entire list [4, 3, 2, 1] is one strictly decreasing run, reversing to [1, 2, 3, 4].",
            "No adjacent pair is strictly decreasing, so every run has length 1 and [1, 2, 2, 3] is unchanged.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseDecreasingRuns",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0, head)
        prev_tail = dummy
        curr = head
        while curr is not None:
            run_tail = curr
            rev_head = curr
            last_val = curr.val
            nxt = curr.next
            curr.next = None
            while nxt is not None and nxt.val < last_val:
                last_val = nxt.val
                after = nxt.next
                nxt.next = rev_head
                rev_head = nxt
                nxt = after
            prev_tail.next = rev_head
            prev_tail = run_tail
            curr = nxt
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0, head);
        ListNode prevTail = dummy;
        ListNode curr = head;
        while (curr != null) {
            ListNode runTail = curr;
            ListNode revHead = curr;
            int lastVal = curr.val;
            ListNode nxt = curr.next;
            curr.next = null;
            while (nxt != null && nxt.val < lastVal) {
                lastVal = nxt.val;
                ListNode after = nxt.next;
                nxt.next = revHead;
                revHead = nxt;
                nxt = after;
            }
            prevTail.next = revHead;
            prevTail = runTail;
            curr = nxt;
        }
        return dummy.next;""",
        "visible": [
            {"head": [5, 3, 1, 4, 2, 2, 7, 6]},
            {"head": [4, 3, 2, 1]},
            {"head": [1, 2, 2, 3]},
        ],
        "hidden": [
            {"head": []},
            {"head": [10]},
            {"head": [2, 1]},
            {"head": [1, 2]},
            {"head": [5, 5, 5, 5]},
            {"head": [9, 8, 7, 7, 6, 5, 4]},
            {"head": [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]},
            {"head": make_rng_list(6401, 200, -50, 50)},
            {"head": make_rng_list(6402, 2500, -100000, 100000)},
        ],
    },
])

TASKS.extend([
    # -------------------------------------------------------------------------
    # 65-70: Merge & Sort
    # -------------------------------------------------------------------------
    {
        "slug": "65-merge-two-sorted-lists-in-reverse",
        "title": "Merge Two Sorted Lists in Reverse Order",
        "difficulty": "Easy",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Oracle"],
        "desc": (
            "Given the heads of two singly linked lists `l1` and `l2` that are each sorted in **non-decreasing** "
            "order, merge them into a single singly linked list sorted in **non-increasing** (descending) order.\n\n"
            "Return the head of the merged descending list. Aim for `O(n + m)` time and `O(1)` extra space without "
            "reversing the input lists beforehand."
        ),
        "cons": [
            "The number of nodes in each list is in the range [0, 5000].",
            "-10^5 <= Node.val <= 10^5",
            "Both l1 and l2 are sorted in non-decreasing order.",
        ],
        "hints": [
            "At each step, pick the smaller front node between `l1` and `l2` and push it onto the front of the result list (`node.next = res; res = node`).",
            "Because smaller elements are inserted onto the front earlier, larger elements naturally end up closer to the head, yielding a descending list in a single pass.",
        ],
        "explanations": [
            "Merging [1, 3, 5] and [2, 4, 6] in descending order gives [6, 5, 4, 3, 2, 1].",
            "Merging [5, 10, 15, 40] and [2, 3, 20] in descending order gives [40, 20, 15, 10, 5, 3, 2].",
            "One list is empty, so [1, 1, 2] simply reverses to [2, 1, 1].",
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "kind": "function",
        "method": "mergeReverse",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "ListNode",
        "py": """        res = None
        while l1 is not None and l2 is not None:
            if l1.val <= l2.val:
                nxt = l1.next
                l1.next = res
                res = l1
                l1 = nxt
            else:
                nxt = l2.next
                l2.next = res
                res = l2
                l2 = nxt
        rem = l1 if l1 is not None else l2
        while rem is not None:
            nxt = rem.next
            rem.next = res
            res = rem
            rem = nxt
        return res""",
        "java": """        ListNode res = null;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                ListNode nxt = l1.next;
                l1.next = res;
                res = l1;
                l1 = nxt;
            } else {
                ListNode nxt = l2.next;
                l2.next = res;
                res = l2;
                l2 = nxt;
            }
        }
        ListNode rem = l1 != null ? l1 : l2;
        while (rem != null) {
            ListNode nxt = rem.next;
            rem.next = res;
            res = rem;
            rem = nxt;
        }
        return res;""",
        "visible": [
            {"l1": [1, 3, 5], "l2": [2, 4, 6]},
            {"l1": [5, 10, 15, 40], "l2": [2, 3, 20]},
            {"l1": [], "l2": [1, 1, 2]},
        ],
        "hidden": [
            {"l1": [], "l2": []},
            {"l1": [7], "l2": []},
            {"l1": [1], "l2": [1]},
            {"l1": [-10, -5, 0], "l2": [-8, -3, 2]},
            {"l1": [1, 2, 3], "l2": [4, 5, 6]},
            {"l1": [4, 5, 6], "l2": [1, 2, 3]},
            {"l1": [2, 2, 2], "l2": [2, 2]},
            {"l1": sorted(make_rng_list(6501, 150, -500, 500)), "l2": sorted(make_rng_list(6502, 150, -500, 500))},
            {"l1": sorted(make_rng_list(6503, 1500, -100000, 100000)), "l2": sorted(make_rng_list(6504, 1500, -100000, 100000))},
        ],
    },
    {
        "slug": "66-symmetric-difference-of-sorted-lists",
        "title": "Symmetric Difference of Sorted Lists",
        "difficulty": "Easy",
        "subtopic": "Merge & Sort",
        "companies": ["Google", "Amazon", "Meta", "LinkedIn"],
        "desc": (
            "You are given the heads of two singly linked lists `l1` and `l2`, each sorted in **strictly increasing** "
            "order (so every value is unique within its own list).\n\n"
            "Return a new singly linked list sorted in strictly increasing order containing all values that appear in "
            "**exactly one** of `l1` or `l2` (their symmetric difference). If the symmetric difference is empty, "
            "return `null` (`None` in Python). Aim for `O(n + m)` time and `O(1)` auxiliary space."
        ),
        "cons": [
            "The number of nodes in each list is in the range [0, 5000].",
            "-10^5 <= Node.val <= 10^5",
            "Both l1 and l2 are sorted in strictly increasing order.",
        ],
        "hints": [
            "Walk two pointers `p1` and `p2` through `l1` and `l2` simultaneously like the merge step of merge sort.",
            "When `p1.val < p2.val` append `p1` and advance `p1`; when `p2.val < p1.val` append `p2` and advance `p2`; when `p1.val == p2.val` skip both nodes and advance both pointers.",
        ],
        "explanations": [
            "Values 2 and 4 appear in both lists and are dropped, leaving [1, 3, 5, 6].",
            "Both lists contain the exact same elements [1, 2, 3], so the symmetric difference is empty (null).",
            "Since l1 is empty, every element of l2 belongs to the symmetric difference: [-5, 0, 5].",
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "kind": "function",
        "method": "symmetricDifference",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0)
        tail = dummy
        while l1 is not None and l2 is not None:
            if l1.val < l2.val:
                tail.next = l1
                tail = l1
                l1 = l1.next
            elif l2.val < l1.val:
                tail.next = l2
                tail = l2
                l2 = l2.next
            else:
                l1 = l1.next
                l2 = l2.next
        tail.next = l1 if l1 is not None else l2
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val < l2.val) {
                tail.next = l1;
                tail = l1;
                l1 = l1.next;
            } else if (l2.val < l1.val) {
                tail.next = l2;
                tail = l2;
                l2 = l2.next;
            } else {
                l1 = l1.next;
                l2 = l2.next;
            }
        }
        tail.next = l1 != null ? l1 : l2;
        return dummy.next;""",
        "visible": [
            {"l1": [1, 2, 4, 5], "l2": [2, 3, 4, 6]},
            {"l1": [1, 2, 3], "l2": [1, 2, 3]},
            {"l1": [], "l2": [-5, 0, 5]},
        ],
        "hidden": [
            {"l1": [], "l2": []},
            {"l1": [1, 3, 5], "l2": [2, 4, 6]},
            {"l1": [10], "l2": [10]},
            {"l1": [10], "l2": [20]},
            {"l1": [1, 2, 3, 4, 5], "l2": [1, 5]},
            {"l1": [-100, -50, 0, 50, 100], "l2": [-50, 0, 50]},
            {"l1": [1, 2, 3], "l2": [4, 5, 6]},
            {"l1": make_unique_sorted_list(6601, 200, 3, -100), "l2": make_unique_sorted_list(6602, 200, 3, -100)},
            {"l1": make_unique_sorted_list(6603, 1500, 3, -2000), "l2": make_unique_sorted_list(6604, 1500, 3, -2000)},
        ],
    },
    {
        "slug": "67-merge-two-linked-lists-alternately",
        "title": "Merge Two Linked Lists Alternately",
        "difficulty": "Easy",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Apple", "Microsoft", "Adobe"],
        "desc": (
            "Given the heads of two singly linked lists `l1` and `l2`, merge them into a single linked list by "
            "alternating nodes starting with `l1`: `l1[0], l2[0], l1[1], l2[1], ...`.\n\n"
            "If one list is longer than the other, append all remaining nodes of the longer list to the end of the "
            "merged list. Return the head of the merged list in `O(n + m)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in each list is in the range [0, 5000].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Maintain a sentinel `dummy` and `tail` pointer; in each iteration while both `l1` and `l2` are non-null, save `l1.next` and `l2.next`, append `l1` then `l2` to `tail`, and advance both lists.",
            "After the loop finishes, attach whichever of `l1` or `l2` is still non-null directly to `tail.next`.",
        ],
        "explanations": [
            "Taking nodes alternately from [1, 3, 5] and [2, 4, 6] gives [1, 2, 3, 4, 5, 6].",
            "After alternating 1, 10, 2, 20, the remaining nodes [30, 40] of l2 are appended.",
            "When l1 is empty, all nodes of l2 are returned as-is.",
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "kind": "function",
        "method": "mergeAlternately",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0)
        tail = dummy
        while l1 is not None and l2 is not None:
            n1 = l1.next
            n2 = l2.next
            tail.next = l1
            l1.next = l2
            tail = l2
            l1 = n1
            l2 = n2
        tail.next = l1 if l1 is not None else l2
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null && l2 != null) {
            ListNode n1 = l1.next;
            ListNode n2 = l2.next;
            tail.next = l1;
            l1.next = l2;
            tail = l2;
            l1 = n1;
            l2 = n2;
        }
        tail.next = l1 != null ? l1 : l2;
        return dummy.next;""",
        "visible": [
            {"l1": [1, 3, 5], "l2": [2, 4, 6]},
            {"l1": [1, 2], "l2": [10, 20, 30, 40]},
            {"l1": [], "l2": [7, 8, 9]},
        ],
        "hidden": [
            {"l1": [], "l2": []},
            {"l1": [5, 6, 7], "l2": []},
            {"l1": [1], "l2": [2]},
            {"l1": [1, 2, 3, 4, 5], "l2": [9]},
            {"l1": [9], "l2": [1, 2, 3, 4, 5]},
            {"l1": [-1, -2, -3], "l2": [1, 2, 3]},
            {"l1": [0, 0, 0], "l2": [1, 1, 1, 1]},
            {"l1": make_rng_list(6701, 120, -1000, 1000), "l2": make_rng_list(6702, 80, -1000, 1000)},
            {"l1": make_rng_list(6703, 1500, -100000, 100000), "l2": make_rng_list(6704, 1200, -100000, 100000)},
        ],
    },
    {
        "slug": "68-sort-k-sorted-linked-list",
        "title": "Sort a K-Sorted Linked List",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Google", "Amazon", "Meta", "Uber"],
        "desc": (
            "You are given the `head` of a singly linked list of length `n` and a non-negative integer `k`. "
            "The linked list is **k-sorted**, meaning that every node is at most `k` positions away from its final "
            "position in the sorted (non-decreasing) order.\n\n"
            "Sort the linked list in non-decreasing order and return its new head. Aim for `O(n log k)` time and "
            "`O(k)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "0 <= k <= n",
            "-10^5 <= Node.val <= 10^5",
            "Every node is at most k positions away from its target index in the sorted list.",
        ],
        "hints": [
            "The smallest element of the entire list is guaranteed to appear among the first `k + 1` nodes.",
            "Maintain a min-heap holding at most `k + 1` nodes: repeatedly pop the minimum node to append to the output list, push the next unread node into the heap, and terminate the tail with `tail.next = null`.",
        ],
        "explanations": [
            "Each node in [3, 6, 2, 12, 56, 8] is at most k=2 positions from its sorted position [2, 3, 6, 8, 12, 56].",
            "With k=3, sorting [6, 5, 3, 2, 8, 10, 9] yields [2, 3, 5, 6, 8, 9, 10].",
            "With k=0, the list [1, 2, 3, 4] is already sorted.",
        ],
        "time": "O(n log k)",
        "space": "O(k)",
        "kind": "function",
        "method": "sortKSortedList",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode",
        "py_full": """import heapq


class Solution:
    def sortKSortedList(self, head: Optional[ListNode], k: int) -> Optional[ListNode]:
        if head is None or head.next is None or k == 0:
            return head
        heap: list[tuple[int, int, ListNode]] = []
        curr = head
        uid = 0
        for _ in range(k + 1):
            if curr is None:
                break
            heapq.heappush(heap, (curr.val, uid, curr))
            uid += 1
            curr = curr.next
        dummy = ListNode(0)
        tail = dummy
        while heap:
            _, _, node = heapq.heappop(heap)
            tail.next = node
            tail = node
            if curr is not None:
                heapq.heappush(heap, (curr.val, uid, curr))
                uid += 1
                curr = curr.next
        tail.next = None
        return dummy.next
""",
        "java_full": """class Solution {
    public ListNode sortKSortedList(ListNode head, int k) {
        if (head == null || head.next == null || k == 0) {
            return head;
        }
        PriorityQueue<ListNode> pq = new PriorityQueue<>((a, b) -> Integer.compare(a.val, b.val));
        ListNode curr = head;
        for (int i = 0; i <= k && curr != null; i++) {
            pq.offer(curr);
            curr = curr.next;
        }
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (!pq.isEmpty()) {
            ListNode node = pq.poll();
            tail.next = node;
            tail = node;
            if (curr != null) {
                pq.offer(curr);
                curr = curr.next;
            }
        }
        tail.next = null;
        return dummy.next;
    }
}
""",
        "visible": [
            {"head": [3, 6, 2, 12, 56, 8], "k": 2},
            {"head": [6, 5, 3, 2, 8, 10, 9], "k": 3},
            {"head": [1, 2, 3, 4], "k": 0},
        ],
        "hidden": [
            {"head": [], "k": 0},
            {"head": [5], "k": 1},
            {"head": [2, 1], "k": 1},
            {"head": [4, 3, 2, 1], "k": 3},
            {"head": [2, 1, 4, 3, 6, 5, 8, 7], "k": 1},
            {"head": [-5, -10, -2, -8, 0, -1], "k": 2},
            {"head": [5, 5, 1, 5, 1, 9, 5], "k": 4},
            {"head": make_k_sorted_list(6801, 200, 10), "k": 10},
            {"head": make_k_sorted_list(6802, 2500, 25), "k": 25},
        ],
    },
    {
        "slug": "69-sort-bitonic-linked-list",
        "title": "Sort Bitonic Linked List",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Google"],
        "desc": (
            "A singly linked list is called **bitonic** if its values are first **non-decreasing** up to some peak "
            "node and then **non-increasing** from that peak to the tail (this includes lists that are purely "
            "non-decreasing or purely non-increasing).\n\n"
            "Given the `head` of a bitonic singly linked list, sort it in **non-decreasing** order and return its "
            "new head in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "The input list is guaranteed to be bitonic (non-decreasing prefix followed by non-increasing suffix).",
        ],
        "hints": [
            "Scan forward from `head` to find the first node `peak` where `peak.val > peak.next.val`; split the list right after `peak` into an ascending first half and a descending second half.",
            "Reverse the descending second half in O(n) time and O(1) space, then merge the two non-decreasing linked lists.",
        ],
        "explanations": [
            "Ascending prefix [2, 5, 7, 12] and descending suffix [10, 6, 4, 1] (reversed to [1, 4, 6, 10]) merge into [1, 2, 4, 5, 6, 7, 10, 12].",
            "Purely non-increasing [5, 4, 3, 2, 1] splits into [5] and [4, 3, 2, 1] -> [1, 2, 3, 4, 5].",
            "Already non-decreasing [1, 3, 3, 5] needs no change.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "sortBitonicList",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py_full": """class Solution:
    def sortBitonicList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        curr = head
        while curr.next is not None and curr.val <= curr.next.val:
            curr = curr.next
        if curr.next is None:
            return head
        second = curr.next
        curr.next = None

        prev = None
        while second is not None:
            nxt = second.next
            second.next = prev
            prev = second
            second = nxt

        dummy = ListNode(0)
        tail = dummy
        a, b = head, prev
        while a is not None and b is not None:
            if a.val <= b.val:
                tail.next = a
                a = a.next
            else:
                tail.next = b
                b = b.next
            tail = tail.next
        tail.next = a if a is not None else b
        return dummy.next
""",
        "java_full": """class Solution {
    public ListNode sortBitonicList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode curr = head;
        while (curr.next != null && curr.val <= curr.next.val) {
            curr = curr.next;
        }
        if (curr.next == null) {
            return head;
        }
        ListNode second = curr.next;
        curr.next = null;

        ListNode prev = null;
        while (second != null) {
            ListNode nxt = second.next;
            second.next = prev;
            prev = second;
            second = nxt;
        }

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        ListNode a = head;
        ListNode b = prev;
        while (a != null && b != null) {
            if (a.val <= b.val) {
                tail.next = a;
                a = a.next;
            } else {
                tail.next = b;
                b = b.next;
            }
            tail = tail.next;
        }
        tail.next = a != null ? a : b;
        return dummy.next;
    }
}
""",
        "visible": [
            {"head": [2, 5, 7, 12, 10, 6, 4, 1]},
            {"head": [5, 4, 3, 2, 1]},
            {"head": [1, 3, 3, 5]},
        ],
        "hidden": [
            {"head": []},
            {"head": [8]},
            {"head": [8, 2]},
            {"head": [1, 5, 5, 5, 3, 3, 1]},
            {"head": [-10, -5, 0, 5, -2, -8, -20]},
            {"head": [7, 7, 7, 7]},
            {"head": [1, 2, 3, 100, 50, 25, 0]},
            {"head": make_bitonic_list(6901, 100, 120)},
            {"head": make_bitonic_list(6902, 1500, 1500)},
        ],
    },
    {
        "slug": "70-count-inversions-in-linked-list",
        "title": "Count Inversions in Linked List",
        "difficulty": "Hard",
        "subtopic": "Merge & Sort",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list of integers, return the total number of **inversions** in the "
            "list. A pair of 0-based indices `(i, j)` forms an inversion if `i < j` and `node[i].val > node[j].val`.\n\n"
            "Because the answer can be large, return it as a 64-bit integer (`long` in Java, `int` in Python). "
            "Aim for `O(n log n)` time using merge sort directly on the linked list."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Count the list length `n` first, then run top-down merge sort passing `(head, length)` so splitting into `leftLen = length // 2` and `rightLen = length - leftLen` is exact and gives you the exact remaining left count during merging.",
            "While merging two sorted sublists `left` and `right`, whenever `right.val < left.val`, every remaining node in `left` (`leftRem` nodes) forms an inversion with `right`, so add `leftRem` to the total.",
        ],
        "explanations": [
            "In [2, 4, 1, 3, 5], the inversions are (2, 1), (4, 1), and (4, 3): 3 total.",
            "A strictly decreasing list of length 4 has 4*3/2 = 6 inversions.",
            "An already sorted list [1, 2, 2, 3] has 0 inversions (equal values do not count).",
        ],
        "time": "O(n log n)",
        "space": "O(log n)",
        "kind": "function",
        "method": "countInversions",
        "params": [("head", "ListNode")],
        "ret": "long",
        "py_full": """class Solution:
    def countInversions(self, head: Optional[ListNode]) -> int:
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next

        def sort_count(node: Optional[ListNode], length: int) -> tuple[Optional[ListNode], int]:
            if length <= 1 or node is None:
                return node, 0
            left_len = length // 2
            right_len = length - left_len
            mid = node
            for _ in range(left_len - 1):
                mid = mid.next
            right_head = mid.next
            mid.next = None

            left, inv_l = sort_count(node, left_len)
            right, inv_r = sort_count(right_head, right_len)
            inv = inv_l + inv_r
            left_rem = left_len

            dummy = ListNode(0)
            tail = dummy
            while left is not None and right is not None:
                if left.val <= right.val:
                    tail.next = left
                    left = left.next
                    left_rem -= 1
                else:
                    tail.next = right
                    right = right.next
                    inv += left_rem
                tail = tail.next
            tail.next = left if left is not None else right
            return dummy.next, inv

        _, ans = sort_count(head, n)
        return ans
""",
        "java_full": """class Solution {
    private long inv;

    private ListNode sortCount(ListNode node, int length) {
        if (length <= 1 || node == null) {
            return node;
        }
        int leftLen = length / 2;
        int rightLen = length - leftLen;
        ListNode mid = node;
        for (int i = 0; i < leftLen - 1; i++) {
            mid = mid.next;
        }
        ListNode rightHead = mid.next;
        mid.next = null;

        ListNode left = sortCount(node, leftLen);
        ListNode right = sortCount(rightHead, rightLen);
        int leftRem = leftLen;

        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (left != null && right != null) {
            if (left.val <= right.val) {
                tail.next = left;
                left = left.next;
                leftRem--;
            } else {
                tail.next = right;
                right = right.next;
                inv += leftRem;
            }
            tail = tail.next;
        }
        tail.next = left != null ? left : right;
        return dummy.next;
    }

    public long countInversions(ListNode head) {
        inv = 0L;
        int n = 0;
        ListNode curr = head;
        while (curr != null) {
            n++;
            curr = curr.next;
        }
        sortCount(head, n);
        return inv;
    }
}
""",
        "visible": [
            {"head": [2, 4, 1, 3, 5]},
            {"head": [4, 3, 2, 1]},
            {"head": [1, 2, 2, 3]},
        ],
        "hidden": [
            {"head": []},
            {"head": [10]},
            {"head": [2, 1]},
            {"head": [5, 5, 5, 5]},
            {"head": [3, 1, 2, 3, 1, 2]},
            {"head": [-1, -2, -3, -4, -5]},
            {"head": [8, 4, 2, 1, 9, 5, 3, 7, 6]},
            {"head": list(range(300, 0, -1))},
            {"head": make_rng_list(7001, 2500, -100000, 100000)},
        ],
    },
])

TASKS.extend([
    # -------------------------------------------------------------------------
    # 71-76: LRU Design
    # -------------------------------------------------------------------------
    {
        "slug": "71-design-mru-queue",
        "title": "Design MRU Queue",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Bloomberg"],
        "desc": (
            "Design a queue-like data structure `MRUQueue` that moves the most recently used element to the end of "
            "the queue:\n"
            "- `MRUQueue(int n)` constructs the queue containing the `n` integers `[1, 2, 3, ..., n]` in order.\n"
            "- `int fetch(int k)` moves the `k`-th element (**1-indexed**) to the end of the queue and returns its "
            "value.\n\n"
            "Aim for `O(sqrt(n))` time per `fetch` using sqrt-decomposed linked-list buckets (or `O(log n)` with an "
            "order-statistic tree / Fenwick tree)."
        ),
        "cons": [
            "1 <= n <= 2000",
            "1 <= k <= n",
            "At most 2000 calls will be made to fetch.",
        ],
        "hints": [
            "Partition the `n` elements into `ceil(n / B)` doubly linked lists (deques) of bucket size `B = isqrt(n) + 1`, so locating bucket `b = (k - 1) // B` and offset `(k - 1) % B` takes O(sqrt(n)) time.",
            "After removing the fetched element from bucket `b` and appending it to the last bucket, shift the front element of bucket `j + 1` to the back of bucket `j` for each `j` from `b` to `numBuckets - 2` in O(1) per bucket, preserving fixed bucket sizes.",
        ],
        "explanations": [
            "Start [1..8]: fetch(3)->3 ([1,2,4,5,6,7,8,3]), fetch(5)->6 ([1,2,4,5,7,8,3,6]), fetch(2)->2 ([1,4,5,7,8,3,6,2]), fetch(8)->2.",
            "With n=1, the single element 1 is always fetched and placed back at index 1.",
            "Start [1,2,3,4]: fetch(1)->1 ([2,3,4,1]), fetch(1)->2 ([3,4,1,2]), fetch(4)->2, fetch(3)->1.",
        ],
        "time": "O(sqrt(n)) per fetch",
        "space": "O(n)",
        "kind": "design",
        "className": "MRUQueue",
        "ctor_params": [("n", "int")],
        "methods": [
            {"name": "fetch", "params": [("k", "int")], "ret": "int"},
        ],
        "py_full": """from collections import deque
import math


class MRUQueue:
    def __init__(self, n: int):
        self.block = max(1, math.isqrt(n))
        self.buckets: list[deque[int]] = []
        for start in range(1, n + 1, self.block):
            end = min(n + 1, start + self.block)
            self.buckets.append(deque(range(start, end)))

    def fetch(self, k: int) -> int:
        b = (k - 1) // self.block
        off = (k - 1) % self.block
        bucket = self.buckets[b]
        bucket.rotate(-off)
        val = bucket.popleft()
        bucket.rotate(off)
        for j in range(b, len(self.buckets) - 1):
            self.buckets[j].append(self.buckets[j + 1].popleft())
        self.buckets[-1].append(val)
        return val
""",
        "java_full": """class MRUQueue {
    private final int block;
    private final LinkedList<Integer>[] buckets;

    @SuppressWarnings("unchecked")
    public MRUQueue(int n) {
        this.block = Math.max(1, (int) Math.sqrt(n));
        int numBuckets = (n + block - 1) / block;
        this.buckets = new LinkedList[numBuckets];
        for (int i = 0; i < numBuckets; i++) {
            buckets[i] = new LinkedList<>();
            int start = i * block + 1;
            int end = Math.min(n, start + block - 1);
            for (int v = start; v <= end; v++) {
                buckets[i].addLast(v);
            }
        }
    }

    public int fetch(int k) {
        int b = (k - 1) / block;
        int off = (k - 1) % block;
        int val = buckets[b].remove(off);
        for (int j = b; j < buckets.length - 1; j++) {
            buckets[j].addLast(buckets[j + 1].removeFirst());
        }
        buckets[buckets.length - 1].addLast(val);
        return val;
    }
}
""",
        "visible": [
            {
                "ops": ["MRUQueue", "fetch", "fetch", "fetch", "fetch"],
                "args": [[8], [3], [5], [2], [8]],
            },
            {
                "ops": ["MRUQueue", "fetch", "fetch"],
                "args": [[1], [1], [1]],
            },
            {
                "ops": ["MRUQueue", "fetch", "fetch", "fetch", "fetch"],
                "args": [[4], [1], [1], [4], [3]],
            },
        ],
        "hidden_fn": "gen_hidden_71",
    },
    {
        "slug": "72-design-lru-cache-with-ttl",
        "title": "Design LRU Cache with TTL",
        "difficulty": "Hard",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Uber", "Netflix"],
        "desc": (
            "Design an LRU cache `TTLLRUCache` where each stored entry also has a **time-to-live (TTL)**:\n"
            "- `TTLLRUCache(int capacity)` initializes the cache with positive `capacity`.\n"
            "- `int get(int key, int timestamp)` returns the value of `key` if it exists and has **not expired** "
            "(`timestamp < expireAt`), marking `key` as the most recently used entry (without changing its `expireAt`). "
            "If `key` does not exist or has expired (`timestamp >= expireAt`), remove it if present and return `-1`.\n"
            "- `void put(int key, int value, int timestamp, int ttl)` inserts or updates `key` with `value`, sets its "
            "expiration time to `expireAt = timestamp + ttl`, and marks it as most recently used. Before evicting any "
            "live entry when at capacity, purge all expired entries (`expireAt <= timestamp`); if the cache is still "
            "at capacity after purging expired entries, evict the least recently used live entry.\n\n"
            "Timestamps across all calls are guaranteed to be non-decreasing."
        ),
        "cons": [
            "1 <= capacity <= 1000",
            "0 <= key, value <= 10^5",
            "0 <= timestamp <= 10^6 (non-decreasing across calls)",
            "1 <= ttl <= 10^6",
            "At most 2000 calls will be made to get and put.",
        ],
        "hints": [
            "Combine a standard LRU doubly linked list + hash map with a min-heap keyed by `(expireAt, version, key)`.",
            "Before executing `get` or `put` at `timestamp`, pop every heap entry with `expireAt <= timestamp` and unlink the corresponding node from the DLL if its `version` still matches (lazy invalidation for updated keys).",
        ],
        "explanations": [
            "Key 1 expires at t=6, so get(1,5)=10 succeeds while get(1,6)=-1; put(3,30,7,5) purges expired key 1 so key 2 is not evicted.",
            "Neither key expires, so get(1,3) refreshes key 1 and put(3,3,4,100) evicts the LRU key 2.",
            "Updating key 1 at t=4 refreshes both its value to 99 and its expiration to 4+10=14.",
        ],
        "time": "O(log n) amortized",
        "space": "O(n)",
        "kind": "design",
        "className": "TTLLRUCache",
        "ctor_params": [("capacity", "int")],
        "methods": [
            {"name": "get", "params": [("key", "int"), ("timestamp", "int")], "ret": "int"},
            {
                "name": "put",
                "params": [("key", "int"), ("value", "int"), ("timestamp", "int"), ("ttl", "int")],
                "ret": "void",
            },
        ],
        "py_full": """import heapq


class _TTLNode:
    __slots__ = ("key", "val", "exp", "ver", "prev", "next")

    def __init__(self, key: int = 0, val: int = 0, exp: int = 0, ver: int = 0):
        self.key = key
        self.val = val
        self.exp = exp
        self.ver = ver
        self.prev: "_TTLNode | None" = None
        self.next: "_TTLNode | None" = None


class TTLLRUCache:
    def __init__(self, capacity: int):
        self.cap = capacity
        self.map: dict[int, _TTLNode] = {}
        self.heap: list[tuple[int, int, int]] = []
        self.ver = 0
        self.head = _TTLNode()
        self.tail = _TTLNode()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _unlink(self, node: _TTLNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_front(self, node: _TTLNode) -> None:
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _purge(self, timestamp: int) -> None:
        while self.heap and self.heap[0][0] <= timestamp:
            _, ver, key = heapq.heappop(self.heap)
            node = self.map.get(key)
            if node is not None and node.ver == ver:
                self._unlink(node)
                del self.map[key]

    def get(self, key: int, timestamp: int) -> int:
        self._purge(timestamp)
        node = self.map.get(key)
        if node is None:
            return -1
        self._unlink(node)
        self._insert_front(node)
        return node.val

    def put(self, key: int, value: int, timestamp: int, ttl: int) -> None:
        self._purge(timestamp)
        self.ver += 1
        exp = timestamp + ttl
        node = self.map.get(key)
        if node is not None:
            node.val = value
            node.exp = exp
            node.ver = self.ver
            self._unlink(node)
            self._insert_front(node)
        else:
            if len(self.map) == self.cap:
                lru = self.tail.prev
                self._unlink(lru)
                del self.map[lru.key]
            node = _TTLNode(key, value, exp, self.ver)
            self._insert_front(node)
            self.map[key] = node
        heapq.heappush(self.heap, (exp, self.ver, key))
""",
        "java_full": """class TTLLRUCache {
    private static class Node {
        int key, val, exp, ver;
        Node prev, next;
        Node(int key, int val, int exp, int ver) {
            this.key = key;
            this.val = val;
            this.exp = exp;
            this.ver = ver;
        }
    }

    private final int cap;
    private final Map<Integer, Node> map = new HashMap<>();
    private final PriorityQueue<int[]> heap = new PriorityQueue<>((a, b) -> {
        if (a[0] != b[0]) return Integer.compare(a[0], b[0]);
        return Integer.compare(a[1], b[1]);
    });
    private int ver = 0;
    private final Node head = new Node(0, 0, 0, 0);
    private final Node tail = new Node(0, 0, 0, 0);

    public TTLLRUCache(int capacity) {
        this.cap = capacity;
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertFront(Node node) {
        node.prev = head;
        node.next = head.next;
        head.next.prev = node;
        head.next = node;
    }

    private void purge(int timestamp) {
        while (!heap.isEmpty() && heap.peek()[0] <= timestamp) {
            int[] top = heap.poll();
            Node node = map.get(top[2]);
            if (node != null && node.ver == top[1]) {
                unlink(node);
                map.remove(top[2]);
            }
        }
    }

    public int get(int key, int timestamp) {
        purge(timestamp);
        Node node = map.get(key);
        if (node == null) {
            return -1;
        }
        unlink(node);
        insertFront(node);
        return node.val;
    }

    public void put(int key, int value, int timestamp, int ttl) {
        purge(timestamp);
        ver++;
        int exp = timestamp + ttl;
        Node node = map.get(key);
        if (node != null) {
            node.val = value;
            node.exp = exp;
            node.ver = ver;
            unlink(node);
            insertFront(node);
        } else {
            if (map.size() == cap) {
                Node lru = tail.prev;
                unlink(lru);
                map.remove(lru.key);
            }
            node = new Node(key, value, exp, ver);
            insertFront(node);
            map.put(key, node);
        }
        heap.offer(new int[]{exp, ver, key});
    }
}
""",
        "visible": [
            {
                "ops": ["TTLLRUCache", "put", "put", "get", "get", "put", "get", "get"],
                "args": [[2], [1, 10, 1, 5], [2, 20, 2, 10], [1, 5], [1, 6], [3, 30, 7, 5], [2, 8], [3, 8]],
            },
            {
                "ops": ["TTLLRUCache", "put", "put", "get", "put", "get", "get", "get"],
                "args": [[2], [1, 1, 1, 100], [2, 2, 2, 100], [1, 3], [3, 3, 4, 100], [2, 5], [1, 5], [3, 5]],
            },
            {
                "ops": ["TTLLRUCache", "put", "put", "get", "get"],
                "args": [[1], [1, 10, 0, 5], [1, 99, 4, 10], [1, 10], [1, 14]],
            },
        ],
        "hidden_fn": "gen_hidden_72",
    },
    {
        "slug": "73-design-playlist-manager",
        "title": "Design Music Playlist Manager",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Apple", "Amazon", "Netflix", "Uber"],
        "desc": (
            "Design a music playlist manager `PlaylistManager` supporting `O(1)` song navigation, arbitrary song "
            "removal, and reordering:\n"
            "- `PlaylistManager()` initializes an empty playlist with no current song.\n"
            "- `void addSong(int songId)` appends `songId` to the end of the playlist (if `songId` is not already "
            "present). If the playlist was empty, `songId` becomes the current song.\n"
            "- `void playNext()` moves the current song pointer to the next song in the playlist if one exists; "
            "otherwise does nothing.\n"
            "- `void playPrev()` moves the current song pointer to the previous song in the playlist if one exists; "
            "otherwise does nothing.\n"
            "- `void removeSong(int songId)` removes `songId` if it is in the playlist. If the removed song was the "
            "current song, advance current to its next song if one exists, otherwise to its previous song if one "
            "exists, otherwise the playlist becomes empty.\n"
            "- `void moveToFront(int songId)` moves `songId` to the front of the playlist if it is present, while "
            "keeping the current pointer on the exact same song node it was already pointing to.\n"
            "- `int getCurrent()` returns the `songId` of the current song, or `-1` if the playlist is empty."
        ),
        "cons": [
            "1 <= songId <= 10^5",
            "At most 2000 calls will be made across all operations.",
        ],
        "hints": [
            "Use a doubly linked list with sentinel `head` and `tail` nodes, a hash map `songId -> Node` for O(1) lookup, and a `curr` node reference.",
            "Because `curr` points directly to a node object, `moveToFront(songId)` only needs to unlink the node and insert it after `head` without changing `curr`.",
        ],
        "explanations": [
            "List [10,20,30], curr=10 -> playNext curr=20 -> moveToFront(30) gives [30,10,20] with curr=20 -> playPrev gives 10 -> playPrev gives 30.",
            "Removing current song 1 advances current to next song 2; removing 2 empties the playlist so getCurrent() returns -1.",
            "When current song 6 is the tail, removing 6 falls back to previous song 5.",
        ],
        "time": "O(1) per operation",
        "space": "O(n)",
        "kind": "design",
        "className": "PlaylistManager",
        "ctor_params": [],
        "methods": [
            {"name": "addSong", "params": [("songId", "int")], "ret": "void"},
            {"name": "playNext", "params": [], "ret": "void"},
            {"name": "playPrev", "params": [], "ret": "void"},
            {"name": "removeSong", "params": [("songId", "int")], "ret": "void"},
            {"name": "moveToFront", "params": [("songId", "int")], "ret": "void"},
            {"name": "getCurrent", "params": [], "ret": "int"},
        ],
        "py_full": """class _SongNode:
    __slots__ = ("song_id", "prev", "next")

    def __init__(self, song_id: int = 0):
        self.song_id = song_id
        self.prev: "_SongNode | None" = None
        self.next: "_SongNode | None" = None


class PlaylistManager:
    def __init__(self):
        self.head = _SongNode()
        self.tail = _SongNode()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.nodes: dict[int, _SongNode] = {}
        self.curr: _SongNode | None = None

    def _unlink(self, node: _SongNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_after(self, ref: _SongNode, node: _SongNode) -> None:
        node.prev = ref
        node.next = ref.next
        ref.next.prev = node
        ref.next = node

    def addSong(self, songId: int) -> None:
        if songId in self.nodes:
            return
        node = _SongNode(songId)
        self._insert_after(self.tail.prev, node)
        self.nodes[songId] = node
        if self.curr is None:
            self.curr = node

    def playNext(self) -> None:
        if self.curr is not None and self.curr.next is not self.tail:
            self.curr = self.curr.next

    def playPrev(self) -> None:
        if self.curr is not None and self.curr.prev is not self.head:
            self.curr = self.curr.prev

    def removeSong(self, songId: int) -> None:
        node = self.nodes.pop(songId, None)
        if node is None:
            return
        if self.curr is node:
            if node.next is not self.tail:
                self.curr = node.next
            elif node.prev is not self.head:
                self.curr = node.prev
            else:
                self.curr = None
        self._unlink(node)

    def moveToFront(self, songId: int) -> None:
        node = self.nodes.get(songId)
        if node is None:
            return
        self._unlink(node)
        self._insert_after(self.head, node)

    def getCurrent(self) -> int:
        return self.curr.song_id if self.curr is not None else -1
""",
        "java_full": """class PlaylistManager {
    private static class Node {
        int songId;
        Node prev, next;
        Node(int songId) {
            this.songId = songId;
        }
    }

    private final Node head = new Node(0);
    private final Node tail = new Node(0);
    private final Map<Integer, Node> nodes = new HashMap<>();
    private Node curr = null;

    public PlaylistManager() {
        head.next = tail;
        tail.prev = head;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertAfter(Node ref, Node node) {
        node.prev = ref;
        node.next = ref.next;
        ref.next.prev = node;
        ref.next = node;
    }

    public void addSong(int songId) {
        if (nodes.containsKey(songId)) {
            return;
        }
        Node node = new Node(songId);
        insertAfter(tail.prev, node);
        nodes.put(songId, node);
        if (curr == null) {
            curr = node;
        }
    }

    public void playNext() {
        if (curr != null && curr.next != tail) {
            curr = curr.next;
        }
    }

    public void playPrev() {
        if (curr != null && curr.prev != head) {
            curr = curr.prev;
        }
    }

    public void removeSong(int songId) {
        Node node = nodes.remove(songId);
        if (node == null) {
            return;
        }
        if (curr == node) {
            if (node.next != tail) {
                curr = node.next;
            } else if (node.prev != head) {
                curr = node.prev;
            } else {
                curr = null;
            }
        }
        unlink(node);
    }

    public void moveToFront(int songId) {
        Node node = nodes.get(songId);
        if (node == null) {
            return;
        }
        unlink(node);
        insertAfter(head, node);
    }

    public int getCurrent() {
        return curr != null ? curr.songId : -1;
    }
}
""",
        "visible": [
            {
                "ops": ["PlaylistManager", "addSong", "addSong", "addSong", "getCurrent", "playNext", "getCurrent", "moveToFront", "playPrev", "getCurrent", "playPrev", "getCurrent"],
                "args": [[], [10], [20], [30], [], [], [], [30], [], [], [], []],
            },
            {
                "ops": ["PlaylistManager", "addSong", "addSong", "removeSong", "getCurrent", "removeSong", "getCurrent"],
                "args": [[], [1], [2], [1], [], [2], []],
            },
            {
                "ops": ["PlaylistManager", "addSong", "addSong", "playNext", "removeSong", "getCurrent"],
                "args": [[], [5], [6], [], [6], []],
            },
        ],
        "hidden_fn": "gen_hidden_73",
    },
    {
        "slug": "74-design-snake-game-linked-list",
        "title": "Design Linked List Snake Game",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Amazon", "Google", "Uber", "Atlassian", "Salesforce"],
        "desc": (
            "Design a Snake game `SnakeGame` backed by a doubly linked list (deque) for the snake's body and a hash "
            "set for `O(1)` collision detection:\n"
            "- `SnakeGame(int width, int height, int[][] food)` initializes a board of `height` rows (`0..height-1`) "
            "and `width` columns (`0..width-1`). The snake starts at `(0, 0)` with length `1` and score `0`. `food` "
            "lists food coordinates `[row, col]` that appear one at a time in order.\n"
            "- `int move(String direction)` moves the snake's head one cell in `\"U\"`, `\"D\"`, `\"L\"`, or `\"R\"`. "
            "If the head goes out of bounds or collides with the snake's own body (note that moving into the exact "
            "cell vacated by the tail on a non-eating move is valid), the game ends and `move` returns `-1` (as do "
            "any subsequent `move` calls). If the head lands on the currently active food item, the snake grows by 1 "
            "(tail does not move), the score increases by 1, and the next food item appears. Return the current score."
        ),
        "cons": [
            "1 <= width, height <= 10^4",
            "0 <= food.length <= 200",
            "food[i].length == 2, 0 <= food[i][0] < height, 0 <= food[i][1] < width",
            "direction is one of \"U\", \"D\", \"L\", or \"R\".",
            "At most 2000 calls will be made to move.",
        ],
        "hints": [
            "Store the snake's occupied cells in a deque (doubly linked list) from head to tail, and mirror them in a hash set of encoded cell keys `row * width + col`.",
            "When the new head cell does not hold the active food item, pop the tail from both the deque and the hash set BEFORE checking whether the new head collides with the occupied set.",
        ],
        "explanations": [
            "The snake eats food at (1,2) and (0,1) to reach score 2, then moves up out of bounds for -1.",
            "After eating 3 food items in a 2x2 grid, moving up into (0,0) succeeds because the tail vacates (0,0) on the same turn.",
            "After growing to length 5, moving up into (0,1) collides with an interior body segment, returning -1.",
        ],
        "time": "O(1) per move",
        "space": "O(L)",
        "kind": "design",
        "className": "SnakeGame",
        "ctor_params": [("width", "int"), ("height", "int"), ("food", "int[][]")],
        "methods": [
            {"name": "move", "params": [("direction", "String")], "ret": "int"},
        ],
        "py_full": """from collections import deque


class SnakeGame:
    def __init__(self, width: int, height: int, food: List[List[int]]):
        self.w = width
        self.h = height
        self.food = food
        self.fi = 0
        self.body: deque[tuple[int, int]] = deque([(0, 0)])
        self.occupied: set[tuple[int, int]] = {(0, 0)}
        self.over = False

    def move(self, direction: str) -> int:
        if self.over:
            return -1
        r, c = self.body[0]
        if direction == "U":
            r -= 1
        elif direction == "D":
            r += 1
        elif direction == "L":
            c -= 1
        else:
            c += 1
        if r < 0 or r >= self.h or c < 0 or c >= self.w:
            self.over = True
            return -1
        eating = self.fi < len(self.food) and self.food[self.fi][0] == r and self.food[self.fi][1] == c
        if not eating:
            tail = self.body.pop()
            self.occupied.remove(tail)
        if (r, c) in self.occupied:
            self.over = True
            return -1
        self.body.appendleft((r, c))
        self.occupied.add((r, c))
        if eating:
            self.fi += 1
        return len(self.body) - 1
""",
        "java_full": """class SnakeGame {
    private final int w;
    private final int h;
    private final int[][] food;
    private int fi = 0;
    private final Deque<Long> body = new ArrayDeque<>();
    private final Set<Long> occupied = new HashSet<>();
    private boolean over = false;

    public SnakeGame(int width, int height, int[][] food) {
        this.w = width;
        this.h = height;
        this.food = food;
        body.addFirst(0L);
        occupied.add(0L);
    }

    private long encode(int r, int c) {
        return (long) r * w + c;
    }

    public int move(String direction) {
        if (over) {
            return -1;
        }
        long headKey = body.peekFirst();
        int r = (int) (headKey / w);
        int c = (int) (headKey % w);
        char ch = direction.charAt(0);
        if (ch == 'U') r--;
        else if (ch == 'D') r++;
        else if (ch == 'L') c--;
        else c++;
        if (r < 0 || r >= h || c < 0 || c >= w) {
            over = true;
            return -1;
        }
        boolean eating = fi < food.length && food[fi][0] == r && food[fi][1] == c;
        if (!eating) {
            long tailKey = body.removeLast();
            occupied.remove(tailKey);
        }
        long newKey = encode(r, c);
        if (occupied.contains(newKey)) {
            over = true;
            return -1;
        }
        body.addFirst(newKey);
        occupied.add(newKey);
        if (eating) {
            fi++;
        }
        return body.size() - 1;
    }
}
""",
        "visible": [
            {
                "ops": ["SnakeGame", "move", "move", "move", "move", "move", "move"],
                "args": [[3, 2, [[1, 2], [0, 1]]], ["R"], ["D"], ["R"], ["U"], ["L"], ["U"]],
            },
            {
                "ops": ["SnakeGame", "move", "move", "move", "move"],
                "args": [[2, 2, [[0, 1], [1, 1], [1, 0]]], ["R"], ["D"], ["L"], ["U"]],
            },
            {
                "ops": ["SnakeGame", "move", "move", "move", "move", "move"],
                "args": [[3, 3, [[0, 1], [0, 2], [1, 2], [1, 1], [1, 0]]], ["R"], ["R"], ["D"], ["L"], ["U"]],
            },
        ],
        "hidden_fn": "gen_hidden_74",
    },
    {
        "slug": "75-design-memory-allocator-free-list",
        "title": "Design Memory Allocator Free List",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "desc": (
            "Design a memory allocator `MemoryAllocator` managing a contiguous address space `[0, n - 1]` of size "
            "`n` (up to `10^9` units) using a **doubly linked list of memory segments** with free-block coalescing:\n"
            "- `MemoryAllocator(int n)` initializes a single free segment `[0, n - 1]` of length `n`.\n"
            "- `int allocate(int size, int mID)` finds the **leftmost** contiguous free block of length at least "
            "`size`, allocates its leftmost `size` units to memory ID `mID`, and returns the starting address. If no "
            "free block is large enough, returns `-1`.\n"
            "- `int freeMemory(int mID)` frees all segments currently assigned to `mID`, coalescing each freed segment "
            "with any immediately adjacent free segments on its left or right, and returns the total number of units "
            "freed (`0` if `mID` owns no segments)."
        ),
        "cons": [
            "1 <= n <= 10^9",
            "1 <= size <= 10^9",
            "1 <= mID <= 1000",
            "At most 1000 calls will be made to allocate and freeMemory.",
        ],
        "hints": [
            "Because `n` can be as large as `10^9`, you cannot allocate an array of size `n`. Instead store segments `(start, length, mID)` (with `mID == 0` meaning free) in a doubly linked list and keep a map `mID -> list of owned nodes`.",
            "On `allocate`, split the leftmost free node with `length >= size`; on `freeMemory(mID)`, mark each owned node free (`mID = 0`) and immediately merge it with `node.prev` and/or `node.next` whenever they are also free.",
        ],
        "explanations": [
            "Allocations fill indices 0,1,2; freeing mID 2 opens [1,1]; allocate(3,4) skips [1,1] to take [3..5]; freeing mID 1 frees 3 units across [0,1] and [6].",
            "Works on a 10^9 address space: freeing the first 400M block lets a subsequent 300M allocation succeed at address 0.",
            "Freeing mIDs 1, 3, then 2 coalesces all three regions back into a single 10-unit free block so allocate(10, 5) returns 0.",
        ],
        "time": "O(B) allocate, O(k) free",
        "space": "O(B)",
        "kind": "design",
        "className": "MemoryAllocator",
        "ctor_params": [("n", "int")],
        "methods": [
            {"name": "allocate", "params": [("size", "int"), ("mID", "int")], "ret": "int"},
            {"name": "freeMemory", "params": [("mID", "int")], "ret": "int"},
        ],
        "py_full": """class _SegNode:
    __slots__ = ("start", "length", "mid", "prev", "next")

    def __init__(self, start: int = 0, length: int = 0, mid: int = 0):
        self.start = start
        self.length = length
        self.mid = mid
        self.prev: "_SegNode | None" = None
        self.next: "_SegNode | None" = None


class MemoryAllocator:
    def __init__(self, n: int):
        self.head = _SegNode()
        self.tail = _SegNode()
        first = _SegNode(0, n, 0)
        self.head.next = first
        first.prev = self.head
        first.next = self.tail
        self.tail.prev = first
        self.owned: dict[int, list[_SegNode]] = {}

    def _unlink(self, node: _SegNode) -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def _insert_before(self, ref: _SegNode, node: _SegNode) -> None:
        node.prev = ref.prev
        node.next = ref
        ref.prev.next = node
        ref.prev = node

    def allocate(self, size: int, mID: int) -> int:
        curr = self.head.next
        while curr is not self.tail:
            if curr.mid == 0 and curr.length >= size:
                addr = curr.start
                if curr.length == size:
                    curr.mid = mID
                    alloc = curr
                else:
                    alloc = _SegNode(addr, size, mID)
                    curr.start += size
                    curr.length -= size
                    self._insert_before(curr, alloc)
                self.owned.setdefault(mID, []).append(alloc)
                return addr
            curr = curr.next
        return -1

    def freeMemory(self, mID: int) -> int:
        nodes = self.owned.pop(mID, None)
        if not nodes:
            return 0
        freed = 0
        for node in nodes:
            freed += node.length
            node.mid = 0
            if node.prev is not self.head and node.prev.mid == 0:
                left = node.prev
                node.start = left.start
                node.length += left.length
                self._unlink(left)
            if node.next is not self.tail and node.next.mid == 0:
                right = node.next
                node.length += right.length
                self._unlink(right)
        return freed
""",
        "java_full": """class MemoryAllocator {
    private static class Node {
        int start, length, mid;
        Node prev, next;
        Node(int start, int length, int mid) {
            this.start = start;
            this.length = length;
            this.mid = mid;
        }
    }

    private final Node head = new Node(0, 0, -1);
    private final Node tail = new Node(0, 0, -1);
    private final Map<Integer, List<Node>> owned = new HashMap<>();

    public MemoryAllocator(int n) {
        Node first = new Node(0, n, 0);
        head.next = first;
        first.prev = head;
        first.next = tail;
        tail.prev = first;
    }

    private void unlink(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    private void insertBefore(Node ref, Node node) {
        node.prev = ref.prev;
        node.next = ref;
        ref.prev.next = node;
        ref.prev = node;
    }

    public int allocate(int size, int mID) {
        Node curr = head.next;
        while (curr != tail) {
            if (curr.mid == 0 && curr.length >= size) {
                int addr = curr.start;
                Node alloc;
                if (curr.length == size) {
                    curr.mid = mID;
                    alloc = curr;
                } else {
                    alloc = new Node(addr, size, mID);
                    curr.start += size;
                    curr.length -= size;
                    insertBefore(curr, alloc);
                }
                owned.computeIfAbsent(mID, k -> new ArrayList<>()).add(alloc);
                return addr;
            }
            curr = curr.next;
        }
        return -1;
    }

    public int freeMemory(int mID) {
        List<Node> nodes = owned.remove(mID);
        if (nodes == null || nodes.isEmpty()) {
            return 0;
        }
        int freed = 0;
        for (Node node : nodes) {
            freed += node.length;
            node.mid = 0;
            if (node.prev != head && node.prev.mid == 0) {
                Node left = node.prev;
                node.start = left.start;
                node.length += left.length;
                unlink(left);
            }
            if (node.next != tail && node.next.mid == 0) {
                Node right = node.next;
                node.length += right.length;
                unlink(right);
            }
        }
        return freed;
    }
}
""",
        "visible": [
            {
                "ops": ["MemoryAllocator", "allocate", "allocate", "allocate", "freeMemory", "allocate", "allocate", "allocate", "freeMemory", "allocate", "freeMemory"],
                "args": [[10], [1, 1], [1, 2], [1, 3], [2], [3, 4], [1, 1], [1, 1], [1], [10, 2], [7]],
            },
            {
                "ops": ["MemoryAllocator", "allocate", "allocate", "allocate", "freeMemory", "allocate"],
                "args": [[1000000000], [400000000, 1], [400000000, 2], [300000000, 3], [1], [300000000, 3]],
            },
            {
                "ops": ["MemoryAllocator", "allocate", "allocate", "allocate", "freeMemory", "freeMemory", "freeMemory", "allocate"],
                "args": [[10], [3, 1], [4, 2], [3, 3], [1], [3], [2], [10, 5]],
            },
        ],
        "hidden_fn": "gen_hidden_75",
    },
    {
        "slug": "76-design-skiplist",
        "title": "Design Skiplist",
        "difficulty": "Hard",
        "subtopic": "LRU Design",
        "companies": ["Google", "Meta", "Amazon", "Microsoft", "Bloomberg"],
        "desc": (
            "Design a **Skiplist** (a probabilistic multi-level linked list supporting expected `O(log n)` search, "
            "insertion, and deletion of integers, including duplicates) without using built-in balanced tree maps:\n"
            "- `Skiplist()` initializes an empty skiplist.\n"
            "- `boolean search(int target)` returns `true` if `target` exists in the skiplist, otherwise `false`.\n"
            "- `void add(int num)` inserts `num` into the skiplist (duplicate values are allowed).\n"
            "- `boolean erase(int num)` removes **one** occurrence of `num` from the skiplist and returns `true`; "
            "if `num` is not present, returns `false`."
        ),
        "cons": [
            "-10^5 <= num, target <= 10^5",
            "At most 3000 calls will be made across search, add, and erase.",
        ],
        "hints": [
            "Represent each node with a `forward` pointer array of its randomly chosen height (up to `MAX_LEVEL = 16`, flipping a coin with probability 0.5 per extra level) and maintain a sentinel `head` node.",
            "For `add` and `erase`, traverse from the highest active level down to level 0, recording the rightmost node strictly less than `num` at each level in an `update` array so pointer relinking is O(1) per level.",
        ],
        "explanations": [
            "After adding 1, 2, 3, search(0) is false; after adding 4, search(1) is true; erasing 1 succeeds so subsequent search(1) is false.",
            "Adding 5 twice stores two occurrences; erasing 5 once leaves one copy still searchable, and erasing a second time removes it completely.",
            "Searching or erasing from an empty skiplist returns false; negative values and zero work identically to positive integers.",
        ],
        "time": "O(log n) expected",
        "space": "O(n)",
        "kind": "design",
        "className": "Skiplist",
        "ctor_params": [],
        "methods": [
            {"name": "search", "params": [("target", "int")], "ret": "boolean"},
            {"name": "add", "params": [("num", "int")], "ret": "void"},
            {"name": "erase", "params": [("num", "int")], "ret": "boolean"},
        ],
        "py_full": """import random


class _SkipNode:
    __slots__ = ("val", "forward")

    def __init__(self, val: int, level: int):
        self.val = val
        self.forward: list[_SkipNode | None] = [None] * level


class Skiplist:
    MAX_LEVEL = 16

    def __init__(self):
        self.head = _SkipNode(-10**9, self.MAX_LEVEL)
        self.level = 1
        self.rng = random.Random(42)

    def _random_level(self) -> int:
        lvl = 1
        while lvl < self.MAX_LEVEL and self.rng.getrandbits(1):
            lvl += 1
        return lvl

    def search(self, target: int) -> bool:
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].val < target:
                curr = curr.forward[i]
        cand = curr.forward[0]
        return cand is not None and cand.val == target

    def add(self, num: int) -> None:
        update = [self.head] * self.MAX_LEVEL
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].val < num:
                curr = curr.forward[i]
            update[i] = curr
        lvl = self._random_level()
        if lvl > self.level:
            self.level = lvl
        node = _SkipNode(num, lvl)
        for i in range(lvl):
            node.forward[i] = update[i].forward[i]
            update[i].forward[i] = node

    def erase(self, num: int) -> bool:
        update = [self.head] * self.MAX_LEVEL
        curr = self.head
        for i in range(self.level - 1, -1, -1):
            while curr.forward[i] is not None and curr.forward[i].val < num:
                curr = curr.forward[i]
            update[i] = curr
        target = curr.forward[0]
        if target is None or target.val != num:
            return False
        for i in range(len(target.forward)):
            if update[i].forward[i] is target:
                update[i].forward[i] = target.forward[i]
        while self.level > 1 and self.head.forward[self.level - 1] is None:
            self.level -= 1
        return True
""",
        "java_full": """class Skiplist {
    private static final int MAX_LEVEL = 16;

    private static class Node {
        int val;
        Node[] forward;
        Node(int val, int level) {
            this.val = val;
            this.forward = new Node[level];
        }
    }

    private final Node head = new Node(Integer.MIN_VALUE, MAX_LEVEL);
    private int level = 1;
    private final Random rng = new Random(42);

    public Skiplist() {
    }

    private int randomLevel() {
        int lvl = 1;
        while (lvl < MAX_LEVEL && rng.nextBoolean()) {
            lvl++;
        }
        return lvl;
    }

    public boolean search(int target) {
        Node curr = head;
        for (int i = level - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < target) {
                curr = curr.forward[i];
            }
        }
        Node cand = curr.forward[0];
        return cand != null && cand.val == target;
    }

    public void add(int num) {
        Node[] update = new Node[MAX_LEVEL];
        Arrays.fill(update, head);
        Node curr = head;
        for (int i = level - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < num) {
                curr = curr.forward[i];
            }
            update[i] = curr;
        }
        int lvl = randomLevel();
        if (lvl > level) {
            level = lvl;
        }
        Node node = new Node(num, lvl);
        for (int i = 0; i < lvl; i++) {
            node.forward[i] = update[i].forward[i];
            update[i].forward[i] = node;
        }
    }

    public boolean erase(int num) {
        Node[] update = new Node[MAX_LEVEL];
        Arrays.fill(update, head);
        Node curr = head;
        for (int i = level - 1; i >= 0; i--) {
            while (curr.forward[i] != null && curr.forward[i].val < num) {
                curr = curr.forward[i];
            }
            update[i] = curr;
        }
        Node target = curr.forward[0];
        if (target == null || target.val != num) {
            return false;
        }
        for (int i = 0; i < target.forward.length; i++) {
            if (update[i].forward[i] == target) {
                update[i].forward[i] = target.forward[i];
            }
        }
        while (level > 1 && head.forward[level - 1] == null) {
            level--;
        }
        return true;
    }
}
""",
        "visible": [
            {
                "ops": ["Skiplist", "add", "add", "add", "search", "add", "search", "erase", "erase", "search"],
                "args": [[], [1], [2], [3], [0], [4], [1], [0], [1], [1]],
            },
            {
                "ops": ["Skiplist", "add", "add", "search", "erase", "search", "erase", "search"],
                "args": [[], [5], [5], [5], [5], [5], [5], [5]],
            },
            {
                "ops": ["Skiplist", "search", "erase", "add", "add", "search", "erase", "search"],
                "args": [[], [10], [10], [-3], [0], [-3], [-3], [0]],
            },
        ],
        "hidden_fn": "gen_hidden_76",
    },
])


def gen_hidden_71() -> list[dict]:
    tests = [
        {"ops": ["MRUQueue", "fetch", "fetch", "fetch"], "args": [[2], [1], [1], [2]]},
        {"ops": ["MRUQueue", "fetch", "fetch", "fetch", "fetch"], "args": [[3], [2], [2], [1], [3]]},
        {"ops": ["MRUQueue", "fetch", "fetch", "fetch", "fetch", "fetch"], "args": [[5], [5], [4], [3], [2], [1]]},
        {"ops": ["MRUQueue", "fetch", "fetch", "fetch", "fetch", "fetch"], "args": [[5], [1], [1], [1], [1], [1]]},
        {"ops": ["MRUQueue", "fetch", "fetch", "fetch", "fetch", "fetch", "fetch"], "args": [[10], [1], [10], [5], [5], [2], [9]]},
        {"ops": ["MRUQueue"] + ["fetch"] * 12, "args": [[16]] + [[k] for k in [4, 8, 12, 16, 1, 5, 9, 13, 3, 7, 11, 15]]},
        {"ops": ["MRUQueue"] + ["fetch"] * 20, "args": [[25]] + [[(i * 7) % 25 + 1] for i in range(20)]},
    ]
    rng1 = random.Random(7101)
    tests.append({"ops": ["MRUQueue"] + ["fetch"] * 120, "args": [[100]] + [[rng1.randint(1, 100)] for _ in range(120)]})
    rng2 = random.Random(7102)
    tests.append({"ops": ["MRUQueue"] + ["fetch"] * 800, "args": [[1000]] + [[rng2.randint(1, 1000)] for _ in range(800)]})
    return tests


def gen_hidden_72() -> list[dict]:
    tests = [
        {
            "ops": ["TTLLRUCache", "get", "put", "get", "get"],
            "args": [[1], [5, 0], [5, 50, 1, 1], [5, 1], [5, 2]],
        },
        {
            "ops": ["TTLLRUCache", "put", "put", "get", "get"],
            "args": [[1], [1, 10, 0, 10], [2, 20, 1, 10], [1, 2], [2, 2]],
        },
        {
            "ops": ["TTLLRUCache", "put", "put", "put", "get", "get", "get"],
            "args": [[2], [1, 1, 0, 5], [2, 2, 0, 5], [3, 3, 5, 5], [1, 6], [2, 6], [3, 6]],
        },
        {
            "ops": ["TTLLRUCache", "put", "put", "put", "get", "get"],
            "args": [[2], [1, 10, 1, 2], [2, 20, 1, 10], [3, 30, 3, 10], [2, 4], [3, 4]],
        },
        {
            "ops": ["TTLLRUCache", "put", "put", "put", "get", "get", "get"],
            "args": [[2], [1, 10, 0, 100], [1, 20, 5, 2], [2, 30, 6, 100], [1, 6], [1, 7], [2, 7]],
        },
        {
            "ops": ["TTLLRUCache", "put", "put", "put", "get", "put", "get", "get", "get"],
            "args": [[3], [1, 1, 0, 20], [2, 2, 1, 20], [3, 3, 2, 20], [1, 3], [4, 4, 4, 20], [2, 5], [1, 5], [3, 5]],
        },
        {
            "ops": ["TTLLRUCache", "put", "put", "get", "put", "get", "get"],
            "args": [[2], [10, 100, 10, 5], [20, 200, 10, 5], [10, 12], [30, 300, 12, 5], [20, 13], [10, 14]],
        },
    ]
    for seed, cap, count in [(7201, 5, 100), (7202, 40, 600)]:
        rng = random.Random(seed)
        ops = ["TTLLRUCache"]
        args = [[cap]]
        t = 0
        for _ in range(count):
            t += rng.randint(0, 3)
            if rng.random() < 0.55:
                ops.append("put")
                args.append([rng.randint(1, cap * 2), rng.randint(0, 10000), t, rng.randint(1, 25)])
            else:
                ops.append("get")
                args.append([rng.randint(1, cap * 2), t])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_73() -> list[dict]:
    tests = [
        {
            "ops": ["PlaylistManager", "getCurrent", "playNext", "playPrev", "removeSong", "moveToFront", "getCurrent"],
            "args": [[], [], [], [], [99], [99], []],
        },
        {
            "ops": ["PlaylistManager", "addSong", "getCurrent", "playNext", "getCurrent", "playPrev", "getCurrent"],
            "args": [[], [7], [], [], [], [], []],
        },
        {
            "ops": ["PlaylistManager", "addSong", "addSong", "addSong", "moveToFront", "getCurrent", "playNext", "getCurrent"],
            "args": [[], [1], [2], [3], [1], [], [], []],
        },
        {
            "ops": ["PlaylistManager", "addSong", "addSong", "addSong", "playNext", "playNext", "moveToFront", "getCurrent", "playPrev", "getCurrent", "playNext", "getCurrent"],
            "args": [[], [1], [2], [3], [], [], [3], [], [], [], [], []],
        },
        {
            "ops": ["PlaylistManager", "addSong", "addSong", "addSong", "removeSong", "getCurrent", "playNext", "getCurrent"],
            "args": [[], [10], [20], [30], [20], [], [], []],
        },
        {
            "ops": ["PlaylistManager", "addSong", "addSong", "removeSong", "removeSong", "addSong", "getCurrent"],
            "args": [[], [4], [5], [4], [5], [6], []],
        },
        {
            "ops": ["PlaylistManager", "addSong", "addSong", "addSong", "addSong", "playNext", "moveToFront", "removeSong", "getCurrent", "playPrev", "getCurrent"],
            "args": [[], [1], [2], [3], [4], [], [4], [2], [], [], []],
        },
    ]
    for seed, count in [(7301, 120), (7302, 700)]:
        rng = random.Random(seed)
        ops = ["PlaylistManager"]
        args = [[]]
        pool = list(range(1, 60))
        for _ in range(count):
            r = rng.random()
            if r < 0.25:
                ops.append("addSong")
                args.append([rng.choice(pool)])
            elif r < 0.42:
                ops.append("playNext")
                args.append([])
            elif r < 0.59:
                ops.append("playPrev")
                args.append([])
            elif r < 0.74:
                ops.append("removeSong")
                args.append([rng.choice(pool)])
            elif r < 0.87:
                ops.append("moveToFront")
                args.append([rng.choice(pool)])
            else:
                ops.append("getCurrent")
                args.append([])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_74() -> list[dict]:
    tests = [
        {"ops": ["SnakeGame", "move", "move"], "args": [[1, 1, []], ["R"], ["D"]]},
        {"ops": ["SnakeGame", "move", "move", "move"], "args": [[3, 1, [[0, 1], [0, 2]]], ["R"], ["R"], ["R"]]},
        {"ops": ["SnakeGame", "move", "move", "move", "move"], "args": [[1, 3, [[1, 0], [2, 0]]], ["D"], ["D"], ["U"], ["D"]]},
        {"ops": ["SnakeGame", "move", "move", "move", "move"], "args": [[2, 2, []], ["R"], ["D"], ["L"], ["U"]]},
        {"ops": ["SnakeGame", "move", "move", "move", "move", "move"], "args": [[3, 3, [[0, 1], [1, 1], [1, 0]]], ["R"], ["D"], ["L"], ["U"], ["R"]]},
        {"ops": ["SnakeGame", "move", "move", "move", "move", "move"], "args": [[4, 4, [[0, 1], [0, 2], [0, 3]]], ["R"], ["R"], ["R"], ["L"], ["D"]]},
        {"ops": ["SnakeGame", "move", "move", "move"], "args": [[5, 5, [[2, 2]]], ["U"], ["R"], ["D"]]},
        {
            "ops": ["SnakeGame"] + ["move"] * 18,
            "args": [[4, 4, [[0, 1], [0, 2], [0, 3], [1, 3], [2, 3], [3, 3]]]]
            + [[d] for d in ["R", "R", "R", "D", "D", "D", "L", "L", "L", "U", "U", "R", "R", "D", "L", "L", "U", "U"]],
        },
    ]
    # Larger performance test: snake weaves across a 30x30 board eating food along the way
    moves = []
    food = []
    r, c = 0, 0
    for row in range(25):
        if row % 2 == 0:
            for col in range(1, 25):
                moves.append(["R"])
                if (row + col) % 5 == 0:
                    food.append([row, col])
            if row < 24:
                moves.append(["D"])
        else:
            for col in range(23, -1, -1):
                moves.append(["L"])
                if (row + col) % 5 == 0:
                    food.append([row, col])
            if row < 24:
                moves.append(["D"])
    tests.append({"ops": ["SnakeGame"] + ["move"] * len(moves), "args": [[25, 25, food]] + moves})
    return tests


def gen_hidden_75() -> list[dict]:
    tests = [
        {"ops": ["MemoryAllocator", "allocate", "freeMemory", "allocate"], "args": [[1], [1, 1], [1], [1, 2]]},
        {"ops": ["MemoryAllocator", "allocate", "allocate", "freeMemory"], "args": [[5], [6, 1], [5, 1], [1]]},
        {"ops": ["MemoryAllocator", "allocate", "allocate", "freeMemory", "allocate"], "args": [[10], [4, 1], [4, 1], [1], [9, 2]]},
        {"ops": ["MemoryAllocator", "allocate", "allocate", "allocate", "freeMemory", "allocate", "allocate"], "args": [[12], [4, 1], [4, 2], [4, 3], [2], [2, 4], [2, 5]]},
        {"ops": ["MemoryAllocator", "freeMemory", "allocate", "freeMemory", "freeMemory"], "args": [[20], [9], [10, 3], [3], [3]]},
        {"ops": ["MemoryAllocator", "allocate", "allocate", "allocate", "freeMemory", "freeMemory", "allocate"], "args": [[100], [30, 1], [40, 2], [30, 3], [2], [1], [70, 4]]},
        {"ops": ["MemoryAllocator", "allocate", "allocate", "allocate", "freeMemory", "freeMemory", "allocate"], "args": [[100], [30, 1], [40, 2], [30, 3], [2], [3], [70, 4]]},
    ]
    for seed, cap, count in [(7501, 500, 100), (7502, 1000000000, 500)]:
        rng = random.Random(seed)
        ops = ["MemoryAllocator"]
        args = [[cap]]
        max_sz = max(1, cap // 25)
        for _ in range(count):
            if rng.random() < 0.7:
                ops.append("allocate")
                args.append([rng.randint(1, max_sz), rng.randint(1, 25)])
            else:
                ops.append("freeMemory")
                args.append([rng.randint(1, 25)])
        tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_76() -> list[dict]:
    tests = [
        {"ops": ["Skiplist", "search", "erase"], "args": [[], [0], [0]]},
        {"ops": ["Skiplist", "add", "search", "erase", "search", "erase"], "args": [[], [7], [7], [7], [7], [7]]},
        {"ops": ["Skiplist", "add", "add", "add", "add", "search", "search", "erase", "search"], "args": [[], [10], [5], [15], [1], [1], [15], [5], [5]]},
        {"ops": ["Skiplist", "add", "add", "add", "erase", "erase", "erase", "erase"], "args": [[], [3], [3], [3], [3], [3], [3], [3]]},
        {"ops": ["Skiplist", "add", "add", "add", "add", "search", "erase", "search"], "args": [[], [-100000], [100000], [0], [-1], [-100000], [-100000], [100000]]},
        {
            "ops": ["Skiplist"] + ["add"] * 10 + ["search"] * 5 + ["erase"] * 5 + ["search"] * 5,
            "args": [[]] + [[i] for i in range(10, 0, -1)] + [[i] for i in [1, 5, 10, 0, 11]] + [[i] for i in [2, 4, 6, 8, 10]] + [[i] for i in [2, 3, 6, 7, 10]],
        },
        {
            "ops": ["Skiplist"] + ["add"] * 10 + ["erase"] * 10 + ["search"] * 3,
            "args": [[]] + [[i] for i in range(1, 11)] + [[i] for i in range(1, 11)] + [[1], [5], [10]],
        },
    ]
    for seed, count, hi in [(7601, 150, 40), (7602, 1200, 400)]:
        rng = random.Random(seed)
        ops = ["Skiplist"]
        args = [[]]
        for _ in range(count):
            r = rng.random()
            v = rng.randint(-hi, hi)
            if r < 0.45:
                ops.append("add")
            elif r < 0.75:
                ops.append("search")
            else:
                ops.append("erase")
            args.append([v])
        tests.append({"ops": ops, "args": args})
    return tests


HIDDEN_GENERATORS = {
    "gen_hidden_71": gen_hidden_71,
    "gen_hidden_72": gen_hidden_72,
    "gen_hidden_73": gen_hidden_73,
    "gen_hidden_74": gen_hidden_74,
    "gen_hidden_75": gen_hidden_75,
    "gen_hidden_76": gen_hidden_76,
}


def main():
    assert len(TASKS) == 30, f"Expected 30 tasks, got {len(TASKS)}"
    expected_nums = list(range(47, 77))
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

    print(f"Generated {len(TASKS)} linked-lists problems (47-76)")


if __name__ == "__main__":
    main()
