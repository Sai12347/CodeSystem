class Solution:
    def equationsPossible(self, equations: List[str]) -> bool:
        adj = [[] for _ in range(26)]
        for eq in equations:
            if eq[1] == "=":
                u = ord(eq[0]) - 97
                v = ord(eq[3]) - 97
                adj[u].append(v)
                adj[v].append(u)

        comp = [-1] * 26
        cid = 0
        for i in range(26):
            if comp[i] == -1:
                q = deque([i])
                comp[i] = cid
                while q:
                    cur = q.popleft()
                    for nxt in adj[cur]:
                        if comp[nxt] == -1:
                            comp[nxt] = cid
                            q.append(nxt)
                cid += 1

        for eq in equations:
            if eq[1] == "!":
                if comp[ord(eq[0]) - 97] == comp[ord(eq[3]) - 97]:
                    return False
        return True
