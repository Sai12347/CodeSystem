class Solution:
    def minOperationsToFormTarget(self, nums: List[int], target: int) -> int:
        if sum(nums) < target:
            return -1
        cnt = [0] * 32
        for x in nums:
            cnt[x.bit_length() - 1] += 1
        ops = 0
        for b in range(31):
            if (target >> b) & 1:
                if cnt[b] > 0:
                    cnt[b] -= 1
                else:
                    j = b + 1
                    while cnt[j] == 0:
                        j += 1
                    cnt[j] -= 1
                    for m in range(b, j):
                        cnt[m] += 1
                    ops += j - b
            cnt[b + 1] += cnt[b] // 2
        return ops
