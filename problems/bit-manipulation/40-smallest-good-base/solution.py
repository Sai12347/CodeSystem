class Solution:
    def smallestGoodBase(self, n: str) -> str:
        val = int(n)
        max_m = val.bit_length() - 1
        for m in range(max_m, 1, -1):
            lo, hi = 2, val - 1
            while lo <= hi:
                mid = (lo + hi) // 2
                total = 1
                term = 1
                over = False
                for _ in range(m):
                    if term > (val - total) // mid:
                        over = True
                        break
                    term *= mid
                    total += term
                if not over and total == val:
                    return str(mid)
                if over:
                    hi = mid - 1
                else:
                    lo = mid + 1
        return str(val - 1)
