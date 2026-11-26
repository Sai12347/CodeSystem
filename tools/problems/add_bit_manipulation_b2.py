#!/usr/bin/env python3
"""Generate bit-manipulation problems 41-70 for AlgoPlay (Batch 2)."""
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


TASKS = [
    # ------------------------------------------------------------------
    # XOR Tricks (41-48)
    # ------------------------------------------------------------------
    {
        "slug": "41-xor-operation-in-arithmetic-array",
        "title": "XOR Operation in an Arithmetic Array",
        "difficulty": "Easy",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": (
            "Given two integers `n` and `start`, consider the array `nums` of length `n` defined by "
            "`nums[i] = start + 2 * i` for `0 <= i < n`. Return the bitwise XOR of all elements of `nums`. "
            "Because `n` can be as large as `10^9`, compute the result without iterating through all `n` elements."
        ),
        "cons": [
            "1 <= n <= 10^9",
            "0 <= start <= 10^9",
        ],
        "hints": [
            "Every term `start + 2 * i` shares the exact same least significant bit (`start & 1`), while dividing by 2 shifts the sequence into consecutive integers `(start >> 1) + i`.",
            "The prefix XOR `0 ^ 1 ^ ... ^ x` repeats with period 4 (`x`, `1`, `x + 1`, `0` for `x % 4 == 0, 1, 2, 3`), letting you compute any consecutive range XOR in O(1) time.",
        ],
        "explanations": [
            "The array is [0, 2, 4, 6, 8], and 0 ^ 2 ^ 4 ^ 6 ^ 8 = 8.",
            "The array is [3, 5, 7, 9], and 3 ^ 5 ^ 7 ^ 9 = 8.",
            "The single-element array [7] has XOR 7.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "xorArithmeticArray",
        "params": [("n", "long"), ("start", "long")],
        "ret": "long",
        "py": """        def xor_to(x: int) -> int:
            if x < 0:
                return 0
            r = x & 3
            if r == 0:
                return x
            if r == 1:
                return 1
            if r == 2:
                return x + 1
            return 0

        s = start >> 1
        high = xor_to(s + n - 1) ^ xor_to(s - 1)
        low = (start & 1) & (n & 1)
        return (high << 1) | low""",
        "java": """        long s = start >> 1;
        long high = xorTo(s + n - 1) ^ xorTo(s - 1);
        long low = (start & 1L) & (n & 1L);
        return (high << 1) | low;
    }

    private long xorTo(long x) {
        if (x < 0) return 0L;
        long r = x & 3L;
        if (r == 0L) return x;
        if (r == 1L) return 1L;
        if (r == 2L) return x + 1L;
        return 0L;""",
        "visible": [
            {"n": 5, "start": 0},
            {"n": 4, "start": 3},
            {"n": 1, "start": 7},
        ],
        "hidden": [
            {"n": 1, "start": 0},
            {"n": 2, "start": 1},
            {"n": 3, "start": 1},
            {"n": 10, "start": 5},
            {"n": 16, "start": 0},
            {"n": 17, "start": 2},
            {"n": 100000, "start": 99999},
            {"n": 999999999, "start": 123456789},
            {"n": 1000000000, "start": 1000000000},
        ],
    },
    {
        "slug": "42-decode-xored-array",
        "title": "Decode XORed Array",
        "difficulty": "Easy",
        "subtopic": "XOR Tricks",
        "companies": ["Amazon", "Microsoft", "Apple"],
        "desc": (
            "There is a hidden integer array `arr` consisting of `n` non-negative integers. It was encoded "
            "into another integer array `encoded` of length `n - 1` such that `encoded[i] = arr[i] XOR arr[i + 1]` "
            "for every `0 <= i < n - 1`. Given `encoded` and the first element `first = arr[0]`, return the "
            "original array `arr`."
        ),
        "cons": [
            "1 <= encoded.length <= 10^4",
            "0 <= encoded[i] <= 10^5",
            "0 <= first <= 10^5",
        ],
        "hints": [
            "XOR is its own inverse: if `encoded[i] = arr[i] ^ arr[i + 1]`, then `arr[i + 1] = arr[i] ^ encoded[i]`.",
            "Initialize the result array with `first` and iteratively XOR the last decoded element with `encoded[i]`.",
        ],
        "explanations": [
            "Starting from 1: 1^1=0, 0^2=2, 2^3=1, recovering [1, 0, 2, 1].",
            "Starting from 4: 4^6=2, 2^2=0, 0^7=7, 7^3=4, recovering [4, 2, 0, 7, 4].",
            "With a single encoded value 0, both elements equal first = 5.",
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "decodeXoredArray",
        "params": [("encoded", "int[]"), ("first", "int")],
        "ret": "int[]",
        "py": """        arr = [first] * (len(encoded) + 1)
        for i, v in enumerate(encoded):
            arr[i + 1] = arr[i] ^ v
        return arr""",
        "java": """        int n = encoded.length;
        int[] arr = new int[n + 1];
        arr[0] = first;
        for (int i = 0; i < n; i++) {
            arr[i + 1] = arr[i] ^ encoded[i];
        }
        return arr;""",
        "visible": [
            {"encoded": [1, 2, 3], "first": 1},
            {"encoded": [6, 2, 7, 3], "first": 4},
            {"encoded": [0], "first": 5},
        ],
        "hidden": [
            {"encoded": [0], "first": 0},
            {"encoded": [100000], "first": 100000},
            {"encoded": [7, 7, 7, 7], "first": 3},
            {"encoded": [1, 0, 1, 0, 1], "first": 0},
            {"encoded": [15, 31, 63, 127], "first": 255},
            {"encoded": [12, 34, 56, 78, 90], "first": 11},
            {"encoded": [0, 0, 0, 0, 0], "first": 42},
            {"encoded": [99999, 88888, 77777, 66666], "first": 55555},
            {"encoded": [(i * 37 + 13) % 100001 for i in range(1500)], "first": 65432},
        ],
    },
    {
        "slug": "43-neighboring-bitwise-xor",
        "title": "Neighboring Bitwise XOR",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Meta", "Oracle"],
        "desc": (
            "A 0-indexed binary array `derived` of length `n` is formed from a hidden binary array `original` "
            "of length `n` by taking the cyclic pairwise XOR of adjacent elements: for `0 <= i < n - 1`, "
            "`derived[i] = original[i] XOR original[i + 1]`, and for `i = n - 1`, "
            "`derived[n - 1] = original[n - 1] XOR original[0]`. Given `derived`, return `true` if there "
            "exists at least one valid binary array `original` that produces `derived`, or `false` otherwise."
        ),
        "cons": [
            "1 <= derived.length <= 10^5",
            "derived[i] is either 0 or 1.",
        ],
        "hints": [
            "Take the XOR of all elements in `derived`: every `original[i]` appears exactly twice in the product.",
            "Because each `original[i]` cancels itself out, a valid `original` exists if and only if the XOR of all entries in `derived` equals 0.",
        ],
        "explanations": [
            "original = [0, 1, 0] gives [0^1, 1^0, 0^0] = [1, 1, 0].",
            "original = [0, 1] gives [0^1, 1^0] = [1, 1].",
            "Total XOR of [1, 0] is 1 != 0, so no cyclic binary array can produce it.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "doesValidArrayExist",
        "params": [("derived", "int[]")],
        "ret": "boolean",
        "py": """        x = 0
        for v in derived:
            x ^= v
        return x == 0""",
        "java": """        int x = 0;
        for (int v : derived) {
            x ^= v;
        }
        return x == 0;""",
        "visible": [
            {"derived": [1, 1, 0]},
            {"derived": [1, 1]},
            {"derived": [1, 0]},
        ],
        "hidden": [
            {"derived": [0]},
            {"derived": [1]},
            {"derived": [0, 0, 0, 0]},
            {"derived": [1, 1, 1, 1]},
            {"derived": [1, 1, 1]},
            {"derived": [0, 1, 0, 1, 0, 1]},
            {"derived": [1, 0, 1, 0, 1, 1]},
            {"derived": [0, 1] * 1000},
            {"derived": [1, 0] * 1000 + [1]},
        ],
    },
    {
        "slug": "44-bitwise-xor-of-all-pairings",
        "title": "Bitwise XOR of All Pairings",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Amazon", "Google", "Goldman Sachs"],
        "desc": (
            "You are given two 0-indexed arrays of non-negative integers `nums1` and `nums2`. Consider the "
            "array formed by taking `nums1[i] XOR nums2[j]` for every valid pair of indices `(i, j)`. Return "
            "the bitwise XOR of all integers in this pairing array."
        ),
        "cons": [
            "1 <= nums1.length, nums2.length <= 10^5",
            "0 <= nums1[i], nums2[j] <= 10^9",
        ],
        "hints": [
            "Each element of `nums1` participates in `nums2.length` pairings, and each element of `nums2` participates in `nums1.length` pairings.",
            "Any number XORed with itself an even number of times becomes 0, so an array contributes its total XOR only when the other array has odd length.",
        ],
        "explanations": [
            "nums1 has length 3 (odd) and nums2 has length 4 (even), so only nums2 contributes: 10^2^5^0 = 13.",
            "Both arrays have even length 2, so every value cancels out and the total XOR is 0.",
            "Both arrays have length 1 (odd), giving 7 ^ 9 = 14.",
        ],
        "time": "O(n + m)",
        "space": "O(1)",
        "method": "xorAllNums",
        "params": [("nums1", "int[]"), ("nums2", "int[]")],
        "ret": "int",
        "py": """        ans = 0
        if len(nums2) & 1:
            for v in nums1:
                ans ^= v
        if len(nums1) & 1:
            for v in nums2:
                ans ^= v
        return ans""",
        "java": """        int ans = 0;
        if ((nums2.length & 1) == 1) {
            for (int v : nums1) ans ^= v;
        }
        if ((nums1.length & 1) == 1) {
            for (int v : nums2) ans ^= v;
        }
        return ans;""",
        "visible": [
            {"nums1": [2, 1, 3], "nums2": [10, 2, 5, 0]},
            {"nums1": [1, 2], "nums2": [3, 4]},
            {"nums1": [7], "nums2": [9]},
        ],
        "hidden": [
            {"nums1": [0], "nums2": [0]},
            {"nums1": [5, 5, 5], "nums2": [5, 5, 5]},
            {"nums1": [1, 2, 3, 4], "nums2": [8, 16, 32]},
            {"nums1": [1000000000], "nums2": [999999999, 1, 2]},
            {"nums1": [1000000000, 1000000000], "nums2": [123456789]},
            {"nums1": [15, 240, 3840], "nums2": [1, 2, 4, 8, 16]},
            {"nums1": [42], "nums2": [42, 42]},
            {"nums1": [i * 17 for i in range(1001)], "nums2": [i * 31 for i in range(1001)]},
            {"nums1": [i * 23 for i in range(1000)], "nums2": [i * 29 for i in range(1001)]},
        ],
    },
    {
        "slug": "45-minimum-flips-for-target-xor",
        "title": "Minimum Bit Flips to Reach Target XOR",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Amazon", "Microsoft", "Uber"],
        "desc": (
            "You are given a 0-indexed array of non-negative integers `nums` and a non-negative integer `k`. "
            "In a single operation, you may choose any element of `nums` and flip any one bit in its binary "
            "representation (changing a 0 to 1 or a 1 to 0). Return the minimum number of operations required "
            "to make the bitwise XOR of all elements in `nums` equal to `k`."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i] <= 10^9",
            "0 <= k <= 10^9",
        ],
        "hints": [
            "Flipping bit `b` of any single element in `nums` flips bit `b` of the overall XOR of `nums`.",
            "Compute `diff = (XOR of all nums) ^ k`; each set bit in `diff` requires exactly one bit flip.",
        ],
        "explanations": [
            "Current XOR is 2^1^3^4 = 4 (100), target k = 1 (001); they differ in 2 bit positions.",
            "Current XOR is 2^0^2^0 = 0, which already equals k = 0, so 0 flips are needed.",
            "Current XOR is 0 and target k = 7 (111), requiring 3 bit flips.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "minOperationsForXor",
        "params": [("nums", "int[]"), ("k", "int")],
        "ret": "int",
        "py": """        diff = k
        for v in nums:
            diff ^= v
        return diff.bit_count()""",
        "java": """        int diff = k;
        for (int v : nums) {
            diff ^= v;
        }
        return Integer.bitCount(diff);""",
        "visible": [
            {"nums": [2, 1, 3, 4], "k": 1},
            {"nums": [2, 0, 2, 0], "k": 0},
            {"nums": [0], "k": 7},
        ],
        "hidden": [
            {"nums": [0], "k": 0},
            {"nums": [15], "k": 15},
            {"nums": [1, 2, 4, 8], "k": 0},
            {"nums": [1000000000], "k": 0},
            {"nums": [0, 1000000000], "k": 1000000000},
            {"nums": [3, 5, 9, 17, 33], "k": 63},
            {"nums": [536870911, 536870912], "k": 0},
            {"nums": [1, 1, 1, 1, 1], "k": 1000000000},
            {"nums": [(i * 9973) % 1000000000 for i in range(2000)], "k": 123456789},
        ],
    },
    {
        "slug": "46-maximum-xor-for-each-query",
        "title": "Maximum XOR for Each Query",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Meta", "Adobe"],
        "desc": (
            "You are given an integer array `nums` of length `n` and an integer `maximumBit` such that every "
            "element satisfies `0 <= nums[i] < 2^maximumBit`. You perform `n` queries: for the `i`-th query "
            "(0-indexed), find the non-negative integer `k < 2^maximumBit` that maximizes "
            "`nums[0] XOR nums[1] XOR ... XOR nums[n - 1 - i] XOR k`, and record `k` as `answer[i]` "
            "(removing the last remaining element after each query). Return the array `answer`."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "1 <= maximumBit <= 20",
            "0 <= nums[i] < 2^maximumBit",
        ],
        "hints": [
            "The maximum possible XOR value representable with `maximumBit` bits is `mask = (1 << maximumBit) - 1` (all ones).",
            "For any prefix XOR `p`, choosing `k = p ^ mask` achieves `p ^ k = mask`, and you can shrink the prefix XOR from the right in O(1) per query.",
        ],
        "explanations": [
            "mask = 3. Prefix XORs from full array down are 3, 0, 1, 0, giving k = [0, 3, 2, 3].",
            "mask = 7. Prefix XORs are 2, 5, 1, 2, giving k = 5, 2, 6, 5.",
            "mask = 7. Prefix XORs from full array down are 3, 4, 1, 3, 1, 0, giving k = [4, 3, 6, 4, 6, 7].",
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "getMaximumXor",
        "params": [("nums", "int[]"), ("maximumBit", "int")],
        "ret": "int[]",
        "py": """        mask = (1 << maximumBit) - 1
        cur = 0
        for v in nums:
            cur ^= v
        n = len(nums)
        ans = [0] * n
        for i in range(n):
            ans[i] = cur ^ mask
            cur ^= nums[n - 1 - i]
        return ans""",
        "java": """        int mask = (1 << maximumBit) - 1;
        int cur = 0;
        for (int v : nums) cur ^= v;
        int n = nums.length;
        int[] ans = new int[n];
        for (int i = 0; i < n; i++) {
            ans[i] = cur ^ mask;
            cur ^= nums[n - 1 - i];
        }
        return ans;""",
        "visible": [
            {"nums": [0, 1, 1, 3], "maximumBit": 2},
            {"nums": [2, 3, 4, 7], "maximumBit": 3},
            {"nums": [0, 1, 2, 2, 5, 7], "maximumBit": 3},
        ],
        "hidden": [
            {"nums": [0], "maximumBit": 1},
            {"nums": [1], "maximumBit": 1},
            {"nums": [0, 0, 0, 0], "maximumBit": 5},
            {"nums": [15, 15, 15], "maximumBit": 4},
            {"nums": [1, 2, 4, 8, 16], "maximumBit": 5},
            {"nums": [1048575], "maximumBit": 20},
            {"nums": [123, 456, 789, 1011], "maximumBit": 10},
            {"nums": [524288, 262144, 131072, 65536], "maximumBit": 20},
            {"nums": [(i * 4099) & ((1 << 20) - 1) for i in range(1500)], "maximumBit": 20},
        ],
    },
    {
        "slug": "47-count-pairs-with-xor-in-range",
        "title": "Count Pairs With XOR in a Range",
        "difficulty": "Hard",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Meta", "Amazon"],
        "desc": (
            "Given an integer array `nums` and two integers `low` and `high`, return the number of index pairs "
            "`(i, j)` with `0 <= i < j < nums.length` such that `low <= (nums[i] XOR nums[j]) <= high`."
        ),
        "cons": [
            "1 <= nums.length <= 2 * 10^4",
            "0 <= nums[i] <= 2 * 10^4",
            "0 <= low <= high <= 2 * 10^4",
        ],
        "hints": [
            "Transform the range query `[low, high]` into `countLess(high + 1) - countLess(low)`, where `countLess(limit)` counts pairs whose XOR is strictly less than `limit`.",
            "Insert numbers one by one into a bitwise Trie (most significant bit first) storing subtree counts; when bit `b` of `limit` is 1, all previously inserted numbers matching bit `b` of `x` yield XOR bit 0 and can be counted immediately.",
        ],
        "explanations": [
            "All 6 unordered pairs of [1, 4, 2, 7] have XOR in [2, 6]: 1^4=5, 1^2=3, 1^7=6, 4^2=6, 4^7=3, 2^7=5.",
            "Among [9, 8, 4, 2, 1], 8 pairs have XOR in [5, 14].",
            "With a single element, there are 0 pairs.",
        ],
        "time": "O(n log M)",
        "space": "O(n log M)",
        "method": "countPairsXorInRange",
        "params": [("nums", "int[]"), ("low", "int"), ("high", "int")],
        "ret": "int",
        "py": """        MAX_BIT = 15

        def count_less(limit: int) -> int:
            if limit <= 0:
                return 0
            c0 = [0]
            c1 = [0]
            cnt = [0]
            total = 0
            for x in nums:
                node = 0
                for b in range(MAX_BIT, -1, -1):
                    xb = (x >> b) & 1
                    lb = (limit >> b) & 1
                    if lb == 1:
                        same = c1[node] if xb == 1 else c0[node]
                        if same:
                            total += cnt[same]
                        nxt = c0[node] if xb == 1 else c1[node]
                    else:
                        nxt = c1[node] if xb == 1 else c0[node]
                    if nxt == 0:
                        break
                    node = nxt
                node = 0
                for b in range(MAX_BIT, -1, -1):
                    xb = (x >> b) & 1
                    if xb == 0:
                        if c0[node] == 0:
                            c0[node] = len(cnt)
                            c0.append(0)
                            c1.append(0)
                            cnt.append(0)
                        node = c0[node]
                    else:
                        if c1[node] == 0:
                            c1[node] = len(cnt)
                            c0.append(0)
                            c1.append(0)
                            cnt.append(0)
                        node = c1[node]
                    cnt[node] += 1
            return total

        return count_less(high + 1) - count_less(low)""",
        "java": """        return countLess(nums, high + 1) - countLess(nums, low);
    }

    private int countLess(int[] nums, int limit) {
        if (limit <= 0) return 0;
        final int MAX_BIT = 15;
        int maxNodes = nums.length * (MAX_BIT + 1) + 2;
        int[] c0 = new int[maxNodes];
        int[] c1 = new int[maxNodes];
        int[] cnt = new int[maxNodes];
        int nodes = 1;
        int total = 0;
        for (int x : nums) {
            int node = 0;
            for (int b = MAX_BIT; b >= 0; b--) {
                int xb = (x >> b) & 1;
                int lb = (limit >> b) & 1;
                if (lb == 1) {
                    int same = (xb == 1) ? c1[node] : c0[node];
                    if (same != 0) total += cnt[same];
                    node = (xb == 1) ? c0[node] : c1[node];
                } else {
                    node = (xb == 1) ? c1[node] : c0[node];
                }
                if (node == 0) break;
            }
            node = 0;
            for (int b = MAX_BIT; b >= 0; b--) {
                int xb = (x >> b) & 1;
                if (xb == 0) {
                    if (c0[node] == 0) c0[node] = nodes++;
                    node = c0[node];
                } else {
                    if (c1[node] == 0) c1[node] = nodes++;
                    node = c1[node];
                }
                cnt[node]++;
            }
        }
        return total;""",
        "visible": [
            {"nums": [1, 4, 2, 7], "low": 2, "high": 6},
            {"nums": [9, 8, 4, 2, 1], "low": 5, "high": 14},
            {"nums": [5], "low": 0, "high": 10},
        ],
        "hidden": [
            {"nums": [3, 3, 3, 3], "low": 0, "high": 0},
            {"nums": [3, 3, 3, 3], "low": 1, "high": 10},
            {"nums": [0, 0, 1, 1], "low": 0, "high": 1},
            {"nums": [20000, 19999, 1, 0], "low": 10000, "high": 20000},
            {"nums": [1, 2, 3, 4, 5, 6, 7, 8], "low": 4, "high": 7},
            {"nums": [16384, 8192, 4096, 2048, 1024], "low": 10000, "high": 20000},
            {"nums": [10, 20, 30, 40, 50, 60], "low": 0, "high": 100},
            {"nums": [(i * 131 + 17) % 500 for i in range(300)], "low": 100, "high": 400},
            {"nums": [(i * 997 + 41) % 20001 for i in range(1500)], "low": 5000, "high": 15000},
        ],
    },
    {
        "slug": "48-maximum-subset-xor",
        "title": "Maximum Subset XOR",
        "difficulty": "Hard",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": (
            "Given an array `nums` of non-negative integers, choose any subset of elements (possibly empty, "
            "whose XOR is `0`) so that the bitwise XOR of all chosen elements is as large as possible. "
            "Return this maximum subset XOR value."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "0 <= nums[i] <= 10^9",
        ],
        "hints": [
            "Think of each integer as a 31-bit vector over GF(2) and maintain a linear XOR basis where `basis[b]` holds a basis vector whose highest set bit is `b`.",
            "After building the basis by reducing each number against existing basis vectors, greedily XOR `ans` with `basis[b]` from the highest bit down whenever `ans ^ basis[b] > ans`.",
        ],
        "explanations": [
            "Choosing {2, 5} yields 2 ^ 5 = 7, the maximum possible subset XOR.",
            "Choosing {8, 2, 4, 1} yields 8 ^ 2 ^ 4 ^ 1 = 15.",
            "All elements are 0, so the maximum subset XOR is 0.",
        ],
        "time": "O(n log M)",
        "space": "O(log M)",
        "method": "maxSubsetXor",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        basis = [0] * 31
        for x in nums:
            for b in range(30, -1, -1):
                if (x >> b) & 1:
                    if basis[b] == 0:
                        basis[b] = x
                        break
                    x ^= basis[b]
        ans = 0
        for b in range(30, -1, -1):
            if (ans ^ basis[b]) > ans:
                ans ^= basis[b]
        return ans""",
        "java": """        int[] basis = new int[31];
        for (int x : nums) {
            for (int b = 30; b >= 0; b--) {
                if (((x >> b) & 1) != 0) {
                    if (basis[b] == 0) {
                        basis[b] = x;
                        break;
                    }
                    x ^= basis[b];
                }
            }
        }
        int ans = 0;
        for (int b = 30; b >= 0; b--) {
            if ((ans ^ basis[b]) > ans) {
                ans ^= basis[b];
            }
        }
        return ans;""",
        "visible": [
            {"nums": [2, 4, 5]},
            {"nums": [9, 8, 5, 2, 4, 1]},
            {"nums": [0, 0, 0]},
        ],
        "hidden": [
            {"nums": [0]},
            {"nums": [1000000000]},
            {"nums": [3, 5, 6]},
            {"nums": [8, 1, 2, 12, 7, 6]},
            {"nums": [1 << i for i in range(30)]},
            {"nums": [7, 7, 7, 7]},
            {"nums": [536870912, 536870911]},
            {"nums": [12, 15, 7, 14, 10, 9]},
            {"nums": [(i * 104729 + 12345) % 1000000001 for i in range(2000)]},
        ],
    },

    # ------------------------------------------------------------------
    # Counting Bits (49-56)
    # ------------------------------------------------------------------
    {
        "slug": "49-even-and-odd-bit-counts",
        "title": "Number of Even and Odd Bits",
        "difficulty": "Easy",
        "subtopic": "Counting Bits",
        "companies": ["Amazon", "Apple", "Adobe"],
        "desc": (
            "Given a positive integer `n`, let `even` be the number of 1-bits located at even 0-indexed bit "
            "positions (0, 2, 4, ...) in the binary representation of `n`, and let `odd` be the number of 1-bits "
            "located at odd bit positions (1, 3, 5, ...). Return the two-element integer array `[even, odd]`."
        ),
        "cons": [
            "1 <= n <= 10^9",
        ],
        "hints": [
            "Bit positions 0, 2, 4, ... correspond to the alternating bitmask `0x55555555`, while odd positions 1, 3, 5, ... correspond to `0x2AAAAAAA`.",
            "Mask `n` with each constant and count the remaining set bits using popcount in O(1) time.",
        ],
        "explanations": [
            "17 in binary is 10001, with 1-bits at positions 0 and 4 (both even), giving [2, 0].",
            "2 in binary is 10, with a single 1-bit at position 1 (odd), giving [0, 1].",
            "50 in binary is 110010, with 1-bits at positions 1, 4, and 5 (one even, two odd), giving [1, 2].",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "evenOddBit",
        "params": [("n", "int")],
        "ret": "int[]",
        "py": """        return [(n & 0x55555555).bit_count(), (n & 0x2AAAAAAA).bit_count()]""",
        "java": """        return new int[]{Integer.bitCount(n & 0x55555555), Integer.bitCount(n & 0x2AAAAAAA)};""",
        "visible": [
            {"n": 17},
            {"n": 2},
            {"n": 50},
        ],
        "hidden": [
            {"n": 1},
            {"n": 3},
            {"n": 15},
            {"n": 21},
            {"n": 42},
            {"n": 1023},
            {"n": 357913941},
            {"n": 715827882},
            {"n": 1000000000},
        ],
    },
    {
        "slug": "50-smallest-number-with-all-set-bits",
        "title": "Smallest Number With All Set Bits",
        "difficulty": "Easy",
        "subtopic": "Counting Bits",
        "companies": ["Amazon", "Google", "Microsoft"],
        "desc": (
            "Given a positive integer `n`, return the smallest integer `x` greater than or equal to `n` "
            "such that the binary representation of `x` consists exclusively of set bits (`1`s), i.e. "
            "`x = 2^k - 1` for some positive integer `k`."
        ),
        "cons": [
            "1 <= n <= 10^9",
        ],
        "hints": [
            "If `n` has `b` bits in binary (so `2^(b-1) <= n < 2^b`), what is the smallest all-ones number with at least `b` bits?",
            "Compute `b = bitLength(n)` and return `(1 << b) - 1`, or smear the highest set bit downward.",
        ],
        "explanations": [
            "5 in binary is 101; the smallest all-ones number >= 5 is 7 (111).",
            "10 in binary is 1010; the smallest all-ones number >= 10 is 15 (1111).",
            "3 in binary is already 11, so the answer is 3.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "smallestAllSetBits",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        return (1 << n.bit_length()) - 1""",
        "java": """        int bits = 32 - Integer.numberOfLeadingZeros(n);
        return (1 << bits) - 1;""",
        "visible": [
            {"n": 5},
            {"n": 10},
            {"n": 3},
        ],
        "hidden": [
            {"n": 1},
            {"n": 2},
            {"n": 4},
            {"n": 7},
            {"n": 8},
            {"n": 63},
            {"n": 64},
            {"n": 536870912},
            {"n": 1000000000},
        ],
    },
    {
        "slug": "51-minimize-xor-with-same-set-bits",
        "title": "Minimize XOR With Matching Set Bits",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Salesforce"],
        "desc": (
            "Given two positive integers `num1` and `num2`, find the positive integer `x` such that `x` has "
            "the exact same number of set bits (`1`-bits) as `num2`, and the value `x XOR num1` is minimized. "
            "Return `x`. (The optimal `x` is guaranteed to be unique.)"
        ),
        "cons": [
            "1 <= num1, num2 <= 10^9",
        ],
        "hints": [
            "To minimize `x ^ num1`, cancel out the highest set bits of `num1` first by placing `1`-bits of `x` at those same positions from MSB down to LSB.",
            "If you still have leftover `1`-bits to place after matching all set bits of `num1`, place them in the lowest unset bit positions of `x` from LSB up.",
        ],
        "explanations": [
            "num2 = 5 (101) has 2 set bits. Matching num1 = 3 (11) gives x = 3 with XOR 0.",
            "num2 = 12 (1100) has 2 set bits. Match bit 0 of num1 = 1 and place the remaining bit at position 1, giving x = 3 (11).",
            "num2 = 7 (111) has 3 set bits. Match bits 4 and 3 of num1 = 25 (11001) and bit 0, giving x = 25.",
        ],
        "time": "O(log M)",
        "space": "O(1)",
        "method": "minimizeXor",
        "params": [("num1", "int"), ("num2", "int")],
        "ret": "int",
        "py": """        need = num2.bit_count()
        res = 0
        for b in range(30, -1, -1):
            if need > 0 and ((num1 >> b) & 1):
                res |= 1 << b
                need -= 1
        for b in range(31):
            if need > 0 and not ((res >> b) & 1):
                res |= 1 << b
                need -= 1
        return res""",
        "java": """        int need = Integer.bitCount(num2);
        int res = 0;
        for (int b = 30; b >= 0 && need > 0; b--) {
            if (((num1 >> b) & 1) != 0) {
                res |= 1 << b;
                need--;
            }
        }
        for (int b = 0; b <= 30 && need > 0; b++) {
            if (((res >> b) & 1) == 0) {
                res |= 1 << b;
                need--;
            }
        }
        return res;""",
        "visible": [
            {"num1": 3, "num2": 5},
            {"num1": 1, "num2": 12},
            {"num1": 25, "num2": 7},
        ],
        "hidden": [
            {"num1": 1, "num2": 1},
            {"num1": 65, "num2": 84},
            {"num1": 25, "num2": 72},
            {"num1": 1023, "num2": 1},
            {"num1": 1, "num2": 1023},
            {"num1": 536870912, "num2": 536870911},
            {"num1": 536870911, "num2": 536870912},
            {"num1": 999999999, "num2": 123456789},
            {"num1": 1000000000, "num2": 987654321},
        ],
    },
    {
        "slug": "52-largest-combination-with-positive-and",
        "title": "Largest Combination With Bitwise AND Greater Than Zero",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Amazon", "Meta", "Microsoft"],
        "desc": (
            "Given an array of positive integers `candidates`, evaluate the bitwise AND of any non-empty "
            "subset (combination) of `candidates`. Return the maximum size of a subset whose bitwise AND is "
            "strictly greater than `0`."
        ),
        "cons": [
            "1 <= candidates.length <= 10^5",
            "1 <= candidates[i] <= 10^7",
        ],
        "hints": [
            "A subset has bitwise AND > 0 if and only if there exists at least one bit position `b` where every chosen element has a `1`.",
            "For each bit position `b` from 0 to 23, count how many elements of `candidates` have bit `b` set, and return the maximum count.",
        ],
        "explanations": [
            "The subset [16, 17, 62, 24] all have bit 4 (value 16) set, giving a size-4 combination with AND > 0.",
            "Both 8 and 8 share bit 3, giving size 2.",
            "Powers of two have disjoint set bits, so at most 1 element can be chosen.",
        ],
        "time": "O(n log M)",
        "space": "O(1)",
        "method": "largestCombination",
        "params": [("candidates", "int[]")],
        "ret": "int",
        "py": """        best = 0
        for b in range(24):
            mask = 1 << b
            cnt = 0
            for x in candidates:
                if x & mask:
                    cnt += 1
            if cnt > best:
                best = cnt
        return best""",
        "java": """        int best = 0;
        for (int b = 0; b < 24; b++) {
            int mask = 1 << b;
            int cnt = 0;
            for (int x : candidates) {
                if ((x & mask) != 0) cnt++;
            }
            if (cnt > best) best = cnt;
        }
        return best;""",
        "visible": [
            {"candidates": [16, 17, 71, 62, 12, 24, 14]},
            {"candidates": [8, 8]},
            {"candidates": [1, 2, 4, 8, 16]},
        ],
        "hidden": [
            {"candidates": [1]},
            {"candidates": [10000000]},
            {"candidates": [7, 7, 7, 7, 7]},
            {"candidates": [1, 3, 5, 7, 9, 11]},
            {"candidates": [16, 32, 48, 64, 80, 96]},
            {"candidates": [3, 6, 12, 24, 48, 96]},
            {"candidates": [8388608, 8388609, 8388610, 1]},
            {"candidates": [1 << (i % 20) for i in range(500)]},
            {"candidates": [(i * 97 + 1) % 10000000 + 1 for i in range(2000)]},
        ],
    },
    {
        "slug": "53-longest-bitwise-disjoint-subarray",
        "title": "Longest Bitwise-Disjoint Subarray",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": (
            "You are given an array `nums` consisting of positive integers. A contiguous subarray of `nums` "
            "is called bitwise-disjoint if the bitwise AND of every pair of elements at different indices "
            "within the subarray equals `0`. Return the length of the longest bitwise-disjoint subarray "
            "(every single-element subarray is trivially bitwise-disjoint)."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "1 <= nums[i] <= 10^9",
        ],
        "hints": [
            "In a bitwise-disjoint subarray, no two elements may share a `1` at the same bit position, so the bitwise OR of the window captures every currently occupied bit.",
            "Use a sliding window with a bitmask `used`: while `used & nums[right] != 0`, remove `nums[left]` via `used ^= nums[left]` and advance `left`.",
        ],
        "explanations": [
            "The subarray [3, 8, 48] has 3&8=0, 3&48=0, and 8&48=0, giving length 3.",
            "Every adjacent pair shares at least one set bit, so the longest valid subarray has length 1.",
            "All five powers of two are pairwise disjoint, giving length 5.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "longestDisjointSubarray",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        used = 0
        left = 0
        best = 0
        for right, x in enumerate(nums):
            while used & x:
                used ^= nums[left]
                left += 1
            used |= x
            cur = right - left + 1
            if cur > best:
                best = cur
        return best""",
        "java": """        int used = 0;
        int left = 0;
        int best = 0;
        for (int right = 0; right < nums.length; right++) {
            int x = nums[right];
            while ((used & x) != 0) {
                used ^= nums[left++];
            }
            used |= x;
            int cur = right - left + 1;
            if (cur > best) best = cur;
        }
        return best;""",
        "visible": [
            {"nums": [1, 3, 8, 48, 10]},
            {"nums": [3, 1, 5, 11, 13]},
            {"nums": [1, 2, 4, 8, 16]},
        ],
        "hidden": [
            {"nums": [7]},
            {"nums": [1, 1, 1, 1]},
            {"nums": [1 << i for i in range(30)]},
            {"nums": [1, 2, 4, 3, 8, 16, 32, 64]},
            {"nums": [1000000000, 1, 2, 4, 8]},
            {"nums": [5, 2, 8, 16, 3, 4, 32]},
            {"nums": [536870912, 268435456, 134217728, 67108864]},
            {"nums": [1 << (i % 15) for i in range(600)]},
            {"nums": [(1 << (i % 25)) if i % 26 != 25 else 1023 for i in range(2000)]},
        ],
    },
    {
        "slug": "54-check-all-binary-codes-of-size-k",
        "title": "Check If a String Contains All Binary Codes of Size K",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Meta", "Atlassian"],
        "desc": (
            "Given a binary string `s` and a positive integer `k`, return `true` if every binary string of "
            "length `k` (all `2^k` possible codes) appears as a contiguous substring of `s`, and `false` otherwise."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "1 <= k <= 18",
            "s[i] is either '0' or '1'.",
        ],
        "hints": [
            "There are `2^k` distinct binary codes of length `k`, so if `s.length - k + 1 < 2^k` you can return `false` immediately.",
            "Maintain a rolling `k`-bit integer mask `code = ((code << 1) & mask) | bit` and track newly seen codes in a boolean array of size `2^k`.",
        ],
        "explanations": [
            "All four 2-bit codes (\"00\", \"01\", \"10\", \"11\") appear in \"00110110\".",
            "Both 1-bit codes (\"0\" and \"1\") appear in \"0110\".",
            "The 2-bit code \"00\" never appears in \"0110\".",
        ],
        "time": "O(n)",
        "space": "O(2^k)",
        "method": "hasAllCodes",
        "params": [("s", "String"), ("k", "int")],
        "ret": "boolean",
        "py": """        need = 1 << k
        if len(s) - k + 1 < need:
            return False
        seen = bytearray(need)
        mask = need - 1
        code = 0
        for i, ch in enumerate(s):
            code = ((code << 1) & mask) | (ord(ch) - 48)
            if i >= k - 1 and not seen[code]:
                seen[code] = 1
                need -= 1
                if need == 0:
                    return True
        return False""",
        "java": """        int need = 1 << k;
        if (s.length() - k + 1 < need) return false;
        boolean[] seen = new boolean[need];
        int mask = need - 1;
        int code = 0;
        for (int i = 0; i < s.length(); i++) {
            code = ((code << 1) & mask) | (s.charAt(i) - '0');
            if (i >= k - 1 && !seen[code]) {
                seen[code] = true;
                if (--need == 0) return true;
            }
        }
        return false;""",
        "visible": [
            {"s": "00110110", "k": 2},
            {"s": "0110", "k": 1},
            {"s": "0110", "k": 2},
        ],
        "hidden": [
            {"s": "0", "k": 1},
            {"s": "1", "k": 1},
            {"s": "0001011100", "k": 3},
            {"s": "000101110", "k": 3},
            {"s": "00110", "k": 2},
            {"s": "0000000000", "k": 1},
            {"s": "0000100110101111000", "k": 4},
            {"s": "01" * 1000, "k": 10},
            {"s": "".join(format(i, "010b") for i in range(1024)), "k": 10},
        ],
    },
    {
        "slug": "55-minimum-array-end",
        "title": "Minimum Array End",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "You are given two positive integers `n` and `x`. You must construct an array `nums` of `n` "
            "strictly increasing positive integers (`nums[0] < nums[1] < ... < nums[n - 1]`) such that the "
            "bitwise AND of all `n` elements equals `x`. Return the minimum possible value of `nums[n - 1]`."
        ),
        "cons": [
            "1 <= n <= 10^8",
            "1 <= x <= 10^8",
        ],
        "hints": [
            "Every element of `nums` must have all set bits of `x` turned on, so the smallest possible `nums[0]` is `x` itself and only the zero-bit positions of `x` are free to vary.",
            "The `(n - 1)`-th strictly larger valid number is formed by writing the binary bits of `n - 1` directly into the 0-bit slots of `x` from LSB to MSB.",
        ],
        "explanations": [
            "For n = 3, x = 4 (100), the minimal array is [4, 5, 6] (100, 101, 110), whose last element is 6.",
            "For n = 2, x = 7 (111), the minimal array is [7, 15] (0111, 1111), whose last element is 15.",
            "For n = 1, the array is just [x] = [10].",
        ],
        "time": "O(log n + log x)",
        "space": "O(1)",
        "method": "minEnd",
        "params": [("n", "int"), ("x", "int")],
        "ret": "long",
        "py": """        res = x
        rem = n - 1
        bit = 1
        while rem > 0:
            if (res & bit) == 0:
                if rem & 1:
                    res |= bit
                rem >>= 1
            bit <<= 1
        return res""",
        "java": """        long res = x;
        long rem = n - 1L;
        long bit = 1L;
        while (rem > 0L) {
            if ((res & bit) == 0L) {
                if ((rem & 1L) != 0L) {
                    res |= bit;
                }
                rem >>= 1;
            }
            bit <<= 1;
        }
        return res;""",
        "visible": [
            {"n": 3, "x": 4},
            {"n": 2, "x": 7},
            {"n": 1, "x": 10},
        ],
        "hidden": [
            {"n": 1, "x": 1},
            {"n": 2, "x": 1},
            {"n": 5, "x": 1},
            {"n": 4, "x": 8},
            {"n": 10, "x": 5},
            {"n": 100, "x": 63},
            {"n": 1000000, "x": 1000000},
            {"n": 100000000, "x": 1},
            {"n": 100000000, "x": 100000000},
        ],
    },
    {
        "slug": "56-count-integers-with-k-set-bits",
        "title": "Count Integers With Exactly K Set Bits",
        "difficulty": "Hard",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Microsoft", "Goldman Sachs"],
        "desc": (
            "Given a non-negative integer `n` and an integer `k`, return the total number of integers `x` "
            "satisfying `0 <= x <= n` whose binary representation has exactly `k` set bits (`1`-bits)."
        ),
        "cons": [
            "0 <= n <= 10^15",
            "0 <= k <= 60",
        ],
        "hints": [
            "Scan the binary representation of `n` from the most significant bit down to bit 0, tracking how many set bits `rem` remain to be placed.",
            "Whenever bit `b` of `n` is `1`, placing a `0` at bit `b` guarantees the number is strictly less than `n`, contributing `C(b, rem)` valid completions from Pascal's triangle; then fix bit `b` to `1` and decrement `rem`.",
        ],
        "explanations": [
            "Among 0..5, the integers with 2 set bits are 3 (11) and 5 (101), so the count is 2.",
            "Among 0..7, the integers with 1 set bit are 1, 2, and 4, so the count is 3.",
            "Only 0 has 0 set bits, so the count is 1.",
        ],
        "time": "O(log^2 n)",
        "space": "O(log^2 n)",
        "method": "countWithKSetBits",
        "params": [("n", "long"), ("k", "int")],
        "ret": "long",
        "py": """        if k == 0:
            return 1
        MAX_B = 60
        comb = [[0] * (MAX_B + 1) for _ in range(MAX_B + 1)]
        for i in range(MAX_B + 1):
            comb[i][0] = 1
            for j in range(1, i + 1):
                comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j]
        ans = 0
        rem = k
        for b in range(MAX_B - 1, -1, -1):
            if (n >> b) & 1:
                if 0 <= rem <= b:
                    ans += comb[b][rem]
                rem -= 1
                if rem < 0:
                    break
        if rem == 0:
            ans += 1
        return ans""",
        "java": """        if (k == 0) return 1L;
        final int MAX_B = 60;
        long[][] comb = new long[MAX_B + 1][MAX_B + 1];
        for (int i = 0; i <= MAX_B; i++) {
            comb[i][0] = 1L;
            for (int j = 1; j <= i; j++) {
                comb[i][j] = comb[i - 1][j - 1] + comb[i - 1][j];
            }
        }
        long ans = 0L;
        int rem = k;
        for (int b = MAX_B - 1; b >= 0; b--) {
            if (((n >> b) & 1L) != 0L) {
                if (rem >= 0 && rem <= b) {
                    ans += comb[b][rem];
                }
                rem--;
                if (rem < 0) break;
            }
        }
        if (rem == 0) ans++;
        return ans;""",
        "visible": [
            {"n": 5, "k": 2},
            {"n": 7, "k": 1},
            {"n": 10, "k": 0},
        ],
        "hidden": [
            {"n": 0, "k": 0},
            {"n": 0, "k": 1},
            {"n": 15, "k": 4},
            {"n": 15, "k": 5},
            {"n": 100, "k": 3},
            {"n": 1023, "k": 5},
            {"n": 1000000000, "k": 10},
            {"n": 1000000000000000, "k": 25},
            {"n": 1000000000000000, "k": 55},
        ],
    },

    # ------------------------------------------------------------------
    # Two Complement (57-63)
    # ------------------------------------------------------------------
    {
        "slug": "57-binary-prefix-divisible-by-five",
        "title": "Binary Prefixes Divisible by 5",
        "difficulty": "Easy",
        "subtopic": "Two Complement",
        "companies": ["Amazon", "Apple", "Oracle"],
        "desc": (
            "You are given a binary array `nums` containing only `0`s and `1`s. Define `x_i` as the integer "
            "whose binary representation is the subarray `nums[0..i]` from most significant bit to least "
            "significant bit. Return a boolean array `answer` of the same length where `answer[i]` is `true` "
            "if `x_i` is divisible by `5`, and `false` otherwise."
        ),
        "cons": [
            "1 <= nums.length <= 10^5",
            "nums[i] is either 0 or 1.",
        ],
        "hints": [
            "Appending a bit `b` to a binary number `x` shifts it left by 1 and ORs in `b`: `x_new = (x << 1) | b`.",
            "Track only `x % 5` at each step using `rem = ((rem << 1) | bit) % 5` to avoid integer overflow.",
        ],
        "explanations": [
            "The prefixes represent 0, 1, and 3 in decimal; only 0 is divisible by 5.",
            "The prefixes represent 1, 3, and 7; none is divisible by 5.",
            "The prefixes represent 1, 2, 5, 10, and 21; 5 and 10 are divisible by 5.",
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "prefixesDivBy5",
        "params": [("nums", "int[]")],
        "ret": "boolean[]",
        "py": """        ans = [False] * len(nums)
        rem = 0
        for i, bit in enumerate(nums):
            rem = ((rem << 1) | bit) % 5
            ans[i] = rem == 0
        return ans""",
        "java": """        boolean[] ans = new boolean[nums.length];
        int rem = 0;
        for (int i = 0; i < nums.length; i++) {
            rem = ((rem << 1) | nums[i]) % 5;
            ans[i] = rem == 0;
        }
        return ans;""",
        "visible": [
            {"nums": [0, 1, 1]},
            {"nums": [1, 1, 1]},
            {"nums": [1, 0, 1, 0, 1]},
        ],
        "hidden": [
            {"nums": [0]},
            {"nums": [1]},
            {"nums": [0, 0, 0, 0]},
            {"nums": [1, 0, 1]},
            {"nums": [1, 1, 1, 1]},
            {"nums": [0, 1, 1, 1, 1, 1]},
            {"nums": [1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 1]},
            {"nums": [1, 0, 1, 0] * 100},
            {"nums": [(i * 7 + 3) % 2 for i in range(1500)]},
        ],
    },
    {
        "slug": "58-steps-to-reduce-binary-to-one",
        "title": "Steps to Reduce a Binary Number to One",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Microsoft", "Google", "Meta"],
        "desc": (
            "Given the binary representation of a positive integer as a string `s` (with no leading zeros), "
            "return the number of steps required to reduce it to `1` under the following rules: if the current "
            "number is even, divide it by `2`; if the current number is odd, add `1` to it."
        ),
        "cons": [
            "1 <= s.length <= 10^5",
            "s consists only of '0' and '1', and s[0] == '1'.",
        ],
        "hints": [
            "Process the binary string from the least significant bit (rightmost) toward index 1 while maintaining a `carry` bit (0 or 1).",
            "If `bit + carry == 1`, the current number is odd, so you add 1 (setting `carry = 1`) and then shift right (2 steps total); otherwise it is even and shifts right in 1 step.",
        ],
        "explanations": [
            "1101 (13) -> 14 -> 7 -> 8 -> 4 -> 2 -> 1 takes 6 steps.",
            "10 (2) -> 1 takes 1 step.",
            "1 is already 1, taking 0 steps.",
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "numSteps",
        "params": [("s", "String")],
        "ret": "int",
        "py": """        steps = 0
        carry = 0
        for i in range(len(s) - 1, 0, -1):
            if (ord(s[i]) - 48) + carry == 1:
                steps += 2
                carry = 1
            else:
                steps += 1
        return steps + carry""",
        "java": """        int steps = 0;
        int carry = 0;
        for (int i = s.length() - 1; i > 0; i--) {
            if ((s.charAt(i) - '0') + carry == 1) {
                steps += 2;
                carry = 1;
            } else {
                steps += 1;
            }
        }
        return steps + carry;""",
        "visible": [
            {"s": "1101"},
            {"s": "10"},
            {"s": "1"},
        ],
        "hidden": [
            {"s": "11"},
            {"s": "100"},
            {"s": "111"},
            {"s": "10000"},
            {"s": "11111111"},
            {"s": "101010101"},
            {"s": "11000101011101"},
            {"s": "1" + "0" * 2000},
            {"s": "1" * 2000},
        ],
    },
    {
        "slug": "59-next-higher-same-popcount",
        "title": "Next Higher Integer With Same Set Bits",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Apple", "Bloomberg"],
        "desc": (
            "Given a positive integer `n`, return the smallest integer strictly greater than `n` that has the "
            "exact same number of `1`-bits in its binary representation."
        ),
        "cons": [
            "1 <= n <= 10^15",
        ],
        "hints": [
            "Isolate the lowest set bit with two's complement: `c = n & -n`. Adding `c` to `n` (`r = n + c`) turns the rightmost contiguous block of `1`-bits into `0`s and promotes the next `0` bit to `1`.",
            "Gosper's hack restores the remaining `k - 1` ones from that block to the lowest bit positions in O(1): `(((r ^ n) >> 2) // c) | r`.",
        ],
        "explanations": [
            "6 is 110 in binary (two 1s); the next higher integer with two 1s is 9 (1001).",
            "12 is 1100 in binary (two 1s); the next higher integer with two 1s is 17 (10001).",
            "1 is 1 in binary (one 1); the next higher integer with one 1 is 2 (10).",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "nextHigherSameBits",
        "params": [("n", "long")],
        "ret": "long",
        "py": """        c = n & -n
        r = n + c
        return (((r ^ n) >> 2) // c) | r""",
        "java": """        long c = n & -n;
        long r = n + c;
        return (((r ^ n) >> 2) / c) | r;""",
        "visible": [
            {"n": 6},
            {"n": 12},
            {"n": 1},
        ],
        "hidden": [
            {"n": 2},
            {"n": 3},
            {"n": 7},
            {"n": 15},
            {"n": 18},
            {"n": 156},
            {"n": 1073741823},
            {"n": 1000000000000},
            {"n": 1000000000000000},
        ],
    },
    {
        "slug": "60-min-power-of-two-ops-to-zero",
        "title": "Minimum Power-of-Two Operations to Zero",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Amazon", "Google", "Uber"],
        "desc": (
            "You are given a positive integer `n`. In one operation, you may add or subtract any power of two "
            "(`2^i` for any integer `i >= 0`) to or from `n`. Return the minimum number of operations required "
            "to reduce `n` to `0`."
        ),
        "cons": [
            "1 <= n <= 10^9",
        ],
        "hints": [
            "Inspect the lowest set bit `low = n & -n` using two's complement.",
            "If the next bit `(low << 1)` is also set (a run of two or more consecutive `1`s), adding `low` collapses the entire run into a single higher bit; otherwise subtracting `low` eliminates that isolated bit.",
        ],
        "explanations": [
            "39 + 1 = 40, 40 - 8 = 32, 32 - 32 = 0 (3 operations).",
            "54 + 2 = 56, 56 + 8 = 64, 64 - 64 = 0 (3 operations).",
            "16 is already a power of two, so 16 - 16 = 0 takes 1 operation.",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "minOpsToZero",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        x = n
        ops = 0
        while x > 0:
            low = x & -x
            if x & (low << 1):
                x += low
            else:
                x -= low
            ops += 1
        return ops""",
        "java": """        long x = n;
        int ops = 0;
        while (x > 0L) {
            long low = x & -x;
            if ((x & (low << 1)) != 0L) {
                x += low;
            } else {
                x -= low;
            }
            ops++;
        }
        return ops;""",
        "visible": [
            {"n": 39},
            {"n": 54},
            {"n": 16},
        ],
        "hidden": [
            {"n": 1},
            {"n": 3},
            {"n": 5},
            {"n": 7},
            {"n": 11},
            {"n": 27},
            {"n": 1023},
            {"n": 715827882},
            {"n": 1000000000},
        ],
    },
    {
        "slug": "61-add-two-negabinary-numbers",
        "title": "Add Two Negabinary Numbers",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Bloomberg", "Microsoft"],
        "desc": (
            "Given two numbers `arr1` and `arr2` represented in base `-2` (negabinary) as arrays of `0`s and `1`s "
            "from most significant bit to least significant bit with no leading zeros (except `[0]` for zero), "
            "return their sum in the same base `-2` format with no leading zeros."
        ),
        "cons": [
            "1 <= arr1.length, arr2.length <= 1000",
            "arr1[i] and arr2[i] are either 0 or 1.",
            "arr1 and arr2 have no leading zeros unless representing 0 as [0].",
        ],
        "hints": [
            "Add from right to left while keeping a signed `carry` that can be `-1`, `0`, or `1`.",
            "At each digit with total `s = bit1 + bit2 + carry`, emit `s & 1` and propagate `carry = -(s >> 1)` because `2 * (-2)^k = (-1) * (-2)^(k+1)` and `(-1) * (-2)^k = 1 * (-2)^k + 1 * (-2)^(k+1)`.",
        ],
        "explanations": [
            "[1,1,1,1,1] is 11 and [1,0,1] is 5; their sum 16 in base -2 is [1,0,0,0,0].",
            "0 + 0 = 0, represented as [0].",
            "[1,1] (-1) + [1] (1) = 0, represented as [0] after stripping leading zeros.",
        ],
        "time": "O(n + m)",
        "space": "O(n + m)",
        "method": "addNegabinary",
        "params": [("arr1", "int[]"), ("arr2", "int[]")],
        "ret": "int[]",
        "py": """        i = len(arr1) - 1
        j = len(arr2) - 1
        carry = 0
        res = []
        while i >= 0 or j >= 0 or carry != 0:
            if i >= 0:
                carry += arr1[i]
                i -= 1
            if j >= 0:
                carry += arr2[j]
                j -= 1
            res.append(carry & 1)
            carry = -(carry >> 1)
        while len(res) > 1 and res[-1] == 0:
            res.pop()
        res.reverse()
        return res""",
        "java": """        int i = arr1.length - 1;
        int j = arr2.length - 1;
        int carry = 0;
        List<Integer> list = new ArrayList<>();
        while (i >= 0 || j >= 0 || carry != 0) {
            if (i >= 0) carry += arr1[i--];
            if (j >= 0) carry += arr2[j--];
            list.add(carry & 1);
            carry = -(carry >> 1);
        }
        while (list.size() > 1 && list.get(list.size() - 1) == 0) {
            list.remove(list.size() - 1);
        }
        int n = list.size();
        int[] res = new int[n];
        for (int k = 0; k < n; k++) {
            res[k] = list.get(n - 1 - k);
        }
        return res;""",
        "visible": [
            {"arr1": [1, 1, 1, 1, 1], "arr2": [1, 0, 1]},
            {"arr1": [0], "arr2": [0]},
            {"arr1": [1, 1], "arr2": [1]},
        ],
        "hidden": [
            {"arr1": [0], "arr2": [1]},
            {"arr1": [1], "arr2": [1]},
            {"arr1": [1, 0, 1], "arr2": [1, 0, 1]},
            {"arr1": [1, 1, 0], "arr2": [1, 0]},
            {"arr1": [1, 0, 0, 0, 0], "arr2": [1, 1, 0, 0, 0]},
            {"arr1": [1, 1, 1, 1], "arr2": [1, 1, 1, 1]},
            {"arr1": [1, 0, 1, 0, 1, 0, 1], "arr2": [1, 1, 0, 1, 1, 0]},
            {"arr1": [1] + [0, 1] * 250, "arr2": [1] + [1, 0] * 250},
            {"arr1": [1] * 1000, "arr2": [1] * 1000},
        ],
    },
    {
        "slug": "62-integer-replacement-to-one",
        "title": "Minimum Replacements to Reduce Integer to One",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Amazon", "Apple"],
        "desc": (
            "Given a positive integer `n`, you can repeatedly apply one operation: if `n` is even, replace `n` "
            "with `n / 2`; if `n` is odd, replace `n` with either `n + 1` or `n - 1`. Return the minimum number "
            "of operations needed for `n` to become `1`."
        ),
        "cons": [
            "1 <= n <= 2^31 - 1",
        ],
        "hints": [
            "When `n` is odd, examine its lowest two bits (`n & 3`): if `(n & 3) == 1` or `n == 3`, decrementing produces more trailing zeros (or reaches 2 directly); otherwise incrementing creates at least two trailing zeros.",
            "Promote `n` to a 64-bit integer so that adding 1 to `2^31 - 1` does not overflow a signed 32-bit integer.",
        ],
        "explanations": [
            "8 -> 4 -> 2 -> 1 takes 3 operations.",
            "7 -> 8 -> 4 -> 2 -> 1 takes 4 operations.",
            "3 -> 2 -> 1 takes 2 operations.",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "integerReplacement",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        x = n
        steps = 0
        while x > 1:
            if (x & 1) == 0:
                x >>= 1
            elif x == 3 or (x & 3) == 1:
                x -= 1
            else:
                x += 1
            steps += 1
        return steps""",
        "java": """        long x = n;
        int steps = 0;
        while (x > 1L) {
            if ((x & 1L) == 0L) {
                x >>= 1;
            } else if (x == 3L || (x & 3L) == 1L) {
                x--;
            } else {
                x++;
            }
            steps++;
        }
        return steps;""",
        "visible": [
            {"n": 8},
            {"n": 7},
            {"n": 3},
        ],
        "hidden": [
            {"n": 1},
            {"n": 2},
            {"n": 4},
            {"n": 15},
            {"n": 65535},
            {"n": 10000},
            {"n": 123456789},
            {"n": 2147483646},
            {"n": 2147483647},
        ],
    },
    {
        "slug": "63-non-negative-integers-without-consecutive-ones",
        "title": "Non-Negative Integers Without Consecutive Ones",
        "difficulty": "Hard",
        "subtopic": "Two Complement",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": (
            "Given a non-negative integer `n`, return the count of integers `x` in the inclusive range `[0, n]` "
            "whose binary representations do not contain two consecutive `1`-bits."
        ),
        "cons": [
            "0 <= n <= 10^9",
        ],
        "hints": [
            "The number of valid `b`-bit binary strings with no consecutive ones follows the Fibonacci sequence: `fib[0] = 1, fib[1] = 2, fib[b] = fib[b - 1] + fib[b - 2]`.",
            "Walk the bits of `n` from MSB to LSB: whenever bit `b` is `1`, add `fib[b]` for putting `0` at bit `b`; if the previous bit was also `1`, stop immediately because no valid number can match this prefix.",
        ],
        "explanations": [
            "In [0, 5], 0 (0), 1 (1), 2 (10), 4 (100), and 5 (101) have no consecutive ones; only 3 (11) fails, leaving 5.",
            "In [0, 1], both 0 and 1 are valid, giving 2.",
            "In [0, 3], 0, 1, and 2 are valid while 3 (11) is not, giving 3.",
        ],
        "time": "O(log n)",
        "space": "O(log n)",
        "method": "findIntegers",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        fib = [0] * 32
        fib[0] = 1
        fib[1] = 2
        for i in range(2, 32):
            fib[i] = fib[i - 1] + fib[i - 2]
        ans = 0
        prev_bit = 0
        for b in range(30, -1, -1):
            if (n >> b) & 1:
                ans += fib[b]
                if prev_bit == 1:
                    return ans
                prev_bit = 1
            else:
                prev_bit = 0
        return ans + 1""",
        "java": """        int[] fib = new int[32];
        fib[0] = 1;
        fib[1] = 2;
        for (int i = 2; i < 32; i++) {
            fib[i] = fib[i - 1] + fib[i - 2];
        }
        int ans = 0;
        int prevBit = 0;
        for (int b = 30; b >= 0; b--) {
            if (((n >> b) & 1) != 0) {
                ans += fib[b];
                if (prevBit == 1) return ans;
                prevBit = 1;
            } else {
                prevBit = 0;
            }
        }
        return ans + 1;""",
        "visible": [
            {"n": 5},
            {"n": 1},
            {"n": 3},
        ],
        "hidden": [
            {"n": 0},
            {"n": 2},
            {"n": 4},
            {"n": 7},
            {"n": 8},
            {"n": 21},
            {"n": 1000},
            {"n": 715827882},
            {"n": 1000000000},
        ],
    },

    # ------------------------------------------------------------------
    # Fast Exponentiation (64-70)
    # ------------------------------------------------------------------
    {
        "slug": "64-power-of-three-check",
        "title": "Power of Three Check",
        "difficulty": "Easy",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Amazon", "LinkedIn"],
        "desc": (
            "Given a signed 32-bit integer `n`, return `true` if `n` is a power of three (meaning there exists "
            "an integer `k >= 0` such that `n == 3^k`), and `false` otherwise."
        ),
        "cons": [
            "-2^31 <= n <= 2^31 - 1",
        ],
        "hints": [
            "Because 3 is prime, a positive 32-bit integer is a power of 3 if and only if it divides the largest power of 3 that fits in a signed 32-bit integer.",
            "The largest power of 3 within `2^31 - 1` is `3^19 = 1162261467`, so check `n > 0 && 1162261467 % n == 0` in O(1) time.",
        ],
        "explanations": [
            "27 = 3^3, so return true.",
            "0 is not a power of three.",
            "Negative integers like -9 can never equal 3^k for any integer k.",
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "isPowerOfThree",
        "params": [("n", "int")],
        "ret": "boolean",
        "py": """        return n > 0 and 1162261467 % n == 0""",
        "java": """        return n > 0 && 1162261467 % n == 0;""",
        "visible": [
            {"n": 27},
            {"n": 0},
            {"n": -9},
        ],
        "hidden": [
            {"n": 1},
            {"n": 3},
            {"n": 9},
            {"n": 45},
            {"n": -1},
            {"n": -2147483648},
            {"n": 1162261467},
            {"n": 1162261466},
            {"n": 2147483647},
        ],
    },
    {
        "slug": "65-sum-of-powers-of-three",
        "title": "Check if Number is a Sum of Powers of Three",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Amazon", "Google", "Adobe"],
        "desc": (
            "Given a positive integer `n`, return `true` if `n` can be represented as the sum of one or more "
            "distinct powers of three (`3^k` for distinct non-negative integers `k`), and `false` otherwise."
        ),
        "cons": [
            "1 <= n <= 10^9",
        ],
        "hints": [
            "Express `n` in base 3: using each power of three at most once means every base-3 digit of `n` must be `0` or `1`.",
            "Repeatedly check `n % 3`: if the remainder is ever `2`, return `false`; otherwise divide `n` by `3` until `n == 0`.",
        ],
        "explanations": [
            "12 = 3^1 + 3^2 = 3 + 9.",
            "91 = 3^0 + 3^2 + 3^4 = 1 + 9 + 81.",
            "21 in base 3 is 210_3, which requires two copies of 3^2, so return false.",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "checkPowersOfThree",
        "params": [("n", "int")],
        "ret": "boolean",
        "py": """        while n > 0:
            if n % 3 == 2:
                return False
            n //= 3
        return True""",
        "java": """        while (n > 0) {
            if (n % 3 == 2) return false;
            n /= 3;
        }
        return true;""",
        "visible": [
            {"n": 12},
            {"n": 91},
            {"n": 21},
        ],
        "hidden": [
            {"n": 1},
            {"n": 2},
            {"n": 3},
            {"n": 4},
            {"n": 6},
            {"n": 757},
            {"n": 10000000},
            {"n": 387420489 + 129140163 + 43046721 + 1},
            {"n": 1000000000},
        ],
    },
    {
        "slug": "66-floating-point-power",
        "title": "Fast Power (x^n)",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Meta", "Google", "Amazon"],
        "desc": (
            "Implement `myPow(x, n)`, which calculates `x` raised to the integer power `n` (`x^n`) using "
            "binary exponentiation. Note that `n` can be zero or negative, including `-2^31`, and answers "
            "are compared within a floating-point tolerance of `1e-5`."
        ),
        "cons": [
            "-100.0 < x < 100.0",
            "-2^31 <= n <= 2^31 - 1",
            "Either x != 0.0 or n > 0.",
            "-10^4 <= x^n <= 10^4",
        ],
        "hints": [
            "Promote `n` to a 64-bit signed integer before negating it so `-2^31` does not overflow; when `n < 0`, replace `x` with `1.0 / x` and negate `n`.",
            "Repeatedly square `x` and shift `n` right by 1 bit, multiplying into the result whenever the lowest bit of `n` is 1.",
        ],
        "explanations": [
            "2.0^10 = 1024.0.",
            "2.1^3 = 9.261.",
            "2.0^(-2) = 1 / 4 = 0.25.",
        ],
        "time": "O(log |n|)",
        "space": "O(1)",
        "compare": "float",
        "method": "myPow",
        "params": [("x", "double"), ("n", "int")],
        "ret": "double",
        "py": """        exp = n
        base = x
        if exp < 0:
            base = 1.0 / base
            exp = -exp
        res = 1.0
        while exp > 0:
            if exp & 1:
                res *= base
            base *= base
            exp >>= 1
        return res""",
        "java": """        long exp = n;
        double base = x;
        if (exp < 0L) {
            base = 1.0 / base;
            exp = -exp;
        }
        double res = 1.0;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) {
                res *= base;
            }
            base *= base;
            exp >>= 1;
        }
        return res;""",
        "visible": [
            {"x": 2.0, "n": 10},
            {"x": 2.1, "n": 3},
            {"x": 2.0, "n": -2},
        ],
        "hidden": [
            {"x": 1.0, "n": 0},
            {"x": 0.0, "n": 5},
            {"x": -2.0, "n": 3},
            {"x": -2.0, "n": 4},
            {"x": 1.0, "n": -2147483648},
            {"x": -1.0, "n": -2147483648},
            {"x": -1.0, "n": 2147483647},
            {"x": 2.0, "n": -2147483648},
            {"x": 1.00001, "n": 123456},
        ],
    },
    {
        "slug": "67-modular-multiplicative-inverse",
        "title": "Modular Multiplicative Inverse",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Goldman Sachs", "Microsoft"],
        "desc": (
            "Given a non-negative integer `a` and a prime integer `p`, find the unique integer `x` in "
            "`[1, p - 1]` such that `(a * x) % p == 1`. If no such modular inverse exists (which happens "
            "when `a` is divisible by `p`), return `-1`."
        ),
        "cons": [
            "0 <= a <= 10^15",
            "2 <= p <= 10^9 + 7",
            "p is guaranteed to be a prime number.",
        ],
        "hints": [
            "First reduce `a = a % p`; if `a == 0`, no inverse exists modulo `p`, so return `-1`.",
            "By Fermat's Little Theorem for prime `p`, `a^(p - 1) == 1 (mod p)`, so `a^(-1) == a^(p - 2) (mod p)`, computable via binary exponentiation in O(log p).",
        ],
        "explanations": [
            "3 * 5 = 15 == 1 (mod 7), so the inverse of 3 mod 7 is 5.",
            "10 is divisible by 5, so no inverse exists and we return -1.",
            "2 * 500000004 = 1000000008 == 1 (mod 1000000007).",
        ],
        "time": "O(log p)",
        "space": "O(1)",
        "method": "modInverse",
        "params": [("a", "long"), ("p", "long")],
        "ret": "long",
        "py": """        base = a % p
        if base == 0:
            return -1
        exp = p - 2
        res = 1
        while exp > 0:
            if exp & 1:
                res = (res * base) % p
            base = (base * base) % p
            exp >>= 1
        return res""",
        "java": """        long base = a % p;
        if (base == 0L) return -1L;
        long exp = p - 2L;
        long res = 1L;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) {
                res = (res * base) % p;
            }
            base = (base * base) % p;
            exp >>= 1;
        }
        return res;""",
        "visible": [
            {"a": 3, "p": 7},
            {"a": 10, "p": 5},
            {"a": 2, "p": 1000000007},
        ],
        "hidden": [
            {"a": 0, "p": 2},
            {"a": 1, "p": 2},
            {"a": 1, "p": 1000000007},
            {"a": 1000000006, "p": 1000000007},
            {"a": 2000000014, "p": 1000000007},
            {"a": 123456789, "p": 998244353},
            {"a": 999999999999999, "p": 1000000007},
            {"a": 7, "p": 13},
            {"a": 987654321012345, "p": 998244353},
        ],
    },
    {
        "slug": "68-geometric-series-sum-modulo",
        "title": "Geometric Series Sum Modulo M",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": (
            "Given non-negative integers `a` and `n` and a positive integer `mod` (which is NOT necessarily "
            "prime), compute the geometric series sum `(1 + a + a^2 + ... + a^(n - 1)) % mod`. "
            "When `n == 0`, the empty sum is `0`; by convention `0^0 = 1`, so when `a == 0` and `n >= 1`, "
            "the result is `1 % mod`."
        ),
        "cons": [
            "0 <= a <= 10^9",
            "0 <= n <= 10^15",
            "1 <= mod <= 10^9",
        ],
        "hints": [
            "Because `mod` may not be coprime to `a - 1`, you cannot divide by `a - 1` using a modular inverse.",
            "Use binary doubling: track `curSum = 1 + a + ... + a^(2^k - 1)` and `curPow = a^(2^k)` modulo `mod`, updating `ans = (ans * curPow + curSum) % mod` whenever bit `k` of `n` is 1, then doubling `curSum = curSum * (1 + curPow) % mod`.",
        ],
        "explanations": [
            "1 + 2 + 4 + 8 + 16 = 31, and 31 % 100 = 31.",
            "1 + 3 + 9 + 27 = 40, and 40 % 10 = 0 (note 3 - 1 = 2 is not invertible mod 10).",
            "When n = 0, the empty sum is 0.",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "geometricSeriesMod",
        "params": [("a", "long"), ("n", "long"), ("mod", "long")],
        "ret": "long",
        "py": """        ans = 0
        cur_sum = 1 % mod
        cur_pow = a % mod
        rem = n
        while rem > 0:
            if rem & 1:
                ans = (ans * cur_pow + cur_sum) % mod
            cur_sum = (cur_sum * (1 + cur_pow)) % mod
            cur_pow = (cur_pow * cur_pow) % mod
            rem >>= 1
        return ans""",
        "java": """        long ans = 0L;
        long curSum = 1L % mod;
        long curPow = a % mod;
        long rem = n;
        while (rem > 0L) {
            if ((rem & 1L) != 0L) {
                ans = (ans * curPow + curSum) % mod;
            }
            curSum = (curSum * (1L + curPow)) % mod;
            curPow = (curPow * curPow) % mod;
            rem >>= 1;
        }
        return ans;""",
        "visible": [
            {"a": 2, "n": 5, "mod": 100},
            {"a": 3, "n": 4, "mod": 10},
            {"a": 5, "n": 0, "mod": 1000},
        ],
        "hidden": [
            {"a": 0, "n": 1, "mod": 10},
            {"a": 0, "n": 100, "mod": 10},
            {"a": 1, "n": 1000000000000000, "mod": 1000000000},
            {"a": 7, "n": 10, "mod": 1},
            {"a": 2, "n": 1, "mod": 7},
            {"a": 5, "n": 6, "mod": 12},
            {"a": 10, "n": 1000000000000, "mod": 999999937},
            {"a": 999999999, "n": 999999999999999, "mod": 1000000000},
            {"a": 123456789, "n": 1000000000000000, "mod": 998244353},
        ],
    },
    {
        "slug": "69-maximize-nice-divisors",
        "title": "Maximize Number of Nice Divisors",
        "difficulty": "Hard",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Meta", "Netflix"],
        "desc": (
            "You are given a positive integer `primeFactors`. You may construct a positive integer `n` whose "
            "prime factorization contains at most `primeFactors` prime factors (counted with multiplicity). "
            "A divisor of `n` is called nice if it is divisible by every distinct prime factor of `n`. Return "
            "the maximum number of nice divisors `n` can have, modulo `10^9 + 7`."
        ),
        "cons": [
            "1 <= primeFactors <= 10^9",
        ],
        "hints": [
            "If `n = p_1^{e_1} * p_2^{e_2} * ... * p_k^{e_k}` with `e_1 + ... + e_k <= primeFactors`, the number of nice divisors is the product `e_1 * e_2 * ... * e_k`.",
            "To maximize the product of positive integers with fixed sum `S >= 4`, split `S` into as many `3`s as possible (using `2 * 2` instead of `3 * 1` when `S % 3 == 1`), and compute `3^q` via fast modular exponentiation.",
        ],
        "explanations": [
            "Split 5 = 3 + 2 to get product 3 * 2 = 6 nice divisors (e.g., n = 2^3 * 3^2 = 72).",
            "Split 8 = 3 + 3 + 2 to get product 3 * 3 * 2 = 18 nice divisors.",
            "With 1 prime factor, n = 2 has only 1 nice divisor.",
        ],
        "time": "O(log primeFactors)",
        "space": "O(1)",
        "method": "maxNiceDivisors",
        "params": [("primeFactors", "int")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007
        if primeFactors <= 3:
            return primeFactors
        q, r = divmod(primeFactors, 3)
        if r == 0:
            return pow(3, q, MOD)
        if r == 1:
            return (pow(3, q - 1, MOD) * 4) % MOD
        return (pow(3, q, MOD) * 2) % MOD""",
        "java": """        final long MOD = 1_000_000_007L;
        if (primeFactors <= 3) return primeFactors;
        long q = primeFactors / 3;
        int r = primeFactors % 3;
        if (r == 0) return (int) modPow(3L, q, MOD);
        if (r == 1) return (int) ((modPow(3L, q - 1L, MOD) * 4L) % MOD);
        return (int) ((modPow(3L, q, MOD) * 2L) % MOD);
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
            {"primeFactors": 5},
            {"primeFactors": 8},
            {"primeFactors": 1},
        ],
        "hidden": [
            {"primeFactors": 2},
            {"primeFactors": 3},
            {"primeFactors": 4},
            {"primeFactors": 6},
            {"primeFactors": 7},
            {"primeFactors": 10},
            {"primeFactors": 100},
            {"primeFactors": 999999997},
            {"primeFactors": 1000000000},
        ],
    },
    {
        "slug": "70-count-vowel-permutations-large-n",
        "title": "Count Vowel Permutations for Large N",
        "difficulty": "Hard",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": (
            "Given a positive integer `n`, count how many strings of length `n` can be formed from the five "
            "lowercase vowels `{'a', 'e', 'i', 'o', 'u'}` under the following transition rules: "
            "`'a'` may only be followed by `'e'`; `'e'` may only be followed by `'a'` or `'i'`; `'i'` may not "
            "be followed by another `'i'`; `'o'` may only be followed by `'i'` or `'u'`; and `'u'` may only "
            "be followed by `'a'`. Because `n` can be as large as `10^15`, return the answer modulo `10^9 + 7`."
        ),
        "cons": [
            "1 <= n <= 10^15",
        ],
        "hints": [
            "Model the five vowel counts `[a, e, i, o, u]` at length `k` as a 5-element vector multiplied by a fixed `5 x 5` transition matrix `M` at each step.",
            "Compute `M^(n - 1) mod (10^9 + 7)` using binary matrix exponentiation in O(log n) time; since the base vector at length 1 is all ones, the answer is simply the sum of all 25 entries of `M^(n - 1)`.",
        ],
        "explanations": [
            "For n = 1, the 5 single-vowel strings \"a\", \"e\", \"i\", \"o\", \"u\" are valid.",
            "For n = 2, the 10 valid strings are \"ae\", \"ea\", \"ei\", \"ia\", \"ie\", \"io\", \"iu\", \"oi\", \"ou\", \"ua\".",
            "For n = 5, there are 68 valid vowel strings.",
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "countVowelPermutation",
        "params": [("n", "long")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007

        def mul(A, B):
            C = [[0] * 5 for _ in range(5)]
            for i in range(5):
                ai = A[i]
                ci = C[i]
                for k in range(5):
                    v = ai[k]
                    if v:
                        bk = B[k]
                        for j in range(5):
                            ci[j] = (ci[j] + v * bk[j]) % MOD
            return C

        res = [[1 if i == j else 0 for j in range(5)] for i in range(5)]
        base = [
            [0, 1, 1, 0, 1],
            [1, 0, 1, 0, 0],
            [0, 1, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 1, 0],
        ]
        exp = n - 1
        while exp > 0:
            if exp & 1:
                res = mul(res, base)
            base = mul(base, base)
            exp >>= 1
        return sum(sum(row) for row in res) % MOD""",
        "java": """        final long MOD = 1_000_000_007L;
        long[][] res = new long[5][5];
        for (int i = 0; i < 5; i++) res[i][i] = 1L;
        long[][] base = {
            {0, 1, 1, 0, 1},
            {1, 0, 1, 0, 0},
            {0, 1, 0, 1, 0},
            {0, 0, 1, 0, 0},
            {0, 0, 1, 1, 0}
        };
        long exp = n - 1L;
        while (exp > 0L) {
            if ((exp & 1L) != 0L) res = mul(res, base, MOD);
            base = mul(base, base, MOD);
            exp >>= 1;
        }
        long total = 0L;
        for (int i = 0; i < 5; i++) {
            for (int j = 0; j < 5; j++) {
                total = (total + res[i][j]) % MOD;
            }
        }
        return (int) total;
    }

    private long[][] mul(long[][] a, long[][] b, long mod) {
        long[][] c = new long[5][5];
        for (int i = 0; i < 5; i++) {
            for (int k = 0; k < 5; k++) {
                long v = a[i][k];
                if (v == 0L) continue;
                for (int j = 0; j < 5; j++) {
                    c[i][j] = (c[i][j] + v * b[k][j]) % mod;
                }
            }
        }
        return c;""",
        "visible": [
            {"n": 1},
            {"n": 2},
            {"n": 5},
        ],
        "hidden": [
            {"n": 3},
            {"n": 4},
            {"n": 10},
            {"n": 20},
            {"n": 144},
            {"n": 10000},
            {"n": 1000000000},
            {"n": 999999999999999},
            {"n": 1000000000000000},
        ],
    },
]


def main() -> None:
    expected_prefixes = list(range(41, 71))
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

    print(f"Generated {len(TASKS)} bit-manipulation problems (41-70)")


if __name__ == "__main__":
    main()
