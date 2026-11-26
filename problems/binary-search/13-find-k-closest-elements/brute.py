class Solution:
    def findClosestElements(self, arr: List[int], k: int, x: int) -> List[int]:
        chosen = sorted(arr, key=lambda v: (abs(v - x), v))[:k]
        chosen.sort()
        return chosen
