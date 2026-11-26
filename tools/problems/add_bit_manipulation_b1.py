#!/usr/bin/env python3
"""Generate bit-manipulation problems 11-40 for AlgoPlay."""
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


def _make_encoded_perm(perm: list[int]) -> list[int]:
    return [perm[i] ^ perm[i + 1] for i in range(len(perm) - 1)]


def _det_perm(n: int, step: int) -> list[int]:
    # Deterministic permutation of 1..n (step coprime to n)
    return [((i * step) % n) + 1 for i in range(n)]


TASKS = [
    # ------------------------------------------------------------------
    # 11-18: XOR Tricks
    # ------------------------------------------------------------------
    {
        "slug": "11-hamming-distance",
        "title": "Hamming Distance",
        "difficulty": "Easy",
        "subtopic": "XOR Tricks",
        "companies": ["Meta", "Google", "Amazon"],
        "desc": "The Hamming distance between two non-negative integers is the number of bit positions at which their binary representations differ. Given two integers `x` and `y`, return the Hamming distance between them.",
        "cons": ["0 <= x, y <= 2^31 - 1"],
        "hints": [
            "Compute the bitwise XOR `x ^ y` so that every differing bit position becomes a `1`.",
            "Count the number of set bits in `x ^ y` using Brian Kernighan's trick or a built-in popcount."
        ],
        "explanations": [
            "1 is 0001 and 4 is 0100 in binary; they differ at bit positions 0 and 2.",
            "3 is 11 and 1 is 01 in binary; only bit position 1 differs.",
            "Identical numbers have no differing bits, so the distance is 0."
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "hammingDistance",
        "params": [("x", "int"), ("y", "int")],
        "ret": "int",
        "py": """        return (x ^ y).bit_count()""",
        "java": """        return Integer.bitCount(x ^ y);""",
        "visible": [
            {"x": 1, "y": 4},
            {"x": 3, "y": 1},
            {"x": 7, "y": 7},
        ],
        "hidden": [
            {"x": 0, "y": 0},
            {"x": 0, "y": 1},
            {"x": 0, "y": 2147483647},
            {"x": 2147483647, "y": 2147483647},
            {"x": 1431655765, "y": 715827882},
            {"x": 1024, "y": 1023},
            {"x": 93, "y": 73},
            {"x": 123456789, "y": 987654321},
            {"x": 2147483646, "y": 1},
        ],
    },
    {
        "slug": "12-total-hamming-distance",
        "title": "Total Hamming Distance",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Meta", "Google", "Bloomberg"],
        "desc": "Given an integer array `nums` of non-negative integers, return the sum of the Hamming distances between all unordered pairs of elements `(nums[i], nums[j])` with `0 <= i < j < nums.length`.",
        "cons": [
            "1 <= nums.length <= 10^4",
            "0 <= nums[i] <= 10^9",
            "The answer is guaranteed to fit in a 32-bit signed integer."
        ],
        "hints": [
            "Bit positions are independent, so evaluate the contribution of each of the 31 bit positions separately.",
            "If `ones` numbers have bit `b` set and `n - ones` have bit `b` clear, bit `b` contributes `ones * (n - ones)` to the total."
        ],
        "explanations": [
            "Pairs are (4,14)=2, (4,2)=2, and (14,2)=2, giving a total of 6.",
            "Pairs are (4,14)=2, (4,4)=0, and (14,4)=2, giving a total of 4.",
            "A single-element array has no unordered pairs, so the total is 0."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "totalHammingDistance",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        n = len(nums)
        total = 0
        for b in range(31):
            ones = sum((v >> b) & 1 for v in nums)
            total += ones * (n - ones)
        return total""",
        "java": """        int n = nums.length;
        int total = 0;
        for (int b = 0; b < 31; b++) {
            int ones = 0;
            for (int v : nums) {
                ones += (v >>> b) & 1;
            }
            total += ones * (n - ones);
        }
        return total;""",
        "visible": [
            {"nums": [4, 14, 2]},
            {"nums": [4, 14, 4]},
            {"nums": [42]},
        ],
        "hidden": [
            {"nums": [0, 0, 0, 0]},
            {"nums": [1, 2, 4, 8, 16]},
            {"nums": [0, 1000000000]},
            {"nums": [7, 7, 7, 7, 7]},
            {"nums": [0, 1, 2, 3, 4, 5, 6, 7]},
            {"nums": [1000000000, 999999999, 536870912, 536870911]},
            {"nums": [15, 240, 3840, 61440]},
            {"nums": [(i * 2654435761) % 1000000001 for i in range(1, 80)]},
            {"nums": [(i * 1103515245 + 12345) % 1000000001 for i in range(1500)]},
        ],
    },
    {
        "slug": "13-xor-queries-of-a-subarray",
        "title": "XOR Queries of a Subarray",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Amazon", "Google", "Salesforce"],
        "desc": "You are given an integer array `arr` of non-negative integers and a 2D array `queries` where `queries[i] = [left, right]`. For each query `i`, compute the bitwise XOR of all elements from index `left` to `right` inclusive (`arr[left] ^ arr[left + 1] ^ ... ^ arr[right]`). Return an array containing the answer to each query in order.",
        "cons": [
            "1 <= arr.length, queries.length <= 3 * 10^4",
            "0 <= arr[i] <= 10^9",
            "0 <= queries[i][0] <= queries[i][1] < arr.length"
        ],
        "hints": [
            "Precompute a prefix XOR array where `pref[i + 1] = arr[0] ^ arr[1] ^ ... ^ arr[i]`.",
            "Because XOR is its own inverse, the range XOR over `[left, right]` is `pref[right + 1] ^ pref[left]`."
        ],
        "explanations": [
            "Each query evaluates the XOR over its inclusive slice: [0,1]->2, [1,2]->7, [0,3]->14, [3,3]->8.",
            "The four queries yield 8, 0, 4, and 4 respectively.",
            "A single-element array queried at [0,0] returns that element itself."
        ],
        "time": "O(n + q)",
        "space": "O(n)",
        "method": "xorQueries",
        "params": [("arr", "int[]"), ("queries", "int[][]")],
        "ret": "int[]",
        "py": """        pref = [0] * (len(arr) + 1)
        for i, v in enumerate(arr):
            pref[i + 1] = pref[i] ^ v
        return [pref[r + 1] ^ pref[l] for l, r in queries]""",
        "java": """        int n = arr.length;
        int[] pref = new int[n + 1];
        for (int i = 0; i < n; i++) {
            pref[i + 1] = pref[i] ^ arr[i];
        }
        int[] ans = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            ans[i] = pref[queries[i][1] + 1] ^ pref[queries[i][0]];
        }
        return ans;""",
        "visible": [
            {"arr": [1, 3, 4, 8], "queries": [[0, 1], [1, 2], [0, 3], [3, 3]]},
            {"arr": [4, 8, 2, 10], "queries": [[2, 3], [1, 3], [0, 0], [0, 3]]},
            {"arr": [16], "queries": [[0, 0]]},
        ],
        "hidden": [
            {"arr": [0, 0, 0], "queries": [[0, 2], [1, 1], [0, 1]]},
            {"arr": [5, 5, 5, 5], "queries": [[0, 0], [0, 1], [0, 2], [0, 3]]},
            {"arr": [1, 2, 3, 4, 5, 6, 7], "queries": [[0, 6], [1, 5], [2, 4], [3, 3]]},
            {"arr": [1000000000, 999999999, 1000000000], "queries": [[0, 2], [0, 1], [1, 2]]},
            {"arr": [9, 1, 8, 2, 7, 3, 6, 4], "queries": [[0, 7], [2, 6], [4, 7], [0, 3]]},
            {"arr": [10, 20, 30, 40, 50], "queries": [[0, 4], [4, 4], [0, 0], [1, 3], [2, 2]]},
            {"arr": [1 << i for i in range(20)], "queries": [[0, 19], [5, 10], [0, 0], [19, 19]]},
            {"arr": [i * 37 % 1000 for i in range(100)], "queries": [[i, 99 - i] for i in range(50)]},
            {
                "arr": [(i * 48271) % 1000000000 for i in range(1000)],
                "queries": [[(i * 17) % 500, 500 + (i * 31) % 500] for i in range(1000)],
            },
        ],
    },
    {
        "slug": "14-decode-xored-permutation",
        "title": "Decode XORed Permutation",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Amazon", "Meta"],
        "desc": "There is a hidden integer array `perm` that is a permutation of the first `n` positive integers (`1` through `n`), where `n` is guaranteed to be odd. It was encoded into an array `encoded` of length `n - 1` such that `encoded[i] = perm[i] ^ perm[i + 1]` for all `0 <= i < n - 1`. Given `encoded`, reconstruct and return the original permutation `perm`.",
        "cons": [
            "3 <= n <= 10^5",
            "n is odd.",
            "encoded.length == n - 1",
            "A unique valid permutation perm of 1..n is guaranteed to exist."
        ],
        "hints": [
            "Compute `total = 1 ^ 2 ^ ... ^ n`, which equals `perm[0] ^ perm[1] ^ ... ^ perm[n - 1]`.",
            "XORing the odd-indexed entries `encoded[1] ^ encoded[3] ^ ... ^ encoded[n - 2]` equals `perm[1] ^ perm[2] ^ ... ^ perm[n - 1]`, immediately revealing `perm[0]`."
        ],
        "explanations": [
            "perm = [1, 2, 3] encodes to [1^2, 2^3] = [3, 1].",
            "perm = [2, 4, 1, 5, 3] encodes to [6, 5, 4, 6].",
            "perm = [3, 1, 2] encodes to [3^1, 1^2] = [2, 3]."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "decodeXoredPermutation",
        "params": [("encoded", "int[]")],
        "ret": "int[]",
        "py": """        n = len(encoded) + 1
        total = 0
        for x in range(1, n + 1):
            total ^= x
        odd_xor = 0
        for i in range(1, n - 1, 2):
            odd_xor ^= encoded[i]
        perm = [0] * n
        perm[0] = total ^ odd_xor
        for i in range(n - 1):
            perm[i + 1] = perm[i] ^ encoded[i]
        return perm""",
        "java": """        int n = encoded.length + 1;
        int total = 0;
        for (int x = 1; x <= n; x++) {
            total ^= x;
        }
        int oddXor = 0;
        for (int i = 1; i < n - 1; i += 2) {
            oddXor ^= encoded[i];
        }
        int[] perm = new int[n];
        perm[0] = total ^ oddXor;
        for (int i = 0; i < n - 1; i++) {
            perm[i + 1] = perm[i] ^ encoded[i];
        }
        return perm;""",
        "visible": [
            {"encoded": [3, 1]},
            {"encoded": [6, 5, 4, 6]},
            {"encoded": [2, 3]},
        ],
        "hidden": [
            {"encoded": _make_encoded_perm([3, 2, 1])},
            {"encoded": _make_encoded_perm([2, 1, 3])},
            {"encoded": _make_encoded_perm([5, 4, 3, 2, 1])},
            {"encoded": _make_encoded_perm([1, 3, 5, 2, 4])},
            {"encoded": _make_encoded_perm([7, 2, 5, 1, 6, 3, 4])},
            {"encoded": _make_encoded_perm([9, 1, 8, 2, 7, 3, 6, 4, 5])},
            {"encoded": _make_encoded_perm(_det_perm(25, 7))},
            {"encoded": _make_encoded_perm(_det_perm(101, 13))},
            {"encoded": _make_encoded_perm(_det_perm(1501, 23))},
        ],
    },
    {
        "slug": "15-find-original-array-of-prefix-xor",
        "title": "Find Original Array of Prefix XOR",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Amazon", "Microsoft", "Apple"],
        "desc": "You are given an integer array `pref` of length `n`. Find and return the unique array `arr` of length `n` such that `pref[i] = arr[0] ^ arr[1] ^ ... ^ arr[i]` for every `0 <= i < n`.",
        "cons": [
            "1 <= pref.length <= 10^5",
            "0 <= pref[i] <= 10^6"
        ],
        "hints": [
            "Since `pref[i] = pref[i - 1] ^ arr[i]`, XOR both sides with `pref[i - 1]`.",
            "That gives `arr[0] = pref[0]` and `arr[i] = pref[i] ^ pref[i - 1]` for all `i >= 1`."
        ],
        "explanations": [
            "arr = [5, 7, 2, 3, 2] produces prefix XORs [5, 2, 0, 3, 1].",
            "A single-element prefix array equals the original array [13].",
            "Zero prefix XORs mean every original element is 0."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "findOriginalPrefixXor",
        "params": [("pref", "int[]")],
        "ret": "int[]",
        "py": """        n = len(pref)
        ans = [pref[0]] * n
        for i in range(1, n):
            ans[i] = pref[i] ^ pref[i - 1]
        return ans""",
        "java": """        int n = pref.length;
        int[] ans = new int[n];
        ans[0] = pref[0];
        for (int i = 1; i < n; i++) {
            ans[i] = pref[i] ^ pref[i - 1];
        }
        return ans;""",
        "visible": [
            {"pref": [5, 2, 0, 3, 1]},
            {"pref": [13]},
            {"pref": [0, 0, 0]},
        ],
        "hidden": [
            {"pref": [0]},
            {"pref": [1, 1, 1, 1]},
            {"pref": [1000000, 0, 1000000]},
            {"pref": [1, 3, 0, 4, 1, 7, 0]},
            {"pref": [8, 15, 7, 3, 1, 0]},
            {"pref": [999999, 555555, 111111, 777777]},
            {"pref": [1 << i for i in range(18)]},
            {"pref": [i ^ (i >> 1) for i in range(100)]},
            {"pref": [(i * 7919) % 1000001 for i in range(2000)]},
        ],
    },
    {
        "slug": "16-count-triplets-with-equal-xor",
        "title": "Count Triplets with Equal XOR",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Goldman Sachs", "Amazon"],
        "desc": "Given an array of positive integers `arr`, count the number of index triplets `(i, j, k)` with `0 <= i < j <= k < arr.length` such that `a == b`, where `a = arr[i] ^ arr[i + 1] ^ ... ^ arr[j - 1]` and `b = arr[j] ^ arr[j + 1] ^ ... ^ arr[k]`.",
        "cons": [
            "1 <= arr.length <= 1000",
            "1 <= arr[i] <= 10^8"
        ],
        "hints": [
            "`a == b` holds if and only if `a ^ b == 0`, meaning the entire subarray `arr[i..k]` has XOR equal to `0` (`pref[i] == pref[k + 1]`).",
            "Every pair `(i, k)` with `pref[i] == pref[k + 1]` contributes `k - i` valid choices of `j`; track the frequency and index-sum of each prefix XOR in hash maps for O(n) time."
        ],
        "explanations": [
            "The 4 valid triplets are (0,1,2), (0,2,2), (2,3,4), and (2,4,4).",
            "Every even-length subarray of all 1s has XOR 0, yielding 10 valid triplets.",
            "No subarray of [2, 3] has XOR 0, so there are 0 valid triplets."
        ],
        "time": "O(n)",
        "space": "O(n)",
        "method": "countEqualXorTriplets",
        "params": [("arr", "int[]")],
        "ret": "int",
        "py": """        cnt = {0: 1}
        idx_sum = {0: 0}
        pref = 0
        ans = 0
        for m, v in enumerate(arr, 1):
            pref ^= v
            if pref in cnt:
                ans += cnt[pref] * (m - 1) - idx_sum[pref]
                cnt[pref] += 1
                idx_sum[pref] += m
            else:
                cnt[pref] = 1
                idx_sum[pref] = m
        return ans""",
        "java": """        Map<Integer, Integer> cnt = new HashMap<>();
        Map<Integer, Long> idxSum = new HashMap<>();
        cnt.put(0, 1);
        idxSum.put(0, 0L);
        int pref = 0;
        long ans = 0;
        for (int m = 1; m <= arr.length; m++) {
            pref ^= arr[m - 1];
            int c = cnt.getOrDefault(pref, 0);
            long s = idxSum.getOrDefault(pref, 0L);
            if (c > 0) {
                ans += (long) c * (m - 1) - s;
            }
            cnt.put(pref, c + 1);
            idxSum.put(pref, s + m);
        }
        return (int) ans;""",
        "visible": [
            {"arr": [2, 3, 1, 6, 7]},
            {"arr": [1, 1, 1, 1, 1]},
            {"arr": [2, 3]},
        ],
        "hidden": [
            {"arr": [7]},
            {"arr": [5, 5]},
            {"arr": [1, 3, 5, 7, 9]},
            {"arr": [7, 11, 12, 9, 5, 2, 7, 17, 22]},
            {"arr": [4, 4, 4, 4, 4, 4]},
            {"arr": [1, 2, 3, 1, 2, 3]},
            {"arr": [100000000, 100000000, 50000000, 50000000]},
            {"arr": [1, 2, 4, 8, 16, 32, 64]},
            {"arr": [((i * 13) % 7) + 1 for i in range(600)]},
        ],
    },
    {
        "slug": "17-minimum-flips-for-bitwise-or",
        "title": "Minimum Flips for Bitwise OR",
        "difficulty": "Medium",
        "subtopic": "XOR Tricks",
        "companies": ["Microsoft", "Amazon", "Adobe"],
        "desc": "Given three positive integers `a`, `b`, and `c`, return the minimum number of single-bit flips required in the binary representations of `a` and `b` so that `(a | b) == c`. A flip changes a single bit from `0` to `1` or from `1` to `0`.",
        "cons": ["1 <= a, b, c <= 10^9"],
        "hints": [
            "Inspect each bit independently: `(a | b) ^ c` identifies every bit position where `a | b` differs from `c`.",
            "Every mismatching bit needs 1 flip, except when `c` has bit `0` while both `a` and `b` have bit `1`, which requires 2 flips."
        ],
        "explanations": [
            "Flipping 2 (0010) to 1 (0001) and 6 (0110) to 4 (0100) takes 3 flips so 1 | 4 == 5.",
            "Flipping bit 0 of 4 (0100) to 5 (0101) takes 1 flip so 5 | 2 == 7.",
            "1 | 2 already equals 3, so 0 flips are needed."
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "minFlipsForOr",
        "params": [("a", "int"), ("b", "int"), ("c", "int")],
        "ret": "int",
        "py": """        diff = (a | b) ^ c
        return diff.bit_count() + (a & b & diff).bit_count()""",
        "java": """        int diff = (a | b) ^ c;
        return Integer.bitCount(diff) + Integer.bitCount(a & b & diff);""",
        "visible": [
            {"a": 2, "b": 6, "c": 5},
            {"a": 4, "b": 2, "c": 7},
            {"a": 1, "b": 2, "c": 3},
        ],
        "hidden": [
            {"a": 1, "b": 1, "c": 1},
            {"a": 8, "b": 3, "c": 5},
            {"a": 7, "b": 7, "c": 1},
            {"a": 1, "b": 1, "c": 1000000000},
            {"a": 1000000000, "b": 1000000000, "c": 1},
            {"a": 536870911, "b": 536870911, "c": 536870912},
            {"a": 123456, "b": 654321, "c": 777777},
            {"a": 1023, "b": 1023, "c": 1023},
            {"a": 999999999, "b": 888888888, "c": 111111111},
        ],
    },
    {
        "slug": "18-maximum-xor-subarray",
        "title": "Maximum XOR Subarray",
        "difficulty": "Hard",
        "subtopic": "XOR Tricks",
        "companies": ["Google", "Meta", "Uber"],
        "desc": "Given an integer array `nums` of non-negative integers, find the maximum possible bitwise XOR value among all non-empty contiguous subarrays `nums[l..r]` (`0 <= l <= r < nums.length`).",
        "cons": [
            "1 <= nums.length <= 2 * 10^4",
            "0 <= nums[i] <= 10^9"
        ],
        "hints": [
            "Every subarray XOR `nums[l..r]` equals `pref[r + 1] ^ pref[l]`, reducing the problem to finding the maximum XOR between two prefix XORs (including `pref[0] = 0`).",
            "Insert prefix XORs from MSB (bit 29) to LSB (bit 0) into a binary trie and greedily take the opposite bit branch at each level when querying."
        ],
        "explanations": [
            "The subarray [1, 2, 12] has XOR 1 ^ 2 ^ 12 = 15, which is the maximum possible.",
            "The entire array [4, 6] has XOR 4 ^ 6 = 2, while single subarray [6] has XOR 6.",
            "The subarray [1, 2, 3, 4] has XOR 4, while [3, 4] has XOR 7."
        ],
        "time": "O(n log M)",
        "space": "O(n log M)",
        "method": "maxXorSubarray",
        "params": [("nums", "int[]")],
        "ret": "int",
        "py": """        c0 = [-1]
        c1 = [-1]

        def insert(val: int) -> None:
            node = 0
            for b in range(29, -1, -1):
                bit = (val >> b) & 1
                if bit == 0:
                    nxt = c0[node]
                    if nxt == -1:
                        nxt = len(c0)
                        c0[node] = nxt
                        c0.append(-1)
                        c1.append(-1)
                    node = nxt
                else:
                    nxt = c1[node]
                    if nxt == -1:
                        nxt = len(c0)
                        c1[node] = nxt
                        c0.append(-1)
                        c1.append(-1)
                    node = nxt

        def query(val: int) -> int:
            node = 0
            res = 0
            for b in range(29, -1, -1):
                bit = (val >> b) & 1
                if bit == 0:
                    if c1[node] != -1:
                        res |= 1 << b
                        node = c1[node]
                    else:
                        node = c0[node]
                else:
                    if c0[node] != -1:
                        res |= 1 << b
                        node = c0[node]
                    else:
                        node = c1[node]
            return res

        insert(0)
        pref = 0
        best = 0
        for x in nums:
            pref ^= x
            cand = query(pref)
            if cand > best:
                best = cand
            insert(pref)
        return best""",
        "java": """        int maxNodes = (nums.length + 2) * 31;
        int[] c0 = new int[maxNodes];
        int[] c1 = new int[maxNodes];
        Arrays.fill(c0, -1);
        Arrays.fill(c1, -1);
        int size = 1;

        // Insert prefix 0
        int node = 0;
        for (int b = 29; b >= 0; b--) {
            if (c0[node] == -1) c0[node] = size++;
            node = c0[node];
        }

        int pref = 0;
        int best = 0;
        for (int x : nums) {
            pref ^= x;
            node = 0;
            int cand = 0;
            for (int b = 29; b >= 0; b--) {
                int bit = (pref >>> b) & 1;
                if (bit == 0) {
                    if (c1[node] != -1) {
                        cand |= 1 << b;
                        node = c1[node];
                    } else {
                        node = c0[node];
                    }
                } else {
                    if (c0[node] != -1) {
                        cand |= 1 << b;
                        node = c0[node];
                    } else {
                        node = c1[node];
                    }
                }
            }
            if (cand > best) best = cand;

            node = 0;
            for (int b = 29; b >= 0; b--) {
                int bit = (pref >>> b) & 1;
                if (bit == 0) {
                    if (c0[node] == -1) c0[node] = size++;
                    node = c0[node];
                } else {
                    if (c1[node] == -1) c1[node] = size++;
                    node = c1[node];
                }
            }
        }
        return best;""",
        "visible": [
            {"nums": [8, 1, 2, 12, 7, 6]},
            {"nums": [4, 6]},
            {"nums": [1, 2, 3, 4]},
        ],
        "hidden": [
            {"nums": [0]},
            {"nums": [0, 0, 0, 0]},
            {"nums": [1000000000]},
            {"nums": [3, 10, 5, 25, 2, 8]},
            {"nums": [14, 70, 53, 83, 49, 91, 36, 80, 92, 51, 66, 70]},
            {"nums": [1, 2, 4, 8, 16, 32]},
            {"nums": [15, 15, 15, 15]},
            {"nums": [536870912, 536870911, 268435456, 268435455]},
            {"nums": [(i * 1664525 + 1013904223) % 1000000001 for i in range(1500)]},
        ],
    },

    # ------------------------------------------------------------------
    # 19-26: Counting Bits
    # ------------------------------------------------------------------
    {
        "slug": "19-binary-gap",
        "title": "Binary Gap",
        "difficulty": "Easy",
        "subtopic": "Counting Bits",
        "companies": ["Amazon", "Apple", "Oracle"],
        "desc": "Given a positive integer `n`, find and return the longest distance between any two adjacent `1`s in the binary representation of `n`. Two `1`s are adjacent if there are only `0`s separating them (possibly none). The distance between two `1`s is the absolute difference between their bit positions. If there are fewer than two `1`s, return `0`.",
        "cons": ["1 <= n <= 10^9"],
        "hints": [
            "Scan bits from least significant to most significant while maintaining the index `last` of the most recently seen `1` bit.",
            "Whenever you encounter a new `1` at bit index `pos`, update the answer with `pos - last` if `last != -1`."
        ],
        "explanations": [
            "22 in binary is 10110; adjacent 1s are at distances 2 and 1, so the maximum is 2.",
            "8 in binary is 1000, which contains only one 1 bit, so return 0.",
            "5 in binary is 101; the two 1 bits are separated by distance 2."
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "binaryGap",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        last = -1
        best = 0
        pos = 0
        while n > 0:
            if n & 1:
                if last != -1 and pos - last > best:
                    best = pos - last
                last = pos
            n >>= 1
            pos += 1
        return best""",
        "java": """        int last = -1;
        int best = 0;
        int pos = 0;
        while (n > 0) {
            if ((n & 1) == 1) {
                if (last != -1 && pos - last > best) {
                    best = pos - last;
                }
                last = pos;
            }
            n >>>= 1;
            pos++;
        }
        return best;""",
        "visible": [
            {"n": 22},
            {"n": 8},
            {"n": 5},
        ],
        "hidden": [
            {"n": 1},
            {"n": 3},
            {"n": 6},
            {"n": 9},
            {"n": 513},
            {"n": 1024},
            {"n": 536870913},
            {"n": 1000000000},
            {"n": 999999999},
        ],
    },
    {
        "slug": "20-sort-integers-by-set-bits",
        "title": "Sort Integers by Set Bits",
        "difficulty": "Easy",
        "subtopic": "Counting Bits",
        "companies": ["Amazon", "Goldman Sachs", "Bloomberg"],
        "desc": "Given an integer array `arr` of non-negative integers, sort the integers in ascending order by the number of `1`s in their binary representation. If two or more integers have the same number of set bits, sort them in ascending order of their numeric value. Return the sorted array.",
        "cons": [
            "1 <= arr.length <= 1000",
            "0 <= arr[i] <= 10^5"
        ],
        "hints": [
            "Use a composite sort key `(popcount(x), x)` for each element.",
            "Since `x <= 10^5 < 2^17`, you can even pack `(popcount(x) << 20) | x` into a single 32-bit integer to sort primitives in-place."
        ],
        "explanations": [
            "0 has 0 set bits; [1,2,4,8] have 1 set bit; [3,5,6] have 2 set bits; 7 has 3 set bits.",
            "Every power of two has exactly 1 set bit, so ties are broken in ascending numeric order.",
            "0 has 0 set bits, 1 has 1, 3 has 2, and 7 has 3."
        ],
        "time": "O(n log n)",
        "space": "O(n)",
        "method": "sortBySetBits",
        "params": [("arr", "int[]")],
        "ret": "int[]",
        "py": """        return sorted(arr, key=lambda x: (x.bit_count(), x))""",
        "java": """        int n = arr.length;
        int[] packed = new int[n];
        for (int i = 0; i < n; i++) {
            packed[i] = (Integer.bitCount(arr[i]) << 20) | arr[i];
        }
        Arrays.sort(packed);
        for (int i = 0; i < n; i++) {
            packed[i] &= 0xFFFFF;
        }
        return packed;""",
        "visible": [
            {"arr": [0, 1, 2, 3, 4, 5, 6, 7, 8]},
            {"arr": [1024, 512, 256, 128, 64, 32, 16, 8, 4, 2, 1]},
            {"arr": [7, 3, 1, 0]},
        ],
        "hidden": [
            {"arr": [0]},
            {"arr": [100000, 99999, 65535, 65536, 0]},
            {"arr": [5, 5, 3, 3, 1, 1]},
            {"arr": [15, 14, 13, 12, 11, 10, 9, 8]},
            {"arr": [31, 15, 7, 3, 1, 63, 127]},
            {"arr": [10, 100, 1000, 10000, 100000]},
            {"arr": [42, 21, 85, 170, 341, 682]},
            {"arr": [i for i in range(50, -1, -1)]},
            {"arr": [(i * 9973) % 100001 for i in range(1000)]},
        ],
    },
    {
        "slug": "21-prime-number-of-set-bits",
        "title": "Prime Number of Set Bits",
        "difficulty": "Easy",
        "subtopic": "Counting Bits",
        "companies": ["Amazon", "Adobe", "LinkedIn"],
        "desc": "Given two positive integers `left` and `right`, return the count of integers in the inclusive range `[left, right]` whose binary representation has a prime number of set bits (`1`s). Recall that `1` is not a prime number.",
        "cons": [
            "1 <= left <= right <= 10^6",
            "0 <= right - left <= 10^4"
        ],
        "hints": [
            "Since `right <= 10^6 < 2^20`, the number of set bits in any value is at most 20.",
            "Encode all primes up to 20 (`2, 3, 5, 7, 11, 13, 17, 19`) in a single bitmask `665772` and test `(665772 >> popcount(x)) & 1` in O(1) time."
        ],
        "explanations": [
            "In [6, 10], set-bit counts are 6->2(prime), 7->3(prime), 8->1, 9->2(prime), 10->2(prime), totaling 4.",
            "In [10, 15], set-bit counts are 10->2, 11->3, 12->2, 13->3, 14->3, 15->4; five of them are prime.",
            "1 has 1 set bit, which is not prime, so the count is 0."
        ],
        "time": "O(right - left)",
        "space": "O(1)",
        "method": "countPrimeSetBits",
        "params": [("left", "int"), ("right", "int")],
        "ret": "int",
        "py": """        prime_mask = 665772
        ans = 0
        for x in range(left, right + 1):
            if (prime_mask >> x.bit_count()) & 1:
                ans += 1
        return ans""",
        "java": """        int primeMask = 665772;
        int ans = 0;
        for (int x = left; x <= right; x++) {
            if (((primeMask >>> Integer.bitCount(x)) & 1) == 1) {
                ans++;
            }
        }
        return ans;""",
        "visible": [
            {"left": 6, "right": 10},
            {"left": 10, "right": 15},
            {"left": 1, "right": 1},
        ],
        "hidden": [
            {"left": 1, "right": 2},
            {"left": 3, "right": 3},
            {"left": 8, "right": 8},
            {"left": 15, "right": 16},
            {"left": 1, "right": 100},
            {"left": 999990, "right": 1000000},
            {"left": 524287, "right": 524289},
            {"left": 842, "right": 888},
            {"left": 990000, "right": 1000000},
        ],
    },
    {
        "slug": "22-alternating-bits-check",
        "title": "Alternating Bits Check",
        "difficulty": "Easy",
        "subtopic": "Counting Bits",
        "companies": ["Apple", "Microsoft", "Atlassian"],
        "desc": "Given a positive integer `n`, return `true` if its binary representation has alternating bits — meaning no two adjacent bits have the same value — and `false` otherwise. Leading zeros above the most significant set bit are ignored.",
        "cons": ["1 <= n <= 2^31 - 1"],
        "hints": [
            "What happens when you XOR `n` with `n >> 1` if all adjacent bits of `n` are different?",
            "Every bit up to the MSB becomes `1`, which holds if and only if `(x & (x + 1)) == 0` where `x = n ^ (n >> 1)`."
        ],
        "explanations": [
            "5 in binary is 101, which strictly alternates.",
            "7 in binary is 111, which has adjacent 1s.",
            "11 in binary is 1011, which has adjacent 1s at the lowest two bits."
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "hasAlternatingBits",
        "params": [("n", "int")],
        "ret": "boolean",
        "py": """        x = n ^ (n >> 1)
        return (x & (x + 1)) == 0""",
        "java": """        long x = (long) n ^ (n >>> 1);
        return (x & (x + 1)) == 0;""",
        "visible": [
            {"n": 5},
            {"n": 7},
            {"n": 11},
        ],
        "hidden": [
            {"n": 1},
            {"n": 2},
            {"n": 3},
            {"n": 4},
            {"n": 10},
            {"n": 21},
            {"n": 1431655765},
            {"n": 1431655764},
            {"n": 2147483647},
        ],
    },
    {
        "slug": "23-minimum-one-bit-operations",
        "title": "Minimum One Bit Operations",
        "difficulty": "Hard",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Meta", "Amazon"],
        "desc": "Given a non-negative integer `n`, you may transform it into `0` using two operations any number of times: (1) change the rightmost bit (bit `0`), or (2) change bit `i` (`i > 0`) if bit `i - 1` is `1` and all bits from `0` through `i - 2` are `0`. Return the minimum number of operations needed to reduce `n` to `0`.",
        "cons": ["0 <= n <= 10^9"],
        "hints": [
            "The sequence of states visited when reducing `2^k` to `0` is the reflected binary Gray code, taking `2^(k + 1) - 1` steps.",
            "The minimum steps from any `n` to `0` is the inverse Gray code of `n`, computed by repeatedly XORing `n` with `n >> 1` down to `0`."
        ],
        "explanations": [
            "3 (11) -> 2 (10) -> 0 (00) takes 2 operations.",
            "6 (110) -> 7 (111) -> 5 (101) -> 4 (100) -> 0 (000) takes 4 operations.",
            "0 is already zero, so 0 operations are needed."
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "minimumOneBitOperations",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        ans = 0
        while n > 0:
            ans ^= n
            n >>= 1
        return ans""",
        "java": """        int ans = 0;
        while (n > 0) {
            ans ^= n;
            n >>>= 1;
        }
        return ans;""",
        "visible": [
            {"n": 3},
            {"n": 6},
            {"n": 0},
        ],
        "hidden": [
            {"n": 1},
            {"n": 2},
            {"n": 4},
            {"n": 9},
            {"n": 333},
            {"n": 1024},
            {"n": 65535},
            {"n": 536870912},
            {"n": 1000000000},
        ],
    },
    {
        "slug": "24-maximum-product-of-word-lengths",
        "title": "Maximum Product of Word Lengths",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": "Given an array of lowercase English strings `words`, return the maximum value of `words[i].length * words[j].length` over all pairs `(i, j)` such that `words[i]` and `words[j]` share no common letters. If no two words are letter-disjoint, return `0`.",
        "cons": [
            "2 <= words.length <= 1000",
            "1 <= words[i].length <= 1000",
            "words[i] consists only of lowercase English letters."
        ],
        "hints": [
            "Represent the character set of each word as a 26-bit integer mask; two words share no letters if and only if `(mask1 & mask2) == 0`.",
            "Deduplicate identical masks by keeping only the longest word length for each mask before checking pairs."
        ],
        "explanations": [
            "\"abcw\" (length 4) and \"xtfn\" (length 4) share no letters, giving 4 * 4 = 16.",
            "\"ab\" (length 2) and \"cd\" (length 2) share no letters, giving 2 * 2 = 4.",
            "Every pair shares at least the letter 'a', so no disjoint pair exists and the answer is 0."
        ],
        "time": "O(L + m^2)",
        "space": "O(m)",
        "method": "maxWordLengthProduct",
        "params": [("words", "String[]")],
        "ret": "int",
        "py": """        best_len = {}
        for w in words:
            mask = 0
            for ch in w:
                mask |= 1 << (ord(ch) - 97)
            if len(w) > best_len.get(mask, 0):
                best_len[mask] = len(w)
        items = list(best_len.items())
        ans = 0
        for i in range(len(items)):
            m1, l1 = items[i]
            for j in range(i + 1, len(items)):
                m2, l2 = items[j]
                if (m1 & m2) == 0 and l1 * l2 > ans:
                    ans = l1 * l2
        return ans""",
        "java": """        Map<Integer, Integer> bestLen = new HashMap<>();
        for (String w : words) {
            int mask = 0;
            for (int i = 0; i < w.length(); i++) {
                mask |= 1 << (w.charAt(i) - 'a');
            }
            bestLen.merge(mask, w.length(), Math::max);
        }
        int m = bestLen.size();
        int[] masks = new int[m];
        int[] lens = new int[m];
        int idx = 0;
        for (Map.Entry<Integer, Integer> e : bestLen.entrySet()) {
            masks[idx] = e.getKey();
            lens[idx] = e.getValue();
            idx++;
        }
        int ans = 0;
        for (int i = 0; i < m; i++) {
            for (int j = i + 1; j < m; j++) {
                if ((masks[i] & masks[j]) == 0) {
                    int prod = lens[i] * lens[j];
                    if (prod > ans) ans = prod;
                }
            }
        }
        return ans;""",
        "visible": [
            {"words": ["abcw", "baz", "foo", "bar", "xtfn", "abcdef"]},
            {"words": ["a", "ab", "abc", "d", "cd", "bcd", "abcd"]},
            {"words": ["a", "aa", "aaa", "aaaa"]},
        ],
        "hidden": [
            {"words": ["a", "b"]},
            {"words": ["ab", "ba"]},
            {"words": ["abcdefghijklm", "nopqrstuvwxyz"]},
            {"words": ["eae", "ea", "aaf", "bda", "fcf", "dc", "ac", "ce", "cefde", "dabae"]},
            {"words": ["zzzzzz", "yyyyy", "z", "y", "zy"]},
            {"words": ["quick", "brown", "fox", "jumps", "over", "lazy", "dog"]},
            {"words": ["abc", "def", "ghi", "abcdef", "ghijkl"]},
            {"words": ["a" * 50, "b" * 40, "ab" * 30]},
            {
                "words": [
                    chr(97 + (i % 26)) * ((i % 15) + 1) + chr(97 + ((i * 7) % 26))
                    for i in range(250)
                ]
            },
        ],
    },
    {
        "slug": "25-bitwise-ors-of-subarrays",
        "title": "Bitwise ORs of Subarrays",
        "difficulty": "Medium",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": "Given an integer array `arr` of non-negative integers, consider the bitwise OR of every non-empty contiguous subarray `arr[i..j]` (`0 <= i <= j < arr.length`). Return the number of distinct bitwise OR results across all subarrays.",
        "cons": [
            "1 <= arr.length <= 5 * 10^4",
            "0 <= arr[i] <= 10^9"
        ],
        "hints": [
            "Maintain the set `cur` of all distinct bitwise ORs of subarrays ending at the current index `j`.",
            "As a subarray extends leftward, its bitwise OR can only turn `0` bits into `1` bits, so `cur` holds at most 32 distinct values at any step."
        ],
        "explanations": [
            "The only non-empty subarray is [0], giving 1 distinct value: {0}.",
            "Subarrays give ORs 1, 1, 2, 1|1=1, 1|2=3, 1|1|2=3 -> 3 distinct values: {1, 2, 3}.",
            "The distinct subarray ORs are {1, 2, 3, 4, 6, 7}, totaling 6."
        ],
        "time": "O(n log M)",
        "space": "O(n log M)",
        "method": "subarrayBitwiseORs",
        "params": [("arr", "int[]")],
        "ret": "int",
        "py": """        ans = set()
        cur = set()
        for x in arr:
            cur = {x | y for y in cur}
            cur.add(x)
            ans.update(cur)
        return len(ans)""",
        "java": """        Set<Integer> ans = new HashSet<>();
        Set<Integer> cur = new HashSet<>();
        for (int x : arr) {
            Set<Integer> nxt = new HashSet<>();
            nxt.add(x);
            for (int y : cur) {
                nxt.add(x | y);
            }
            cur = nxt;
            ans.addAll(cur);
        }
        return ans.size();""",
        "visible": [
            {"arr": [0]},
            {"arr": [1, 1, 2]},
            {"arr": [1, 2, 4]},
        ],
        "hidden": [
            {"arr": [5, 5, 5, 5]},
            {"arr": [0, 0, 0, 1, 0, 0]},
            {"arr": [1, 2, 4, 8, 16, 32]},
            {"arr": [3, 6, 12, 24, 48]},
            {"arr": [7, 1, 2, 4, 0, 8]},
            {"arr": [1000000000, 500000000, 250000000, 125000000]},
            {"arr": [15, 7, 3, 1, 0]},
            {"arr": [(1 << (i % 15)) for i in range(60)]},
            {"arr": [(i * 1103515245 + 12345) % 1000000001 for i in range(1500)]},
        ],
    },
    {
        "slug": "26-count-total-set-bits-to-n",
        "title": "Count Total Set Bits to N",
        "difficulty": "Hard",
        "subtopic": "Counting Bits",
        "companies": ["Google", "Amazon", "Goldman Sachs"],
        "desc": "Given a non-negative 64-bit integer `n`, return the total number of set bits (`1`s) across the binary representations of all integers from `0` to `n` inclusive.",
        "cons": ["0 <= n <= 10^15"],
        "hints": [
            "In the sequence `0, 1, 2, ..., n`, bit position `b` repeats a periodic pattern of `2^b` zeros followed by `2^b` ones (period `2^(b + 1)`).",
            "For each bit `b` with `2^b <= n`, count full cycles in `m = n + 1` plus the partial remainder `max(0, (m % 2^(b + 1)) - 2^b)`."
        ],
        "explanations": [
            "Binary forms for 0..3 are 0, 1, 10, 11 -> 0 + 1 + 1 + 2 = 4 set bits.",
            "Binary forms for 0..5 add 100 (1) and 101 (2) to 4, totaling 7 set bits.",
            "0 has 0 set bits."
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "countTotalSetBits",
        "params": [("n", "long")],
        "ret": "long",
        "py": """        m = n + 1
        total = 0
        half = 1
        while half <= n:
            cycle = half << 1
            total += (m // cycle) * half
            rem = m % cycle
            if rem > half:
                total += rem - half
            half = cycle
        return total""",
        "java": """        long m = n + 1;
        long total = 0;
        long half = 1;
        while (half <= n) {
            long cycle = half << 1;
            total += (m / cycle) * half;
            long rem = m % cycle;
            if (rem > half) {
                total += rem - half;
            }
            half = cycle;
        }
        return total;""",
        "visible": [
            {"n": 3},
            {"n": 5},
            {"n": 0},
        ],
        "hidden": [
            {"n": 1},
            {"n": 2},
            {"n": 7},
            {"n": 8},
            {"n": 15},
            {"n": 100},
            {"n": 1000000},
            {"n": 1099511627775},
            {"n": 1000000000000000},
        ],
    },

    # ------------------------------------------------------------------
    # 27-33: Two Complement
    # ------------------------------------------------------------------
    {
        "slug": "27-number-complement",
        "title": "Number Complement",
        "difficulty": "Easy",
        "subtopic": "Two Complement",
        "companies": ["Apple", "Amazon", "Salesforce"],
        "desc": "The complement of a positive integer is the integer you get when you flip all the `0`s to `1`s and all the `1`s to `0`s in its binary representation, starting from its most significant set bit down to bit `0` (ignoring leading zeros). Given a positive integer `num`, return its complement.",
        "cons": ["1 <= num <= 2^31 - 1"],
        "hints": [
            "Construct a bitmask consisting of all `1`s with the exact same bit length as `num`.",
            "XOR `num` with that mask (`((1 << bit_length) - 1) ^ num`), being careful not to overflow signed 32-bit integers."
        ],
        "explanations": [
            "5 is 101 in binary; flipping every bit gives 010, which is 2.",
            "1 is 1 in binary; flipping it gives 0.",
            "7 is 111 in binary; flipping all bits gives 000, which is 0."
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "findComplement",
        "params": [("num", "int")],
        "ret": "int",
        "py": """        mask = (1 << num.bit_length()) - 1
        return num ^ mask""",
        "java": """        long mask = ((long) Integer.highestOneBit(num) << 1) - 1;
        return (int) (num ^ mask);""",
        "visible": [
            {"num": 5},
            {"num": 1},
            {"num": 7},
        ],
        "hidden": [
            {"num": 2},
            {"num": 4},
            {"num": 10},
            {"num": 16},
            {"num": 1023},
            {"num": 1024},
            {"num": 1431655765},
            {"num": 2147483646},
            {"num": 2147483647},
        ],
    },
    {
        "slug": "28-power-of-four",
        "title": "Power of Four",
        "difficulty": "Easy",
        "subtopic": "Two Complement",
        "companies": ["Google", "Amazon", "Apple"],
        "desc": "Given a 32-bit signed integer `n`, return `true` if it is a power of four (that is, there exists an integer `x >= 0` such that `n == 4^x`), and `false` otherwise. Solve it in O(1) time without loops or recursion.",
        "cons": ["-2^31 <= n <= 2^31 - 1"],
        "hints": [
            "First verify `n > 0` and `(n & (n - 1)) == 0` so that `n` is a positive power of two.",
            "A power of two is a power of four if and only if its single set bit sits at an even bit index (0, 2, 4, ...), which can be tested with `0x55555555`."
        ],
        "explanations": [
            "16 = 4^2, so return true.",
            "5 is not a power of four, so return false.",
            "1 = 4^0, so return true."
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "isPowerOfFour",
        "params": [("n", "int")],
        "ret": "boolean",
        "py": """        return n > 0 and (n & (n - 1)) == 0 and (n & 0x55555555) != 0""",
        "java": """        return n > 0 && (n & (n - 1)) == 0 && (n & 0x55555555) != 0;""",
        "visible": [
            {"n": 16},
            {"n": 5},
            {"n": 1},
        ],
        "hidden": [
            {"n": 0},
            {"n": -4},
            {"n": -16},
            {"n": 2},
            {"n": 4},
            {"n": 8},
            {"n": 64},
            {"n": 1073741824},
            {"n": -2147483648},
        ],
    },
    {
        "slug": "29-gray-code-sequence",
        "title": "Gray Code Sequence",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Amazon", "Microsoft", "Apple"],
        "desc": "An `n`-bit Gray code sequence is an ordering of all `2^n` integers in `[0, 2^n - 1]` starting with `0` where consecutive elements (as well as the first and last elements) differ in exactly one binary bit. Given `n`, return the standard reflected binary Gray code sequence defined by `seq[i] = i ^ (i >> 1)` for `0 <= i < 2^n`.",
        "cons": ["1 <= n <= 16"],
        "hints": [
            "Each index `i` maps directly to its reflected binary Gray code via `i ^ (i >> 1)`.",
            "Verify that `i` and `i + 1` differ by a trailing run of `1`s flipping to `0`s plus one carry bit, so `(i ^ (i >> 1))` and `((i + 1) ^ ((i + 1) >> 1))` differ in exactly one bit."
        ],
        "explanations": [
            "For n = 2, the sequence is [00, 01, 11, 10] = [0, 1, 3, 2].",
            "For n = 1, the sequence is [0, 1].",
            "For n = 3, the 8-element reflected binary Gray code is [0, 1, 3, 2, 6, 7, 5, 4]."
        ],
        "time": "O(2^n)",
        "space": "O(2^n)",
        "method": "grayCode",
        "params": [("n", "int")],
        "ret": "int[]",
        "py": """        return [i ^ (i >> 1) for i in range(1 << n)]""",
        "java": """        int size = 1 << n;
        int[] ans = new int[size];
        for (int i = 0; i < size; i++) {
            ans[i] = i ^ (i >> 1);
        }
        return ans;""",
        "visible": [
            {"n": 2},
            {"n": 1},
            {"n": 3},
        ],
        "hidden": [
            {"n": 4},
            {"n": 5},
            {"n": 6},
            {"n": 7},
            {"n": 8},
            {"n": 9},
            {"n": 10},
            {"n": 11},
            {"n": 12},
        ],
    },
    {
        "slug": "30-convert-integer-to-hexadecimal",
        "title": "Convert Integer to Hexadecimal",
        "difficulty": "Easy",
        "subtopic": "Two Complement",
        "companies": ["Meta", "Amazon", "Oracle"],
        "desc": "Given a 32-bit signed integer `num`, return its hexadecimal representation as a lowercase string. For negative integers, use standard 32-bit two's complement representation. The result must contain no leading zeros except when `num` is `0`, which is represented as `\"0\"`.",
        "cons": ["-2^31 <= num <= 2^31 - 1"],
        "hints": [
            "Mask `num` to 32 unsigned bits (`num & 0xFFFFFFFF` in Python, or use unsigned right shift `>>>` in Java).",
            "Repeatedly extract the lowest 4 bits (`n & 0xF`) to map to `'0'-'9'` or `'a'-'f'`, shift right by 4, and reverse the collected digits."
        ],
        "explanations": [
            "26 = 1 * 16 + 10, which is \"1a\" in hexadecimal.",
            "In 32-bit two's complement, -1 has all 32 bits set, giving \"ffffffff\".",
            "0 is represented as \"0\"."
        ],
        "time": "O(1)",
        "space": "O(1)",
        "method": "toHex",
        "params": [("num", "int")],
        "ret": "String",
        "py": """        if num == 0:
            return "0"
        digits = "0123456789abcdef"
        n = num & 0xFFFFFFFF
        out = []
        while n > 0:
            out.append(digits[n & 0xF])
            n >>= 4
        return "".join(reversed(out))""",
        "java": """        if (num == 0) return "0";
        char[] digits = "0123456789abcdef".toCharArray();
        StringBuilder sb = new StringBuilder();
        int n = num;
        while (n != 0) {
            sb.append(digits[n & 0xF]);
            n >>>= 4;
        }
        return sb.reverse().toString();""",
        "visible": [
            {"num": 26},
            {"num": -1},
            {"num": 0},
        ],
        "hidden": [
            {"num": 1},
            {"num": 15},
            {"num": 16},
            {"num": -2},
            {"num": -16},
            {"num": -2147483648},
            {"num": 2147483647},
            {"num": 305419896},
            {"num": -559038737},
        ],
    },
    {
        "slug": "31-utf8-validation",
        "title": "UTF-8 Validation",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": "Given an integer array `data` where only the least significant 8 bits of each element represent a byte, return `true` if `data` forms a valid sequence of UTF-8 characters under the byte-prefix rules, and `false` otherwise. Valid characters use 1 to 4 bytes: 1-byte `0xxxxxxx`; 2-byte `110xxxxx 10xxxxxx`; 3-byte `1110xxxx 10xxxxxx 10xxxxxx`; 4-byte `11110xxx 10xxxxxx 10xxxxxx 10xxxxxx`.",
        "cons": [
            "1 <= data.length <= 2 * 10^4",
            "0 <= data[i] <= 255"
        ],
        "hints": [
            "Maintain a counter `remaining` of how many continuation bytes (`10xxxxxx`) are still expected for the current character.",
            "When `remaining == 0`, inspect the leading bits of `byte & 0xFF` to determine whether the character has 0, 1, 2, or 3 continuation bytes; reject any byte starting with `10` or five or more `1`s."
        ],
        "explanations": [
            "197 (11000101) starts a 2-byte char followed by continuation 130 (10000010), then 1 (00000001) is a 1-byte char.",
            "235 (11101011) expects two continuation bytes, but 4 (00000100) does not start with 10.",
            "240 (11110000) is a 4-byte header followed by three valid 10xxxxxx continuation bytes."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "validUtf8",
        "params": [("data", "int[]")],
        "ret": "boolean",
        "py": """        rem = 0
        for raw in data:
            b = raw & 0xFF
            if rem == 0:
                if (b >> 7) == 0:
                    continue
                elif (b >> 5) == 0b110:
                    rem = 1
                elif (b >> 4) == 0b1110:
                    rem = 2
                elif (b >> 3) == 0b11110:
                    rem = 3
                else:
                    return False
            else:
                if (b >> 6) != 0b10:
                    return False
                rem -= 1
        return rem == 0""",
        "java": """        int rem = 0;
        for (int raw : data) {
            int b = raw & 0xFF;
            if (rem == 0) {
                if ((b >>> 7) == 0) {
                    continue;
                } else if ((b >>> 5) == 0b110) {
                    rem = 1;
                } else if ((b >>> 4) == 0b1110) {
                    rem = 2;
                } else if ((b >>> 3) == 0b11110) {
                    rem = 3;
                } else {
                    return false;
                }
            } else {
                if ((b >>> 6) != 0b10) {
                    return false;
                }
                rem--;
            }
        }
        return rem == 0;""",
        "visible": [
            {"data": [197, 130, 1]},
            {"data": [235, 140, 4]},
            {"data": [240, 162, 138, 147]},
        ],
        "hidden": [
            {"data": [0]},
            {"data": [127]},
            {"data": [128]},
            {"data": [197]},
            {"data": [248, 130, 130, 130, 130]},
            {"data": [255]},
            {"data": [230, 136, 145, 228, 184, 150, 231, 149, 140]},
            {"data": [240, 162, 138, 147, 145]},
            {"data": [197, 130, 235, 140, 130, 65, 240, 159, 152, 128] * 200},
        ],
    },
    {
        "slug": "32-concatenation-of-consecutive-binary",
        "title": "Concatenation of Consecutive Binary",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": "Given a positive integer `n`, return the decimal value of the binary string formed by concatenating the binary representations of all integers from `1` to `n` in order (without leading zeros), modulo `10^9 + 7`.",
        "cons": ["1 <= n <= 10^5"],
        "hints": [
            "Appending the binary representation of `i` (which has bit length `bits`) to the current value `ans` transforms `ans` into `((ans << bits) | i) % (10^9 + 7)`.",
            "The bit length `bits` increases by 1 precisely when `i` is a power of two, i.e., `(i & (i - 1)) == 0`."
        ],
        "explanations": [
            "Binary of 1 is \"1\", which equals 1.",
            "Concatenating 1, 10, 11 gives \"11011\" = 27.",
            "Concatenating 1..12 yields 118505380540, which is 505379714 modulo 10^9 + 7."
        ],
        "time": "O(n)",
        "space": "O(1)",
        "method": "concatenatedBinary",
        "params": [("n", "int")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007
        ans = 0
        bits = 0
        for i in range(1, n + 1):
            if (i & (i - 1)) == 0:
                bits += 1
            ans = ((ans << bits) | i) % MOD
        return ans""",
        "java": """        final long MOD = 1_000_000_007L;
        long ans = 0;
        int bits = 0;
        for (int i = 1; i <= n; i++) {
            if ((i & (i - 1)) == 0) {
                bits++;
            }
            ans = ((ans << bits) | i) % MOD;
        }
        return (int) ans;""",
        "visible": [
            {"n": 1},
            {"n": 3},
            {"n": 12},
        ],
        "hidden": [
            {"n": 2},
            {"n": 4},
            {"n": 7},
            {"n": 8},
            {"n": 42},
            {"n": 100},
            {"n": 1024},
            {"n": 10000},
            {"n": 100000},
        ],
    },
    {
        "slug": "33-base-neg2-representation",
        "title": "Base -2 Representation",
        "difficulty": "Medium",
        "subtopic": "Two Complement",
        "companies": ["Google", "Meta", "Oracle"],
        "desc": "Given a non-negative integer `n`, return a binary string consisting of `'0'` and `'1'` representing `n` in base `-2` (negabinary), where bit position `k` carries weight `(-2)^k`. The returned string must not have leading zeros unless `n == 0` (which returns `\"0\"`).",
        "cons": ["0 <= n <= 10^9"],
        "hints": [
            "At each step, the least significant negabinary digit is `n & 1` (either 0 or 1).",
            "Subtracting that digit and dividing by `-2` is equivalent to `n = -(n >> 1)` using arithmetic right shift."
        ],
        "explanations": [
            "1 * (-2)^2 + 1 * (-2)^1 + 0 * (-2)^0 = 4 - 2 + 0 = 2.",
            "1 * (-2)^2 + 1 * (-2)^1 + 1 * (-2)^0 = 4 - 2 + 1 = 3.",
            "1 * (-2)^2 + 0 * (-2)^1 + 0 * (-2)^0 = 4."
        ],
        "time": "O(log n)",
        "space": "O(log n)",
        "method": "baseNeg2",
        "params": [("n", "int")],
        "ret": "String",
        "py": """        if n == 0:
            return "0"
        bits = []
        while n != 0:
            bits.append("1" if (n & 1) else "0")
            n = -(n >> 1)
        return "".join(reversed(bits))""",
        "java": """        if (n == 0) return "0";
        StringBuilder sb = new StringBuilder();
        while (n != 0) {
            sb.append((n & 1) == 1 ? '1' : '0');
            n = -(n >> 1);
        }
        return sb.reverse().toString();""",
        "visible": [
            {"n": 2},
            {"n": 3},
            {"n": 4},
        ],
        "hidden": [
            {"n": 0},
            {"n": 1},
            {"n": 5},
            {"n": 6},
            {"n": 7},
            {"n": 10},
            {"n": 100},
            {"n": 536870912},
            {"n": 1000000000},
        ],
    },

    # ------------------------------------------------------------------
    # 34-40: Fast Exponentiation
    # ------------------------------------------------------------------
    {
        "slug": "34-modular-exponentiation",
        "title": "Modular Exponentiation",
        "difficulty": "Easy",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Amazon", "Microsoft"],
        "desc": "Given non-negative integers `base` and `exp` and a positive modulus `mod`, compute `(base^exp) % mod` using binary exponentiation. By convention `0^0 = 1`, so when `exp == 0` the result is `1 % mod`.",
        "cons": [
            "0 <= base <= 10^9",
            "0 <= exp <= 10^15",
            "1 <= mod <= 10^9"
        ],
        "hints": [
            "Repeatedly square `base % mod` while shifting `exp` right by 1 bit.",
            "Whenever the lowest bit of `exp` is `1`, multiply the running answer by the current base power modulo `mod`; initialize the answer to `1 % mod` to handle `mod == 1`."
        ],
        "explanations": [
            "2^10 = 1024, and 1024 % 1000 = 24.",
            "3^0 = 1, and 1 % 7 = 1.",
            "Any integer modulo 1 is 0."
        ],
        "time": "O(log exp)",
        "space": "O(1)",
        "method": "modPow",
        "params": [("base", "long"), ("exp", "long"), ("mod", "long")],
        "ret": "long",
        "py": """        res = 1 % mod
        b = base % mod
        e = exp
        while e > 0:
            if e & 1:
                res = (res * b) % mod
            b = (b * b) % mod
            e >>= 1
        return res""",
        "java": """        long res = 1 % mod;
        long b = base % mod;
        long e = exp;
        while (e > 0) {
            if ((e & 1L) == 1L) {
                res = (res * b) % mod;
            }
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;""",
        "visible": [
            {"base": 2, "exp": 10, "mod": 1000},
            {"base": 3, "exp": 0, "mod": 7},
            {"base": 5, "exp": 123, "mod": 1},
        ],
        "hidden": [
            {"base": 0, "exp": 0, "mod": 10},
            {"base": 0, "exp": 0, "mod": 1},
            {"base": 0, "exp": 1000000000000, "mod": 1000000007},
            {"base": 1, "exp": 1000000000000000, "mod": 998244353},
            {"base": 2, "exp": 1000000000000000, "mod": 1000000000},
            {"base": 999999937, "exp": 999999936, "mod": 999999937},
            {"base": 123456789, "exp": 987654321012345, "mod": 1000000000},
            {"base": 1000000000, "exp": 1000000000000000, "mod": 999999937},
            {"base": 7, "exp": 1000000000000000, "mod": 998244353},
        ],
    },
    {
        "slug": "35-super-pow",
        "title": "Super Pow",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Amazon", "Google", "Bloomberg"],
        "desc": "Given a positive integer `a` and a very large positive integer `b` represented as an array of decimal digits (most significant digit first, with no leading zeros), compute `a^b mod 1337`.",
        "cons": [
            "1 <= a <= 2^31 - 1",
            "1 <= b.length <= 2000",
            "0 <= b[i] <= 9",
            "b does not contain leading zeros and represents a positive integer."
        ],
        "hints": [
            "Use the exponent identity `a^(10 * q + d) = (a^q)^10 * a^d (mod 1337)` to process `b` one decimal digit at a time from left to right.",
            "Reduce `a` modulo `1337` upfront and evaluate each small power (`^10` and `^d`) with modular binary exponentiation."
        ],
        "explanations": [
            "2^3 mod 1337 = 8.",
            "2^10 mod 1337 = 1024.",
            "1^433852 mod 1337 = 1."
        ],
        "time": "O(b.length)",
        "space": "O(1)",
        "method": "superPow",
        "params": [("a", "int"), ("b", "int[]")],
        "ret": "int",
        "py": """        MOD = 1337
        base = a % MOD
        ans = 1
        for d in b:
            ans = (pow(ans, 10, MOD) * pow(base, d, MOD)) % MOD
        return ans""",
        "java": """        final int MOD = 1337;
        int base = a % MOD;
        int ans = 1;
        for (int d : b) {
            int p10 = 1;
            int cur = ans;
            int e = 10;
            while (e > 0) {
                if ((e & 1) == 1) p10 = (p10 * cur) % MOD;
                cur = (cur * cur) % MOD;
                e >>= 1;
            }
            int pd = 1;
            cur = base;
            e = d;
            while (e > 0) {
                if ((e & 1) == 1) pd = (pd * cur) % MOD;
                cur = (cur * cur) % MOD;
                e >>= 1;
            }
            ans = (p10 * pd) % MOD;
        }
        return ans;""",
        "visible": [
            {"a": 2, "b": [3]},
            {"a": 2, "b": [1, 0]},
            {"a": 1, "b": [4, 3, 3, 8, 5, 2]},
        ],
        "hidden": [
            {"a": 2147483647, "b": [2, 0, 0]},
            {"a": 1337, "b": [9, 9, 9]},
            {"a": 1338, "b": [1, 2, 3, 4, 5]},
            {"a": 7, "b": [1, 1, 4, 0]},
            {"a": 191, "b": [5, 0, 0, 0]},
            {"a": 999999999, "b": [1]},
            {"a": 3, "b": [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]},
            {"a": 42, "b": [1] + [0] * 100},
            {"a": 78267, "b": [(i * 7 + 3) % 10 for i in range(1500)]},
        ],
    },
    {
        "slug": "36-count-good-digit-strings",
        "title": "Count Good Digit Strings",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Amazon", "Google", "Goldman Sachs"],
        "desc": "A digit string of length `n` (which may have leading zeros) is called good if every digit at an even 0-based index is an even digit (`0, 2, 4, 6, 8`) and every digit at an odd 0-based index is a prime digit (`2, 3, 5, 7`). Given `n`, return the total number of good digit strings of length `n` modulo `10^9 + 7`.",
        "cons": ["1 <= n <= 10^15"],
        "hints": [
            "Positions are independent: there are `ceil(n / 2) = (n + 1) // 2` even indices (5 choices each) and `floor(n / 2) = n // 2` odd indices (4 choices each).",
            "Compute `5^((n + 1) // 2) * 4^(n // 2) mod (10^9 + 7)` using binary exponentiation."
        ],
        "explanations": [
            "For n = 1, only index 0 exists (even index), giving 5 choices: 0, 2, 4, 6, 8.",
            "For n = 4, there are 2 even indices and 2 odd indices, giving 5^2 * 4^2 = 400.",
            "For n = 50, 5^25 * 4^25 mod (10^9 + 7) = 564908303."
        ],
        "time": "O(log n)",
        "space": "O(1)",
        "method": "countGoodDigitStrings",
        "params": [("n", "long")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007
        even_cnt = (n + 1) // 2
        odd_cnt = n // 2
        return (pow(5, even_cnt, MOD) * pow(4, odd_cnt, MOD)) % MOD""",
        "java": """        final long MOD = 1_000_000_007L;
        long evenCnt = (n + 1) / 2;
        long oddCnt = n / 2;
        return (int) ((modPow(5L, evenCnt, MOD) * modPow(4L, oddCnt, MOD)) % MOD);
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1;
        long b = base % mod;
        long e = exp;
        while (e > 0) {
            if ((e & 1L) == 1L) res = (res * b) % mod;
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;""",
        "visible": [
            {"n": 1},
            {"n": 4},
            {"n": 50},
        ],
        "hidden": [
            {"n": 2},
            {"n": 3},
            {"n": 5},
            {"n": 10},
            {"n": 100},
            {"n": 1000000},
            {"n": 1000000007},
            {"n": 999999999999999},
            {"n": 1000000000000000},
        ],
    },
    {
        "slug": "37-nth-fibonacci-modulo",
        "title": "Nth Fibonacci Number Modulo",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Meta", "Microsoft"],
        "desc": "The Fibonacci sequence is defined by `F(0) = 0`, `F(1) = 1`, and `F(n) = F(n - 1) + F(n - 2)` for `n >= 2`. Given a non-negative integer `n` up to `10^15`, return `F(n) mod (10^9 + 7)` in `O(log n)` time.",
        "cons": ["0 <= n <= 10^15"],
        "hints": [
            "Express the recurrence as a 2x2 matrix power `[[1, 1], [1, 0]]^n`, or use the fast doubling identities `F(2k) = F(k) * (2*F(k + 1) - F(k))` and `F(2k + 1) = F(k)^2 + F(k + 1)^2`.",
            "Keep intermediate values modulo `10^9 + 7` using 64-bit integers and handle subtraction cleanly so remainders stay non-negative."
        ],
        "explanations": [
            "F(0) = 0 by definition.",
            "F(10) = 55.",
            "F(50) = 12586269025, which equals 586268941 modulo 10^9 + 7."
        ],
        "time": "O(log n)",
        "space": "O(log n)",
        "method": "fibonacciMod",
        "params": [("n", "long")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007

        def fib(k: int) -> tuple[int, int]:
            if k == 0:
                return (0, 1)
            a, b = fib(k >> 1)
            c = a * ((2 * b - a) % MOD) % MOD
            d = (a * a + b * b) % MOD
            if k & 1:
                return (d, (c + d) % MOD)
            return (c, d)

        return fib(n)[0]""",
        "java": """        return (int) fib(n)[0];
    }

    private long[] fib(long k) {
        final long MOD = 1_000_000_007L;
        if (k == 0) return new long[]{0L, 1L};
        long[] p = fib(k >> 1);
        long a = p[0], b = p[1];
        long twoBMinusA = ((2 * b - a) % MOD + MOD) % MOD;
        long c = (a * twoBMinusA) % MOD;
        long d = (a * a + b * b) % MOD;
        if ((k & 1L) == 1L) {
            return new long[]{d, (c + d) % MOD};
        }
        return new long[]{c, d};""",
        "visible": [
            {"n": 0},
            {"n": 10},
            {"n": 50},
        ],
        "hidden": [
            {"n": 1},
            {"n": 2},
            {"n": 3},
            {"n": 20},
            {"n": 100},
            {"n": 1000000},
            {"n": 1000000007},
            {"n": 999999999999999},
            {"n": 1000000000000000},
        ],
    },
    {
        "slug": "38-minimum-non-zero-product",
        "title": "Minimum Non-Zero Product",
        "difficulty": "Medium",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Amazon", "Bloomberg"],
        "desc": "Given a positive integer `p`, consider the array `nums = [1, 2, ..., 2^p - 1]` containing every positive `p`-bit integer. In one operation you may choose two elements of `nums` and swap their bits at any single bit position. Return the minimum possible non-zero product of all elements of `nums` after any number of operations, modulo `10^9 + 7`.",
        "cons": ["1 <= p <= 60"],
        "hints": [
            "Swapping bits preserves the sum of the two chosen numbers while minimizing their product when pushed as far apart as possible (while remaining >= 1).",
            "Pair every complementary pair `(x, (2^p - 1) - x)` into `(1, 2^p - 2)`, leaving one unpaired `2^p - 1`; the minimum product is `(2^p - 1) * (2^p - 2)^(2^(p - 1) - 1) mod (10^9 + 7)`."
        ],
        "explanations": [
            "For p = 1, nums = [1] and the product is 1.",
            "For p = 2, nums = [1, 2, 3] already minimizes the non-zero product at 1 * 2 * 3 = 6.",
            "For p = 3, pairing gives [1, 1, 1, 6, 6, 6, 7], whose product is 6^3 * 7 = 1512."
        ],
        "time": "O(p)",
        "space": "O(1)",
        "method": "minNonZeroProduct",
        "params": [("p", "int")],
        "ret": "int",
        "py": """        MOD = 1_000_000_007
        max_val = (1 << p) - 1
        pair_base = (max_val - 1) % MOD
        pair_cnt = (1 << (p - 1)) - 1
        return ((max_val % MOD) * pow(pair_base, pair_cnt, MOD)) % MOD""",
        "java": """        final long MOD = 1_000_000_007L;
        long maxVal = (1L << p) - 1L;
        long pairBase = (maxVal - 1L) % MOD;
        long pairCnt = (1L << (p - 1)) - 1L;
        long res = 1L;
        long b = pairBase;
        long e = pairCnt;
        while (e > 0) {
            if ((e & 1L) == 1L) res = (res * b) % MOD;
            b = (b * b) % MOD;
            e >>= 1;
        }
        return (int) (((maxVal % MOD) * res) % MOD);""",
        "visible": [
            {"p": 1},
            {"p": 2},
            {"p": 3},
        ],
        "hidden": [
            {"p": 4},
            {"p": 5},
            {"p": 10},
            {"p": 20},
            {"p": 30},
            {"p": 31},
            {"p": 45},
            {"p": 59},
            {"p": 60},
        ],
    },
    {
        "slug": "39-ways-to-make-array-with-product",
        "title": "Ways to Make Array With Product",
        "difficulty": "Hard",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Meta", "Goldman Sachs"],
        "desc": "You are given a 2D integer array `queries` where `queries[i] = [n, k]`. For each query, return the number of different arrays of length `n` consisting of positive integers whose elements multiply to `k`, modulo `10^9 + 7`. Two arrays are different if they differ at any index.",
        "cons": [
            "1 <= queries.length <= 10^4",
            "1 <= n, k <= 10^4"
        ],
        "hints": [
            "Factorize `k = p1^e1 * p2^e2 * ... * pr^er`. Distributing `e` identical copies of a prime into `n` distinct positions can be done in `C(n + e - 1, e)` ways (stars and bars), independently for each prime.",
            "Precompute factorials up to `max(n) + 14` and their modular inverses via Fermat's Little Theorem (`fact[M]^(MOD - 2) mod MOD`) using fast exponentiation, plus a smallest-prime-factor sieve for O(log k) factorization per query."
        ],
        "explanations": [
            "[2, 6]: [1,6],[6,1],[2,3],[3,2] -> 4; [5, 1]: only [1,1,1,1,1] -> 1; [73, 660]: 660 = 2^2 * 3 * 5 * 11 gives 50734910.",
            "Any array of length 1 multiplying to k must be [k], giving 1 way for every query.",
            "4 = 2^2 gives C(3+2-1, 2) = 6 ways; 8 = 2^3 gives C(2+3-1, 3) = 4 ways."
        ],
        "time": "O(M + Q log K)",
        "space": "O(M)",
        "method": "waysToFillArray",
        "params": [("queries", "int[][]")],
        "ret": "int[]",
        "py": """        MOD = 1_000_000_007
        max_n = max(q[0] for q in queries)
        max_k = max(q[1] for q in queries)
        limit = max_n + 15

        fact = [1] * (limit + 1)
        for i in range(1, limit + 1):
            fact[i] = (fact[i - 1] * i) % MOD
        inv_fact = [1] * (limit + 1)
        inv_fact[limit] = pow(fact[limit], MOD - 2, MOD)
        for i in range(limit, 0, -1):
            inv_fact[i - 1] = (inv_fact[i] * i) % MOD

        spf = list(range(max_k + 1))
        p = 2
        while p * p <= max_k:
            if spf[p] == p:
                for m in range(p * p, max_k + 1, p):
                    if spf[m] == m:
                        spf[m] = p
            p += 1

        ans = []
        for n, k in queries:
            ways = 1
            x = k
            while x > 1:
                prime = spf[x]
                exp = 0
                while x % prime == 0:
                    x //= prime
                    exp += 1
                comb = fact[n + exp - 1] * inv_fact[exp] % MOD * inv_fact[n - 1] % MOD
                ways = (ways * comb) % MOD
            ans.append(ways)
        return ans""",
        "java": """        final long MOD = 1_000_000_007L;
        int maxN = 1, maxK = 1;
        for (int[] q : queries) {
            if (q[0] > maxN) maxN = q[0];
            if (q[1] > maxK) maxK = q[1];
        }
        int limit = maxN + 15;
        long[] fact = new long[limit + 1];
        fact[0] = 1;
        for (int i = 1; i <= limit; i++) {
            fact[i] = (fact[i - 1] * i) % MOD;
        }
        long[] invFact = new long[limit + 1];
        invFact[limit] = modPow(fact[limit], MOD - 2, MOD);
        for (int i = limit; i >= 1; i--) {
            invFact[i - 1] = (invFact[i] * i) % MOD;
        }

        int[] spf = new int[maxK + 1];
        for (int i = 0; i <= maxK; i++) spf[i] = i;
        for (int p = 2; p * p <= maxK; p++) {
            if (spf[p] == p) {
                for (int m = p * p; m <= maxK; m += p) {
                    if (spf[m] == m) spf[m] = p;
                }
            }
        }

        int[] ans = new int[queries.length];
        for (int i = 0; i < queries.length; i++) {
            int n = queries[i][0], x = queries[i][1];
            long ways = 1;
            while (x > 1) {
                int prime = spf[x];
                int exp = 0;
                while (x % prime == 0) {
                    x /= prime;
                    exp++;
                }
                long comb = fact[n + exp - 1] * invFact[exp] % MOD * invFact[n - 1] % MOD;
                ways = (ways * comb) % MOD;
            }
            ans[i] = (int) ways;
        }
        return ans;
    }

    private long modPow(long base, long exp, long mod) {
        long res = 1;
        long b = base % mod;
        long e = exp;
        while (e > 0) {
            if ((e & 1L) == 1L) res = (res * b) % mod;
            b = (b * b) % mod;
            e >>= 1;
        }
        return res;""",
        "visible": [
            {"queries": [[2, 6], [5, 1], [73, 660]]},
            {"queries": [[1, 1], [1, 2], [1, 100]]},
            {"queries": [[3, 4], [2, 8]]},
        ],
        "hidden": [
            {"queries": [[1, 1]]},
            {"queries": [[10000, 1], [1, 10000], [10000, 10000]]},
            {"queries": [[2, 2], [2, 3], [2, 4], [2, 16], [2, 36]]},
            {"queries": [[10, 8192], [10, 7560], [10, 9973]]},
            {"queries": [[100, 2310], [500, 5040], [1000, 9240]]},
            {"queries": [[50, 9999], [50, 9998], [50, 9997], [50, 9996]]},
            {"queries": [[9999, 8192], [9999, 7560], [9999, 9240]]},
            {"queries": [[i, i * 12] for i in range(1, 51)]},
            {"queries": [[(i * 97) % 10000 + 1, (i * 193) % 10000 + 1] for i in range(500)]},
        ],
    },
    {
        "slug": "40-smallest-good-base",
        "title": "Smallest Good Base",
        "difficulty": "Hard",
        "subtopic": "Fast Exponentiation",
        "companies": ["Google", "Meta", "Uber"],
        "desc": "Given a decimal integer `n` represented as a string (`3 <= n <= 10^18`), return the smallest good base `k` (`k >= 2`) as a string. An integer `k >= 2` is called a good base of `n` if every digit of `n` when written in base `k` is `1` (meaning `n = 1 + k + k^2 + ... + k^m` for some integer `m >= 1`).",
        "cons": [
            "n is a decimal integer string in the range [3, 10^18].",
            "n does not contain leading zeros."
        ],
        "hints": [
            "A smaller base `k` corresponds to more `1`-digits `m + 1`, so test `m` from `floor(log2(n))` down to `2`; the first valid base found is guaranteed to be the smallest (otherwise `m = 1` gives `k = n - 1`).",
            "For each fixed `m`, binary search `k` in `[2, n - 1]` and evaluate `1 + k + ... + k^m` with overflow-safe checks (`term > (n - sum) // k`) to avoid 64-bit integer overflow."
        ],
        "explanations": [
            "13 in base 3 is 111 (1 + 3 + 9 = 13), so 3 is the smallest good base.",
            "4681 in base 8 is 11111 (1 + 8 + 64 + 512 + 4096 = 4681).",
            "10^18 has no good base with 3 or more digits, so its smallest good base is 10^18 - 1 (giving \"11\")."
        ],
        "time": "O((log n)^3)",
        "space": "O(1)",
        "method": "smallestGoodBase",
        "params": [("n", "String")],
        "ret": "String",
        "py": """        val = int(n)
        max_m = val.bit_length() - 1
        for m in range(max_m, 1, -1):
            lo, hi = 2, val - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                total = 1
                term = 1
                over = False
                for _ in range(m):
                    if term > (val - total) // mid:
                        over = True
                        break
                    term *= mid
                    total += term
                if not over and total == val:
                    return str(mid)
                if over:
                    hi = mid - 1
                else:
                    lo = mid + 1
        return str(val - 1)""",
        "java": """        long val = Long.parseLong(n);
        int maxM = 63 - Long.numberOfLeadingZeros(val);
        for (int m = maxM; m >= 2; m--) {
            long lo = 2, hi = val - 1;
            while (lo <= hi) {
                long mid = lo + ((hi - lo) >>> 1);
                long total = 1;
                long term = 1;
                boolean over = false;
                for (int i = 0; i < m; i++) {
                    if (term > (val - total) / mid) {
                        over = true;
                        break;
                    }
                    term *= mid;
                    total += term;
                }
                if (!over && total == val) {
                    return Long.toString(mid);
                }
                if (over) {
                    hi = mid - 1;
                } else {
                    lo = mid + 1;
                }
            }
        }
        return Long.toString(val - 1);""",
        "visible": [
            {"n": "13"},
            {"n": "4681"},
            {"n": "1000000000000000000"},
        ],
        "hidden": [
            {"n": "3"},
            {"n": "4"},
            {"n": "7"},
            {"n": "15"},
            {"n": "31"},
            {"n": "2251799813685247"},
            {"n": "14919921443713777"},
            {"n": "727004545306745403"},
            {"n": "999999999999999999"},
        ],
    },
]


def main() -> None:
    expected_prefixes = list(range(11, 41))
    actual_prefixes = [int(p["slug"].split("-", 1)[0]) for p in TASKS]
    assert actual_prefixes == expected_prefixes, f"Prefix mismatch: {actual_prefixes}"

    existing_slugs: dict[str, Path] = {}
    existing_titles: dict[str, Path] = {}
    for p in (ROOT / "problems").rglob("problem.json"):
        m = re.match(r"^(\d{2,3})-(.+)$", p.parent.name)
        if m:
            existing_slugs[m.group(2)] = p.parent
        meta = json.loads(p.read_text(encoding="utf-8"))
        existing_titles[meta["title"].lower()] = p.parent

    seen_new_slugs: set[str] = set()
    seen_new_titles: set[str] = set()

    for p in TASKS:
        assert p["subtopic"] in ALLOWED_SUBTOPICS, f"Bad subtopic: {p['subtopic']}"
        assert all(c in ALLOWED_COMPANIES for c in p["companies"]), f"Bad company: {p['companies']}"
        assert len(p["desc"].strip()) >= 60, f"Short description: {p['slug']}"
        assert len(p["hints"]) == 2, f"Expected 2 hints: {p['slug']}"
        assert len(p["visible"]) == 3, f"Expected 3 visible tests: {p['slug']}"
        assert len(p["hidden"]) == 9, f"Expected 9 hidden tests: {p['slug']}"
        assert len(p["explanations"]) == 3, f"Expected 3 explanations: {p['slug']}"

        slug_only = p["slug"].split("-", 1)[1]
        folder = BASE / p["slug"]

        assert slug_only not in seen_new_slugs, f"Duplicate slug in batch: {slug_only}"
        assert p["title"].lower() not in seen_new_titles, f"Duplicate title in batch: {p['title']}"
        seen_new_slugs.add(slug_only)
        seen_new_titles.add(p["title"].lower())

        if slug_only in existing_slugs and existing_slugs[slug_only] != folder:
            raise AssertionError(f"Global duplicate slug '{slug_only}' already in {existing_slugs[slug_only]}")
        if p["title"].lower() in existing_titles and existing_titles[p["title"].lower()] != folder:
            raise AssertionError(
                f"Global duplicate title '{p['title']}' already in {existing_titles[p['title'].lower()]}"
            )

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

    print(f"Generated {len(TASKS)} bit-manipulation problems (11-40) cleanly.")


if __name__ == "__main__":
    main()
