class Solution:
    def minCostToBalance(self, s: str, openCost: List[int], closeCost: List[int]) -> int:
        import heapq
        n = len(s)
        if n % 2 == 1:
            return -1
        bal = 0
        cost = 0
        pq = []
        for i, ch in enumerate(s):
            if ch == '(':
                bal += 1
            elif ch == ')':
                bal -= 1
            else:
                bal -= 1
                cost += closeCost[i]
                heapq.heappush(pq, openCost[i] - closeCost[i])
            while bal < 0:
                if not pq:
                    return -1
                cost += heapq.heappop(pq)
                bal += 2
        return cost if bal == 0 else -1
