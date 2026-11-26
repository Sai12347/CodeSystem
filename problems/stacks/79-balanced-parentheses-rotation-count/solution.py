class Solution:
    def countBalancedRotations(self, s: str) -> int:
        bal = 0
        min_bal = 0
        min_cnt = 0
        for ch in s:
            if bal < min_bal:
                min_bal = bal
                min_cnt = 1
            elif bal == min_bal:
                min_cnt += 1
            bal += 1 if ch == '(' else -1
        return min_cnt if bal == 0 else 0
