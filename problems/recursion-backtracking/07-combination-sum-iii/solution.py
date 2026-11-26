class Solution:
    def combinationSum3(self, k: int, n: int) -> List[List[int]]:
        res: List[List[int]] = []
        path: List[int] = []

        def dfs(start: int, need: int, rem: int) -> None:
            if need == 0:
                if rem == 0:
                    res.append(path.copy())
                return
            max_start = 10 - need
            for num in range(start, max_start + 1):
                # Smallest possible sum choosing `need` numbers starting from `num`
                min_sum = need * (2 * num + need - 1) // 2
                if min_sum > rem:
                    break
                # Largest possible sum choosing `num` plus `need - 1` largest digits
                max_sum = num + (need - 1) * (20 - need) // 2
                if max_sum < rem:
                    continue
                path.append(num)
                dfs(num + 1, need - 1, rem - num)
                path.pop()

        dfs(1, k, n)
        return res
