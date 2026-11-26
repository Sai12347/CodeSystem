class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        candidates.sort()
        res: List[List[int]] = []
        path: List[int] = []
        n = len(candidates)

        def dfs(start: int, rem: int) -> None:
            if rem == 0:
                res.append(path.copy())
                return
            for i in range(start, n):
                val = candidates[i]
                if val > rem:
                    break
                path.append(val)
                dfs(i, rem - val)
                path.pop()

        dfs(0, target)
        return res
