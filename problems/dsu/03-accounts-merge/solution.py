class Solution:
    def accountsMerge(self, accounts: List[List[str]]) -> List[List[str]]:
        n = len(accounts)
        parent = list(range(n))
        rank = [0] * n

        def find(x: int) -> int:
            while parent[x] != x:
                parent[x] = parent[parent[x]]
                x = parent[x]
            return x

        def union(a: int, b: int) -> None:
            ra, rb = find(a), find(b)
            if ra == rb:
                return
            if rank[ra] < rank[rb]:
                ra, rb = rb, ra
            parent[rb] = ra
            if rank[ra] == rank[rb]:
                rank[ra] += 1

        email_to_acc = {}
        for i, acc in enumerate(accounts):
            for email in acc[1:]:
                if email in email_to_acc:
                    union(i, email_to_acc[email])
                else:
                    email_to_acc[email] = i

        groups = defaultdict(list)
        for email, acc_idx in email_to_acc.items():
            groups[find(acc_idx)].append(email)

        res = []
        for root, emails in groups.items():
            emails.sort()
            res.append([accounts[root][0]] + emails)
        return res
