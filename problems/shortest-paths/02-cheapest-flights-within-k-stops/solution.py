class Solution:
    def findCheapestPrice(
        self, n: int, flights: List[List[int]], src: int, dst: int, k: int
    ) -> int:
        inf = 10**18
        dist = [inf] * n
        dist[src] = 0

        for _ in range(k + 1):
            nxt = dist[:]
            updated = False
            for u, v, price in flights:
                if dist[u] != inf and dist[u] + price < nxt[v]:
                    nxt[v] = dist[u] + price
                    updated = True
            dist = nxt
            if not updated:
                break

        return -1 if dist[dst] == inf else dist[dst]
