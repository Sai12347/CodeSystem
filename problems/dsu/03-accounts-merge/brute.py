class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        adj = defaultdict(set)
        owner = {}
        for acc in accounts:
            name = acc[0]
            first = acc[1]
            owner[first] = name
            adj[first]
            for email in acc[2:]:
                owner[email] = name
                adj[first].add(email)
                adj[email].add(first)

        visited = set()
        res = []
        for email in owner:
            if email in visited:
                continue
            comp = []
            q = deque([email])
            visited.add(email)
            while q:
                cur = q.popleft()
                comp.append(cur)
                for nxt in adj[cur]:
                    if nxt not in visited:
                        visited.add(nxt)
                        q.append(nxt)
            comp.sort()
            res.append([owner[email]] + comp)
        return res
