class Solution:
    def closestToTarget(self, nums: List[int], target: int) -> int:
        ans = abs(nums[0] - target)
        cur = set()
        for x in nums:
            nxt = {x}
            for v in cur:
                nxt.add(v & x)
            for v in nxt:
                d = abs(v - target)
                if d < ans:
                    ans = d
            cur = nxt
            if ans == 0:
                return 0
        return ans
