class Solution:
    def isBipartite(self, graph: List[List[int]]) -> bool:
        n = len(graph)
        color = [0] * n

        for start in range(n):
            if color[start] != 0:
                continue
            color[start] = 1
            queue = deque([start])
            while queue:
                u = queue.popleft()
                next_color = -color[u]
                for v in graph[u]:
                    if color[v] == 0:
                        color[v] = next_color
                        queue.append(v)
                    elif color[v] != next_color:
                        return False
        return True
