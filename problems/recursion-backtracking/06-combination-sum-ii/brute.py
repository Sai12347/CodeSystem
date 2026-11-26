class Solution:
    def combinationSum2(self, candidates: List[int], target: int) -> List[List[int]]:
        freq = Counter(candidates)
        dp: List[List[List[int]]] = [[] for _ in range(target + 1)]
        dp[0] = [[]]
        for val in sorted(freq):
            cnt = freq[val]
            next_dp = [list(lst) for lst in dp]
            for s in range(target + 1):
                if not dp[s]:
                    continue
                for k in range(1, cnt + 1):
                    ns = s + k * val
                    if ns > target:
                        break
                    add = [val] * k
                    for comb in dp[s]:
                        next_dp[ns].append(comb + add)
            dp = next_dp
        return dp[target]
