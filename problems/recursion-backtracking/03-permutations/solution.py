class Solution:
    def permute(self, nums: List[int]) -> List[List[int]]:
        n = len(nums)
        res: List[List[int]] = []
        path: List[int] = []
        used = [False] * n

        def dfs() -> None:
            if len(path) == n:
                res.append(path.copy())
                return
            for i in range(n):
                if not used[i]:
                    used[i] = True
                    path.append(nums[i])
                    dfs()
                    path.pop()
                    used[i] = False

        dfs()
        return res
