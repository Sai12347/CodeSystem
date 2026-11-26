class Solution:
    def kSmallestPairs(self, nums1: List[int], nums2: List[int], k: int) -> List[List[int]]:
        a = nums1[:k]
        b = nums2[:k]
        pairs = [[u, v] for u in a for v in b]
        pairs.sort(key=lambda p: p[0] + p[1])
        return pairs[:k]
