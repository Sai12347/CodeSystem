#!/usr/bin/env python3
"""Generate linked-lists problems 17-46 (batch 1) for AlgoPlay."""
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


def make_sorted_list(seed: int, n: int, lo: int, hi: int) -> list[int]:
    return sorted(make_rng_list(seed, n, lo, hi))


def make_unique_sorted_list(seed: int, n: int, step_max: int = 5, start: int = -500) -> list[int]:
    rng = random.Random(seed)
    out = []
    cur = start
    for _ in range(n):
        cur += rng.randint(1, step_max)
        out.append(cur)
    return out


TASKS = [
    # -------------------------------------------------------------------------
    # 17-22: Pointers & Nodes
    # -------------------------------------------------------------------------
    {
        "slug": "17-remove-linked-list-elements",
        "title": "Remove Linked List Elements",
        "difficulty": "Easy",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list and an integer `val`, remove all nodes of the linked list "
            "that have `Node.val == val`, and return the new head of the modified list.\n\n"
            "If all nodes are removed or the input list is empty, return `null` (`None` in Python)."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "1 <= Node.val <= 50",
            "0 <= val <= 50",
        ],
        "hints": [
            "Attach a sentinel dummy node before `head` so removing the original head node follows the exact same pointer update as removing any interior node.",
            "Advance the `curr` pointer only when `curr.next.val != val`; when deleting `curr.next`, re-link `curr.next = curr.next.next` and inspect the new successor on the next iteration.",
        ],
        "explanations": [
            "Both nodes with value 6 (at positions 3 and 7) are removed, leaving [1, 2, 3, 4, 5].",
            "An empty list has no nodes to remove, so return null.",
            "Every node has value 7, so removing all of them produces an empty list (null).",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "removeElements",
        "params": [("head", "ListNode"), ("val", "int")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0, head)
        curr = dummy
        while curr.next is not None:
            if curr.next.val == val:
                curr.next = curr.next.next
            else:
                curr = curr.next
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0, head);
        ListNode curr = dummy;
        while (curr.next != null) {
            if (curr.next.val == val) {
                curr.next = curr.next.next;
            } else {
                curr = curr.next;
            }
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 6, 3, 4, 5, 6], "val": 6},
            {"head": [], "val": 1},
            {"head": [7, 7, 7, 7], "val": 7},
        ],
        "hidden": [
            {"head": [1], "val": 1},
            {"head": [1], "val": 2},
            {"head": [5, 5, 1, 2, 3], "val": 5},
            {"head": [1, 2, 3, 5, 5], "val": 5},
            {"head": [1, 4, 4, 4, 2, 4, 3], "val": 4},
            {"head": [1, 2, 3, 4, 5], "val": 0},
            {"head": [50, 1, 50, 2, 50], "val": 50},
            {"head": [2, 1, 2, 1, 2, 1], "val": 1},
            {"head": make_rng_list(1701, 2500, 1, 50), "val": 25},
        ],
    },
    {
        "slug": "18-remove-duplicates-from-sorted-list",
        "title": "Remove Duplicates from Sorted List",
        "difficulty": "Easy",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Google", "Meta", "Microsoft"],
        "desc": (
            "Given the `head` of a singly linked list sorted in non-decreasing order, delete all duplicate nodes "
            "such that each distinct value appears only once. Return the head of the resulting sorted linked list.\n\n"
            "Modify the list in-place in `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 3000].",
            "-100 <= Node.val <= 100",
            "The list is guaranteed to be sorted in non-decreasing order.",
        ],
        "hints": [
            "Because the list is sorted, all duplicates of any value appear consecutively.",
            "Compare `curr.val` with `curr.next.val`: if equal, bypass `curr.next`; otherwise move `curr` forward by one step.",
        ],
        "explanations": [
            "The duplicate 1 is removed, yielding [1, 2].",
            "Duplicate copies of 1 and 3 are bypassed, leaving [1, 2, 3].",
            "An empty list remains empty (null).",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "deleteDuplicates",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        curr = head
        while curr is not None and curr.next is not None:
            if curr.val == curr.next.val:
                curr.next = curr.next.next
            else:
                curr = curr.next
        return head""",
        "java": """        ListNode curr = head;
        while (curr != null && curr.next != null) {
            if (curr.val == curr.next.val) {
                curr.next = curr.next.next;
            } else {
                curr = curr.next;
            }
        }
        return head;""",
        "visible": [
            {"head": [1, 1, 2]},
            {"head": [1, 1, 2, 3, 3]},
            {"head": []},
        ],
        "hidden": [
            {"head": [0]},
            {"head": [-100, -100, -100]},
            {"head": [-5, -5, -2, 0, 0, 0, 4, 4]},
            {"head": [1, 2, 3, 4, 5]},
            {"head": [1, 1, 1, 1, 2, 2, 2, 3]},
            {"head": [10, 10]},
            {"head": [-100, 0, 100]},
            {"head": [1, 2, 2, 2, 2, 3, 4, 4, 5, 5, 5]},
            {"head": make_sorted_list(1801, 2000, -100, 100)},
        ],
    },
    {
        "slug": "19-remove-duplicates-from-sorted-list-ii",
        "title": "Remove Duplicates from Sorted List II",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Microsoft", "Meta", "Adobe"],
        "desc": (
            "Given the `head` of a singly linked list sorted in non-decreasing order, delete **all** nodes that "
            "have duplicate values, leaving only values that appeared **strictly once** in the original list. "
            "Return the head of the resulting sorted linked list, or `null` (`None` in Python) if no unique values remain."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 3000].",
            "-100 <= Node.val <= 100",
            "The list is guaranteed to be sorted in non-decreasing order.",
        ],
        "hints": [
            "Use a dummy node before `head` and maintain `prev` pointing to the last confirmed unique node.",
            "Whenever `curr.val == curr.next.val`, skip every node with that value and set `prev.next` to the first node after the duplicate run without advancing `prev`.",
        ],
        "explanations": [
            "Values 3 and 4 appear more than once and are completely removed, leaving [1, 2, 5].",
            "Value 1 appears three times and is completely removed, leaving [2, 3].",
            "All values appear multiple times, so the resulting list is empty (null).",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "deleteAllDuplicates",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0, head)
        prev = dummy
        curr = head
        while curr is not None:
            if curr.next is not None and curr.val == curr.next.val:
                dup = curr.val
                while curr is not None and curr.val == dup:
                    curr = curr.next
                prev.next = curr
            else:
                prev = curr
                curr = curr.next
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        ListNode curr = head;
        while (curr != null) {
            if (curr.next != null && curr.val == curr.next.val) {
                int dup = curr.val;
                while (curr != null && curr.val == dup) {
                    curr = curr.next;
                }
                prev.next = curr;
            } else {
                prev = curr;
                curr = curr.next;
            }
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 3, 4, 4, 5]},
            {"head": [1, 1, 1, 2, 3]},
            {"head": [2, 2, 4, 4]},
        ],
        "hidden": [
            {"head": []},
            {"head": [7]},
            {"head": [1, 2, 3, 4]},
            {"head": [-100, -100, -50, 0, 0, 50, 100, 100]},
            {"head": [1, 1, 2, 2, 3]},
            {"head": [1, 2, 2, 3, 3]},
            {"head": [1, 2, 2, 3, 4, 4, 5, 5]},
            {"head": [-10, -10, -10, -10]},
            {"head": make_sorted_list(1901, 2000, -100, 100)},
        ],
    },
    {
        "slug": "20-delete-n-nodes-after-m-nodes",
        "title": "Delete N Nodes After M Nodes",
        "difficulty": "Easy",
        "subtopic": "Pointers & Nodes",
        "companies": ["Microsoft", "Amazon", "Oracle"],
        "desc": (
            "Given the `head` of a singly linked list and two positive integers `m` and `n`, traverse the list "
            "from the beginning by repeating the following steps until reaching the end:\n"
            "1. Keep the next `m` nodes (including the current node).\n"
            "2. Remove the next `n` nodes.\n\n"
            "Return the `head` of the modified linked list after all removals."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "1 <= Node.val <= 10^6",
            "1 <= m, n <= 1000",
        ],
        "hints": [
            "Walk `m - 1` steps from the start of each kept block to land on the last node to keep.",
            "From that node, advance a second pointer `n` steps forward (stopping early if `null` is reached), then rewire `lastKept.next` to skip the deleted segment.",
        ],
        "explanations": [
            "Keep [1, 2], delete [3, 4, 5], keep [6, 7], delete [8, 9, 10], keep [11, 12], delete [13].",
            "Keep [1], delete [2, 3, 4], keep [5], delete [6, 7, 8], keep [9], delete [10, 11].",
            "Keeping 3 nodes already reaches the end of the 3-node list, so nothing is deleted.",
        ],
        "time": "O(L)",
        "space": "O(1)",
        "kind": "function",
        "method": "deleteNodes",
        "params": [("head", "ListNode"), ("m", "int"), ("n", "int")],
        "ret": "ListNode",
        "py": """        curr = head
        while curr is not None:
            for _ in range(m - 1):
                if curr.next is None:
                    return head
                curr = curr.next
            skip = curr.next
            for _ in range(n):
                if skip is None:
                    break
                skip = skip.next
            curr.next = skip
            curr = skip
        return head""",
        "java": """        ListNode curr = head;
        while (curr != null) {
            for (int i = 1; i < m; i++) {
                if (curr.next == null) {
                    return head;
                }
                curr = curr.next;
            }
            ListNode skip = curr.next;
            for (int i = 0; i < n && skip != null; i++) {
                skip = skip.next;
            }
            curr.next = skip;
            curr = skip;
        }
        return head;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13], "m": 2, "n": 3},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11], "m": 1, "n": 3},
            {"head": [9, 3, 7], "m": 3, "n": 2},
        ],
        "hidden": [
            {"head": [42], "m": 1, "n": 1},
            {"head": [1, 2], "m": 1, "n": 1},
            {"head": [1, 2, 3, 4, 5, 6], "m": 1, "n": 1},
            {"head": [1, 2, 3, 4, 5, 6], "m": 2, "n": 10},
            {"head": [1, 2, 3, 4, 5], "m": 10, "n": 1},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8], "m": 3, "n": 1},
            {"head": [5, 4, 3, 2, 1, 6, 7, 8, 9], "m": 2, "n": 2},
            {"head": list(range(1, 21)), "m": 4, "n": 5},
            {"head": list(range(1, 2501)), "m": 7, "n": 5},
        ],
    },
    {
        "slug": "21-odd-even-linked-list",
        "title": "Odd Even Linked List",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list, group all nodes positioned at **odd 1-based indices** "
            "together followed by the nodes positioned at **even 1-based indices**, and return the reordered list.\n\n"
            "The relative order inside both the odd group and the even group must remain identical to the input. "
            "Solve the problem in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^6 <= Node.val <= 10^6",
        ],
        "hints": [
            "Maintain two running tail pointers `odd` (starting at `head`) and `even` (starting at `head.next`), and save `evenHead = even`.",
            "In each step link `odd.next = even.next`, advance `odd`, link `even.next = odd.next`, and advance `even`; finally connect `odd.next = evenHead`.",
        ],
        "explanations": [
            "Odd-indexed nodes [1, 3, 5] come first, followed by even-indexed nodes [2, 4].",
            "Odd-indexed nodes [2, 3, 6, 7] precede even-indexed nodes [1, 5, 4].",
            "An empty list remains empty (null).",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "oddEvenList",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None:
            return head
        odd = head
        even = head.next
        even_head = even
        while even is not None and even.next is not None:
            odd.next = even.next
            odd = odd.next
            even.next = odd.next
            even = even.next
        odd.next = even_head
        return head""",
        "java": """        if (head == null || head.next == null) {
            return head;
        }
        ListNode odd = head;
        ListNode even = head.next;
        ListNode evenHead = even;
        while (even != null && even.next != null) {
            odd.next = even.next;
            odd = odd.next;
            even.next = odd.next;
            even = even.next;
        }
        odd.next = evenHead;
        return head;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5]},
            {"head": [2, 1, 3, 5, 6, 4, 7]},
            {"head": []},
        ],
        "hidden": [
            {"head": [1]},
            {"head": [1, 2]},
            {"head": [1, 2, 3]},
            {"head": [1, 2, 3, 4]},
            {"head": [10, 20, 30, 40, 50, 60]},
            {"head": [-5, 0, 5, -10, 10]},
            {"head": [7, 7, 7, 7, 7, 7, 7]},
            {"head": [1, 100, 2, 200, 3, 300, 4, 400]},
            {"head": make_rng_list(2101, 2500, -100000, 100000)},
        ],
    },
    {
        "slug": "22-rotate-linked-list",
        "title": "Rotate Linked List",
        "difficulty": "Medium",
        "subtopic": "Pointers & Nodes",
        "companies": ["Amazon", "Google", "Microsoft", "LinkedIn", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list and a non-negative integer `k`, rotate the list to the right "
            "by `k` places and return the new head.\n\n"
            "One right rotation moves the last node of the list to the front. Note that `k` can be much larger "
            "than the length of the list."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 5000].",
            "-1000 <= Node.val <= 1000",
            "0 <= k <= 2 * 10^9",
        ],
        "hints": [
            "First traverse to the tail to compute the list length `n`, then reduce `k = k % n` (if `k == 0`, return `head` immediately).",
            "Temporarily connect `tail.next = head` to form a ring, walk `n - k` steps from `tail` to reach the new tail, and break the ring there.",
        ],
        "explanations": [
            "Rotating [1, 2, 3, 4, 5] right by 2 moves 4 and 5 to the front: [4, 5, 1, 2, 3].",
            "Rotating [0, 1, 2] right by 4 is equivalent to rotating by 4 % 3 = 1: [2, 0, 1].",
            "Rotating an empty list yields null.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "rotateRight",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None or k == 0:
            return head
        n = 1
        tail = head
        while tail.next is not None:
            tail = tail.next
            n += 1
        k %= n
        if k == 0:
            return head
        tail.next = head
        steps = n - k
        new_tail = tail
        for _ in range(steps):
            new_tail = new_tail.next
        new_head = new_tail.next
        new_tail.next = None
        return new_head""",
        "java": """        if (head == null || head.next == null || k == 0) {
            return head;
        }
        int n = 1;
        ListNode tail = head;
        while (tail.next != null) {
            tail = tail.next;
            n++;
        }
        k %= n;
        if (k == 0) {
            return head;
        }
        tail.next = head;
        int steps = n - k;
        ListNode newTail = tail;
        for (int i = 0; i < steps; i++) {
            newTail = newTail.next;
        }
        ListNode newHead = newTail.next;
        newTail.next = null;
        return newHead;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5], "k": 2},
            {"head": [0, 1, 2], "k": 4},
            {"head": [], "k": 5},
        ],
        "hidden": [
            {"head": [1], "k": 0},
            {"head": [1], "k": 1000000000},
            {"head": [1, 2], "k": 1},
            {"head": [1, 2], "k": 2},
            {"head": [1, 2, 3, 4, 5], "k": 0},
            {"head": [1, 2, 3, 4, 5], "k": 5},
            {"head": [1, 2, 3, 4, 5], "k": 2000000000},
            {"head": [-10, -5, 0, 5, 10, 15], "k": 17},
            {"head": list(range(1, 2001)), "k": 123456789},
        ],
    },
    # -------------------------------------------------------------------------
    # 23-28: Fast/Slow Pointer
    # -------------------------------------------------------------------------
    {
        "slug": "23-middle-of-the-linked-list",
        "title": "Middle of the Linked List",
        "difficulty": "Easy",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Google", "Meta", "Apple", "Microsoft"],
        "desc": (
            "Given the `head` of a non-empty singly linked list, return the middle node of the linked list.\n\n"
            "If the list has an even number of nodes (so there are two middle nodes), return the **second** middle node."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "1 <= Node.val <= 10^5",
        ],
        "hints": [
            "Start both `slow` and `fast` pointers at `head`.",
            "While `fast` and `fast.next` are non-null, advance `slow` by 1 node and `fast` by 2 nodes; when the loop ends, `slow` sits on the exact (or second) middle node.",
        ],
        "explanations": [
            "For 5 nodes, the middle node is 3, so the returned suffix is [3, 4, 5].",
            "For 6 nodes, the two middle nodes are 3 and 4; return the second one, giving [4, 5, 6].",
            "A single-node list returns that single node [99].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "middleNode",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        slow = head
        fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        return slow""",
        "java": """        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        return slow;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5]},
            {"head": [1, 2, 3, 4, 5, 6]},
            {"head": [99]},
        ],
        "hidden": [
            {"head": [1, 2]},
            {"head": [1, 2, 3]},
            {"head": [1, 2, 3, 4]},
            {"head": [10, 20, 30, 40, 50, 60, 70]},
            {"head": [5, 5, 5, 5, 5, 5, 5, 5]},
            {"head": [100000, 1, 50000, 2, 99999, 3, 4, 5, 6]},
            {"head": list(range(1, 51))},
            {"head": list(range(1, 52))},
            {"head": list(range(1, 2501))},
        ],
    },
    {
        "slug": "24-delete-the-middle-node-of-a-linked-list",
        "title": "Delete the Middle Node of a Linked List",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Google", "Meta", "Uber"],
        "desc": (
            "You are given the `head` of a non-empty singly linked list of length `n`. Delete the **middle node** "
            "located at 0-based index `floor(n / 2)` and return the `head` of the modified list.\n\n"
            "If the list has only 1 node, deleting it produces an empty list (`null` / `None`)."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "1 <= Node.val <= 10^5",
        ],
        "hints": [
            "Handle the single-node base case (`head.next == null`) by returning `null` directly.",
            "Give `fast` a two-step head start (`fast = head.next.next`) while `slow = head` so that when `fast` reaches the end, `slow` points to the node immediately **before** the middle node.",
        ],
        "explanations": [
            "For length 7, floor(7 / 2) = 3 (node with value 7) is removed, leaving [1, 3, 4, 1, 2, 6].",
            "For length 4, floor(4 / 2) = 2 (node with value 3) is removed, leaving [1, 2, 4].",
            "For length 1, deleting the only node leaves null.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "deleteMiddle",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None:
            return None
        slow = head
        fast = head.next.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        slow.next = slow.next.next
        return head""",
        "java": """        if (head == null || head.next == null) {
            return null;
        }
        ListNode slow = head;
        ListNode fast = head.next.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        slow.next = slow.next.next;
        return head;""",
        "visible": [
            {"head": [1, 3, 4, 7, 1, 2, 6]},
            {"head": [1, 2, 3, 4]},
            {"head": [5]},
        ],
        "hidden": [
            {"head": [2, 1]},
            {"head": [1, 2, 3]},
            {"head": [10, 20, 30, 40, 50]},
            {"head": [10, 20, 30, 40, 50, 60]},
            {"head": [7, 7, 7, 7, 7]},
            {"head": [9, 8, 7, 6, 5, 4, 3, 2]},
            {"head": list(range(1, 51))},
            {"head": list(range(1, 52))},
            {"head": list(range(1, 2502))},
        ],
    },
    {
        "slug": "25-swapping-nodes-in-a-linked-list",
        "title": "Swapping Nodes in a Linked List",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "You are given the `head` of a singly linked list and a 1-indexed integer `k`.\n\n"
            "Swap the **values** of the `k`-th node from the beginning and the `k`-th node from the end of the "
            "list, and return the `head` of the list. Solve the problem in a single traversal using `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is n, with 1 <= k <= n <= 10^4.",
            "0 <= Node.val <= 10^5",
        ],
        "hints": [
            "Walk a `lead` pointer `k - 1` steps from `head` to locate `first`, the `k`-th node from the start.",
            "Then start `second` at `head` and advance `lead` and `second` together until `lead.next` is null; `second` lands on the `k`-th node from the end.",
        ],
        "explanations": [
            "The 2nd node from the start (2) and 2nd node from the end (4) swap values to produce [1, 4, 3, 2, 5].",
            "The 5th node from the start (9) and 5th node from the end (0) swap values.",
            "When k = 1 on a 1-node list, both pointers refer to the same node so the list is unchanged.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "swapNodes",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode",
        "py": """        lead = head
        for _ in range(k - 1):
            lead = lead.next
        first = lead
        second = head
        while lead.next is not None:
            lead = lead.next
            second = second.next
        first.val, second.val = second.val, first.val
        return head""",
        "java": """        ListNode lead = head;
        for (int i = 1; i < k; i++) {
            lead = lead.next;
        }
        ListNode first = lead;
        ListNode second = head;
        while (lead.next != null) {
            lead = lead.next;
            second = second.next;
        }
        int tmp = first.val;
        first.val = second.val;
        second.val = tmp;
        return head;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5], "k": 2},
            {"head": [7, 9, 6, 6, 7, 8, 3, 0, 9, 5], "k": 5},
            {"head": [10], "k": 1},
        ],
        "hidden": [
            {"head": [1, 2], "k": 1},
            {"head": [1, 2], "k": 2},
            {"head": [1, 2, 3], "k": 2},
            {"head": [1, 2, 3, 4, 5], "k": 1},
            {"head": [1, 2, 3, 4, 5], "k": 5},
            {"head": [1, 2, 3, 4, 5], "k": 4},
            {"head": [10, 20, 30, 40, 50, 60], "k": 3},
            {"head": [0, 100000, 50, 25, 75, 99999], "k": 2},
            {"head": list(range(1, 2501)), "k": 777},
        ],
    },
    {
        "slug": "26-maximum-twin-sum-of-a-linked-list",
        "title": "Maximum Twin Sum of a Linked List",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Google", "Meta", "Goldman Sachs"],
        "desc": (
            "In a singly linked list of **even** length `n`, the `i`-th node (0-indexed) and the `(n - 1 - i)`-th "
            "node are called **twins** for every `0 <= i < n / 2`. The **twin sum** of a twin pair is the sum of "
            "the two nodes' values.\n\n"
            "Given the `head` of an even-length singly linked list, return the maximum twin sum across all pairs. "
            "Aim for `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes n is even and lies in the range [2, 10^4].",
            "1 <= Node.val <= 10^5",
        ],
        "hints": [
            "Use slow and fast pointers to find the start of the second half of the list.",
            "Reverse the second half in-place, then walk the first half and reversed second half in lockstep while tracking the maximum sum `first.val + second.val`.",
        ],
        "explanations": [
            "Twin pairs are (5, 1) with sum 6 and (4, 2) with sum 6, so the maximum is 6.",
            "Twin pairs are (4, 3) with sum 7 and (2, 2) with sum 4, so the maximum is 7.",
            "The only twin pair is (1, 100000) with sum 100001.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "pairSum",
        "params": [("head", "ListNode")],
        "ret": "int",
        "py": """        slow = head
        fast = head
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        prev = None
        curr = slow
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        best = 0
        left = head
        right = prev
        while right is not None:
            s = left.val + right.val
            if s > best:
                best = s
            left = left.next
            right = right.next
        return best""",
        "java": """        ListNode slow = head;
        ListNode fast = head;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode prev = null;
        ListNode curr = slow;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        int best = 0;
        ListNode left = head;
        ListNode right = prev;
        while (right != null) {
            int s = left.val + right.val;
            if (s > best) {
                best = s;
            }
            left = left.next;
            right = right.next;
        }
        return best;""",
        "visible": [
            {"head": [5, 4, 2, 1]},
            {"head": [4, 2, 2, 3]},
            {"head": [1, 100000]},
        ],
        "hidden": [
            {"head": [1, 1]},
            {"head": [100000, 100000]},
            {"head": [1, 2, 3, 4, 5, 6]},
            {"head": [10, 1, 1, 1, 1, 10]},
            {"head": [1, 50, 99, 100, 2, 3]},
            {"head": [7, 3, 9, 1, 8, 2, 6, 4]},
            {"head": [5, 5, 5, 5, 5, 5, 5, 5]},
            {"head": [1, 2, 3, 4, 100, 200, 5, 6, 7, 8]},
            {"head": make_rng_list(2601, 2500, 1, 100000)},
        ],
    },
    {
        "slug": "27-interleave-halves-of-linked-list",
        "title": "Interleave Halves of Linked List",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Amazon", "Meta", "Uber", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list of length `n`, split the list into a first half of length "
            "`ceil(n / 2)` (`a_0, a_1, ..., a_{p-1}`) and a second half of length `floor(n / 2)` "
            "(`b_0, b_1, ..., b_{q-1}`), preserving the original order within each half.\n\n"
            "Interleave the two halves alternately as `a_0 -> b_0 -> a_1 -> b_1 -> ...` (if `n` is odd, `a_{p-1}` "
            "appears at the end), and return the head of the modified list. Solve it in-place in `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 5000].",
            "-10^5 <= Node.val <= 10^5",
        ],
        "hints": [
            "Initialize `slow = head` and `fast = head.next`; advancing `slow` by 1 and `fast` by 2 stops `slow` at the tail of the first half (length `ceil(n / 2)`).",
            "Detach the second half at `second = slow.next; slow.next = null`, then weave nodes from `first` and `second` in alternating order without reversing either half.",
        ],
        "explanations": [
            "Halves [1, 2, 3] and [4, 5, 6] interleave into [1, 4, 2, 5, 3, 6].",
            "Halves [1, 2, 3] and [4, 5] interleave into [1, 4, 2, 5, 3].",
            "A 2-node list has halves [10] and [20], which stays [10, 20].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "interleaveHalves",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None:
            return head
        slow = head
        fast = head.next
        while fast is not None and fast.next is not None:
            slow = slow.next
            fast = fast.next.next
        second = slow.next
        slow.next = None
        first = head
        while second is not None:
            nxt1 = first.next
            nxt2 = second.next
            first.next = second
            second.next = nxt1
            first = nxt1
            second = nxt2
        return head""",
        "java": """        if (head == null || head.next == null) {
            return head;
        }
        ListNode slow = head;
        ListNode fast = head.next;
        while (fast != null && fast.next != null) {
            slow = slow.next;
            fast = fast.next.next;
        }
        ListNode second = slow.next;
        slow.next = null;
        ListNode first = head;
        while (second != null) {
            ListNode nxt1 = first.next;
            ListNode nxt2 = second.next;
            first.next = second;
            second.next = nxt1;
            first = nxt1;
            second = nxt2;
        }
        return head;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5, 6]},
            {"head": [1, 2, 3, 4, 5]},
            {"head": [10, 20]},
        ],
        "hidden": [
            {"head": []},
            {"head": [42]},
            {"head": [1, 2, 3]},
            {"head": [1, 2, 3, 4]},
            {"head": [-3, -2, -1, 1, 2, 3, 4]},
            {"head": [5, 5, 5, 1, 1, 1]},
            {"head": [1, 3, 5, 7, 2, 4, 6, 8]},
            {"head": list(range(1, 32))},
            {"head": list(range(1, 2501))},
        ],
    },
    {
        "slug": "28-convert-sorted-list-to-bst",
        "title": "Convert Sorted List to BST",
        "difficulty": "Medium",
        "subtopic": "Fast/Slow Pointer",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list whose elements are sorted in **strictly increasing** order, "
            "convert it to a height-balanced binary search tree (BST) and return its root.\n\n"
            "To guarantee a unique output tree, for every contiguous sublist of `m` nodes (0-indexed `0 .. m - 1`), "
            "select the node at index `floor(m / 2)` as the root of that subtree (for even `m`, this is the right-middle "
            "node reached by standard slow/fast pointers both initialized at the sublist head)."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 2000].",
            "-10^5 <= Node.val <= 10^5",
            "Values in the linked list are strictly increasing.",
        ],
        "hints": [
            "Using slow/fast pointers to split each sublist at index `floor(m / 2)` builds the exact tree in O(n log n) time.",
            "To reach O(n) time, count the total length `n` first, then simulate an in-order traversal over index range `[lo, hi]` with `mid = (lo + hi + 1) // 2`, advancing a single list cursor once per node.",
        ],
        "explanations": [
            "Middle of [-10, -3, 0, 5, 9] is 0; left [-10, -3] picks right-middle -3 and right [5, 9] picks right-middle 9.",
            "An empty list converts to an empty tree (null).",
            "For [1, 2, 3, 4], index 4//2 = 2 (value 3) is root, left [1, 2] has root 2 with left child 1, and right [4] is 4.",
        ],
        "time": "O(n)",
        "space": "O(log n)",
        "kind": "function",
        "method": "sortedListToBST",
        "params": [("head", "ListNode")],
        "ret": "TreeNode",
        "py_full": """class Solution:
    def sortedListToBST(self, head: Optional[ListNode]) -> Optional[TreeNode]:
        n = 0
        curr = head
        while curr is not None:
            n += 1
            curr = curr.next
        cursor = [head]

        def build(lo: int, hi: int) -> Optional[TreeNode]:
            if lo > hi:
                return None
            mid = (lo + hi + 1) // 2
            left = build(lo, mid - 1)
            node = TreeNode(cursor[0].val)
            cursor[0] = cursor[0].next
            node.left = left
            node.right = build(mid + 1, hi)
            return node

        return build(0, n - 1)
""",
        "java_full": """class Solution {
    private ListNode cursor;

    public TreeNode sortedListToBST(ListNode head) {
        int n = 0;
        for (ListNode curr = head; curr != null; curr = curr.next) {
            n++;
        }
        this.cursor = head;
        return build(0, n - 1);
    }

    private TreeNode build(int lo, int hi) {
        if (lo > hi) {
            return null;
        }
        int mid = (lo + hi + 1) / 2;
        TreeNode left = build(lo, mid - 1);
        TreeNode root = new TreeNode(cursor.val);
        cursor = cursor.next;
        root.left = left;
        root.right = build(mid + 1, hi);
        return root;
    }
}
""",
        "visible": [
            {"head": [-10, -3, 0, 5, 9]},
            {"head": []},
            {"head": [1, 2, 3, 4]},
        ],
        "hidden": [
            {"head": [0]},
            {"head": [1, 2]},
            {"head": [1, 2, 3]},
            {"head": [-5, -4, -3, -2, -1, 0, 1]},
            {"head": [2, 4, 6, 8, 10, 12, 14, 16]},
            {"head": [-100000, 0, 100000]},
            {"head": list(range(1, 16))},
            {"head": list(range(-30, 30, 2))},
            {"head": make_unique_sorted_list(2801, 1500, 5, -5000)},
        ],
    },
    # -------------------------------------------------------------------------
    # 29-34: Reversal
    # -------------------------------------------------------------------------
    {
        "slug": "29-reverse-linked-list-ii",
        "title": "Reverse Linked List II",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list and two 1-indexed integers `left` and `right` where "
            "`1 <= left <= right <= n`, reverse the nodes of the list from position `left` to position `right` "
            "(inclusive), and return the head of the modified list.\n\n"
            "Complete the reversal in a single pass using `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is n, with 1 <= n <= 5000.",
            "-5000 <= Node.val <= 5000",
            "1 <= left <= right <= n",
        ],
        "hints": [
            "Attach a dummy node before `head` and walk `prev` forward `left - 1` steps so `prev` sits immediately before the sublist to reverse.",
            "Keep `curr = prev.next` fixed as the growing reversed sublist's tail, and repeatedly splice `curr.next` directly after `prev` for `right - left` iterations.",
        ],
        "explanations": [
            "Reversing positions 2 through 4 of [1, 2, 3, 4, 5] turns [2, 3, 4] into [4, 3, 2], giving [1, 4, 3, 2, 5].",
            "A single-node range [1, 1] leaves [5] unchanged.",
            "Reversing positions 1 through 4 reverses the entire list into [4, 3, 2, 1].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseBetween",
        "params": [("head", "ListNode"), ("left", "int"), ("right", "int")],
        "ret": "ListNode",
        "py": """        if head is None or left == right:
            return head
        dummy = ListNode(0, head)
        prev = dummy
        for _ in range(left - 1):
            prev = prev.next
        curr = prev.next
        for _ in range(right - left):
            move = curr.next
            curr.next = move.next
            move.next = prev.next
            prev.next = move
        return dummy.next""",
        "java": """        if (head == null || left == right) {
            return head;
        }
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        for (int i = 1; i < left; i++) {
            prev = prev.next;
        }
        ListNode curr = prev.next;
        for (int i = 0; i < right - left; i++) {
            ListNode move = curr.next;
            curr.next = move.next;
            move.next = prev.next;
            prev.next = move;
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5], "left": 2, "right": 4},
            {"head": [5], "left": 1, "right": 1},
            {"head": [1, 2, 3, 4], "left": 1, "right": 4},
        ],
        "hidden": [
            {"head": [3, 5], "left": 1, "right": 2},
            {"head": [3, 5], "left": 2, "right": 2},
            {"head": [1, 2, 3, 4, 5], "left": 1, "right": 3},
            {"head": [1, 2, 3, 4, 5], "left": 3, "right": 5},
            {"head": [1, 2, 3, 4, 5], "left": 4, "right": 5},
            {"head": [-10, -5, 0, 5, 10, 15], "left": 2, "right": 5},
            {"head": [7, 7, 1, 2, 7, 7], "left": 3, "right": 4},
            {"head": list(range(1, 21)), "left": 5, "right": 16},
            {"head": list(range(1, 2501)), "left": 400, "right": 2100},
        ],
    },
    {
        "slug": "30-swap-nodes-in-pairs",
        "title": "Swap Nodes in Pairs",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list, swap every two adjacent nodes and return its new head.\n\n"
            "You must solve the problem by rewiring node links rather than modifying node values. "
            "If the list has an odd number of nodes, the final node remains in place."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 5000].",
            "0 <= Node.val <= 10^4",
        ],
        "hints": [
            "Place a dummy node before `head` and keep a `prev` pointer before the next pair `(first, second)`.",
            "Rewire `prev.next = second`, `first.next = second.next`, `second.next = first`, then advance `prev = first` for the next pair.",
        ],
        "explanations": [
            "Swapping (1, 2) and (3, 4) produces [2, 1, 4, 3].",
            "An empty list remains empty (null).",
            "With 3 nodes, (1, 2) swap while the trailing 3 stays at the end: [2, 1, 3].",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "swapPairs",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        dummy = ListNode(0, head)
        prev = dummy
        while prev.next is not None and prev.next.next is not None:
            first = prev.next
            second = first.next
            first.next = second.next
            second.next = first
            prev.next = second
            prev = first
        return dummy.next""",
        "java": """        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        while (prev.next != null && prev.next.next != null) {
            ListNode first = prev.next;
            ListNode second = first.next;
            first.next = second.next;
            second.next = first;
            prev.next = second;
            prev = first;
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 4]},
            {"head": []},
            {"head": [1, 2, 3]},
        ],
        "hidden": [
            {"head": [1]},
            {"head": [1, 2]},
            {"head": [1, 2, 3, 4, 5]},
            {"head": [1, 2, 3, 4, 5, 6]},
            {"head": [9, 9, 9, 9]},
            {"head": [10, 20, 30, 40, 50, 60, 70]},
            {"head": [0, 10000, 1, 9999, 2, 9998]},
            {"head": list(range(1, 51))},
            {"head": list(range(1, 2502))},
        ],
    },
    {
        "slug": "31-reverse-nodes-in-even-length-groups",
        "title": "Reverse Nodes in Even Length Groups",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Google", "Meta", "Oracle"],
        "desc": (
            "You are given the `head` of a non-empty singly linked list. The nodes are sequentially partitioned into "
            "contiguous groups whose target lengths are the natural numbers `1, 2, 3, 4, ...`. The final group may "
            "contain fewer nodes than its target length if the list ends early.\n\n"
            "Reverse the nodes in every group whose **actual** length is **even**, and leave every group of odd "
            "actual length unchanged. Return the `head` of the modified list in `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "0 <= Node.val <= 10^5",
        ],
        "hints": [
            "For each group with target size `g`, first count how many nodes `actual` are actually available (at most `g`) before deciding whether to reverse.",
            "If `actual % 2 == 0`, reverse exactly `actual` nodes starting from `prev.next` and update `prev` to the new tail of the group; otherwise simply advance `prev` by `actual` steps.",
        ],
        "explanations": [
            "Groups are [5] (len 1), [2, 6] (len 2, reversed -> [6, 2]), [3, 9, 1] (len 3), [7, 3, 8, 4] (len 4, reversed -> [4, 8, 3, 7]).",
            "Groups are [1] (len 1), [1, 0] (len 2, reversed -> [0, 1]), [6] (len 1, odd so unchanged).",
            "Groups are [1] (len 1), [1, 0] (len 2, reversed -> [0, 1]), [6, 5] (len 2, actual length is even so reversed -> [5, 6]).",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseEvenLengthGroups",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        prev = head
        group_len = 2
        while prev.next is not None:
            node = prev
            count = 0
            while count < group_len and node.next is not None:
                node = node.next
                count += 1
            if count % 2 == 0:
                group_head = prev.next
                nxt_group = node.next
                rprev = nxt_group
                curr = group_head
                for _ in range(count):
                    nxt = curr.next
                    curr.next = rprev
                    rprev = curr
                    curr = nxt
                prev.next = rprev
                prev = group_head
            else:
                prev = node
            group_len += 1
        return head""",
        "java": """        ListNode prev = head;
        int groupLen = 2;
        while (prev.next != null) {
            ListNode node = prev;
            int count = 0;
            while (count < groupLen && node.next != null) {
                node = node.next;
                count++;
            }
            if (count % 2 == 0) {
                ListNode groupHead = prev.next;
                ListNode nxtGroup = node.next;
                ListNode rprev = nxtGroup;
                ListNode curr = groupHead;
                for (int i = 0; i < count; i++) {
                    ListNode nxt = curr.next;
                    curr.next = rprev;
                    rprev = curr;
                    curr = nxt;
                }
                prev.next = rprev;
                prev = groupHead;
            } else {
                prev = node;
            }
            groupLen++;
        }
        return head;""",
        "visible": [
            {"head": [5, 2, 6, 3, 9, 1, 7, 3, 8, 4]},
            {"head": [1, 1, 0, 6]},
            {"head": [1, 1, 0, 6, 5]},
        ],
        "hidden": [
            {"head": [8]},
            {"head": [1, 2]},
            {"head": [1, 2, 3]},
            {"head": [1, 2, 3, 4, 5, 6]},
            {"head": [1, 2, 3, 4, 5, 6, 7]},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8]},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8, 9]},
            {"head": list(range(1, 26))},
            {"head": list(range(1, 2501))},
        ],
    },
    {
        "slug": "32-reverse-alternating-k-node-groups",
        "title": "Reverse Alternating K-Node Groups",
        "difficulty": "Hard",
        "subtopic": "Reversal",
        "companies": ["Google", "Amazon", "Meta", "Microsoft", "Uber"],
        "desc": (
            "Given the `head` of a singly linked list and a positive integer `k`, partition the list into consecutive "
            "groups of `k` nodes (the final group may have fewer than `k` nodes).\n\n"
            "Numbering the groups `1, 2, 3, ...`, **reverse every odd-numbered group** (groups `1, 3, 5, ...` — "
            "including a trailing partial group if it falls on an odd group number) and **leave every even-numbered "
            "group** (`2, 4, 6, ...`) in its original order. Return the head of the modified list in `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 5000].",
            "-10^4 <= Node.val <= 10^4",
            "1 <= k <= 5000",
        ],
        "hints": [
            "Toggle a boolean flag `shouldReverse` (starting `true`) after each group of up to `k` nodes.",
            "When `shouldReverse` is true, reverse up to `k` nodes in-place and connect the previous tail to the reversed group's new head; when false, simply advance `prev` up to `k` steps.",
        ],
        "explanations": [
            "Group 1 [1, 2, 3] reverses to [3, 2, 1], group 2 [4, 5, 6] stays [4, 5, 6], and partial odd group 3 [7, 8] reverses to [8, 7].",
            "With k = 2, group 1 [1, 2] -> [2, 1], group 2 [3, 4] stays, group 3 [5, 6] -> [6, 5], group 4 [7] stays.",
            "With k = 1, every group has length 1 so the list is unchanged.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "reverseAlternatingKGroup",
        "params": [("head", "ListNode"), ("k", "int")],
        "ret": "ListNode",
        "py": """        if head is None or k <= 1:
            return head
        dummy = ListNode(0, head)
        prev = dummy
        curr = head
        should_reverse = True
        while curr is not None:
            if should_reverse:
                group_tail = curr
                rprev = None
                count = 0
                while curr is not None and count < k:
                    nxt = curr.next
                    curr.next = rprev
                    rprev = curr
                    curr = nxt
                    count += 1
                prev.next = rprev
                group_tail.next = curr
                prev = group_tail
            else:
                count = 0
                while curr is not None and count < k:
                    prev = curr
                    curr = curr.next
                    count += 1
            should_reverse = not should_reverse
        return dummy.next""",
        "java": """        if (head == null || k <= 1) {
            return head;
        }
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy;
        ListNode curr = head;
        boolean shouldReverse = true;
        while (curr != null) {
            if (shouldReverse) {
                ListNode groupTail = curr;
                ListNode rprev = null;
                int count = 0;
                while (curr != null && count < k) {
                    ListNode nxt = curr.next;
                    curr.next = rprev;
                    rprev = curr;
                    curr = nxt;
                    count++;
                }
                prev.next = rprev;
                groupTail.next = curr;
                prev = groupTail;
            } else {
                int count = 0;
                while (curr != null && count < k) {
                    prev = curr;
                    curr = curr.next;
                    count++;
                }
            }
            shouldReverse = !shouldReverse;
        }
        return dummy.next;""",
        "visible": [
            {"head": [1, 2, 3, 4, 5, 6, 7, 8], "k": 3},
            {"head": [1, 2, 3, 4, 5, 6, 7], "k": 2},
            {"head": [1, 2, 3, 4, 5], "k": 1},
        ],
        "hidden": [
            {"head": [], "k": 3},
            {"head": [9], "k": 2},
            {"head": [1, 2, 3, 4], "k": 10},
            {"head": [1, 2, 3, 4, 5, 6], "k": 3},
            {"head": [1, 2, 3, 4, 5], "k": 3},
            {"head": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10], "k": 4},
            {"head": [-5, -4, -3, -2, -1, 0, 1, 2, 3], "k": 2},
            {"head": list(range(1, 30)), "k": 5},
            {"head": list(range(1, 2501)), "k": 13},
        ],
    },
    {
        "slug": "33-add-two-numbers-ii",
        "title": "Add Two Numbers II",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Bloomberg", "Amazon", "Microsoft", "Meta", "Oracle"],
        "desc": (
            "You are given two non-empty singly linked lists `l1` and `l2` representing two non-negative integers. "
            "The **most significant digit** comes first, and each node stores a single decimal digit (`0`–`9`).\n\n"
            "Add the two numbers and return the sum as a linked list in the same most-significant-digit-first order. "
            "Neither input list contains leading zeros except for the number `0` itself."
        ),
        "cons": [
            "The number of nodes in each linked list is in the range [1, 2000].",
            "0 <= Node.val <= 9",
            "Neither number has leading zeros, except the number 0 itself.",
        ],
        "hints": [
            "Reversing both input lists aligns their least significant digits at the heads so standard carry addition works in a single pass.",
            "Prepend each newly computed sum digit to the front of the output list so the result is naturally built in most-significant-digit-first order.",
        ],
        "explanations": [
            "7243 + 564 = 7807, represented as [7, 8, 0, 7].",
            "243 + 564 = 807, represented as [8, 0, 7].",
            "999 + 1 = 1000 propagates a carry into a new leading node [1, 0, 0, 0].",
        ],
        "time": "O(m + n)",
        "space": "O(1)",
        "kind": "function",
        "method": "addTwoNumbers",
        "params": [("l1", "ListNode"), ("l2", "ListNode")],
        "ret": "ListNode",
        "py_full": """class Solution:
    def _reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    def addTwoNumbers(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        r1 = self._reverse(l1)
        r2 = self._reverse(l2)
        carry = 0
        ans = None
        while r1 is not None or r2 is not None or carry:
            total = carry
            if r1 is not None:
                total += r1.val
                r1 = r1.next
            if r2 is not None:
                total += r2.val
                r2 = r2.next
            carry, digit = divmod(total, 10)
            ans = ListNode(digit, ans)
        return ans
""",
        "java_full": """class Solution {
    private ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    public ListNode addTwoNumbers(ListNode l1, ListNode l2) {
        ListNode r1 = reverse(l1);
        ListNode r2 = reverse(l2);
        int carry = 0;
        ListNode ans = null;
        while (r1 != null || r2 != null || carry != 0) {
            int total = carry;
            if (r1 != null) {
                total += r1.val;
                r1 = r1.next;
            }
            if (r2 != null) {
                total += r2.val;
                r2 = r2.next;
            }
            carry = total / 10;
            ans = new ListNode(total % 10, ans);
        }
        return ans;
    }
}
""",
        "visible": [
            {"l1": [7, 2, 4, 3], "l2": [5, 6, 4]},
            {"l1": [2, 4, 3], "l2": [5, 6, 4]},
            {"l1": [9, 9, 9], "l2": [1]},
        ],
        "hidden": [
            {"l1": [0], "l2": [0]},
            {"l1": [0], "l2": [7, 3]},
            {"l1": [5], "l2": [5]},
            {"l1": [1], "l2": [9, 9, 9, 9]},
            {"l1": [9, 9, 9, 9], "l2": [9, 9, 9, 9]},
            {"l1": [1, 0, 0, 0, 0], "l2": [1]},
            {"l1": [8, 9, 9], "l2": [2]},
            {"l1": [1, 2, 3, 4, 5, 6, 7, 8, 9], "l2": [9, 8, 7, 6, 5, 4, 3, 2, 1]},
            {"l1": [9] * 1000, "l2": [1] + [0] * 999},
        ],
    },
    {
        "slug": "34-remove-nodes-with-greater-right",
        "title": "Remove Nodes with Greater Right",
        "difficulty": "Medium",
        "subtopic": "Reversal",
        "companies": ["Amazon", "Google", "Meta", "Microsoft"],
        "desc": (
            "You are given the `head` of a non-empty singly linked list. Remove every node that has another node "
            "with a **strictly greater** value anywhere to its right in the list.\n\n"
            "Return the head of the modified linked list. Note that the remaining node values will form a "
            "non-increasing sequence. Solve this in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [1, 10^4].",
            "1 <= Node.val <= 10^5",
        ],
        "hints": [
            "Scanning right-to-left lets you maintain a single running maximum `maxSoFar` and discard any node with `val < maxSoFar`.",
            "To scan right-to-left in O(1) extra space, reverse the list, filter out nodes smaller than the running maximum, and reverse the filtered list back.",
        ],
        "explanations": [
            "Nodes 5, 2, and 3 all have 13 or 8 to their right and are removed, leaving [13, 8].",
            "All values are equal (1), so no node has a strictly greater value to its right: [1, 1, 1, 1].",
            "The list is strictly increasing, so only the rightmost node [5] survives.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "removeNodes",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py_full": """class Solution:
    def _reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    def removeNodes(self, head: Optional[ListNode]) -> Optional[ListNode]:
        rev = self._reverse(head)
        max_val = rev.val
        curr = rev
        while curr.next is not None:
            if curr.next.val < max_val:
                curr.next = curr.next.next
            else:
                curr = curr.next
                max_val = curr.val
        return self._reverse(rev)
""",
        "java_full": """class Solution {
    private ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    public ListNode removeNodes(ListNode head) {
        ListNode rev = reverse(head);
        int maxVal = rev.val;
        ListNode curr = rev;
        while (curr.next != null) {
            if (curr.next.val < maxVal) {
                curr.next = curr.next.next;
            } else {
                curr = curr.next;
                maxVal = curr.val;
            }
        }
        return reverse(rev);
    }
}
""",
        "visible": [
            {"head": [5, 2, 13, 3, 8]},
            {"head": [1, 1, 1, 1]},
            {"head": [1, 2, 3, 4, 5]},
        ],
        "hidden": [
            {"head": [42]},
            {"head": [5, 4, 3, 2, 1]},
            {"head": [10, 5, 10, 5, 10]},
            {"head": [2, 10, 1, 9, 3, 8, 4, 7]},
            {"head": [100, 1, 2, 3, 4, 5]},
            {"head": [1, 2, 3, 4, 5, 100]},
            {"head": [7, 3, 9, 9, 2, 8, 8, 1]},
            {"head": [50, 40, 45, 30, 35, 20, 25, 10]},
            {"head": make_rng_list(3401, 2500, 1, 100000)},
        ],
    },
    # -------------------------------------------------------------------------
    # 35-40: Merge & Sort
    # -------------------------------------------------------------------------
    {
        "slug": "35-insertion-sort-list",
        "title": "Insertion Sort List",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Microsoft", "Bloomberg", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list, sort the list using **insertion sort** (or return the nodes "
            "re-linked in non-decreasing order), and return the sorted list's head.\n\n"
            "Maintain a growing sorted prefix starting from a dummy node, detaching each subsequent node and "
            "inserting it into its proper sorted position in `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 2000].",
            "-5000 <= Node.val <= 5000",
        ],
        "hints": [
            "Keep a pointer `lastSorted` at the end of the already-sorted prefix: if `curr.val >= lastSorted.val`, you can skip scanning from the dummy head and advance `lastSorted` in O(1).",
            "Otherwise, walk `prev` from `dummy` until `prev.next.val >= curr.val`, detach `curr`, and splice it right after `prev`.",
        ],
        "explanations": [
            "Inserting 2 before 4, 1 before 2, and 3 between 2 and 4 yields [1, 2, 3, 4].",
            "Sorting [-1, 5, 3, 4, 0] produces [-1, 0, 3, 4, 5].",
            "An empty list remains empty (null).",
        ],
        "time": "O(n^2)",
        "space": "O(1)",
        "kind": "function",
        "method": "insertionSortList",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None or head.next is None:
            return head
        dummy = ListNode(0, head)
        last_sorted = head
        curr = head.next
        while curr is not None:
            if last_sorted.val <= curr.val:
                last_sorted = last_sorted.next
            else:
                prev = dummy
                while prev.next.val <= curr.val:
                    prev = prev.next
                last_sorted.next = curr.next
                curr.next = prev.next
                prev.next = curr
            curr = last_sorted.next
        return dummy.next""",
        "java": """        if (head == null || head.next == null) {
            return head;
        }
        ListNode dummy = new ListNode(0, head);
        ListNode lastSorted = head;
        ListNode curr = head.next;
        while (curr != null) {
            if (lastSorted.val <= curr.val) {
                lastSorted = lastSorted.next;
            } else {
                ListNode prev = dummy;
                while (prev.next.val <= curr.val) {
                    prev = prev.next;
                }
                lastSorted.next = curr.next;
                curr.next = prev.next;
                prev.next = curr;
            }
            curr = lastSorted.next;
        }
        return dummy.next;""",
        "visible": [
            {"head": [4, 2, 1, 3]},
            {"head": [-1, 5, 3, 4, 0]},
            {"head": []},
        ],
        "hidden": [
            {"head": [7]},
            {"head": [2, 1]},
            {"head": [1, 2, 3, 4, 5]},
            {"head": [5, 4, 3, 2, 1]},
            {"head": [3, 3, 1, 1, 2, 2]},
            {"head": [-5000, 5000, 0, -5000, 5000]},
            {"head": [10, -2, 7, -2, 10, 0, -9, 4]},
            {"head": list(range(100, 0, -1))},
            {"head": make_rng_list(3501, 600, -5000, 5000)},
        ],
    },
    {
        "slug": "36-partition-linked-list",
        "title": "Partition Linked List",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Apple"],
        "desc": (
            "Given the `head` of a singly linked list and an integer `x`, partition the list so that all nodes "
            "with values **strictly less than** `x` come before all nodes with values **greater than or equal to** `x`.\n\n"
            "You must preserve the original relative order of the nodes in each of the two partitions. "
            "Solve the problem in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 5000].",
            "-1000 <= Node.val <= 1000",
            "-1000 <= x <= 1000",
        ],
        "hints": [
            "Maintain two separate dummy-headed lists: `before` for nodes `< x` and `after` for nodes `>= x`.",
            "After distributing every node, terminate `afterTail.next = null` (to prevent cycles!) and link `beforeTail.next = afterDummy.next`.",
        ],
        "explanations": [
            "Nodes < 3 are [1, 2, 2] and nodes >= 3 are [4, 3, 5], yielding [1, 2, 2, 4, 3, 5].",
            "Nodes < 2 are [1] and nodes >= 2 are [2], yielding [1, 2].",
            "An empty list remains empty (null).",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "partition",
        "params": [("head", "ListNode"), ("x", "int")],
        "ret": "ListNode",
        "py": """        before_dummy = ListNode(0)
        after_dummy = ListNode(0)
        before = before_dummy
        after = after_dummy
        curr = head
        while curr is not None:
            if curr.val < x:
                before.next = curr
                before = before.next
            else:
                after.next = curr
                after = after.next
            curr = curr.next
        after.next = None
        before.next = after_dummy.next
        return before_dummy.next""",
        "java": """        ListNode beforeDummy = new ListNode(0);
        ListNode afterDummy = new ListNode(0);
        ListNode before = beforeDummy;
        ListNode after = afterDummy;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val < x) {
                before.next = curr;
                before = before.next;
            } else {
                after.next = curr;
                after = after.next;
            }
            curr = curr.next;
        }
        after.next = null;
        before.next = afterDummy.next;
        return beforeDummy.next;""",
        "visible": [
            {"head": [1, 4, 3, 2, 5, 2], "x": 3},
            {"head": [2, 1], "x": 2},
            {"head": [], "x": 0},
        ],
        "hidden": [
            {"head": [5], "x": 5},
            {"head": [5], "x": 10},
            {"head": [1, 2, 3, 4], "x": 10},
            {"head": [1, 2, 3, 4], "x": 0},
            {"head": [3, 3, 3, 1, 1, 2], "x": 3},
            {"head": [10, -5, 0, -10, 5, -1, 1], "x": 0},
            {"head": [4, 3, 2, 5, 2, 1, 0], "x": 3},
            {"head": [-1000, 1000, -1000, 1000, 0], "x": 0},
            {"head": make_rng_list(3601, 2000, -1000, 1000), "x": 0},
        ],
    },
    {
        "slug": "37-sort-linked-list-of-zeros-ones-twos",
        "title": "Sort Linked List of 0s, 1s, and 2s",
        "difficulty": "Easy",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Oracle"],
        "desc": (
            "Given the `head` of a singly linked list where every node's value is `0`, `1`, or `2`, sort the "
            "linked list in non-decreasing order by rewiring node pointers in a single pass, and return the new head.\n\n"
            "Solve the problem in `O(n)` time and `O(1)` extra space without modifying node values."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "Node.val is 0, 1, or 2.",
        ],
        "hints": [
            "Create three dummy-headed sublists for 0s, 1s, and 2s and append each visited node to the matching tail.",
            "Terminate the 2s tail with `null`, connect the 1s tail to `twoDummy.next`, and connect the 0s tail to `oneDummy.next` if non-empty (otherwise `twoDummy.next`).",
        ],
        "explanations": [
            "Grouping 0s, then 1s, then 2s produces [0, 0, 1, 1, 2, 2].",
            "Only 0s and 2s are present, so the 0-chain connects directly to the 2-chain: [0, 0, 2, 2].",
            "An empty list remains empty (null).",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "sortZeroOneTwo",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        z_head = ListNode(0)
        o_head = ListNode(0)
        t_head = ListNode(0)
        z, o, t = z_head, o_head, t_head
        curr = head
        while curr is not None:
            if curr.val == 0:
                z.next = curr
                z = z.next
            elif curr.val == 1:
                o.next = curr
                o = o.next
            else:
                t.next = curr
                t = t.next
            curr = curr.next
        t.next = None
        o.next = t_head.next
        z.next = o_head.next if o_head.next is not None else t_head.next
        return z_head.next""",
        "java": """        ListNode zHead = new ListNode(0);
        ListNode oHead = new ListNode(0);
        ListNode tHead = new ListNode(0);
        ListNode z = zHead, o = oHead, t = tHead;
        ListNode curr = head;
        while (curr != null) {
            if (curr.val == 0) {
                z.next = curr;
                z = z.next;
            } else if (curr.val == 1) {
                o.next = curr;
                o = o.next;
            } else {
                t.next = curr;
                t = t.next;
            }
            curr = curr.next;
        }
        t.next = null;
        o.next = tHead.next;
        z.next = (oHead.next != null) ? oHead.next : tHead.next;
        return zHead.next;""",
        "visible": [
            {"head": [2, 1, 0, 2, 1, 0]},
            {"head": [2, 0, 2, 0]},
            {"head": []},
        ],
        "hidden": [
            {"head": [0]},
            {"head": [1]},
            {"head": [2]},
            {"head": [1, 1, 1, 1]},
            {"head": [2, 2, 1, 1]},
            {"head": [1, 0, 1, 0, 1]},
            {"head": [0, 1, 2, 0, 1, 2, 0, 1, 2]},
            {"head": [2, 2, 2, 1, 0, 0]},
            {"head": make_rng_list(3701, 2500, 0, 2)},
        ],
    },
    {
        "slug": "38-sort-list-already-sorted-by-absolute-values",
        "title": "Sort List Already Sorted by Absolute Values",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Google", "Meta", "Bloomberg"],
        "desc": (
            "Given the `head` of a singly linked list whose nodes are already sorted in **non-decreasing order of "
            "their absolute values** (`|Node.val|`), return the list sorted in **non-decreasing order of their "
            "actual signed values**.\n\n"
            "Solve the problem in `O(n)` time and `O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-5000 <= Node.val <= 5000",
            "The input list is sorted in non-decreasing order of |Node.val|.",
        ],
        "hints": [
            "Non-negative nodes are already in non-decreasing relative order, whereas negative nodes appear in reverse (non-increasing) order.",
            "Traverse the list with `curr`: whenever `curr.next.val < 0`, unlink `curr.next` and prepend it to the front of the list so negative numbers end up in ascending order ahead of all non-negative values.",
        ],
        "explanations": [
            "Moving -5 and -10 to the front in order of encounter places -10 before -5, yielding [-10, -5, 0, 2, 5, 10].",
            "Moving -1 and -2 to the front produces [-2, -1, 0, 1].",
            "All values are already non-negative, so [0, 1, 3, 5] is unchanged.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "sortLinkedList",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py": """        if head is None:
            return None
        curr = head
        while curr.next is not None:
            if curr.next.val < 0:
                node = curr.next
                curr.next = node.next
                node.next = head
                head = node
            else:
                curr = curr.next
        return head""",
        "java": """        if (head == null) {
            return null;
        }
        ListNode curr = head;
        while (curr.next != null) {
            if (curr.next.val < 0) {
                ListNode node = curr.next;
                curr.next = node.next;
                node.next = head;
                head = node;
            } else {
                curr = curr.next;
            }
        }
        return head;""",
        "visible": [
            {"head": [0, 2, -5, 5, 10, -10]},
            {"head": [0, 1, -1, -2]},
            {"head": [0, 1, 3, 5]},
        ],
        "hidden": [
            {"head": []},
            {"head": [-7]},
            {"head": [-1, -2, -3, -4, -5]},
            {"head": [-2, 2, -2, 2, -5, 5]},
            {"head": [-1, 2, -3, 4, -5, 6]},
            {"head": [0, 0, 0, -1, 1, -100, 100]},
            {"head": [-5000, 5000]},
            {"head": [1, -2, -2, 3, -4, 4, -5]},
            {"head": sorted(make_rng_list(3801, 2500, -5000, 5000), key=abs)},
        ],
    },
    {
        "slug": "39-sort-alternating-ascending-descending-list",
        "title": "Sort Alternating Ascending and Descending List",
        "difficulty": "Medium",
        "subtopic": "Merge & Sort",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs", "Adobe"],
        "desc": (
            "You are given the `head` of a singly linked list with a special alternating structure:\n"
            "- Nodes at **odd 1-based positions** (`1st, 3rd, 5th, ...`) are sorted in **non-decreasing** order.\n"
            "- Nodes at **even 1-based positions** (`2nd, 4th, 6th, ...`) are sorted in **non-increasing** order.\n\n"
            "Sort the entire linked list in non-decreasing order and return its new head in `O(n)` time and "
            "`O(1)` extra space."
        ),
        "cons": [
            "The number of nodes in the list is in the range [0, 10^4].",
            "-10^5 <= Node.val <= 10^5",
            "Odd-positioned nodes are non-decreasing; even-positioned nodes are non-increasing.",
        ],
        "hints": [
            "Split the list into two chains by parity of position: `asc` (odd positions) and `desc` (even positions).",
            "Reverse the `desc` chain so both chains are sorted in non-decreasing order, then merge the two sorted lists in O(n) time.",
        ],
        "explanations": [
            "Odd chain is [10, 30, 50], even chain is [40, 20] which reverses to [20, 40]; merging gives [10, 20, 30, 40, 50].",
            "Odd chain [1, 3, 5] and reversed even chain [2, 4, 6] merge to [1, 2, 3, 4, 5, 6].",
            "A single-node list [7] is already sorted.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "kind": "function",
        "method": "sortAlternatingList",
        "params": [("head", "ListNode")],
        "ret": "ListNode",
        "py_full": """class Solution:
    def _reverse(self, head: Optional[ListNode]) -> Optional[ListNode]:
        prev = None
        curr = head
        while curr is not None:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        return prev

    def _merge(self, l1: Optional[ListNode], l2: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while l1 is not None and l2 is not None:
            if l1.val <= l2.val:
                tail.next = l1
                l1 = l1.next
            else:
                tail.next = l2
                l2 = l2.next
            tail = tail.next
        tail.next = l1 if l1 is not None else l2
        return dummy.next

    def sortAlternatingList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        if head is None or head.next is None:
            return head
        asc_head = head
        desc_head = head.next
        asc = asc_head
        desc = desc_head
        while desc is not None and desc.next is not None:
            asc.next = desc.next
            asc = asc.next
            desc.next = asc.next
            desc = desc.next
        asc.next = None
        desc_sorted = self._reverse(desc_head)
        return self._merge(asc_head, desc_sorted)
""",
        "java_full": """class Solution {
    private ListNode reverse(ListNode head) {
        ListNode prev = null;
        ListNode curr = head;
        while (curr != null) {
            ListNode nxt = curr.next;
            curr.next = prev;
            prev = curr;
            curr = nxt;
        }
        return prev;
    }

    private ListNode merge(ListNode l1, ListNode l2) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (l1 != null && l2 != null) {
            if (l1.val <= l2.val) {
                tail.next = l1;
                l1 = l1.next;
            } else {
                tail.next = l2;
                l2 = l2.next;
            }
            tail = tail.next;
        }
        tail.next = (l1 != null) ? l1 : l2;
        return dummy.next;
    }

    public ListNode sortAlternatingList(ListNode head) {
        if (head == null || head.next == null) {
            return head;
        }
        ListNode ascHead = head;
        ListNode descHead = head.next;
        ListNode asc = ascHead;
        ListNode desc = descHead;
        while (desc != null && desc.next != null) {
            asc.next = desc.next;
            asc = asc.next;
            desc.next = asc.next;
            desc = desc.next;
        }
        asc.next = null;
        ListNode descSorted = reverse(descHead);
        return merge(ascHead, descSorted);
    }
}
""",
        "visible": [
            {"head": [10, 40, 30, 20, 50]},
            {"head": [1, 6, 3, 4, 5, 2]},
            {"head": [7]},
        ],
        "hidden": [
            {"head": []},
            {"head": [5, 2]},
            {"head": [2, 5]},
            {"head": [1, 100, 2, 50, 3, 25, 4]},
            {"head": [-10, 10, -5, 5, 0, 0, 5, -5]},
            {"head": [3, 3, 3, 3, 3, 3]},
            {"head": [10, 9, 20, 8, 30, 7, 40, 6]},
            {"head": [-100, -1, -50, -2, -20, -3, -10, -4, 0]},
            {"head": [
                x
                for pair in zip(
                    make_sorted_list(3901, 1250, -50000, 50000),
                    list(reversed(make_sorted_list(3902, 1250, -50000, 50000))),
                )
                for x in pair
            ]},
        ],
    },
    {
        "slug": "40-common-elements-in-k-sorted-lists",
        "title": "Common Elements in K Sorted Lists",
        "difficulty": "Hard",
        "subtopic": "Merge & Sort",
        "companies": ["Google", "Amazon", "Meta", "LinkedIn", "Uber"],
        "desc": (
            "You are given an array `lists` of `k` singly linked lists, where each list is sorted in "
            "**non-decreasing** order (and may contain duplicate values).\n\n"
            "Return a singly linked list sorted in non-decreasing order representing the **multiset intersection** "
            "of all `k` lists: each value `v` must appear `min_i(count_i(v))` times in the result (where `count_i(v)` "
            "is the number of occurrences of `v` in `lists[i]`).\n\n"
            "If `lists` is empty, if any list in `lists` is empty, or if no value appears in all `k` lists, return "
            "`null` (`None` in Python). Aim for `O(N)` total time where `N` is the total number of nodes across all lists."
        ),
        "cons": [
            "0 <= lists.length <= 1000",
            "0 <= lists[i].length <= 2000",
            "-10^4 <= lists[i][j] <= 10^4",
            "Each lists[i] is sorted in non-decreasing order.",
            "The sum of all list lengths does not exceed 10^4.",
        ],
        "hints": [
            "Two-pointer intersection of two sorted linked lists runs in O(len(a) + len(b)) time and produces a list whose length is at most min(len(a), len(b)).",
            "Start with the shortest list as the running intersection `res` (length L_min <= L_i for all i); intersecting `res` with each remaining list takes O(L_min + L_i) <= O(2 * L_i), giving O(N) total time and O(1) extra space.",
        ],
        "explanations": [
            "Common elements across all three lists are a single 2 and a single 4: [2, 4].",
            "Value 2 appears twice in both lists and value 5 once, yielding [2, 2, 5].",
            "No value is shared by all three lists, so return null.",
        ],
        "time": "O(N)",
        "space": "O(1)",
        "kind": "function",
        "method": "commonElementsKLists",
        "params": [("lists", "ListNode[]")],
        "ret": "ListNode",
        "py_full": """class Solution:
    def _intersect_two(self, a: Optional[ListNode], b: Optional[ListNode]) -> Optional[ListNode]:
        dummy = ListNode(0)
        tail = dummy
        while a is not None and b is not None:
            if a.val == b.val:
                tail.next = a
                tail = tail.next
                a = a.next
                b = b.next
            elif a.val < b.val:
                a = a.next
            else:
                b = b.next
        tail.next = None
        return dummy.next

    def commonElementsKLists(self, lists: List[Optional[ListNode]]) -> Optional[ListNode]:
        if not lists:
            return None
        min_idx = 0
        min_len = 10**18
        for i, node in enumerate(lists):
            length = 0
            curr = node
            while curr is not None:
                length += 1
                curr = curr.next
            if length == 0:
                return None
            if length < min_len:
                min_len = length
                min_idx = i
        res = lists[min_idx]
        for i, node in enumerate(lists):
            if i == min_idx:
                continue
            res = self._intersect_two(res, node)
            if res is None:
                return None
        return res
""",
        "java_full": """class Solution {
    private ListNode intersectTwo(ListNode a, ListNode b) {
        ListNode dummy = new ListNode(0);
        ListNode tail = dummy;
        while (a != null && b != null) {
            if (a.val == b.val) {
                tail.next = a;
                tail = tail.next;
                a = a.next;
                b = b.next;
            } else if (a.val < b.val) {
                a = a.next;
            } else {
                b = b.next;
            }
        }
        tail.next = null;
        return dummy.next;
    }

    public ListNode commonElementsKLists(ListNode[] lists) {
        if (lists == null || lists.length == 0) {
            return null;
        }
        int minIdx = 0;
        int minLen = Integer.MAX_VALUE;
        for (int i = 0; i < lists.length; i++) {
            int len = 0;
            for (ListNode curr = lists[i]; curr != null; curr = curr.next) {
                len++;
            }
            if (len == 0) {
                return null;
            }
            if (len < minLen) {
                minLen = len;
                minIdx = i;
            }
        }
        ListNode res = lists[minIdx];
        for (int i = 0; i < lists.length; i++) {
            if (i == minIdx) {
                continue;
            }
            res = intersectTwo(res, lists[i]);
            if (res == null) {
                return null;
            }
        }
        return res;
    }
}
""",
        "visible": [
            {"lists": [[1, 2, 4, 5], [2, 3, 4, 6], [0, 2, 4, 8]]},
            {"lists": [[1, 2, 2, 2, 5], [2, 2, 3, 5, 5]]},
            {"lists": [[1, 2, 3], [2, 3, 4], [4, 5, 6]]},
        ],
        "hidden": [
            {"lists": []},
            {"lists": [[]]},
            {"lists": [[1, 2, 3], []]},
            {"lists": [[-5, 0, 5]]},
            {"lists": [[1, 1, 1], [1, 1, 1, 1], [1, 1]]},
            {"lists": [[-10, -5, 0, 5, 10], [-10, -5, 1, 5, 10], [-10, -5, 5, 10]]},
            {"lists": [[1, 3, 5, 7, 9], [1, 2, 3, 4, 5, 6, 7, 8, 9], [3, 7], [0, 3, 4, 7, 10]]},
            {"lists": [[i * 2 for i in range(50)], [i * 3 for i in range(35)], [i * 6 for i in range(20)]]},
            {"lists": [
                sorted(list(range(0, 400, 4)) + make_rng_list(4000 + k, 200, -50, 450))
                for k in range(8)
            ]},
        ],
    },
    # -------------------------------------------------------------------------
    # 41-46: LRU Design (Doubly Linked List + HashMap / Cursor Design)
    # -------------------------------------------------------------------------
    {
        "slug": "41-design-singly-linked-list",
        "title": "Design Singly Linked List",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "Design and implement your own linked list class `MyLinkedList` (using singly or doubly linked nodes) "
            "that supports 0-indexed operations:\n"
            "- `MyLinkedList()` initializes an empty linked list.\n"
            "- `int get(int index)` returns the value of the `index`-th node, or `-1` if `index` is out of bounds.\n"
            "- `void addAtHead(int val)` inserts a node with value `val` before the first element.\n"
            "- `void addAtTail(int val)` appends a node with value `val` as the last element.\n"
            "- `void addAtIndex(int index, int val)` inserts a node with value `val` before the `index`-th node. "
            "If `index == length`, appends at the tail. If `index < 0` or `index > length`, does nothing.\n"
            "- `void deleteAtIndex(int index)` deletes the `index`-th node if `0 <= index < length`; otherwise does nothing."
        ),
        "cons": [
            "0 <= val <= 10^5",
            "-1000 <= index <= 10^4",
            "At most 2000 calls will be made to get, addAtHead, addAtTail, addAtIndex, and deleteAtIndex.",
        ],
        "hints": [
            "Using a doubly linked list with sentinel `head` and `tail` dummy nodes plus a `size` counter eliminates edge cases at both ends.",
            "To reach any valid `index` in O(min(index, size - index)), walk forward from `head` if `index < size / 2` and backward from `tail` otherwise.",
        ],
        "explanations": [
            "After addAtHead(1), addAtTail(3), addAtIndex(1, 2) the list is [1, 2, 3]; get(1) is 2; deleteAtIndex(1) leaves [1, 3]; get(1) is 3.",
            "Out-of-bounds get/delete calls safely return -1 or do nothing; valid inserts at head/tail work as expected.",
            "Deleting the sole element empties the list so subsequent get(0) returns -1.",
        ],
        "time": "O(min(index, n - index))",
        "space": "O(n)",
        "kind": "design",
        "className": "MyLinkedList",
        "ctor_params": [],
        "methods": [
            {"name": "get", "params": [("index", "int")], "ret": "int"},
            {"name": "addAtHead", "params": [("val", "int")], "ret": "void"},
            {"name": "addAtTail", "params": [("val", "int")], "ret": "void"},
            {"name": "addAtIndex", "params": [("index", "int"), ("val", "int")], "ret": "void"},
            {"name": "deleteAtIndex", "params": [("index", "int")], "ret": "void"},
        ],
        "py_full": """class MyLinkedList:
    class _Node:
        __slots__ = ("val", "prev", "next")

        def __init__(self, val: int = 0):
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.size = 0

    def _node_at(self, index: int) -> "_Node":
        if index < self.size // 2:
            curr = self.head.next
            for _ in range(index):
                curr = curr.next
        else:
            curr = self.tail.prev
            for _ in range(self.size - 1 - index):
                curr = curr.prev
        return curr

    def _insert_before(self, target: "_Node", val: int) -> None:
        node = self._Node(val)
        prev = target.prev
        prev.next = node
        node.prev = prev
        node.next = target
        target.prev = node
        self.size += 1

    def get(self, index: int) -> int:
        if index < 0 or index >= self.size:
            return -1
        return self._node_at(index).val

    def addAtHead(self, val: int) -> None:
        self._insert_before(self.head.next, val)

    def addAtTail(self, val: int) -> None:
        self._insert_before(self.tail, val)

    def addAtIndex(self, index: int, val: int) -> None:
        if index < 0 or index > self.size:
            return
        if index == self.size:
            self._insert_before(self.tail, val)
        else:
            self._insert_before(self._node_at(index), val)

    def deleteAtIndex(self, index: int) -> None:
        if index < 0 or index >= self.size:
            return
        node = self._node_at(index)
        node.prev.next = node.next
        node.next.prev = node.prev
        self.size -= 1
""",
        "java_full": """class MyLinkedList {
    private static class Node {
        int val;
        Node prev;
        Node next;

        Node(int val) {
            this.val = val;
        }
    }

    private final Node head;
    private final Node tail;
    private int size;

    public MyLinkedList() {
        head = new Node(0);
        tail = new Node(0);
        head.next = tail;
        tail.prev = head;
        size = 0;
    }

    private Node nodeAt(int index) {
        Node curr;
        if (index < size / 2) {
            curr = head.next;
            for (int i = 0; i < index; i++) {
                curr = curr.next;
            }
        } else {
            curr = tail.prev;
            for (int i = size - 1; i > index; i--) {
                curr = curr.prev;
            }
        }
        return curr;
    }

    private void insertBefore(Node target, int val) {
        Node node = new Node(val);
        Node prev = target.prev;
        prev.next = node;
        node.prev = prev;
        node.next = target;
        target.prev = node;
        size++;
    }

    public int get(int index) {
        if (index < 0 || index >= size) {
            return -1;
        }
        return nodeAt(index).val;
    }

    public void addAtHead(int val) {
        insertBefore(head.next, val);
    }

    public void addAtTail(int val) {
        insertBefore(tail, val);
    }

    public void addAtIndex(int index, int val) {
        if (index < 0 || index > size) {
            return;
        }
        if (index == size) {
            insertBefore(tail, val);
        } else {
            insertBefore(nodeAt(index), val);
        }
    }

    public void deleteAtIndex(int index) {
        if (index < 0 || index >= size) {
            return;
        }
        Node node = nodeAt(index);
        node.prev.next = node.next;
        node.next.prev = node.prev;
        size--;
    }
}
""",
        "visible": [
            {
                "ops": ["MyLinkedList", "addAtHead", "addAtTail", "addAtIndex", "get", "deleteAtIndex", "get"],
                "args": [[], [1], [3], [1, 2], [1], [1], [1]],
            },
            {
                "ops": ["MyLinkedList", "get", "addAtIndex", "addAtTail", "addAtHead", "get", "get"],
                "args": [[], [0], [2, 9], [5], [1], [0], [1]],
            },
            {
                "ops": ["MyLinkedList", "addAtHead", "deleteAtIndex", "get"],
                "args": [[], [42], [0], [0]],
            },
        ],
        "hidden_fn": "gen_hidden_41",
    },
    {
        "slug": "42-design-browser-history",
        "title": "Design Browser History",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Amazon", "Google", "Meta", "Bloomberg", "Apple"],
        "desc": (
            "Design a browser tab history manager using a doubly linked list. Implement the `BrowserHistory` class:\n"
            "- `BrowserHistory(String homepage)` initializes the browser on `homepage`.\n"
            "- `void visit(String url)` visits `url` from the current page, clearing all forward history.\n"
            "- `String back(int steps)` moves `steps` backward in history (or as far back as possible if fewer "
            "than `steps` pages exist behind the current page) and returns the resulting current URL.\n"
            "- `String forward(int steps)` moves `steps` forward in history (or as far forward as possible) and "
            "returns the resulting current URL."
        ),
        "cons": [
            "1 <= homepage.length, url.length <= 30",
            "1 <= steps <= 500",
            "At most 2000 calls will be made to visit, back, and forward.",
        ],
        "hints": [
            "Store each visited page in a doubly linked list node with `prev` and `next` pointers and maintain a `curr` pointer.",
            "On `visit(url)`, create a new node linked directly after `curr` (with `newNode.next = null` automatically discarding old forward history) and advance `curr` to it.",
        ],
        "explanations": [
            "Visits build leetcode -> google -> facebook -> youtube; back(1) goes to facebook, back(1) to google, forward(1) to facebook, visit(linkedin) drops youtube, forward(2) stays at linkedin.",
            "Stepping back or forward past the ends clamps cleanly at the homepage or latest visited page.",
            "Visiting a new URL immediately after moving back truncates the old forward branch.",
        ],
        "time": "O(steps) for back/forward, O(1) for visit",
        "space": "O(n)",
        "kind": "design",
        "className": "BrowserHistory",
        "ctor_params": [("homepage", "String")],
        "methods": [
            {"name": "visit", "params": [("url", "String")], "ret": "void"},
            {"name": "back", "params": [("steps", "int")], "ret": "String"},
            {"name": "forward", "params": [("steps", "int")], "ret": "String"},
        ],
        "py_full": """class BrowserHistory:
    class _Node:
        __slots__ = ("url", "prev", "next")

        def __init__(self, url: str):
            self.url = url
            self.prev = None
            self.next = None

    def __init__(self, homepage: str):
        self.curr = self._Node(homepage)

    def visit(self, url: str) -> None:
        node = self._Node(url)
        node.prev = self.curr
        self.curr.next = node
        self.curr = node

    def back(self, steps: int) -> str:
        while steps > 0 and self.curr.prev is not None:
            self.curr = self.curr.prev
            steps -= 1
        return self.curr.url

    def forward(self, steps: int) -> str:
        while steps > 0 and self.curr.next is not None:
            self.curr = self.curr.next
            steps -= 1
        return self.curr.url
""",
        "java_full": """class BrowserHistory {
    private static class Node {
        final String url;
        Node prev;
        Node next;

        Node(String url) {
            this.url = url;
        }
    }

    private Node curr;

    public BrowserHistory(String homepage) {
        this.curr = new Node(homepage);
    }

    public void visit(String url) {
        Node node = new Node(url);
        node.prev = curr;
        curr.next = node;
        curr = node;
    }

    public String back(int steps) {
        while (steps > 0 && curr.prev != null) {
            curr = curr.prev;
            steps--;
        }
        return curr.url;
    }

    public String forward(int steps) {
        while (steps > 0 && curr.next != null) {
            curr = curr.next;
            steps--;
        }
        return curr.url;
    }
}
""",
        "visible": [
            {
                "ops": ["BrowserHistory", "visit", "visit", "visit", "back", "back", "forward", "visit", "forward", "back", "back"],
                "args": [["home.com"], ["google.com"], ["fb.com"], ["yt.com"], [1], [1], [1], ["li.com"], [2], [2], [7]],
            },
            {
                "ops": ["BrowserHistory", "back", "forward", "visit", "back", "forward"],
                "args": [["start.org"], [5], [5], ["docs.org"], [10], [10]],
            },
            {
                "ops": ["BrowserHistory", "visit", "visit", "back", "visit", "forward", "back"],
                "args": [["a.io"], ["b.io"], ["c.io"], [1], ["d.io"], [1], [1]],
            },
        ],
        "hidden_fn": "gen_hidden_42",
    },
    {
        "slug": "43-first-unique-number-stream",
        "title": "First Unique Number Stream",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Amazon", "Google", "Meta", "Microsoft", "Bloomberg"],
        "desc": (
            "You have a stream of integers, and you want to find the **first unique** integer (an integer that has "
            "appeared **exactly once** so far, choosing the earliest inserted one) at any time.\n\n"
            "Implement the `FirstUnique` class:\n"
            "- `FirstUnique(int[] nums)` initializes the object with the initial stream elements `nums` in order.\n"
            "- `int showFirstUnique()` returns the value of the **first unique** integer currently in the stream, "
            "or `-1` if no unique integer exists.\n"
            "- `void add(int value)` appends `value` to the stream.\n\n"
            "Both `showFirstUnique` and `add` must run in `O(1)` average time."
        ),
        "cons": [
            "0 <= nums.length <= 2000",
            "1 <= nums[i], value <= 10^8",
            "At most 2000 calls will be made to showFirstUnique and add.",
        ],
        "hints": [
            "Maintain a doubly linked list holding only the currently unique values in insertion order, with sentinel `head` and `tail` nodes.",
            "Keep a hash map from `value` to its list node (or a sentinel `null` once the value has appeared at least twice); on a second occurrence, unlink the node in O(1) so `head.next` is always the first unique value.",
        ],
        "explanations": [
            "Initial stream [2, 3, 5] has first unique 2; adding 5 duplicates 5 (first unique still 2); adding 2 duplicates 2 (first unique becomes 3); adding 3 duplicates 3 (no unique left -> -1).",
            "Initial stream [7, 7, 7, 7] has no unique values (-1); adding 7 keeps -1; adding 3 makes 3 the first unique.",
            "Starting empty returns -1; adding 10 then 20 makes 10 first unique; adding 10 again promotes 20.",
        ],
        "time": "O(1) per operation",
        "space": "O(n)",
        "kind": "design",
        "className": "FirstUnique",
        "ctor_params": [("nums", "int[]")],
        "methods": [
            {"name": "showFirstUnique", "params": [], "ret": "int"},
            {"name": "add", "params": [("value", "int")], "ret": "void"},
        ],
        "py_full": """class FirstUnique:
    class _Node:
        __slots__ = ("val", "prev", "next")

        def __init__(self, val: int = 0):
            self.val = val
            self.prev = None
            self.next = None

    def __init__(self, nums: List[int]):
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.nodes = {}
        for x in nums:
            self.add(x)

    def _append(self, node: "_Node") -> None:
        prev = self.tail.prev
        prev.next = node
        node.prev = prev
        node.next = self.tail
        self.tail.prev = node

    def _remove(self, node: "_Node") -> None:
        node.prev.next = node.next
        node.next.prev = node.prev

    def showFirstUnique(self) -> int:
        if self.head.next is self.tail:
            return -1
        return self.head.next.val

    def add(self, value: int) -> None:
        if value not in self.nodes:
            node = self._Node(value)
            self._append(node)
            self.nodes[value] = node
        else:
            existing = self.nodes[value]
            if existing is not None:
                self._remove(existing)
                self.nodes[value] = None
""",
        "java_full": """class FirstUnique {
    private static class Node {
        final int val;
        Node prev;
        Node next;

        Node(int val) {
            this.val = val;
        }
    }

    private final Node head;
    private final Node tail;
    private final Map<Integer, Node> nodes;

    public FirstUnique(int[] nums) {
        this.head = new Node(0);
        this.tail = new Node(0);
        this.head.next = this.tail;
        this.tail.prev = this.head;
        this.nodes = new HashMap<>();
        for (int x : nums) {
            add(x);
        }
    }

    private void append(Node node) {
        Node prev = tail.prev;
        prev.next = node;
        node.prev = prev;
        node.next = tail;
        tail.prev = node;
    }

    private void remove(Node node) {
        node.prev.next = node.next;
        node.next.prev = node.prev;
    }

    public int showFirstUnique() {
        if (head.next == tail) {
            return -1;
        }
        return head.next.val;
    }

    public void add(int value) {
        if (!nodes.containsKey(value)) {
            Node node = new Node(value);
            append(node);
            nodes.put(value, node);
        } else {
            Node existing = nodes.get(value);
            if (existing != null) {
                remove(existing);
                nodes.put(value, null);
            }
        }
    }
}
""",
        "visible": [
            {
                "ops": ["FirstUnique", "showFirstUnique", "add", "showFirstUnique", "add", "showFirstUnique", "add", "showFirstUnique"],
                "args": [[[2, 3, 5]], [], [5], [], [2], [], [3], []],
            },
            {
                "ops": ["FirstUnique", "showFirstUnique", "add", "add", "showFirstUnique"],
                "args": [[[7, 7, 7, 7]], [], [7], [3], []],
            },
            {
                "ops": ["FirstUnique", "showFirstUnique", "add", "add", "showFirstUnique", "add", "showFirstUnique"],
                "args": [[[]], [], [10], [20], [], [10], []],
            },
        ],
        "hidden_fn": "gen_hidden_43",
    },
    {
        "slug": "44-design-front-middle-back-queue",
        "title": "Design Front Middle Back Queue",
        "difficulty": "Medium",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Uber"],
        "desc": (
            "Design a queue supporting `O(1)` insertions and removals at the **front**, **middle**, and **back**.\n\n"
            "Implement the `FrontMiddleBackQueue` class:\n"
            "- `FrontMiddleBackQueue()` initializes an empty queue.\n"
            "- `void pushFront(int val)` adds `val` to the front of the queue.\n"
            "- `void pushMiddle(int val)` inserts `val` at 0-based index `floor(n / 2)` where `n` is the current size.\n"
            "- `void pushBack(int val)` adds `val` to the back of the queue.\n"
            "- `int popFront()` removes and returns the front element, or `-1` if empty.\n"
            "- `int popMiddle()` removes and returns the element at 0-based index `floor((n - 1) / 2)` (the frontmost "
            "of the two middle elements when `n` is even), or `-1` if empty.\n"
            "- `int popBack()` removes and returns the back element, or `-1` if empty."
        ),
        "cons": [
            "1 <= val <= 10^9",
            "At most 2000 calls will be made across all operations.",
        ],
        "hints": [
            "Split the elements across two doubly linked lists (deques) `left` and `right`, maintaining the invariant `left.size == right.size` or `left.size == right.size + 1`.",
            "Under this invariant, `popMiddle` always pops the back of `left`, and `pushMiddle` moves the back of `left` to the front of `right` if `left.size > right.size` before appending to `left`.",
        ],
        "explanations": [
            "Pushes form [1, 4, 3, 2]; pops remove front 1, middle 3, middle 4, back 2, then empty -1.",
            "Popping from an empty queue always returns -1; pushing to middle on empty inserts at index 0.",
            "Alternating pushFront, pushMiddle, and pushBack maintains exact middle indices for both even and odd sizes.",
        ],
        "time": "O(1) per operation",
        "space": "O(n)",
        "kind": "design",
        "className": "FrontMiddleBackQueue",
        "ctor_params": [],
        "methods": [
            {"name": "pushFront", "params": [("val", "int")], "ret": "void"},
            {"name": "pushMiddle", "params": [("val", "int")], "ret": "void"},
            {"name": "pushBack", "params": [("val", "int")], "ret": "void"},
            {"name": "popFront", "params": [], "ret": "int"},
            {"name": "popMiddle", "params": [], "ret": "int"},
            {"name": "popBack", "params": [], "ret": "int"},
        ],
        "py_full": """class FrontMiddleBackQueue:
    def __init__(self):
        self.left = deque()
        self.right = deque()

    def _rebalance(self) -> None:
        if len(self.left) > len(self.right) + 1:
            self.right.appendleft(self.left.pop())
        elif len(self.left) < len(self.right):
            self.left.append(self.right.popleft())

    def pushFront(self, val: int) -> None:
        self.left.appendleft(val)
        self._rebalance()

    def pushMiddle(self, val: int) -> None:
        if len(self.left) > len(self.right):
            self.right.appendleft(self.left.pop())
        self.left.append(val)

    def pushBack(self, val: int) -> None:
        self.right.append(val)
        self._rebalance()

    def popFront(self) -> int:
        if not self.left:
            return -1
        val = self.left.popleft()
        self._rebalance()
        return val

    def popMiddle(self) -> int:
        if not self.left:
            return -1
        val = self.left.pop()
        self._rebalance()
        return val

    def popBack(self) -> int:
        if not self.left:
            return -1
        if not self.right:
            return self.left.pop()
        val = self.right.pop()
        self._rebalance()
        return val
""",
        "java_full": """class FrontMiddleBackQueue {
    private final Deque<Integer> left;
    private final Deque<Integer> right;

    public FrontMiddleBackQueue() {
        this.left = new ArrayDeque<>();
        this.right = new ArrayDeque<>();
    }

    private void rebalance() {
        if (left.size() > right.size() + 1) {
            right.addFirst(left.removeLast());
        } else if (left.size() < right.size()) {
            left.addLast(right.removeFirst());
        }
    }

    public void pushFront(int val) {
        left.addFirst(val);
        rebalance();
    }

    public void pushMiddle(int val) {
        if (left.size() > right.size()) {
            right.addFirst(left.removeLast());
        }
        left.addLast(val);
    }

    public void pushBack(int val) {
        right.addLast(val);
        rebalance();
    }

    public int popFront() {
        if (left.isEmpty()) {
            return -1;
        }
        int val = left.removeFirst();
        rebalance();
        return val;
    }

    public int popMiddle() {
        if (left.isEmpty()) {
            return -1;
        }
        int val = left.removeLast();
        rebalance();
        return val;
    }

    public int popBack() {
        if (left.isEmpty()) {
            return -1;
        }
        if (right.isEmpty()) {
            return left.removeLast();
        }
        int val = right.removeLast();
        rebalance();
        return val;
    }
}
""",
        "visible": [
            {
                "ops": ["FrontMiddleBackQueue", "pushFront", "pushBack", "pushMiddle", "pushMiddle", "popFront", "popMiddle", "popMiddle", "popBack", "popFront"],
                "args": [[], [1], [2], [3], [4], [], [], [], [], []],
            },
            {
                "ops": ["FrontMiddleBackQueue", "popFront", "popMiddle", "popBack", "pushMiddle", "popBack"],
                "args": [[], [], [], [], [99], []],
            },
            {
                "ops": ["FrontMiddleBackQueue", "pushBack", "pushFront", "pushMiddle", "popMiddle", "popFront", "popBack"],
                "args": [[], [10], [20], [30], [], [], []],
            },
        ],
        "hidden_fn": "gen_hidden_44",
    },
    {
        "slug": "45-all-oone-frequency-tracker",
        "title": "All O(1) Frequency Tracker",
        "difficulty": "Hard",
        "subtopic": "LRU Design",
        "companies": ["LinkedIn", "Google", "Amazon", "Meta", "Uber"],
        "desc": (
            "Design a data structure that tracks positive integer counts for string keys and answers minimum, "
            "maximum, and point count queries all in **`O(1)` average time**.\n\n"
            "Implement the `AllOneTracker` class:\n"
            "- `AllOneTracker()` initializes an empty tracker.\n"
            "- `void inc(String key)` increments the count of `key` by `1` (inserting `key` with count `1` if absent).\n"
            "- `void dec(String key)` decrements the count of `key` by `1` if present; if its count drops to `0`, "
            "removes `key` completely. If `key` is not present, does nothing.\n"
            "- `int getMaxCount()` returns the maximum count among all currently stored keys, or `0` if empty.\n"
            "- `int getMinCount()` returns the minimum count among all currently stored keys, or `0` if empty.\n"
            "- `int getCount(String key)` returns the current count of `key`, or `0` if absent."
        ),
        "cons": [
            "1 <= key.length <= 16",
            "key consists of lowercase English letters.",
            "At most 2000 calls will be made across all methods.",
        ],
        "hints": [
            "Maintain a doubly linked list of non-empty frequency buckets sorted in strictly increasing order of `count`, where each bucket stores the set of keys currently at that count.",
            "Map each active `key` directly to its bucket node so `inc`/`dec` move a key to an adjacent bucket (creating it if needed) and unlink empty buckets in O(1); `head.next.count` and `tail.prev.count` immediately give min and max counts.",
        ],
        "explanations": [
            "Incrementing 'a' twice gives min=max=2; adding 'b' once sets min=1, max=2; decrementing 'b' removes it so min returns to 2.",
            "On an empty tracker (or after decrementing a non-existent key), min, max, and key counts all return 0.",
            "Incrementing three keys to counts 1, 2, 3 then removing the count-3 key lowers maxCount to 2 in O(1).",
        ],
        "time": "O(1) per operation",
        "space": "O(n)",
        "kind": "design",
        "className": "AllOneTracker",
        "ctor_params": [],
        "methods": [
            {"name": "inc", "params": [("key", "String")], "ret": "void"},
            {"name": "dec", "params": [("key", "String")], "ret": "void"},
            {"name": "getMaxCount", "params": [], "ret": "int"},
            {"name": "getMinCount", "params": [], "ret": "int"},
            {"name": "getCount", "params": [("key", "String")], "ret": "int"},
        ],
        "py_full": """class AllOneTracker:
    class _Bucket:
        __slots__ = ("count", "keys", "prev", "next")

        def __init__(self, count: int = 0):
            self.count = count
            self.keys = set()
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = self._Bucket(0)
        self.tail = self._Bucket(0)
        self.head.next = self.tail
        self.tail.prev = self.head
        self.key_map = {}

    def _insert_after(self, prev: "_Bucket", count: int) -> "_Bucket":
        node = self._Bucket(count)
        nxt = prev.next
        prev.next = node
        node.prev = prev
        node.next = nxt
        nxt.prev = node
        return node

    def _remove_if_empty(self, node: "_Bucket") -> None:
        if not node.keys:
            node.prev.next = node.next
            node.next.prev = node.prev

    def inc(self, key: str) -> None:
        if key not in self.key_map:
            if self.head.next is self.tail or self.head.next.count != 1:
                target = self._insert_after(self.head, 1)
            else:
                target = self.head.next
            target.keys.add(key)
            self.key_map[key] = target
            return
        cur = self.key_map[key]
        nxt_cnt = cur.count + 1
        if cur.next is self.tail or cur.next.count != nxt_cnt:
            target = self._insert_after(cur, nxt_cnt)
        else:
            target = cur.next
        target.keys.add(key)
        self.key_map[key] = target
        cur.keys.remove(key)
        self._remove_if_empty(cur)

    def dec(self, key: str) -> None:
        if key not in self.key_map:
            return
        cur = self.key_map[key]
        if cur.count == 1:
            del self.key_map[key]
        else:
            prv_cnt = cur.count - 1
            if cur.prev is self.head or cur.prev.count != prv_cnt:
                target = self._insert_after(cur.prev, prv_cnt)
            else:
                target = cur.prev
            target.keys.add(key)
            self.key_map[key] = target
        cur.keys.remove(key)
        self._remove_if_empty(cur)

    def getMaxCount(self) -> int:
        if self.head.next is self.tail:
            return 0
        return self.tail.prev.count

    def getMinCount(self) -> int:
        if self.head.next is self.tail:
            return 0
        return self.head.next.count

    def getCount(self, key: str) -> int:
        b = self.key_map.get(key)
        return 0 if b is None else b.count
""",
        "java_full": """class AllOneTracker {
    private static class Bucket {
        final int count;
        final Set<String> keys = new HashSet<>();
        Bucket prev;
        Bucket next;

        Bucket(int count) {
            this.count = count;
        }
    }

    private final Bucket head;
    private final Bucket tail;
    private final Map<String, Bucket> keyMap;

    public AllOneTracker() {
        head = new Bucket(0);
        tail = new Bucket(0);
        head.next = tail;
        tail.prev = head;
        keyMap = new HashMap<>();
    }

    private Bucket insertAfter(Bucket prev, int count) {
        Bucket node = new Bucket(count);
        Bucket nxt = prev.next;
        prev.next = node;
        node.prev = prev;
        node.next = nxt;
        nxt.prev = node;
        return node;
    }

    private void removeIfEmpty(Bucket node) {
        if (node.keys.isEmpty()) {
            node.prev.next = node.next;
            node.next.prev = node.prev;
        }
    }

    public void inc(String key) {
        Bucket cur = keyMap.get(key);
        if (cur == null) {
            Bucket target = (head.next == tail || head.next.count != 1)
                ? insertAfter(head, 1)
                : head.next;
            target.keys.add(key);
            keyMap.put(key, target);
            return;
        }
        int nxtCnt = cur.count + 1;
        Bucket target = (cur.next == tail || cur.next.count != nxtCnt)
            ? insertAfter(cur, nxtCnt)
            : cur.next;
        target.keys.add(key);
        keyMap.put(key, target);
        cur.keys.remove(key);
        removeIfEmpty(cur);
    }

    public void dec(String key) {
        Bucket cur = keyMap.get(key);
        if (cur == null) {
            return;
        }
        if (cur.count == 1) {
            keyMap.remove(key);
        } else {
            int prvCnt = cur.count - 1;
            Bucket target = (cur.prev == head || cur.prev.count != prvCnt)
                ? insertAfter(cur.prev, prvCnt)
                : cur.prev;
            target.keys.add(key);
            keyMap.put(key, target);
        }
        cur.keys.remove(key);
        removeIfEmpty(cur);
    }

    public int getMaxCount() {
        return head.next == tail ? 0 : tail.prev.count;
    }

    public int getMinCount() {
        return head.next == tail ? 0 : head.next.count;
    }

    public int getCount(String key) {
        Bucket b = keyMap.get(key);
        return b == null ? 0 : b.count;
    }
}
""",
        "visible": [
            {
                "ops": ["AllOneTracker", "inc", "inc", "getMaxCount", "getMinCount", "inc", "getMinCount", "dec", "getMinCount"],
                "args": [[], ["a"], ["a"], [], [], ["b"], [], ["b"], []],
            },
            {
                "ops": ["AllOneTracker", "getMaxCount", "getMinCount", "dec", "getCount"],
                "args": [[], [], [], ["missing"], ["missing"]],
            },
            {
                "ops": ["AllOneTracker", "inc", "inc", "inc", "inc", "inc", "inc", "getMaxCount", "dec", "getMaxCount", "getCount"],
                "args": [[], ["x"], ["y"], ["y"], ["z"], ["z"], ["z"], [], ["z"], [], ["z"]],
            },
        ],
        "hidden_fn": "gen_hidden_45",
    },
    {
        "slug": "46-design-text-editor",
        "title": "Design a Text Editor",
        "difficulty": "Hard",
        "subtopic": "LRU Design",
        "companies": ["Google", "Amazon", "Meta", "Atlassian", "Bloomberg"],
        "desc": (
            "Design a text editor with a movable cursor backed by a doubly linked list. Implement the `TextEditor` class:\n"
            "- `TextEditor()` initializes an empty document with the cursor at the beginning.\n"
            "- `void addText(String text)` inserts `text` immediately before the cursor; the cursor remains right after "
            "the newly inserted characters.\n"
            "- `int deleteText(int k)` deletes up to `k` characters immediately to the left of the cursor and returns "
            "the actual number of characters deleted.\n"
            "- `String cursorLeft(int k)` moves the cursor left by up to `k` positions and returns the last "
            "`min(10, len)` characters to the left of the cursor (where `len` is the number of characters left of the cursor).\n"
            "- `String cursorRight(int k)` moves the cursor right by up to `k` positions and returns the last "
            "`min(10, len)` characters to the left of the cursor."
        ),
        "cons": [
            "1 <= text.length, k <= 40",
            "text consists of lowercase English letters.",
            "At most 2000 calls will be made to addText, deleteText, cursorLeft, and cursorRight.",
        ],
        "hints": [
            "Represent the document as a doubly linked list of character nodes with sentinel `head` and `tail` nodes, keeping a `cursor` pointer on the character immediately left of the cursor (or `head` when at position 0).",
            "Inserting a character splices a node right after `cursor` in O(1); deleting unlinks `cursor` and moves it to `cursor.prev` in O(1); reading the left preview walks back at most 10 links.",
        ],
        "explanations": [
            "Typing 'leetcode', deleting 4 leaves 'leet', typing 'practice' gives 'leetpractice', moving left 8 lands after 'leet', deleting 10 removes all 4 chars, moving right 6 lands after 'practi'.",
            "Deleting or moving left on an empty editor returns 0 and empty string without error.",
            "Inserting text in the middle of a word after moving the cursor left splices cleanly between adjacent nodes.",
        ],
        "time": "O(text.length) / O(k) per operation",
        "space": "O(total characters)",
        "kind": "design",
        "className": "TextEditor",
        "ctor_params": [],
        "methods": [
            {"name": "addText", "params": [("text", "String")], "ret": "void"},
            {"name": "deleteText", "params": [("k", "int")], "ret": "int"},
            {"name": "cursorLeft", "params": [("k", "int")], "ret": "String"},
            {"name": "cursorRight", "params": [("k", "int")], "ret": "String"},
        ],
        "py_full": """class TextEditor:
    class _Node:
        __slots__ = ("ch", "prev", "next")

        def __init__(self, ch: str = ""):
            self.ch = ch
            self.prev = None
            self.next = None

    def __init__(self):
        self.head = self._Node()
        self.tail = self._Node()
        self.head.next = self.tail
        self.tail.prev = self.head
        self.cursor = self.head

    def _left_preview(self) -> str:
        chars = []
        p = self.cursor
        for _ in range(10):
            if p is self.head:
                break
            chars.append(p.ch)
            p = p.prev
        chars.reverse()
        return "".join(chars)

    def addText(self, text: str) -> None:
        for ch in text:
            node = self._Node(ch)
            nxt = self.cursor.next
            self.cursor.next = node
            node.prev = self.cursor
            node.next = nxt
            nxt.prev = node
            self.cursor = node

    def deleteText(self, k: int) -> int:
        deleted = 0
        while deleted < k and self.cursor is not self.head:
            prev = self.cursor.prev
            nxt = self.cursor.next
            prev.next = nxt
            nxt.prev = prev
            self.cursor = prev
            deleted += 1
        return deleted

    def cursorLeft(self, k: int) -> str:
        while k > 0 and self.cursor is not self.head:
            self.cursor = self.cursor.prev
            k -= 1
        return self._left_preview()

    def cursorRight(self, k: int) -> str:
        while k > 0 and self.cursor.next is not self.tail:
            self.cursor = self.cursor.next
            k -= 1
        return self._left_preview()
""",
        "java_full": """class TextEditor {
    private static class Node {
        final char ch;
        Node prev;
        Node next;

        Node(char ch) {
            this.ch = ch;
        }
    }

    private final Node head;
    private final Node tail;
    private Node cursor;

    public TextEditor() {
        head = new Node(' ');
        tail = new Node(' ');
        head.next = tail;
        tail.prev = head;
        cursor = head;
    }

    private String leftPreview() {
        StringBuilder sb = new StringBuilder(10);
        Node p = cursor;
        for (int i = 0; i < 10 && p != head; i++) {
            sb.append(p.ch);
            p = p.prev;
        }
        return sb.reverse().toString();
    }

    public void addText(String text) {
        for (int i = 0; i < text.length(); i++) {
            Node node = new Node(text.charAt(i));
            Node nxt = cursor.next;
            cursor.next = node;
            node.prev = cursor;
            node.next = nxt;
            nxt.prev = node;
            cursor = node;
        }
    }

    public int deleteText(int k) {
        int deleted = 0;
        while (deleted < k && cursor != head) {
            Node prev = cursor.prev;
            Node nxt = cursor.next;
            prev.next = nxt;
            nxt.prev = prev;
            cursor = prev;
            deleted++;
        }
        return deleted;
    }

    public String cursorLeft(int k) {
        while (k > 0 && cursor != head) {
            cursor = cursor.prev;
            k--;
        }
        return leftPreview();
    }

    public String cursorRight(int k) {
        while (k > 0 && cursor.next != tail) {
            cursor = cursor.next;
            k--;
        }
        return leftPreview();
    }
}
""",
        "visible": [
            {
                "ops": ["TextEditor", "addText", "deleteText", "addText", "cursorRight", "cursorLeft", "deleteText", "cursorLeft", "cursorRight"],
                "args": [[], ["leetcode"], [4], ["practice"], [3], [8], [10], [2], [6]],
            },
            {
                "ops": ["TextEditor", "deleteText", "cursorLeft", "cursorRight", "addText", "cursorLeft"],
                "args": [[], [5], [3], [3], ["hi"], [1]],
            },
            {
                "ops": ["TextEditor", "addText", "cursorLeft", "addText", "cursorRight"],
                "args": [[], ["ac"], [1], ["b"], [5]],
            },
        ],
        "hidden_fn": "gen_hidden_46",
    },
]


