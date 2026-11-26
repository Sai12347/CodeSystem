from itertools import permutations


class Solution:
    def largestNumber(self, nums: List[int]) -> str:
        strs = [str(x) for x in nums]
        if len(strs) <= 7:
            best = max("".join(p) for p in permutations(strs))
            return "0" if best[0] == "0" else best
        # Pairwise swap bubble sort by numeric concatenation
        n = len(strs)
        for i in range(n):
            for j in range(0, n - 1 - i):
                if int(strs[j] + strs[j + 1]) < int(strs[j + 1] + strs[j]):
                    strs[j], strs[j + 1] = strs[j + 1], strs[j]
        return "0" if strs[0] == "0" else "".join(strs)
