class Solution:
    def maximumHappiness(self, happiness: List[int], k: int) -> int:
        total = 0
        for i, x in enumerate(sorted(happiness, reverse=True)[:k]): total += max(0, x - i)
        return total
