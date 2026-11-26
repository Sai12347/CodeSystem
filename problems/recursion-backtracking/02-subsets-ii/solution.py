class Solution:
    def subsetsWithDup(self, nums: List[int]) -> List[List[int]]:
        nums.sort()
        res: List[List[int]] = []
        path: List[int] = []
        n = len(nums)

        def dfs(start: int) -> None:
            res.append(path.copy())
            for i in range(start, n):
                if i > start and nums[i] == nums[i - 1]:
                    continue
                path.append(nums[i])
                dfs(i + 1)
                path.pop()

        dfs(0)
        return res
