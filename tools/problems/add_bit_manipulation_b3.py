#!/usr/bin/env python3
"""Generate bit-manipulation problems 71-100 for AlgoPlay (Batch 3)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
BASE = ROOT / "problems" / "bit-manipulation"

ALLOWED_SUBTOPICS = {
    "XOR Tricks",
    "Counting Bits",
    "Two Complement",
    "Fast Exponentiation",
}

ALLOWED_COMPANIES = {
    "Google",
    "Amazon",
    "Microsoft",
    "Meta",
    "Apple",
    "Netflix",
    "Uber",
    "Goldman Sachs",
    "Adobe",
    "Atlassian",
    "Salesforce",
    "Oracle",
    "Bloomberg",
    "LinkedIn",
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
    }[t]


def _lcg_array(n: int, mod: int, seed: int = 1337, offset: int = 0) -> list[int]:
    out = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF
        out.append((x % mod) + offset)
    return out


TASKS = [
    # ------------------------------------------------------------------
    # XOR Tricks (71-78)
    # ------------------------------------------------------------------
    {
        "slug": "71-sum-of-all-subset-xor-totals",
        "title": "Sum of All Subset XOR Totals",
        "difficulty": "Easy",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "The XOR total of a subset is defined as the bitwise XOR of all its elements, or `0` if the "
            "subset is empty. Given an array `nums` of non-negative integers, return the sum of the XOR "
            "totals for every one of the `2^n` subsets of `nums` (counting subsets with identical elements "
            "at different indices separately)."
        ),
        "cons": [
            "1 <= nums.length <= 30",
            "0 <= nums[i] <= 10^9",
        ],
        "hints": [
            "Consider each bit position `b` independently: if no element has bit `b` set, it contributes `0`; if at least one element has bit `b` set, exactly half (`2^(n - 1)`) of all subsets have an odd number of 1s at bit `b`.",
            "Therefore, the sum of all subset XOR totals equals `(nums[0] | nums[1] | ... | nums[n - 1]) << (n - 1)`.",
        ],
        "explanations": [
            "Subsets {}, {1}, {3}, {1, 3} have XOR totals 0, 1, 3, 2 whose sum is 6.",
            "The bitwise OR of [5, 1, 6] is 7, and 7 * 2^(3 - 1) = 7 * 4 = 28.",
            "The bitwise OR of [3, 4, 5, 6, 7, 8] is 15, and 15 * 2^5 = 480.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "subsetXorSum",
        "params": [("nums", "int[]")],
        "ret": "long",
        "py": """        or_all = 0
        for x in nums:
            or_all |= x
        return or_all << (len(nums) - 1)""",
        "java": """        long orAll = 0L;
        for (int x : nums) {
            orAll |= x;
        }
        return orAll << (nums.length - 1);""",
        "visible": [
            {"nums": [1, 3]},
            {"nums": [5, 1, 6]},
            {"nums": [3, 4, 5, 6, 7, 8]},
        ],
        "hidden": [
            {"nums": [0]},
            {"nums": [7]},
            {"nums": [0, 0, 0, 0]},
            {"nums": [1, 1, 1]},
            {"nums": [2, 4, 8, 16]},
            {"nums": [1000000000]},
            {"nums": [1000000000, 500000000, 250000000]},
            {"nums": [1 << i for i in range(20)]},
            {"nums": _lcg_array(30, 1_000_000_000, seed=71)},
        ],
    },
    {
        "slug": "72-find-xor-beauty-of-array",
        "title": "Find XOR-Beauty of Array",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Microsoft", "Bloomberg"],
        "desc": (
            "Given a 0-indexed integer array `nums` of length `n`, the effective value of any ordered index "
            "triplet `(i, j, k)` with `0 <= i, j, k < n` is defined as `((nums[i] | nums[j]) & nums[k])`. "
            "The XOR-beauty of `nums` is the bitwise XOR of the effective values of all `n^3` ordered "
            "triplets `(i, j, k)`. Return the XOR-beauty of `nums`."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i] <= 10^9",
        ],
        "hints": [
            "Notice symmetry in `(i, j)`: for any `i != j`, the triplets `(i, j, k)` and `(j, i, k)` produce the exact same effective value and cancel each other out under XOR, leaving only triplets with `i == j`.",
            "When `i == j`, the expression simplifies to `nums[i] & nums[k]`, where again `i != k` pairs cancel by symmetry, leaving only `i == j == k` and reducing the entire answer to the XOR of all elements of `nums`.",
        ],
        "explanations": [
            "Evaluating all 8 triplets for [1, 4] and XORing them yields 1 ^ 4 = 5.",
            "Symmetric off-diagonal triplets cancel out, leaving the XOR of all elements which equals 34.",
            "The only triplet (0, 0, 0) gives (7 | 7) & 7 = 7.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "xorBeauty",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        ans = 0
        for x in nums:
            ans ^= x
        return ans""",
        "java": """        int ans = 0;
        for (int x : nums) {
            ans ^= x;
        }
        return ans;""",
        "visible": [
            {"nums": [1, 4]},
            {"nums": [15, 45, 20, 2, 34, 35, 5, 44, 32, 30]},
            {"nums": [7]},
        ],
        "hidden": [
            {"nums": [0]},
            {"nums": [5, 5]},
            {"nums": [1, 2, 3]},
            {"nums": [8, 8, 8]},
            {"nums": [0, 1000000000, 536870911]},
            {"nums": [1023, 511, 255, 127, 63, 31, 15, 7, 3, 1]},
            {"nums": [42, 99, 42, 99, 17]},
            {"nums": _lcg_array(500, 1_000_000_000, seed=72)},
            {"nums": _lcg_array(3000, 1_000_000_000, seed=720)},
        ],
    },
    {
        "slug": "73-count-subarrays-with-given-xor",
        "title": "Count Subarrays With Given XOR",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Amazon", "Google", "Adobe"],
        "desc": (
            "Given an array `nums` of non-negative integers and a target non-negative integer `k`, return "
            "the total number of non-empty contiguous subarrays of `nums` whose elements have a bitwise XOR "
            "equal to `k`."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i], k <= 10^9",
        ],
        "hints": [
            "Maintain the running prefix XOR `pref = nums[0] ^ ... ^ nums[i]`. A subarray `(j..i]` has XOR equal to `k` if and only if `pref[j] ^ pref[i] == k`, i.e., `pref[j] == pref[i] ^ k`.",
            "Store frequencies of all seen prefix XOR values in a hash map initialized with `{0: 1}` to count valid subarrays ending at each index in O(1) average time.",
        ],
        "explanations": [
            "The 4 subarrays with XOR 6 are [4, 2], [4, 2, 2, 6, 4], [2, 2, 6], and [6].",
            "The 2 subarrays with XOR 5 are [5] and [5, 6, 7, 8, 9].",
            "Every one of the 6 non-empty subarrays of [0, 0, 0] has XOR 0.",
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "countSubarraysWithXor",
        "params": [("nums", "int[]"), ("k", "int")],
        "ret": "long",
        "py": """        freq = {0: 1}
        pref = 0
        ans = 0
        for x in nums:
            pref ^= x
            ans += freq.get(pref ^ k, 0)
            freq[pref] = freq.get(pref, 0) + 1
        return ans""",
        "java": """        Map<Integer, Integer> freq = new HashMap<>();
        freq.put(0, 1);
        int pref = 0;
        long ans = 0L;
        for (int x : nums) {
            pref ^= x;
            ans += freq.getOrDefault(pref ^ k, 0);
            freq.put(pref, freq.getOrDefault(pref, 0) + 1);
        }
        return ans;""",
        "visible": [
            {"nums": [4, 2, 2, 6, 4], "k": 6},
            {"nums": [5, 6, 7, 8, 9], "k": 5},
            {"nums": [0, 0, 0], "k": 0},
        ],
        "hidden": [
            {"nums": [7], "k": 7},
            {"nums": [7], "k": 3},
            {"nums": [1, 1, 1, 1], "k": 0},
            {"nums": [1, 1, 1, 1], "k": 1},
            {"nums": [2, 3, 1, 6, 7], "k": 0},
            {"nums": [1000000000, 1000000000, 5], "k": 5},
            {"nums": [0] * 100, "k": 0},
            {"nums": _lcg_array(400, 16, seed=73), "k": 7},
            {"nums": _lcg_array(3000, 64, seed=730), "k": 42},
        ],
    },
    {
        "slug": "74-minimum-xor-pair-in-array",
        "title": "Minimum XOR Value of Any Pair",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Amazon", "Goldman Sachs"],
        "desc": (
            "Given an integer array `nums` containing at least two non-negative integers, find and return "
            "the minimum possible value of `nums[i] ^ nums[j]` over all distinct index pairs `0 <= i < j < nums.length`."
        ),
        "cons": [
            "2 <= nums.length <= 10^5",
            "0 <= nums[i] <= 10^9",
        ],
        "hints": [
            "For any three sorted integers `a <= b <= c`, consider the highest bit where `a` and `c` differ: `b` must agree with either `a` or `c` on that bit, so `min(a ^ b, b ^ c) <= a ^ c`.",
            "Sort the array and take the minimum bitwise XOR over adjacent pairs `(nums[i], nums[i + 1])`.",
        ],
        "explanations": [
            "Pair (3, 5) has XOR 3 ^ 5 = 6, which is smaller than 9 ^ 5 = 12 and 9 ^ 3 = 10.",
            "Pair (4, 7) achieves the minimum XOR 4 ^ 7 = 3.",
            "The duplicate elements 8 and 8 produce 8 ^ 8 = 0.",
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "method": "minXorPair",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        arr = sorted(nums)
        ans = arr[0] ^ arr[1]
        for i in range(1, len(arr) - 1):
            v = arr[i] ^ arr[i + 1]
            if v < ans:
                ans = v
        return ans""",
        "java": """        int[] arr = nums.clone();
        Arrays.sort(arr);
        int ans = arr[0] ^ arr[1];
        for (int i = 1; i < arr.length - 1; i++) {
            int v = arr[i] ^ arr[i + 1];
            if (v < ans) ans = v;
        }
        return ans;""",
        "visible": [
            {"nums": [9, 5, 3]},
            {"nums": [0, 4, 7, 9]},
            {"nums": [8, 2, 8]},
        ],
        "hidden": [
            {"nums": [0, 1]},
            {"nums": [0, 1000000000]},
            {"nums": [15, 14, 13, 12]},
            {"nums": [1, 2, 4, 8, 16, 32]},
            {"nums": [100, 101, 200, 204, 300]},
            {"nums": [536870912, 536870911, 268435456]},
            {"nums": [7, 7]},
            {"nums": _lcg_array(500, 1_000_000_000, seed=74)},
            {"nums": _lcg_array(3000, 1_000_000_000, seed=740)},
        ],
    },
    {
        "slug": "75-total-xor-of-all-subarrays",
        "title": "Total XOR of All Subarray XORs",
        "difficulty": "Easy",
        "subtopic": "XOR Tricks",
        "companies": ["Amazon", "Microsoft", "Atlassian"],
        "desc": (
            "Given an integer array `nums`, compute the bitwise XOR of every non-empty contiguous subarray, "
            "and then return the bitwise XOR of all those subarray XOR values combined."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i] <= 10^9",
        ],
        "hints": [
            "Count how many contiguous subarrays include index `i`: there are `(i + 1)` choices for the left endpoint and `(n - i)` choices for the right endpoint, giving `(i + 1) * (n - i)` occurrences.",
            "Because `x ^ x = 0`, `nums[i]` contributes only when `(i + 1) * (n - i)` is odd, which occurs if and only if `n` is odd and `i` is even.",
        ],
        "explanations": [
            "Subarray XORs are 1, 2, 3, (1^2)=3, (2^3)=1, (1^2^3)=0; XORing all of them gives 2.",
            "Because length n = 4 is even, every element appears in an even number of subarrays, so the result is 0.",
            "With a single element [9], the only subarray has XOR 9.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "totalSubarrayXor",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        n = len(nums)
        if n % 2 == 0:
            return 0
        ans = 0
        for i in range(0, n, 2):
            ans ^= nums[i]
        return ans""",
        "java": """        int n = nums.length;
        if ((n & 1) == 0) return 0;
        int ans = 0;
        for (int i = 0; i < n; i += 2) {
            ans ^= nums[i];
        }
        return ans;""",
        "visible": [
            {"nums": [1, 2, 3]},
            {"nums": [4, 5, 7, 5]},
            {"nums": [9]},
        ],
        "hidden": [
            {"nums": [0]},
            {"nums": [1, 2]},
            {"nums": [3, 4, 5]},
            {"nums": [10, 20, 30, 40, 50]},
            {"nums": [7, 7, 7, 7, 7]},
            {"nums": [1000000000, 999999999, 1000000000]},
            {"nums": _lcg_array(500, 1_000_000_000, seed=75)},
            {"nums": _lcg_array(501, 1_000_000_000, seed=751)},
            {"nums": _lcg_array(3001, 1_000_000_000, seed=7501)},
        ],
    },
    {
        "slug": "76-kth-smallest-subset-xor",
        "title": "K-th Smallest Distinct Subset XOR",
        "difficulty": "Hard",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Meta", "Goldman Sachs"],
        "desc": (
            "Given an array `nums` of non-negative integers and a 1-indexed positive integer `k`, consider "
            "the set of all **distinct** values that can be formed as the bitwise XOR of any subset of "
            "`nums` (including the empty subset, whose XOR is `0`). Return the `k`-th smallest distinct "
            "value in this set, or `-1` if fewer than `k` distinct subset XOR values exist."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i] <= 10^9",
            "1 <= k <= 10^9",
        ],
        "hints": [
            "Build a linear XOR basis over GF(2) for `nums`, then reduce it to reduced row-echelon form (RREF) so that every basis vector's pivot bit is cleared in all higher basis vectors.",
            "If the basis has rank `r`, there are exactly `2^r` distinct subset XORs; sort the `r` basis vectors in ascending order and combine them according to the binary bits of `k - 1`.",
        ],
        "explanations": [
            "The distinct subset XORs of [1, 2, 3] are {0, 1, 2, 3}; the 3rd smallest is 2.",
            "The distinct subset XORs of [4, 2, 6] are {0, 2, 4, 6} (only 4 values), so k = 5 returns -1.",
            "The distinct subset XORs of [5, 3] are {0, 3, 5, 6}; the 4th smallest is 6.",
        ],
        "time": "O(n log M + log^2 M)",
        "space": "O(log M)",
        "method": "kthSmallestSubsetXor",
        "params": [("nums", "int[]"), ("k", "long")],
        "ret": "int",
        "py": """        basis = [0] * 30
        for x in nums:
            v = x
            for b in range(29, -1, -1):
                if (v >> b) & 1:
                    if basis[b] == 0:
                        basis[b] = v
                        break
                    v ^= basis[b]
        for b in range(30):
            if basis[b]:
                for high in range(b + 1, 30):
                    if (basis[high] >> b) & 1:
                        basis[high] ^= basis[b]
        vecs = [basis[b] for b in range(30) if basis[b]]
        r = len(vecs)
        if k > (1 << r):
            return -1
        idx = k - 1
        ans = 0
        for i in range(r):
            if (idx >> i) & 1:
                ans ^= vecs[i]
        return ans""",
        "java": """        int[] basis = new int[30];
        for (int x : nums) {
            int v = x;
            for (int b = 29; b >= 0; b--) {
                if (((v >> b) & 1) != 0) {
                    if (basis[b] == 0) {
                        basis[b] = v;
                        break;
                    }
                    v ^= basis[b];
                }
            }
        }
        for (int b = 0; b < 30; b++) {
            if (basis[b] != 0) {
                for (int high = b + 1; high < 30; high++) {
                    if (((basis[high] >> b) & 1) != 0) {
                        basis[high] ^= basis[b];
                    }
                }
            }
        }
        int[] vecs = new int[30];
        int r = 0;
        for (int b = 0; b < 30; b++) {
            if (basis[b] != 0) vecs[r++] = basis[b];
        }
        if (k > (1L << r)) return -1;
        long idx = k - 1L;
        int ans = 0;
        for (int i = 0; i < r; i++) {
            if (((idx >> i) & 1L) != 0L) {
                ans ^= vecs[i];
            }
        }
        return ans;""",
        "visible": [
            {"nums": [1, 2, 3], "k": 3},
            {"nums": [4, 2, 6], "k": 5},
            {"nums": [5, 3], "k": 4},
        ],
        "hidden": [
            {"nums": [0, 0, 0], "k": 1},
            {"nums": [0, 0, 0], "k": 2},
            {"nums": [8, 4, 2, 1], "k": 1},
            {"nums": [8, 4, 2, 1], "k": 16},
            {"nums": [8, 4, 2, 1], "k": 17},
            {"nums": [10, 6, 12, 15, 3], "k": 6},
            {"nums": [1 << i for i in range(30)], "k": 1000000000},
            {"nums": [7, 14, 28, 56, 112, 224], "k": 37},
            {"nums": _lcg_array(2000, 1_000_000_000, seed=76), "k": 123456789},
        ],
    },
    {
        "slug": "77-maximum-xor-with-element-threshold",
        "title": "Maximum XOR With an Element Threshold",
        "difficulty": "Hard",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Meta", "Uber"],
        "desc": (
            "You are given an array `nums` of non-negative integers and a 2D array `queries` where "
            "`queries[i] = [xi, mi]`. The answer to the `i`-th query is the maximum bitwise XOR value of "
            "`xi` and any element `nums[j]` such that `nums[j] <= mi`. If every element in `nums` is "
            "strictly greater than `mi`, the answer to that query is `-1`. Return an integer array `answer` "
            "of length `queries.length` containing the answers to all queries."
        ),
        "cons": [
            "1 <= nums.length, queries.length <= 5 * 10^4",
            "queries[i].length == 2",
            "0 <= nums[i], xi, mi <= 10^9",
        ],
        "hints": [
            "Sort `nums` in ascending order and sort the queries offline by their upper bound `mi` while keeping track of each query's original index.",
            "Incrementally insert all `nums[j] <= mi` into a 30-bit binary trie, then answer query `xi` by greedily taking the opposite bit branch from MSB to LSB.",
        ],
        "explanations": [
            "For [3,1] pick 0 -> 3^0=3; for [1,3] pick 2 -> 1^2=3; for [5,6] pick 2 -> 5^2=7.",
            "For [12,4] pick 3 -> 12^3=15; for [8,1] no element <= 1 so -1; for [6,3] pick 3 -> 6^3=5.",
            "Only 0 is <= 0, giving 5^0 = 5 and 0^0 = 0.",
        ],
        "time": "O((n + q) log M + n log n + q log q)",
        "space": "O(n log M + q)",
        "method": "maximizeXor",
        "params": [("nums", "int[]"), ("queries", "int[][]")],
        "ret": "int[]",
        "py": """        arr = sorted(nums)
        order = sorted(range(len(queries)), key=lambda i: queries[i][1])
        c0 = [0]
        c1 = [0]
        ans = [-1] * len(queries)
        ptr = 0
        n = len(arr)
        for qi in order:
            x, m = queries[qi]
            while ptr < n and arr[ptr] <= m:
                v = arr[ptr]
                ptr += 1
                node = 0
                for b in range(29, -1, -1):
                    if (v >> b) & 1:
                        nxt = c1[node]
                        if nxt == 0:
                            nxt = len(c0)
                            c1[node] = nxt
                            c0.append(0)
                            c1.append(0)
                        node = nxt
                    else:
                        nxt = c0[node]
                        if nxt == 0:
                            nxt = len(c0)
                            c0[node] = nxt
                            c0.append(0)
                            c1.append(0)
                        node = nxt
            if ptr == 0:
                ans[qi] = -1
            else:
                node = 0
                best = 0
                for b in range(29, -1, -1):
                    if (x >> b) & 1:
                        if c0[node]:
                            best |= 1 << b
                            node = c0[node]
                        else:
                            node = c1[node]
                    else:
                        if c1[node]:
                            best |= 1 << b
                            node = c1[node]
                        else:
                            node = c0[node]
                ans[qi] = best
        return ans""",
        "java": """        int n = nums.length;
        int q = queries.length;
        int[] arr = nums.clone();
        Arrays.sort(arr);
        Integer[] order = new Integer[q];
        for (int i = 0; i < q; i++) order[i] = i;
        Arrays.sort(order, (a, b) -> Integer.compare(queries[a][1], queries[b][1]));

        int maxNodes = n * 31 + 2;
        int[] c0 = new int[maxNodes];
        int[] c1 = new int[maxNodes];
        int nodes = 1;

        int[] ans = new int[q];
        int ptr = 0;
        for (int qi : order) {
            int x = queries[qi][0];
            int m = queries[qi][1];
            while (ptr < n && arr[ptr] <= m) {
                int v = arr[ptr++];
                int node = 0;
                for (int b = 29; b >= 0; b--) {
                    if (((v >> b) & 1) != 0) {
                        if (c1[node] == 0) c1[node] = nodes++;
                        node = c1[node];
                    } else {
                        if (c0[node] == 0) c0[node] = nodes++;
                        node = c0[node];
                    }
                }
            }
            if (ptr == 0) {
                ans[qi] = -1;
            } else {
                int node = 0;
                int best = 0;
                for (int b = 29; b >= 0; b--) {
                    if (((x >> b) & 1) != 0) {
                        if (c0[node] != 0) {
                            best |= 1 << b;
                            node = c0[node];
                        } else {
                            node = c1[node];
                        }
                    } else {
                        if (c1[node] != 0) {
                            best |= 1 << b;
                            node = c1[node];
                        } else {
                            node = c0[node];
                        }
                    }
                }
                ans[qi] = best;
            }
        }
        return ans;""",
        "visible": [
            {"nums": [0, 1, 2, 3, 4], "queries": [[3, 1], [1, 3], [5, 6]]},
            {"nums": [5, 2, 4, 6, 6, 3], "queries": [[12, 4], [8, 1], [6, 3]]},
            {"nums": [0], "queries": [[5, 0], [0, 0]]},
        ],
        "hidden": [
            {"nums": [10], "queries": [[5, 9], [5, 10], [10, 10]]},
            {"nums": [1, 1, 1], "queries": [[1, 0], [1, 1], [0, 1]]},
            {"nums": [1000000000, 0], "queries": [[1000000000, 0], [1000000000, 1000000000], [536870911, 1000000000]]},
            {"nums": [7, 15, 31, 63], "queries": [[0, 6], [0, 7], [16, 15], [16, 31]]},
            {"nums": [1, 2, 4, 8, 16, 32], "queries": [[31, 15], [31, 16], [63, 64]]},
            {"nums": [9, 8, 7, 6, 5], "queries": [[1, 4], [1, 5], [1, 9]]},
            {"nums": _lcg_array(50, 1000, seed=77), "queries": [[x, y] for x, y in zip(_lcg_array(20, 1000, seed=771), _lcg_array(20, 1000, seed=772))]},
            {"nums": _lcg_array(200, 1_000_000_000, seed=773), "queries": [[x, y] for x, y in zip(_lcg_array(100, 1_000_000_000, seed=774), _lcg_array(100, 1_000_000_000, seed=775))]},
            {"nums": _lcg_array(1000, 1_000_000_000, seed=776), "queries": [[x, y] for x, y in zip(_lcg_array(500, 1_000_000_000, seed=777), _lcg_array(500, 1_000_000_000, seed=778))]},
        ],
    },
    {
        "slug": "78-minimum-xor-sum-of-two-arrays",
        "title": "Minimum XOR Sum of Two Arrays",
        "difficulty": "Hard",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "You are given two integer arrays `nums1` and `nums2` of equal length `n`. The XOR sum of the "
            "two arrays is `(nums1[0] ^ nums2[0]) + (nums1[1] ^ nums2[1]) + ... + (nums1[n - 1] ^ nums2[n - 1])`. "
            "You may rearrange the elements of `nums2` in any order. Return the minimum possible XOR sum "
            "after optimally rearranging `nums2`."
        ),
        "cons": [
            "1 <= nums1.length == nums2.length <= 14",
            "0 <= nums1[i], nums2[i] <= 10^7",
        ],
        "hints": [
            "Represent the subset of `nums2` indices already matched to the first `i = popcount(mask)` elements of `nums1` as an `n`-bit integer `mask`.",
            "Compute `dp[mask]` over all `2^n` masks by trying each set bit `j` in `mask` as the partner of `nums1[popcount(mask) - 1]`, taking the minimum of `dp[mask ^ (1 << j)] + (nums1[i - 1] ^ nums2[j])`.",
        ],
        "explanations": [
            "Rearranging nums2 to [3, 2] yields (1 ^ 3) + (2 ^ 2) = 2 + 0 = 2.",
            "Rearranging nums2 to [5, 4, 3] yields (1 ^ 5) + (0 ^ 4) + (3 ^ 3) = 4 + 4 + 0 = 8.",
            "With one element each, 7 ^ 7 = 0.",
        ],
        "time": "O(n * 2^n)",
        "space": "O(2^n)",
        "method": "minimumXorSum",
        "params": [("nums1", "int[]"), ("nums2", "int[]")],
        "ret": "int",
        "py": """        n = len(nums1)
        size = 1 << n
        INF = 10**18
        dp = [INF] * size
        dp[0] = 0
        for mask in range(1, size):
            i = mask.bit_count() - 1
            a = nums1[i]
            best = INF
            rem = mask
            while rem:
                lb = rem & -rem
                j = lb.bit_length() - 1
                cand = dp[mask ^ lb] + (a ^ nums2[j])
                if cand < best:
                    best = cand
                rem ^= lb
            dp[mask] = best
        return dp[size - 1]""",
        "java": """        int n = nums1.length;
        int size = 1 << n;
        int[] dp = new int[size];
        Arrays.fill(dp, Integer.MAX_VALUE / 2);
        dp[0] = 0;
        for (int mask = 1; mask < size; mask++) {
            int i = Integer.bitCount(mask) - 1;
            int a = nums1[i];
            int best = Integer.MAX_VALUE / 2;
            int rem = mask;
            while (rem != 0) {
                int lb = rem & -rem;
                int j = Integer.numberOfTrailingZeros(lb);
                int cand = dp[mask ^ lb] + (a ^ nums2[j]);
                if (cand < best) best = cand;
                rem ^= lb;
            }
            dp[mask] = best;
        }
        return dp[size - 1];""",
        "visible": [
            {"nums1": [1, 2], "nums2": [2, 3]},
            {"nums1": [1, 0, 3], "nums2": [5, 3, 4]},
            {"nums1": [7], "nums2": [7]},
        ],
        "hidden": [
            {"nums1": [0], "nums2": [10000000]},
            {"nums1": [1, 2, 3, 4], "nums2": [4, 3, 2, 1]},
            {"nums1": [0, 0, 0, 0], "nums2": [1, 2, 4, 8]},
            {"nums1": [72, 97, 8, 32, 15], "nums2": [63, 97, 57, 60, 83]},
            {"nums1": [10, 20, 30, 40, 50, 60], "nums2": [60, 50, 40, 30, 20, 10]},
            {"nums1": [1, 3, 7, 15, 31, 63, 127], "nums2": [2, 6, 14, 30, 62, 126, 254]},
            {"nums1": _lcg_array(10, 100000, seed=781), "nums2": _lcg_array(10, 100000, seed=782)},
            {"nums1": _lcg_array(12, 10_000_000, seed=783), "nums2": _lcg_array(12, 10_000_000, seed=784)},
            {"nums1": _lcg_array(14, 10_000_000, seed=785), "nums2": _lcg_array(14, 10_000_000, seed=786)},
        ],
    },
    # ------------------------------------------------------------------
    # Counting Bits (79-86)
    # ------------------------------------------------------------------
    {
        "slug": "79-bit-changes-to-make-integers-equal",
        "title": "Number of Bit Changes to Make Two Integers Equal",
        "difficulty": "Easy",
        "subtopic": "Counting Bits",
        "companies": ["Amazon", "Apple", "Microsoft"],
        "desc": (
            "You are given two non-negative integers `n` and `k`. In one operation, you may choose any bit "
            "in the binary representation of `n` that is currently equal to `1` and change it to `0` (you "
            "cannot change a `0` bit to `1`). Return the minimum number of operations needed to make `n` "
            "equal to `k`, or `-1` if it is impossible."
        ),
        "cons": [
            "0 <= n, k <= 10^9",
        ],
        "hints": [
            "Since you can only clear `1` bits to `0`, every `1` bit in `k` must already be a `1` bit in `n`, which holds if and only if `(n & k) == k`.",
            "When `(n & k) == k`, the exact number of bits that must be cleared is the population count of `n ^ k`.",
        ],
        "explanations": [
            "13 is 1101 and 4 is 0100 in binary; clearing bits 3 and 0 takes 2 changes.",
            "21 already equals 21, requiring 0 bit changes.",
            "14 is 1110 and 13 is 1101; bit 0 is 0 in 14 but 1 in 13, so it is impossible.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "minBitChanges",
        "params": [("n", "int"), ("k", "int")],
        "ret": "int",
        "py": """        if (n & k) != k:
            return -1
        return (n ^ k).bit_count()""",
        "java": """        if ((n & k) != k) return -1;
        return Integer.bitCount(n ^ k);""",
        "visible": [
            {"n": 13, "k": 4},
            {"n": 21, "k": 21},
            {"n": 14, "k": 13},
        ],
        "hidden": [
            {"n": 0, "k": 0},
            {"n": 0, "k": 1},
            {"n": 1, "k": 0},
            {"n": 1023, "k": 0},
            {"n": 1023, "k": 341},
            {"n": 536870911, "k": 1},
            {"n": 1000000000, "k": 1000000000},
            {"n": 999999999, "k": 511},
            {"n": 1000000000, "k": 536870912},
        ],
    },
    {
        "slug": "80-find-if-array-can-be-sorted-by-set-bits",
        "title": "Find if Array Can Be Sorted by Set Bits",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "You are given a 0-indexed array `nums` of positive integers. In one operation, you may swap "
            "any two **adjacent** elements if and only if they have the same number of `1` bits in their "
            "binary representation. Return `true` if you can sort `nums` in non-decreasing order using any "
            "number of operations, and `false` otherwise."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "1 <= nums[i] <= 10^9",
        ],
        "hints": [
            "Elements cannot cross into a neighboring group of different popcount, so `nums` splits into maximal contiguous segments of equal popcount.",
            "Within each segment you can sort freely, so the entire array is sortable if and only if every segment's minimum element is greater than or equal to the previous segment's maximum element.",
        ],
        "explanations": [
            "Segments [8, 4, 2] (1 set bit) and [30, 15] (4 set bits) sort to [2, 4, 8] and [15, 30], and 15 >= 8.",
            "The array is already sorted in non-decreasing order.",
            "Segment [3] has max 3 (2 set bits), followed by [16, 8, 4, 2] with min 2 (1 set bit); since 2 < 3, return false.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "canSortBySetBits",
        "params": [("nums", "int[]")],
        "ret": "boolean",
        "py": """        prev_max = 0
        cur_pop = nums[0].bit_count()
        cur_min = nums[0]
        cur_max = nums[0]
        for x in nums[1:]:
            p = x.bit_count()
            if p == cur_pop:
                if x < cur_min:
                    cur_min = x
                if x > cur_max:
                    cur_max = x
            else:
                if cur_min < prev_max:
                    return False
                prev_max = cur_max
                cur_pop = p
                cur_min = x
                cur_max = x
        return cur_min >= prev_max""",
        "java": """        int prevMax = 0;
        int curPop = Integer.bitCount(nums[0]);
        int curMin = nums[0];
        int curMax = nums[0];
        for (int i = 1; i < nums.length; i++) {
            int x = nums[i];
            int p = Integer.bitCount(x);
            if (p == curPop) {
                if (x < curMin) curMin = x;
                if (x > curMax) curMax = x;
            } else {
                if (curMin < prevMax) return false;
                prevMax = curMax;
                curPop = p;
                curMin = x;
                curMax = x;
            }
        }
        return curMin >= prevMax;""",
        "visible": [
            {"nums": [8, 4, 2, 30, 15]},
            {"nums": [1, 2, 3, 4, 5]},
            {"nums": [3, 16, 8, 4, 2]},
        ],
        "hidden": [
            {"nums": [1]},
            {"nums": [2, 1]},
            {"nums": [3, 1]},
            {"nums": [7, 7, 7]},
            {"nums": [20, 16]},
            {"nums": [6, 5, 3, 15, 7, 14, 30, 29]},
            {"nums": [6, 5, 3, 15, 14, 7, 30, 23, 16]},
            {"nums": [1 << (29 - i) for i in range(30)] + [(1 << 30) - 1]},
            {"nums": [((1 << 10) - 1) << i for i in range(15, -1, -1)] + [((1 << 11) - 1) << i for i in range(15, -1, -1)]},
        ],
    },
    {
        "slug": "81-shortest-subarray-with-or-at-least-k",
        "title": "Shortest Subarray With Bitwise OR at Least K",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Meta", "Uber"],
        "desc": (
            "Given an array `nums` of non-negative integers and a non-negative integer `k`, a non-empty "
            "contiguous subarray is called special if the bitwise OR of all its elements is at least `k`. "
            "Return the length of the shortest special subarray of `nums`, or `-1` if no special subarray exists."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i], k <= 10^9",
        ],
        "hints": [
            "Bitwise OR is monotonically non-decreasing as a window expands, so a two-pointer sliding window applies once you can remove elements from the left.",
            "Maintain a 30-element array `bitCount[b]` tracking how many elements in the current window have bit `b` set; a bit drops from the window OR only when its count falls to `0`.",
        ],
        "explanations": [
            "The single-element subarray [2] (or [3]) already has bitwise OR >= 2, so the shortest length is 1.",
            "Only the full subarray [2, 1, 8] achieves bitwise OR 11 >= 10, giving length 3.",
            "Even the entire array [1, 2] has bitwise OR 3 < 4, so return -1.",
        ],
        "time": "O(n log M)",
        "space": "O(log M)",
        "method": "minimumSubarrayLength",
        "params": [("nums", "int[]"), ("k", "int")],
        "ret": "int",
        "py": """        n = len(nums)
        counts = [0] * 30
        cur_or = 0
        ans = n + 1
        left = 0
        for right, x in enumerate(nums):
            cur_or |= x
            v = x
            while v:
                lb = v & -v
                counts[lb.bit_length() - 1] += 1
                v ^= lb
            while left <= right and cur_or >= k:
                length = right - left + 1
                if length < ans:
                    ans = length
                y = nums[left]
                left += 1
                while y:
                    lb = y & -y
                    b = lb.bit_length() - 1
                    counts[b] -= 1
                    if counts[b] == 0:
                        cur_or ^= lb
                    y ^= lb
        return -1 if ans > n else ans""",
        "java": """        int n = nums.length;
        int[] counts = new int[30];
        int curOr = 0;
        int ans = n + 1;
        int left = 0;
        for (int right = 0; right < n; right++) {
            int x = nums[right];
            curOr |= x;
            for (int v = x; v != 0; v &= v - 1) {
                counts[Integer.numberOfTrailingZeros(v)]++;
            }
            while (left <= right && curOr >= k) {
                int len = right - left + 1;
                if (len < ans) ans = len;
                int y = nums[left++];
                for (int v = y; v != 0; v &= v - 1) {
                    int b = Integer.numberOfTrailingZeros(v);
                    if (--counts[b] == 0) {
                        curOr ^= (1 << b);
                    }
                }
            }
        }
        return ans > n ? -1 : ans;""",
        "visible": [
            {"nums": [1, 2, 3], "k": 2},
            {"nums": [2, 1, 8], "k": 10},
            {"nums": [1, 2], "k": 4},
        ],
        "hidden": [
            {"nums": [0, 0, 0], "k": 0},
            {"nums": [0, 0, 0], "k": 1},
            {"nums": [1, 2, 32, 21], "k": 55},
            {"nums": [1, 2, 4, 8, 16, 32], "k": 63},
            {"nums": [1, 2, 4, 8, 16, 32], "k": 64},
            {"nums": [16, 8, 4, 2, 1, 31], "k": 31},
            {"nums": [1000000000], "k": 1000000000},
            {"nums": [1 << (i % 20) for i in range(400)], "k": (1 << 20) - 1},
            {"nums": _lcg_array(3000, 1_000_000, seed=81), "k": 1_048_575},
        ],
    },
    {
        "slug": "82-subarray-bitwise-and-closest-to-target",
        "title": "Subarray Bitwise AND Closest to Target",
        "difficulty": "Hard",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": (
            "Given an array `nums` of non-negative integers and a non-negative integer `target`, choose any "
            "non-empty contiguous subarray `nums[l..r]` (`0 <= l <= r < nums.length`) to minimize "
            "`|(nums[l] & nums[l + 1] & ... & nums[r]) - target|`. Return this minimum absolute difference."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i], target <= 10^9",
        ],
        "hints": [
            "As a subarray extends leftward from a fixed right index `r`, its bitwise AND can only clear `1` bits to `0`, so there are at most `31` distinct bitwise AND values ending at `r`.",
            "Maintain the small set of distinct suffix AND values ending at `r - 1`, intersect each with `nums[r]` (plus `nums[r]` itself), and update the best distance to `target`.",
        ],
        "explanations": [
            "Subarrays [3, 7] (AND = 3) and [7, 15] (AND = 7) are both at distance 2 from target 5.",
            "Every subarray has bitwise AND 1000000, giving |1000000 - 1| = 999999.",
            "Subarray [1, 2] has bitwise AND 1 & 2 = 0, matching target 0 with difference 0.",
        ],
        "time": "O(n log M)",
        "space": "O(log M)",
        "method": "closestToTarget",
        "params": [("nums", "int[]"), ("target", "int")],
        "ret": "int",
        "py": """        ans = abs(nums[0] - target)
        cur = set()
        for x in nums:
            nxt = {x}
            for v in cur:
                nxt.add(v & x)
            for v in nxt:
                d = abs(v - target)
                if d < ans:
                    ans = d
            cur = nxt
            if ans == 0:
                return 0
        return ans""",
        "java": """        int ans = Math.abs(nums[0] - target);
        int[] cur = new int[32];
        int[] nxt = new int[32];
        int curLen = 0;
        for (int x : nums) {
            int nxtLen = 0;
            nxt[nxtLen++] = x;
            for (int i = 0; i < curLen; i++) {
                int v = cur[i] & x;
                if (v != nxt[nxtLen - 1]) {
                    nxt[nxtLen++] = v;
                }
            }
            for (int i = 0; i < nxtLen; i++) {
                int d = Math.abs(nxt[i] - target);
                if (d < ans) ans = d;
            }
            if (ans == 0) return 0;
            int[] tmp = cur;
            cur = nxt;
            nxt = tmp;
            curLen = nxtLen;
        }
        return ans;""",
        "visible": [
            {"nums": [9, 12, 3, 7, 15], "target": 5},
            {"nums": [1000000, 1000000, 1000000], "target": 1},
            {"nums": [1, 2, 4, 8, 16], "target": 0},
        ],
        "hidden": [
            {"nums": [0], "target": 0},
            {"nums": [7], "target": 10},
            {"nums": [15, 7, 3, 1], "target": 2},
            {"nums": [1023, 511, 255, 127, 63], "target": 100},
            {"nums": [1000000000, 536870911], "target": 500000000},
            {"nums": [31, 29, 27, 23, 15], "target": 19},
            {"nums": [12, 10, 6, 14, 15], "target": 9},
            {"nums": _lcg_array(500, 1_000_000_000, seed=82), "target": 123456},
            {"nums": _lcg_array(3000, 1_000_000_000, seed=820), "target": 7777777},
        ],
    },
    {
        "slug": "83-maximum-bitmasks-covered-by-k-bits",
        "title": "Maximum Bitmasks Covered by K Bits",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Salesforce"],
        "desc": (
            "You are given an array `masks` of non-negative integers (each strictly less than `2^m`), an "
            "integer bit-width `m`, and an integer `k`. An element `x` in `masks` is covered by a chosen "
            "bitmask `S` if every `1` bit of `x` is also a `1` bit of `S` (that is, `(x & S) == x`). "
            "Choose a bitmask `S` in `[0, 2^m - 1]` with **exact** population count `k` to maximize the "
            "number of covered elements in `masks`, and return that maximum count."
        ),
        "cons": [
            "1 <= masks.length <= 10^4",
            "1 <= m <= 15",
            "0 <= k <= m",
            "0 <= masks[i] < 2^m",
        ],
        "hints": [
            "Count the frequency of each bitmask in an array `dp` of size `2^m`.",
            "Apply Sum Over Subsets (SOS) DP across each bit `0..m - 1` so `dp[S]` holds the exact number of elements in `masks` that are submasks of `S`, then take the maximum of `dp[S]` over all `S` with `popcount(S) == k`.",
        ],
        "explanations": [
            "Choosing S = 5 (binary 101) with k = 2 set bits covers 4 (100), 5 (101), and 1 (001) for a total of 3.",
            "With k = 1, any single bit covers at most 1 of {1, 2, 4}.",
            "With k = 0, S = 0 covers both 0s in [0, 0, 3], giving 2.",
        ],
        "time": "O(n + m * 2^m)",
        "space": "O(2^m)",
        "method": "maxCoveredBitmasks",
        "params": [("masks", "int[]"), ("m", "int"), ("k", "int")],
        "ret": "int",
        "py": """        size = 1 << m
        dp = [0] * size
        for x in masks:
            dp[x] += 1
        for b in range(m):
            bit = 1 << b
            step = bit << 1
            for start in range(bit, size, step):
                for mask in range(start, start + bit):
                    dp[mask] += dp[mask ^ bit]
        ans = 0
        for s in range(size):
            if s.bit_count() == k and dp[s] > ans:
                ans = dp[s]
        return ans""",
        "java": """        int size = 1 << m;
        int[] dp = new int[size];
        for (int x : masks) {
            dp[x]++;
        }
        for (int b = 0; b < m; b++) {
            int bit = 1 << b;
            int step = bit << 1;
            for (int start = bit; start < size; start += step) {
                for (int mask = start; mask < start + bit; mask++) {
                    dp[mask] += dp[mask ^ bit];
                }
            }
        }
        int ans = 0;
        for (int s = 0; s < size; s++) {
            if (Integer.bitCount(s) == k && dp[s] > ans) {
                ans = dp[s];
            }
        }
        return ans;""",
        "visible": [
            {"masks": [4, 5, 1, 2], "m": 3, "k": 2},
            {"masks": [1, 2, 4], "m": 3, "k": 1},
            {"masks": [0, 0, 3], "m": 2, "k": 0},
        ],
        "hidden": [
            {"masks": [1], "m": 1, "k": 0},
            {"masks": [1], "m": 1, "k": 1},
            {"masks": [7, 7, 7, 7], "m": 3, "k": 3},
            {"masks": [7, 7, 7, 7], "m": 3, "k": 2},
            {"masks": [1, 2, 3, 4, 5, 6, 7], "m": 3, "k": 2},
            {"masks": [0, 1, 2, 4, 8, 3, 5, 9, 12], "m": 4, "k": 2},
            {"masks": _lcg_array(300, 1 << 10, seed=83), "m": 10, "k": 5},
            {"masks": _lcg_array(1000, 1 << 12, seed=831), "m": 12, "k": 6},
            {"masks": _lcg_array(2000, 1 << 15, seed=832), "m": 15, "k": 8},
        ],
    },
    {
        "slug": "84-triples-with-bitwise-and-equal-to-zero",
        "title": "Triples With Bitwise AND Equal to Zero",
        "difficulty": "Hard",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Meta", "Oracle"],
        "desc": (
            "Given an integer array `nums` where every element lies in `[0, 2^16 - 1]`, return the number "
            "of ordered index triples `(i, j, k)` (`0 <= i, j, k < nums.length`) such that "
            "`(nums[i] & nums[j] & nums[k]) == 0`."
        ),
        "cons": [
            "1 <= nums.length <= 1000",
            "0 <= nums[i] < 2^16",
        ],
        "hints": [
            "First count how many ordered pairs `(i, j)` produce each pairwise AND value `v = nums[i] & nums[j]` in an array `dp[v]` of size `2^B` (grouping duplicate values of `nums` speeds this up further).",
            "Run Sum Over Subsets (SOS) DP on `dp` so `dp[mask]` stores the count of pairs whose AND is a submask of `mask`; then for each `x` in `nums`, add `dp[((1 << B) - 1) ^ x]`.",
        ],
        "explanations": [
            "There are 12 ordered index triples in [2, 1, 3] whose bitwise AND is 0.",
            "Every one of the 3^3 = 27 triples in [0, 0, 0] has bitwise AND 0.",
            "Every triple in [1, 1] has bitwise AND 1 != 0, so the count is 0.",
        ],
        "time": "O(u^2 + B * 2^B)",
        "space": "O(2^B)",
        "method": "countTriplets",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        max_val = max(nums)
        n = len(nums)
        if max_val == 0:
            return n * n * n
        bits = max_val.bit_length()
        size = 1 << bits
        full = size - 1
        freq = {}
        for x in nums:
            freq[x] = freq.get(x, 0) + 1
        items = list(freq.items())
        dp = [0] * size
        m = len(items)
        for i in range(m):
            a, ca = items[i]
            dp[a] += ca * ca
            for j in range(i + 1, m):
                b, cb = items[j]
                dp[a & b] += 2 * ca * cb
        for b in range(bits):
            bit = 1 << b
            step = bit << 1
            for start in range(bit, size, step):
                for mask in range(start, start + bit):
                    dp[mask] += dp[mask ^ bit]
        ans = 0
        for x, cx in items:
            ans += cx * dp[full ^ x]
        return ans""",
        "java": """        int maxVal = 0;
        for (int x : nums) {
            if (x > maxVal) maxVal = x;
        }
        int n = nums.length;
        if (maxVal == 0) return n * n * n;
        int bits = 32 - Integer.numberOfLeadingZeros(maxVal);
        int size = 1 << bits;
        int full = size - 1;
        int[] freq = new int[size];
        int unique = 0;
        for (int x : nums) {
            if (freq[x]++ == 0) unique++;
        }
        int[] vals = new int[unique];
        int[] cnts = new int[unique];
        int idx = 0;
        for (int v = 0; v < size; v++) {
            if (freq[v] > 0) {
                vals[idx] = v;
                cnts[idx] = freq[v];
                idx++;
            }
        }
        int[] dp = new int[size];
        for (int i = 0; i < unique; i++) {
            int a = vals[i], ca = cnts[i];
            dp[a] += ca * ca;
            for (int j = i + 1; j < unique; j++) {
                dp[a & vals[j]] += 2 * ca * cnts[j];
            }
        }
        for (int b = 0; b < bits; b++) {
            int bit = 1 << b;
            int step = bit << 1;
            for (int start = bit; start < size; start += step) {
                for (int mask = start; mask < start + bit; mask++) {
                    dp[mask] += dp[mask ^ bit];
                }
            }
        }
        int ans = 0;
        for (int i = 0; i < unique; i++) {
            ans += cnts[i] * dp[full ^ vals[i]];
        }
        return ans;""",
        "visible": [
            {"nums": [2, 1, 3]},
            {"nums": [0, 0, 0]},
            {"nums": [1, 1]},
        ],
        "hidden": [
            {"nums": [0]},
            {"nums": [65535]},
            {"nums": [0, 65535]},
            {"nums": [1, 2, 4, 8]},
            {"nums": [7, 11, 13, 14]},
            {"nums": [65535, 65534, 65533, 65531]},
            {"nums": [3, 5, 6, 9, 10, 12]},
            {"nums": _lcg_array(100, 1024, seed=84)},
            {"nums": _lcg_array(400, 65536, seed=840)},
        ],
    },
    {
        "slug": "85-minimum-bitmasks-to-cover-target",
        "title": "Minimum Bitmasks to Cover Target Mask",
        "difficulty": "Hard",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Apple"],
        "desc": (
            "Given a non-negative integer `target` (`0 <= target < 2^16`) and an array `masks` of "
            "non-negative integers, find the minimum number of elements from `masks` whose bitwise OR "
            "covers all set bits of `target` — that is, `(orSum & target) == target`. If `target == 0`, "
            "return `0` since no elements are needed. If it is impossible to cover `target`, return `-1`."
        ),
        "cons": [
            "0 <= target < 2^16",
            "1 <= masks.length <= 60",
            "0 <= masks[i] < 2^16",
        ],
        "hints": [
            "Compress the set bit positions of `target` into `b = popcount(target)` consecutive bit indices (`0..b - 1`) and project every element of `masks` onto those `b` bits, discarding zeros and duplicates.",
            "Run bitmask DP over `dp[s]` = minimum number of projected masks needed to form bitmask `s`, updating `dp[s | p] = min(dp[s | p], dp[s] + 1)` for each unique projected mask `p`.",
        ],
        "explanations": [
            "Picking 3 (011) and 4 (100) gives 3 | 4 = 7 (111) using 2 masks (1 and 6 also works).",
            "Bit 2 of target 7 (111) is not set in any element of [1, 2, 3], so return -1.",
            "Target 0 has no set bits to cover, so 0 masks are needed.",
        ],
        "time": "O(m * 2^popcount(target))",
        "space": "O(2^popcount(target))",
        "method": "minMasksToCover",
        "params": [("target", "int"), ("masks", "int[]")],
        "ret": "int",
        "py": """        if target == 0:
            return 0
        all_or = 0
        for x in masks:
            all_or |= x
        if (all_or & target) != target:
            return -1
        pos = [b for b in range(16) if (target >> b) & 1]
        b_cnt = len(pos)
        projs = set()
        for x in masks:
            p = 0
            for idx, bit in enumerate(pos):
                if (x >> bit) & 1:
                    p |= 1 << idx
            if p:
                projs.add(p)
        # Drop any projected mask dominated by another
        plist = sorted(projs, key=lambda v: v.bit_count(), reverse=True)
        filtered = []
        for p in plist:
            if not any((p & q) == p for q in filtered):
                filtered.append(p)
        full = (1 << b_cnt) - 1
        INF = 100
        dp = [INF] * (full + 1)
        dp[0] = 0
        for p in filtered:
            for s in range(full, -1, -1):
                cur = dp[s]
                if cur + 1 < dp[s | p]:
                    dp[s | p] = cur + 1
        return -1 if dp[full] >= INF else dp[full]""",
        "java": """        if (target == 0) return 0;
        int allOr = 0;
        for (int x : masks) allOr |= x;
        if ((allOr & target) != target) return -1;

        int[] pos = new int[16];
        int bCnt = 0;
        for (int b = 0; b < 16; b++) {
            if (((target >> b) & 1) != 0) pos[bCnt++] = b;
        }
        Set<Integer> projSet = new HashSet<>();
        for (int x : masks) {
            int p = 0;
            for (int i = 0; i < bCnt; i++) {
                if (((x >> pos[i]) & 1) != 0) p |= (1 << i);
            }
            if (p != 0) projSet.add(p);
        }
        List<Integer> plist = new ArrayList<>(projSet);
        plist.sort((a, b) -> Integer.compare(Integer.bitCount(b), Integer.bitCount(a)));
        List<Integer> filtered = new ArrayList<>();
        for (int p : plist) {
            boolean dominated = false;
            for (int q : filtered) {
                if ((p & q) == p) {
                    dominated = true;
                    break;
                }
            }
            if (!dominated) filtered.add(p);
        }
        int full = (1 << bCnt) - 1;
        int INF = 100;
        int[] dp = new int[full + 1];
        Arrays.fill(dp, INF);
        dp[0] = 0;
        for (int p : filtered) {
            for (int s = full; s >= 0; s--) {
                int cur = dp[s];
                if (cur + 1 < dp[s | p]) {
                    dp[s | p] = cur + 1;
                }
            }
        }
        return dp[full] >= INF ? -1 : dp[full];""",
        "visible": [
            {"target": 7, "masks": [1, 2, 4, 3, 6]},
            {"target": 7, "masks": [1, 2, 3]},
            {"target": 0, "masks": [5, 3]},
        ],
        "hidden": [
            {"target": 15, "masks": [15, 1, 2, 4, 8]},
            {"target": 15, "masks": [3, 6, 12, 9]},
            {"target": 31, "masks": [1, 2, 4, 8, 16]},
            {"target": 42, "masks": [10, 32, 8, 2, 34, 40]},
            {"target": 255, "masks": [15, 51, 85, 170, 240, 12]},
            {"target": 1023, "masks": [7, 56, 448, 512, 63, 960]},
            {"target": 4095, "masks": [31, 496, 3840, 255, 3855, 1020]},
            {"target": 16383, "masks": [(7 << i) & 16383 for i in range(0, 14, 2)] + [12288, 3072, 768, 192, 48, 12, 3]},
            {"target": 32767, "masks": [((1 << 4) - 1) << (i % 12) for i in range(20)] + [1 << i for i in range(15)]},
        ],
    },
    {
        "slug": "86-count-pairs-with-and-greater-than-xor",
        "title": "Count Pairs With Bitwise AND Greater Than XOR",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": (
            "Given an array `nums` of positive integers, return the number of index pairs `(i, j)` with "
            "`0 <= i < j < nums.length` such that `(nums[i] & nums[j]) > (nums[i] ^ nums[j])`."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "1 <= nums[i] <= 10^9",
        ],
        "hints": [
            "Compare `(a & b)` and `(a ^ b)` at the highest set bit of `max(a, b)`: if `a` and `b` share the same most significant `1` bit, that bit is `1` in `a & b` and `0` in `a ^ b`, guaranteeing `(a & b) > (a ^ b)`.",
            "Conversely, if their highest set bits differ, the highest bit is `0` in `a & b` and `1` in `a ^ b`, so `(a & b) < (a ^ b)`. Bucket elements by their highest set bit position `b` and sum `c * (c - 1) / 2`.",
        ],
        "explanations": [
            "Only 4 (100) and 7 (111) share the same highest set bit (bit 2), giving 4 & 7 = 4 > 4 ^ 7 = 3.",
            "All three 1s share highest set bit 0, forming 3 * 2 / 2 = 3 valid pairs.",
            "1, 2, 4, 8 have distinct highest set bits (0, 1, 2, 3), so 0 pairs satisfy the condition.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "countAndGreaterThanXor",
        "params": [("nums", "int[]")],
        "ret": "long",
        "py": """        buckets = [0] * 31
        for x in nums:
            buckets[x.bit_length() - 1] += 1
        ans = 0
        for c in buckets:
            ans += c * (c - 1) // 2
        return ans""",
        "java": """        long[] buckets = new long[31];
        for (int x : nums) {
            buckets[31 - Integer.numberOfLeadingZeros(x)]++;
        }
        long ans = 0L;
        for (long c : buckets) {
            ans += c * (c - 1L) / 2L;
        }
        return ans;""",
        "visible": [
            {"nums": [1, 4, 3, 7, 10]},
            {"nums": [1, 1, 1]},
            {"nums": [1, 2, 4, 8]},
        ],
        "hidden": [
            {"nums": [5]},
            {"nums": [2, 3]},
            {"nums": [4, 5, 6, 7]},
            {"nums": [1000000000, 536870912, 536870911]},
            {"nums": [8, 9, 10, 11, 12, 13, 14, 15]},
            {"nums": [3, 2, 1, 6, 5, 4, 12, 10, 8]},
            {"nums": [1000000000] * 100},
            {"nums": _lcg_array(500, 1_000_000_000, seed=86, offset=1)},
            {"nums": _lcg_array(3000, 1_000_000_000, seed=860, offset=1)},
        ],
    },
    # ------------------------------------------------------------------
    # Two Complement (87-93)
    # ------------------------------------------------------------------
    {
        "slug": "87-swap-odd-and-even-bits",
        "title": "Swap Odd and Even Bits",
        "difficulty": "Easy",
        "subtopic": "Two Complement",
        "companies": ["Apple", "Microsoft", "Amazon"],
        "desc": (
            "Given a 32-bit signed integer `n`, swap every pair of adjacent bits in its 32-bit two's "
            "complement binary representation: swap bit `0` with bit `1`, bit `2` with bit `3`, and so on "
            "up to bit `30` with bit `31`. Return the resulting 32-bit signed integer."
        ),
        "cons": [
            "-2^31 <= n <= 2^31 - 1",
        ],
        "hints": [
            "Mask all odd-indexed bits with `0xAAAAAAAA` and shift them right logically (unsigned) by `1`; mask all even-indexed bits with `0x55555555` and shift them left by `1`.",
            "Combine both shifted halves with bitwise OR, taking care to interpret the 32-bit result as a signed two's complement integer.",
        ],
        "explanations": [
            "23 is 010111 in binary; swapping adjacent pairs (01)(01)(11) produces (10)(10)(11) = 43.",
            "2 is 10 in binary; swapping bits 0 and 1 gives 01 = 1.",
            "-1 has all 32 bits set to 1, so swapping adjacent bits leaves it unchanged as -1.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "swapOddEvenBits",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        u = n & 0xFFFFFFFF
        res = (((u & 0xAAAAAAAA) >> 1) | ((u & 0x55555555) << 1)) & 0xFFFFFFFF
        return res - 0x100000000 if res >= 0x80000000 else res""",
        "java": """        return ((n & 0xAAAAAAAA) >>> 1) | ((n & 0x55555555) << 1);""",
        "visible": [
            {"n": 23},
            {"n": 2},
            {"n": -1},
        ],
        "hidden": [
            {"n": 0},
            {"n": 1},
            {"n": 10},
            {"n": 0x55555555},
            {"n": -1431655766},
            {"n": -2147483648},
            {"n": 1073741824},
            {"n": 2147483647},
            {"n": -2},
        ],
    },
    {
        "slug": "88-insert-bits-into-range",
        "title": "Insert Bits Into Bit Range",
        "difficulty": "Easy",
        "subtopic": "Two Complement",
        "companies": ["Apple", "Microsoft", "Oracle"],
        "desc": (
            "You are given two 32-bit signed integers `n` and `m`, and two bit positions `i` and `j` "
            "(`0 <= i <= j <= 31`, 0-indexed from the least significant bit). Clear bits `i` through `j` "
            "(inclusive) in the 32-bit two's complement representation of `n`, and replace them with the "
            "lowest `j - i + 1` bits of `m`. Return the resulting 32-bit signed integer."
        ),
        "cons": [
            "-2^31 <= n, m <= 2^31 - 1",
            "0 <= i <= j <= 31",
        ],
        "hints": [
            "Be careful with shift widths when `j - i + 1 == 32`, since shifting a 32-bit integer by `32` wraps modulo 32 in Java.",
            "Build the width mask in 64-bit arithmetic as `low = (1L << (j - i + 1)) - 1L`, clear `(low << i)` in `n`, and OR in `((m & low) << i)` before truncating to a signed 32-bit integer.",
        ],
        "explanations": [
            "Inserting 19 (10011) into bits 2..6 of 1024 (10000000000) yields 10001001100 = 1100.",
            "Clearing bits 0..3 of -1 (all 1s) and inserting 0 gives ...11110000 = -16.",
            "Replacing the entire 32-bit range 0..31 with -1 returns -1.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "insertBits",
        "params": [("n", "int"), ("m", "int"), ("i", "int"), ("j", "int")],
        "ret": "int",
        "py": """        low = (1 << (j - i + 1)) - 1
        field_mask = low << i
        res = (((n & 0xFFFFFFFF) & ~field_mask) | (((m & low) << i))) & 0xFFFFFFFF
        return res - 0x100000000 if res >= 0x80000000 else res""",
        "java": """        long low = (1L << (j - i + 1)) - 1L;
        long fieldMask = low << i;
        long res = ((n & 0xFFFFFFFFL) & ~fieldMask) | (((m & low) << i));
        return (int) res;""",
        "visible": [
            {"n": 1024, "m": 19, "i": 2, "j": 6},
            {"n": -1, "m": 0, "i": 0, "j": 3},
            {"n": 12345, "m": -1, "i": 0, "j": 31},
        ],
        "hidden": [
            {"n": 0, "m": 1, "i": 31, "j": 31},
            {"n": -2147483648, "m": 0, "i": 31, "j": 31},
            {"n": 2147483647, "m": 0, "i": 0, "j": 30},
            {"n": -1, "m": 5, "i": 4, "j": 7},
            {"n": 0x12345678, "m": 0xABCD, "i": 8, "j": 23},
            {"n": -123456789, "m": 42, "i": 10, "j": 15},
            {"n": 255, "m": 255, "i": 0, "j": 0},
            {"n": 0, "m": -1, "i": 16, "j": 31},
            {"n": -2147483648, "m": 2147483647, "i": 0, "j": 31},
        ],
    },
    {
        "slug": "89-signed-varint-byte-encoding",
        "title": "Signed Varint (ZigZag + LEB128) Encoding",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Meta", "Netflix"],
        "desc": (
            "Protocol Buffers encodes 32-bit signed integers compactly in two steps: first, **ZigZag "
            "encoding** maps signed 32-bit `n` to an unsigned 32-bit integer `u = ((n << 1) ^ (n >> 31))` "
            "(using arithmetic right shift, so `0 -> 0`, `-1 -> 1`, `1 -> 2`, `-2 -> 3`, ..., "
            "`-2^31 -> 2^32 - 1`); second, **Base-128 Varint (LEB128)** splits `u` into 7-bit groups from "
            "least significant to most significant, setting the continuation bit `0x80` (`128`) on every "
            "byte except the final byte. Given `n`, return the encoded byte sequence as an integer array "
            "with values in `[0, 255]`."
        ),
        "cons": [
            "-2^31 <= n <= 2^31 - 1",
        ],
        "hints": [
            "Compute the unsigned 32-bit ZigZag value `u = ((n << 1) ^ (n >> 31)) & 0xFFFFFFFF` (using `Integer.toUnsignedLong` in Java so shifts stay unsigned).",
            "While `u >= 128`, emit `(u & 0x7F) | 0x80` and shift `u >>= 7`; finally emit the remaining 7-bit chunk `u`.",
        ],
        "explanations": [
            "n = 0 ZigZag-encodes to u = 0, which fits in one 7-bit byte [0].",
            "n = -1 ZigZag-encodes to u = 1, producing [1].",
            "n = -100 ZigZag-encodes to u = 199 = 1 * 128 + 71; low 7 bits with continuation flag give 71 | 128 = 199, followed by 1.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "encodeSignedVarint",
        "params": [("n", "int")],
        "ret": "int[]",
        "py": """        u = ((n << 1) ^ (n >> 31)) & 0xFFFFFFFF
        out = []
        while u >= 0x80:
            out.append((u & 0x7F) | 0x80)
            u >>= 7
        out.append(u)
        return out""",
        "java": """        long u = Integer.toUnsignedLong((n << 1) ^ (n >> 31));
        int[] buf = new int[5];
        int len = 0;
        while (u >= 0x80L) {
            buf[len++] = (int) ((u & 0x7FL) | 0x80L);
            u >>>= 7;
        }
        buf[len++] = (int) u;
        return Arrays.copyOf(buf, len);""",
        "visible": [
            {"n": 0},
            {"n": -1},
            {"n": -100},
        ],
        "hidden": [
            {"n": 1},
            {"n": -2},
            {"n": 63},
            {"n": -64},
            {"n": 64},
            {"n": -65},
            {"n": 100000},
            {"n": 2147483647},
            {"n": -2147483648},
        ],
    },
    {
        "slug": "90-morton-code-bit-interleaving",
        "title": "2D Morton Code Bit Interleaving",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Apple", "Uber"],
        "desc": (
            "Given two 16-bit non-negative integers `x` and `y` (`0 <= x, y <= 65535`), compute their "
            "32-bit unsigned 2D Morton code (Z-order curve index) by interleaving their binary bits: bit "
            "`i` of `x` is placed at bit `2 * i`, and bit `i` of `y` is placed at bit `2 * i + 1` for "
            "`0 <= i < 16`. Return the resulting unsigned 32-bit value as a non-negative 64-bit integer."
        ),
        "cons": [
            "0 <= x, y <= 65535",
        ],
        "hints": [
            "Spread the 16 bits of a coordinate into even bit positions using four parallel divide-and-conquer shift-and-mask rounds with masks `0x00FF00FF`, `0x0F0F0F0F`, `0x33333333`, and `0x55555555`.",
            "Combine the spread coordinates via `spread(x) | (spread(y) << 1)` in 64-bit arithmetic so bit 31 never turns negative.",
        ],
        "explanations": [
            "x = 1 (01) places bits at even positions (0001) and y = 2 (10) places bits at odd positions (1000), giving 1001 = 9.",
            "x = 3 (11) and y = 3 (11) interleave to 1111 = 15.",
            "x = 5 (101) spreads to 10001 = 17, and y = 0 contributes 0.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "mortonEncode",
        "params": [("x", "int"), ("y", "int")],
        "ret": "long",
        "py": """        def spread(v: int) -> int:
            v = (v | (v << 8)) & 0x00FF00FF
            v = (v | (v << 4)) & 0x0F0F0F0F
            v = (v | (v << 2)) & 0x33333333
            v = (v | (v << 1)) & 0x55555555
            return v

        return spread(x) | (spread(y) << 1)""",
        "java": """        return spread(x) | (spread(y) << 1);
    }

    private long spread(long v) {
        v = (v | (v << 8)) & 0x00FF00FFL;
        v = (v | (v << 4)) & 0x0F0F0F0FL;
        v = (v | (v << 2)) & 0x33333333L;
        v = (v | (v << 1)) & 0x55555555L;
        return v;""",
        "visible": [
            {"x": 1, "y": 2},
            {"x": 3, "y": 3},
            {"x": 5, "y": 0},
        ],
        "hidden": [
            {"x": 0, "y": 0},
            {"x": 0, "y": 1},
            {"x": 1, "y": 0},
            {"x": 255, "y": 0},
            {"x": 0, "y": 255},
            {"x": 65535, "y": 0},
            {"x": 0, "y": 65535},
            {"x": 65535, "y": 65535},
            {"x": 43690, "y": 21845},
        ],
    },
    {
        "slug": "91-balanced-ternary-representation",
        "title": "Balanced Ternary Representation",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Bloomberg", "Microsoft"],
        "desc": (
            "Balanced ternary represents every signed integer uniquely in base `3` using the three signed "
            "digits `'-'` (`-1`), `'0'` (`0`), and `'+'` (`+1`), where digit `d_k` at position `k` from "
            "the right contributes `d_k * 3^k`. Given a 64-bit signed integer `n`, return its canonical "
            "balanced ternary string with no leading `'0'` characters (except `\"0\"` when `n == 0`)."
        ),
        "cons": [
            "-10^15 <= n <= 10^15",
        ],
        "hints": [
            "Extract the least significant digit using the non-negative remainder `r = ((n % 3) + 3) % 3`: `0 -> '0'`, `1 -> '+'` (subtract 1 before dividing by 3), and `2 -> '-'` (add 1 before dividing by 3).",
            "Repeat until `n == 0` and reverse the collected digits.",
        ],
        "explanations": [
            "5 = 9 - 3 - 1 = (+1)*3^2 + (-1)*3^1 + (-1)*3^0, written \"+--\".",
            "-2 = -3 + 1 = (-1)*3^1 + (+1)*3^0, written \"-+\".",
            "0 is represented as \"0\".",
        ],
        "time": "O(log |n|)",
        "space": "O(log |n|)",
        "method": "toBalancedTernary",
        "params": [("n", "long")],
        "ret": "String",
        "py": """        if n == 0:
            return "0"
        digits = []
        x = n
        while x != 0:
            r = x % 3
            if r == 0:
                digits.append("0")
                x //= 3
            elif r == 1:
                digits.append("+")
                x = (x - 1) // 3
            else:
                digits.append("-")
                x = (x + 1) // 3
        digits.reverse()
        return "".join(digits)""",
        "java": """        if (n == 0L) return "0";
        StringBuilder sb = new StringBuilder();
        long x = n;
        while (x != 0L) {
            long r = ((x % 3L) + 3L) % 3L;
            if (r == 0L) {
                sb.append('0');
                x /= 3L;
            } else if (r == 1L) {
                sb.append('+');
                x = (x - 1L) / 3L;
            } else {
                sb.append('-');
                x = (x + 1L) / 3L;
            }
        }
        return sb.reverse().toString();""",
        "visible": [
            {"n": 5},
            {"n": -2},
            {"n": 0},
        ],
        "hidden": [
            {"n": 1},
            {"n": -1},
            {"n": 2},
            {"n": -5},
            {"n": 27},
            {"n": -40},
            {"n": 123456789},
            {"n": -987654321012345},
            {"n": 1000000000000000},
        ],
    },
    {
        "slug": "92-minimum-splits-of-powers-of-two",
        "title": "Minimum Splits of Powers of Two to Form Target",
        "difficulty": "Hard",
        "subtopic": "Two Complement",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "You are given an array `nums` in which every element is a non-negative integer power of two "
            "(`2^k` for `0 <= k <= 30`), and a positive integer `target`. In one operation, you may choose "
            "an element `nums[i] > 1`, remove it from `nums`, and append two copies of `nums[i] / 2`. "
            "Return the minimum number of operations needed so that some subsequence of `nums` sums to "
            "`target`, or `-1` if it is impossible."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "1 <= nums[i] <= 2^30 and nums[i] is a power of two.",
            "1 <= target <= 2^31 - 1",
        ],
        "hints": [
            "A solution exists if and only if the total sum of `nums` is at least `target`. Count how many copies `cnt[b]` of each power `2^b` you hold.",
            "Process bits `b = 0..30` greedily: if bit `b` of `target` is `1` and `cnt[b] == 0`, borrow the smallest available `j > b` with `cnt[j] > 0` (costing `j - b` splits and populating one copy at each bit `b..j - 1`), then carry `cnt[b] // 2` pairs up to `cnt[b + 1]`.",
        ],
        "explanations": [
            "Split 8 into 4 + 4 (1 operation) so subsequence [1, 2, 4] sums to 7.",
            "Combine 1+1+2 = 4, and split 32 -> 16+16 -> 8+8 (2 operations) to reach 4 + 8 = 12.",
            "The total sum of [1, 32, 1] is 34 < 35, so target 35 is unreachable.",
        ],
        "time": "O(n + log target)",
        "space": "O(1)",
        "method": "minOperationsToFormTarget",
        "params": [("nums", "int[]"), ("target", "int")],
        "ret": "int",
        "py": """        if sum(nums) < target:
            return -1
        cnt = [0] * 32
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ops = 0
        for b in range(31):
            if (target >> b) & 1:
                if cnt[b] > 0:
                    cnt[b] -= 1
                else:
                    j = b + 1
                    while cnt[j] == 0:
                        j += 1
                    cnt[j] -= 1
                    for m in range(b, j):
                        cnt[m] += 1
                    ops += j - b
            cnt[b + 1] += cnt[b] // 2
        return ops""",
        "java": """        long total = 0L;
        int[] cnt = new int[32];
        for (int x : nums) {
            total += x;
            cnt[Integer.numberOfTrailingZeros(x)]++;
        }
        if (total < target) return -1;
        int ops = 0;
        for (int b = 0; b < 31; b++) {
            if (((target >> b) & 1) != 0) {
                if (cnt[b] > 0) {
                    cnt[b]--;
                } else {
                    int j = b + 1;
                    while (cnt[j] == 0) j++;
                    cnt[j]--;
                    for (int m = b; m < j; m++) {
                        cnt[m]++;
                    }
                    ops += j - b;
                }
            }
            cnt[b + 1] += cnt[b] / 2;
        }
        return ops;""",
        "visible": [
            {"nums": [1, 2, 8], "target": 7},
            {"nums": [1, 32, 1, 2], "target": 12},
            {"nums": [1, 32, 1], "target": 35},
        ],
        "hidden": [
            {"nums": [1], "target": 1},
            {"nums": [1073741824], "target": 1},
            {"nums": [1073741824, 1073741824], "target": 2147483647},
            {"nums": [1, 1, 1, 1, 1, 1, 1, 1], "target": 8},
            {"nums": [16, 16, 4], "target": 3},
            {"nums": [2, 2, 2, 2, 16], "target": 24},
            {"nums": [1, 128, 128, 128], "target": 127},
            {"nums": [1 << (i % 31) for i in range(500)], "target": 1234567890},
            {"nums": [1073741824] * 100 + [1] * 500, "target": 2147483647},
        ],
    },
    {
        "slug": "93-minimal-power-of-two-range-blocks",
        "title": "Minimal Aligned Power-of-Two Range Blocks",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Amazon", "LinkedIn"],
        "desc": (
            "An aligned power-of-two block (like a CIDR IP block or binary buddy-allocator block) is a "
            "contiguous integer interval `[a, a + 2^k - 1]` of length `2^k` (`k >= 0`) whose starting "
            "address `a` is divisible by `2^k`. Given a non-negative starting integer `start` and a "
            "positive integer length `n`, return the minimum number of disjoint aligned power-of-two "
            "blocks required to exactly cover the interval `[start, start + n - 1]`."
        ),
        "cons": [
            "0 <= start <= 10^15",
            "1 <= n <= 10^15",
        ],
        "hints": [
            "At the current position `start`, the largest aligned block starting at `start` has size limited by `lowbit(start) = start & -start` (using two's complement; unbounded when `start == 0`).",
            "The block size also cannot exceed the highest power of two `<= n`. Repeatedly advance `start += step` and `n -= step` with `step = min(lowbit(start), highestPow2(n))` until `n == 0`.",
        ],
        "explanations": [
            "Interval [0, 7] is itself a single aligned block of length 8.",
            "Interval [1, 6] splits into 4 aligned blocks: [1,1], [2,3], [4,5], and [6,6].",
            "Interval [4, 10] splits into 3 aligned blocks: [4,7], [8,9], and [10,10].",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "minAlignedBlocks",
        "params": [("start", "long"), ("n", "long")],
        "ret": "int",
        "py": """        blocks = 0
        cur = start
        rem = n
        while rem > 0:
            max_step = 1 << (rem.bit_length() - 1)
            if cur == 0:
                step = max_step
            else:
                low = cur & -cur
                step = low if low < max_step else max_step
            cur += step
            rem -= step
            blocks += 1
        return blocks""",
        "java": """        int blocks = 0;
        long cur = start;
        long rem = n;
        while (rem > 0L) {
            long maxStep = 1L << (63 - Long.numberOfLeadingZeros(rem));
            long step = (cur == 0L) ? maxStep : Math.min(cur & -cur, maxStep);
            cur += step;
            rem -= step;
            blocks++;
        }
        return blocks;""",
        "visible": [
            {"start": 0, "n": 8},
            {"start": 1, "n": 6},
            {"start": 4, "n": 7},
        ],
        "hidden": [
            {"start": 0, "n": 1},
            {"start": 1, "n": 1},
            {"start": 0, "n": 15},
            {"start": 1, "n": 14},
            {"start": 7, "n": 10},
            {"start": 1024, "n": 1024},
            {"start": 1, "n": (1 << 40) - 2},
            {"start": 123456789012345, "n": 987654321098765},
            {"start": 999999999999999, "n": 1000000000000000},
        ],
    },
    # ------------------------------------------------------------------
    # Fast Exponentiation (94-100)
    # ------------------------------------------------------------------
    {
        "slug": "94-last-digit-of-large-power",
        "title": "Last Digit of a Large Power",
        "difficulty": "Easy",
        "subtopic": "Fast Exponentiation",
        "companies": ["Amazon", "Microsoft", "Goldman Sachs"],
        "desc": (
            "Given two non-negative 64-bit integers `base` and `exp`, compute and return the last decimal "
            "digit (the ones digit) of `base^exp`. Follow the standard mathematical convention `0^0 = 1`."
        ),
        "cons": [
            "0 <= base <= 10^15",
            "0 <= exp <= 10^15",
        ],
        "hints": [
            "Only `base % 10` affects the last decimal digit of any power.",
            "Compute `(base % 10)^exp % 10` using binary exponentiation in O(log exp) time, which naturally returns `1` when `exp == 0`.",
        ],
        "explanations": [
            "3^10 = 59049, whose last digit is 9.",
            "7^4 = 2401 ends in 1, so 7^100 = (7^4)^25 also ends in 1.",
            "By convention 0^0 = 1, so the last digit is 1.",
        ],
        "time": "O(log exp)",
        "space": "O(1)",
        "method": "lastDigitOfPower",
        "params": [("base", "long"), ("exp", "long")],
        "ret": "int",
        "py": """        res = 1
        b = base % 10
        e = exp
        while e > 0:
            if e & 1:
                res = (res * b) % 10
            b = (b * b) % 10
            e >>= 1
        return res""",
        "java": """        int res = 1;
        int b = (int) (base % 10L);
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) {
                res = (res * b) % 10;
            }
            b = (b * b) % 10;
            e >>= 1;
        }
        return res;""",
        "visible": [
            {"base": 3, "exp": 10},
            {"base": 7, "exp": 100},
            {"base": 0, "exp": 0},
        ],
        "hidden": [
            {"base": 0, "exp": 1},
            {"base": 0, "exp": 1000000000000000},
            {"base": 123456789012345, "exp": 0},
            {"base": 2, "exp": 1000000000000000},
            {"base": 9, "exp": 999999999999999},
            {"base": 9, "exp": 999999999999998},
            {"base": 14, "exp": 27},
            {"base": 987654321012348, "exp": 765432109876543},
            {"base": 1000000000000000, "exp": 1000000000000000},
        ],
    },
    {
        "slug": "95-domino-tromino-tiling-large-n",
        "title": "Domino and Tromino Tilings for Large N",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "You have two types of tiles: a `2 x 1` domino shape and an L-shaped tromino (3 cells) that "
            "may be rotated in any orientation. Given a positive 64-bit integer `n`, return the number of "
            "distinct ways to completely tile a `2 x n` board with these tiles, modulo `10^9 + 7`."
        ),
        "cons": [
            "1 <= n <= 10^15",
        ],
        "hints": [
            "The number of tilings satisfies the 3rd-order linear recurrence `f(n) = 2 * f(n - 1) + f(n - 3)` with base values `f(0) = 1`, `f(1) = 1`, and `f(2) = 2`.",
            "Express the recurrence as a `3 x 3` transition matrix `[[2, 0, 1], [1, 0, 0], [0, 1, 0]]` and raise it to the power `n - 2` modulo `10^9 + 7` via binary matrix exponentiation.",
        ],
        "explanations": [
            "For a 2 x 3 board, there are 5 valid domino/tromino tilings.",
            "For a 2 x 1 board, only a single vertical domino fits (1 way).",
            "For a 2 x 4 board, f(4) = 2 * f(3) + f(1) = 2 * 5 + 1 = 11.",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "numTilingsLargeN",
        "params": [("n", "long")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007
        if n == 1:
            return 1
        if n == 2:
            return 2

        def mul(A, B):
            C = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]
            for i in range(3):
                for k in range(3):
                    v = A[i][k]
                    if v:
                        for j in range(3):
                            C[i][j] = (C[i][j] + v * B[k][j]) % MOD
            return C

        res = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        base = [[2, 0, 1], [1, 0, 0], [0, 1, 0]]
        exp = n - 2
        while exp > 0:
            if exp & 1:
                res = mul(res, base)
            base = mul(base, base)
            exp >>= 1
        return (res[0][0] * 2 + res[0][1] + res[0][2]) % MOD""",
        "java": """        final long MOD = 1_000_000_007L;
        if (n == 1L) return 1;
        if (n == 2L) return 2;
        long[][] res = {
            {1, 0, 0},
            {0, 1, 0},
            {0, 0, 1}
        };
        long[][] base = {
            {2, 0, 1},
            {1, 0, 0},
            {0, 1, 0}
        };
        long exp = n - 2L;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) res = mul(res, base, MOD);
            base = mul(base, base, MOD);
            exp >>= 1;
        }
        long ans = (res[0][0] * 2L + res[0][1] + res[0][2]) % MOD;
        return (int) ans;
    }

    private long[][] mul(long[][] a, long[][] b, long mod) {
        long[][] c = new long[3][3];
        for (int i = 0; i < 3; i++) {
            for (int k = 0; k < 3; k++) {
                long v = a[i][k];
                if (v == 0L) continue;
                for (int j = 0; j < 3; j++) {
                    c[i][j] = (c[i][j] + v * b[k][j]) % mod;
                }
            }
        }
        return c;""",
        "visible": [
            {"n": 3},
            {"n": 1},
            {"n": 4},
        ],
        "hidden": [
            {"n": 2},
            {"n": 5},
            {"n": 10},
            {"n": 30},
            {"n": 100},
            {"n": 1000},
            {"n": 1000000000},
            {"n": 999999999999999},
            {"n": 1000000000000000},
        ],
    },
    {
        "slug": "96-binomial-coefficient-lucas-modulo",
        "title": "Binomial Coefficient Modulo Small Prime",
        "difficulty": "Hard",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Goldman Sachs", "Meta"],
        "desc": (
            "Given non-negative 64-bit integers `n` and `k` (`0 <= k <= n <= 10^15`) and a prime integer "
            "`p` (`2 <= p <= 10^5`), compute the binomial coefficient `C(n, k) % p`, where `C(n, k) = "
            "n! / (k! * (n - k)!)`. Because `n` can greatly exceed `p`, ordinary factorial tables up to "
            "`n` are infeasible and `n!` may be divisible by `p`."
        ),
        "cons": [
            "0 <= k <= n <= 10^15",
            "2 <= p <= 10^5",
            "p is guaranteed to be a prime number.",
        ],
        "hints": [
            "By Lucas's Theorem, `C(n, k) == C(n % p, k % p) * C(n // p, k // p) (mod p)`, where `C(a, b) = 0` whenever `b > a`.",
            "Precompute factorials `fact[0..p - 1]` and inverse factorials `invFact[0..p - 1]` modulo `p` using Fermat's Little Theorem (`fact[p - 1]^(p - 2) mod p`) via fast exponentiation.",
        ],
        "explanations": [
            "C(5, 2) = 10, and 10 % 7 = 3.",
            "C(10, 3) = 120, which is divisible by 3, so the result is 0.",
            "In base 2, 7 is 111 and 3 is 011; every base-2 digit satisfies k_i <= n_i, so C(7, 3) = 35 == 1 (mod 2).",
        ],
        "time": "O(p + log_p n)",
        "space": "O(p)",
        "method": "binomialModPrime",
        "params": [("n", "long"), ("k", "long"), ("p", "int")],
        "ret": "int",
        "py": """        fact = [1] * p
        for i in range(1, p):
            fact[i] = (fact[i - 1] * i) % p
        inv_fact = [1] * p
        inv_fact[p - 1] = pow(fact[p - 1], p - 2, p)
        for i in range(p - 2, 0, -1):
            inv_fact[i] = (inv_fact[i + 1] * (i + 1)) % p

        ans = 1
        nn, kk = n, k
        while nn > 0 or kk > 0:
            ni = nn % p
            ki = kk % p
            if ki > ni:
                return 0
            ans = (ans * fact[ni] % p * inv_fact[ki] % p * inv_fact[ni - ki]) % p
            nn //= p
            kk //= p
        return ans""",
        "java": """        long[] fact = new long[p];
        fact[0] = 1L;
        for (int i = 1; i < p; i++) {
            fact[i] = (fact[i - 1] * i) % p;
        }
        long[] invFact = new long[p];
        invFact[p - 1] = modPow(fact[p - 1], p - 2, p);
        for (int i = p - 2; i >= 0; i--) {
            invFact[i] = (invFact[i + 1] * (i + 1)) % p;
        }
        long ans = 1L;
        long nn = n, kk = k;
        while (nn > 0L || kk > 0L) {
            int ni = (int) (nn % p);
            int ki = (int) (kk % p);
            if (ki > ni) return 0;
            ans = ans * fact[ni] % p * invFact[ki] % p * invFact[ni - ki] % p;
            nn /= p;
            kk /= p;
        }
        return (int) ans;
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1L;
        long b = base % mod;
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) res = (res * b) % mod;
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;""",
        "visible": [
            {"n": 5, "k": 2, "p": 7},
            {"n": 10, "k": 3, "p": 3},
            {"n": 7, "k": 3, "p": 2},
        ],
        "hidden": [
            {"n": 0, "k": 0, "p": 2},
            {"n": 1000000000000000, "k": 0, "p": 99991},
            {"n": 1000000000000000, "k": 1000000000000000, "p": 99991},
            {"n": 1000, "k": 500, "p": 13},
            {"n": 1000000, "k": 123456, "p": 1009},
            {"n": 999999999999999, "k": 333333333333333, "p": 97},
            {"n": 123456789012345, "k": 67890123456789, "p": 10007},
            {"n": 987654321098765, "k": 123456789012345, "p": 99991},
            {"n": 1000000000000000, "k": 500000000000000, "p": 99991},
        ],
    },
    {
        "slug": "97-modular-power-tower-three",
        "title": "Modular Power Tower a^(b^c) mod P",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Microsoft", "Bloomberg"],
        "desc": (
            "Given non-negative 64-bit integers `a`, `b`, `c` and a prime modulus `p`, compute the power "
            "tower `a^(b^c) % p` (evaluated right-associatively as `a` raised to the power `(b^c)`). "
            "Follow the convention `0^0 = 1`."
        ),
        "cons": [
            "0 <= a, b, c <= 10^15",
            "2 <= p <= 10^9 + 7",
            "p is guaranteed to be a prime number.",
        ],
        "hints": [
            "Handle the zero-exponent case `b^c == 0` first (which happens if and only if `b == 0` and `c > 0`, yielding `a^0 % p = 1`); otherwise `b^c >= 1`, so if `a % p == 0`, the answer is `0`.",
            "When `a % p != 0`, Fermat's Little Theorem gives `a^(p - 1) == 1 (mod p)`, so reduce the exponent `e = b^c mod (p - 1)` with binary exponentiation and then return `a^e mod p`.",
        ],
        "explanations": [
            "2^(3^2) = 2^9 = 512, and 512 % 1000000007 = 512.",
            "Since 0^5 = 0, the expression is 7^0 % 13 = 1.",
            "Since 3^4 = 81 and 81 % (7 - 1) = 3, 2^81 == 2^3 = 8 == 1 (mod 7).",
        ],
        "time": "O(log c + log p)",
        "space": "O(1)",
        "method": "modPowerTower",
        "params": [("a", "long"), ("b", "long"), ("c", "long"), ("p", "long")],
        "ret": "long",
        "py": """        if b == 0 and c > 0:
            return 1
        a_mod = a % p
        if a_mod == 0:
            return 0
        if p == 2:
            return 1
        e = pow(b % (p - 1), c, p - 1)
        return pow(a_mod, e, p)""",
        "java": """        if (b == 0L && c > 0L) return 1L;
        long aMod = a % p;
        if (aMod == 0L) return 0L;
        if (p == 2L) return 1L;
        long e = modPow(b % (p - 1L), c, p - 1L);
        return modPow(aMod, e, p);
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1L % mod;
        long b = base % mod;
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) res = (res * b) % mod;
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;""",
        "visible": [
            {"a": 2, "b": 3, "c": 2, "p": 1000000007},
            {"a": 7, "b": 0, "c": 5, "p": 13},
            {"a": 2, "b": 3, "c": 4, "p": 7},
        ],
        "hidden": [
            {"a": 0, "b": 0, "c": 0, "p": 7},
            {"a": 0, "b": 0, "c": 5, "p": 7},
            {"a": 0, "b": 5, "c": 0, "p": 7},
            {"a": 14, "b": 3, "c": 2, "p": 7},
            {"a": 15, "b": 100, "c": 200, "p": 2},
            {"a": 1000000007, "b": 0, "c": 1, "p": 1000000007},
            {"a": 3, "b": 1000000006, "c": 0, "p": 1000000007},
            {"a": 123456789, "b": 987654321, "c": 1000000000000, "p": 1000000007},
            {"a": 999999999999999, "b": 888888888888888, "c": 777777777777777, "p": 998244353},
        ],
    },
    {
        "slug": "98-count-walks-of-length-k",
        "title": "Count Directed Walks of Exact Length K",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Meta", "Uber"],
        "desc": (
            "You are given a directed graph with `n` vertices labeled `0` to `n - 1` and a list of "
            "directed edges `edges` where each entry `[u, v]` represents a directed edge from `u` to `v` "
            "(self-loops and parallel edges are allowed and count as distinct edges). Given source `src`, "
            "destination `dst`, and a non-negative 64-bit integer `k`, return the number of distinct "
            "directed walks of exact length `k` from `src` to `dst`, modulo `10^9 + 7`."
        ),
        "cons": [
            "1 <= n <= 20",
            "0 <= edges.length <= 400",
            "0 <= u, v, src, dst < n",
            "0 <= k <= 10^15",
        ],
        "hints": [
            "Construct the `n x n` adjacency matrix `A` where `A[u][v]` counts the number of directed edges from `u` to `v`.",
            "The entry `(A^k)[src][dst]` equals the exact number of walks of length `k` from `src` to `dst`; compute `A^k mod (10^9 + 7)` using binary matrix exponentiation in O(n^3 log k) time.",
        ],
        "explanations": [
            "The only walk of length 2 from 0 to 2 is 0 -> 1 -> 2, giving 1.",
            "The 3 walks of length 3 from 0 to 0 are 0-0-0-0, 0-0-1-0, and 0-1-0-0.",
            "A walk of length 0 starts and ends at the same vertex, so src == dst gives 1.",
        ],
        "time": "O(n^3 log k)",
        "space": "O(n^2)",
        "method": "countWalks",
        "params": [("n", "int"), ("edges", "int[][]"), ("src", "int"), ("dst", "int"), ("k", "long")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007
        base = [[0] * n for _ in range(n)]
        for u, v in edges:
            base[u][v] += 1
        res = [[1 if i == j else 0 for j in range(n)] for i in range(n)]

        def mul(A, B):
            C = [[0] * n for _ in range(n)]
            for i in range(n):
                ai = A[i]
                ci = C[i]
                for mid in range(n):
                    v = ai[mid]
                    if v:
                        bm = B[mid]
                        for j in range(n):
                            ci[j] = (ci[j] + v * bm[j]) % MOD
            return C

        exp = k
        while exp > 0:
            if exp & 1:
                res = mul(res, base)
            base = mul(base, base)
            exp >>= 1
        return res[src][dst]""",
        "java": """        final long MOD = 1_000_000_007L;
        long[][] base = new long[n][n];
        for (int[] e : edges) {
            base[e[0]][e[1]]++;
        }
        long[][] res = new long[n][n];
        for (int i = 0; i < n; i++) res[i][i] = 1L;

        long exp = k;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) res = mul(res, base, n, MOD);
            base = mul(base, base, n, MOD);
            exp >>= 1;
        }
        return (int) res[src][dst];
    }

    private long[][] mul(long[][] a, long[][] b, int n, long mod) {
        long[][] c = new long[n][n];
        for (int i = 0; i < n; i++) {
            for (int mid = 0; mid < n; mid++) {
                long v = a[i][mid];
                if (v == 0L) continue;
                for (int j = 0; j < n; j++) {
                    c[i][j] = (c[i][j] + v * b[mid][j]) % mod;
                }
            }
        }
        return c;""",
        "visible": [
            {"n": 3, "edges": [[0, 1], [1, 2], [2, 0], [0, 2]], "src": 0, "dst": 2, "k": 2},
            {"n": 2, "edges": [[0, 1], [1, 0], [0, 0]], "src": 0, "dst": 0, "k": 3},
            {"n": 3, "edges": [[0, 1]], "src": 1, "dst": 1, "k": 0},
        ],
        "hidden": [
            {"n": 3, "edges": [[0, 1]], "src": 0, "dst": 2, "k": 0},
            {"n": 1, "edges": [[0, 0], [0, 0]], "src": 0, "dst": 0, "k": 10},
            {"n": 2, "edges": [], "src": 0, "dst": 1, "k": 5},
            {"n": 4, "edges": [[0, 1], [1, 2], [2, 3], [3, 0]], "src": 0, "dst": 2, "k": 1000000002},
            {"n": 4, "edges": [[0, 1], [1, 2], [2, 3], [3, 0]], "src": 0, "dst": 2, "k": 1000000003},
            {"n": 3, "edges": [[0, 1], [0, 1], [1, 2], [2, 0]], "src": 0, "dst": 0, "k": 9},
            {"n": 5, "edges": [[i, (i + 1) % 5] for i in range(5)] + [[i, (i + 2) % 5] for i in range(5)], "src": 0, "dst": 3, "k": 1000000000000},
            {"n": 10, "edges": [[i, (i + 1) % 10] for i in range(10)] + [[i, (i + 3) % 10] for i in range(10)], "src": 2, "dst": 7, "k": 987654321012345},
            {"n": 20, "edges": [[i, (i + 1) % 20] for i in range(20)] + [[i, (i + 5) % 20] for i in range(20)] + [[i, (i + 7) % 20] for i in range(20)], "src": 0, "dst": 19, "k": 1000000000000000},
        ],
    },
    {
        "slug": "99-primality-test-large-integer",
        "title": "Deterministic Primality Test for Large Integers",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Amazon", "Goldman Sachs"],
        "desc": (
            "Given a non-negative 64-bit integer `n` (`0 <= n <= 10^15`), determine whether `n` is a prime "
            "number. Because `n` can be as large as `10^15`, trial division up to `sqrt(n)` is too slow; "
            "return `true` if `n` is prime and `false` otherwise."
        ),
        "cons": [
            "0 <= n <= 10^15",
        ],
        "hints": [
            "Use the deterministic Miller-Rabin primality test: factor `n - 1 = d * 2^s` with `d` odd and test the fixed witness bases `[2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37]`, which is provably exact for all 64-bit integers.",
            "In 64-bit languages like Java, `a * b` can exceed `2^63 - 1` when `mod` is up to `10^15`; use Russian peasant binary modular multiplication `mulMod(a, b, mod)` inside your binary modular exponentiation.",
        ],
        "explanations": [
            "17 has no divisors other than 1 and 17, so it is prime.",
            "561 = 3 * 11 * 17 is the smallest Carmichael number (composite despite passing Fermat tests for coprime bases).",
            "1000000007 is prime.",
        ],
        "time": "O(k * log^2 n)",
        "space": "O(1)",
        "method": "isPrimeLarge",
        "params": [("n", "long")],
        "ret": "boolean",
        "py": """        if n < 2:
            return False
        small = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
        for p in small:
            if n == p:
                return True
            if n % p == 0:
                return False
        d = n - 1
        s = 0
        while (d & 1) == 0:
            d >>= 1
            s += 1
        for a in small:
            x = pow(a, d, n)
            if x == 1 or x == n - 1:
                continue
            for _ in range(s - 1):
                x = (x * x) % n
                if x == n - 1:
                    break
            else:
                return False
        return True""",
        "java": """        if (n < 2L) return false;
        long[] small = {2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37};
        for (long p : small) {
            if (n == p) return true;
            if (n % p == 0L) return false;
        }
        long d = n - 1L;
        int s = 0;
        while ((d & 1L) == 0L) {
            d >>= 1;
            s++;
        }
        for (long a : small) {
            long x = powMod(a % n, d, n);
            if (x == 1L || x == n - 1L) continue;
            boolean witness = true;
            for (int r = 1; r < s; r++) {
                x = mulMod(x, x, n);
                if (x == n - 1L) {
                    witness = false;
                    break;
                }
            }
            if (witness) return false;
        }
        return true;
    }

    private long mulMod(long a, long b, long mod) {
        long res = 0L;
        long x = a % mod;
        long y = b % mod;
        while (y > 0L) {
            if ((y & 1L) != 0L) {
                res += x;
                if (res >= mod) res -= mod;
            }
            x += x;
            if (x >= mod) x -= mod;
            y >>= 1;
        }
        return res;
    }

    private long powMod(long base, long exp, long mod) {
        long res = 1L;
        long b = base % mod;
        long e = exp;
        while (e > 0L) {
            if ((e & 1L) != 0L) res = mulMod(res, b, mod);
            b = mulMod(b, b, mod);
            e >>= 1;
        }
        return res;""",
        "visible": [
            {"n": 17},
            {"n": 561},
            {"n": 1000000007},
        ],
        "hidden": [
            {"n": 0},
            {"n": 1},
            {"n": 2},
            {"n": 9},
            {"n": 341550071728321},
            {"n": 999999937},
            {"n": 999999999999989},
            {"n": 999999999999997},
            {"n": 1000000000000000},
        ],
    },
    {
        "slug": "100-maximize-ball-passing-score-k-steps",
        "title": "Maximize Value of Function in K-Step Passing Game",
        "difficulty": "Hard",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Meta", "Amazon"],
        "desc": (
            "You are given a 0-indexed integer array `receiver` of length `n` (`0 <= receiver[i] < n`) and "
            "a positive 64-bit integer `k`. Starting with any player `x` (`0 <= x < n`), the ball is passed "
            "exactly `k` times: in each pass, the current holder `cur` passes the ball to `receiver[cur]`. "
            "The score `f(x)` is the sum of the IDs of all `k + 1` players who hold the ball (including `x` "
            "and counting repeated visits). Return the maximum possible value of `f(x)` over all starting "
            "players `0 <= x < n`."
        ),
        "cons": [
            "1 <= receiver.length <= 10^4",
            "0 <= receiver[i] < receiver.length",
            "1 <= k <= 10^10",
        ],
        "hints": [
            "Model the `k`-step functional transition as binary lifting (exponentiation by squaring on the function `cur -> receiver[cur]`): track `up[i]` (node reached in `2^b` steps) and `w[i]` (sum of visited receiver IDs along those `2^b` steps).",
            "Maintain `pos[i]` and `score[i]` initialized to `i` for each starting player; iterate over the binary bits of `k`, applying `(up, w)` whenever bit `b` of `k` is `1` and squaring `up` and `w` in O(n) space.",
        ],
        "explanations": [
            "Starting from player 2 yields sequence 2 -> 1 -> 0 -> 2 -> 1 with sum 2 + 1 + 0 + 2 + 1 = 6.",
            "Starting from player 4 yields sequence 4 -> 3 -> 2 -> 1 with sum 4 + 3 + 2 + 1 = 10.",
            "Player 0 passes to itself 10^10 times, giving sum 0.",
        ],
        "time": "O(n log k)",
        "space": "O(n)",
        "method": "maxBallPassingScore",
        "params": [("receiver", "int[]"), ("k", "long")],
        "ret": "long",
        "py": """        n = len(receiver)
        up = list(receiver)
        w = list(receiver)
        pos = list(range(n))
        score = list(range(n))
        rem = k
        while rem > 0:
            if rem & 1:
                for i in range(n):
                    p = pos[i]
                    score[i] += w[p]
                    pos[i] = up[p]
            rem >>= 1
            if rem > 0:
                new_up = [0] * n
                new_w = [0] * n
                for i in range(n):
                    mid = up[i]
                    new_up[i] = up[mid]
                    new_w[i] = w[i] + w[mid]
                up = new_up
                w = new_w
        return max(score)""",
        "java": """        int n = receiver.length;
        int[] up = receiver.clone();
        long[] w = new long[n];
        int[] pos = new int[n];
        long[] score = new long[n];
        for (int i = 0; i < n; i++) {
            w[i] = receiver[i];
            pos[i] = i;
            score[i] = i;
        }
        long rem = k;
        while (rem > 0L) {
            if ((rem & 1L) != 0L) {
                for (int i = 0; i < n; i++) {
                    int p = pos[i];
                    score[i] += w[p];
                    pos[i] = up[p];
                }
            }
            rem >>= 1;
            if (rem > 0L) {
                int[] newUp = new int[n];
                long[] newW = new long[n];
                for (int i = 0; i < n; i++) {
                    int mid = up[i];
                    newUp[i] = up[mid];
                    newW[i] = w[i] + w[mid];
                }
                up = newUp;
                w = newW;
            }
        }
        long best = score[0];
        for (int i = 1; i < n; i++) {
            if (score[i] > best) best = score[i];
        }
        return best;""",
        "visible": [
            {"receiver": [2, 0, 1], "k": 4},
            {"receiver": [1, 1, 1, 2, 3], "k": 3},
            {"receiver": [0], "k": 10000000000},
        ],
        "hidden": [
            {"receiver": [1, 0], "k": 1},
            {"receiver": [1, 0], "k": 2},
            {"receiver": [0, 1, 2, 3], "k": 10000000000},
            {"receiver": [1, 2, 3, 4, 0], "k": 7},
            {"receiver": [2, 2, 3, 4, 2], "k": 100},
            {"receiver": [0, 0, 1, 2, 3, 4], "k": 5},
            {"receiver": [(i * 7 + 3) % 50 for i in range(50)], "k": 1000000},
            {"receiver": [(i * 31 + 17) % 500 for i in range(500)], "k": 9876543210},
            {"receiver": [(i * 97 + 13) % 2000 for i in range(2000)], "k": 10000000000},
        ],
    },
]


