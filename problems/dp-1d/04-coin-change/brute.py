class Solution:
    def coinChange(self, coins: List[int], amount: int) -> int:
        # Independent BFS shortest-path formulation from sum 0 to amount
        if amount == 0:
            return 0
        usable = sorted({c for c in coins if c <= amount})
        if not usable:
            return -1

        visited = [False] * (amount + 1)
        visited[0] = True
        queue = deque([(0, 0)])
        while queue:
            curr, steps = queue.popleft()
            next_steps = steps + 1
            for c in usable:
                nxt = curr + c
                if nxt == amount:
                    return next_steps
                if nxt > amount:
                    break
                if not visited[nxt]:
                    visited[nxt] = True
                    queue.append((nxt, next_steps))
        return -1
