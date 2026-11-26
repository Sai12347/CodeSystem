class Solution:
    def smallestRange(self, nums: List[List[int]]) -> List[int]:
        k = len(nums)
        merged = []
        for i, row in enumerate(nums):
            for v in row:
                merged.append((v, i))
        merged.sort()
        counts = [0] * k
        covered = 0
        left = 0
        best_l, best_r = -10**9, 10**9
        for right, (val_r, idx_r) in enumerate(merged):
            if counts[idx_r] == 0:
                covered += 1
            counts[idx_r] += 1
            while covered == k:
                val_l, idx_l = merged[left]
                if val_r - val_l < best_r - best_l or (
                    val_r - val_l == best_r - best_l and val_l < best_l
                ):
                    best_l, best_r = val_l, val_r
                counts[idx_l] -= 1
                if counts[idx_l] == 0:
                    covered -= 1
                left += 1
        return [best_l, best_r]
