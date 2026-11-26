class Solution:
    def fourSum(self, nums: List[int], target: int) -> List[List[int]]:
        n = len(nums)
        arr = sorted(nums)
        res = set()
        for i in range(n - 3):
            for j in range(i + 1, n - 2):
                seen = set()
                rem = target - arr[i] - arr[j]
                for k in range(j + 1, n):
                    need = rem - arr[k]
                    if need in seen:
                        res.add((arr[i], arr[j], need, arr[k]))
                    seen.add(arr[k])
        return [list(q) for q in sorted(res)]
