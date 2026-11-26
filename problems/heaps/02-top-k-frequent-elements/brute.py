class Solution:
    def topKFrequent(self, nums: List[int], k: int) -> List[int]:
        counts = Counter(nums)
        ordered = sorted(counts.keys(), key=lambda x: -counts[x])
        return ordered[:k]