def main() -> None:
    expected_prefixes = list(range(71, 101))
    assert len(TASKS) == 30, f"Expected 30 tasks, got {len(TASKS)}"

    existing_slugs: set[str] = set()
    existing_titles: set[str] = set()
    for p in (ROOT / "problems").rglob("problem.json"):
        m = re.match(r"^(\d{2,3})-(.+)$", p.parent.name)
        if m:
            existing_slugs.add(m.group(2))
        meta = json.loads(p.read_text(encoding="utf-8"))
        existing_titles.add(meta["title"].lower())

    seen_new_slugs: set[str] = set()
    seen_new_titles: set[str] = set()

    for idx, p in enumerate(TASKS):
        prefix_str, slug_only = p["slug"].split("-", 1)
        assert int(prefix_str) == expected_prefixes[idx], (
            f"Expected prefix {expected_prefixes[idx]}, got {prefix_str}"
        )
        assert p["subtopic"] in ALLOWED_SUBTOPICS, f"Invalid subtopic: {p['subtopic']}"
        assert len(p["desc"].strip()) >= 60, f"Description too short for {p['slug']}"
        assert len(p["hints"]) == 2, f"Expected 2 hints for {p['slug']}"
        assert len(p["visible"]) == 3, f"Expected 3 visible tests for {p['slug']}"
        assert len(p["hidden"]) == 9, f"Expected 9 hidden tests for {p['slug']}"
        assert len(p["explanations"]) == 3, f"Expected 3 explanations for {p['slug']}"
        for c in p["companies"]:
            assert c in ALLOWED_COMPANIES, f"Invalid company {c} in {p['slug']}"

        all_test_keys = [json.dumps(t, sort_keys=True) for t in p["visible"] + p["hidden"]]
        assert len(all_test_keys) == len(set(all_test_keys)), f"Duplicate test inputs in {p['slug']}"

        assert slug_only not in seen_new_slugs, f"Internal duplicate slug: {slug_only}"
        assert p["title"].lower() not in seen_new_titles, f"Internal duplicate title: {p['title']}"
        seen_new_slugs.add(slug_only)
        seen_new_titles.add(p["title"].lower())

        folder = BASE / p["slug"]
        if not folder.exists():
            assert slug_only not in existing_slugs, f"Global duplicate slug: {slug_only}"
            assert p["title"].lower() not in existing_titles, f"Global duplicate title: {p['title']}"
            existing_slugs.add(slug_only)
            existing_titles.add(p["title"].lower())

        folder.mkdir(parents=True, exist_ok=True)

        params = [{"name": n, "type": t} for n, t in p["params"]]
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
            "signature": {
                "kind": "function",
                "method": p["method"],
                "params": params,
                "returns": p["ret"],
            },
        }
        (folder / "problem.json").write_text(json.dumps(meta, indent=2) + "\n", encoding="utf-8")

        pyparams = "".join(f", {n}: {py_type(t)}" for n, t in p["params"])
        (folder / "solution.py").write_text(
            f"class Solution:\n    def {p['method']}(self{pyparams}) -> {py_type(p['ret'])}:\n"
            + p["py"]
            + "\n",
            encoding="utf-8",
        )

        jparams = ", ".join(f"{t} {n}" for n, t in p["params"])
        (folder / "Solution.java").write_text(
            f"class Solution {{\n    public {p['ret']} {p['method']}({jparams}) {{\n"
            + p["java"]
            + "\n    }\n}\n",
            encoding="utf-8",
        )

        vis_code = repr([{"in": x} for x in p["visible"]])
        hid_code = repr([{"in": x} for x in p["hidden"]])
        (folder / "tests.py").write_text(
            f"def visible():\n    return {vis_code}\n\ndef hidden():\n    return {hid_code}\n",
            encoding="utf-8",
        )

    print(f"Generated {len(TASKS)} bit-manipulation problems (71-100)")


if __name__ == "__main__":
    main()