# -----------------------------------------------------------------------------
# Deterministic hidden test generators for design problems 41-46
# -----------------------------------------------------------------------------

def gen_hidden_41() -> list[dict]:
    tests = [
        {"ops": ["MyLinkedList", "get", "deleteAtIndex", "get"], "args": [[], [-1], [0], [5]]},
        {"ops": ["MyLinkedList", "addAtIndex", "get", "addAtIndex", "get"], "args": [[], [0, 10], [0], [1, 20], [1]]},
        {"ops": ["MyLinkedList", "addAtHead", "addAtHead", "addAtHead", "get", "get", "get"], "args": [[], [3], [2], [1], [0], [1], [2]]},
        {"ops": ["MyLinkedList", "addAtTail", "addAtTail", "deleteAtIndex", "get", "get"], "args": [[], [7], [8], [0], [0], [1]]},
        {"ops": ["MyLinkedList", "addAtTail", "addAtTail", "deleteAtIndex", "get", "get"], "args": [[], [7], [8], [1], [0], [1]]},
        {"ops": ["MyLinkedList", "addAtIndex", "addAtIndex", "addAtHead", "addAtIndex", "get"], "args": [[], [-5, 1], [10, 2], [9], [1, 8], [1]]},
        {
            "ops": ["MyLinkedList", "addAtHead", "addAtTail", "addAtHead", "addAtTail", "deleteAtIndex", "deleteAtIndex", "get", "get", "get"],
            "args": [[], [2], [3], [1], [4], [0], [2], [0], [1], [2]],
        },
        {
            "ops": ["MyLinkedList", "addAtHead", "addAtIndex", "addAtIndex", "addAtIndex", "get", "get", "get", "get"],
            "args": [[], [10], [1, 30], [1, 20], [3, 40], [0], [1], [2], [3]],
        },
    ]
    rng = random.Random(4101)
    ops = ["MyLinkedList"]
    args = [[]]
    size = 0
    for _ in range(450):
        choice = rng.randint(0, 4)
        if choice == 0:
            ops.append("addAtHead")
            args.append([rng.randint(0, 10000)])
            size += 1
        elif choice == 1:
            ops.append("addAtTail")
            args.append([rng.randint(0, 10000)])
            size += 1
        elif choice == 2:
            idx = rng.randint(-1, size + 2)
            ops.append("addAtIndex")
            args.append([idx, rng.randint(0, 10000)])
            if 0 <= idx <= size:
                size += 1
        elif choice == 3:
            idx = rng.randint(-1, size + 1)
            ops.append("deleteAtIndex")
            args.append([idx])
            if 0 <= idx < size:
                size -= 1
        else:
            idx = rng.randint(-1, size + 1)
            ops.append("get")
            args.append([idx])
    tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_42() -> list[dict]:
    tests = [
        {"ops": ["BrowserHistory", "back", "forward"], "args": [["root.com"], [1], [1]]},
        {"ops": ["BrowserHistory", "visit", "back", "forward", "back"], "args": [["h.com"], ["p1.com"], [1], [1], [1]]},
        {"ops": ["BrowserHistory", "visit", "visit", "visit", "back", "visit", "forward", "back"], "args": [["a"], ["b"], ["c"], ["d"], [2], ["e"], [5], [1]]},
        {"ops": ["BrowserHistory", "visit", "visit", "back", "back", "forward", "forward"], "args": [["u0"], ["u1"], ["u2"], [1], [1], [1], [1]]},
        {"ops": ["BrowserHistory", "visit", "back", "visit", "back", "visit", "forward"], "args": [["x"], ["y"], [1], ["z"], [1], ["w"], [2]]},
        {"ops": ["BrowserHistory", "visit", "visit", "visit", "visit", "back", "forward"], "args": [["p0"], ["p1"], ["p2"], ["p3"], ["p4"], [100], [100]]},
        {"ops": ["BrowserHistory", "visit", "visit", "back", "visit", "visit", "back", "back", "forward"], "args": [["s0"], ["s1"], ["s2"], [2], ["t1"], ["t2"], [1], [1], [2]]},
        {"ops": ["BrowserHistory", "visit", "visit", "visit", "back", "back", "visit", "back"], "args": [["same"], ["same"], ["other"], ["same"], [2], [1], ["end"], [1]]},
    ]
    rng = random.Random(4201)
    ops = ["BrowserHistory"]
    args = [["home.dev"]]
    for i in range(450):
        r = rng.random()
        if r < 0.45:
            ops.append("visit")
            args.append([f"p{i % 60}.dev"])
        elif r < 0.75:
            ops.append("back")
            args.append([rng.randint(1, 12)])
        else:
            ops.append("forward")
            args.append([rng.randint(1, 12)])
    tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_43() -> list[dict]:
    tests = [
        {"ops": ["FirstUnique", "showFirstUnique"], "args": [[[1]], []]},
        {"ops": ["FirstUnique", "showFirstUnique", "add", "showFirstUnique"], "args": [[[1, 1]], [], [2], []]},
        {"ops": ["FirstUnique", "add", "add", "add", "showFirstUnique"], "args": [[[]], [5], [5], [5], []]},
        {"ops": ["FirstUnique", "showFirstUnique", "add", "showFirstUnique", "add", "showFirstUnique"], "args": [[[1, 2, 3, 2, 1]], [], [3], [], [4], []]},
        {"ops": ["FirstUnique", "showFirstUnique", "add", "add", "showFirstUnique"], "args": [[[100000000, 99999999]], [], [100000000], [99999999], []]},
        {"ops": ["FirstUnique", "add", "showFirstUnique", "add", "showFirstUnique", "add", "showFirstUnique"], "args": [[[4, 5, 6]], [4], [], [6], [], [5], []]},
        {"ops": ["FirstUnique", "showFirstUnique", "add", "showFirstUnique"], "args": [[[8, 9, 8, 10, 9, 11]], [], [10], []]},
        {"ops": ["FirstUnique", "add", "add", "showFirstUnique", "add", "showFirstUnique"], "args": [[[1, 2, 3, 4, 5]], [1], [2], [], [3], []]},
    ]
    rng = random.Random(4301)
    init = [rng.randint(1, 80) for _ in range(100)]
    ops = ["FirstUnique", "showFirstUnique"]
    args = [[init], []]
    for _ in range(450):
        if rng.random() < 0.65:
            ops.append("add")
            args.append([rng.randint(1, 140)])
        else:
            ops.append("showFirstUnique")
            args.append([])
    tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_44() -> list[dict]:
    tests = [
        {"ops": ["FrontMiddleBackQueue", "pushFront", "popFront", "popFront"], "args": [[], [5], [], []]},
        {"ops": ["FrontMiddleBackQueue", "pushBack", "popBack", "popBack"], "args": [[], [7], [], []]},
        {"ops": ["FrontMiddleBackQueue", "pushFront", "popBack", "pushBack", "popFront"], "args": [[], [1], [], [2], []]},
        {"ops": ["FrontMiddleBackQueue", "pushMiddle", "pushMiddle", "pushMiddle", "popMiddle", "popMiddle", "popMiddle"], "args": [[], [1], [2], [3], [], [], []]},
        {"ops": ["FrontMiddleBackQueue", "pushBack", "pushBack", "pushBack", "pushBack", "popMiddle", "popMiddle", "popMiddle", "popMiddle"], "args": [[], [1], [2], [3], [4], [], [], [], []]},
        {"ops": ["FrontMiddleBackQueue", "pushFront", "pushFront", "pushFront", "pushFront", "popMiddle", "popBack", "popFront", "popMiddle"], "args": [[], [1], [2], [3], [4], [], [], [], []]},
        {"ops": ["FrontMiddleBackQueue", "pushBack", "pushMiddle", "pushFront", "pushMiddle", "pushBack", "popFront", "popBack", "popMiddle", "popMiddle", "popMiddle"], "args": [[], [10], [20], [30], [40], [50], [], [], [], [], []]},
        {"ops": ["FrontMiddleBackQueue", "pushFront", "popMiddle", "pushBack", "popMiddle", "popBack"], "args": [[], [1000000000], [], [999999999], [], []]},
    ]
    rng = random.Random(4401)
    ops = ["FrontMiddleBackQueue"]
    args = [[]]
    names = ["pushFront", "pushMiddle", "pushBack", "popFront", "popMiddle", "popBack"]
    for _ in range(500):
        op = rng.choice(names)
        ops.append(op)
        if op.startswith("push"):
            args.append([rng.randint(1, 100000)])
        else:
            args.append([])
    tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_45() -> list[dict]:
    tests = [
        {"ops": ["AllOneTracker", "inc", "getMinCount", "getMaxCount", "dec", "getMinCount", "getMaxCount"], "args": [[], ["k"], [], [], ["k"], [], []]},
        {"ops": ["AllOneTracker", "inc", "inc", "inc", "dec", "dec", "getCount", "getMinCount", "getMaxCount"], "args": [[], ["a"], ["a"], ["a"], ["a"], ["a"], ["a"], [], []]},
        {"ops": ["AllOneTracker", "inc", "inc", "inc", "inc", "getMinCount", "getMaxCount", "dec", "getMinCount"], "args": [[], ["a"], ["b"], ["b"], ["c"], [], [], ["a"], []]},
        {"ops": ["AllOneTracker", "inc", "inc", "dec", "dec", "dec", "getCount", "getMaxCount"], "args": [[], ["x"], ["x"], ["x"], ["x"], ["x"], ["x"], []]},
        {"ops": ["AllOneTracker", "inc", "inc", "inc", "inc", "inc", "dec", "dec", "getMinCount", "getMaxCount"], "args": [[], ["a"], ["a"], ["a"], ["b"], ["c"], ["a"], ["b"], [], []]},
        {"ops": ["AllOneTracker", "inc", "inc", "inc", "inc", "inc", "inc", "dec", "getMinCount", "getMaxCount"], "args": [[], ["p"], ["p"], ["p"], ["q"], ["q"], ["q"], ["p"], [], []]},
        {"ops": ["AllOneTracker", "inc", "dec", "inc", "inc", "getCount", "getMinCount", "getMaxCount"], "args": [[], ["re"], ["re"], ["re"], ["re"], ["re"], [], []]},
        {"ops": ["AllOneTracker", "inc", "inc", "inc", "inc", "dec", "dec", "getMaxCount", "getMinCount", "getCount"], "args": [[], ["k1"], ["k2"], ["k3"], ["k1"], ["k2"], ["k3"], [], [], ["k1"]]},
    ]
    rng = random.Random(4501)
    vocab = [f"k{i}" for i in range(25)]
    ops = ["AllOneTracker"]
    args = [[]]
    for _ in range(500):
        r = rng.random()
        if r < 0.42:
            ops.append("inc")
            args.append([rng.choice(vocab)])
        elif r < 0.72:
            ops.append("dec")
            args.append([rng.choice(vocab)])
        elif r < 0.82:
            ops.append("getMaxCount")
            args.append([])
        elif r < 0.92:
            ops.append("getMinCount")
            args.append([])
        else:
            ops.append("getCount")
            args.append([rng.choice(vocab)])
    tests.append({"ops": ops, "args": args})
    return tests


