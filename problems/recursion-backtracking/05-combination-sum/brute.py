class Solution:
    def combinationSum(self, candidates: List[int], target: int) -> List[List[int]]:
        dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
        dp[0] = [[]]
        for c in sorted(candidates):
            for s in range(c, target + 1):
                for comb in dp[s - c]:
                    dp[s].append(comb + [c])
        return dp[target]
