class Solution:
    def xorQueries(self, arr: List[int], queries: List[List[int]]) -> List[int]:
        pref = [0] * (len(arr) + 1)
        for i, v in enumerate(arr):
            pref[i + 1] = pref[i] ^ v
        return [pref[r + 1] ^ pref[l] for l, r in queries]