def gen_hidden_46() -> list[dict]:
    tests = [
        {"ops": ["TextEditor", "addText", "deleteText", "deleteText", "cursorRight"], "args": [[], ["abc"], [2], [5], [5]]},
        {"ops": ["TextEditor", "addText", "cursorLeft", "cursorRight"], "args": [[], ["abcdefghijklmno"], [3], [1]]},
        {"ops": ["TextEditor", "addText", "cursorLeft", "deleteText", "cursorRight"], "args": [[], ["hello"], [5], [3], [5]]},
        {"ops": ["TextEditor", "addText", "cursorLeft", "addText", "cursorLeft", "deleteText", "cursorRight"], "args": [[], ["world"], [5], ["hello"], [2], [1], [10]]},
        {"ops": ["TextEditor", "addText", "cursorLeft", "cursorLeft", "cursorRight", "cursorRight"], "args": [[], ["abcdefghijk"], [4], [4], [3], [20]]},
        {"ops": ["TextEditor", "addText", "deleteText", "addText", "cursorLeft", "deleteText", "cursorRight"], "args": [[], ["zzzzzzzzzzzz"], [12], ["abcdef"], [2], [2], [2]]},
        {"ops": ["TextEditor", "addText", "cursorLeft", "addText", "cursorLeft", "addText", "cursorRight"], "args": [[], ["end"], [3], ["mid"], [3], ["beg"], [9]]},
        {"ops": ["TextEditor", "addText", "cursorLeft", "deleteText", "addText", "cursorLeft", "cursorRight"], "args": [[], ["algorithmplay"], [4], [5], ["data"], [1], [10]]},
    ]
    rng = random.Random(4601)
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    ops = ["TextEditor"]
    args = [[]]
    for _ in range(420):
        r = rng.random()
        if r < 0.35:
            length = rng.randint(1, 8)
            s = "".join(rng.choice(alphabet) for _ in range(length))
            ops.append("addText")
            args.append([s])
        elif r < 0.55:
            ops.append("deleteText")
            args.append([rng.randint(1, 10)])
        elif r < 0.78:
            ops.append("cursorLeft")
            args.append([rng.randint(1, 15)])
        else:
            ops.append("cursorRight")
            args.append([rng.randint(1, 15)])
    tests.append({"ops": ops, "args": args})
    return tests


HIDDEN_GENERATORS = {
    "gen_hidden_41": gen_hidden_41,
    "gen_hidden_42": gen_hidden_42,
    "gen_hidden_43": gen_hidden_43,
    "gen_hidden_44": gen_hidden_44,
    "gen_hidden_45": gen_hidden_45,
    "gen_hidden_46": gen_hidden_46,
}


def main():
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

    print(f"Generated {len(TASKS)} linked-lists problems (17-46)")


if __name__ == "__main__":
    main()
