from collections import Counter
import heapq
import solution


def _expected_k_sums(nums1, nums2, k):
    target = min(k, len(nums1) * len(nums2))
    heap = [(nums1[i] + nums2[0], i, 0) for i in range(min(len(nums1), target))]
    heapq.heapify(heap)
    sums = []
    while heap and len(sums) < target:
        s, i, j = heapq.heappop(heap)
        sums.append(s)
        if j + 1 < len(nums2):
            heapq.heappush(heap, (nums1[i] + nums2[j + 1], i, j + 1))
    return sums


def run(inp):
    nums1 = list(inp["nums1"])
    nums2 = list(inp["nums2"])
    k = inp["k"]
    res = solution.Solution().kSmallestPairs(list(nums1), list(nums2), k)
    target = min(k, len(nums1) * len(nums2))
    if not isinstance(res, list):
        return f"Expected list, got {type(res).__name__}"
    if len(res) != target:
        return f"Expected {target} pairs, got {len(res)}"
    cnt1 = Counter(nums1)
    cnt2 = Counter(nums2)
    pair_cnt = Counter()
    got_sums = []
    for idx, p in enumerate(res):
        if not isinstance(p, (list, tuple)) or len(p) != 2:
            return f"Element at index {idx} is not a 2-element pair"
        u, v = p[0], p[1]
        if isinstance(u, bool) or isinstance(v, bool) or not isinstance(u, int) or not isinstance(v, int):
            return f"Pair at index {idx} must contain two integers"
        if cnt1[u] == 0 or cnt2[v] == 0:
            return f"Pair [{u}, {v}] uses values not present in nums1/nums2"
        pair_cnt[(u, v)] += 1
        if pair_cnt[(u, v)] > cnt1[u] * cnt2[v]:
            return f"Pair [{u}, {v}] appears more times than distinct index pairs allow"
        got_sums.append(u + v)
    got_sums.sort()
    exp_sums = _expected_k_sums(nums1, nums2, k)
    if got_sums != exp_sums:
        return f"Returned pair sums {got_sums[:10]} do not match the k smallest sums {exp_sums[:10]}"
    return True
