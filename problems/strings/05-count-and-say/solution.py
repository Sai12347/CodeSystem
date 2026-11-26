class Solution:
    def countAndSay(self, n: int) -> str:
        cur = "1"
        for _ in range(n - 1):
            parts = []
            i = 0
            m = len(cur)
            while i < m:
                j = i + 1
                while j < m and cur[j] == cur[i]:
                    j += 1
                parts.append(str(j - i))
                parts.append(cur[i])
                i = j
            cur = "".join(parts)
        return cur
