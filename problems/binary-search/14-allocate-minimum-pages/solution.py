class Solution:
    def allocatePages(self, pages: List[int], students: int) -> int:
        if students > len(pages):
            return -1
        left, right = max(pages), sum(pages)
        while left < right:
            mid = left + (right - left) // 2
            needed = 1
            cur = 0
            for p in pages:
                if cur + p > mid:
                    needed += 1
                    cur = p
                else:
                    cur += p
            if needed <= students:
                right = mid
            else:
                left = mid + 1
        return left
