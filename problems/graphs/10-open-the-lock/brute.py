class Solution:
    def openLock(self, deadends: List[str], target: str) -> int:
        # Independent unidirectional BFS over integer states 0..9999
        blocked = [False] * 10000
        for s in deadends:
            blocked[int(s)] = True
        if blocked[0]:
            return -1
        goal = int(target)
        if goal == 0:
            return 0

        dist = [-1] * 10000
        dist[0] = 0
        q = deque([0])
        powers = (1, 10, 100, 1000)

        while q:
            u = q.popleft()
            du = dist[u]
            for p in powers:
                digit = (u // p) % 10
                base = u - digit * p
                for nd in ((digit + 1) % 10, (digit + 9) % 10):
                    v = base + nd * p
                    if not blocked[v] and dist[v] == -1:
                        if v == goal:
                            return du + 1
                        dist[v] = du + 1
                        q.append(v)
        return -1
