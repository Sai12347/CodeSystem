class Solution:
    def isAlienSorted(self, words: List[str], order: str) -> bool:
        mapped = [tuple(order.index(ch) for ch in w) for w in words]
        return mapped == sorted(mapped)
