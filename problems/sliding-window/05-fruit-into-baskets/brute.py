class Solution:
    def totalFruit(self, fruits: List[int]) -> int:
        n = len(fruits)
        best = 0
        for i in range(n):
            if n - i <= best:
                break
            seen = set()
            j = i
            while j < n:
                seen.add(fruits[j])
                if len(seen) > 2:
                    break
                j += 1
            if j - i > best:
                best = j - i
        return best
